"""Puduu .pen generator v11 — Material-icon parity (same glyphs as Flutter app).
Kills ALL ledger DNA (paper/ember/Fraunces/Inter/ruled lines/numbered tabs).
New language: white cards r16, teal accent, dark ink, Outfit + Work Sans,
dark pill bottom nav with white active pill, dark hero cards, tinted icon
tiles, status chips. Source of truth: puduu-app/lib/main.dart + puduu_theme.dart (HP render).
Icons: assets/icons/m11-* rendered from the SAME MaterialIcons-Regular.otf
the Flutter app uses (codepoints verified in icons.dart). v10 Lucide set deleted.
Schema 2.19. validator errors=0, emoji=0, images all present.
Run: python3 gen_puduu_pen_v11.py -> puduu.pen
"""
import json, itertools, re

_uid = itertools.count(1)
_AL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def nid():
    n = next(_uid)
    s = ""
    while n > 0:
        n, r = divmod(n, 62)
        s = _AL[r] + s
    return s.rjust(5, "0")

C = {
    "bg": "#F2F5F4", "card": "#FFFFFF",
    "ink": "#0F1F1E", "soft": "#3E5452", "mute": "#7A8F8D",
    "line": "#E4EBEA",
    "teal": "#0E9384", "tealDeep": "#0B7468", "tealWash": "#DDF3F0",
    "amber": "#F59E0B", "amberWash": "#FEF3DF",
    "moss": "#4D7C0F", "mossWash": "#EFF6DF",
    "dark": "#101E1D", "danger": "#DC2626", "white": "#FFFFFF",
    "navDim": "#8FA3A1", "mint": "#7DD3C7", "pale": "#B9CDC9",
    "chipGray": "#E8F1F6",
}
DISP = "Outfit"
UI = "Work Sans"
A = "./assets/icons"

def T(content, size=14.0, color="soft", weight="400", align="left",
      width=None, family=UI, name="Txt"):
    n = {"id": nid(), "type": "text", "name": name, "x": 0, "y": 0,
         "content": content, "fill": C.get(color, color),
         "fontSize": size, "fontFamily": family,
         "fontWeight": weight, "textAlign": align}
    if width is not None:
        n["width"] = width
        n["textGrowth"] = "fixed-width"
    return n

def R(width=None, height=None, fill="card", radius=16, name="Box",
      layout=None, children=None, padding=None, gap=None,
      align=None, justify=None, stroke=None, sw=None):
    n = {"id": nid(), "type": "frame", "name": name, "x": 0, "y": 0}
    if width is not None:
        n["width"] = width
    if height is not None:
        n["height"] = height
    n["fill"] = C.get(fill, fill)
    n["cornerRadius"] = radius
    if layout:
        n["layout"] = layout
    if padding is not None:
        n["padding"] = padding
    if gap is not None:
        n["gap"] = gap
    if align:
        n["alignItems"] = align
    if justify:
        n["justifyContent"] = justify
    if stroke:
        n["stroke"] = C.get(stroke, stroke)
    if sw:
        n["strokeWidth"] = sw
    n["children"] = children or []
    return n

def IMG(url, w, h, radius=8, name="Img"):
    return {"id": nid(), "type": "rectangle", "name": name, "x": 0, "y": 0,
            "width": w, "height": h, "cornerRadius": radius,
            "fill": {"type": "image", "url": url, "mode": "fill"}}

def CT(content, size, color, weight, family, width, name):
    return T(content, size, color, weight, "center", width, family, name)

def IC(icon, tile, name):
    # tinted icon tile 36px like the app TaskCard
    return R(36, 36, tile, 12, f"{name}Tile", "vertical",
             [IMG(f"{A}/m11-{icon}.png", 19, 19, 5, f"{name}Ic")],
             align="center", justify="center")

# ---------- fresh primitives ----------

