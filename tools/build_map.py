#!/usr/bin/env python3
"""
Avrupa - Orta Dogu - Afrika haritasini Natural Earth verisinden uretir.

Cikti: tools/emea_grid.txt (izgara) ve "Turkish Leaders/Maps/TL_EMEA.lua" (harita betigi).
Her karakter bir altigeni temsil eder:
  ~ okyanus/deniz   g/G cayir (duz/tepe)   p/P ova (duz/tepe)
  d/D col (duz/tepe)  t/T tundra (duz/tepe)  s kar   M dag
Kullanim:  python3 tools/build_map.py <natural-earth-geojson-klasoru>
           python3 tools/build_map.py --assemble   (yalnizca sablondan yeniden olustur)
"""
import json
import math
import os
import sys

from shapely.geometry import LineString, Point, shape
from shapely.ops import unary_union
from shapely.prepared import prep

GEO = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "geo"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Turkish Leaders", "Maps", "TL_EMEA.lua")

W, H = 100, 90                 # harita boyutu (altigen)
LON_MIN, LON_MAX = -25.0, 75.0
LAT_MAX, LAT_MIN = 72.0, -36.0
DLON = (LON_MAX - LON_MIN) / W
DLAT = (LAT_MAX - LAT_MIN) / H


def load(name):
    with open(os.path.join(GEO, name + ".geojson"), encoding="utf-8") as fh:
        return json.load(fh)["features"]


def cell_center(x, y):
    """Civ5 koordinati (y=0 guney) -> boylam/enlem. Tek satirlar yarim kayik."""
    shift = 0.5 if (y % 2 == 1) else 0.0
    lon = LON_MIN + (x + 0.5 + shift) * DLON
    lat = LAT_MIN + (y + 0.5) * DLAT
    return lon, lat


