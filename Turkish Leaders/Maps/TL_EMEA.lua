------------------------------------------------------------------------------
--	FILE:	 TL_EMEA.lua
--	AUTHOR:  Turk Liderleri Modu
--	PURPOSE: Avrupa, Orta Dogu, Arabistan ve Afrika'yi kapsayan sabit harita.
--	         Arazi verisi Natural Earth (kamu mali) kullanilarak tools/build_map.py
--	         ile uretilmistir. Bu dosya otomatik olusturulur; tools/map_template.lua
--	         dosyasini duzenleyin.
------------------------------------------------------------------------------
include("MapGenerator");
include("FeatureGenerator");
include("TerrainGenerator");
include("AssignStartingPlots");

-- Kaynak: Natural Earth (kamu mali). Satirlar kuzeyden guneye siralidir.
TL_EMEA = {}
TL_EMEA.Width = 100
TL_EMEA.Height = 90
TL_EMEA.LonMin = -25.0
TL_EMEA.LonMax = 75.0
TL_EMEA.LatMin = -36.0
TL_EMEA.LatMax = 72.0
TL_EMEA.Rows = {
"tt~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~tt~~~~~~~~~~~~tttts~ss",
"ts~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ttssttttt~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ttttss~T",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~tTTTtTtttttttTTtttt~~~~~~~~~~~~t~~~~~~~~~~~pppttt~~pttt~~p",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PTTMttTttttttttttttttTttt~~~~Tt~~~ttttTttppttttttttTtttttt~t",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~tTTTttttttttttttptttttttttt~~~~ttttttttttTttttttttTttttTtt~ttt",
"~~ttttttttt~~~~~~~~~~~~~~~~~~~~~~~~~~TtMMtTtttt~~~tttTpPttTt~~~~~tppttttttttttttttTttTTtTttttttTtttT",
"~~~tttTtt~~~~~~~~~~~~~~~~~~~~~~~~~~tTMMtttttt~~~pptTTtTtttttttttttttttttttTtttttttTTTttttttttTtttttt",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ppPMMPppppt~~~pggggGgGggptttppppppttpPpPttpggpTtttptTttttttppgGgggpt",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gPpppMttpppt~~~~gGgggG~gpppttp~ppppptpPpppppgggppppppPtttTtpppgggppppp",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pMPPptttTtttt~~~gGgPppPppp~~pppppggPttpppgggggggppgggPptttppgggggpTtpp",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pPMpptttttttt~~~~~~PptpppppppppppgpptppppGggggggpPggGppppppggGgGgpttpP",
"~~~~~~~~~~~~~~~~~~~~g~~~~~~~~~~~p~~~pppppT~~~~~~~gggGggppttpPpppppppPggpPppggPpppppPGgGgggggggggggpP",
"~~~~~~~~~~~~~~~~~~pPpp~~~~~~~~~~~~g~~pggg~~~~~gpppppppGgggggGggGgGggppPgGgggggggggMPMPppppppppppppgg",
"~~~~~~~~~~~~~~~~~~~~gPp~~~~~~~~~~gg~~~g~~~~~~~ggpppppggggggggggggGgggppgpPppppppppPPMgpppgggpppgggpp",
"~~~~~~~~~~~~~~~~ggg~~ggp~~~~~~~~~pp~~~~~~gg~gggGpgggggggggggGGggggggggggppPppppppPpMppppppggpPpgggpp",
"~~~~~~~~~~~~~~~Gggg~~~ggp~~~~~~ppppgggggggggggggggggggggggGGgGggggggggggppppppppPPppppppPpggppppggpp",
"~~~~~~~~~~~~~~ppgg~~gggppg~~~ggggggggGgggggggggggggggggGggggGGgggpppggggppPppppPpPPpppppppPppPpppppp",
"~~~~~~~~~~~~~~~~~~~~~pppgg~gGgggggggpPpggggggggGGggggggGgGggGggGGppppppgpppggpppppppppPppppppppppppp",
"~~~~~~~~~~~~~~~~~~~~~~~~~gGgggGggggggggggGgGMGggggggggggggGggGggggggggGgPPggpppppppPppppppPpppppPPpP",
"~~~~~~~~~~~~~~~~~~~~~ggggggggggGgppggGggggggMMMgGggggGggggggggGgggggggggpGGgggPppppppppppppppgggGGPp",
"~~~~~~~~~~~~~~~~~~~~~~gggggggGgggPMGMggGGPpPPppMMMggggggggggggGgggggggggppggggppppppppppPppppGGGgpPp",
"~~~~~~~~~~~~~~~~~~~~~~~~gGgGgggMgMGMGMgpppppgggGGGGMgggg~ggg~~~gggggggggPp~~~~ggpppppDddddpppDdddppp",
"~~~~~~~~~~~~~~~~~~~~~~~ggGgggpMMggggg~pPMPppGGgpPGgggg~~~~pg~~GGGpppgggg~~~~ppgGppppDddddddpDpdddpPp",
"~~~~~~~~~~~~~~~~~~~~~~~pppppgggMg~~pMM~~~gGGgpPggGgpp~~~~~~~~~~~PGMGMppp~~~~ddppPppddddddddddpDddddp",
"~~~~~~~~~~~~~~~GgGGGppPpMMPG~~~~~p~~gGg~~~~GGGGggGGg~~~~~~~~~~~~~~gGPPPg~~~~~ddddddDddDddddddpppppMM",
"~~~~~~~~~~~~~~~~GgGgpPpppPP~~~~~~~~~~~gPg~~~ggggGgggg~~~~PpMg~~~~~ggpPpgPp~~~~~ddddddddDddddDdpppPMP",
"~~~~~~~~~~~~~~~~gggggppPP~~~~~~~~g~~~~~~p~~~pPpp~~~~~pppppPggppPppMPpPPppp~~~~ddddddddddddddppppppMP",
"~~~~~~~~~~~~~~~~PGGgGGgpp~~~~~~~~~~~~~~~~P~~~~Pp~~~pPpppggGGGgpPPPPpPpppdd~~~~dddddddDddddddddddMPPd",
"~~~~~~~~~~~~~~~~ggggGGgP~~~~~~~~~~~~~~gG~~~~~~pp~~~ppppPppPMMMpPMpPpPpppdd~~~~dddddddddddddddpppMMpM",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~pMGGGMMMg~~~~~~~~~~~~~~~~~~DP~PP~~ppdppggPDdddddMddPMppppppdddddpgGMgGGGM",
"~~~~~~~~~~~~~~~~~~gg~~~pPPPPpgMGGgg~~~~~~~~~~~~~~~~~~~~~~~~~ppPDpGggdddddddddppPpPMpPppdddpPGGGMGGgG",
"~~~~~~~~~~~~~~~~~~PPGGGMPPPpMgdddDM~~~~~~~~~~~~~~~~~~~~~~~~~~GgdddggggpMDDdDdddddDpppPMppddPpppggggg",
"~~~~~~~~~~~~~~~~dMdMMPPPDddddddddddp~~~~~~~~~~~~~~~~~~~~~~~~GddddDddggpdDDPpMddddddPpppppdpppppggGGg",
"~~~~~~~~~~~~~~~PPPppPMPMddddddddddDddppp~~~~~ddddd~~~~~~~~~~ggddddddppppddpPpPDdddddpppppdDppPpppggg",
"~~~~~~~~~~~~~~~pPPPpddDdddDDddddDdddddddppP~ddddpDdDdddPdppgGddddddddDddddDMMdDddddddDdddPggppppppGg",
"~~~~~~~~~~~~~~~pPMdDddddddddDddddddddddddddddddDdddddddppggGGdddddddddddd~~~MDdddddddddddpppGggggddd",
"~~~~~~~~~~~~~gdddddddddddddddddDdddDdDddddddddDdDddddddpddggMdddddddddddd~~~DDdDDdddddddDpGPppddddDd",
"~~~~~~~~~~~~DdddddddddddddddddddddddddddddddDddddddddddppdD~~DDdddddddddDdD~~~dMP~dDDddddppGpppddddg",
"~~~~~~~~~~dDdddddDddddddDdddDDdDddDdddddddddddddddddddDpPDd~~dDddDddddddddD~~~~~~~DdddppppggPddddggg",
"~~~~~~~~~~ddddddddddddddddMMdDddddddddddddddddDddddDddddppdd~~~dMDddDddDdDDdd~~~DP~~~~~~~~~~ggdggggg",
"~~~~~~~~gdddddddDddddddddddddDMDMddddddddddMddddddDdddddppDD~~~DDdddddddddddddDdpPp~~~~~~~~~~ggggggg",
"~~~~~~~~ddddddddddddDddddddddddMdddddDddddDDMdddddddDdDddpdDdd~~ddddDddddddddddddpppd~~~~~~~~~gGgGgG",
"~~~~~~~~DddDDdddddddddddpdddddDdDddddddddDMMddddddddddDddddddd~~dMMddddddddddddddpp~~~~~~~~~~~~g~ggg",
"~~~~~~~~~dddddddddDddDdddDdDdddddMdddddddddMDddddddddddddddddd~~~~MMdddDDddddddddPp~~~~~~~~~~~~~~~Mg",
"~~~~~~~~dddddDdDddddDddddddDdddddMdddddddddddDdddddddddddddddd~~~~dDddddDdddddddP~~~~~~~~~~~~~~~~GGg",
"~~~~~~~~~dddddDddddddddddddddddddddddddDdddddddddddddDdddddDddDP~~~ppgdddddddddd~~~~~~~~~~~~~~~~~~Mg",
"~~~~~~~~dddddddddddddpdDdddddddddddDdddddDddDddddDddddddddddddMp~~~pPdddddDDd~~~~~~~~~~~~~~~~~~~~~Gg",
"~~~~~~~~pppdddppppddpdddddddDdddDddddddddddddddddddddDdddddddpdMP~~~PpddDDP~~~~~~~~~~~~~~~~~~~~~~~~M",
"~~~~~~~~ppppgppppppppppppppppppppdddDdddDdddddddddddddddDdddppPMMp~~PddD~~~~~~~~~~~~~~~~~~~~~~~~~~~G",
"~~~~~~~~~PppggppppggpppPpppppppppppPppDddddDdddDddddDddddddDpPMMPpgg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~pppgpppppgpppppggppppppppppppDdgdgdddDdddddddddddgpMpPpgppp~~~~~~Pp~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~GggggggggggGGpppggggggggggGpDdpgggdgdgddDddddddDGGGGGGGpppppppppp~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~gggppgggggggpPpGggGggggggppppgGggggggggGgggggggggMGGGMpPppppddpp~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~GgppPggggggGppggggGgggggPpPPPgggGGgggggGgggggGggGgggMPppppppDdp~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~ppppgggggggpggGgGppggGGpPppPGgggPgggggggggggpppPggggppppppDdd~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~pppppGGGGg~~~~~ppggGggpPpPggggppgggggggggggggppMMMgppPppddd~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gggggggggggggGGgggGgggggggggGggGpdppppd~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gggggggggggGGGGppPGgggggggMMgggdDdppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gggggggGGggGggpPpPgggggggggMgpgdddp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ggggGGgggggGpppppgGGggggggGgPpgdd~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gGggGggggggggppppggGgg~~~ggGPpGdd~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GMGgggggggggggpppgGGggg~~ggGgppg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MGMGgggggggggppgggPpggGgggGgPg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~gggggggggggggggGgG~pGggggGpPp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pppgggggGgGggGgggggggggMPpp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MPpgggggggggggggGggggggPpp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MMgggGggggpgggGGgggggggggg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pgGgGgggggPPGggGGGgggggggg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ppppPgppggGgPpppppPpppppppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PpPpGgppGggGGGGggpPP~ggppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PppppGPppgggggGgGppppPgpppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddDpppGGPPpgGGgggGMppPpPppppp~~~~~~~Pp~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~dddpppgPppggggggMPppppppppGg~~~~~~~pMg~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddDdpdppppppggggMPppppppppgg~~~~~gppPg~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~dddddDdpppppppgMgPppGggggp~~~~~~~pggMg~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddpddDpppppppgGgpPPggggg~~~~~~~~pggGg~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~dppdddpppPppgggggpppppp~~~~~~~~~GGgg~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ppdddpppppPgGgggpPppp~~~~~~~~~ggGM~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~dpddddDdddggggpppppPp~~~~~~~~GGpPp~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddpddddDdddgggppMpPpgg~~~~~~~~ppPp~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddppdddddddgggpPMpPgg~~~~~~~~pppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddpgddddddpggppPPp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddDDddddDdggpppMp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddppdddddppppPMMp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ddppppdpdpppMGG~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ppppppppppMGgg~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pppppMPPpPP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pppPpPPMMP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~pppp~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
}

