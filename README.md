# World News — Thursday 19 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261119)
[![date](https://img.shields.io/badge/date-19%20November%202026-gold)](https://make.fun/bounty/news-image-20261119)
[![entry](https://img.shields.io/badge/entry-entry.png-green)](https://make.fun/bounty/news-image-20261119)

One image summing up the world's news of **Thursday 19 November 2026**:
a dark-navy header naming the day, and a 2×3 grid of six stories, each
with a hand-drawn pictogram, a short title and one-line caption.

## The six stories

1. **Trump–Xi–Putin summit** — first-ever US–China–Russia summit, held
   in Shenzhen, with nuclear arms control and two wars on the agenda.
2. **GTA VI launches** — global release; players return to Vice City.
3. **Japan earthquake** — a magnitude 5.7 quake hits Kumamoto, Kyushu.
4. **US–Venezuela pact** — defence deal signed after the US defence
   secretary's visit to Caracas; the two militaries rebuild ties.
5. **Gaza flood aid call** — Australia, Canada, Italy and the UK jointly
   urge Israel to let aid into flood-hit Gaza.
6. **Voyager 1 milestone** — NASA's Voyager 1 probe reaches one
   light-day from Earth.

Sources: AP, The Hindu, SBS, Manila Times, The Paris Eye, JagranJosh
(all reporting 19 November 2026).

## How it is made

`draw.py` draws the 1024×1024 PNG with Pillow and the DejaVu fonts
(build time only): fixed layout, fixed colours, no randomness, no
network, no stock photos — every icon is basic shapes. `main.py`
(standard library only) copies the pre-rendered `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, so the two scoring runs produce
byte-identical output.

## Verify locally

```sh
python3 draw.py            # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im=Image.open('out/entry.png'); print(im.size, im.format)"
```

Owner: drizzle020106.
