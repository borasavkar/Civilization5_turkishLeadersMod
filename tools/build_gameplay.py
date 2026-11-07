#!/usr/bin/env python3
"""
Medeniyet, lider, yetenek, renk, simge atlasi, terfi ve isim verilerini XML olarak uretir:
  "Turkish Leaders/Core/TL_Gameplay.xml"

Bu veriler bilincli olarak XML'dedir: oyun XML dosyalarini her kosulda isler. Mevcut bir satiri
kopyalamayi gerektiren isler (benzersiz birim ve binalar) SQL dosyalarinda kalir.
"""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texts  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Turkish Leaders", "Core", "TL_Gameplay.xml")
OUT_EXTRAS = os.path.join(ROOT, "Turkish Leaders", "Core", "TL_Extras.xml")
OUT_AUDIO = os.path.join(ROOT, "Turkish Leaders", "Core", "TL_Audio.xml")

# ----------------------------------------------------------------- muzik
# Haritadaki muzik: Civilizations.SoundtrackTag -> SONG_<ETIKET>_PEACE_n / SONG_<ETIKET>_WAR_n
# Diplomasi ekrani: LEADER_X -> AS2D_LEADER_MUSIC_X_PEACE / _WAR
# Dosya adlari uzantisiz yazilir; mp3 dosyalari Sounds/ klasorunde ve VFS'e aktarilir.
SOUNDTRACK_TAG = "TLTurk"
MUSIC_PEACE = ["TL_Music_Gezinti", "TL_Music_Ask", "TL_Music_Locatin"]   # yalnizca baris
MUSIC_WAR = ["TL_Music_Atak"]                                             # yalnizca savas
LEADER_PEACE = {"BATTAL": "TL_Music_Gezinti"}   # digerleri: TL_Music_Locatin
LEADER_PEACE_DEFAULT = "TL_Music_Locatin"
LEADER_WAR = "TL_Music_Atak"
MUSIC_VOLUME = 60
# Bir XML dosyasindaki tek hata tum dosyayi iptal eder. Bu yuzden medeniyet ve liderlerin
# gorunmesi icin sart olmayan tablolar ayri bir dosyaya yazilir.
EXTRA_TABLES = {"UnitPromotions", "UnitPromotions_UnitCombatMods", "BuildingClasses", "Buildings",
                "Building_YieldChanges", "Building_YieldModifiers", "Building_UnitCombatProductionModifiers",
                "Building_UnitCombatFreeExperiences", "Trait_FreePromotionUnitCombats"}

CIVS = texts.CIVS  # OSMAN ORHAN FATIH YAVUZ BATTAL ATATURK
SCENE_NAME = {"OSMAN": "Osman", "ORHAN": "Orhan", "FATIH": "Fatih", "YAVUZ": "Yavuz",
              "BATTAL": "Battal", "ATATURK": "Ataturk"}

# (simge rengi, arka plan rengi, yazi rengi)  0..1
COLORS = {
    "OSMAN":   ((0.851, 0.706, 0.247), (0.110, 0.322, 0.169), (0.400, 0.780, 0.450)),
    "ORHAN":   ((0.957, 0.878, 0.596), (0.443, 0.102, 0.122), (0.850, 0.450, 0.420)),
    "FATIH":   ((0.957, 0.945, 0.902), (0.639, 0.071, 0.102), (1.000, 0.420, 0.420)),
    "YAVUZ":   ((0.980, 0.980, 0.960), (0.000, 0.388, 0.259), (0.300, 0.850, 0.600)),
    "BATTAL":  ((0.808, 0.157, 0.118), (0.106, 0.106, 0.118), (0.900, 0.350, 0.300)),
    "ATATURK": ((1.000, 1.000, 1.000), (0.890, 0.039, 0.090), (1.000, 0.300, 0.330)),
}

# Lider kisilikleri
PERSONALITY_KEYS = ["VictoryCompetitiveness", "WonderCompetitiveness", "MinorCivCompetitiveness", "Boldness",
                    "DiploBalance", "WarmongerHate", "DenounceWillingness", "DoFWillingness", "Loyalty",
                    "Neediness", "Forgiveness", "Chattiness", "Meanness"]
