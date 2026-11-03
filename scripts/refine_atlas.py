#!/usr/bin/env python3
"""JSON'daki yaklasik sprite kutularini ImageMagick ile tespit edilen
gercek icerik sinirlariyla refine eder.

Yontem: JSON kutusu +/- margin ile pencere alinir, o penceredeki icerik
maskesi connected-components ile parcalara ayrilir; pencerenin merkezine
yakin ve makul boyutlu parcalar secilip birleştirilerek sinir union ile
daraltılır. Boylece JSON'un yanlis/abartili kutulari gercek icerige kilitlenir.

Cikti:
  /tmp/opencode/atlas-qc/refined.json    duzeltilmis koordinatlar
  /tmp/opencode/atlas-qc/refined_atlas.png  ustune cizilmis kontrol gorseli (2x)

Kullanim: scripts/refine_atlas.py [margin]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "gerekli_gereksiz_atlas.png"
META = ROOT / "gerekli_gereksiz_atlas.json"
QC = Path("/tmp/opencode/atlas-qc")
WORK = QC / "refine"
BG = "rgb(245,243,234)"
BG_TOL = 8
CC_RE = re.compile(r"^\s*(\d+):\s+(\d+)x(\d+)\+(\d+)\+(\d+)\s+\S+\s+([\d.e+]+)")
AW, AH = 1312, 1199


def magick(*args: object) -> str:
    cmd = ["magick"] + [str(a) for a in args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"magick hata: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout


def cc(path: Path) -> list[tuple[int, int, int, int]]:
    """(x, y, w, h) listesi; id 0 (arka plan) ve ince/gurultu parcalar elenir."""
    out = magick(path, "-define", "connected-components:verbose=true",
                 "-connected-components", "8", "null:")
    boxes = []
    for line in out.splitlines():
        m = CC_RE.match(line)
        if not m or m.group(1) == "0":
            continue
        w, h, x, y = (int(m.group(i)) for i in range(2, 6))
        area = float(m.group(6))
        if area < 20 or min(w, h) < 2 or max(w, h) / max(1, min(w, h)) > 12:
            continue  # cizgi/etiket/gurultu
        boxes.append((x, y, w, h))
    return boxes


def refine(sp: dict, mask: Path, win: Path, margin: int) -> dict:
    jx, jy, jw, jh = sp["x"], sp["y"], sp["width"], sp["height"]
    cx, cy = jx + jw / 2, jy + jh / 2

    x1 = max(0, jx - margin); y1 = max(0, jy - margin)
    x2 = min(AW, jx + jw + margin); y2 = min(AH, jy + jh + margin)
    w, h = x2 - x1, y2 - y1

    magick(mask, "-crop", f"{w}x{h}+{x1}+{y1}", "+repage",
           "-morphology", "Dilate", "Disk:2", win)

    # Parcalarin merkezine gore mesafe limiti: kutunun buyuk kenari + margin
    rmax = max(jw, jh) / 2 + margin * 0.7
    kept = []
    for bx, by, bw, bh in cc(win):
        gx, gy = x1 + bx + bw / 2, y1 + by + bh / 2
        if (gx - cx) ** 2 + (gy - cy) ** 2 <= rmax ** 2:
            kept.append((x1 + bx, y1 + by, bw, bh))

    if not kept:
        return {"x": jx, "y": jy, "width": jw, "height": jh,
                "method": "json-fallback"}

    ax1 = min(k[0] for k in kept); ay1 = min(k[1] for k in kept)
    ax2 = max(k[0] + k[2] for k in kept); ay2 = max(k[1] + k[3] for k in kept)
    return {"x": ax1, "y": ay1, "width": ax2 - ax1, "height": ay2 - ay1,
            "method": f"ccx{len(kept)}"}


def main() -> int:
    margin = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    WORK.mkdir(parents=True, exist_ok=True)
    mask = WORK / "mask.png"

    magick(ATLAS, "-alpha", "set", "-fuzz", f"{BG_TOL}%", "-fill", "none",
           "+opaque", BG, "-alpha", "extract", "-negate", mask)

    sprites = json.loads(META.read_text())["sprites"]
    refined: dict[str, dict] = {}
    for key, sp in sprites.items():
        r = refine(sp, mask, WORK / f"{key}_win.png", margin)
        refined[key] = r
        dx = r["x"] - sp["x"]; dy = r["y"] - sp["y"]
        dw = r["width"] - sp["width"]; dh = r["height"] - sp["height"]
        note = "" if (abs(dx) < 8 and abs(dy) < 8 and abs(dw) < 15
                      and abs(dh) < 15) else "  <-- DEGISIM"
        print(f"  {key:34s} json {sp['width']}x{sp['height']}+{sp['x']}+{sp['y']}"
              f" -> {r['width']}x{r['height']}+{r['x']}+{r['y']} {note}")

    (QC / "refined.json").write_text(json.dumps(
        {"margin": margin, "sprites": refined}, indent=2, ensure_ascii=False))

    draws = []
    for key, r in refined.items():
        draws += ["-draw", f"stroke #D00000 fill none stroke-width 2 "
                  f"rectangle {r['x']},{r['y']} "
                  f"{r['x'] + r['width'] - 1},{r['y'] + r['height'] - 1}",
                  "-draw", f"fill #D00000 stroke none font-size 11 "
                  f"text {r['x']},{r['y'] - 3} '{key}'"]
    magick(ATLAS, "-fill", "none", "-strokewidth", "1", *draws,
           QC / "refined_atlas.png")
    magick(QC / "refined_atlas.png", "-resize", "200%",
           QC / "refined_atlas_2x.png")
    print(f"\ncikti: {QC / 'refined.json'} | {QC / 'refined_atlas_2x.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
