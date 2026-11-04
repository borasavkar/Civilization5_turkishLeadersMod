#!/usr/bin/env python3
"""
Lua betiklerini oyun disinda, Civ5 API'sinin basit bir taklidiyle (Lua 5.1) test eder.
  - TL_EMEA.lua: arazi/zemin uretimi ve tarihi baslangic noktalari
  - TL_Traits.lua: olay kayitlari, gorunmez binalar, fetih bonuslari
Kullanim: pip install lupa && python3 tools/test_lua.py
"""
import os
import sys

from lupa import lua51

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "Turkish Leaders")

MOCK_COMMON = r"""
print = function(...) end
GameDefines = { MAX_MAJOR_CIVS = 22 }
local nextId = 0
local function enum(names)
  local t = {}
  for i, n in ipairs(names) do t[n] = i - 1 end
  return t
end
GameInfoTypes = enum({
  "TERRAIN_GRASS","TERRAIN_PLAINS","TERRAIN_DESERT","TERRAIN_TUNDRA","TERRAIN_SNOW","TERRAIN_COAST","TERRAIN_OCEAN",
})
GameInfoTypes.FEATURE_ICE = 0
GameInfoTypes.CIVILIZATION_TL_FATIH = 100
GameInfoTypes.CIVILIZATION_TL_YAVUZ = 101
GameInfoTypes.CIVILIZATION_TL_OSMAN = 102
GameInfoTypes.CIVILIZATION_TL_ATATURK = 103
GameInfoTypes.CIVILIZATION_TL_ORHAN = 104
GameInfoTypes.CIVILIZATION_TL_BATTAL = 105
GameInfoTypes.CIVILIZATION_OTTOMAN = 106
GameInfoTypes.CIVILIZATION_ENGLAND = 107
GameInfoTypes.CIVILIZATION_CHINA = 108
GameInfoTypes.BUILDING_TL_DUMMY_OSMAN = 500
GameInfoTypes.BUILDING_TL_DUMMY_ORHAN = 501
GameInfoTypes.BUILDING_TL_DUMMY_ATATURK = 502
civNames = {}
for k, v in pairs(GameInfoTypes) do if string.sub(k,1,13) == "CIVILIZATION_" then civNames[v] = k end end
GameInfo = { Civilizations = setmetatable({}, {__index = function(_, id) if civNames[id] then return {Type = civNames[id]} end end}) }
PlotTypes = { PLOT_OCEAN = 0, PLOT_LAND = 1, PLOT_HILLS = 2, PLOT_MOUNTAIN = 3 }
"""

