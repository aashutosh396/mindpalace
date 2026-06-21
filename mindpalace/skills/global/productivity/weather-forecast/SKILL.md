---
name: weather-forecast
description: "Use when the user asks about weather, temperature, forecast, rain, or conditions for any city — current, hourly, multi-day via wttr.in. No API key or install needed."
version: 1.0.0
license: MIT
tags: [weather, forecast, temperature, conditions, wttr, assistant, productivity]
source: https://github.com/daxaur/openpaw/tree/main/skills/c-weather
derived_from: awesomeclaude
---

# Weather Forecast

Get weather via `curl` and wttr.in — no API key, nothing to install.

## When to use
Any question about current weather, forecast, temperature, or conditions for a
location.

## Commands

```bash
curl -s "wttr.in?format=3"                # Current, auto-location, one line
curl -s "wttr.in/London"                  # Specific city
curl -s "wttr.in/New+York"                # Multi-word city
curl -s "wttr.in/Berlin?1"                # Today only
curl -s "wttr.in"                         # Full forecast (today + 2 days)
curl -s "wttr.in/London?format=j1"        # JSON for parsing
curl -s "wttr.in/Moon"                    # Moon phase
curl -s "wttr.in/Paris?format=%l:+%c+%t+(feels+like+%f)+%h+%w"   # Custom
```

## Format codes
`%c` icon · `%t` temp · `%f` feels-like · `%h` humidity · `%w` wind ·
`%p` precip · `%l` location · `%S` sunrise · `%s` sunset

## Guidelines
- Default to the user's known city (check memory) if none given.
- Use `format=3` for quick checks, full output for detailed forecasts.
- Always include temperature and conditions; mention "feels like" when it differs.
