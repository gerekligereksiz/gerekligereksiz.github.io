#!/usr/bin/env python3
"""gerekli_gereksiz_atlas.png sprite kesici.

Onaylanmis sinirlarla (bkz. scripts/detect_atlas.py) atlasi crop eder ve
WebP'ye cevirir. Arka plan ve renklerle OYNANMAZ: seffaflastirma, trim,
floodfill veya renk duzeltmesi yok — kutu neyi iceriyorsa aynen aktarilir.

Cikti: assets/images/atlas/<key>.webp

Kullanim:
  scripts/cut_atlas.py                # tum sprite'lar
  scripts/cut_atlas.py key1 key2      # secili sprite'lar

Ortam degiskenleri:
  DETECTED  sinir dosyasi (varsayilan: /tmp/opencode/atlas-qc/detected.json)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ortam degiskenleriyle baska atlas da kesilebilir:
#   ATLAS=... META=... OUT_DIR=... PREFIX=bulletin_ RESIZE=256 LOSSY_CATS=sticker
ATLAS = Path(os.environ.get("ATLAS", ROOT / "gerekli_gereksiz_atlas.png"))
META = Path(os.environ.get("META", ROOT / "gerekli_gereksiz_atlas.json"))
DETECTED = Path(os.environ.get("DETECTED", "/tmp/opencode/atlas-qc/detected.json"))
OUT_DIR = Path(os.environ.get("OUT_DIR", ROOT / "assets" / "images" / "atlas"))
QC_DIR = Path(os.environ.get("QC_DIR", "/tmp/opencode/atlas-qc"))
PREFIX = os.environ.get("PREFIX", "")
RESIZE = os.environ.get("RESIZE", "")  # "256" -> 256x256 (kare kutular icin)
QUALITY = os.environ.get("QUALITY", "88")
# Fotograf iceren kartlar lossy, geri kalan her sey lossless (netlik korunur)
LOSSY_CATS = set(os.environ.get("LOSSY_CATS", "content-card").split(","))


def magick(*args: object) -> str:
    cmd = ["magick"] + [str(a) for a in args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"magick hata: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout


def main() -> int:
    if not ATLAS.exists() or not META.exists():
        print("atlas png/json bulunamadi", file=sys.stderr)
        return 1
    if not DETECTED.exists():
        print(f"sinir dosyasi yok: {DETECTED}\n"
              "once scripts/detect_atlas.py calistir", file=sys.stderr)
        return 1

    meta = json.loads(META.read_text())["sprites"]  # kategori bilgisi
    boxes = json.loads(DETECTED.read_text())["sprites"]  # onayli sinirlar
    keys = sys.argv[1:] or list(boxes)
    bad = [k for k in keys if k not in boxes]
    if bad:
        print(f"bilinmeyen key: {bad}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QC_DIR.mkdir(parents=True, exist_ok=True)
    print(f"{len(keys)} sprite (renk/arka plan mudahalesi yok)")

    rows = []
    for key in keys:
        b = boxes[key]
        cat = meta.get(key, {}).get("category", "?")
        out = OUT_DIR / f"{PREFIX}{key}.webp"
        crop = f"{b['width']}x{b['height']}+{b['x']}+{b['y']}"

        if cat in LOSSY_CATS:
            extra = ["-resize", f"{RESIZE}x{RESIZE}"] if RESIZE else []
            magick(ATLAS, "-crop", crop, "+repage", *extra,
                   "-quality", QUALITY, out)
            mode = f"lossy{QUALITY}"
        else:
            extra = ["-resize", f"{RESIZE}x{RESIZE}"] if RESIZE else []
            magick(ATLAS, "-crop", crop, "+repage", *extra,
                   "-define", "webp:lossless=true", out)
            mode = "lossless"

        kb = round(out.stat().st_size / 1024, 1)
        ow, oh = magick(out, "-format", "%w %h", "info:").split()
        rows.append((key, cat, f"{b['width']}x{b['height']}->{ow}x{oh}", kb, mode))
        print(f"  {key:36s} {b['width']:>3}x{b['height']:<3} "
              f"+{b['x']}+{b['y']}  {kb:>7} KB  {mode}")

    lines = ["| key | kategori | boyut | kb | mode |", "|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in rows]
    (QC_DIR / "cut_report.md").write_text("\n".join(lines) + "\n")
    print(f"\nrapor: {QC_DIR / 'cut_report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
