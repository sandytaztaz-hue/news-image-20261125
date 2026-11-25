# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sandytaztaz-hue/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sandytaztaz-hue/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page broadsheet summing up the world news of Wednesday 25 November 2026 in a single 1024x1024 image. Round 1 entry: 36 stories, 7 regions, one consequential lead: Shenzhou-24 lifts off with China's first foreign astronaut — a Pakistani payload specialist — plus the Flinders Island bushfire emergency, the Thanksgiving-eve US data pile, and Zelenskyy's confirmation that Ukraine hit a Russian ship. Cream paper with a red masthead band, one big drawn lead scene, three drawn second-row scenes, nine small drawn card scenes, an ALSO TODAY strip, a real-geography map, a UTC timeline, a stat strip and a DATE CHECK box naming the big stories that did not happen on Wednesday. The program draws every pixel itself with the Python standard library only — no image files, no network — and writes byte-identical output on every run.

SPDX-License-Identifier: MIT

## What is on the page

- Masthead: Wednesday 25 November 2026, THE WHOLE WORLD - ONE DAY, wires as of about 02:00 UTC
- The lead: Shenzhou-24 lifts off at 00:18 UTC from Jiuquan; Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali, 40, aboard; first Pakistani in orbit, first foreign astronaut on Tiangong (Xinhua / CMSA)
- Second row: Flinders Island bushfire emergency, "too late to leave" (Tas Fire Service); Thanksgiving-eve US data pile, GDP, PCE, jobless claims at 13:30 UTC (BEA / Labor Dept); Zelenskyy confirms Ukraine hit a Russian ship in the Gulf of Finland (confirmed)
- Twelve cards: Australia's October CPI, a warship sunk off Benghazi, the Riyadh tower hit, Houthis 60 km from Aden, 11 killed near Kyiv, Giuliani honoured, the CIA/ODNI breach, Huawei guilty, the EU-Balkans summit, the Africa summit in Accra, 47,000 women killed in 2025, the Swedish vote on the PM
- ALSO TODAY: briefs 16-36, from Germany's Q3 GDP final to the Dutch gas jump
- WHERE: a real-geography world map with numbered pins; HOW SURE: what CONFIRMED, OFFICIAL, REPORTED, SCHED and CLAIM mean; DATE CHECK: GTA 6, COP31, the 20 Nov Kyiv attack, Man Utd's 3 Nov comeback and the Nepal PM visit — none of them Wednesday's news

## Run it

```
python3 main.py
```

Writes the image to `/output/entry.png` (or to the path given as the first argument). Pure standard library only; running it twice writes byte-identical bytes. The image in this repo (`entry.png`) is the output of that program.
