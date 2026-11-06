"""Client-side account/AppKey exchange; credentials exist only for this invocation."""

from __future__ import annotations

import asyncio
import json

import httpx

from config.order_design import OrderDesignSettings
from .localization import localize_text


MAX_AUTH_RESPONSE_BYTES = 64 * 1024


class AuthenticationError(ValueError):
    """Fixed public error; never include a response, account, key, token or URL."""


async def exchange_appkey(
    settings: OrderDesignSettings, username: str, appkey: str,
    *, transport: httpx.AsyncBaseTransport | None = None, language: str = "zh",
) -> str:
    if not settings.base_url:
        raise AuthenticationError(localize_text("请先配置 RUSHDATA_BASE_URL；尚未请求登录或业务接口。", language))
    if (not isinstance(username, str) or not 1 <= len(username.strip()) <= 254
            or any(ord(char) < 32 for char in username)
            or not isinstance(appkey, str) or not 1 <= len(appkey) <= 8192
            or any(ord(char) < 33 or ord(char) > 126 for char in appkey)):
        raise AuthenticationError(localize_text("Biointron Account 或 App Key 格式无效，请重新填写。", language))
    try:
        async with asyncio.timeout(settings.timeout), httpx.AsyncClient(
            timeout=settings.timeout, follow_redirects=False, trust_env=False, transport=transport,
        ) as client:
            async with client.stream("POST", settings.base_url.rstrip("/") + "/customer/getAccessToken",
                                     json={"username": username.strip(), "appkey": appkey}) as response:
                if not 200 <= response.status_code < 300:
                    raise AuthenticationError(localize_text("Biointron Account / App Key 换取业务令牌失败；未继续请求业务接口。", language))
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_AUTH_RESPONSE_BYTES:
                        raise AuthenticationError(localize_text("登录响应超过大小限制；未继续请求业务接口。", language))
        payload = json.loads(body)
        if (not isinstance(payload, dict) or type(payload.get("code")) is not int or payload["code"] != 200
                or payload.get("success") is not True or not isinstance(payload.get("result"), dict)):
            raise AuthenticationError(localize_text("登录响应未确认成功；请核对 Biointron Account 和 App Key，未继续请求业务接口。", language))
        token = payload["result"].get("token")
        if (not isinstance(token, str) or not 1 <= len(token) <= 8192
                or any(ord(char) < 33 or ord(char) > 126 for char in token)):
            raise AuthenticationError(localize_text("登录响应缺少有效业务令牌；未继续请求业务接口。", language))
        return token
    except AuthenticationError:
        raise
    except (httpx.HTTPError, httpx.InvalidURL, TimeoutError, ValueError, UnicodeError):
        raise AuthenticationError(localize_text("登录请求失败、超时或响应格式无效；未重试，也未继续请求业务接口。", language)) from None