def HELLO(hello, sub, name, bell=False):
    av = R(38, 38, "teal", 19, f"{name}Av", "vertical",
           [T("A", 15, "white", "700", "center", 38, DISP,
              f"{name}AvT")],
           align="center", justify="center")
    kids = [R(220, None, "bg", 0, f"{name}Tx", "vertical",
              [T(hello, 23, "ink", "700", "left", 220, DISP,
                 f"{name}Ti"),
               T(sub, 12.5, "tealDeep", "600", "left", 220, UI,
                 f"{name}Sb")], gap=2),
            av]
    if bell:
        kids.insert(1, R(38, 38, "card", 19, f"{name}Bell",
                         "vertical",
                         [R(26, 26, "card", 13, f"{name}BellIn",
                            "horizontal",
                            [IMG(f"{A}/m11-bell-out-soft.png",
                                 19, 19, 5, f"{name}BellIc"),
                             R(8, 8, "danger", 4, f"{name}BellDot",
                               "none", [])],
                            gap=-6, align="center",
                            justify="center"),
                          T("", 1, "mute", "400", "left", 1, UI,
                            f"{name}BellPad")],
                         align="center", justify="center",
                         stroke="line", sw=1))
    return R(350, None, "bg", 0, name, "horizontal", kids,
             gap=8, align="center", justify="space_between")

def SEARCH(hint, name):
    return R(350, 48, "card", 16, name, "horizontal",
             [IMG(f"{A}/m11-search-mute.png", 18, 18, 4,
                  f"{name}Ic"),
              T(hint, 13.5, "mute", "400", "left", 290, UI,
                f"{name}Tx")],
             gap=10, align="center", padding=14,
             stroke="line", sw=1)

def SEC(label, action="", name="Sec"):
    kids = [T(label.upper(), 12.5, "soft", "700", "left", 190, DISP,
               f"{name}Lb")]
    if action:
        kids.append(T(action, 12, "tealDeep", "600", "right", 140, UI,
                      f"{name}Ac"))
    return R(350, 28, "bg", 0, name, "horizontal", kids,
             justify="space_between", align="center")

def HERO(tag, title, meta, pct, primary, secondary, name):
    return R(350, None, "dark", 20, name, "vertical",
             [T(tag, 10.5, "mint", "700", "left", 318, DISP,
                f"{name}Tag"),
              T(title, 19, "white", "700", "left", 318, DISP,
                f"{name}Ti"),
              T(meta, 12, "pale", "400", "left", 318, UI,
                f"{name}Mt"),
              R(318, 6, "dark", 3, f"{name}Tr", "horizontal",
                [R(pct, 6, "teal", 3, f"{name}Fl", "none", [])]),
              R(318, None, "dark", 0, f"{name}Btns", "horizontal",
                [R(152, 48, "teal", 14, f"{name}Go", "horizontal",
                   [IMG(f"{A}/m11-play-white.png", 17, 17, 4,
                        f"{name}GoIc"),
                    T(primary, 13.5, "white", "700", "left", 110,
                      DISP, f"{name}GoLb")],
                   gap=6, align="center", justify="center"),
                 R(152, 48, "dark", 14, f"{name}Sk", "horizontal",
                   [T(secondary, 13.5, "white", "700", "center",
                      140, DISP, f"{name}SkLb")],
                   align="center", justify="center",
                   stroke="pale", sw=1)],
                gap=8, align="center")],
             padding=16, gap=9)

def CARD(icon, tile, title, detail, side, side_done, name):
    tx = R(196, None, "card", 0, f"{name}Tx", "vertical",
           [T(title, 13.5, "ink", "600", "left", 196, UI,
              f"{name}Ti"),
            T(detail, 11.5, "mute", "400", "left", 196, UI,
              f"{name}Sb")], gap=2)
    return R(350, None, "card", 16, name, "horizontal",
             [IC(icon, tile, name), tx,
              T(side, 11.5, "moss" if side_done else "tealDeep",
                "700", "right", 64, UI, f"{name}Sd")],
             gap=12, align="center", padding=12,
             stroke="line", sw=1)

def DOT(dot, title, detail, side, side_done, name):
    # app TaskCard without icon: 10px status dot, no tile (main.dart 424-439)
    tx = R(196, None, "card", 0, f"{name}Tx", "vertical",
           [T(title, 13.5, "ink", "600", "left", 196, UI,
              f"{name}Ti"),
            T(detail, 11.5, "mute", "400", "left", 196, UI,
              f"{name}Sb")], gap=2)
    return R(350, None, "card", 16, name, "horizontal",
             [R(10, 10, dot, 5, f"{name}Dot", "none", []), tx,
              T(side, 11.5, "moss" if side_done else "tealDeep",
                "700", "right", 64, UI, f"{name}Sd")],
             gap=12, align="center", padding=12,
             stroke="line", sw=1)

