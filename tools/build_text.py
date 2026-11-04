#!/usr/bin/env python3
"""tools/texts.py icindeki verilerden metin XML'i ve isim SQL'ini uretir."""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texts  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "Turkish Leaders")


def sql_str(s):
    return "'" + s.replace("'", "''") + "'"


def main():
    rows = dict(texts.TEXT)
    sql = ["-- Bu dosya tools/build_text.py ile otomatik uretilmistir. Elle duzenlemeyin.", ""]

    # sehir adlari: benzersizlik kontrolu
    seen = {}
    for civ in texts.CIVS:
        for name in texts.CITIES[civ]:
            if name in seen:
                raise SystemExit("Ayni sehir adi iki kez kullanilmis: %s (%s, %s)" % (name, seen[name], civ))
            seen[name] = civ

    sql.append("INSERT INTO Civilization_CityNames (CivilizationType, CityName) VALUES")
    vals = []
    for civ in texts.CIVS:
        for i, name in enumerate(texts.CITIES[civ]):
            tag = "TXT_KEY_TL_CITY_%s_%02d" % (civ, i + 1)
            rows[tag] = name
            vals.append("\t('CIVILIZATION_TL_%s', '%s')" % (civ, tag))
    sql.append(",\n".join(vals) + ";")
    sql.append("")

    sql.append("INSERT INTO Civilization_SpyNames (CivilizationType, SpyName) VALUES")
    vals = []
    for civ in texts.CIVS:
        for i, name in enumerate(texts.SPIES[civ]):
            tag = "TXT_KEY_TL_SPY_%s_%02d" % (civ, i + 1)
            rows[tag] = name
            vals.append("\t('CIVILIZATION_TL_%s', '%s')" % (civ, tag))
    sql.append(",\n".join(vals) + ";")
    sql.append("")

    sql.append("INSERT INTO Diplomacy_Responses (LeaderType, ResponseType, Response, Bias) VALUES")
    vals = []
    for civ, lines in texts.DIPLO.items():
        for key in lines:
            vals.append("\t('LEADER_TL_%s', '%s', 'TXT_KEY_LEADER_TL_%s_%s%%', 1)"
                        % (civ, texts.RESPONSE_TYPES[key], civ, key))
    sql.append(",\n".join(vals) + ";")
    sql.append("")

    with open(os.path.join(MOD, "Core", "TL_Names.sql"), "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(sql))

    out = ['<?xml version="1.0" encoding="utf-8"?>',
           "<!-- Bu dosya tools/build_text.py ile otomatik uretilmistir. Elle duzenlemeyin. -->",
           "<GameData>", "\t<Language_en_US>"]
    for tag in sorted(rows):
        out.append('\t\t<Row Tag="%s">\n\t\t\t<Text>%s</Text>\n\t\t</Row>' % (tag, escape(rows[tag])))
    out += ["\t</Language_en_US>", "</GameData>", ""]
    with open(os.path.join(MOD, "Text", "TL_Text.xml"), "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write("\n".join(out))
    print("metin satiri:", len(rows))


if __name__ == "__main__":
    main()