MOCK_MAP = r"""
W, H = 100, 90
local plots = {}
local Plot = {}
Plot.__index = Plot
function Plot:SetPlotType(t) self.ptype = t end
function Plot:SetTerrainType(t) self.terrain = t end
function Plot:GetTerrainType() return self.terrain end
function Plot:IsWater() return self.ptype == PlotTypes.PLOT_OCEAN end
function Plot:IsMountain() return self.ptype == PlotTypes.PLOT_MOUNTAIN end
function Plot:IsHills() return self.ptype == PlotTypes.PLOT_HILLS end
function Plot:IsImpassable() return false end
function Plot:GetFeatureType() return -1 end
function Plot:IsRiver() return false end
function Plot:IsCoastalLand() return false end
function Plot:GetX() return self.x end
function Plot:GetY() return self.y end
for y = 0, H-1 do for x = 0, W-1 do
  plots[y*W+x] = setmetatable({x=x, y=y, ptype=0, terrain=GameInfoTypes.TERRAIN_OCEAN}, Plot)
end end
Map = {}
function Map.GetPlot(x, y) if x < 0 or y < 0 or x >= W or y >= H then return nil end return plots[y*W+x] end
local function toCube(x, y) local q = x - (y - (y % 2)) / 2; return q, y, -q - y end
function Map.PlotDistance(x1, y1, x2, y2)
  local a1,b1,c1 = toCube(x1,y1); local a2,b2,c2 = toCube(x2,y2)
  return math.max(math.abs(a1-a2), math.abs(b1-b2), math.abs(c1-c2))
end
local customOpts = {1, 2}
function Map.GetCustomOption(i) return customOpts[i] end
function Map.Rand(n) return 0 end
function SetPlotTypes(t) for i = 0, W*H-1 do plots[i]:SetPlotType(t[i]) end end
function SetTerrainTypes(t) for i = 0, W*H-1 do assert(t[i] ~= nil, "terrain nil at "..i); plots[i]:SetTerrainType(t[i]) end end
function GenerateCoasts() end
function GetCoreMapOptions() return {}, {}, {}, {}, {Name = "res"} end
FeatureGenerator = { Create = function() return { AddFeatures = function(self)
  assert(math.abs(self:GetLatitudeAtPlot(0, 0) - 35.4/90) < 0.02, "enlem hesabi hatali")
end } end }
-- Oyuncular
local Player = {}; Player.__index = Player
function Player:IsEverAlive() return true end
function Player:GetCivilizationType() return self.civ end
function Player:GetStartingPlot() return self.start end
function Player:SetStartingPlot(p) self.start = p end
Players = {}
local civs = {"CIVILIZATION_TL_OSMAN","CIVILIZATION_TL_ORHAN","CIVILIZATION_TL_FATIH","CIVILIZATION_TL_YAVUZ",
  "CIVILIZATION_TL_BATTAL","CIVILIZATION_TL_ATATURK","CIVILIZATION_OTTOMAN","CIVILIZATION_ENGLAND","CIVILIZATION_CHINA"}
AssignStartingPlots = { Create = function() return {
  GenerateRegions = function() end, ChooseLocations = function() end,
  BalanceAndAssign = function()
    -- hepsini Afrika'nin ortasina koy (tarihi konum testi icin)
    for i, c in ipairs(civs) do
      Players[i-1] = setmetatable({civ = GameInfoTypes[c], start = Map.GetPlot(40 + i*3, 40)}, Player)
    end
  end,
  PlaceImpactAndRipples = function() end,
  PlaceNaturalWonders = function() end, PlaceResourcesAndCityStates = function() end,
} end }
function include() end
"""

CHECK_MAP = r"""
GeneratePlotTypes()
GenerateTerrain()
AddFeatures()
StartPlotSystem()
local info = GetMapScriptInfo()
assert(info.CustomOptions[1].DefaultValue == 1)
local init = GetMapInitData(0)
assert(init.Width == 100 and init.Height == 90)
local out = {}
for i = 0, 8 do
  local p = Players[i]:GetStartingPlot()
  assert(not p:IsWater(), "baslangic suda")
  assert(not p:IsMountain(), "baslangic dagda")
  out[#out+1] = civNames[Players[i].civ] .. "=" .. p:GetX() .. "," .. p:GetY()
end
for i = 0, 8 do for j = i+1, 8 do
  local a, b = Players[i]:GetStartingPlot(), Players[j]:GetStartingPlot()
  assert(Map.PlotDistance(a:GetX(), a:GetY(), b:GetX(), b:GetY()) >= 6, "baslangiclar cok yakin: "..i.." "..j)
end end
return table.concat(out, "\n")
"""

