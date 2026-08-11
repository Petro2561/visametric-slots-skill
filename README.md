# Visametric slots — проверка свободных дат на запись на подачу Шенген в Германию

Скилл для AI-агентов (Codex, Claude, Cursor), который **смотрит, есть ли свободные даты** записи на визу на сайте [Visametric RU](https://ru-appointment.visametric.com/ru).

Типичный сценарий: «есть ли слоты в Москве на Германию?» — агент проходит капчу, выбирает город и офис и возвращает список дат в JSON.

**Запись на приём не создаётся.** Паспортные и личные данные не нужны и не запрашиваются.

## Что умеет

- Проверяет свободные даты в городах: Москва, Санкт-Петербург, Екатеринбург, Новосибирск
- Учитывает типы офисов: NORMAL, PRIME, VIP
- Решает капчу (Playwright + OCR)
- Отдаёт результат в JSON — удобно и человеку, и агенту

## Чего не делает

- Не бронирует слот
- Не заполняет анкету и паспортные данные
- Не обходит оплату и следующие шаги записи

## Важно

Инструмент для личной проверки доступности. Автоматизация сайта может противоречить правилам Visametric — используйте на свой риск.

## Установка

### Codex

```text
$skill-installer install https://github.com/Petro2561/visametric-slots-skill/tree/main/skills/visametric-slots
```

Или:

```bash
python3 path/to/skill-installer/scripts/install-skill-from-github.py \
  --repo Petro2561/visametric-slots-skill \
  --path skills/visametric-slots
```

После установки перезапустите Codex.

### Claude

Скопируйте `skills/visametric-slots` в `~/.claude/skills/visametric-slots`.

### Cursor

Скопируйте `skills/visametric-slots` в `~/.cursor/skills/visametric-slots` (или в `.cursor/skills/` проекта).

## Первый запуск

Из каталога скилла:

```bash
cd skills/visametric-slots
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
```

Нужны Python 3.10+, pip и Chromium для Playwright.

## Пример CLI

```bash
cd skills/visametric-slots
python3 scripts/check_slots_cli.py --city "Москва"
```

Полезные флаги:

```bash
python3 scripts/check_slots_cli.py --city "Санкт-Петербург" --office-type NORMAL
python3 scripts/check_slots_cli.py --city "Москва" --visiting-country "Германия" --headed
```

В stdout — JSON с полями `dates` и `by_type`. Код выхода `2` — ошибка капчи или проверки.

Пример ответа:

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

Даты в формате `ДД-ММ-ГГГГ`. Скриншоты и логи пишутся в `./artifacts`.

## Структура

```
skills/visametric-slots/
  SKILL.md              # инструкции для агента
  scripts/              # Playwright + OCR
  models/digit_mlp.joblib
  config.example.yaml
  requirements.txt
```

Совместим со спецификацией Agent Skills ([agentskills.io](https://agentskills.io/specification)).

## Лицензия

MIT — см. [LICENSE](LICENSE).
