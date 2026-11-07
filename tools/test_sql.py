#!/usr/bin/env python3
"""
SQL ve XML dosyalarini, oyunun veritabaninin basitlestirilmis bir taklidi uzerinde calistirir.
Amac: sozdizimi hatalarini ve kopyalama mantigini oyunu acmadan yakalamak.
Not: Gercek semayi birebir icermez; oyundaki Database.log her zaman son kontroldur.
"""
import os
import sqlite3
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "Turkish Leaders")

SCHEMA = """
CREATE TABLE Colors (Type TEXT UNIQUE, Red REAL, Green REAL, Blue REAL, Alpha REAL);
CREATE TABLE PlayerColors (Type TEXT UNIQUE, PrimaryColor TEXT, SecondaryColor TEXT, TextColor TEXT);
CREATE TABLE IconTextureAtlases (Atlas TEXT, IconSize INTEGER, Filename TEXT, IconsPerRow INTEGER, IconsPerColumn INTEGER);
CREATE TABLE UnitPromotions (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE NOT NULL, Description TEXT, Help TEXT,
  Sound TEXT, CannotBeChosen BOOLEAN DEFAULT 0, PortraitIndex INTEGER, IconAtlas TEXT, PediaType TEXT, PediaEntry TEXT,
  CityAttack INTEGER DEFAULT 0, OutsideFriendlyLandsModifier INTEGER DEFAULT 0, FriendlyLandsModifier INTEGER DEFAULT 0,
  MovesChange INTEGER DEFAULT 0);
CREATE TABLE UnitPromotions_UnitCombatMods (PromotionType TEXT, UnitCombatType TEXT, Modifier INTEGER);
CREATE TABLE Units (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE NOT NULL, Class TEXT, Combat INTEGER DEFAULT 0,
  RangedCombat INTEGER DEFAULT 0, Cost INTEGER, Moves INTEGER, Description TEXT, Civilopedia TEXT, Strategy TEXT, Help TEXT,
  UnitArtInfo TEXT, UnitFlagAtlas TEXT, UnitFlagIconOffset INTEGER, IconAtlas TEXT, PortraitIndex INTEGER, PrereqTech TEXT);
CREATE TABLE Unit_AITypes (UnitType TEXT, UnitAIType TEXT);
CREATE TABLE Unit_ClassUpgrades (UnitType TEXT, UnitClassType TEXT);
CREATE TABLE Unit_Flavors (UnitType TEXT, FlavorType TEXT, Flavor INTEGER);
CREATE TABLE Unit_FreePromotions (UnitType TEXT, PromotionType TEXT);
CREATE TABLE Unit_ResourceQuantityRequirements (UnitType TEXT, ResourceType TEXT, Cost INTEGER);
CREATE TABLE UnitGameplay2DScripts (UnitType TEXT, SelectionSound TEXT, FirstSelectionSound TEXT);
CREATE TABLE ArtDefine_UnitInfos (Type TEXT);
CREATE TABLE BuildingClasses (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE, DefaultBuilding TEXT, Description TEXT,
  NoLimit BOOLEAN DEFAULT 0, MaxGlobalInstances INTEGER DEFAULT -1);
CREATE TABLE Buildings (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE NOT NULL, BuildingClass TEXT, Cost INTEGER,
  FaithCost INTEGER DEFAULT 0, GreatWorkCount INTEGER DEFAULT 0, GoldMaintenance INTEGER DEFAULT 0, PrereqTech TEXT,
  Description TEXT, Civilopedia TEXT, Strategy TEXT, Help TEXT, NeverCapture BOOLEAN DEFAULT 0, NukeImmune BOOLEAN DEFAULT 0,
  ConquestProb INTEGER DEFAULT 0, HurryCostModifier INTEGER DEFAULT 0, MinAreaSize INTEGER DEFAULT 0, IconAtlas TEXT,
  PortraitIndex INTEGER, Happiness INTEGER DEFAULT 0, Defense INTEGER DEFAULT 0, ExtraCityHitPoints INTEGER DEFAULT 0,
  Experience INTEGER DEFAULT 0, CultureRateModifier INTEGER DEFAULT 0);
CREATE TABLE Building_YieldChanges (BuildingType TEXT, YieldType TEXT, Yield INTEGER);
CREATE TABLE Building_YieldModifiers (BuildingType TEXT, YieldType TEXT, Yield INTEGER);
CREATE TABLE Building_Flavors (BuildingType TEXT, FlavorType TEXT, Flavor INTEGER);
CREATE TABLE Building_ClassesNeededInCity (BuildingType TEXT, BuildingClassType TEXT);
CREATE TABLE Building_LocalResourceOrs (BuildingType TEXT, ResourceType TEXT);
CREATE TABLE Building_ResourceQuantityRequirements (BuildingType TEXT, ResourceType TEXT, Cost INTEGER);
CREATE TABLE Building_UnitCombatProductionModifiers (BuildingType TEXT, UnitCombatType TEXT, Modifier INTEGER);
CREATE TABLE Building_UnitCombatFreeExperiences (BuildingType TEXT, UnitCombatType TEXT, Experience INTEGER);
CREATE TABLE Traits (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE, Description TEXT, ShortDescription TEXT,
  PlotCultureCostModifier INTEGER DEFAULT 0, LandUnitMaintenanceModifier INTEGER DEFAULT 0, FaithFromKills INTEGER DEFAULT 0,
  GreatGeneralRateModifier INTEGER DEFAULT 0, PlunderModifier INTEGER DEFAULT 0);
CREATE TABLE Trait_FreePromotionUnitCombats (TraitType TEXT, UnitCombatType TEXT, PromotionType TEXT);
CREATE TABLE Leaders (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE, Description TEXT, Civilopedia TEXT,
  CivilopediaTag TEXT, ArtDefineTag TEXT, VictoryCompetitiveness INTEGER, WonderCompetitiveness INTEGER,
  MinorCivCompetitiveness INTEGER, Boldness INTEGER, DiploBalance INTEGER, WarmongerHate INTEGER,
  DenounceWillingness INTEGER, DoFWillingness INTEGER, Loyalty INTEGER, Neediness INTEGER, Forgiveness INTEGER,
  Chattiness INTEGER, Meanness INTEGER, IconAtlas TEXT, PortraitIndex INTEGER);
CREATE TABLE Leader_Traits (LeaderType TEXT, TraitType TEXT);
CREATE TABLE Leader_MajorCivApproachBiases (LeaderType TEXT, MajorCivApproachType TEXT, Bias INTEGER);
CREATE TABLE Leader_MinorCivApproachBiases (LeaderType TEXT, MinorCivApproachType TEXT, Bias INTEGER);
CREATE TABLE Leader_Flavors (LeaderType TEXT, FlavorType TEXT, Flavor INTEGER);
CREATE TABLE Flavors (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE);
CREATE TABLE Civilizations (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT UNIQUE, Description TEXT, ShortDescription TEXT,
  Adjective TEXT, Civilopedia TEXT, CivilopediaTag TEXT, DefaultPlayerColor TEXT, ArtDefineTag TEXT, ArtStyleType TEXT,
  ArtStyleSuffix TEXT, ArtStylePrefix TEXT, DerivativeCiv TEXT, Playable BOOLEAN, AIPlayable BOOLEAN, PortraitIndex INTEGER,
  IconAtlas TEXT, AlphaIconAtlas TEXT, SoundtrackTag TEXT, MapImage TEXT, DawnOfManQuote TEXT, DawnOfManImage TEXT,
  DawnOfManAudio TEXT);
CREATE TABLE Civilization_Leaders (CivilizationType TEXT, LeaderheadType TEXT);
CREATE TABLE Civilization_FreeBuildingClasses (CivilizationType TEXT, BuildingClassType TEXT);
CREATE TABLE Civilization_FreeTechs (CivilizationType TEXT, TechType TEXT);
CREATE TABLE Civilization_FreeUnits (CivilizationType TEXT, UnitClassType TEXT, Count INTEGER, UnitAIType TEXT);
CREATE TABLE Civilization_Religions (CivilizationType TEXT, ReligionType TEXT);
CREATE TABLE Civilization_UnitClassOverrides (CivilizationType TEXT, UnitClassType TEXT, UnitType TEXT);
CREATE TABLE Civilization_BuildingClassOverrides (CivilizationType TEXT, BuildingClassType TEXT, BuildingType TEXT);
CREATE TABLE Civilization_Start_Region_Priority (CivilizationType TEXT, RegionType TEXT);
CREATE TABLE Civilization_Start_Along_Ocean (CivilizationType TEXT, StartAlongOcean BOOLEAN);
CREATE TABLE Civilization_CityNames (CivilizationType TEXT, CityName TEXT);
CREATE TABLE Civilization_SpyNames (CivilizationType TEXT, SpyName TEXT);
CREATE TABLE Diplomacy_Responses (LeaderType TEXT, ResponseType TEXT, Response TEXT, Bias INTEGER DEFAULT 1);
CREATE TABLE Audio_Sounds (SoundID TEXT UNIQUE, Filename TEXT, LoadType TEXT);
CREATE TABLE Audio_2DSounds (ScriptID TEXT UNIQUE, SoundID TEXT, SoundType TEXT, MinVolume INTEGER, MaxVolume INTEGER, IsMusic BOOLEAN);
CREATE TABLE Language_en_US (ID INTEGER PRIMARY KEY AUTOINCREMENT, Tag TEXT UNIQUE NOT NULL, Text TEXT, Gender TEXT, Plurality TEXT);
"""