MOCK_TRAITS = r"""
local notifications = 0
NotificationTypes = { NOTIFICATION_GENERIC = 1 }
Locale = { ConvertTextKey = function(k, ...) return k end }
Game = { GetActivePlayer = function() return 0 end }
local function makeEvent() local e = {handlers = {}}; function e.Add(f) table.insert(e.handlers, f) end
  function e.Fire(...) for _, f in ipairs(e.handlers) do f(...) end end; return e end
GameEvents = { PlayerDoTurn = makeEvent(), PlayerCityFounded = makeEvent(), CityCaptureComplete = makeEvent() }
local City = {}; City.__index = City
function City:GetNumRealBuilding(b) return self.b[b] or 0 end
function City:SetNumRealBuilding(b, n) self.b[b] = n end
function City:GetPopulation() return self.pop end
function City:GetResistanceTurns() return self.res end
function City:ChangeResistanceTurns(n) self.res = self.res + n end
function City:GetName() return "Test" end
function City:GetX() return 1 end
function City:GetY() return 1 end
local Player = {}; Player.__index = Player
function Player:IsEverAlive() return true end
function Player:IsAlive() return true end
function Player:IsHuman() return self.id == 0 end
function Player:GetID() return self.id end
function Player:GetCivilizationType() return self.civ end
function Player:Cities() local i = 0; return function() i = i + 1; return self.cities[i] end end
function Player:ChangeGold(n) self.gold = self.gold + n end
function Player:ChangeFaith(n) self.faith = self.faith + n end
function Player:AddNotification() notifications = notifications + 1 end
local captured = setmetatable({b = {}, pop = 6, res = 6}, City)
Map = { GetPlot = function() return { GetPlotCity = function() return captured end } end }
Players = {}
local civs = {"CIVILIZATION_TL_OSMAN","CIVILIZATION_TL_FATIH","CIVILIZATION_TL_YAVUZ","CIVILIZATION_TL_ATATURK","CIVILIZATION_ENGLAND"}
for i, c in ipairs(civs) do
  Players[i-1] = setmetatable({id = i-1, civ = GameInfoTypes[c], gold = 0, faith = 0,
    cities = { setmetatable({b = {}, pop = 3, res = 0}, City) }}, Player)
end
function check()
  -- yukleme sirasinda Osman'in sehrine bina konmus olmali
  assert(Players[0].cities[1]:GetNumRealBuilding(GameInfoTypes.BUILDING_TL_DUMMY_OSMAN) == 1, "Osman binasi yok")
  assert(Players[3].cities[1]:GetNumRealBuilding(GameInfoTypes.BUILDING_TL_DUMMY_ATATURK) == 1, "Ataturk binasi yok")
  assert(Players[4].cities[1]:GetNumRealBuilding(GameInfoTypes.BUILDING_TL_DUMMY_OSMAN) == 0, "Ingiltere'ye bina verilmis")
  -- yeni sehir
  table.insert(Players[0].cities, setmetatable({b = {}, pop = 1, res = 0}, City))
  GameEvents.PlayerCityFounded.Fire(0, 1, 1)
  assert(Players[0].cities[2]:GetNumRealBuilding(GameInfoTypes.BUILDING_TL_DUMMY_OSMAN) == 1, "yeni sehre bina konmadi")
  -- Fatih fethi
  GameEvents.CityCaptureComplete.Fire(4, false, 1, 1, 1, 6, true)
  assert(captured.res == 3, "direnis yarilanmadi: " .. captured.res)
  assert(Players[1].gold == 60, "Fatih altini hatali")
  -- Yavuz fethi
  GameEvents.CityCaptureComplete.Fire(4, false, 1, 1, 2, 6, true)
  assert(Players[2].faith == 90, "Yavuz inanci hatali")
  GameEvents.PlayerDoTurn.Fire(3)
  return "ok"
end
"""


def run_map():
    lua = lua51.LuaRuntime(unpack_returned_tuples=True)
    lua.execute(MOCK_COMMON)
    lua.execute(MOCK_MAP)
    with open(os.path.join(MOD, "Maps", "TL_EMEA.lua"), encoding="utf-8") as fh:
        lua.execute(fh.read())
    print(lua.execute(CHECK_MAP))
    print("TL_EMEA.lua: TAMAM")


def run_traits():
    lua = lua51.LuaRuntime(unpack_returned_tuples=True)
    lua.execute(MOCK_COMMON)
    lua.execute(MOCK_TRAITS)
    with open(os.path.join(MOD, "Lua", "TL_Traits.lua"), encoding="utf-8") as fh:
        lua.execute(fh.read())
    assert lua.eval("check()") == "ok"
    print("TL_Traits.lua: TAMAM")


if __name__ == "__main__":
    run_map()
    run_traits()