------------------------------------------------------------------------------
-- Yardimcilar
------------------------------------------------------------------------------
local function TL_Char(x, y)
	-- y = 0 guney satiridir; Rows tablosu kuzeyden guneye siralidir.
	local row = TL_EMEA.Rows[TL_EMEA.Height - y];
	if row == nil then return "~"; end
	local c = string.sub(row, x + 1, x + 1);
	if c == nil or c == "" then return "~"; end
	return c;
end

local function TL_Latitude(y)
	local dLat = (TL_EMEA.LatMax - TL_EMEA.LatMin) / TL_EMEA.Height;
	return TL_EMEA.LatMin + (y + 0.5) * dLat;
end

local function TL_LonLatToXY(lon, lat)
	local dLon = (TL_EMEA.LonMax - TL_EMEA.LonMin) / TL_EMEA.Width;
	local dLat = (TL_EMEA.LatMax - TL_EMEA.LatMin) / TL_EMEA.Height;
	local y = math.floor((lat - TL_EMEA.LatMin) / dLat);
	local shift = 0;
	if y % 2 == 1 then shift = 0.5; end
	local x = math.floor((lon - TL_EMEA.LonMin) / dLon - shift);
	if x < 0 then x = 0; end
	if x > TL_EMEA.Width - 1 then x = TL_EMEA.Width - 1; end
	if y < 0 then y = 0; end
	if y > TL_EMEA.Height - 1 then y = TL_EMEA.Height - 1; end
	return x, y;
