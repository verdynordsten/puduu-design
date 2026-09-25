"""Puduu .pen generator v4 — EDITORIAL CALM total rebuild.
New language: paper background, ink, white cards, right-aligned tabular
time gutter, 4px rails, tinted tiles, dark hero, minimal tab bar with
indicator (no toy pills), Fredoka display-only. Every centered moment is
truly centered (textAlign center + centered containers).
Zero emoji. Schema 2.19. Run: python3 gen_puduu_pen.py -> puduu.pen
"""
import json, itertools

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
    "paper": "#FAFAF8", "card": "#FFFFFF", "ink": "#111827",
    "slate": "#4B5563", "faint": "#9AA1AD", "line": "#E6E4DE",
    "pri": "#2563EB", "pdeep": "#1E40AF", "pale": "#EDF2FF",
    "heroA": "#101828", "heroB": "#232F4B",
    "teal": "#0E7490", "tealSoft": "#E4F3F6",
    "amber": "#EA580C", "amberSoft": "#FFF3E8",
    "green": "#15803D", "greenSoft": "#EAF5EE",
    "pur": "#7C3AED", "purSoft": "#F2EAFB",
}
A = "./assets/icons"
MARK = "./assets/puduu-mark.png"
MASCOT = "./assets/puduu-mascot.png"

def T(content, size=15, color="ink", weight="400", align="left", width=None,
      family="Nunito", name="Txt"):
    n = {"id": nid(), "type": "text", "name": name, "x": 0, "y": 0,
         "content": content, "fill": C.get(color, color),
         "fontSize": size, "fontFamily": family,
         "fontWeight": weight, "textAlign": align}
    if width is not None:
        n["width"] = width
        n["textGrowth"] = "fixed-width"
    return n

def IMG(url, w, h, radius=8, name="Img"):
    return {"id": nid(), "type": "rectangle", "name": name, "x": 0, "y": 0,
            "width": w, "height": h, "cornerRadius": radius,
            "fill": {"type": "image", "url": url, "mode": "fill"}}

def R(width=None, height=None, fill="card", radius=14, name="Box", layout=None,
      children=None, padding=None, gap=None, align=None, justify=None,
      stroke=None, sw=None):
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
        n["justify"] = justify
    if stroke:
        n["stroke"] = C.get(stroke, stroke)
    if sw:
        n["strokeWidth"] = sw
    n["children"] = children or []
    return n

# ---------- editorial primitives ----------

def HEAD(greet, sub, name="Hd"):
    return R(358, 104, "paper", 0, f"{name}Wrap", "vertical",
             [R(358, 30, "paper", 0, f"{name}Top", "horizontal",
                [R(150, 30, "paper", 0, f"{name}Wm", "horizontal",
                   [IMG(MARK, 26, 26, 8, f"{name}WmIc"),
                    T("Puduu", 17, "ink", "600", "left", 80, "Fredoka",
                      f"{name}WmTx")], gap=7, align="center"),
                 R(140, 30, "card", 15, f"{name}Date", "horizontal",
                   [IMG(f"{A}/calendar-check.png", 17, 17, 4,
                        f"{name}DateIc"),
                    T("Thu Sep 25", 12, "slate", "700", "left",
                      name=f"{name}DateTx")],
                   gap=6, align="center", justify="center",
                   stroke="line", sw=1)],
                justify="space_between", align="center"),
              T(greet, 26, "ink", "600", "left", 358, "Fredoka",
                f"{name}Ti"),
              T(sub, 13, "slate", "400", "left", 358, "Nunito",
                f"{name}Sb")],
             gap=6)

def SEC(label, action="", name="Sec"):
    kids = [T(label, 11, "slate", "800", "left", 190, "Nunito",
               f"{name}Lb")]
    if action:
        kids.append(T(action, 12, "pri", "800", "right", 160, "Nunito",
                      f"{name}Ac"))
    return R(358, 28, "paper", 0, name, "horizontal", kids,
             justify="space_between", align="center")