def CHIP(big, small, name):
    return R(106, None, "card", 12, name, "vertical",
             [T(big, 16, "ink", "700", "center", 80, DISP,
                f"{name}B"),
              T(small, 10.5, "mute", "400", "center", 80, UI,
                f"{name}S")],
             gap=2, align="center", padding=10,
             stroke="line", sw=1)

def QUOTE(title, detail, dark, name):
    return R(350, None, "dark" if dark else "tealWash", 16, name,
             "vertical",
             [T(title, 13.5, "white" if dark else "ink", "600",
                "left", 318, UI, f"{name}Ti"),
              T(detail, 11.5, "pale" if dark else "mute", "400",
                "left", 318, UI, f"{name}Sb")],
             gap=2, padding=12,
             stroke=None if dark else "teal", sw=None)

def TABBAR(active):
    tabs = [("Today", "calendar"), ("Focus", "timer"),
            ("Reset", "bolt"), ("Progress", "barchart"),
            ("Yours", "settings")]
    kids = []
    for lb, ic in tabs:
        on = lb == active
        # active: white pill w/ dark icon; inactive: dim icon on dark
        iconrow = [IMG(f"{A}/m11-{ic}-{'fill-ink' if on else 'out-navdim'}.png",
                         22, 22, 5, f"Tb{lb}Ic")]
        if lb == "Today" and active == "Today":
            iconrow = [R(34, 24, "white" if on else "dark",
                         8, f"Tb{lb}IcW", "horizontal",
                         iconrow + [R(16, 16, "teal", 8,
                                       f"Tb{lb}Bg", "vertical",
                                       [T("3", 10, "white", "700",
                                          "center", 16, UI,
                                          f"Tb{lb}BgT")],
                                       align="center",
                                       justify="center")],
                         gap=-8, align="center",
                         justify="center")]
        cell = R(64, 52, "white" if on else "dark", 18, f"Tb{lb}",
                   "vertical",
                   iconrow + [
                    T(lb, 10, "dark" if on else "navDim",
                      "700" if on else "500", "center", 60, UI,
                      f"Tb{lb}Lb")],
                   gap=2, align="center", justify="center")
        kids.append(cell)
    return R(358, 68, "dark", 26, "TabBar", "horizontal", kids,
             gap=2, align="center", justify="center")

PHONE_W, PHONE_H = 390, 844

def SPACER(name, h):
    return R(358, max(0, int(h)), "bg", 0, name, "none", [])

def SCREEN(name, x, body, tab, spacer_h=0):
    col = [R(358, None, "bg", 0, f"{name}Bd", "vertical",
             body, gap=0, padding=[0, 4, 0, 4]),
           SPACER(f"{name}Fill", spacer_h),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x,
            "y": 0, "width": PHONE_W, "height": PHONE_H,
            "fill": C["bg"],
            "layout": "vertical", "alignItems": "center",
            "children": col}

def LABELS(screens):
    return [{"id": nid(), "type": "text", "name": s["name"],
             "x": s["x"], "y": -50, "content": s["name"],
             "fill": C["mute"], "fontSize": 14,
             "fontFamily": UI, "fontWeight": "700",
             "textAlign": "left"}
            for s in screens]