BASE_DATA = """
INSERT INTO UnitPromotions (Type, PortraitIndex, IconAtlas) VALUES
 ('PROMOTION_DRILL_1', 1, 'PROMOTION_ATLAS'), ('PROMOTION_SHOCK_1', 2, 'PROMOTION_ATLAS'),
 ('PROMOTION_COVER_1', 3, 'PROMOTION_ATLAS'), ('PROMOTION_MOBILITY', 4, 'PROMOTION_ATLAS');
INSERT INTO Units (Type, Class, Combat, RangedCombat, Description, UnitArtInfo) VALUES
 ('UNIT_WARRIOR','UNITCLASS_WARRIOR',8,0,'TXT_KEY_UNIT_WARRIOR','ART_DEF_UNIT_WARRIOR'),
 ('UNIT_HORSEMAN','UNITCLASS_HORSEMAN',12,0,'TXT_KEY_UNIT_HORSEMAN','ART_DEF_UNIT_HORSEMAN'),
 ('UNIT_SPEARMAN','UNITCLASS_SPEARMAN',11,0,'TXT_KEY_UNIT_SPEARMAN','ART_DEF_UNIT_SPEARMAN'),
 ('UNIT_TREBUCHET','UNITCLASS_TREBUCHET',6,14,'TXT_KEY_UNIT_TREBUCHET','ART_DEF_UNIT_TREBUCHET'),
 ('UNIT_MUSKETMAN','UNITCLASS_MUSKETMAN',24,0,'TXT_KEY_UNIT_MUSKETMAN','ART_DEF_UNIT_MUSKETMAN'),
 ('UNIT_SWORDSMAN','UNITCLASS_SWORDSMAN',14,0,'TXT_KEY_UNIT_SWORDSMAN','ART_DEF_UNIT_SWORDSMAN'),
 ('UNIT_GREAT_WAR_INFANTRY','UNITCLASS_GREAT_WAR_INFANTRY',50,0,'TXT_KEY_UNIT_GWI','ART_DEF_UNIT_GREAT_WAR_INFANTRY');
INSERT INTO Unit_AITypes VALUES ('UNIT_HORSEMAN','UNITAI_ATTACK'),('UNIT_TREBUCHET','UNITAI_CITY_BOMBARD');
INSERT INTO Unit_ClassUpgrades VALUES ('UNIT_HORSEMAN','UNITCLASS_KNIGHT'),('UNIT_MUSKETMAN','UNITCLASS_RIFLEMAN');
INSERT INTO Unit_Flavors VALUES ('UNIT_HORSEMAN','FLAVOR_OFFENSE',5);
INSERT INTO Unit_FreePromotions VALUES ('UNIT_SPEARMAN','PROMOTION_ANTI_MOUNTED_I');
INSERT INTO Unit_ResourceQuantityRequirements VALUES ('UNIT_HORSEMAN','RESOURCE_HORSE',1);
INSERT INTO UnitGameplay2DScripts VALUES ('UNIT_HORSEMAN','AS2D_SELECT_HORSEMAN','AS2D_BIRTH_HORSEMAN');
INSERT INTO ArtDefine_UnitInfos VALUES ('ART_DEF_UNIT_CANNON'),('ART_DEF_UNIT_U_OTTOMAN_JANISSARY');
INSERT INTO Buildings (Type, BuildingClass, Cost, Description, Defense, ExtraCityHitPoints) VALUES
 ('BUILDING_SHRINE','BUILDINGCLASS_SHRINE',40,'x',0,0), ('BUILDING_LIBRARY','BUILDINGCLASS_LIBRARY',75,'x',0,0),
 ('BUILDING_MARKET','BUILDINGCLASS_MARKET',100,'x',0,0), ('BUILDING_TEMPLE','BUILDINGCLASS_TEMPLE',100,'x',0,0),
 ('BUILDING_WALLS','BUILDINGCLASS_WALLS',75,'x',500,50), ('BUILDING_PUBLIC_SCHOOL','BUILDINGCLASS_PUBLIC_SCHOOL',300,'x',0,0);
INSERT INTO Building_YieldChanges VALUES ('BUILDING_SHRINE','YIELD_FAITH',1),('BUILDING_LIBRARY','YIELD_SCIENCE',1),
 ('BUILDING_MARKET','YIELD_GOLD',2),('BUILDING_TEMPLE','YIELD_FAITH',2),('BUILDING_PUBLIC_SCHOOL','YIELD_SCIENCE',3);
INSERT INTO Building_YieldModifiers VALUES ('BUILDING_MARKET','YIELD_GOLD',25);
INSERT INTO Building_ClassesNeededInCity VALUES ('BUILDING_TEMPLE','BUILDINGCLASS_SHRINE'),('BUILDING_PUBLIC_SCHOOL','BUILDINGCLASS_UNIVERSITY');
INSERT INTO Civilizations (Type, ArtDefineTag, ArtStyleType, ArtStyleSuffix, ArtStylePrefix, SoundtrackTag, MapImage)
 VALUES ('CIVILIZATION_OTTOMAN','ART_DEF_CIVILIZATION_OTTOMAN','ARTSTYLE_MIDDLE_EAST','_AFRI','MIDDLE EAST','Ottoman','MapOttoman512.dds');
INSERT INTO Civilization_FreeBuildingClasses VALUES ('CIVILIZATION_OTTOMAN','BUILDINGCLASS_PALACE');
INSERT INTO Civilization_FreeTechs VALUES ('CIVILIZATION_OTTOMAN','TECH_AGRICULTURE');
INSERT INTO Civilization_FreeUnits VALUES ('CIVILIZATION_OTTOMAN','UNITCLASS_SETTLER',1,'UNITAI_SETTLE'),('CIVILIZATION_OTTOMAN','UNITCLASS_WARRIOR',1,'UNITAI_DEFENSE');
INSERT INTO Flavors (Type) VALUES ('FLAVOR_OFFENSE'),('FLAVOR_DEFENSE'),('FLAVOR_SCIENCE'),('FLAVOR_CULTURE'),('FLAVOR_EXPANSION'),('FLAVOR_GROWTH'),('FLAVOR_RELIGION'),('FLAVOR_GOLD');
"""