def TROW(hour, mins, title, detail, rail, icon, tint, done=False, name="Tr"):
    """Editorial timeline row: right-aligned time gutter + rail + tile."""
    title_color = "slate" if done else "ink"
    return R(358, 82, "card", 20, name, "horizontal",
             [R(52, 58, "card", 0, f"{name}Gut", "vertical",
                [T(hour, 14, "slate" if done else "ink", "800", "right", 52,
                   "Nunito", f"{name}Hr"),
                 T(mins, 11, "faint", "700", "right", 52, "Nunito",
                   f"{name}Du")], gap=1),
              R(4, 58, rail, 2, f"{name}Rail", "none", []),
              R(44, 44, tint, 15, f"{name}Tile", "none",
                [IMG(f"{A}/{icon}.png", 26, 26, 5, f"{name}Ic")],
                align="center", justify="center"),
              R(206, 62, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, title_color, "800", "left", 206, "Nunito",
                   f"{name}Ti"),
                 T(detail if not done else "Done",
                   12, "slate", "400", "left", 206, "Nunito", f"{name}Sb")],
                gap=2)],
             padding=12, gap=8, align="center", stroke="line", sw=1)

def OPT(icon, tint, title, detail, name="Op"):
    return R(358, 72, "card", 18, name, "horizontal",
             [R(44, 44, tint, 15, f"{name}Tile", "none",
                [IMG(f"{A}/{icon}.png", 26, 26, 4, f"{name}Ic")],
                align="center", justify="center"),
              R(272, 54, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, "ink", "800", "left", 272, "Nunito",
                   f"{name}Ti"),
                 T(detail, 12, "slate", "400", "left", 272, "Nunito",
                   f"{name}Sb")], gap=2)],
             padding=12, gap=10, align="center", stroke="line", sw=1)

def CTA(label, bg="pri", name="Cta", width=358):
    return R(width, 56, bg, 28, name, "horizontal",
             [T(label, 15, "#FFFFFF", "800", "center", name=f"{name}Lb")],
             align="center", justify="center")

def GHOST(label, name="Gh"):
    return R(358, 52, "card", 26, name, "horizontal",
             [T(label, 14, "pri", "800", "center", name=f"{name}Lb")],
             align="center", justify="center", stroke="pri", sw=1)

def HERO(kicker, title, meta, pct, btn, name="Hero"):
    return R(358, 168, "heroA", 22, name, "vertical",
             [T(kicker, 10, "#FFFFFF", "800", "left", 326, "Nunito",
                f"{name}K"),
              T(title, 20, "#FFFFFF", "600", "left", 326, "Fredoka",
                f"{name}Ti"),
              T(meta, 12, "#FFFFFF", "400", "left", 326, "Nunito",
                f"{name}Sb"),
              R(326, 10, "heroB", 5, f"{name}Tr", "horizontal",
                [R(pct, 10, "pri", 5, f"{name}Fl", "none", [])]),
              R(326, 48, "card", 24, f"{name}Go", "horizontal",
                [IMG(f"{A}/circle-play.png", 22, 22, 11, f"{name}GoIc"),
                 T(btn, 14, "pri", "800", "left", name=f"{name}GoLb")],
                gap=8, align="center", justify="center")],
             padding=14, gap=7)

def CENTERED_TEXT(content, size, color, weight, family, width, name):
    return T(content, size, color, weight, "center", width, family, name)

def TABBAR(active):
    tabs = [("sun", "Today"), ("timer", "Focus"), ("snowflake", "Reset"),
            ("trophy", "Progress"), ("settings", "Yours")]
    kids = []
    for ic, lb in tabs:
        on = lb == active
        kids.append(R(64, 62, "card", 0, f"Tb{lb}", "vertical",
                       [IMG(f"{A}/{ic}.png", 24, 24, 6, f"Tb{lb}Ic"),
                        T(lb, 10, "pri" if on else "faint", "800",
                          "center", 64, "Nunito", f"Tb{lb}Lb"),
                        R(20, 3, "pri" if on else "card", 2,
                          f"Tb{lb}Ind", "none", [])],
                       gap=3, align="center", justify="center"))
    return R(390, 88, "card", 0, "TabBar", "horizontal", kids,
             gap=2, align="center", justify="center")