end

------------------------------------------------------------------------------
function GetMapScriptInfo()
	local world_age, temperature, rainfall, sea_level, resources = GetCoreMapOptions();
	return {
		Name = "TXT_KEY_TL_MAP_EMEA",
		Description = "TXT_KEY_TL_MAP_EMEA_HELP",
		IsAdvancedMap = false,
		SupportsMultiplayer = true,
		IconIndex = 5,
		CustomOptions = {
			{
				Name = "TXT_KEY_TL_MAP_OPTION_START",
				Values = {
					"TXT_KEY_TL_MAP_OPTION_START_HISTORIC",
					"TXT_KEY_TL_MAP_OPTION_START_RANDOM",
				},
				DefaultValue = 1,
				SortPriority = 1,
			},
			resources,
		},
	};
end
------------------------------------------------------------------------------
function GetMapInitData(worldSize)
	return {
		Width = TL_EMEA.Width,
		Height = TL_EMEA.Height,
		WrapX = false,
	};
end
------------------------------------------------------------------------------
function GeneratePlotTypes()
	print("Turk Liderleri haritasi: arazi tipleri olusturuluyor...");
	local plotTypes = {};
	local w, h = TL_EMEA.Width, TL_EMEA.Height;
	for y = 0, h - 1 do
		for x = 0, w - 1 do
			local i = y * w + x;
			local c = TL_Char(x, y);
			if c == "~" then
				plotTypes[i] = PlotTypes.PLOT_OCEAN;
			elseif c == "M" then
				plotTypes[i] = PlotTypes.PLOT_MOUNTAIN;
			elseif c == "G" or c == "P" or c == "D" or c == "T" then
				plotTypes[i] = PlotTypes.PLOT_HILLS;
			else
				plotTypes[i] = PlotTypes.PLOT_LAND;
			end
		end
	end
	SetPlotTypes(plotTypes);
	local args = {expansion_diceroll_table = {10, 6, 4}};
	GenerateCoasts(args);
