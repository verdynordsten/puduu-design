"""Truthful .pen preview renderer — respects textAlign (left/center/right)
and draws image-fill boxes as tinted tiles. PIL is only a structural
preview; the browser mockup remains the visual truth.
Usage: python3 tools/render_preview.py  (reads puduu.pen, writes preview/)
"""
import json
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

SRC = "puduu.pen"
OUT = "preview"


def font(bold, size):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)
    except Exception:
        return ImageFont.load_default()


def hexof(c):
    return c if isinstance(c, str) and c.startswith("#") else "#111827"


def draw_node(dr, o, x, y, max_w=358):
    """Draw text/image nodes honoring alignment. Returns height used."""
    used = 0
    if o.get("type") == "text":
        content = o.get("content", "")[:52]
        size = int(o.get("fontSize", 14))
        bold = str(o.get("fontWeight", "400")) >= "600"
        align = o.get("textAlign", "left")
        w = int(o.get("width", max_w))
        f = font(bold, min(size, 22))
        tx = x
        anchor = "la"
        if align == "center":
            tx = x + w // 2
            anchor = "ma"
        elif align == "right":
            tx = x + w
            anchor = "ra"
        dr.text((tx, y), content, fill=hexof(o.get("fill")), font=f, anchor=anchor)
        used = int(size * 1.6)
    elif o.get("type") == "rectangle" and isinstance(o.get("fill"), dict):
        if o["fill"].get("type") == "image":
            dr.rounded_rectangle([x, y + 4, x + 44, y + 48], radius=12, fill="#EDF2FF")
            dr.text((x + 16, y + 14), "i", fill="#2563EB", font=font(False, 14))
            used = 56
    return used


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for c in d["children"]:
        nm = c.get("name", "")
        if not (c.get("type") == "frame" and nm[:1] == "0"):
            continue
        n += 1
        img = Image.new("RGB", (390, 844), "#FAFAF8")
        dr = ImageDraw.Draw(img)
        dr.rectangle([0, 0, 390, 64], fill="white")
        dr.text((64, 22), nm, fill="#111827", font=font(True, 16))
        dr.rounded_rectangle([12, 14, 52, 54], radius=13, fill="#2563EB")
        dr.text((24, 22), "P", fill="white", font=font(True, 16))
        pos = [80]

        def walk(o):
            if o.get("type") == "text" and not o.get("name", "").startswith(("Tb", "H")) and o.get("name") != nm:
                pos[0] += draw_node(dr, o, 16, pos[0])
            elif o.get("type") == "rectangle" and isinstance(o.get("fill"), dict):
                pos[0] += draw_node(dr, o, 16, pos[0])
            for k in o.get("children", []):
                walk(k)

        for k in c.get("children", []):
            if k.get("name", "").endswith("Bd"):
                walk(k)
        dr.rectangle([0, 758, 390, 844], fill="white", outline="#E6E4DE")
        dr.text((195, 790), "Today   Focus   Reset   Progress   Yours",
                fill="#4B5563", font=font(False, 10), anchor="ma")
        img.save(f"{OUT}/" + nm.replace(" ", "-") + ".png")
    print(f"previews: {n}")


main()
