-- ============================================================
-- Turk Liderleri Modu - Terfiler ve benzersiz birimler
-- Birimler, oyundaki temel birimin tum satiri kopyalanarak
-- olusturulur; boylece BNW'deki tum sutunlar dogru dolar.
-- ============================================================

-- ------------------------------------------------------------
-- TERFILER
-- ------------------------------------------------------------
-- Fatih: Kusatma ustaligi (kusatma birimleri sehirlere karsi +%30)
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry, CityAttack)
SELECT 'PROMOTION_TL_FATIH_SIEGE', 'TXT_KEY_PROMOTION_TL_FATIH_SIEGE', 'TXT_KEY_PROMOTION_TL_FATIH_SIEGE_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_FATIH_SIEGE', 30
FROM UnitPromotions WHERE Type IN ('PROMOTION_SIEGE', 'PROMOTION_DRILL_1') ORDER BY (Type = 'PROMOTION_DRILL_1') LIMIT 1;

-- Battal Gazi: Akinci ruhu (dost topraklar disinda +%15 savas gucu)
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry, OutsideFriendlyLandsModifier)
SELECT 'PROMOTION_TL_BATTAL_RAIDER', 'TXT_KEY_PROMOTION_TL_BATTAL_RAIDER', 'TXT_KEY_PROMOTION_TL_BATTAL_RAIDER_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_BATTAL_RAIDER', 15
FROM UnitPromotions WHERE Type = 'PROMOTION_SHOCK_1';

-- Ataturk: Vatan savunmasi (dost topraklarda +%15 savas gucu)
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry, FriendlyLandsModifier)
SELECT 'PROMOTION_TL_ATATURK_HOMELAND', 'TXT_KEY_PROMOTION_TL_ATATURK_HOMELAND', 'TXT_KEY_PROMOTION_TL_ATATURK_HOMELAND_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_ATATURK_HOMELAND', 15
FROM UnitPromotions WHERE Type = 'PROMOTION_DRILL_1';

-- Akinci: +1 hareket
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry, MovesChange)
SELECT 'PROMOTION_TL_AKINCI', 'TXT_KEY_PROMOTION_TL_AKINCI', 'TXT_KEY_PROMOTION_TL_AKINCI_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_AKINCI', 1
FROM UnitPromotions WHERE Type IN ('PROMOTION_MOBILITY', 'PROMOTION_DRILL_1') ORDER BY (Type = 'PROMOTION_DRILL_1') LIMIT 1;

-- Tufekendaz: Caldiran (atli birimlere karsi +%33)
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry)
SELECT 'PROMOTION_TL_CALDIRAN', 'TXT_KEY_PROMOTION_TL_CALDIRAN', 'TXT_KEY_PROMOTION_TL_CALDIRAN_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_CALDIRAN'
FROM UnitPromotions WHERE Type IN ('PROMOTION_ANTI_MOUNTED_I', 'PROMOTION_DRILL_1') ORDER BY (Type = 'PROMOTION_DRILL_1') LIMIT 1;

INSERT INTO UnitPromotions_UnitCombatMods (PromotionType, UnitCombatType, Modifier) VALUES
	('PROMOTION_TL_CALDIRAN', 'UNITCOMBAT_MOUNTED', 33);

-- Mehmetcik: Canakkale ruhu (dost topraklarda +%25 savas gucu)
INSERT INTO UnitPromotions (Type, Description, Help, Sound, CannotBeChosen, PortraitIndex, IconAtlas, PediaType, PediaEntry, FriendlyLandsModifier)
SELECT 'PROMOTION_TL_CANAKKALE', 'TXT_KEY_PROMOTION_TL_CANAKKALE', 'TXT_KEY_PROMOTION_TL_CANAKKALE_HELP',
	'AS2D_IF_LEVELUP', 1, PortraitIndex, IconAtlas, 'PEDIA_ATTRIBUTES', 'TXT_KEY_PROMOTION_TL_CANAKKALE', 25
FROM UnitPromotions WHERE Type = 'PROMOTION_COVER_1';

-- ------------------------------------------------------------
-- BENZERSIZ BIRIMLER (temel birimin satiri kopyalanir)
-- ------------------------------------------------------------
CREATE TABLE TL_UnitMap (NewType TEXT, BaseType TEXT, Tag TEXT);
INSERT INTO TL_UnitMap (NewType, BaseType, Tag) VALUES
	('UNIT_TL_AKINCI',      'UNIT_HORSEMAN',           'AKINCI'),
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
-- Kayi Akincisi (Atli yerine): +1 hareket
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
