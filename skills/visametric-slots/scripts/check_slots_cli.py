#!/usr/bin/env python3
"""Visametric RU: captcha → step 1 → free dates as JSON (no booking)."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_slots import check_slots, load_config  # noqa: E402


async def run(
    config_path: Path,
    *,
    headed: bool | None,
    city: str | None,
    visiting_country: str | None,
    office_type: str | None,
    all_types: bool,
) -> int:
    config = load_config(config_path)
    settings = config.setdefault("settings", {})
    if headed is not None:
        settings["headed"] = headed

    artifacts = Path(settings.get("artifacts_dir", "artifacts"))
    if not artifacts.is_absolute():
        artifacts = Path.cwd() / artifacts
    artifacts.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(artifacts / "run.log", encoding="utf-8"),
        ],
    )
    log = logging.getLogger("visametric-slots")

    summary = await check_slots(
        config=config,
        city=city,
        visiting_country=visiting_country,
        office_type=office_type,
        headed=bool(settings.get("headed", False)),
        all_types=all_types,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary.get("error"):
        log.error("%s", summary["error"])
        return 2
    log.info(
        "Found %s date(s). No appointment was booked.",
        summary.get("available_date_count", 0),
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visametric RU: captcha → step 1 → show free slots (no booking)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=SKILL_ROOT / "config.example.yaml",
        help="Path to config YAML (default: skill config.example.yaml)",
    )
    parser.add_argument("--city", type=str, default=None, help="City, e.g. Москва")
    parser.add_argument(
        "--visiting-country",
        type=str,
        default=None,
        help="Destination country, e.g. Германия",
    )
    parser.add_argument(
        "--office-type",
        type=str,
        choices=["NORMAL", "PRIME", "VIP"],
        default=None,
        help="Check only this office type (default: all types)",
    )
    parser.add_argument(
        "--all-types",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Check NORMAL+PRIME+VIP (default: true; ignored if --office-type set alone)",
    )
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument("--headless", action="store_true", help="Force headless")
    args = parser.parse_args()

    headed: bool | None
    if args.headed:
        headed = True
    elif args.headless:
        headed = False
    else:
        headed = None

    all_types = False if args.office_type else bool(args.all_types)

    raise SystemExit(
        asyncio.run(
            run(
                args.config,
                headed=headed,
                city=args.city,
                visiting_country=args.visiting_country,
                office_type=args.office_type,
                all_types=all_types,
            )
        )
    )


if __name__ == "__main__":
    main()