def SCREEN(name, x, head, body, tab):
    col = [head,
           R(358, None, "paper", 0, f"{name}Bd", "vertical", body, gap=10,
             padding=[0, 0, 0, 0]),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x, "y": 0,
            "width": 390, "height": 844, "fill": C["paper"],
            "layout": "vertical", "alignItems": "center", "children": col}

def GLYPH():
    return {"id": "cmpCard", "type": "frame", "name": "CmpTimelineRow",
            "x": 0, "y": 1200, "width": 358, "height": 82,
            "fill": C["card"], "cornerRadius": 20, "reusable": True,
            "layout": "horizontal", "padding": 12, "gap": 8,
            "alignItems": "center",
            "stroke": C["line"], "strokeWidth": 1,
            "slot": ["cmpSlot"],
            "children": [
                {"id": "cmpRail", "type": "frame", "name": "CmpRail",
                 "x": 0, "y": 0, "width": 4, "height": 58,
                 "fill": C["pri"], "cornerRadius": 2},
                {"id": "cmpSlot", "type": "text", "name": "Slot", "x": 0,
                 "y": 0, "content": "slot", "fill": C["ink"], "fontSize": 15,
                 "fontFamily": "Nunito", "fontWeight": "800",
                 "textAlign": "left", "textGrowth": "fixed-width",
                 "width": 290}]}

def LABELS(screens):
    return [{"id": nid(), "type": "text", "name": s["name"], "x": s["x"],
             "y": -50, "content": s["name"], "fill": C["slate"],
             "fontSize": 14, "fontFamily": "Nunito", "fontWeight": "800",
             "textAlign": "left"}
            for s in screens]