def noise(x, y, seed):
    n = (x * 374761393 + y * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def smooth_noise(lon, lat, scale, seed):
    """Basit deger gurultusu (0..1)."""
    fx, fy = lon / scale, lat / scale
    x0, y0 = math.floor(fx), math.floor(fy)
    tx, ty = fx - x0, fy - y0
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a = noise(x0, y0, seed)
    b = noise(x0 + 1, y0, seed)
    c = noise(x0, y0 + 1, seed)
    d = noise(x0 + 1, y0 + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - ty) + (c * (1 - tx) + d * tx) * ty


# ---------------------------------------------------------------- veri
ASSEMBLE_ONLY = "--assemble" in sys.argv
land_p = deserts = ranges = plateaus = tundras = None
regions = []


def region_union(classes, names=None, exclude=()):
    geoms = []
    for f in regions:
        p = f["properties"]
        if p["FEATURECLA"] in classes and p["NAME"] not in exclude:
            if names is None or p["NAME"] in names:
                geoms.append(shape(f["geometry"]))
    return prep(unary_union(geoms)) if geoms else None


if not ASSEMBLE_ONLY:
    land = unary_union([shape(f["geometry"]) for f in load("ne_50m_land")])
    lakes = unary_union([shape(f["geometry"]) for f in load("ne_50m_lakes")
                         if shape(f["geometry"]).area > 0.6])   # sadece buyuk goller
    land = land.difference(lakes)
    land_p = prep(land)

    regions = load("ne_50m_geography_regions_polys")


    deserts = region_union({"Desert"}, exclude={"PUNJAB"})
    ranges = region_union({"Range/mtn"})
    plateaus = region_union({"Plateau"})
    tundras = region_union({"Tundra"})

# Natural Earth'te eksik kalan ama oyun icin onemli daglar (boylam, enlem) cizgileri
EXTRA_RANGES = [
    ("Toros", [(29.5, 36.8), (32.5, 36.6), (35.0, 37.2), (37.5, 37.8), (40.5, 38.2)], 0.8),
    ("Dogu Anadolu", [(39.0, 39.5), (41.5, 39.6), (43.5, 39.4)], 0.9),
    ("Kuzey Anadolu", [(31.0, 40.9), (34.5, 41.2), (37.0, 40.8)], 0.5),
    ("Lubnan", [(35.8, 33.2), (36.4, 34.6)], 0.4),
    ("Pindus", [(20.6, 40.8), (21.6, 39.0), (22.2, 37.4)], 0.5),
    ("Iskocya", [(-5.0, 56.6), (-4.0, 57.8)], 0.5),
    ("Dogu Afrika Rift", [(36.5, -8.0), (36.8, -3.0), (36.5, 1.0), (37.2, 4.0)], 0.7),
    ("Madagaskar", [(46.8, -24.0), (47.2, -19.0), (48.8, -14.0)], 0.6),
    ("Hacer", [(56.2, 24.5), (57.8, 23.2), (59.0, 22.5)], 0.4),
    ("Yemen", [(43.5, 13.5), (44.0, 15.5), (43.6, 17.5)], 0.6),
    ("Sina", [(33.8, 28.6), (34.2, 29.4)], 0.4),
    ("Kirim", [(34.0, 44.6), (34.8, 44.8)], 0.3),
    ("Sicilya-Kalabriya", [(14.8, 37.8), (16.2, 38.8)], 0.3),
    ("Iran Platosu", [(55.0, 34.5), (59.0, 35.2), (61.0, 34.0)], 0.6),
]
extra_lines = [(LineString(pts), w) for _, pts, w in EXTRA_RANGES]


def near_extra_range(pt):
    for line, w in extra_lines:
        if line.distance(pt) < w:
            return True
    return False


def land_fraction(x, y):
    lon, lat = cell_center(x, y)
    hits = 0
    total = 0
    for dx in (-0.35, 0.0, 0.35):
        for dy in (-0.35, 0.0, 0.35):
            total += 1
            if land_p.contains(Point(lon + dx * DLON, lat + dy * DLAT)):
                hits += 1
    return hits / total


# ----------------------------------------------------------- iklim kurali
def base_terrain(lon, lat, pt):
    """Duz arazi tipi: g p d t s"""
    n = smooth_noise(lon, lat, 3.0, 7)
    alat = abs(lat)
    # Kutup / kuzey
    if lat > 69.5:
        return "s" if n < 0.25 else "t"
    if lat > 63.0 or (tundras and tundras.contains(pt)):
        return "t" if n < 0.75 else "p"
    if lat > 58.0:
        return "t" if n < 0.25 else ("p" if n < 0.6 else "g")
    # Collar
    if deserts and deserts.contains(pt):
        # Nil vadisi istisna
        if 30.3 < lon < 33.2 and 22.0 < lat < 31.5 and abs(lon - nile_lon(lat)) < 0.9:
            return "p"
        return "d" if n < 0.92 else "p"
    # Arap Yarimadasi
    if 35.0 < lon < 60.0 and 12.5 < lat < 31.0 and lon > 36.5 + (lat - 28) * 0.9 - 2:
        if lon < 45.0 and lat < 18.5:          # Yemen / Asir
            return "p" if n < 0.6 else "g"
        if lon > 55.5 and lat < 25.5:          # Umman kiyisi
            return "p" if n < 0.5 else "d"
        return "d" if n < 0.85 else "p"
    # Mezopotamya ve Levant
    if 38.0 < lon < 48.5 and 29.5 < lat < 37.0:
        if abs(lon - (44.0 - (lat - 33.0) * 0.9)) < 2.0:   # Dicle-Firat ovasi
            return "p" if n < 0.6 else "g"
        return "d" if n < 0.6 else "p"
    # Iran platosu
    if 48.0 < lon < 66.0 and 25.0 < lat < 37.0:
        return "d" if n < 0.5 else "p"
    # Orta Asya bozkiri
    if lon > 47.0 and 37.0 <= lat <= 56.0:
        if lat < 45.0:
            return "d" if n < 0.45 else "p"
        return "p" if n < 0.8 else "g"
    # Kuzey Afrika kiyisi (Libya, Misir kiyisi)
    if -10.0 < lon < 32.0 and 26.0 < lat < 37.5 and not (lon < 11.5 and lat > 33.0):
        if 30.3 < lon < 32.5:
            return "p"
        return "d" if n < 0.35 else "p"
    # Afrika boynuzu
    if lon > 40.5 and -2.0 < lat < 12.5:
        return "d" if n < 0.45 else "p"
    # Sahel
    if 11.0 < lat < 18.5 and lon < 40.0:
        return "p" if n < 0.75 else ("d" if lat > 15.0 else "g")
    # Tropikler
    if alat < 10.0:
        return "g" if n < 0.75 else "p"
    # Guney Afrika
    if lat < -10.0:
        if lon < 18.5 and lat > -30.0:               # Namibya kiyisi
            return "d" if n < 0.6 else "p"
        return "p" if n < 0.55 else "g"
    # Akdeniz havzasi
    if 30.0 <= lat < 45.0:
        if 26.0 < lon < 45.0 and 36.5 < lat < 40.5:  # Anadolu ic yayla
            return "p" if n < 0.7 else "g"
        return "p" if n < 0.45 else "g"
    # Avrupa
    return "g" if n < 0.7 else "p"


def nile_lon(lat):
    # kabaca Nil'in boylami (Asvan - Kahire)
    if lat > 30.0:
        return 31.2
    if lat > 27.0:
        return 30.9 + (lat - 27.0) * 0.1
    if lat > 24.0:
        return 32.6 - (lat - 24.0) * 0.55
    return 32.9


def relief(lon, lat, pt):
    """'' duz, 'H' tepe, 'M' dag"""
    r = noise(int(lon * 10), int(lat * 10), 11)
    if ranges and ranges.contains(pt):
        if r < 0.33:
            return "M"
        if r < 0.80:
            return "H"
        return ""
    if near_extra_range(pt):
        if r < 0.25:
            return "M"
        if r < 0.75:
            return "H"
        return ""
    if plateaus and plateaus.contains(pt):
        return "H" if r < 0.40 else ""
    # Anadolu genelinde ve Balkanlarda biraz daha engebe
    if 26.0 < lon < 45.0 and 36.5 < lat < 41.5:
        return "H" if r < 0.30 else ""
    if 19.0 < lon < 27.0 and 39.0 < lat < 44.0:
        return "H" if r < 0.30 else ""
    return "H" if r < 0.10 else ""


# Elle duzeltmeler: (boylam, enlem, karakter)  ~ = deniz
MANUAL = [
    (28.6, 40.9, "~"),   # Marmara Denizi
    (28.0, 40.2, "~"),   # Marmara guneyi
    (27.0, 40.2, "~"),   # Canakkale Bogazi
    (-5.5, 36.6, "~"),  # Cebelitarik
    (56.2, 25.8, "~"),   # Hurmuz Bogazi
    (32.35, 30.4, "d"),  # Suveys kara koprusu (Afrika-Asya bagli kalsin)
]


def build():
    grid = [["~"] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if land_fraction(x, y) < 0.45:
                continue
            lon, lat = cell_center(x, y)
            pt = Point(lon, lat)
            t = base_terrain(lon, lat, pt)
            rel = relief(lon, lat, pt)
            if t == "s":
                grid[y][x] = "s"
            elif rel == "M":
                grid[y][x] = "M"
            elif rel == "H":
                grid[y][x] = t.upper()
            else:
                grid[y][x] = t
    for lon, lat, ch in MANUAL:
        x = int((lon - LON_MIN) / DLON)
        y = int((lat - LAT_MIN) / DLAT)
        if y % 2 == 1:
            x = int((lon - LON_MIN) / DLON - 0.5)
        grid[y][x] = ch
    # Bogaz kenarlarindaki daglari kaldir, tek basina kalan daglari tepeye cevir
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "M":
                water = sum(1 for nx, ny in neighbors(x, y) if grid[ny][nx] == "~")
                if water >= 3:
                    grid[y][x] = "P"
    return grid


def neighbors(x, y):
    if y % 2 == 0:
        dirs = [(-1, 0), (1, 0), (-1, 1), (0, 1), (-1, -1), (0, -1)]
    else:
        dirs = [(-1, 0), (1, 0), (0, 1), (1, 1), (0, -1), (1, -1)]
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H:
            yield nx, ny


GRID_FILE = os.path.join(ROOT, "tools", "emea_grid.txt")
TEMPLATE = os.path.join(ROOT, "tools", "map_template.lua")


def assemble(rows):
    """Izgara satirlarini map_template.lua icine gomerek TL_EMEA.lua dosyasini yazar."""
    data = ["-- Kaynak: Natural Earth (kamu mali). Satirlar kuzeyden guneye siralidir.",
            "TL_EMEA = {}",
            "TL_EMEA.Width = %d" % W, "TL_EMEA.Height = %d" % H,
            "TL_EMEA.LonMin = %.1f" % LON_MIN, "TL_EMEA.LonMax = %.1f" % LON_MAX,
            "TL_EMEA.LatMin = %.1f" % LAT_MIN, "TL_EMEA.LatMax = %.1f" % LAT_MAX,
            "TL_EMEA.Rows = {"]
    data += ['"%s",' % r for r in rows]
    data.append("}")
    with open(TEMPLATE, encoding="utf-8") as fh:
        tpl = fh.read()
    out = tpl.replace("--@@MAPDATA@@", "\n".join(data))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(out)


def main():
    if "--assemble" in sys.argv:
        with open(GRID_FILE, encoding="utf-8") as fh:
            rows = [l.rstrip("\n") for l in fh if l.strip()]
    else:
        grid = build()
        rows = ["".join(grid[y]) for y in range(H - 1, -1, -1)]   # kuzeyden guneye
        with open(GRID_FILE, "w", encoding="utf-8") as fh:
            fh.write("\n".join(rows) + "\n")
    assert len(rows) == H and all(len(r) == W for r in rows)
    assemble(rows)
    land_count = sum(c != "~" for r in rows for c in r)
    print("kara orani: %.1f%%  ->  %s" % (100.0 * land_count / (W * H), OUT))


if __name__ == "__main__":
    main()
