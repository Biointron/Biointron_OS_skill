"""Run an explicit live RushData check; no retries and no implicit writes."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from config.order_design import OrderDesignSettings
from skill.order_design.scripts.client import RushDataClient, RushDataError


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="RushData integration check: preflight is read-only; other modes write to the business system.")
    result.add_argument("--mode", choices=("preflight", "design", "submit", "full"), default="preflight")
    result.add_argument("--request", type=Path, help="Design request JSON containing customer-provided data")
    result.add_argument("--file", type=Path, help="Customer-provided .xlsx design workbook")
    result.add_argument("--orders", nargs="+", help="Order numbers explicitly selected for submit mode")
    result.add_argument("--report", type=Path, help="Optional local JSON result file; excludes tokens and design contents")
    return result


def outcome(result: dict) -> dict:
    """Keep reports to identity/status; upstream cart and submission bodies can vary."""
    return {key: result[key] for key in (
        "status", "orderNo", "rushDataServiceId", "orderNos", "experimentSubmissionVerified",
    ) if key in result}


async def run(args: argparse.Namespace) -> dict:
    settings = OrderDesignSettings.from_env()
    settings.require_connection()
    client = RushDataClient(settings)
    if args.mode == "preflight":
        await client.preflight()
        # Only persist the readiness summary, not the customer's company data/catalog.
        return {"stage": "preflight", "status": "passed", "full_chain_verified": False}
    if args.mode == "submit":
        if not args.orders:
            raise ValueError("submit mode requires --orders to identify the selected orders.")
        return {"stage": "submit", "result": outcome(await client.submit(args.orders)), "full_chain_verified": False}
    if args.request is None or args.file is None:
        raise ValueError("design/full modes require --request and --file.")
    if args.file.suffix.lower() != ".xlsx" or args.file.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("The design file must be an .xlsx workbook no larger than 10 MiB.")
    data = json.loads(args.request.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("The request file must contain a JSON object.")
    designed = await client.design_to_cart(data, args.file.read_bytes(), args.file.name)
    if args.mode == "design":
        return {"stage": "design", "result": outcome(designed), "full_chain_verified": False}
    order_no = designed.get("orderNo")
    if not order_no:
        raise RushDataError("The design result is missing orderNo; submission has stopped.", details=designed)
    try:
        submitted = await client.submit([order_no])
    except RushDataError as error:
        error.details = {**error.details, "orderNo": order_no,
                         "rushDataServiceId": designed.get("rushDataServiceId")}
        raise
    return {"stage": "full", "design": outcome(designed), "submission": outcome(submitted), "full_chain_verified": True}


def main() -> int:
    args = parser().parse_args()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    report = {"mode": args.mode, "tested_at_utc": datetime.now(timezone.utc).isoformat(), "live": True}
    try:
        report.update(asyncio.run(run(args)))
        exit_code = 0
    except RushDataError as error:
        report.update(status="blocked_or_failed", full_chain_verified=False,
                      message=str(error), details=error.details)
        exit_code = 1
    except (ValueError, OSError) as error:
        # Do not print source contents or secrets from malformed input files.
        message = str(error) if not isinstance(error, (json.JSONDecodeError, OSError)) else "The input file could not be read or parsed."
        report.update(status="blocked", full_chain_verified=False, message=message)
        exit_code = 1
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
