#!/usr/bin/env python3
"""Atlas ustune sprite sinirlarini cizen dogrulama gorseli.

Kesim yapmadan, JSON'daki her sprite icin dikdortgen + etiket cizip
2x buyuklugunde teslim eder; koordinat kontrolu icin.

Kullanim:
  scripts/mark_atlas.py                # tum sprite'lar
  scripts/mark_atlas.py key1 key2      # secili sprite'lar
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ortam degiskenleriyle baska atlas/JSON de isaretlenebilir:
#   ATLAS=... META=... OUT=... SCALE=100%
ATLAS = Path(os.environ.get("ATLAS", ROOT / "gerekli_gereksiz_atlas.png"))
META = Path(os.environ.get("META", ROOT / "gerekli_gereksiz_atlas.json"))
OUT = Path(os.environ.get("OUT", "/tmp/opencode/atlas-qc/marked_atlas.png"))
SCALE = os.environ.get("SCALE", "200%")

# Kategori bazli cizim renkleri (krem zeminde okunur)
COLORS = {
    "logo": "#D00000",
    "color-swatch": "#7B2CBF",
    "typography": "#0077B6",
    "category-icon-color": "#2D6A4F",
    "category-icon-mono": "#57917D",
    "illustration": "#E85D04",
    "content-card": "#3A0CA3",
    "ui-icon": "#000000",
    "sticker": "#BC6C25",
    "text-art": "#6A040F",
}


def magick(*args: object) -> str:
    cmd = ["magick"] + [str(a) for a in args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"magick hata: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout


def atlas_width() -> int:
    out = magick(ATLAS, "-format", "%w", "info:")
    return int(out)


def main() -> int:
    sprites = json.loads(META.read_text())["sprites"]
    keys = sys.argv[1:] or list(sprites)
    OUT.parent.mkdir(parents=True, exist_ok=True)

    draws: list[str] = []
    legend: dict[str, str] = {}
    for key in keys:
        sp = sprites[key]
        x, y = sp["x"], sp["y"]
        x2, y2 = x + sp["width"] - 1, y + sp["height"] - 1
        color = COLORS.get(sp.get("category", "sticker"), "#333333")
        legend[sp.get("category", "sticker")] = color
        draws.append(f"stroke {color} fill none stroke-width 2 "
                     f"rectangle {x},{y} {x2},{y2}")
        draws.append(f"fill {color} stroke none font-size 11 "
                     f"text {x},{y - 3} '{key}'")

    # Alt serit: kategori renk aciklamasi
    strip = "/tmp/opencode/atlas-qc/_legend.png"
    legend_draws = []
    lx = 8
    for cat, color in legend.items():
        legend_draws.append(f"fill {color} stroke none rectangle {lx},8 {lx + 14},22")
        legend_draws.append(f"fill {color} font-size 12 text {lx + 18},20 '{cat}'")
        lx += 24 + 7 * len(cat)
    magick("-size", f"{atlas_width()}x32", "xc:#F5F3EA", "-fill", "none",
           *(a for d in legend_draws for a in ("-draw", d)), strip)

    marked = "/tmp/opencode/atlas-qc/_marked.png"
    magick(ATLAS, "-fill", "none", "-strokewidth", "1",
           *(a for d in draws for a in ("-draw", d)), marked)
    magick(marked, strip, "-append", "-resize", SCALE, OUT)
    print(f"cizildi: {OUT}  ({len(keys)} sprite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