PERSONALITY = {
    "OSMAN":   [6, 4, 6, 7, 6, 5, 5, 6, 8, 5, 6, 5, 5],
    "ORHAN":   [7, 5, 6, 7, 6, 5, 5, 6, 7, 5, 5, 5, 5],
    "FATIH":   [9, 7, 6, 9, 5, 4, 6, 5, 6, 6, 4, 5, 6],
    "YAVUZ":   [9, 5, 5, 10, 4, 3, 8, 4, 5, 6, 3, 4, 8],
    "BATTAL":  [7, 3, 5, 9, 4, 4, 6, 6, 8, 4, 5, 6, 6],
    "ATATURK": [8, 7, 6, 6, 8, 7, 6, 7, 8, 4, 6, 6, 3],
}
MAJOR_APPROACHES = ["WAR", "HOSTILE", "DECEPTIVE", "GUARDED", "AFRAID", "FRIENDLY", "NEUTRAL"]
MAJOR_BIAS = {
    "OSMAN":   [6, 5, 4, 6, 3, 6, 5],
    "ORHAN":   [6, 5, 4, 6, 3, 6, 6],
    "FATIH":   [8, 6, 5, 5, 2, 5, 5],
    "YAVUZ":   [9, 7, 4, 5, 1, 4, 4],
    "BATTAL":  [7, 6, 3, 6, 2, 6, 5],
    "ATATURK": [4, 3, 3, 7, 2, 7, 7],
}
MINOR_APPROACHES = ["IGNORE", "FRIENDLY", "PROTECTIVE", "CONQUEST", "BULLY"]
MINOR_BIAS = {
    "OSMAN":   [4, 5, 6, 5, 4],
    "ORHAN":   [4, 5, 6, 5, 4],
    "FATIH":   [4, 5, 6, 7, 4],
    "YAVUZ":   [4, 5, 6, 7, 4],
    "BATTAL":  [4, 5, 6, 5, 4],
    "ATATURK": [4, 7, 6, 2, 4],
}
FLAVORS = ["OFFENSE", "DEFENSE", "CITY_DEFENSE", "MILITARY_TRAINING", "RECON", "RANGED", "MOBILE", "NAVAL",
           "NAVAL_RECON", "NAVAL_GROWTH", "NAVAL_TILE_IMPROVEMENT", "AIR", "EXPANSION", "GROWTH",
           "TILE_IMPROVEMENT", "INFRASTRUCTURE", "PRODUCTION", "GOLD", "SCIENCE", "CULTURE", "HAPPINESS",
           "GREAT_PEOPLE", "WONDER", "RELIGION", "DIPLOMACY", "SPACESHIP", "WATER_CONNECTION", "NUKE",
           "USE_NUKE", "ESPIONAGE", "ANTIAIR", "AIR_CARRIER", "ARCHAEOLOGY", "I_LAND_TRADE_ROUTE",
           "I_SEA_TRADE_ROUTE", "I_TRADE_ORIGIN", "I_TRADE_DESTINATION", "AIRLIFT"]
FLAVOR_OVERRIDES = {
    "OSMAN": {"EXPANSION": 9, "GROWTH": 8, "MOBILE": 7, "RELIGION": 6, "TILE_IMPROVEMENT": 7, "NAVAL": 3},
    "ORHAN": {"OFFENSE": 7, "MILITARY_TRAINING": 8, "DEFENSE": 7, "SCIENCE": 7, "GOLD": 6, "EXPANSION": 7},
    "FATIH": {"OFFENSE": 9, "RANGED": 8, "NAVAL": 7, "GOLD": 7, "WONDER": 7, "SCIENCE": 6, "CITY_DEFENSE": 4},
    "YAVUZ": {"OFFENSE": 10, "MILITARY_TRAINING": 8, "RELIGION": 8, "MOBILE": 7, "DIPLOMACY": 3, "CULTURE": 4},
    "BATTAL": {"OFFENSE": 9, "MOBILE": 8, "RECON": 7, "CITY_DEFENSE": 7, "GREAT_PEOPLE": 6, "SCIENCE": 4},
    "ATATURK": {"SCIENCE": 9, "CULTURE": 8, "DEFENSE": 8, "INFRASTRUCTURE": 8, "GROWTH": 7, "OFFENSE": 4,
                "DIPLOMACY": 7, "RELIGION": 2, "SPACESHIP": 7},
}

