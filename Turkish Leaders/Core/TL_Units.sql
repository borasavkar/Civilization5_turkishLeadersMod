-- ============================================================
-- Turk Liderleri Modu - Terfiler ve benzersiz birimler
-- Birimler, oyundaki temel birimin tum satiri kopyalanarak
-- olusturulur. Boylece BNW sutunlarinin hepsi dogru dolar.
-- Terfiler TL_Gameplay.xml dosyasindadir.
-- ============================================================

-- ------------------------------------------------------------
-- BENZERSIZ BIRIMLER (temel birimin satiri kopyalanir)
-- ------------------------------------------------------------
CREATE TABLE TL_UnitMap (NewType TEXT, BaseType TEXT, Tag TEXT);
INSERT INTO TL_UnitMap (NewType, BaseType, Tag) VALUES
	('UNIT_TL_AKINCI',      'UNIT_KNIGHT',             'AKINCI'),
	('UNIT_TL_YAYA',        'UNIT_SPEARMAN',           'YAYA'),
	('UNIT_TL_SAHI_TOPU',   'UNIT_TREBUCHET',          'SAHI_TOPU'),
	('UNIT_TL_TUFEKENDAZ',  'UNIT_MUSKETMAN',          'TUFEKENDAZ'),
	('UNIT_TL_GAZI',        'UNIT_SWORDSMAN',          'GAZI'),
	('UNIT_TL_MEHMETCIK',   'UNIT_GREAT_WAR_INFANTRY', 'MEHMETCIK');

CREATE TABLE TL_TmpUnits AS SELECT * FROM Units WHERE 0;
INSERT INTO TL_TmpUnits SELECT u.* FROM Units u INNER JOIN TL_UnitMap m ON u.Type = m.BaseType;
UPDATE TL_TmpUnits SET
	ID          = NULL,
	Description = 'TXT_KEY_UNIT_TL_'            || (SELECT Tag FROM TL_UnitMap WHERE BaseType = TL_TmpUnits.Type),
	Civilopedia = 'TXT_KEY_CIV5_UNIT_TL_'       || (SELECT Tag FROM TL_UnitMap WHERE BaseType = TL_TmpUnits.Type) || '_TEXT',
	Strategy    = 'TXT_KEY_UNIT_TL_'            || (SELECT Tag FROM TL_UnitMap WHERE BaseType = TL_TmpUnits.Type) || '_STRATEGY',
	Help        = 'TXT_KEY_UNIT_HELP_TL_'       || (SELECT Tag FROM TL_UnitMap WHERE BaseType = TL_TmpUnits.Type),
	Type        = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_TmpUnits.Type);
INSERT INTO Units SELECT * FROM TL_TmpUnits;
DROP TABLE TL_TmpUnits;

-- Yardimci tablolari kopyala
CREATE TABLE TL_Tmp AS SELECT * FROM Unit_AITypes WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Unit_AITypes t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO Unit_AITypes SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Unit_ClassUpgrades WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Unit_ClassUpgrades t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO Unit_ClassUpgrades SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Unit_Flavors WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Unit_Flavors t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO Unit_Flavors SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Unit_FreePromotions WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Unit_FreePromotions t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO Unit_FreePromotions SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM Unit_ResourceQuantityRequirements WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM Unit_ResourceQuantityRequirements t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO Unit_ResourceQuantityRequirements SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

CREATE TABLE TL_Tmp AS SELECT * FROM UnitGameplay2DScripts WHERE 0;
INSERT INTO TL_Tmp SELECT t.* FROM UnitGameplay2DScripts t INNER JOIN TL_UnitMap m ON t.UnitType = m.BaseType;
UPDATE TL_Tmp SET UnitType = (SELECT NewType FROM TL_UnitMap WHERE BaseType = TL_Tmp.UnitType);
INSERT INTO UnitGameplay2DScripts SELECT * FROM TL_Tmp;
DROP TABLE TL_Tmp;

DROP TABLE TL_UnitMap;