def main():
    s1 = SCREEN("01 Today", 0, [
        HELLO("Hello, Alex", "Morning plan", "H1", bell=True),
        SEARCH("Search a task or ritual", "Srch1"),
        HERO("NOW · 09:00 · 50 MIN", "Deep work: portfolio",
             "Step 2 of 4 · timer ready", 194,
             "Begin session", "Skip", "Hero1"),
        SEC("Categories", "See all ›", "S1"),
        R(350, None, "bg", 0, "CatGrid", "horizontal", [
            R(80, 76, "card", 14, "C1", "vertical",
              [R(34, 34, "tealWash", 12, "C1T", "vertical",
                 [IMG(f"{A}/m11-timer-out-soft.png", 18, 18, 5, "C1I")],
                 align="center", justify="center"),
               T("Focus", 10.5, "ink", "600", "center", 64, UI,
                 "C1L")], gap=6, align="center", padding=6,
              stroke="line", sw=1),
            R(80, 76, "card", 14, "C2", "vertical",
              [R(34, 34, "amberWash", 12, "C2T", "vertical",
                 [IMG(f"{A}/m11-bolt-out-soft.png", 18, 18, 5, "C2I")],
                 align="center", justify="center"),
               T("Reset", 10.5, "ink", "600", "center", 64, UI,
                 "C2L")], gap=6, align="center", padding=6,
              stroke="line", sw=1),
            R(80, 76, "card", 14, "C3", "vertical",
              [R(34, 34, "mossWash", 12, "C3T", "vertical",
                 [IMG(f"{A}/m11-check-soft.png", 18, 18, 5, "C3I")],
                 align="center", justify="center"),
               T("Habits", 10.5, "ink", "600", "center", 64, UI,
                 "C3L")], gap=6, align="center", padding=6,
              stroke="line", sw=1),
            R(80, 76, "card", 14, "C4", "vertical",
              [R(34, 34, "chipGray", 12, "C4T", "vertical",
                 [IMG(f"{A}/m11-sort-out-soft.png", 18, 18, 5,
                      "C4I")],
                 align="center", justify="center"),
               T("More", 10.5, "ink", "600", "center", 64, UI,
                 "C4L")], gap=6, align="center", padding=6,
              stroke="line", sw=1),
        ], gap=8, align="center"),
        SEC("Up next", "3 waiting", "S2"),
        DOT("teal", "Deep work: portfolio",
            "09:00 · Hero section, phone away", "Begin", False,
            "T1"),
        DOT("moss", "Walk outside",
            "11:00 · Fifteen minutes, no podcast", "Done", True,
            "T2"),
        SEC("Inbox", "", "S2b"),
        R(350, None, "card", 16, "InboxCard", "vertical", [
            R(326, None, "card", 0, "InboxRow", "horizontal", [
                T("Capture a task, idea, or reminder…", 13.5, "mute",
                  "400", "left", 196, UI, "InboxHint"),
                R(96, 44, "teal", 14, "AddBtn", "horizontal", [
                    IMG(f"{A}/m11-plus-white.png", 16, 16, 4,
                        "AddIc"),
                    T("Add", 13.5, "white", "700", "left", 44,
                      DISP, "AddLb")],
                  gap=4, align="center", justify="center"),
            ], gap=8, align="center"),
            R(326, 48, "card", 14, "SortBtn", "horizontal", [
                IMG(f"{A}/m11-sort-out-teal.png", 17, 17, 4,
                    "SortIc"),
                T("Sort into my day", 13.5, "tealDeep", "700",
                  "center", 220, DISP, "SortLb")],
              gap=6, align="center", justify="center",
              stroke="tealDeep", sw=1.2),
        ], gap=10, padding=12, stroke="line", sw=1),
    ], "Today", 6)

    s2 = SCREEN("02 Focus", 470, [
        HELLO("Stay with it", "Focus session · step 2 of 4",
              "H2"),
        R(350, None, "dark", 20, "TimerHero", "vertical", [
            CT("32:10", 58, "white", "700", DISP, 318,
               "DialTm"),
            CT("MINUTES LEFT · GENTLE CHIME AT END", 10.5,
               "mint", "700", UI, 318, "DialK"),
            R(318, 6, "dark", 3, "DialTr", "horizontal",
              [R(115, 6, "teal", 3, "DialFl", "none", [])]),
            CT("Sketch the hero section. Phone in another room.",
               12, "pale", "400", UI, 318, "DialSb"),
            R(318, None, "dark", 0, "FocusBtns", "horizontal", [
                R(152, 50, "teal", 14, "PauseBtn", "horizontal",
                  [IMG(f"{A}/m11-pause-white.png", 17, 17, 4,
                       "PauseIc"),
                   T("Pause", 13.5, "white", "700", "left",
                     90, DISP, "PauseLb")],
                  gap=6, align="center", justify="center"),
                R(152, 50, "dark", 14, "EndBtn", "horizontal",
                  [T("End early", 13.5, "white", "700",
                     "center", 140, DISP, "EndLb")],
                  align="center", justify="center",
                  stroke="pale", sw=1),
            ], gap=8, align="center"),
        ], padding=16, gap=10),
        SEC("Session steps", "", "S3"),
        DOT("moss", "Open the file",
            "Done · 2 min", "Done", True, "F1"),
        DOT("teal", "Sketch hero section",
            "Now · 25 min", "25 min", False, "F2"),
        DOT("line", "Review + save",
            "Next · 10 min", "10 min", False, "F3"),
    ], "Focus", 40)

    s3 = SCREEN("03 Reset", 940, [
        HELLO("Hit a wall?", "Two minutes counts", "H3"),
        SEARCH("Search a reset", "Srch3"),
        SEC("Pick the smallest one", "", "S4"),
        CARD("drop-out-soft", "tealWash",
             "Drink a glass of water",
             "Stand up, sip slowly, look far away.", "2 min",
             False, "R1"),
        CARD("bolt-out-soft", "amberWash", "Clear one surface",
             "Just the desk corner. Nothing more.", "2 min",
             False, "R2"),
        CARD("mail-out-soft", "mossWash",
             "Open the difficult email",
             "Read it only. Reply comes later.", "2 min",
             False, "R3"),
        CARD("sort-out-soft", "chipGray", "Sort the inbox",
             "Rule-based now, assisted later.", "3 min",
             False, "R4"),
        QUOTE("Slow is still moving.",
              "Skipping is allowed — Puduu waits.", False,
              "Q3"),
    ], "Reset", 30)

    s4 = SCREEN("04 Progress", 1410, [
        HELLO("Keep growing", "Good days: 5 of 7", "H4"),
        R(350, None, "bg", 0, "Chips", "horizontal", [
            CHIP("5/7", "good days", "CP1"),
            CHIP("+20%", "focus", "CP2"),
            CHIP("×5", "resets", "CP3"),
        ], gap=8, align="center"),
        SEC("This week", "See all ›", "S5"),
        CARD("barchart-out-soft", "tealWash", "Weekly shelf",
             "Early starter ×3 · Reset ×5 · Focus 25m ×8.",
             "W39", False, "G1"),
        CARD("timer-out-soft", "amberWash",
             "Focus trend",
             "Up 20% vs last week. Mornings win", "+20%",
             False, "G2"),
        CARD("bolt-out-soft", "mossWash", "Resets that worked",
             "Water first, then air. Evenings hard", "×5",
             False, "G3"),
        QUOTE("Done is a direction.",
              "Not a streak. Never resets to zero.", True,
              "Q4"),
    ], "Progress", 30)

    s5 = SCREEN("05 Yours", 1880, [
        HELLO("Make it yours", "Plan, sounds, reminders",
              "H5"),
        R(350, None, "teal", 20, "ProHero", "vertical", [
            T("PUDUU PRO · $6.99/MO", 10.5, "tealWash", "700",
              "left", 318, DISP, "ProTag"),
            T("Unlimited resets", 19, "white", "700", "left",
              318, DISP, "ProTi"),
            T("Yearly $49.99 · calm history · backup", 12,
              "tealWash", "400", "left", 318, UI, "ProMt"),
            R(318, 48, "white", 14, "ProBtn", "horizontal",
              [T("Upgrade", 14, "tealDeep", "700", "center",
                 290, DISP, "ProLb")],
              align="center", justify="center"),
        ], padding=16, gap=8),
        SEC("Settings", "", "S6"),
        CARD("bell-out-soft", "amberWash", "Gentle nudges",
             "Max 6 per day · quiet 22:00–07:00.", "On",
             False, "Y2"),
        CARD("sound-out-soft", "tealWash",
             "Sounds and haptics",
             "Calm chime · soft vibration.", "On", False,
             "Y3"),
        CARD("shield-out-soft", "chipGray",
             "Backup and export",
             "Weekly backup · CSV export.", ">", False,
             "Y4"),
    ], "Yours", 40)

    screens = [s1, s2, s3, s4, s5]
    doc = {"version": "2.19",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": screens + LABELS(screens)}
    with open("puduu.pen", "w") as f:
        json.dump(doc, f)
    blob = json.dumps(doc)
    print("wrote puduu.pen:",
          sum(1 for _ in blob.split('"id"')) - 1, "nodes")
    print("emoji hits:", len(re.findall(
        r'[\U0001F000-\U0001FAFF\u2600-\u27BF]', blob)))
    import pathlib
    urls = sorted(set(re.findall(r'"url": "([^"]+)"', blob)))
    miss = [u for u in urls if not pathlib.Path(u).exists()]
    print("images:", len(urls), "| MISSING:", miss if miss else "none")

if __name__ == "__main__":
    main()