def run_sql(db, rel):
    with open(os.path.join(MOD, rel), encoding="utf-8") as fh:
        db.executescript(fh.read())


def run_xml(db, rel):
    root = ET.parse(os.path.join(MOD, rel)).getroot()
    for table in root:
        for row in table:
            if row.tag != "Row":
                continue
            cols = dict(row.attrib)
            for child in row:
                cols[child.tag] = child.text or ""
            keys = list(cols)
            db.execute("INSERT INTO %s (%s) VALUES (%s)" % (table.tag, ",".join(keys), ",".join("?" * len(keys))),
                       [cols[k] for k in keys])


def main():
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)
    db.executescript(BASE_DATA)
    run_xml(db, "Core/TL_Gameplay.xml")
    run_xml(db, "Text/TL_Text.xml")
    run_xml(db, "Core/TL_Extras.xml")
    run_xml(db, "Core/TL_Audio.xml")
    for rel in ["Core/TL_Units.sql", "Core/TL_Buildings.sql", "Core/TL_Civilizations.sql"]:
        run_sql(db, rel)

    q = lambda s: db.execute(s).fetchall()
    # birimler
    units = dict(q("SELECT Type, Combat FROM Units WHERE Type LIKE 'UNIT_TL_%'"))
    assert units == {"UNIT_TL_AKINCI": 12, "UNIT_TL_YAYA": 12, "UNIT_TL_SAHI_TOPU": 8, "UNIT_TL_TUFEKENDAZ": 26,
                     "UNIT_TL_GAZI": 15, "UNIT_TL_MEHMETCIK": 55}, units
    assert q("SELECT UnitArtInfo, RangedCombat FROM Units WHERE Type='UNIT_TL_SAHI_TOPU'") == [("ART_DEF_UNIT_CANNON", 18)]
    assert q("SELECT COUNT(*) FROM Unit_FreePromotions WHERE UnitType='UNIT_TL_YAYA'")[0][0] == 2
    ids = [r[0] for r in q("SELECT ID FROM Units ORDER BY ID")]
    assert ids == list(range(1, len(ids) + 1)), "ID'ler ardisik degil"
    # binalar
    b = q("SELECT Type, Defense FROM Buildings WHERE Type='BUILDING_TL_RIBAT'")
    assert b == [("BUILDING_TL_RIBAT", 800)], b
    assert q("SELECT Yield FROM Building_YieldChanges WHERE BuildingType='BUILDING_TL_KAPALICARSI' AND YieldType='YIELD_GOLD'") == [(4,)]
    assert q("SELECT COUNT(*) FROM Building_ClassesNeededInCity WHERE BuildingType='BUILDING_TL_KULLIYE'")[0][0] == 1
    # medeniyetler
    civs = q("SELECT Type, PortraitIndex, DawnOfManImage, SoundtrackTag FROM Civilizations WHERE Type LIKE 'CIVILIZATION_TL_%' ORDER BY PortraitIndex")
    assert len(civs) == 6, civs
    assert civs[5] == ("CIVILIZATION_TL_ATATURK", 5, "TL_Ataturk_DOM.dds", "TLTurk"), civs[5]
    assert q("SELECT COUNT(*) FROM Civilization_FreeUnits WHERE CivilizationType LIKE 'CIVILIZATION_TL_%'")[0][0] == 12
    assert q("SELECT COUNT(*) FROM Leader_MajorCivApproachBiases")[0][0] == 42
    assert q("SELECT Bias FROM Leader_MajorCivApproachBiases WHERE LeaderType='LEADER_TL_YAVUZ' AND MajorCivApproachType='MAJOR_CIV_APPROACH_WAR'") == [(9,)]
    assert q("SELECT Flavor FROM Leader_Flavors WHERE LeaderType='LEADER_TL_ATATURK' AND FlavorType='FLAVOR_SCIENCE'") == [(9,)]
    assert q("SELECT COUNT(*) FROM Civilization_UnitClassOverrides")[0][0] == 6
    assert q("SELECT COUNT(*) FROM Civilization_BuildingClassOverrides")[0][0] == 6
    assert q("SELECT ArtStylePrefix FROM Civilizations WHERE Type='CIVILIZATION_TL_OSMAN'") == [("MIDDLE EAST",)]
    # muzik: her betik bir sese, her ses var olan bir mp3 dosyasina bagli olmali
    for sid, fname in q("SELECT s.ScriptID, a.Filename FROM Audio_2DSounds s LEFT JOIN Audio_Sounds a ON s.SoundID = a.SoundID"):
        assert fname and os.path.exists(os.path.join(MOD, "Sounds", fname + ".mp3")), (sid, fname)
    assert q("SELECT COUNT(*) FROM Audio_2DSounds WHERE ScriptID LIKE 'SONG_TLTURK_WAR_%'")[0][0] == 1
    assert q("SELECT a.Filename FROM Audio_2DSounds s JOIN Audio_Sounds a ON s.SoundID=a.SoundID WHERE s.ScriptID LIKE 'SONG_TLTURK_WAR_%'") == [("TL_Music_Atak",)]
    # yardimci tablolar kaldirilmis olmali
    leftovers = q("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'TL_%'")
    assert leftovers == [], leftovers

    # tum TXT_KEY referanslarinin metni var mi?
    texts = {r[0] for r in q("SELECT Tag FROM Language_en_US")}
    refs = set()
    for table, cols in {
        "Units": ["Description", "Civilopedia", "Strategy", "Help"],
        "Buildings": ["Description", "Civilopedia", "Strategy", "Help"],
        "BuildingClasses": ["Description"],
        "UnitPromotions": ["Description", "Help"],
        "Traits": ["Description", "ShortDescription"],
        "Leaders": ["Description", "Civilopedia"],
        "Civilizations": ["Description", "ShortDescription", "Adjective", "Civilopedia", "DawnOfManQuote"],
        "Civilization_CityNames": ["CityName"],
        "Civilization_SpyNames": ["SpyName"],
    }.items():
        for col in cols:
            for (v,) in q("SELECT %s FROM %s" % (col, table)):
                if v and v.startswith("TXT_KEY_") and ("_TL_" in v):
                    refs.add(v)
    for (v,) in q("SELECT Response FROM Diplomacy_Responses"):
        refs.add(v.rstrip("%") + "_1")
    for (tag,) in q("SELECT CivilopediaTag FROM Leaders WHERE Type LIKE 'LEADER_TL_%'"):
        refs |= {tag + s for s in ("_NAME", "_SUBTITLE", "_LIVED", "_HEADING_1", "_TEXT_1")}
    for (tag,) in q("SELECT CivilopediaTag FROM Civilizations WHERE Type LIKE 'CIVILIZATION_TL_%'"):
        refs |= {tag + s for s in ("_HEADING_1", "_TEXT_1", "_FACTOID_HEADING", "_FACTOID_TEXT")}
    missing = sorted(refs - texts)
    assert not missing, "metni olmayan anahtarlar: %s" % missing
    print("SQL/XML testi: TAMAM (%d metin anahtari kontrol edildi)" % len(refs))


if __name__ == "__main__":
    main()
