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


def TLROW(time, title, pct, color, done, name):
    bw = 196
    bar = R(bw, 7, "bg", 4, f"{name}Tr", "horizontal",
            [R(max(9, int(bw * pct)), 7, color, 4,
               f"{name}Fl", "none", [])])
    side = T("Done", 11, "moss", "700", "right", 52, UI,
             f"{name}Sd") if done else T("", 1, "mute", "400",
             "right", 52, UI, f"{name}Sd")
    return R(326, None, "card", 0, name, "horizontal",
             [T(time, 11, "mute", "400", "left", 36, UI,
                f"{name}Tm"), bar, side],
             gap=6, align="center")

def NAVROW(icon, tile, title, detail, name):
    tx = R(196, None, "card", 0, f"{name}Tx", "vertical",
           [T(title, 13.5, "ink", "600", "left", 196, UI,
              f"{name}Ti"),
            T(detail, 11.5, "mute", "400", "left", 196, UI,
              f"{name}Sb")], gap=2)
    return R(350, None, "card", 16, name, "horizontal",
             [IC(icon, tile, name), tx,
              IMG(f"{A}/m11-chevron-mute.png", 16, 16, 4,
                  f"{name}Ch")],
             gap=12, align="center", padding=12,
             stroke="line", sw=1)

def PLANROW(tag, title, detail, picked, name):
    return R(350, None, "card", 16, name, "horizontal",
             [IMG(f"{A}/m11-{'radio-on' if picked else 'radio-off'}-x.png",
                  20, 20, 5, f"{name}R"),
              R(240, None, "card", 0, f"{name}Tx", "vertical",
                [T(tag, 10, "tealDeep", "700", "left", 240,
                   DISP, f"{name}Tg"),
                 T(title, 13.5, "ink", "600", "left", 240, UI,
                   f"{name}Ti"),
                 T(detail, 11.5, "mute", "400", "left", 240,
                   UI, f"{name}Sb")], gap=2)],
             gap=10, align="center", padding=12,
             stroke="teal" if picked else "line",
             sw=1.6 if picked else 1)