def main():
    s1 = SCREEN("01 Today", 0,
        HEAD("Good morning, Alex", "Thursday, Sep 25 · 4 blocks planned.", "H1"),
        [HERO("TODAY'S FOCUS", "Deep work: portfolio",
              "09:00 · 50 min · step 2 of 4", 200, "Start focus", "Hero"),
         SEC("UP NEXT", "See all", "S1"),
         TROW("08:00", "25 MIN", "Morning reset", "Meds · water · 5-min tidy",
              C["pri"], "sun-medium", "pale", False, "T1"),
         TROW("09:00", "50 MIN", "Deep work: portfolio",
              "Timer ready · step 2 of 4",
              C["teal"], "timer", "tealSoft", False, "T2"),
         TROW("11:00", "15 MIN", "Walk outside", "",
              C["green"], "check", "greenSoft", True, "T3"),
         TROW("13:00", "30 MIN", "Admin batch", "Bills + inbox",
              C["amber"], "zap", "amberSoft", False, "T4"),
         SEC("INBOX", "3 waiting", "S2"),
         R(358, 128, "card", 18, "InboxBx", "vertical",
           [T("Capture a task, idea, or reminder…", 14, "slate", "400",
              "left", 326, "Nunito", "InPh"),
            CTA("Sort into my day", "pri", "SortBtn", 326)],
           padding=12, gap=10, stroke="line", sw=1),
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        HEAD("Stay with it.", "Deep work: portfolio · step 2 of 4.", "H2"),
        [R(358, 264, "card", 24, "DialBx", "vertical",
           [CENTERED_TEXT("FOCUS SESSION", 10, "slate", "800", "Nunito",
                          326, "DialK"),
            R(160, 160, "tealSoft", 80, "DialRing", "vertical",
              [CENTERED_TEXT("32:10", 34, "ink", "600", "Fredoka", 140,
                             "DialTm"),
               CENTERED_TEXT("LEFT", 10, "slate", "800", "Nunito", 140,
                             "DialU")],
              gap=0, align="center", justify="center"),
            CENTERED_TEXT("Sketch hero section · gentle chime at end", 13,
                          "slate", "400", "Nunito", 326, "DialSb")],
           padding=16, gap=10, align="center", stroke="line", sw=1),
         R(358, 58, "card", 29, "SegRow", "horizontal",
           [T("Pause", 14, "slate", "800", "center", 100, "Nunito", "Sg1"),
            T("+5 min", 14, "slate", "800", "center", 100, "Nunito", "Sg2"),
            R(104, 44, "pale", 22, "SgOn", "horizontal",
              [T("End", 14, "pri", "800", "center", name="Sg3")],
              align="center", justify="center")],
           padding=5, gap=4, align="center", stroke="line", sw=1),
         SEC("SUB-STEPS", "2 of 3", "S3"),
         OPT("circle-check", "greenSoft", "Open file and music", "Done",
             "F1"),
         OPT("timer", "tealSoft", "Sketch hero section",
             "In progress · 10-min timer", "F2"),
         OPT("plus", "pale", "Export PNG", "Up next", "F3"),
         GHOST("Next task — start the 15-sec ritual", "FGo"),
         ], "Focus")

    s3 = SCREEN("03 Reset", 940,
        HEAD("Hit a wall?", "Freeze reset · two minutes counts.", "H3"),
        [R(358, 176, "card", 22, "MascBx", "vertical",
           [IMG(MASCOT, 88, 88, 20, "Mascot"),
            CENTERED_TEXT("HOW IT WORKS", 10, "slate", "800", "Nunito",
                          326, "RsK"),
            CENTERED_TEXT("Pick the tiniest step.", 19, "ink", "600",
                          "Fredoka", 326, "RsTi"),
            CENTERED_TEXT("Slow is still moving. Two minutes unsticks most walls.",
                          13, "slate", "400", "Nunito", 326, "RsSb")],
           padding=14, gap=6, align="center", stroke="line", sw=1),
         SEC("TINY STEPS", "Free 2/day", "S4"),
         OPT("glass-water", "tealSoft", "Drink a glass of water",
             "2 min · raises energy", "R1"),
         OPT("footprints", "greenSoft", "Clear one surface",
             "2 min · just the desk corner", "R2"),
         OPT("mail-open", "purSoft", "Open the difficult email",
             "Just open it. Reply later.", "R3"),
         OPT("sparkles", "pale", "Sort my inbox",
             "Rule-based now · assisted later", "R4"),
         R(358, 56, "pale", 14, "RNote", "horizontal",
           [IMG(f"{A}/shield-check.png", 24, 24, 6, "RNIc"),
            T("Skipping is allowed — Puduu waits.", 12, "slate", "700",
              "left", 292, "Nunito", "RNTx")],
           padding=12, gap=8, align="center"),
         ], "Reset")

    s4 = SCREEN("04 Ritual", 1410,
        HEAD("Between tasks.", "Transition · fifteen seconds.", "H4"),
        [R(358, 120, "card", 22, "RiHead", "vertical",
           [CENTERED_TEXT("TRANSITION", 10, "slate", "800", "Nunito", 326,
                          "RiK"),
            CENTERED_TEXT("Close, breathe, begin.", 22, "ink", "600",
                          "Fredoka", 326, "RiTi"),
            R(200, 8, "paper", 4, "RiBar", "horizontal",
              [R(64, 8, "pri", 4, "RiP1", "none", []),
               R(56, 8, "line", 4, "RiP2", "none", []),
               R(56, 8, "line", 4, "RiP3", "none", [])],
              gap=6, align="center", justify="center")],
           padding=14, gap=8, align="center", stroke="line", sw=1),
         OPT("check", "greenSoft", "1 · Close",
             "Portfolio file saved. Put it away.", "St1"),
         OPT("moon-star", "tealSoft", "2 · Breathe",
             "One slow breath with the ring.", "St2"),
         OPT("zap", "amberSoft", "3 · Begin",
             "Next up: Admin batch · 30 min.", "St3"),
         CTA("Begin Admin batch", "pri", "RiGo"),
         GHOST("Not yet — back to Today", "RiBack"),
         ], "Focus")

    s5 = SCREEN("05 Progress", 1880,
        HEAD("Keep growing.", "Good days: 5 of 7 · never resets to zero.",
             "H5"),
        [R(358, 158, "card", 22, "ConsBx", "vertical",
           [R(326, 30, "card", 0, "ConsTop", "horizontal",
              [T("CONSISTENCY", 10, "slate", "800", "left", 160, "Nunito",
                 "ConsK"),
               T("71%", 22, "ink", "600", "right", 150, "Fredoka",
                 "ConsV")],
              justify="space_between", align="center"),
            R(326, 14, "paper", 7, "ConsTr", "horizontal",
              [R(232, 14, "teal", 7, "ConsFl", "none", [])]),
            T("5 steady days · 2 slow days · both are fine.", 12, "slate",
              "400", "center", 326, "Nunito", "ConsS")],
           padding=14, gap=8, align="center", stroke="line", sw=1),
         SEC("TROPHIES", "View all", "S5"),
         OPT("trophy", "amberSoft", "Weekly shelf",
             "Early starter ×3 · Reset used ×5 · Focus 25m ×8", "G1"),
         OPT("trending-up", "greenSoft", "Focus trend",
             "Up 20% vs last week · mornings work best", "G2"),
         SEC("MOOD TODAY", "Okay", "S6"),
         R(358, 144, "card", 18, "MoodBx", "vertical",
           [R(326, 52, "card", 0, "MoodRow", "horizontal",
              [IMG(f"{A}/smile.png", 44, 44, 13, "Md1"),
               IMG(f"{A}/star.png", 44, 44, 13, "Md2"),
               IMG(f"{A}/heart.png", 44, 44, 13, "Md3")],
              gap=12, align="center", justify="center"),
            CENTERED_TEXT("Low · Flat · Okay (selected) · Good · Great",
                          12, "slate", "400", "Nunito", 326, "MoodTx")],
           padding=12, gap=8, align="center", stroke="line", sw=1),
         ], "Progress")

    s6 = SCREEN("06 Sort", 2350,
        HEAD("Review the plan.", "Drag to reorder · then apply.", "H6"),
        [SEC("SUGGESTED ORDER", "Rule-based", "S7"),
         OPT("zap", "pale", "Call dentist",
             "Tiny first · 10 min · 09:00", "P1"),
         OPT("zap", "pale", "Pay electricity bill",
             "Tiny first · 15 min · 09:15", "P2"),
         OPT("calendar-check", "tealSoft", "Deep work: portfolio hero",
             "Big block · 50 min · 10:00", "P3"),
         CTA("Apply to Today", "pri", "SoGo"),
         R(358, 84, "card", 14, "SoNt", "horizontal",
           [IMG(f"{A}/circle-help.png", 24, 24, 6, "SoNtIc"),
            T("Urgent words first, tiny tasks first, low energy avoids big blocks. Assisted planning slots in here later.",
              12, "slate", "400", "left", 288, "Nunito", "SoNtT")],
           padding=12, gap=8, align="center", stroke="line", sw=1),
         ], "Today")

    s7 = SCREEN("07 Yours", 2820,
        HEAD("Make it yours.", "Settings, plan, and backup.", "H7"),
        [R(358, 196, "heroA", 24, "ProBx", "vertical",
           [T("PUDUU PRO", 10, "#FFFFFF", "800", "left", 326, "Nunito",
              "ProK"),
            T("$6.99/mo · yearly $49.99", 20, "#FFFFFF", "600", "left",
              326, "Fredoka", "ProT"),
            T("Unlimited resets · assisted planning (soon) · widgets on every device.",
              12, "#FFFFFF", "400", "left", 326, "Nunito", "ProS"),
            R(326, 50, "card", 25, "ProGo", "horizontal",
              [IMG(f"{A}/crown.png", 22, 22, 6, "ProIc"),
               T("Try 7 days free", 15, "pri", "800", "left",
                 name="ProLb")],
              gap=8, align="center", justify="center")],
           padding=14, gap=8),
         SEC("PREFERENCES", "", "S8"),
         OPT("bell", "amberSoft", "Gentle nudges",
             "Max 6 per day · quiet 22:00–07:00 on", "Y1"),
         OPT("flame", "amberSoft", "Sounds and haptics",
             "Calm chime · soft vibration on", "Y2"),
         OPT("languages", "pale", "Language and text",
             "English · Large text available", "Y3"),
         OPT("wallet", "purSoft", "Backup and export",
             "On-device first · export anytime", "Y4"),
         ], "Yours")

    screens = [s1, s2, s3, s4, s5, s6, s7]
    doc = {"version": "2.19", "name": "Puduu MVP v4 Editorial Calm",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": [GLYPH()] + screens + LABELS(screens)}
    json.dump(doc, open("puduu.pen", "w"), indent=1)
    print("wrote puduu.pen v4")

main()
