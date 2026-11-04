#!/usr/bin/env python3
"""tools/texts.py icindeki verilerden metin XML'ini uretir."""
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import texts  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "Turkish Leaders")


TR_MAP = str.maketrans({"\u015f": "s", "\u015e": "S", "\u011f": "g", "\u011e": "G", "\u0131": "i", "\u0130": "I"})


def tr_safe(s):
    """Oyunun yazi tipinde olmayan Turkce harfleri cevirir (c, o, u ve sapkali harfler kalir)."""
    return s.translate(TR_MAP)


def main():
    rows = dict(texts.TEXT)

    # sehir adlari: benzersizlik kontrolu
    seen = {}
    for civ in texts.CIVS:
        for name in texts.CITIES[civ]:
            if name in seen:
                raise SystemExit("Ayni sehir adi iki kez kullanilmis: %s (%s, %s)" % (name, seen[name], civ))
            seen[name] = civ

    for civ in texts.CIVS:
        for i, name in enumerate(texts.CITIES[civ]):
            rows["TXT_KEY_TL_CITY_%s_%02d" % (civ, i + 1)] = name
        for i, name in enumerate(texts.SPIES[civ]):
            rows["TXT_KEY_TL_SPY_%s_%02d" % (civ, i + 1)] = name

    # Civ V yazi tipinde s-cedilla, yumusak g ve noktasiz i yok; gosterilebilen karsiliklarina cevir.
    rows = {k: tr_safe(v) for k, v in rows.items()}

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