end
------------------------------------------------------------------------------
local TERRAIN_BY_CHAR = {
	g = "TERRAIN_GRASS",  G = "TERRAIN_GRASS",
	p = "TERRAIN_PLAINS", P = "TERRAIN_PLAINS",
	d = "TERRAIN_DESERT", D = "TERRAIN_DESERT",
	t = "TERRAIN_TUNDRA", T = "TERRAIN_TUNDRA",
	s = "TERRAIN_SNOW",
};

local function MountainTerrain(x, y)
	-- Dag altindaki zemini komsu karelere gore sec
	local counts = {};
	for dy = -1, 1 do
		for dx = -1, 1 do
			local c = TL_Char(x + dx, y + dy);
			local tt = TERRAIN_BY_CHAR[c];
			if tt ~= nil then
				counts[tt] = (counts[tt] or 0) + 1;
			end
		end
	end
	local best, bestN = "TERRAIN_PLAINS", 0;
	for tt, n in pairs(counts) do
		if n > bestN then best, bestN = tt, n; end
	end
	return best;
end

function GenerateTerrain()
	print("Turk Liderleri haritasi: zemin olusturuluyor...");
	local terrainTypes = {};
	local w, h = TL_EMEA.Width, TL_EMEA.Height;
	for y = 0, h - 1 do
		for x = 0, w - 1 do
			local i = y * w + x;
			local plot = Map.GetPlot(x, y);
			local c = TL_Char(x, y);
			if plot:IsWater() then
				terrainTypes[i] = plot:GetTerrainType();
			else
				local sType = TERRAIN_BY_CHAR[c];
				if c == "M" then sType = MountainTerrain(x, y); end
				if sType == nil then sType = "TERRAIN_PLAINS"; end
				terrainTypes[i] = GameInfoTypes[sType];
			end
		end
	end
	SetTerrainTypes(terrainTypes);
