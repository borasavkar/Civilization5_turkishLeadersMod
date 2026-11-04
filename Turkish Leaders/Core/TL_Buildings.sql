-- ============================================================
-- Turk Liderleri Modu - Benzersiz binalar ve gorunmez yetenek binalari
-- ============================================================

-- ------------------------------------------------------------
-- BENZERSIZ BINALAR (temel binanin satiri kopyalanir)
-- ------------------------------------------------------------
CREATE TABLE TL_BuildingMap (NewType TEXT, BaseType TEXT, Tag TEXT);
INSERT INTO TL_BuildingMap (NewType, BaseType, Tag) VALUES
	('BUILDING_TL_ZAVIYE',      'BUILDING_SHRINE',        'ZAVIYE'),
	('BUILDING_TL_MEDRESE',     'BUILDING_LIBRARY',       'MEDRESE'),
	('BUILDING_TL_KAPALICARSI', 'BUILDING_MARKET',        'KAPALICARSI'),
	('BUILDING_TL_KULLIYE',     'BUILDING_TEMPLE',        'KULLIYE'),
	('BUILDING_TL_RIBAT',       'BUILDING_WALLS',         'RIBAT'),
	('BUILDING_TL_HALKEVI',     'BUILDING_PUBLIC_SCHOOL', 'HALKEVI');

CREATE TABLE TL_TmpBuildings AS SELECT * FROM Buildings WHERE 0;
INSERT INTO TL_TmpBuildings SELECT b.* FROM Buildings b INNER JOIN TL_BuildingMap m ON b.Type = m.BaseType;
UPDATE TL_TmpBuildings SET
	ID          = NULL,
	Description = 'TXT_KEY_BUILDING_TL_'      || (SELECT Tag FROM TL_BuildingMap WHERE BaseType = TL_TmpBuildings.Type),
	Civilopedia = 'TXT_KEY_BUILDING_TL_'      || (SELECT Tag FROM TL_BuildingMap WHERE BaseType = TL_TmpBuildings.Type) || '_PEDIA',
	Strategy    = 'TXT_KEY_BUILDING_TL_'      || (SELECT Tag FROM TL_BuildingMap WHERE BaseType = TL_TmpBuildings.Type) || '_STRATEGY',
	Help        = 'TXT_KEY_BUILDING_TL_'      || (SELECT Tag FROM TL_BuildingMap WHERE BaseType = TL_TmpBuildings.Type) || '_HELP',
	Type        = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_TmpBuildings.Type);
INSERT INTO Buildings SELECT * FROM TL_TmpBuildings;
DROP TABLE TL_TmpBuildings;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_YieldChanges WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_YieldChanges t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_YieldChanges SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_YieldModifiers WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_YieldModifiers t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_YieldModifiers SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_Flavors WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_Flavors t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_Flavors SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_ClassesNeededInCity WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_ClassesNeededInCity t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_ClassesNeededInCity SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_LocalResourceOrs WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_LocalResourceOrs t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_LocalResourceOrs SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Building_ResourceQuantityRequirements WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Building_ResourceQuantityRequirements t INNER JOIN TL_BuildingMap m ON t.BuildingType = m.BaseType;
UPDATE TL_Tmp SET BuildingType = (SELECT NewType FROM TL_BuildingMap WHERE BaseType = TL_Tmp.BuildingType);
INSERT INTO Building_ResourceQuantityRequirements SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

DROP TABLE TL_BuildingMap;

-- ------------------------------------------------------------
-- Binaya ozel degisiklikler
-- ------------------------------------------------------------
-- Zaviye (Tapinak/Shrine yerine): +1 Gida
INSERT INTO Building_YieldChanges (BuildingType, YieldType, Yield) VALUES ('BUILDING_TL_ZAVIYE', 'YIELD_FOOD', 1);

-- Medrese (Kutuphane yerine): +1 Kultur, +1 Bilim
UPDATE Building_YieldChanges SET Yield = Yield + 1 WHERE BuildingType = 'BUILDING_TL_MEDRESE' AND YieldType = 'YIELD_SCIENCE';
INSERT INTO Building_YieldChanges (BuildingType, YieldType, Yield) VALUES ('BUILDING_TL_MEDRESE', 'YIELD_CULTURE', 1);

-- Kapalicarsi (Pazar yerine): +2 Altin, +1 Mutluluk
UPDATE Building_YieldChanges SET Yield = Yield + 2 WHERE BuildingType = 'BUILDING_TL_KAPALICARSI' AND YieldType = 'YIELD_GOLD';
UPDATE Buildings SET Happiness = Happiness + 1 WHERE Type = 'BUILDING_TL_KAPALICARSI';