-- ------------------------------------------------------------
-- Birime ozel degisiklikler
-- ------------------------------------------------------------
-- Akinci (Sovalye yerine): +1 hareket
INSERT INTO Unit_FreePromotions (UnitType, PromotionType) VALUES ('UNIT_TL_AKINCI', 'PROMOTION_TL_AKINCI');

-- Yaya (Mizrakci yerine): 12 guc, ucretsiz Talim I
UPDATE Units SET Combat = Combat + 1 WHERE Type = 'UNIT_TL_YAYA';
INSERT INTO Unit_FreePromotions (UnitType, PromotionType) VALUES ('UNIT_TL_YAYA', 'PROMOTION_DRILL_1');

-- Sahi Topu (Mancinik yerine): daha guclu menzilli saldiri, top gorunumu
UPDATE Units SET RangedCombat = RangedCombat + 4, Combat = Combat + 2 WHERE Type = 'UNIT_TL_SAHI_TOPU';
UPDATE Units SET UnitArtInfo = 'ART_DEF_UNIT_CANNON'
WHERE Type = 'UNIT_TL_SAHI_TOPU' AND EXISTS (SELECT 1 FROM ArtDefine_UnitInfos WHERE Type = 'ART_DEF_UNIT_CANNON');

-- Tufekendaz (Tufekci yerine): +2 guc, atlilara karsi +%33, yeniceri gorunumu
UPDATE Units SET Combat = Combat + 2 WHERE Type = 'UNIT_TL_TUFEKENDAZ';
UPDATE Units SET UnitArtInfo = 'ART_DEF_UNIT_U_OTTOMAN_JANISSARY'
WHERE Type = 'UNIT_TL_TUFEKENDAZ' AND EXISTS (SELECT 1 FROM ArtDefine_UnitInfos WHERE Type = 'ART_DEF_UNIT_U_OTTOMAN_JANISSARY');
INSERT INTO Unit_FreePromotions (UnitType, PromotionType) VALUES ('UNIT_TL_TUFEKENDAZ', 'PROMOTION_TL_CALDIRAN');

-- Gazi (Kilicli yerine): +1 guc, ucretsiz Sok I
UPDATE Units SET Combat = Combat + 1 WHERE Type = 'UNIT_TL_GAZI';
INSERT INTO Unit_FreePromotions (UnitType, PromotionType) VALUES ('UNIT_TL_GAZI', 'PROMOTION_SHOCK_1');

-- Mehmetcik (Buyuk Savas Piyadesi yerine): +5 guc, Canakkale ruhu
UPDATE Units SET Combat = Combat + 5 WHERE Type = 'UNIT_TL_MEHMETCIK';
INSERT INTO Unit_FreePromotions (UnitType, PromotionType) VALUES ('UNIT_TL_MEHMETCIK', 'PROMOTION_TL_CANAKKALE');

-- ------------------------------------------------------------
-- Medeniyetlere atama (yalnizca birim gercekten olustuysa)
-- ------------------------------------------------------------
INSERT INTO Civilization_UnitClassOverrides (CivilizationType, UnitClassType, UnitType)
SELECT c.CivType, u.Class, u.Type FROM Units u INNER JOIN (
	SELECT 'CIVILIZATION_TL_OSMAN' AS CivType, 'UNIT_TL_AKINCI' AS UnitType UNION ALL
	SELECT 'CIVILIZATION_TL_ORHAN', 'UNIT_TL_YAYA' UNION ALL
	SELECT 'CIVILIZATION_TL_FATIH', 'UNIT_TL_SAHI_TOPU' UNION ALL
	SELECT 'CIVILIZATION_TL_YAVUZ', 'UNIT_TL_TUFEKENDAZ' UNION ALL
	SELECT 'CIVILIZATION_TL_BATTAL', 'UNIT_TL_GAZI' UNION ALL
	SELECT 'CIVILIZATION_TL_ATATURK', 'UNIT_TL_MEHMETCIK') c ON u.Type = c.UnitType;
