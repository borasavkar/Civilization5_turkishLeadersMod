-- ============================================================
-- Turk Liderleri Modu - Lua yetenekleri
--  * Osman, Orhan, Ataturk: gorunmez yetenek binalarini tum sehirlere yerlestirir
--  * Fatih: fethedilen sehirde direnis yari yariya azalir, altin kazanilir
--  * Yavuz: fethedilen sehirden inanc kazanilir
-- ============================================================
print("Turk Liderleri: TL_Traits.lua yuklendi")

local DUMMY_BUILDINGS = {
	CIVILIZATION_TL_OSMAN   = "BUILDING_TL_DUMMY_OSMAN",
	CIVILIZATION_TL_ORHAN   = "BUILDING_TL_DUMMY_ORHAN",
	CIVILIZATION_TL_ATATURK = "BUILDING_TL_DUMMY_ATATURK",
}

local FATIH_GOLD_PER_POP = 10
local YAVUZ_FAITH_PER_POP = 15

local iFatihCiv = GameInfoTypes["CIVILIZATION_TL_FATIH"]
local iYavuzCiv = GameInfoTypes["CIVILIZATION_TL_YAVUZ"]

-- Oyuncu -> gorunmez bina ID'si
local g_PlayerDummy = {}

local function CacheDummies()
	for iPlayer = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
		local pPlayer = Players[iPlayer]
		if pPlayer ~= nil and pPlayer:IsEverAlive() then
			local civInfo = GameInfo.Civilizations[pPlayer:GetCivilizationType()]
			if civInfo ~= nil then
				local sBuilding = DUMMY_BUILDINGS[civInfo.Type]
				if sBuilding ~= nil and GameInfoTypes[sBuilding] ~= nil then
					g_PlayerDummy[iPlayer] = GameInfoTypes[sBuilding]
				end
			end
		end
	end
end

local function UpdateDummies(iPlayer)
	local iBuilding = g_PlayerDummy[iPlayer]
	if iBuilding == nil then return end
	local pPlayer = Players[iPlayer]
	if pPlayer == nil or not pPlayer:IsAlive() then return end
	for pCity in pPlayer:Cities() do
		if pCity:GetNumRealBuilding(iBuilding) == 0 then
			pCity:SetNumRealBuilding(iBuilding, 1)
		end
	end
end

local function Notify(pPlayer, sKey, sShortKey, pCity, iAmount)
	if pPlayer:IsHuman() and pPlayer:GetID() == Game.GetActivePlayer() then
		local sText = Locale.ConvertTextKey(sKey, pCity:GetName(), iAmount)
		local sShort = Locale.ConvertTextKey(sShortKey)
		pPlayer:AddNotification(NotificationTypes.NOTIFICATION_GENERIC, sText, sShort, pCity:GetX(), pCity:GetY())
	end
end

-- Her turun basinda (tum oyuncular icin)
GameEvents.PlayerDoTurn.Add(function(iPlayer)
	UpdateDummies(iPlayer)
end)

-- Yeni sehir kuruldugunda
GameEvents.PlayerCityFounded.Add(function(iPlayer, iX, iY)
	UpdateDummies(iPlayer)
end)

-- Sehir fethedildiginde
GameEvents.CityCaptureComplete.Add(function(iOldOwner, bIsCapital, iX, iY, iNewOwner)
	local pPlayer = Players[iNewOwner]
	if pPlayer == nil then return end
	UpdateDummies(iNewOwner)

	local pPlot = Map.GetPlot(iX, iY)
	if pPlot == nil then return end
	local pCity = pPlot:GetPlotCity()
	if pCity == nil then return end

	local iCiv = pPlayer:GetCivilizationType()
	local iPop = math.max(1, pCity:GetPopulation())

	if iFatihCiv ~= nil and iCiv == iFatihCiv then
		local iResistance = pCity:GetResistanceTurns()
		if iResistance > 1 then
			pCity:ChangeResistanceTurns(-math.floor(iResistance / 2))
		end
		local iGold = iPop * FATIH_GOLD_PER_POP
		pPlayer:ChangeGold(iGold)
		Notify(pPlayer, "TXT_KEY_TL_FATIH_CONQUEST", "TXT_KEY_TL_FATIH_CONQUEST_SHORT", pCity, iGold)
	end

	if iYavuzCiv ~= nil and iCiv == iYavuzCiv then
		local iFaith = iPop * YAVUZ_FAITH_PER_POP
		pPlayer:ChangeFaith(iFaith)
		Notify(pPlayer, "TXT_KEY_TL_YAVUZ_CONQUEST", "TXT_KEY_TL_YAVUZ_CONQUEST_SHORT", pCity, iFaith)
	end
end)

-- Oyun yuklendiginde mevcut sehirleri hemen guncelle
CacheDummies()
for iPlayer, _ in pairs(g_PlayerDummy) do
	UpdateDummies(iPlayer)
end