-- Kulliye (Mabet/Temple yerine): +1 Kultur, +1 Gida
INSERT INTO Building_YieldChanges (BuildingType, YieldType, Yield) VALUES
	('BUILDING_TL_KULLIYE', 'YIELD_CULTURE', 1),
	('BUILDING_TL_KULLIYE', 'YIELD_FOOD', 1);

-- Ribat (Sur yerine): daha guclu savunma, egitilen birimlere +15 deneyim
UPDATE Buildings SET Defense = Defense + 300, ExtraCityHitPoints = ExtraCityHitPoints + 25, Experience = Experience + 15
WHERE Type = 'BUILDING_TL_RIBAT';

-- Halkevi (Halk Okulu yerine): +2 Kultur
INSERT INTO Building_YieldChanges (BuildingType, YieldType, Yield) VALUES ('BUILDING_TL_HALKEVI', 'YIELD_CULTURE', 2);

-- ------------------------------------------------------------
-- GORUNMEZ YETENEK BINALARI
-- Lua betigi (TL_Traits.lua) bunlari ilgili medeniyetin
-- tum sehirlerine otomatik olarak yerlestirir.
-- ------------------------------------------------------------
INSERT INTO BuildingClasses (Type, DefaultBuilding, Description, NoLimit) VALUES
	('BUILDINGCLASS_TL_DUMMY_OSMAN',   'BUILDING_TL_DUMMY_OSMAN',   'TXT_KEY_BUILDING_TL_DUMMY_OSMAN',   1),
	('BUILDINGCLASS_TL_DUMMY_ORHAN',   'BUILDING_TL_DUMMY_ORHAN',   'TXT_KEY_BUILDING_TL_DUMMY_ORHAN',   1),
	('BUILDINGCLASS_TL_DUMMY_ATATURK', 'BUILDING_TL_DUMMY_ATATURK', 'TXT_KEY_BUILDING_TL_DUMMY_ATATURK', 1);

INSERT INTO Buildings (Type, BuildingClass, Cost, FaithCost, GreatWorkCount, GoldMaintenance, PrereqTech, Description, Help,
	NeverCapture, NukeImmune, ConquestProb, HurryCostModifier, MinAreaSize, IconAtlas, PortraitIndex)
VALUES
	('BUILDING_TL_DUMMY_OSMAN',   'BUILDINGCLASS_TL_DUMMY_OSMAN',   -1, -1, -1, 0, NULL, 'TXT_KEY_BUILDING_TL_DUMMY_OSMAN',   'TXT_KEY_BUILDING_TL_DUMMY_OSMAN_HELP',   1, 1, 0, -1, -1, 'BW_ATLAS_1', 19),
	('BUILDING_TL_DUMMY_ORHAN',   'BUILDINGCLASS_TL_DUMMY_ORHAN',   -1, -1, -1, 0, NULL, 'TXT_KEY_BUILDING_TL_DUMMY_ORHAN',   'TXT_KEY_BUILDING_TL_DUMMY_ORHAN_HELP',   1, 1, 0, -1, -1, 'BW_ATLAS_1', 19),
	('BUILDING_TL_DUMMY_ATATURK', 'BUILDINGCLASS_TL_DUMMY_ATATURK', -1, -1, -1, 0, NULL, 'TXT_KEY_BUILDING_TL_DUMMY_ATATURK', 'TXT_KEY_BUILDING_TL_DUMMY_ATATURK_HELP', 1, 1, 0, -1, -1, 'BW_ATLAS_1', 19);

-- Osman Bey: her sehirde +1 Gida
INSERT INTO Building_YieldChanges (BuildingType, YieldType, Yield) VALUES
	('BUILDING_TL_DUMMY_OSMAN', 'YIELD_FOOD', 1);

-- Orhan Gazi: yaya ve barutlu birimlerin uretimi +%25, bu birimlere +10 deneyim
INSERT INTO Building_UnitCombatProductionModifiers (BuildingType, UnitCombatType, Modifier) VALUES
	('BUILDING_TL_DUMMY_ORHAN', 'UNITCOMBAT_MELEE', 25),
	('BUILDING_TL_DUMMY_ORHAN', 'UNITCOMBAT_GUN',   25);
INSERT INTO Building_UnitCombatFreeExperiences (BuildingType, UnitCombatType, Experience) VALUES
	('BUILDING_TL_DUMMY_ORHAN', 'UNITCOMBAT_MELEE', 10),
	('BUILDING_TL_DUMMY_ORHAN', 'UNITCOMBAT_GUN',   10);

-- Ataturk: her sehirde Bilim ve Kultur +%10
INSERT INTO Building_YieldModifiers (BuildingType, YieldType, Yield) VALUES
	('BUILDING_TL_DUMMY_ATATURK', 'YIELD_SCIENCE', 10);
UPDATE Buildings SET CultureRateModifier = 10 WHERE Type = 'BUILDING_TL_DUMMY_ATATURK';
