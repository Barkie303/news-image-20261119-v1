# The World — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Barkie303/news-image-20261119-v1/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Barkie303/news-image-20261119-v1/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page that sums up the world's news of Thursday
19 November 2026 in one image.

The lead story is the first-ever handshake of Trump, Xi and Putin in
Shenzhen, at the APEC summit — three leaders talking world peace,
nuclear arms and two wars. Around it: a globe marking where the news
happened, the day in numbers (33 stories, 6 continents, 3 leaders,
1 light-day for Voyager 1), and 31 more short stories grouped by
continent — Asia-Pacific, Europe, the Middle East, Africa, the
Americas, and Sport & Business — plus one lighter story to end the
day (GTA VI finally rolls out, and gamers enter Vice City).

## How it is built

- `gen.py` draws `entry.png` (1024x1024, PNG) with Pillow from fixed
  text, so the image is fully deterministic.
- `main.py` (standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
  It checks the PNG magic bytes first and writes the same bytes on
  every run.

## Verify

```
python3 gen.py
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
cmp out1/entry.png out2/entry.png   # identical bytes
```

## The day's stories

Lead: Trump, Xi and Putin shake hands in Shenzhen. Asia-Pacific: Xi
calls for open trade at APEC; Putin blasts Western sanctions; Cyclone
Akvan bears down on India; India and Japan review defence ties; Modi
meets the Prince and Princess of Wales; Congress targets Modi over
inflation; Australia sanctions Israeli settlers; Islam set to be the
world's largest faith by 2035. Europe: Crimean Bridge attacked again;
EU proposes a €45bn Ukraine loan; Mélenchon could win the French
presidency; France's fourth weekend of protests; a Van Gogh sells for
a record $190.4m; an LPG tanker sunk off Bulgaria was hit by
projectiles. Middle East: Israeli tanks cross the Gaza ceasefire line;
four nations call for aid to flooded Gaza; Eisenkot is tapped to form
Israel's government; 1,100 child amputees face treatment limits;
Saudi Arabia says the danger has passed. Africa: South Sudan braces
for Ebola; Nigeria, Kenya and Sudan join forces on misinformation.
Americas: Jeffries set to be the first Black House Speaker; Peltola
wins Alaska; senators warn AI cyber threats are outpacing defences;
the US proposes tougher green-card rules; Canada adjusts China ties;
the US details $12bn of Venezuelan oil revenue. Sport & Business:
Anthropic poised for a $1.4tn market debut; a Crystal Palace 45%
stake bid worth ~£200m; Duckett's 133 puts England on top; India
women open the hockey trophy against Malaysia. And finally: GTA VI
rolls out worldwide.

Entered on [make.fun](https://make.fun/?ref=1qzhe0a6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards.
