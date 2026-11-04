#!/usr/bin/env python3
"""Harita verisinden onizleme PNG'si uretir (altigen goruntu)."""
import math, os, re, sys
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "Turkish Leaders", "Maps", "TL_EMEA.lua"), encoding="utf-8").read()
rows = re.findall(r'^"([^"]+)",', src, re.M)
H, W = len(rows), len(rows[0])
COL = {"~": (36, 84, 140), "g": (96, 150, 60), "G": (70, 120, 45), "p": (176, 160, 90), "P": (140, 125, 70),
       "d": (232, 210, 140), "D": (200, 175, 110), "t": (140, 150, 130), "T": (110, 118, 102), "s": (240, 240, 245),
       "M": (95, 80, 70)}
R = 7
img = Image.new("RGB", (int(W * R * 1.732 + R * 2), int(H * R * 1.5 + R * 2)), (20, 40, 70))
d = ImageDraw.Draw(img)
for row, line in enumerate(rows):
    y = H - 1 - row
    for x, ch in enumerate(line):
        cx = R * 1.732 * (x + (0.5 if y % 2 else 0)) + R * 1.2
        cy = R * 1.5 * row + R * 1.2
        pts = [(cx + R * math.cos(math.radians(60 * i + 30)), cy + R * math.sin(math.radians(60 * i + 30))) for i in range(6)]
        d.polygon(pts, fill=COL.get(ch, (255, 0, 255)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs", "harita_onizleme.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print(out, img.size)
