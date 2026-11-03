#!/usr/bin/env python3
"""Atlas'tan gercek sprite sinirlarini ImageMagick ile tespit eder.

Yontem:
  1) Global arka plan temizligi -> icerik maskesi
  2) Hafif dilasyon (ikon icindeki parcalari birlestirir, komşulari kaydirmez)
  3) Connected-components ile blob'lari bul
  4) Her blob, icinde merkezi dusen (kucultulmus) JSON kutusuna atanir;
     birden fazla kutuya dusuyorsa en buyuk kesisime atanir
  5) Sprite siniri = ona atanan blob'larin union bbox'i

Cikti:
  /tmp/opencode/atlas-qc/detected.json
  /tmp/opencode/atlas-qc/detected_atlas_2x.png

Kullanim: scripts/detect_atlas.py [dilate_r] [orphan_min_area]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Farkli atlaslar icin ortam degiskeniyle gecersiz kilinabilir:
#   ATLAS=... META=... QC=... BG=alpha SQUARE=1 PAD=10
ATLAS = Path(os.environ.get("ATLAS", ROOT / "gerekli_gereksiz_atlas.png"))
META = Path(os.environ.get("META", ROOT / "gerekli_gereksiz_atlas.json"))
QC = Path(os.environ.get("QC", "/tmp/opencode/atlas-qc"))
WORK = QC / "detect"
# BG="alpha" -> seffaf PNG: maske dogrudan alfa kanalindan cikar.
BG = os.environ.get("BG", "rgb(245,243,234)")
BG_TOL = int(os.environ.get("BG_TOL", "8"))
# SQUARE=1 -> icerik bbox'i kareye genisletilir (kesim kutusu = kare + PAD).
SQUARE = os.environ.get("SQUARE", "0") == "1"
PAD = int(os.environ.get("PAD", "8"))
SCALE = os.environ.get("SCALE", "200%")
# Elle duzeltilmis sinirlar (profil analiziyle dogrulanmis)
MANUAL = {
    # yazinin gercek baslangici y301; y227-300 araligi handwritten+monogram
    # alt kismi ve x481-482'deki dikey ayrac ile kaynasiyordu.
    # underline (y331-338) sprite'in parcasi.
    "logo_wordmark_underlined": {"x": 539, "y": 301, "width": 232, "height": 38},
    # otomatik atamada komsu category_sports'un sag kuyruğu (x370-404) bilime
    # kaymis; sutun profilinde x405-433 arasi bosluk, gercek ikon x434-526.
    "category_science": {"x": 434, "y": 433, "width": 93, "height": 97},
    # tespit y1085'ten basliyordu; ustteki sticker_newspaper_logo'nun alt
    # kuyrugunu (y1050-1103) yutuyordu. Gercek tagline yazisi y1137'de basliyor
    # (y1104-1136 arasi bosluk).
    "footer_tagline": {"x": 1061, "y": 1137, "width": 210, "height": 38},
    # krem swatch arka plan rengine cok yakin (238,235,227 vs 246,243,237);
    # global maskelemede kayboluyordu. %2 toleransla CC ile bulundu.
    "color_cream": {"x": 1042, "y": 57, "width": 61, "height": 62},
    # otomatik atama y388/389'dan basliyordu ve ust satirin alt kuyrugunu
    # (y390-402, 12px) yutuyordu; ikonun kendisi y428'de basliyor.
    # Satir profilinde y403-427 arasi bosluk, gercek ikon y428-532.
    "category_news": {"x": 36, "y": 428, "width": 107, "height": 105},
    "category_blog": {"x": 171, "y": 428, "width": 102, "height": 105},
}
CC_RE = re.compile(r"^\s*(\d+):\s+(\d+)x(\d+)\+(\d+)\+(\d+)\s+\S+\s+([\d.e+]+)")


def magick(*args: object) -> str:
    cmd = ["magick"] + [str(a) for a in args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"magick hata: {' '.join(cmd)}\n{r.stderr.strip()}")
    return r.stdout


def atlas_size() -> tuple[int, int]:
    w, h = magick(ATLAS, "-format", "%w %h", "info:").split()
    return int(w), int(h)


def cc(path: Path) -> list[tuple[int, int, int, int, float]]:
    out = magick(path, "-define", "connected-components:verbose=true",
                 "-connected-components", "8", "null:")
    boxes = []
    for line in out.splitlines():
        m = CC_RE.match(line)
        if not m or m.group(1) == "0":
            continue  # id 0 = arka plan
        w, h, x, y = (int(m.group(i)) for i in range(2, 6))
        boxes.append((x, y, w, h, float(m.group(6))))
    return boxes


def main() -> int:
    dilate = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    orphan_area = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    WORK.mkdir(parents=True, exist_ok=True)
    mask = WORK / "mask.png"
    soft = WORK / "soft.png"

    if BG == "alpha":
        # Seffaf PNG: alfa kanali zaten icerik maskesi; once esikle (anti-alias
        # gri tonlari CC'yi binlerce parcaya boler), sonra negate: arka plan
        # beyaz, icerik siyah (CC id 0 = arka plan).
        tol = os.environ.get("ALPHA_TOL", "10%")
        magick(ATLAS, "-alpha", "extract", "-threshold", tol, "-negate", mask)
    else:
        magick(ATLAS, "-alpha", "set", "-fuzz", f"{BG_TOL}%", "-fill", "none",
               "+opaque", BG, "-alpha", "extract", "-negate", mask)
    magick(mask, "-morphology", "Dilate", f"Disk:{dilate}", soft)

    sprites = json.loads(META.read_text())["sprites"]

    # JSON kutulari tam boyutla; atama kesisim alaniyla, kesisim yoksa
    # en yakin merkezle yapilir.
    rects = []
    for key, sp in sprites.items():
        rects.append((key, sp["x"], sp["y"],
                      sp["x"] + sp["width"], sp["y"] + sp["height"],
                      sp["width"] * sp["height"],
                      sp["x"] + sp["width"] / 2, sp["y"] + sp["height"] / 2))

    NEAR = 60  # kesisim yoksa merkeze bu piksel mesafedeki kutuya ata
    assigned: dict[str, list] = {k: [] for k in sprites}
    orphans: list[tuple] = []
    for bx, by, bw, bh, area in cc(soft):
        best, best_ov, best_dist = None, 0.0, None
        for key, x1, y1, x2, y2, rarea, cx, cy in rects:
            ox = max(0, min(bx + bw, x2) - max(bx, x1))
            oy = max(0, min(by + bh, y2) - max(by, y1))
            if ox * oy > 0:
                ov = ox * oy / rarea  # normalize: kucuk kutuya avantaj
                if ov > best_ov:
                    best, best_ov, best_dist = key, ov, None
            elif best_ov == 0:
                d = ((bx + bw / 2 - cx) ** 2 + (by + bh / 2 - cy) ** 2) ** 0.5
                if best_dist is None or d < best_dist:
                    best, best_dist = key, d
        if best is not None and (best_ov > 0 or (best_dist or 1e9) <= NEAR):
            assigned[best].append((bx, by, bw, bh))
        elif area >= orphan_area:
            orphans.append((bx, by, bw, bh, area))

    detected = {}
    empty = []
    AW, AH = atlas_size()
    for key, boxes in assigned.items():
        if key in MANUAL:
            detected[key] = {**MANUAL[key], "blobs": 0, "method": "manual"}
            continue
        if not boxes:
            empty.append(key)
            continue
        x1 = min(b[0] for b in boxes); y1 = min(b[1] for b in boxes)
        x2 = max(b[0] + b[2] for b in boxes)
        y2 = max(b[1] + b[3] for b in boxes)
        w, h = x2 - x1, y2 - y1
        if SQUARE:
            # Kare kesim kutusu: icerik merkezli, PAD kadar seffaf pay.
            # Kenara tasarsa kutu iceri kaydirilir (icerik kirpilmaz).
            side = max(w, h) + 2 * PAD
            nx = int(round(x1 + w / 2 - side / 2))
            ny = int(round(y1 + h / 2 - side / 2))
            nx = max(0, min(nx, AW - side))
            ny = max(0, min(ny, AH - side))
            detected[key] = {"x": nx, "y": ny, "width": side, "height": side,
                             "content": {"x": x1, "y": y1,
                                         "width": w, "height": h},
                             "blobs": len(boxes), "method": "square"}
            continue
        detected[key] = {"x": x1, "y": y1, "width": w,
                         "height": h, "blobs": len(boxes)}

    (QC / "detected.json").write_text(json.dumps({
        "dilate": dilate,
        "sprites": detected,
        "unassigned_blobs": [
            {"x": b[0], "y": b[1], "width": b[2], "height": b[3]}
            for b in orphans],
    }, indent=2, ensure_ascii=False))

    draws = []
    for key, r in detected.items():
        draws += ["-draw", f"stroke #D00000 fill none stroke-width 2 "
                  f"rectangle {r['x']},{r['y']} "
                  f"{r['x'] + r['width'] - 1},{r['y'] + r['height'] - 1}",
                  "-draw", f"fill #D00000 stroke none font-size 11 "
                  f"text {r['x']},{r['y'] - 3} '{key}'"]
    for b in orphans:
        draws += ["-draw", f"stroke #0077B6 fill none stroke-width 2 "
                  f"rectangle {b[0]},{b[1]} "
                  f"{b[0] + b[2] - 1},{b[1] + b[3] - 1}",
                  "-draw", f"fill #0077B6 stroke none font-size 11 "
                  f"text {b[0]},{b[1] - 3} '?{b[2]}x{b[3]}'"]
    magick(ATLAS, "-fill", "none", "-strokewidth", "1", *draws,
           QC / "detected_atlas.png")
    magick(QC / "detected_atlas.png", "-resize", SCALE,
           QC / "detected_atlas_2x.png")

    print(f"{len(detected)} sprite siniri, {len(empty)} bos, "
          f"{len(orphans)} atamasiz blob (dilate={dilate})")
    if empty:
        print("bos kalan:", ", ".join(empty))
    print(f"cikti: {QC / 'detected.json'} | {QC / 'detected_atlas_2x.png'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
