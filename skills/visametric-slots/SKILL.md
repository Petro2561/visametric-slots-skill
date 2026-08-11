---
name: visametric-slots
description: >-
  Checks free Visametric RU appointment dates (Germany Schengen etc.) via
  Playwright: solves captcha, selects city/office, returns JSON dates without
  booking. Use when the user asks about Visametric slots, visa appointment
  availability, or free dates in Moscow/SPb/Yekaterinburg/Novosibirsk.
license: MIT
compatibility: Requires Python 3.10+, pip, and Playwright Chromium.
---

# Visametric slots

Check free appointment dates on Visametric RU. **Never book** an appointment and
**never fill personal/passport data**.

Skill root = this directory (contains `SKILL.md`, `scripts/`, `models/`).

## Setup (first use)

From the skill root:

```bash
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Reuse a venv if present; otherwise create one.

## Workflow

1. Confirm with the user (defaults in brackets):
   - city (`Москва` | `Санкт-Петербург` | `Екатеринбург` | `Новосибирск`)
   - visiting country (`Германия`)
   - office types: all NORMAL+PRIME+VIP, or one of them
2. Run the CLI from the skill root (JSON on stdout; logs on stderr):

```bash
python3 scripts/check_slots_cli.py --city "Москва"
```

Useful flags:

```bash
python3 scripts/check_slots_cli.py --city "Санкт-Петербург" --office-type NORMAL
python3 scripts/check_slots_cli.py --city "Москва" --visiting-country "Германия" --headed
python3 scripts/check_slots_cli.py --config /path/to/config.yaml
```

3. Parse stdout JSON and report dates to the user. State clearly that **no appointment was booked**.
4. On captcha failure (`error` field / exit code 2): retry once, or re-run with `--headed` for debugging. Do not invent dates.

## Output shape

```json
{
  "available_date_count": 2,
  "dates": ["15-08-2026", "22-08-2026"],
  "by_type": {
    "NORMAL": {"dates": ["15-08-2026"], "control": "0", "error": null},
    "PRIME": {"dates": ["22-08-2026"], "control": "0", "error": null},
    "VIP": {"dates": [], "control": "1", "error": null}
  },
  "city": "Москва"
}
```

Dates are `DD-MM-YYYY`. Artifacts (screenshots, `slots.json`, `run.log`) go to `./artifacts` in the current working directory.

## Rules

- Do not submit the appointment form beyond step 1 availability.
- Do not store or request passport/email/phone for this skill.
- Site ToS may restrict automation; use for personal availability checks at the user's risk.
