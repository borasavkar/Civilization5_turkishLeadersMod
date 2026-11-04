#!/usr/bin/env python3
"""
Lider portrelerinden Civ5 icin tum gorselleri uretir:
  * Diplomasi ekrani (1600x900), Dawn of Man yukleme ekrani (1024x768)
  * Lider simgesi atlasi (yuvarlak portreler), medeniyet simgesi atlasi ve alfa sembol atlasi
  * docs/ klasorune README icin onizleme PNG'leri
Kaynak gorseller: tools/art_src/<anahtar>.jpg (kamu mali, bkz. docs/KAYNAKLAR.md)
Kullanim: python3 tools/build_art.py
Gerekli: Pillow, ImageMagick (convert)
"""
import math
import os
import subprocess
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "art_src")
ART = os.path.join(ROOT, "Turkish Leaders", "Art")
DOCS = os.path.join(ROOT, "docs")

# anahtar, dosya adi oneki, simge renkleri (sembol, arka plan), sembol tipi,
# yuz kirpma kutusu (merkez x, merkez y, kare boyu; hepsi gorsel genisligine/yuksekligine oran)
LEADERS = [
    dict(key="osman", name="Osman", fg=(217, 180, 63), bg=(28, 82, 43), symbol="kayi",
         face=(0.40, 0.31, 0.50), portrait_focus=0.30),
    dict(key="orhan", name="Orhan", fg=(244, 224, 152), bg=(113, 26, 31), symbol="crescent",
         face=(0.49, 0.27, 0.48), portrait_focus=0.30),
    dict(key="fatih", name="Fatih", fg=(244, 241, 230), bg=(163, 18, 26), symbol="crescent_star8",
         face=(0.50, 0.45, 0.42), portrait_focus=0.35),
    dict(key="yavuz", name="Yavuz", fg=(250, 250, 245), bg=(0, 99, 66), symbol="three_crescents",
         face=(0.42, 0.27, 0.45), portrait_focus=0.30),
    dict(key="battal", name="Battal", fg=(206, 40, 30), bg=(27, 27, 30), symbol="swords",
         face=(0.50, 0.36, 0.42), portrait_focus=0.20),
    dict(key="ataturk", name="Ataturk", fg=(255, 255, 255), bg=(227, 10, 23), symbol="crescent_star5",
         face=(0.50, 0.24, 0.62), portrait_focus=0.25),
]

GOLD = (212, 175, 90)


# ------------------------------------------------------------------ yardimcilar
def load_src(key):
    for ext in (".jpg", ".png", ".jpeg"):
        p = os.path.join(SRC, key + ext)
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    return None


def cover(img, w, h, focus_y=0.4):
    """Gorseli w x h alanini kaplayacak sekilde olcekle ve kirp."""
    s = max(w / img.width, h / img.height)
    im = img.resize((max(w, int(img.width * s + 0.5)), max(h, int(img.height * s + 0.5))), Image.LANCZOS)
    x = (im.width - w) // 2
    y = int(max(0, min(im.height - h, (im.height - h) * focus_y)))
    return im.crop((x, y, x + w, y + h))


def tint(img, color, amount):
    over = Image.new("RGB", img.size, color)
    return Image.blend(img, over, amount)