end
------------------------------------------------------------------------------
function AddLakes()
	-- Gercek goller harita verisinde var; rastgele gol eklenmez.
end
------------------------------------------------------------------------------
function AddFeatures()
	print("Turk Liderleri haritasi: ormanlar, cengeller ve vahalar ekleniyor...");
	local featuregen = FeatureGenerator.Create({rainfall = 2});
	-- Ozellik ureticisinin enlem hesabini haritanin gercek enlemlerine bagla.
	featuregen.GetLatitudeAtPlot = function(self, iX, iY)
		return math.min(1, math.abs(TL_Latitude(iY)) / 90);
	end
	featuregen:AddFeatures();
end
------------------------------------------------------------------------------
-- Tarihi baslangic noktalari (boylam, enlem). Listede sira onceligi belirler.
local TL_START_LOCATIONS = {
	{"CIVILIZATION_TL_FATIH",   28.9, 41.0},  -- Istanbul
	{"CIVILIZATION_TL_ATATURK", 32.9, 39.9},  -- Ankara
	{"CIVILIZATION_TL_BATTAL",  38.3, 38.4},  -- Malatya
	{"CIVILIZATION_TL_YAVUZ",   31.2, 30.0},  -- Kahire
	{"CIVILIZATION_TL_OSMAN",   30.0, 40.1},  -- Sogut
	{"CIVILIZATION_TL_ORHAN",   26.7, 40.9},  -- Gelibolu / Rumeli
	{"CIVILIZATION_OTTOMAN",    26.6, 41.7},  -- Edirne
	{"CIVILIZATION_BYZANTIUM",  28.9, 41.0},  -- Konstantinopolis
	{"CIVILIZATION_GREECE",     23.7, 38.0},  -- Atina
	{"CIVILIZATION_ROME",       12.5, 41.9},  -- Roma
	{"CIVILIZATION_VENICE",     12.3, 45.4},  -- Venedik
	{"CIVILIZATION_ENGLAND",    -0.1, 51.5},  -- Londra
	{"CIVILIZATION_CELTS",      -4.0, 53.5},  -- Galler / Irlanda
	{"CIVILIZATION_FRANCE",      2.3, 48.9},  -- Paris
	{"CIVILIZATION_SPAIN",      -3.7, 40.4},  -- Madrid
	{"CIVILIZATION_PORTUGAL",   -9.1, 38.7},  -- Lizbon
	{"CIVILIZATION_NETHERLANDS", 4.9, 52.4},  -- Amsterdam
	{"CIVILIZATION_GERMANY",    13.4, 52.5},  -- Berlin
	{"CIVILIZATION_AUSTRIA",    16.4, 48.2},  -- Viyana
	{"CIVILIZATION_HUNS",       19.0, 47.0},  -- Pannonya
	{"CIVILIZATION_POLAND",     21.0, 52.2},  -- Varsova
	{"CIVILIZATION_DENMARK",    12.6, 55.7},  -- Kopenhag
	{"CIVILIZATION_SWEDEN",     18.1, 59.3},  -- Stokholm
	{"CIVILIZATION_RUSSIA",     37.6, 55.8},  -- Moskova
	{"CIVILIZATION_CARTHAGE",   10.3, 36.9},  -- Kartaca
	{"CIVILIZATION_MOROCCO",    -8.0, 31.6},  -- Marakes
	{"CIVILIZATION_EGYPT",      32.6, 25.7},  -- Teb
	{"CIVILIZATION_ARABIA",     39.8, 21.4},  -- Mekke
	{"CIVILIZATION_PERSIA",     52.9, 29.9},  -- Persepolis
	{"CIVILIZATION_BABYLON",    44.4, 32.5},  -- Babil
	{"CIVILIZATION_ASSYRIA",    43.2, 36.4},  -- Ninova
	{"CIVILIZATION_ETHIOPIA",   38.7, 14.1},  -- Aksum
	{"CIVILIZATION_SONGHAI",    -0.0, 16.3},  -- Gao
	{"CIVILIZATION_ZULU",       31.0, -28.5}, -- Zululand
	{"CIVILIZATION_MONGOL",     68.0, 47.0},  -- Bozkir (harita disi; dogu ucu)
	{"CIVILIZATION_INDIA",      72.0, 27.0},  -- Kuzeybati Hindistan
};

