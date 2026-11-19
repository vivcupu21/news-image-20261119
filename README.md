[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vivcupu21/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/vivcupu21/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Image — Thursday, 19 November 2026

A one-page newspaper front page that sums up the world news of
Thursday 19 November 2026 in a single image. The program is
[main.py](main.py) (Python 3.13, standard library only): it copies the
image stored in this repository ([entry.png](entry.png)) to
`/output/entry.png`. No network, no randomness, no timestamps — every
run writes the exact same bytes.

The image itself is drawn from scratch by [draw_entry.py](draw_entry.py)
(Pillow, flat vector-style panels and text; no external images): a
masthead naming the day, a lead story, four more main stories and an
"Also today" strip.

## The day's news in the image

- **Lead — Trump–Xi–Putin summit in Shenzhen.** First-ever
  trilateral as the three leaders meet on the APEC sidelines; nuclear
  arms, Ukraine, Iran, trade and AI on the agenda.
- **Crimean Bridge hit again.** Attacked again, traffic halted — days
  after Ukrainian strikes dropped a span into the Kerch Strait.
- **Israeli tanks cross Gaza line.** Rare ground operation in central
  Gaza, beyond the cease-fire line, as floods swamp the camps.
- **US–Iran fire widens.** Iran hits a US base in Kuwait and strikes
  Bahrain again; the US answers on Qeshm Island.
- **Cyclone Akvan crosses coast.** Bears down on India's east coast,
  set to cross between Machilipatnam and Puri.
- **GTA VI rolls out.** After 13 years, Rockstar's epic returns —
  midnight launch, Metacritic 99.
- **Also today:** Anthropic's $81.3bn IPO — largest ever, ANT debuts;
  ICJ to rule today on the Myanmar genocide case; EU proposes a €45bn
  Ukraine loan; Van Gogh sells for a record $190.4m; Estonia to shut
  its Russia border on 1 December.

Sources: Reuters, BBC, BusinessWorld, Le Monde, TBS News — all reported
19 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint: copies `entry.png` to the output directory.
- `entry.png` — the image (1024×1024, PNG, under 1 MiB).
- `draw_entry.py` — the script that drew `entry.png` from scratch.
- `LICENSE` — MIT.

## License

MIT — see [LICENSE](LICENSE).