TRAITS = {
    "OSMAN": {"PlotCultureCostModifier": -33},
    "ORHAN": {"LandUnitMaintenanceModifier": -25},
    "FATIH": {},
    "YAVUZ": {"FaithFromKills": 50},
    "BATTAL": {"GreatGeneralRateModifier": 50, "PlunderModifier": 100},
    "ATATURK": {},
}
TRAIT_PROMOTIONS = [
    ("FATIH", "UNITCOMBAT_SIEGE", "PROMOTION_TL_FATIH_SIEGE"),
    ("BATTAL", "UNITCOMBAT_MELEE", "PROMOTION_TL_BATTAL_RAIDER"),
    ("BATTAL", "UNITCOMBAT_MOUNTED", "PROMOTION_TL_BATTAL_RAIDER"),
] + [("ATATURK", uc, "PROMOTION_TL_ATATURK_HOMELAND") for uc in
     ["UNITCOMBAT_MELEE", "UNITCOMBAT_GUN", "UNITCOMBAT_ARCHER", "UNITCOMBAT_MOUNTED",
      "UNITCOMBAT_SIEGE", "UNITCOMBAT_ARMOR", "UNITCOMBAT_RECON"]]

# (Type, etki sutunu, deger, simge sirasi)
PROMOTIONS = [
    ("PROMOTION_TL_FATIH_SIEGE", "CityAttack", 30, 3),
    ("PROMOTION_TL_BATTAL_RAIDER", "OutsideFriendlyLandsModifier", 15, 1),
    ("PROMOTION_TL_ATATURK_HOMELAND", "FriendlyLandsModifier", 15, 2),
    ("PROMOTION_TL_AKINCI", "MovesChange", 1, 4),
    ("PROMOTION_TL_CALDIRAN", None, None, 5),
    ("PROMOTION_TL_CANAKKALE", "FriendlyLandsModifier", 25, 2),
]

START_REGION = {"OSMAN": "REGION_GRASS", "ORHAN": "REGION_PLAINS", "YAVUZ": "REGION_PLAINS",
                "BATTAL": "REGION_HILLS", "ATATURK": "REGION_HILLS"}


class Doc:
    def __init__(self):
        self.tables = []

    def table(self, name, rows):
        self.tables.append((name, rows))

    def render(self, only=None, exclude=None):
        out = ['<?xml version="1.0" encoding="utf-8"?>',
               "<!-- Bu dosya tools/build_gameplay.py ile otomatik uretilmistir. Elle duzenlemeyin. -->",
               "<GameData>"]
        for name, rows in self.tables:
            if only is not None and name not in only:
                continue
            if exclude is not None and name in exclude:
                continue
            out.append("\t<%s>" % name)
            for row in rows:
                out.append("\t\t<Row>")
                for k, v in row.items():
                    if v is None:
                        continue
                    if isinstance(v, bool):
                        v = "true" if v else "false"
                    out.append("\t\t\t<%s>%s</%s>" % (k, escape(str(v)), k))
                out.append("\t\t</Row>")
            out.append("\t</%s>" % name)
        out += ["</GameData>", ""]
        return "\n".join(out)