function TL_Neighbors(x, y)
	if y % 2 == 0 then
		return {{x-1, y}, {x+1, y}, {x-1, y+1}, {x, y+1}, {x-1, y-1}, {x, y-1}};
	end
	return {{x-1, y}, {x+1, y}, {x, y+1}, {x+1, y+1}, {x, y-1}, {x+1, y-1}};
end

local function IsValidStart(plot)
	if plot == nil then return false; end
	if plot:IsWater() or plot:IsMountain() or plot:IsImpassable() then return false; end
	local terrain = plot:GetTerrainType();
	if terrain == GameInfoTypes.TERRAIN_SNOW then return false; end
	if plot:GetFeatureType() == GameInfoTypes.FEATURE_ICE then return false; end
	return true;
end

local function StartScore(plot, iDist)
	local score = 100 - iDist * 10;
	local terrain = plot:GetTerrainType();
	if terrain == GameInfoTypes.TERRAIN_GRASS or terrain == GameInfoTypes.TERRAIN_PLAINS then score = score + 15; end
	if terrain == GameInfoTypes.TERRAIN_DESERT then
		score = score - 10;
		if plot:IsRiver() then score = score + 15; end
	end
	if terrain == GameInfoTypes.TERRAIN_TUNDRA then score = score - 15; end
	if plot:IsRiver() then score = score + 10; end
	if plot:IsCoastalLand() then score = score + 8; end
	if plot:IsHills() then score = score + 5; end
	return score;
end