def DOTDEF_PLACEHOLDER():
    return None

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
        SEC("Timeline", "", "S1t"),
        R(350, None, "card", 16, "TlCard", "vertical", [
            TLROW("09:00", "Deep work", 0.61, "teal", False,
                  "TL1"),
            TLROW("11:00", "Walk", 1.0, "moss", True, "TL2"),
            TLROW("13:00", "Admin", 0.04, "amber", False,
                  "TL3"),
            TLROW("15:00", "Call", 0.04, "tealDeep", False,
                  "TL4"),
            T("Open full calendar ›", 12, "tealDeep", "600",
              "center", 318, UI, "TlMore"),
        ], gap=8, padding=12, stroke="line", sw=1),
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
        SEC("Trophies", "", "S5t"),
        R(350, None, "bg", 0, "Troph", "horizontal", [
            R(106, None, "card", 12, "TR1", "vertical",
              [R(36, 36, "amberWash", 18, "TR1T", "vertical",
                 [IMG(f"{A}/m11-sun-out-x.png", 19, 19, 5,
                      "TR1I")],
                 align="center", justify="center"),
               T("x3", 14, "ink", "700", "center", 80, DISP,
                 "TR1B"),
               T("Early bird", 10.5, "mute", "400", "center",
                 80, UI, "TR1S")],
              gap=2, align="center", padding=10,
              stroke="line", sw=1),
            R(106, None, "card", 12, "TR2", "vertical",
              [R(36, 36, "tealWash", 18, "TR2T", "vertical",
                 [IMG(f"{A}/m11-bolt-out-soft.png", 19, 19, 5,
                      "TR2I")],
                 align="center", justify="center"),
               T("x5", 14, "ink", "700", "center", 80, DISP,
                 "TR2B"),
               T("Resetter", 10.5, "mute", "400", "center",
                 80, UI, "TR2S")],
              gap=2, align="center", padding=10,
              stroke="line", sw=1),
            R(106, None, "card", 12, "TR3", "vertical",
              [R(36, 36, "mossWash", 18, "TR3T", "vertical",
                 [IMG(f"{A}/m11-timer-out-soft.png", 19, 19, 5,
                      "TR3I")],
                 align="center", justify="center"),
               T("x8", 14, "ink", "700", "center", 80, DISP,
                 "TR3B"),
               T("Focused", 10.5, "mute", "400", "center",
                 80, UI, "TR3S")],
              gap=2, align="center", padding=10,
              stroke="line", sw=1),
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
        SEC("More", "", "S6m"),
        NAVROW("refresh-out-x", "tealWash", "Routines",
               "Repeatable calm", "NV1"),
        NAVROW("calendar-month-x", "amberWash", "Calendar",
               "Week view - sync", "NV2"),
        NAVROW("sort-out-soft", "chipGray", "Library",
               "Ready-made activities", "NV3"),
        NAVROW("face-sat-x", "mossWash", "Mood",
               "Check-ins + patterns", "NV4"),
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

    s6 = SCREEN("06 Routines", 2350, [
        HELLO("Routines", "Repeatable calm", "H6"),
        SEARCH("Search a routine", "Srch6"),
        SEC("Your routines", "+ New", "S7"),
        R(350, None, "card", 16, "Rt1", "vertical", [
            R(326, None, "card", 0, "Rt1H", "horizontal", [
                IC("refresh-out-x", "tealWash", "Rt1"),
                R(196, None, "card", 0, "Rt1Tx", "vertical",
                  [T("Morning reset", 13.5, "ink", "600",
                     "left", 196, UI, "Rt1Ti"),
                   T("3 steps - daily - 08:00", 11.5, "mute",
                     "400", "left", 196, UI, "Rt1Sb")],
                  gap=2),
                IMG(f"{A}/m11-chevron-mute.png", 16, 16, 4,
                    "Rt1Ch")],
              gap=12, align="center"),
            T("Meds - Water - Tidy 5 min", 12, "soft", "400",
              "left", 318, UI, "Rt1St"),
            R(318, 48, "teal", 14, "Rt1Go", "horizontal",
              [IMG(f"{A}/m11-play-white.png", 16, 16, 4,
                   "Rt1GoIc"),
               T("Start routine", 13.5, "white", "700",
                 "left", 200, DISP, "Rt1GoLb")],
              gap=6, align="center", justify="center"),
        ], gap=10, padding=12, stroke="line", sw=1),
        R(350, None, "card", 16, "Rt2", "vertical", [
            R(326, None, "card", 0, "Rt2H", "horizontal", [
                IC("nightlight-out-x", "mossWash", "Rt2"),
                R(196, None, "card", 0, "Rt2Tx", "vertical",
                  [T("Wind down", 13.5, "ink", "600", "left",
                     196, UI, "Rt2Ti"),
                   T("3 steps - daily - 22:00", 11.5, "mute",
                     "400", "left", 196, UI, "Rt2Sb")],
                  gap=2),
                IMG(f"{A}/m11-chevron-mute.png", 16, 16, 4,
                    "Rt2Ch")],
              gap=12, align="center"),
            T("Dim lights - No screens - Read", 12, "soft",
              "400", "left", 318, UI, "Rt2St"),
        ], gap=10, padding=12, stroke="line", sw=1),
        SEC("Suggested", "", "S8"),
        CARD("timer-out-soft", "tealWash", "Study sprint",
             "25 min focus - 5 min break x4", "+ Add",
             False, "Rt3"),
    ], "Yours", 30)

    s7 = SCREEN("07 Calendar", 2820, [
        HELLO("Calendar", "Week 39 - synced", "H7"),
        R(350, None, "card", 16, "WkCard", "horizontal", [
            R(44, 62, "card", 12, "Wk1", "vertical",
              [T("M", 10, "mute", "700", "center", 40, UI,
                 "Wk1D"),
               T("21", 14, "ink", "700", "center", 40, DISP,
                 "Wk1N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "card", 12, "Wk2", "vertical",
              [T("T", 10, "mute", "700", "center", 40, UI,
                 "Wk2D"),
               T("22", 14, "ink", "700", "center", 40, DISP,
                 "Wk2N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "dark", 12, "Wk3", "vertical",
              [T("W", 10, "white", "700", "center", 40, UI,
                 "Wk3D"),
               T("23", 14, "white", "700", "center", 40,
                 DISP, "Wk3N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "card", 12, "Wk4", "vertical",
              [T("T", 10, "mute", "700", "center", 40, UI,
                 "Wk4D"),
               T("24", 14, "ink", "700", "center", 40, DISP,
                 "Wk4N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "card", 12, "Wk5", "vertical",
              [T("F", 10, "mute", "700", "center", 40, UI,
                 "Wk5D"),
               T("25", 14, "ink", "700", "center", 40, DISP,
                 "Wk5N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "card", 12, "Wk6", "vertical",
              [T("S", 10, "mute", "700", "center", 40, UI,
                 "Wk6D"),
               T("26", 14, "ink", "700", "center", 40, DISP,
                 "Wk6N")],
              gap=2, align="center", justify="center"),
            R(44, 62, "card", 12, "Wk7", "vertical",
              [T("S", 10, "mute", "700", "center", 40, UI,
                 "Wk7D"),
               T("27", 14, "ink", "700", "center", 40, DISP,
                 "Wk7N")],
              gap=2, align="center", justify="center"),
        ], gap=4, align="center", padding=8, stroke="line",
          sw=1),
        SEC("Wednesday", "Sync calendars", "S9"),
        CARD("timer-out-soft", "tealWash",
             "09:00 - Deep work: portfolio",
             "50 min - timer ready", "Begin", False,
             "W1"),
        CARD("check-soft", "mossWash",
             "11:00 - Walk outside",
             "15 min - no podcast", "Done", True, "W2"),
        CARD("bolt-out-soft", "amberWash",
             "13:00 - Admin batch",
             "30 min - bills + inbox", "30 min", False,
             "W3"),
    ], "Yours", 120)

    s8 = SCREEN("08 Library", 3290, [
        HELLO("Library", "Ready-made calm", "H8"),
        SEARCH("Search activities", "Srch8"),
        SEC("Body", "", "S10"),
        CARD("drop-out-soft", "tealWash", "Drink water",
             "2 min - stand up, sip slowly", "+ Add",
             False, "L1"),
        CARD("bolt-out-soft", "amberWash", "Stretch",
             "5 min - neck, shoulders, back", "+ Add",
             False, "L2"),
        SEC("Reset", "", "S11"),
        CARD("bolt-out-soft", "amberWash",
             "Clear one surface",
             "2 min - just the desk corner", "+ Add",
             False, "L3"),
        CARD("sort-out-soft", "chipGray", "Box breathing",
             "3 min - in 4, hold 4, out 4", "+ Add",
             False, "L4"),
        SEC("Focus", "", "S12"),
        CARD("timer-out-soft", "chipGray", "Study sprint",
             "25 min - focus, 5 min break", "+ Add",
             False, "L5"),
        SEC("Evening", "", "S13"),
        CARD("nightlight-out-x", "mossWash", "Journal",
             "10 min - three lines, no filter", "+ Add",
             False, "L6"),
    ], "Yours", 30)

    s9 = SCREEN("09 Mood", 3760, [
        HELLO("Mood", "How today felt", "H9"),
        R(350, None, "card", 16, "MdCard", "vertical", [
            T("Good", 19, "ink", "700", "center", 318, DISP,
              "MdTi"),
            T("Tap how today felt overall", 12, "mute",
              "400", "center", 318, UI, "MdSb"),
            R(318, None, "card", 0, "MdRow", "horizontal", [
                IMG(f"{A}/m11-face-very-dis-x.png", 44, 44,
                    22, "Md1"),
                IMG(f"{A}/m11-face-dis-x.png", 44, 44, 22,
                    "Md2"),
                IMG(f"{A}/m11-face-neutral-x.png", 44, 44,
                    22, "Md3"),
                R(52, 52, "teal", 26, "Md4W", "vertical",
                  [IMG(f"{A}/m11-face-sat-x.png", 44, 44,
                       22, "Md4")],
                  align="center", justify="center"),
                IMG(f"{A}/m11-face-very-sat-x.png", 44, 44,
                    22, "Md5"),
            ], gap=6, align="center", justify="center"),
            R(318, 48, "teal", 14, "MdGo", "horizontal",
              [T("Log today", 13.5, "white", "700", "center",
                 290, DISP, "MdGoLb")],
              align="center", justify="center"),
        ], gap=10, align="center", padding=16,
          stroke="line", sw=1),
        SEC("Patterns", "", "S14"),
        R(350, None, "card", 16, "MdChart", "vertical", [
            T("Good days start before 09:00 - 5 of 7", 12,
              "soft", "400", "left", 318, UI, "MdIn"),
            R(318, 90, "card", 0, "MdBars", "horizontal", [
                R(34, 48, "amber", 6, "Mb1", "none", []),
                R(34, 64, "teal", 6, "Mb2", "none", []),
                R(34, 80, "teal", 6, "Mb3", "none", []),
                R(34, 56, "amber", 6, "Mb4", "none", []),
                R(34, 80, "teal", 6, "Mb5", "none", []),
                R(34, 40, "danger", 6, "Mb6", "none", []),
                R(34, 72, "teal", 6, "Mb7", "none", []),
            ], gap=6, align="end", justify="center"),
        ], gap=10, padding=12, stroke="line", sw=1),
    ], "Yours", 60)

    s10 = SCREEN("10 Pro", 4230, [
        HELLO("Puduu Pro", "Calm, unlimited", "H10"),
        R(350, None, "dark", 20, "PayHero", "vertical", [
            T("PUDUU PRO - 7 DAYS FREE", 10.5, "mint", "700",
              "left", 318, DISP, "PayTag"),
            T("Unlimited calm", 24, "white", "700", "left",
              318, DISP, "PayTi"),
            T("AI co-planner - web - sync - nudges", 12,
              "pale", "400", "left", 318, UI, "PayMt"),
            R(318, None, "card", 14, "Pk1", "horizontal",
              [IC("sort-out-soft", "tealWash", "Pk1"),
               R(170, None, "card", 0, "Pk1Tx", "vertical",
                 [T("AI Co-Planner", 13, "ink", "600", "left",
                    170, UI, "Pk1Ti"),
                  T("Brain-dump to schedule", 11, "mute",
                    "400", "left", 170, UI, "Pk1Sb")],
                 gap=2),
               T("Included", 11, "tealDeep", "700", "right",
                 56, UI, "Pk1Sd")],
              gap=10, align="center", padding=10),
            R(318, None, "card", 14, "Pk2", "horizontal",
              [IC("calendar-month-x", "amberWash", "Pk2"),
               R(170, None, "card", 0, "Pk2Tx", "vertical",
                 [T("Web + sync", 13, "ink", "600", "left",
                    170, UI, "Pk2Ti"),
                  T("Desktop + calendar import", 11, "mute",
                    "400", "left", 170, UI, "Pk2Sb")],
                 gap=2),
               T("Included", 11, "tealDeep", "700", "right",
                 56, UI, "Pk2Sd")],
              gap=10, align="center", padding=10),
        ], padding=16, gap=10),
        PLANROW("YEARLY - SAVE 30%", "$49.99 / year",
                "$4.17/mo - billed yearly", True, "Pl1"),
        PLANROW("MONTHLY", "$6.99 / month",
                "Cancel anytime", False, "Pl2"),
        R(350, 50, "teal", 14, "PayGo", "horizontal",
          [T("Start 7-day free trial", 14, "white", "700",
             "center", 318, DISP, "PayGoLb")],
          align="center", justify="center"),
        T("Restore purchase - Terms - Privacy", 11.5,
          "mute", "400", "center", 350, UI, "PayFt"),
    ], "Yours", 30)

    s11 = SCREEN("11 Welcome", 4700, [
        R(350, None, "bg", 0, "ObSp", "none", []),
        R(72, 72, "tealWash", 22, "ObIc", "vertical",
          [IMG(f"{A}/m11-calendar-month-x.png", 34, 34, 8,
               "ObIcI")],
          align="center", justify="center"),
        T("See your day", 26, "ink", "700", "left", 350,
          DISP, "ObTi"),
        T("A visual timeline built for busy brains - one block at a time.",
          14.5, "soft", "400", "left", 350, UI, "ObSb"),
        R(350, None, "bg", 0, "ObDots", "horizontal", [
            R(24, 8, "teal", 4, "ObD1", "none", []),
            R(8, 8, "line", 4, "ObD2", "none", []),
            R(8, 8, "line", 4, "ObD3", "none", []),
        ], gap=6, align="center"),
        R(350, 50, "teal", 14, "ObGo", "horizontal",
          [T("Next", 14, "white", "700", "center", 318,
             DISP, "ObGoLb")],
          align="center", justify="center"),
    ], "Today", 260)

    screens = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]
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
