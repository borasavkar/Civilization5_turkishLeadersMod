-- ============================================================
-- Turk Liderleri Modu - Benzersiz binalar
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
-- Medeniyetlere atama (yalnizca bina gercekten olustuysa)
-- Gorunmez yetenek binalari TL_Gameplay.xml dosyasindadir.
-- ------------------------------------------------------------
INSERT INTO Civilization_BuildingClassOverrides (CivilizationType, BuildingClassType, BuildingType)
SELECT c.CivType, b.BuildingClass, b.Type FROM Buildings b INNER JOIN (
	SELECT 'CIVILIZATION_TL_OSMAN' AS CivType, 'BUILDING_TL_ZAVIYE' AS BuildingType UNION ALL
	SELECT 'CIVILIZATION_TL_ORHAN', 'BUILDING_TL_MEDRESE' UNION ALL
	SELECT 'CIVILIZATION_TL_FATIH', 'BUILDING_TL_KAPALICARSI' UNION ALL
	SELECT 'CIVILIZATION_TL_YAVUZ', 'BUILDING_TL_KULLIYE' UNION ALL
	SELECT 'CIVILIZATION_TL_BATTAL', 'BUILDING_TL_RIBAT' UNION ALL
	SELECT 'CIVILIZATION_TL_ATATURK', 'BUILDING_TL_HALKEVI') c ON b.Type = c.BuildingType;