local function ApplyHistoricStarts(start_plot_database)
	local MIN_DISTANCE = 6;
	local MAX_RADIUS = 18;

	-- Hangi oyuncunun hangi medeniyet oldugunu bul
	local civToPlayers = {};
	for iPlayer = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
		local pPlayer = Players[iPlayer];
		if pPlayer ~= nil and pPlayer:IsEverAlive() then
			local civInfo = GameInfo.Civilizations[pPlayer:GetCivilizationType()];
			if civInfo ~= nil then
				civToPlayers[civInfo.Type] = civToPlayers[civInfo.Type] or {};
				table.insert(civToPlayers[civInfo.Type], iPlayer);
			end
		end
	end

	-- Tarihi konumu olan oyunculari belirle
	local relocate = {};
	local isRelocated = {};
	for _, entry in ipairs(TL_START_LOCATIONS) do
		local list = civToPlayers[entry[1]];
		if list ~= nil then
			for _, iPlayer in ipairs(list) do
				if not isRelocated[iPlayer] then
					table.insert(relocate, {iPlayer, entry[2], entry[3]});
					isRelocated[iPlayer] = true;
				end
			end
		end
	end
	if #relocate == 0 then return; end

	-- Sabit kalan oyuncularin baslangic noktalari
	local taken = {};
	for iPlayer = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
		local pPlayer = Players[iPlayer];
		if pPlayer ~= nil and pPlayer:IsEverAlive() and not isRelocated[iPlayer] then
			local plot = pPlayer:GetStartingPlot();
			if plot ~= nil then table.insert(taken, {plot:GetX(), plot:GetY()}); end
		end
	end

	local w, h = TL_EMEA.Width, TL_EMEA.Height;
	for _, r in ipairs(relocate) do
		local iPlayer, lon, lat = r[1], r[2], r[3];
		local tx, ty = TL_LonLatToXY(lon, lat);
		local bestPlot, bestScore = nil, -9999;

		-- Hedef suda ise en yakin kara karesinden basla
		local sx, sy = nil, nil;
		for radius = 0, 4 do
			for y = math.max(0, ty - radius), math.min(h - 1, ty + radius) do
				for x = math.max(0, tx - radius), math.min(w - 1, tx + radius) do
					if sx == nil and Map.PlotDistance(x, y, tx, ty) == radius and not Map.GetPlot(x, y):IsWater() then
						sx, sy = x, y;
					end
				end
			end
			if sx ~= nil then break; end
		end

		-- Karadan genisleyen arama: denizin karsi kiyisina atlamaz
		if sx ~= nil then
			local dist = {};
			local queue = {{sx, sy}};
			dist[sy * w + sx] = 0;
			local head = 1;
			local bestDist = nil;
			while head <= #queue do
				local cx, cy = queue[head][1], queue[head][2];
				head = head + 1;
				local d = dist[cy * w + cx];
				if bestDist ~= nil and d > bestDist + 1 then break; end
				local plot = Map.GetPlot(cx, cy);
				if IsValidStart(plot) then
					local ok = true;
					for _, p in ipairs(taken) do
						if Map.PlotDistance(cx, cy, p[1], p[2]) < MIN_DISTANCE then ok = false; break; end
					end
					if ok then
						local sc = StartScore(plot, d);
						if sc > bestScore then
							bestPlot, bestScore = plot, sc;
							if bestDist == nil then bestDist = d; end
						end
					end
				end
				if d < MAX_RADIUS then
					for _, nb in ipairs(TL_Neighbors(cx, cy)) do
						local nx, ny = nb[1], nb[2];
						if nx >= 0 and nx < w and ny >= 0 and ny < h and dist[ny * w + nx] == nil then
							if not Map.GetPlot(nx, ny):IsWater() then
								dist[ny * w + nx] = d + 1;
								table.insert(queue, {nx, ny});
							end
						end
					end
				end
			end
		end
		if bestPlot ~= nil then
			Players[iPlayer]:SetStartingPlot(bestPlot);
			table.insert(taken, {bestPlot:GetX(), bestPlot:GetY()});
			-- Sehir devletleri ve kaynak dagitimi yeni noktayi hesaba katsin
			if start_plot_database ~= nil and start_plot_database.PlaceImpactAndRipples ~= nil then
				pcall(function() start_plot_database:PlaceImpactAndRipples(bestPlot:GetX(), bestPlot:GetY()); end);
			end
			print("Turk Liderleri haritasi: oyuncu " .. iPlayer .. " tarihi konuma yerlestirildi (" .. bestPlot:GetX() .. "," .. bestPlot:GetY() .. ")");
		else
			local plot = Players[iPlayer]:GetStartingPlot();
			if plot ~= nil then table.insert(taken, {plot:GetX(), plot:GetY()}); end
		end
	end
end
------------------------------------------------------------------------------
function StartPlotSystem()
	local startOption = Map.GetCustomOption(1);
	local res = Map.GetCustomOption(2);
	if res == 6 then
		res = 1 + Map.Rand(3, "Random Resources Option - Lua");
	end

	print("Turk Liderleri haritasi: baslangic noktalari belirleniyor...");
	local start_plot_database = AssignStartingPlots.Create();

	local args = {
		method = 2,
		resources = res,
	};
	start_plot_database:GenerateRegions(args);
	start_plot_database:ChooseLocations();
	start_plot_database:BalanceAndAssign();

	if startOption == 1 then
		ApplyHistoricStarts(start_plot_database);
	end

	start_plot_database:PlaceNaturalWonders();
	start_plot_database:PlaceResourcesAndCityStates();
end
------------------------------------------------------------------------------
