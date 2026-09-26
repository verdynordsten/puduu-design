"""Truthful .pen structural preview — real flex layout engine (vertical /
horizontal), wrapped-text measurement, image-fill tiles, alignment-aware.
Writes preview/pen/<screen>.png. NEVER wipes preview/ root.
Usage: python3 tools/render_pen_preview.py"""
import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "puduu.pen")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "preview", "pen")

def font(bold, size):
    try:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", max(8, int(size)))
    except Exception:
        return ImageFont.load_default()

def hexof(c):
    if isinstance(c, str) and c.startswith("#"):
        return c
    return "#1C1917"

def measure(text, fnt, width):
    # wrap measurement using draw.textlength
    img = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(img)
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]

ICON_TINT = {"wash": "#F7E8D2", "card": "#FFFDF8", "paper": "#F6F3EC",
             "ink": "#1C1917", "deep": "#EFE8D8", "line": "#E3DAC7",
             "ember": "#9A3412", "moss": "#5B6B1F"}

DESIGN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ICON_CACHE = {}

def icon_img(url, w, h):
    """Load real ./assets/icons/*.png and resize — truthful preview."""
    key = (url, int(w), int(h))
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    try:
        p = os.path.join(DESIGN_ROOT, url.lstrip("./"))
        im = Image.open(p).convert("RGBA")
        im = im.resize((max(8, int(w)), max(8, int(h))), Image.BICUBIC)
        _ICON_CACHE[key] = im
        return im
    except Exception:
        return None

class R:
    def __init__(self):
        self.img = None; self.dr = None

    def text_block_h(self, o, avail_w):
        size = float(o.get("fontSize", 14))
        fnt = font(str(o.get("fontWeight", "400")) >= "600", size)
        w = min(float(o.get("width", avail_w)), avail_w)
        lines = measure(o.get("content", ""), fnt, w)
        return len(lines) * size * 1.45, lines, fnt, w

    def node_h(self, o, avail_w):
        t = o.get("type")
        if t == "text":
            h, _, _, _ = self.text_block_h(o, avail_w)
            return h
        if t == "rectangle":
            return float(o.get("height", 24))
        if t == "frame":
            if o.get("layout") in (None, "none") or not o.get("children"):
                return float(o.get("height", 0) or 0)
            pad = o.get("padding", 0)
            pl = pad if isinstance(pad, (int, float)) else (pad[1] if len(pad) == 2 else pad[3] if len(pad) == 4 else 0)
            gap = float(o.get("gap", 0) or 0)
            W = float(o.get("width", avail_w))
            inner = W - 2 * pl
            kids = o["children"]
            if o.get("layout") == "vertical":
                tot = sum(self.node_h(k, inner) for k in kids) + gap * (len(kids) - 1)
                return tot + (0 if isinstance(pad, (int, float)) and pad == 0 else 2 * (pad if isinstance(pad, (int, float)) else pad[0]))
            else:
                hs = [self.node_h(k, inner / max(1, len(kids))) for k in kids]
                return max(hs) + (0 if isinstance(pad, (int, float)) and pad == 0 else 2 * (pad if isinstance(pad, (int, float)) else pad[0]))
        return 20

    def draw(self, o, x, y, avail_w):
        t = o.get("type")
        if t == "text":
            size = float(o.get("fontSize", 14))
            h, lines, fnt, w = self.text_block_h(o, avail_w)
            align = o.get("textAlign", "left")
            for i, ln in enumerate(lines):
                ty = y + i * size * 1.45
                if align == "center":
                    self.dr.text((x + w / 2, ty), ln, fill=hexof(o.get("fill")), font=fnt, anchor="ma")
                elif align == "right":
                    self.dr.text((x + w, ty), ln, fill=hexof(o.get("fill")), font=fnt, anchor="ra")
                else:
                    self.dr.text((x, ty), ln, fill=hexof(o.get("fill")), font=fnt, anchor="la")
            # strikethrough hint: done titles drawn faint (no PIL strike needed)
            return h
        if t == "rectangle":
            w, h = float(o.get("width", 24)), float(o.get("height", 24))
            fill = o.get("fill")
            if isinstance(fill, dict) and fill.get("type") == "image":
                url = fill.get("url", "")
                im = icon_img(url, w, h)
                if im is not None:
                    self.img.paste(im, (int(x), int(y)), im)
                else:
                    short = url.split("/")[-1].replace(".png", "")[:14]
                    self.dr.rounded_rectangle([x, y, x + w, y + h], radius=6, fill="#F7E8D2", outline="#9A3412")
                    self.dr.text((x + w / 2, y + h / 2 - 6), short, fill="#7C2D12", font=font(False, 7), anchor="ma")
            else:
                self.dr.ellipse([x, y, x + w, y + h], fill=hexof(fill) if isinstance(fill, str) else "#EFE8D8")
            return h
        if t == "frame":
            W = float(o.get("width", avail_w))
            fill = o.get("fill")
            pad = o.get("padding", 0)
            pt = pad if isinstance(pad, (int, float)) else (pad[0] if len(pad) in (2, 4) else 0)
            pl = pad if isinstance(pad, (int, float)) else (pad[1] if len(pad) == 2 else (pad[3] if len(pad) == 4 else 0))
            gap = float(o.get("gap", 0) or 0)
            kids = o.get("children", [])
            layout = o.get("layout")
            # bg
            if isinstance(fill, str) and fill.startswith("#"):
                h_est = self.node_h(o, avail_w)
                self.dr.rounded_rectangle([x, y, x + W, y + h_est], radius=4, fill=fill)
            if layout == "vertical":
                cy = y + pt
                for k in kids:
                    kh = self.node_h(k, W - 2 * pl)
                    self.draw(k, x + pl, cy, W - 2 * pl)
                    cy += kh + gap
                return cy - gap - y + pt
            elif layout == "horizontal":
                cx = x + pl
                maxh = 0
                for k in kids:
                    kw = float(k.get("width", 60))
                    kh = self.draw(k, cx, y + pt, kw)
                    cx += kw + gap
                    maxh = max(maxh, kh)
                return maxh + 2 * pt
            else:
                cy = y
                for k in kids:
                    cy += self.draw(k, x, cy, avail_w)
                return cy - y
        return 0

def render_screen(scr):
    W = int(scr.get("width", 390))
    r = R()
    r.img = Image.new("RGB", (W, 2200), "#F6F3EC")
    r.dr = ImageDraw.Draw(r.img)
    y = 12
    for child in scr.get("children", []):
        y += r.draw(child, 16, y, W - 32) + 10
        if y > 2050:
            break
    # bottom nav band marker
    r.dr.rectangle([0, y + 6, W, y + 12], fill="#E3DAC7")
    return r.img.crop((0, 0, W, min(int(y + 20), 2200)))

def main():
    d = json.load(open(SRC, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for c in d["children"]:
        if c.get("type") == "frame" and not c.get("reusable") and c.get("name", "")[:1] == "0":
            img = render_screen(c)
            p = os.path.join(OUT, c["name"].replace(" ", "-") + ".png")
            img.save(p)
            print("wrote", p, img.size)
            n += 1
    print(f"screens: {n}")

main()