def vignette(w, h, strength=0.75, center=(0.5, 0.5)):
    """0..255 arasinda bir karartma maskesi (L)."""
    small = Image.new("L", (w // 8, h // 8))
    px = small.load()
    cx, cy = center[0] * small.width, center[1] * small.height
    rmax = math.hypot(max(cx, small.width - cx), max(cy, small.height - cy))
    for y in range(small.height):
        for x in range(small.width):
            r = math.hypot(x - cx, y - cy) / rmax
            px[x, y] = int(255 * min(1.0, max(0.0, (r - 0.35) / 0.65)) ** 1.6 * strength)
    return small.resize((w, h), Image.BILINEAR)


def star_points(cx, cy, r_out, r_in, n, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pattern_layer(w, h, color, alpha, step=120):
    """Osmanli sekiz koseli yildiz motifinden olusan seffaf desen."""
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for row, y in enumerate(range(-step, h + step, step)):
        off = (step // 2) if row % 2 else 0
        for x in range(-step + off, w + step, step):
            d.polygon(star_points(x, y, step * 0.30, step * 0.20, 8, rot=-90 + 22.5),
                      outline=color + (alpha,), width=2)
            d.ellipse((x - step * 0.07, y - step * 0.07, x + step * 0.07, y + step * 0.07),
                      outline=color + (alpha,), width=2)
    return layer


def feather_mask(w, h, left=0, right=0, bottom=0, top=0):
    m = Image.new("L", (w, h), 255)
    px = m.load()
    for x in range(w):
        for y in range(h):
            v = 1.0
            if left and x < left:
                v *= x / left
            if right and x > w - right:
                v *= (w - x) / right
            if bottom and y > h - bottom:
                v *= (h - y) / bottom
            if top and y < top:
                v *= y / top
            px[x, y] = int(255 * (v ** 1.3))
    return m


def compose_scene(src, leader, w, h, portrait_cx):
    """Bulanik arka plan + desen + net portre."""
    # zemin: medeniyet renginde koyu gradyan + cok hafif bulanik portre
    base = Image.new("RGB", (w, h))
    bd = ImageDraw.Draw(base)
    c1 = tuple(int(v * 0.55) for v in leader["bg"])
    c2 = tuple(int(v * 0.18) for v in leader["bg"])
    for x in range(w):
        t = x / (w - 1)
        bd.line((x, 0, x, h), fill=tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3)))
    blur = cover(src, w, h, leader["portrait_focus"]).filter(ImageFilter.GaussianBlur(max(w, h) / 30))
    base = Image.blend(base, tint(blur, leader["bg"], 0.5), 0.22)
    canvas = base.convert("RGBA")
    canvas.alpha_composite(pattern_layer(w, h, GOLD, 34, step=int(h / 7)))

    # portre: yuksekligi kaplasin
    ph = h
    pw = int(src.width * ph / src.height)
    if pw > w * 0.62:
        pw = int(w * 0.62)
        portrait = cover(src, pw, ph, leader["portrait_focus"])
    else:
        portrait = src.resize((pw, ph), Image.LANCZOS)
    mask = feather_mask(pw, ph, left=int(pw * 0.35), right=int(pw * 0.30), bottom=int(ph * 0.12), top=int(ph * 0.04))
    shadow = Image.new("RGBA", (pw + 80, ph), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (40, 0), mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    x = int(portrait_cx - pw / 2)
    canvas.alpha_composite(shadow, (x - 40, 0))
    pr = portrait.convert("RGBA")
    pr.putalpha(mask)
    canvas.alpha_composite(pr, (x, 0))

    # karartma ve altin cerceve
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dark.putalpha(vignette(w, h, 0.85, center=(portrait_cx / w, 0.42)))
    canvas.alpha_composite(dark)
    d = ImageDraw.Draw(canvas)
    m = int(h * 0.025)
    d.rectangle((m, m, w - m, h - m), outline=GOLD + (200,), width=max(2, h // 300))
    m2 = m + max(5, h // 120)
    d.rectangle((m2, m2, w - m2, h - m2), outline=GOLD + (120,), width=1)
    return canvas


# ------------------------------------------------------------------ semboller
def draw_crescent(d, cx, cy, r, color, cut_dx=0.28, cut_r=0.80, bgcolor=None):
    """Sagga acik hilal: buyuk daireden kaydirilmis daire cikarilir (maske uzerinde)."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    rr = r * cut_r
    ox = cx + r * cut_dx
    d.ellipse((ox - rr, cy - rr, ox + rr, cy + rr), fill=bgcolor)


def symbol_mask(kind, size):
    """Beyaz sembol, seffaf zemin; size x size L maske dondurur."""
    S = size
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    c = S / 2
    if kind == "crescent":
        draw_crescent(d, c - S * 0.03, c, S * 0.36, 255, 0.30, 0.82, 0)
    elif kind in ("crescent_star5", "crescent_star8"):
        draw_crescent(d, c - S * 0.10, c, S * 0.33, 255, 0.27, 0.80, 0)
        n = 5 if kind == "crescent_star5" else 8
        rin = 0.38 if n == 5 else 0.55
        d.polygon(star_points(c + S * 0.22, c, S * 0.13, S * 0.13 * rin, n, rot=180 if n == 5 else -90), fill=255)
    elif kind == "three_crescents":
        for (dx, dy) in ((-0.17, -0.13), (0.17, -0.13), (0.0, 0.17)):
            draw_crescent(d, c + S * dx - S * 0.02, c + S * dy, S * 0.15, 255, 0.30, 0.80, 0)
    elif kind == "kayi":
        # Kayi damgasindan esinlenen sembol: govde ve iki ok ucu
        lw = int(S * 0.07)
        d.line((c, S * 0.20, c, S * 0.82), fill=255, width=lw)
        for y0 in (0.20, 0.42):
            d.line((c - S * 0.20, S * (y0 + 0.20), c, S * y0), fill=255, width=lw)
            d.line((c + S * 0.20, S * (y0 + 0.20), c, S * y0), fill=255, width=lw)
        d.line((c - S * 0.16, S * 0.84, c, S * 0.70), fill=255, width=lw)
        d.line((c + S * 0.16, S * 0.84, c, S * 0.70), fill=255, width=lw)
    elif kind == "swords_old":
        # iki capraz egri kilic
        for sgn in (-1, 1):
            blade = Image.new("L", (S, S), 0)
            bd = ImageDraw.Draw(blade)
            # egri bicak: iki yay arasi
            box = (c - S * 0.55, S * 0.12, c + S * 0.25, S * 1.10)
            bd.pieslice(box, 200, 268, fill=255)
            box2 = (c - S * 0.50, S * 0.19, c + S * 0.24, S * 1.12)
            bd.pieslice(box2, 195, 275, fill=0)
            # kabza
            bd.line((c - S * 0.33, S * 0.66, c - S * 0.20, S * 0.80), fill=255, width=int(S * 0.06))
            bd.line((c - S * 0.36, S * 0.73, c - S * 0.20, S * 0.63), fill=255, width=int(S * 0.035))
            blade = blade.rotate(-sgn * 0, resample=Image.BICUBIC)
            if sgn == 1:
                blade = blade.transpose(Image.FLIP_LEFT_RIGHT)
            m = ImageChops.lighter(m, blade)
        d = ImageDraw.Draw(m)
    elif kind == "swords":
        # iki capraz pala (egri kilic)
        for ang in (-38, 38):
            blade = Image.new("L", (S, S), 0)
            bd = ImageDraw.Draw(blade)
            pts = []
            n = 24
            for i in range(n + 1):           # bicagin dis kenari (hafif egri)
                t = i / n
                y = S * (0.12 + 0.62 * t)
                x = c + S * 0.05 * math.sin(t * math.pi * 0.9) - S * 0.03
                pts.append((x, y))
            for i in range(n, -1, -1):       # ic kenar, uca dogru incelir
                t = i / n
                y = S * (0.12 + 0.62 * t)
                x = c + S * 0.05 * math.sin(t * math.pi * 0.9) + S * (0.005 + 0.055 * t ** 0.6)
                pts.append((x, y))
            bd.polygon(pts, fill=255)
            bd.rectangle((c - S * 0.12, S * 0.74, c + S * 0.14, S * 0.775), fill=255)   # balcak
            bd.rectangle((c - S * 0.02, S * 0.775, c + S * 0.045, S * 0.90), fill=255)   # kabza
            bd.ellipse((c - S * 0.035, S * 0.885, c + S * 0.06, S * 0.95), fill=255)    # topuz
            blade = blade.rotate(ang, resample=Image.BICUBIC, center=(c, S * 0.55))
            m = ImageChops.lighter(m, blade)
    return m


def civ_icon(leader, size):
    S = 1024
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = S * 0.02
    d.ellipse((pad, pad, S - pad, S - pad), fill=leader["bg"] + (255,))
    # ic halka
    d.ellipse((S * 0.06, S * 0.06, S * 0.94, S * 0.94), outline=leader["fg"] + (110,), width=int(S * 0.012))
    sym = symbol_mask(leader["symbol"], int(S * 0.80))
    layer = Image.new("RGBA", sym.size, leader["fg"] + (255,))
    layer.putalpha(sym)
    off = int(S * 0.10)
    img.alpha_composite(layer, (off, off))
    return img.resize((size, size), Image.LANCZOS)


def alpha_icon(leader, size):
    S = 1024
    sym = symbol_mask(leader["symbol"], S)
    img = Image.new("RGBA", (S, S), (255, 255, 255, 0))
    img.putalpha(sym)
    return img.resize((size, size), Image.LANCZOS)


def leader_icon(src, leader, size):
    S = 1024
    fx, fy, fs = leader["face"]
    side = int(src.width * fs)
    cx, cy = int(src.width * fx), int(src.height * fy)
    x0 = max(0, min(src.width - side, cx - side // 2))
    y0 = max(0, min(src.height - side, cy - side // 2))
    face = src.crop((x0, y0, x0 + side, y0 + side)).resize((S, S), Image.LANCZOS)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), fill=255)
    img.paste(face, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse((S * 0.03, S * 0.03, S * 0.97, S * 0.97), outline=GOLD + (255,), width=int(S * 0.035))
    return img.resize((size, size), Image.LANCZOS)


# ------------------------------------------------------------------ DDS
def save_dds(img, path, has_alpha=True):
    """Sikistirmasiz 32 bit (A8R8G8B8) DDS, mipmap yok."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    img.convert("RGBA").save(tmp_path)
    try:
        subprocess.check_call(["convert", tmp_path, "-alpha", "on", "-define", "dds:compression=none",
                               "-define", "dds:mipmaps=0", path])
    finally:
        os.remove(tmp_path)


def atlas(images, size, cols=4, rows=2):
    a = Image.new("RGBA", (size * cols, size * rows), (0, 0, 0, 0))
    for i, im in enumerate(images):
        if im is None:
            continue
        a.alpha_composite(im, ((i % cols) * size, (i // cols) * size))
    return a


def placeholder_portrait(leader):
    """Kaynak gorsel yoksa renkli bir yer tutucu."""
    img = Image.new("RGB", (800, 1100), leader["bg"])
    d = ImageDraw.Draw(img)
    sym = symbol_mask(leader["symbol"], 600)
    layer = Image.new("RGB", (600, 600), leader["fg"])
    img.paste(layer, (100, 250), sym)
    return img


def main():
    os.makedirs(DOCS, exist_ok=True)
    srcs = []
    for L in LEADERS:
        src = load_src(L["key"])
        if src is None:
            print("UYARI: kaynak gorsel yok, yer tutucu kullaniliyor:", L["key"])
            src = placeholder_portrait(L)
        srcs.append(src)

    gallery = []
    for L, src in zip(LEADERS, srcs):
        scene = compose_scene(src, L, 1600, 900, portrait_cx=1060)
        save_dds(scene, os.path.join(ART, "Leaders", "TL_%s_Diplo.dds" % L["name"]))
        dom = compose_scene(src, L, 1024, 768, portrait_cx=690)
        save_dds(dom.convert("RGB").convert("RGBA"), os.path.join(ART, "Leaders", "TL_%s_DOM.dds" % L["name"]))
        scene.convert("RGB").resize((800, 450), Image.LANCZOS).save(os.path.join(DOCS, "lider_%s.jpg" % L["key"]), quality=88)
        gallery.append(scene)

        # Lider sahnesi XML'i
        with open(os.path.join(ART, "Leaders", "TL_%s_Scene.xml" % L["name"]), "w", encoding="utf-8") as fh:
            fh.write('<LeaderScene FallbackImage="TL_%s_Diplo.dds"></LeaderScene>\n' % L["name"])

    for size in (256, 128, 80, 64, 48, 45, 32, 24, 16):
        save_dds(atlas([civ_icon(L, size) for L in LEADERS], size), os.path.join(ART, "Icons", "TL_CivAtlas_%d.dds" % size))
    for size in (128, 80, 64, 48, 45, 32, 24, 16):
        save_dds(atlas([alpha_icon(L, size) for L in LEADERS], size), os.path.join(ART, "Icons", "TL_CivAlphaAtlas_%d.dds" % size))
    for size in (256, 128, 80, 64, 45, 32):
        save_dds(atlas([leader_icon(s, L, size) for L, s in zip(LEADERS, srcs)], size),
                 os.path.join(ART, "Icons", "TL_LeaderAtlas_%d.dds" % size))

    # README onizlemesi: simgeler
    sheet = Image.new("RGBA", (6 * 300 + 40, 620), (24, 24, 28, 255))
    for i, (L, s) in enumerate(zip(LEADERS, srcs)):
        sheet.alpha_composite(leader_icon(s, L, 256), (20 + i * 300 + 22, 20))
        sheet.alpha_composite(civ_icon(L, 256), (20 + i * 300 + 22, 320))
    sheet.convert("RGB").save(os.path.join(DOCS, "simgeler.png"))
    print("Gorseller uretildi.")


if __name__ == "__main__":
    main()
