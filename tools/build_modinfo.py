#!/usr/bin/env python3
"""Mod klasorundeki dosyalari tarar, MD5 degerlerini hesaplar ve TurkishLeaders.modinfo dosyasini yazar."""
import hashlib
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "Turkish Leaders")
MOD_ID = "8b1f7c52-4e0a-4d6e-9a1b-5c2f3e7d9a10"
VERSION = 1

DB_ORDER = [
    "Core/TL_Colors.sql",
    "Core/TL_Art.sql",
    "Core/TL_Units.sql",
    "Core/TL_Buildings.sql",
    "Core/TL_Civilizations.sql",
    "Core/TL_Names.sql",
    "Text/TL_Text.xml",
]
NO_IMPORT = set(DB_ORDER) | {"Lua/TL_Traits.lua", "Maps/TL_EMEA.lua"}

NAME = "Türk Liderleri (Turkish Leaders)"
TEASER = "Osman Bey, Orhan Gazi, Fatih, Yavuz, Battal Gazi ve Atatürk ile altı yeni Türk medeniyeti ve Avrupa-Orta Doğu-Afrika haritası."
DESCRIPTION = (
    "Altı yeni medeniyet ekler: Kayı Beyliği (Osman Bey), Osmanlı Beyliği (Orhan Gazi), Osmanlı Devleti "
    "(Fatih Sultan Mehmet), Osmanlı Hilafeti (Yavuz Sultan Selim), Uç Gazileri (Seyyid Battal Gazi) ve "
    "Türkiye Cumhuriyeti (Mustafa Kemal Atatürk). Her medeniyetin kendine özgü yeteneği, birimi ve binası "
    "vardır. Ayrıca gerçek coğrafyaya dayanan, tarihî başlangıç noktalı bir Avrupa, Orta Doğu ve Afrika "
    "haritası içerir. Brave New World gerektirir."
)


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main():
    files = []
    for dirpath, _, names in os.walk(MOD):
        for n in names:
            if n.endswith(".modinfo"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, n), MOD).replace(os.sep, "/")
            files.append(rel)
    files.sort()
    for f in DB_ORDER:
        assert f in files, "eksik dosya: " + f

    out = ['<?xml version="1.0" encoding="utf-8"?>',
           '<Mod id="%s" version="%d">' % (MOD_ID, VERSION),
           "  <Properties>",
           "    <Name>%s</Name>" % escape(NAME),
           "    <Stability>Beta</Stability>",
           "    <Teaser>%s</Teaser>" % escape(TEASER),
           "    <Description>%s</Description>" % escape(DESCRIPTION),
           "    <Authors>Bora Şavkar</Authors>",
           "    <HideSetupGame>0</HideSetupGame>",
           "    <AffectsSavedGames>1</AffectsSavedGames>",
           "    <MinCompatibleSaveVersion>0</MinCompatibleSaveVersion>",
           "    <SupportsSinglePlayer>1</SupportsSinglePlayer>",
           "    <SupportsMultiplayer>1</SupportsMultiplayer>",
           "    <SupportsHotSeat>1</SupportsHotSeat>",
           "    <SupportsMac>1</SupportsMac>",
           "    <ReloadAudioSystem>0</ReloadAudioSystem>",
           "    <ReloadLandmarkSystem>0</ReloadLandmarkSystem>",
           "    <ReloadStrategicViewSystem>0</ReloadStrategicViewSystem>",
           "    <ReloadUnitSystem>0</ReloadUnitSystem>",
           "  </Properties>",
           "  <Dependencies />",
           "  <References />",
           "  <Blocks />",
           "  <Files>"]
    for f in files:
        imp = "0" if f in NO_IMPORT else "1"
        out.append('    <File md5="%s" import="%s">%s</File>' % (md5(os.path.join(MOD, f)), imp, escape(f)))
    out += ["  </Files>",
            "  <Actions>",
            "    <OnModActivated>"]
    for f in DB_ORDER:
        out.append("      <UpdateDatabase>%s</UpdateDatabase>" % f)
    out += ["    </OnModActivated>",
            "  </Actions>",
            "  <EntryPoints>",
            '    <EntryPoint type="InGameUIAddin" file="Lua/TL_Traits.lua">',
            "      <Name>TL_Traits</Name>",
            "      <Description>Türk liderlerinin Lua ile çalışan yetenekleri</Description>",
            "    </EntryPoint>",
            '    <EntryPoint type="MapScript" file="Maps/TL_EMEA.lua">',
            "      <Name>TXT_KEY_TL_MAP_EMEA</Name>",
            "      <Description>TXT_KEY_TL_MAP_EMEA_HELP</Description>",
            "    </EntryPoint>",
            "  </EntryPoints>",
            "</Mod>", ""]
    with open(os.path.join(MOD, "TurkishLeaders.modinfo"), "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(out))
    print("modinfo yazildi: %d dosya" % len(files))


if __name__ == "__main__":
    main()