def main():
    d = Doc()

    # Renkler
    colors, pcolors = [], []
    for c in CIVS:
        icon, bg, txt = COLORS[c]
        for suffix, rgb in (("ICON", icon), ("BACKGROUND", bg), ("TEXT", txt)):
            colors.append({"Type": "COLOR_PLAYER_TL_%s_%s" % (c, suffix),
                           "Red": rgb[0], "Green": rgb[1], "Blue": rgb[2], "Alpha": 1})
        pcolors.append({"Type": "PLAYERCOLOR_TL_" + c,
                        "PrimaryColor": "COLOR_PLAYER_TL_%s_ICON" % c,
                        "SecondaryColor": "COLOR_PLAYER_TL_%s_BACKGROUND" % c,
                        "TextColor": "COLOR_PLAYER_TL_%s_TEXT" % c})
    d.table("Colors", colors)
    d.table("PlayerColors", pcolors)

    # Simge atlaslari (4 sutun x 2 satir)
    atlases = []
    for atlas, prefix, sizes in (("TL_CIV_ATLAS", "TL_CivAtlas", (256, 128, 80, 64, 48, 45, 32, 24, 16)),
                                 ("TL_CIV_ALPHA_ATLAS", "TL_CivAlphaAtlas", (128, 80, 64, 48, 45, 32, 24, 16)),
                                 ("TL_LEADER_ATLAS", "TL_LeaderAtlas", (256, 128, 80, 64, 45, 32))):
        for s in sizes:
            atlases.append({"Atlas": atlas, "IconSize": s, "Filename": "%s_%d.dds" % (prefix, s),
                            "IconsPerRow": 4, "IconsPerColumn": 2})
    d.table("IconTextureAtlases", atlases)

    # Terfiler
    promos = []
    for ptype, col, val, idx in PROMOTIONS:
        row = {"Type": ptype, "Description": "TXT_KEY_" + ptype,
               "Help": "TXT_KEY_" + ptype + "_HELP", "Sound": "AS2D_IF_LEVELUP", "CannotBeChosen": True,
               "PortraitIndex": idx, "IconAtlas": "PROMOTION_ATLAS", "PediaType": "PEDIA_ATTRIBUTES",
               "PediaEntry": "TXT_KEY_" + ptype}
        if col:
            row[col] = val
        promos.append(row)
    d.table("UnitPromotions", promos)
    d.table("UnitPromotions_UnitCombatMods", [
        {"PromotionType": "PROMOTION_TL_CALDIRAN", "UnitCombatType": "UNITCOMBAT_MOUNTED", "Modifier": 33}])

    # Gorunmez yetenek binalari
    dummies = ["OSMAN", "ORHAN", "ATATURK"]
    d.table("BuildingClasses", [{"Type": "BUILDINGCLASS_TL_DUMMY_" + c, "DefaultBuilding": "BUILDING_TL_DUMMY_" + c,
                                 "Description": "TXT_KEY_BUILDING_TL_DUMMY_" + c, "NoLimit": True} for c in dummies])
    brow = []
    for c in dummies:
        r = {"Type": "BUILDING_TL_DUMMY_" + c, "BuildingClass": "BUILDINGCLASS_TL_DUMMY_" + c, "Cost": -1,
             "FaithCost": -1, "GreatWorkCount": -1, "GoldMaintenance": 0,
             "Description": "TXT_KEY_BUILDING_TL_DUMMY_" + c, "Help": "TXT_KEY_BUILDING_TL_DUMMY_%s_HELP" % c,
             "NeverCapture": True, "NukeImmune": True, "ConquestProb": 0, "HurryCostModifier": -1,
             "MinAreaSize": -1, "IconAtlas": "BW_ATLAS_1", "PortraitIndex": 19}
        if c == "ATATURK":
            r["CultureRateModifier"] = 10
        brow.append(r)
    d.table("Buildings", brow)
    d.table("Building_YieldChanges", [{"BuildingType": "BUILDING_TL_DUMMY_OSMAN", "YieldType": "YIELD_FOOD", "Yield": 1}])
    d.table("Building_YieldModifiers", [{"BuildingType": "BUILDING_TL_DUMMY_ATATURK", "YieldType": "YIELD_SCIENCE", "Yield": 10}])
    d.table("Building_UnitCombatProductionModifiers", [
        {"BuildingType": "BUILDING_TL_DUMMY_ORHAN", "UnitCombatType": uc, "Modifier": 25}
        for uc in ("UNITCOMBAT_MELEE", "UNITCOMBAT_GUN")])
    d.table("Building_UnitCombatFreeExperiences", [
        {"BuildingType": "BUILDING_TL_DUMMY_ORHAN", "UnitCombatType": uc, "Experience": 10}
        for uc in ("UNITCOMBAT_MELEE", "UNITCOMBAT_GUN")])

    # Yetenekler
    traits = []
    for c in CIVS:
        r = {"Type": "TRAIT_TL_" + c, "Description": "TXT_KEY_TRAIT_TL_" + c,
             "ShortDescription": "TXT_KEY_TRAIT_TL_%s_SHORT" % c}
        r.update(TRAITS[c])
        traits.append(r)
    d.table("Traits", traits)
    d.table("Trait_FreePromotionUnitCombats", [
        {"TraitType": "TRAIT_TL_" + c, "UnitCombatType": uc, "PromotionType": p} for c, uc, p in TRAIT_PROMOTIONS])

    # Liderler
    leaders = []
    for i, c in enumerate(CIVS):
        r = {"Type": "LEADER_TL_" + c, "Description": "TXT_KEY_LEADER_TL_" + c,
             "Civilopedia": "TXT_KEY_LEADER_TL_%s_PEDIA" % c,
             "CivilopediaTag": "TXT_KEY_CIVILOPEDIA_LEADERS_TL_" + c,
             "ArtDefineTag": "TL_%s_Scene.xml" % SCENE_NAME[c]}
        r.update(dict(zip(PERSONALITY_KEYS, PERSONALITY[c])))
        r.update({"IconAtlas": "TL_LEADER_ATLAS", "PortraitIndex": i})
        leaders.append(r)
    d.table("Leaders", leaders)
    d.table("Leader_Traits", [{"LeaderType": "LEADER_TL_" + c, "TraitType": "TRAIT_TL_" + c} for c in CIVS])
    d.table("Leader_MajorCivApproachBiases", [
        {"LeaderType": "LEADER_TL_" + c, "MajorCivApproachType": "MAJOR_CIV_APPROACH_" + a, "Bias": b}
        for c in CIVS for a, b in zip(MAJOR_APPROACHES, MAJOR_BIAS[c])])
    d.table("Leader_MinorCivApproachBiases", [
        {"LeaderType": "LEADER_TL_" + c, "MinorCivApproachType": "MINOR_CIV_APPROACH_" + a, "Bias": b}
        for c in CIVS for a, b in zip(MINOR_APPROACHES, MINOR_BIAS[c])])
    d.table("Leader_Flavors", [
        {"LeaderType": "LEADER_TL_" + c, "FlavorType": "FLAVOR_" + f, "Flavor": FLAVOR_OVERRIDES[c].get(f, 5)}
        for c in CIVS for f in FLAVORS])

    # Medeniyetler. Gorunum degerleri Osmanli'ninkidir; TL_Civilizations.sql bunlari
    # oyundaki Osmanli satirindan yeniden kopyalayarak garantiye alir.
    civs = []
    for i, c in enumerate(CIVS):
        civs.append({
            "Type": "CIVILIZATION_TL_" + c,
            "Description": "TXT_KEY_CIV_TL_%s_DESC" % c,
            "ShortDescription": "TXT_KEY_CIV_TL_%s_SHORT_DESC" % c,
            "Adjective": "TXT_KEY_CIV_TL_%s_ADJECTIVE" % c,
            "Civilopedia": "TXT_KEY_CIV5_TL_%s_TEXT_1" % c,
            "CivilopediaTag": "TXT_KEY_CIVILOPEDIA_CIVS_TL_" + c,
            "DefaultPlayerColor": "PLAYERCOLOR_TL_" + c,
            "ArtDefineTag": "ART_DEF_CIVILIZATION_OTTOMAN",
            "ArtStyleType": "ARTSTYLE_MIDDLE_EAST",
            "ArtStyleSuffix": "_AFRI",
            "ArtStylePrefix": "AFRICAN ",
            "PortraitIndex": i,
            "IconAtlas": "TL_CIV_ATLAS",
            "AlphaIconAtlas": "TL_CIV_ALPHA_ATLAS",
            "SoundtrackTag": SOUNDTRACK_TAG,
            "MapImage": "MapOttoman512.dds",
            "DawnOfManQuote": "TXT_KEY_CIV5_DAWN_TL_%s_TEXT" % c,
            "DawnOfManImage": "TL_%s_DOM.dds" % SCENE_NAME[c],
            "Playable": True,
            "AIPlayable": True,
        })
    d.table("Civilizations", civs)
    d.table("Civilization_Leaders", [{"CivilizationType": "CIVILIZATION_TL_" + c, "LeaderheadType": "LEADER_TL_" + c}
                                     for c in CIVS])
    d.table("Civilization_FreeBuildingClasses", [{"CivilizationType": "CIVILIZATION_TL_" + c,
                                                  "BuildingClassType": "BUILDINGCLASS_PALACE"} for c in CIVS])
    d.table("Civilization_FreeTechs", [{"CivilizationType": "CIVILIZATION_TL_" + c, "TechType": "TECH_AGRICULTURE"}
                                       for c in CIVS])
    d.table("Civilization_FreeUnits", [
        {"CivilizationType": "CIVILIZATION_TL_" + c, "UnitClassType": u, "Count": 1, "UnitAIType": ai}
        for c in CIVS for u, ai in (("UNITCLASS_SETTLER", "UNITAI_SETTLE"), ("UNITCLASS_WARRIOR", "UNITAI_DEFENSE"))])
    d.table("Civilization_Religions", [{"CivilizationType": "CIVILIZATION_TL_" + c, "ReligionType": "RELIGION_ISLAM"}
                                       for c in CIVS])
    d.table("Civilization_Start_Region_Priority", [{"CivilizationType": "CIVILIZATION_TL_" + c, "RegionType": r}
                                                   for c, r in START_REGION.items()])
    d.table("Civilization_Start_Along_Ocean", [{"CivilizationType": "CIVILIZATION_TL_FATIH", "StartAlongOcean": True}])

    # Isimler ve diplomasi
    d.table("Civilization_CityNames", [
        {"CivilizationType": "CIVILIZATION_TL_" + c, "CityName": "TXT_KEY_TL_CITY_%s_%02d" % (c, i + 1)}
        for c in CIVS for i in range(len(texts.CITIES[c]))])
    d.table("Civilization_SpyNames", [
        {"CivilizationType": "CIVILIZATION_TL_" + c, "SpyName": "TXT_KEY_TL_SPY_%s_%02d" % (c, i + 1)}
        for c in CIVS for i in range(len(texts.SPIES[c]))])
    d.table("Diplomacy_Responses", [
        {"LeaderType": "LEADER_TL_" + c, "ResponseType": texts.RESPONSE_TYPES[k],
         "Response": "TXT_KEY_LEADER_TL_%s_%s%%" % (c, k), "Bias": 1}
        for c, lines in texts.DIPLO.items() for k in lines])

    with open(OUT, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(d.render(exclude=EXTRA_TABLES))
    with open(OUT_EXTRAS, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(d.render(only=EXTRA_TABLES))
    write_audio()
    print("yazildi:", OUT, OUT_EXTRAS, OUT_AUDIO)


def write_audio():
    a = Doc()
    sounds, scripts = [], []

    def snd(fname):
        return "SND_" + fname.upper()

    for fname in sorted(set(MUSIC_PEACE + MUSIC_WAR + [LEADER_WAR, LEADER_PEACE_DEFAULT] + list(LEADER_PEACE.values()))):
        sounds.append({"SoundID": snd(fname), "Filename": fname, "LoadType": "DynamicResident"})

    def script(sid, fname):
        scripts.append({"ScriptID": sid, "SoundID": snd(fname), "SoundType": "GAME_MUSIC",
                        "MinVolume": MUSIC_VOLUME, "MaxVolume": MUSIC_VOLUME, "IsMusic": True})

    tag = SOUNDTRACK_TAG.upper()
    for i, f in enumerate(MUSIC_PEACE, 1):
        script("SONG_%s_PEACE_%d" % (tag, i), f)
    for i, f in enumerate(MUSIC_WAR, 1):
        script("SONG_%s_WAR_%d" % (tag, i), f)
    for c in CIVS:
        script("AS2D_LEADER_MUSIC_TL_%s_PEACE" % c, LEADER_PEACE.get(c, LEADER_PEACE_DEFAULT))
        script("AS2D_LEADER_MUSIC_TL_%s_WAR" % c, LEADER_WAR)
    a.table("Audio_Sounds", sounds)
    a.table("Audio_2DSounds", scripts)
    with open(OUT_AUDIO, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(a.render())


if __name__ == "__main__":
    main()
