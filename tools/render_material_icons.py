"""Render Puduu v11 icons from the SAME MaterialIcons font the Flutter app uses.
Source: /opt/data/flutter-sdk/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf
Codepoints = exact values from flutter/packages/flutter/lib/src/material/icons.dart
Output: assets/icons/m11-<name>-<slot>.png (96px, exact slot color).
This kills the Lucide-vs-Material mismatch: same glyphs as the HP render, pixel-identical family."""
import pathlib
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

FONT = pathlib.Path("/opt/data/flutter-sdk/flutter/bin/cache/artifacts/material_fonts/MaterialIcons-Regular.otf")
OUT = pathlib.Path("/opt/data/puduu/puduu-design/assets/icons")
OUT.mkdir(parents=True, exist_ok=True)

# codepoints verified against icons.dart (see session)
GLYPHS = {
    "calendar-out": 0xEF11, "calendar-fill": 0xE122,
    "timer-out": 0xF44A, "timer-fill": 0xE662,
    "bolt-out": 0xEEDD, "bolt-fill": 0xE0EE,
    "barchart-out": 0xEEBC, "barchart-fill": 0xE0CC,
    "settings-out": 0xF36E, "settings-fill": 0xE57F,
    "search": 0xE567, "bell-out": 0xF237,
    "play": 0xE4CB, "pause": 0xE47C,
    "check": 0xE156, "plus": 0xE047,
    "chevron": 0xE15F, "drop-out": 0xF0695,
    "walk": 0xE1E1, "mail-out": 0xE3C4,
    "sort-out": 0xEEA9, "crown-out": 0xF06A1,
    "sound-out": 0xF4A8, "shield-out": 0xF379,
}
SLOTS = {
    "ink": "#0F1F1E", "soft": "#3E5452", "mute": "#7A8F8D",
    "white": "#FFFFFF", "teal": "#0B7468", "tealbright": "#0E9384",
    "amber": "#B45309", "moss": "#4D7C0F",
}
# which slots each glyph needs (mirrors v10 usage + nav ink+white pairs)
NEED = {
    "calendar-out": ["ink", "white"], "calendar-fill": ["ink"],
    "timer-out": ["ink", "white", "mute", "soft"], "timer-fill": ["ink"],
    "bolt-out": ["amber", "white", "mute"], "bolt-fill": ["ink"],
    "barchart-out": ["ink", "white", "mute"], "barchart-fill": ["ink"],
    "settings-out": ["ink", "white", "mute"], "settings-fill": ["ink"],
    "search": ["mute"], "bell-out": ["soft"],
    "play": ["white"], "pause": ["white"],
    "check": ["moss", "white"], "plus": ["white"],
    "chevron": ["mute"], "drop-out": ["tealbright", "soft"],
    "walk": ["amber", "soft"], "mail-out": ["soft"],
    "sort-out": ["soft"], "crown-out": ["white"],
    "sound-out": ["soft"], "shield-out": ["soft"],
}
SIZE = 96
PAD = 8
fnt = TTFont(str(FONT))
cmap = fnt.getBestCmap()
missing = [k for k, cp in GLYPHS.items() if cp not in cmap]
print("GLYPHS missing from font:", missing if missing else "none")

def render(cp, color, out):
    font = ImageFont.truetype(str(FONT), 76)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ch = chr(cp)
    bb = d.textbbox((0, 0), ch, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((SIZE - w) / 2 - bb[0], (SIZE - h) / 2 - bb[1]), ch, font=font, fill=color)
    img.save(out)

count = 0
for name, cpslots in NEED.items():
    for slot in cpslots:
        out = OUT / f"m11-{name}-{slot}.png"
        render(GLYPHS[name], SLOTS[slot], out)
        count += 1
print(f"rendered {count} icons -> {OUT}")
