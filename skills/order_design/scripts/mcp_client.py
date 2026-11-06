"""One MCP tool call per process; JSON in/out, no retries or retained credentials."""

from __future__ import annotations

import asyncio
import json
import logging
import math
import os
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlsplit


def _failure(kind: str, stage: str, message: str, *, result: Any = None,
             exception: BaseException | None = None) -> dict[str, Any]:
    error = {"kind": kind, "stage": stage, "message": message}
    if exception is not None:
        # Exception messages may include request arguments, URLs or credentials.
        error["exception_type"] = type(exception).__name__
    return {"ok": False, "result": result, "error": error}


def decode_tool_result(response: Any) -> dict[str, Any]:
    """Accept SDK models and wire dictionaries without assuming content exists."""
    if hasattr(response, "model_dump"):
        response = response.model_dump(mode="json", by_alias=True)
    if not isinstance(response, dict):
        return _failure("protocol_error", "decode", "The MCP tool result is not an object.")
    is_error = response.get("isError", response.get("is_error", False))
    if not isinstance(is_error, bool):
        return _failure("protocol_error", "decode", "The MCP error flag is invalid.")
    result = response.get("structuredContent", response.get("structured_content"))
    content = response.get("content")
    if result is None and isinstance(content, list):
        for item in content:
            if not isinstance(item, dict) or item.get("type") != "text" or not isinstance(item.get("text"), str):
                continue
            try:
                result = json.loads(item["text"])
            except (ValueError, UnicodeError):
                continue
            if result is not None:
                break
    if is_error:
        # Keep structured needs_input/needs_credentials feedback and original tool text.
        return _failure("tool_error", "call_tool", "The MCP tool returned an error; inspect the result.",
                        result=result if result is not None else response)
    if result is None:
        return _failure("protocol_error", "decode", "The MCP tool returned no structured result or valid JSON text.")
    return {"ok": True, "result": result, "error": None}


def _redact(value: Any, secrets: tuple[str, ...]) -> Any:
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[redacted]")
    elif isinstance(value, list):
        value = [_redact(item, secrets) for item in value]
    elif isinstance(value, dict):
        value = {key: _redact(item, secrets) for key, item in value.items()}
    return value


async def call_mcp_tool(url: str, name: str, arguments: dict[str, Any], *,
                        timeout: float = 300.0) -> dict[str, Any]:
    """Use the current service token; arguments must explicitly carry customer credentials/language."""
    stage = "input"
    outcome = None
    try:
        if (not isinstance(url, str) or not isinstance(name, str) or not name.strip()
                or not isinstance(arguments, dict) or type(timeout) not in (int, float)
                or not math.isfinite(timeout) or timeout <= 0):
            return _failure("input_error", stage, "Supply url, name, arguments and a positive finite timeout.")
        endpoint = urlsplit(url)
        local_http = endpoint.scheme == "http" and endpoint.hostname in ("localhost", "127.0.0.1", "::1")
        if (not endpoint.hostname or not (endpoint.scheme == "https" or local_http)
                or endpoint.username is not None or endpoint.password is not None
                or endpoint.query or endpoint.fragment):
            return _failure("input_error", stage, "Use the configured HTTPS MCP endpoint without URL credentials or query parameters.")

        stage = "configuration"
        from dotenv import dotenv_values
        # Read the service credential without importing unrelated config into process state.
        service_token = os.getenv("MCP_ACCESS_TOKEN")
        if service_token is None:
            service_token = dotenv_values(Path(__file__).resolve().parents[3] / "config" / ".env").get("MCP_ACCESS_TOKEN") or ""
        if (not re.fullmatch(r"[A-Za-z0-9_.~-]{32,}", service_token)
                or service_token.lower().startswith(("replace", "change", "example"))):
            return _failure("configuration_error", stage, "The existing MCP_ACCESS_TOKEN is missing or invalid.")

        # The pinned MCP 2.3 SDK uses httpx2, independently of the business API's httpx.
        import httpx2
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
        from mcp.shared.exceptions import MCPError

        stage = "connect"
        async with asyncio.timeout(timeout):
            async with httpx2.AsyncClient(
                headers={"Authorization": "Bearer " + service_token}, timeout=timeout,
                follow_redirects=False, trust_env=False,
            ) as http_client:
                async with streamable_http_client(url, http_client=http_client) as (read, write):
                    async with ClientSession(read, write, read_timeout_seconds=timeout) as session:
                        stage = "initialize"
                        await session.initialize()
                        stage = "call_tool"
                        response = await session.call_tool(name, arguments, read_timeout_seconds=timeout)
                        stage = "decode"
                        decoded = decode_tool_result(response)
                        business_token = arguments.get("business_token")
                        outcome = _redact(decoded, (service_token, business_token if isinstance(business_token, str) else ""))
                        stage = "close"
        return outcome
    except Exception as exception:
        # AnyIO may wrap the actual transport failure in a task-group exception.
        while isinstance(exception, BaseExceptionGroup) and len(exception.exceptions) == 1:
            exception = exception.exceptions[0]
        if (isinstance(exception, TimeoutError)
                or stage in ("connect", "initialize", "call_tool", "close")
                and isinstance(exception, httpx2.TimeoutException)):
            kind, message = "timeout", "The MCP request timed out; no automatic retry was made."
        elif stage == "decode":
            kind, message = "protocol_error", "The MCP tool response could not be decoded."
        elif stage in ("input", "configuration"):
            kind, message = stage + "_error", "The MCP client could not complete this local stage."
        elif isinstance(exception, MCPError):
            kind, message = "protocol_error", "The MCP service returned a protocol error; no automatic retry was made."
        else:
            kind, message = "transport_error", "The MCP request failed; no automatic retry was made."
        failure = _failure(kind, stage, message, exception=exception)
        if stage not in ("input", "configuration") and isinstance(exception, MCPError):
            failure["error"]["rpc_code"] = exception.code
        elif stage not in ("input", "configuration") and isinstance(exception, httpx2.HTTPStatusError):
            failure["error"]["http_status"] = exception.response.status_code
        if outcome is not None:
            # A failed shutdown must not erase an already received tool result.
            outcome["cleanup_error"] = failure["error"]
            return outcome
        return failure


def main() -> int:
    # stdout is a single ASCII-safe JSON record even on a Windows code-page console.
    # SDK diagnostics can contain URLs or response bodies, so this process emits only our envelope.
    logging.disable(logging.CRITICAL)
    try:
        request = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
        if not isinstance(request, dict):
            raise ValueError("Expected an object")
        outcome = asyncio.run(call_mcp_tool(
            request.get("url"), request.get("name"), request.get("arguments"),
            timeout=request.get("timeout", 300.0),
        ))
    except Exception as exception:
        outcome = _failure("input_error", "input", "The request must be one UTF-8 JSON object on standard input.",
                           exception=exception)
    try:
        serialized = json.dumps(outcome, ensure_ascii=True, allow_nan=False)
    except (TypeError, ValueError) as exception:
        outcome = _failure("protocol_error", "decode", "The MCP tool result is not valid JSON.", exception=exception)
        serialized = json.dumps(outcome, ensure_ascii=True)
    sys.stdout.write(serialized + "\n")
    sys.stdout.flush()
    return 0 if outcome["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
