"""Puduu .pen generator v3 — TOTAL REBUILD, premium soft-card system.
Kills v2's cheap full-bleed solid blocks. New language:
- white cards, 4px color rail on the left, tinted icon tile, dark text
- real app header (wordmark + date pill + avatar), section rows with actions
- bottom tab bar with active pill
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
    "pri": "#2563EB", "pdeep": "#1E40AF", "pale": "#EFF4FF",
    "sec": "#0E7490", "ssoft": "#E0F2F7", "acc": "#EA580C",
    "asoft": "#FFF1E7", "bg": "#F6F8FC", "ink": "#0F172A",
    "mut": "#475569", "line": "#E2E8F0", "card": "#FFFFFF",
    "ok": "#15803D", "oksoft": "#E7F6EC", "pink": "#E11D48",
    "pur": "#7C3AED", "pusoft": "#F1E9FF",
}
A = "./assets/icons"
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

# ---------- premium primitives ----------

def APPHEAD(greet, sub, name="Hd"):
    """Real app header: wordmark row + greeting block."""
    return R(358, 108, "bg", 0, f"{name}Wrap", "vertical",
             [R(358, 30, "bg", 0, f"{name}Top", "horizontal",
                [IMG(MASCOT, 28, 28, 9, f"{name}WmIc"),
                 T("PUDUU", 13, "pri", "800", "left", 90, "Fredoka",
                   f"{name}Wm"),
                 R(150, 30, "card", 15, f"{name}Date", "horizontal",
                   [IMG(f"{A}/calendar-check.png", 18, 18, 4,
                        f"{name}DateIc"),
                    T("Thu, Sep 25", 12, "mut", "700", "left",
                      name=f"{name}DateTx")],
                   gap=6, align="center", justify="center",
                   stroke="line", sw=1)],
                justify="space_between", align="center"),
              R(358, 64, "bg", 0, f"{name}Gr", "horizontal",
                [R(270, 60, "bg", 0, f"{name}GrTx", "vertical",
                   [T(greet, 24, "ink", "600", "left", 270, "Fredoka",
                      f"{name}Ti"),
                    T(sub, 13, "mut", "400", "left", 270, "Nunito",
                      f"{name}Sb")], gap=2),
                 IMG(MASCOT, 56, 56, 18, f"{name}Av")],
                gap=8, align="center")],
             gap=6)

def SECROW(label, action, name="Sec"):
    return R(358, 30, "bg", 0, name, "horizontal",
             [T(label, 12, "mut", "800", "left", 200, "Nunito",
                f"{name}Lb"),
              T(action, 12, "pri", "800", "right", 150, "Nunito",
                f"{name}Ac")],
             justify="space_between", align="center")

def TASKCARD(hour, mins, title, detail, rail, icon, tint, done=False,
             name="Tk"):
    """White card + 4px rail + tinted icon tile + dark text + status."""
    return R(358, 84, "card", 18, name, "horizontal",
             [R(5, 60, rail, 3, f"{name}Rail", "none", []),
              R(46, 46, tint, 15, f"{name}Tile", "none",
                [IMG(f"{A}/{icon}.png", 28, 28, 5, f"{name}Ic")],
                align="center", justify="center"),
              R(242, 62, "card", 0, f"{name}Tx", "vertical",
                [T(f"{hour} - {mins} MIN", 10, "mut", "800", "left", 242,
                   "Nunito", f"{name}Tm"),
                 T(title, 15, "ink", "800", "left", 242, "Nunito",
                   f"{name}Ti"),
                 T(detail, 12, "mut", "400", "left", 242, "Nunito",
                   f"{name}Sb")], gap=1)],
             padding=12, gap=10, align="center", stroke="line", sw=1)

def OPTCARD(icon, tint, title, detail, right="chevron-right", hot=False,
            name="Op"):
    return R(358, 72, "card", 16, name, "horizontal",
             [R(44, 44, tint, 14, f"{name}Tile", "none",
                [IMG(f"{A}/{icon}.png", 26, 26, 4, f"{name}Ic")],
                align="center", justify="center"),
              R(226, 52, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, "ink", "800", "left", 226, "Nunito",
                   f"{name}Ti"),
                 T(detail, 12, "mut", "400", "left", 226, "Nunito",
                   f"{name}Sb")], gap=2),
              IMG(f"{A}/{right}.png", 24, 24, 6, f"{name}Go")],
             padding=12, gap=10, align="center",
             stroke="pri" if hot else "line", sw=2 if hot else 1)

def CTA(label, bg="pri", name="Cta"):
    return R(326, 54, bg, 27, name, "horizontal",
             [T(label, 15, "#FFFFFF", "800", "center", name=f"{name}Lb")],
             align="center", justify="center")

def GHOST(label, name="Gh"):
    return R(326, 50, "card", 25, name, "horizontal",
             [T(label, 14, "pri", "800", "center", name=f"{name}Lb")],
             align="center", justify="center", stroke="pri", sw=1)

def TABBAR(active):
    tabs = [("sun", "Today"), ("timer", "Focus"), ("snowflake", "Reset"),
            ("trophy", "Progress"), ("settings", "Yours")]
    kids = []
    for ic, lb in tabs:
        on = lb == active
        kids.append(R(66, 60, "pale" if on else "card", 16, f"Tb{lb}",
                       "vertical",
                       [IMG(f"{A}/{ic}.png", 24, 24, 6, f"Tb{lb}Ic"),
                        T(lb, 10, "pri" if on else "mut", "800", "center",
                          name=f"Tb{lb}Lb")],
                       gap=3, align="center", justify="center"))
    return R(390, 88, "card", 0, "TabBar", "horizontal", kids,
             gap=3, align="center", justify="center")

def SCREEN(name, x, head, body, tab):
    col = [head,
           R(358, None, "bg", 0, f"{name}Bd", "vertical", body, gap=10,
             padding=[0, 0, 0, 0]),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x, "y": 0,
            "width": 390, "height": 844, "fill": C["bg"], "layout": "vertical",
            "alignItems": "center", "children": col}

def GLYPH():
    return {"id": "cmpCard", "type": "frame", "name": "CmpTaskCard",
            "x": 0, "y": 1200, "width": 358, "height": 84,
            "fill": C["card"], "cornerRadius": 18, "reusable": True,
            "layout": "horizontal", "padding": 12, "gap": 10,
            "alignItems": "center",
            "stroke": C["line"], "strokeWidth": 1,
            "slot": ["cmpSlot"],
            "children": [
                {"id": "cmpRail", "type": "frame", "name": "CmpRail",
                 "x": 0, "y": 0, "width": 5, "height": 60,
                 "fill": C["pri"], "cornerRadius": 3},
                {"id": "cmpSlot", "type": "text", "name": "Slot", "x": 0,
                 "y": 0, "content": "slot", "fill": C["ink"], "fontSize": 15,
                 "fontFamily": "Nunito", "fontWeight": "800",
                 "textAlign": "left", "textGrowth": "fixed-width",
                 "width": 280}]}

def LABELS(screens):
    return [{"id": nid(), "type": "text", "name": s["name"], "x": s["x"],
             "y": -50, "content": s["name"], "fill": C["mut"], "fontSize": 14,
             "fontFamily": "Nunito", "fontWeight": "800", "textAlign": "left"}
            for s in screens]

def main():
    s1 = SCREEN("01 Today", 0,
        APPHEAD("Good morning, Alex", "Thursday - 4 blocks - 2 done, steady pace.", "H1"),
        [R(358, 96, "pri", 20, "Hero", "horizontal",
           [R(212, 72, "pri", 0, "HeroTx", "vertical",
              [T("TODAY'S FOCUS", 10, "#FFFFFF", "800", "left", 206,
                 "Nunito", "HeroK"),
               T("Deep work: portfolio", 18, "#FFFFFF", "600", "left", 206,
                 "Fredoka", "HeroTi"),
               T("09:00 - 50 min - step 2 of 4", 12, "#FFFFFF", "400",
                 "left", 206, "Nunito", "HeroSb")], gap=3),
            R(104, 72, "pri", 0, "HeroGo", "vertical",
              [IMG(f"{A}/circle-play.png", 44, 44, 22, "HeroIc"),
               T("Start", 12, "#FFFFFF", "800", "center", name="HeroLb")],
              gap=4, align="center", justify="center")],
           padding=14, gap=6, align="center"),
         SECROW("UP NEXT", "See all", "S1"),
         TASKCARD("08:00", "25", "Morning reset", "Meds - water - 5-min tidy",
                  C["pri"], "sun-medium", "pale", False, "T1"),
         TASKCARD("09:00", "50", "Deep work: portfolio",
                  "Timer ready - step 2 of 4",
                  C["sec"], "timer", "ssoft", False, "T2"),
         TASKCARD("11:00", "15", "Walk outside", "Completed",
                  C["ok"], "check", "oksoft", True, "T3"),
         TASKCARD("13:00", "30", "Admin batch", "Bills + inbox",
                  C["acc"], "zap", "asoft", False, "T4"),
         SECROW("INBOX", "3 waiting", "S2"),
         R(358, 122, "card", 16, "InboxBx", "vertical",
           [T("Capture it here... e.g. call dentist", 14, "mut", "400",
              "left", 326, "Nunito", "InPh"),
            R(326, 52, "pri", 26, "SortBtn", "horizontal",
              [IMG(f"{A}/list-checks.png", 22, 22, 4, "SortIc"),
               T("Sort into my day", 15, "#FFFFFF", "800", "left",
                 name="SortLb")],
              gap=8, align="center", justify="center")],
           padding=12, gap=10, stroke="line", sw=1),
         {"id": nid(), "type": "ref", "name": "ResetCta", "x": 0, "y": 0,
          "ref": "cmpCard",
          "descendants": {"cmpSlot": {"content": "Stalling? Take a 2-minute reset"}}},
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        APPHEAD("Stay with it", "Deep work: portfolio - step 2 of 4.", "H2"),
        [R(358, 250, "card", 22, "DialBx", "vertical",
           [R(150, 150, "ssoft", 75, "DialRing", "vertical",
              [T("32:10", 32, "ink", "600", "center", 130, "Fredoka",
                 "DialTm"),
               T("LEFT", 10, "mut", "800", "center", 130, "Nunito",
                 "DialK")],
              gap=0, align="center", justify="center"),
            T("Sketch hero section - gentle chime at end", 13, "mut", "400",
              "center", 300, "Nunito", "DialSb")],
           padding=16, gap=10, align="center", stroke="line", sw=1),
         R(358, 58, "card", 29, "SegRow", "horizontal",
           [T("Pause", 14, "mut", "800", "center", 100, "Nunito", "Sg1"),
            T("+5 min", 14, "mut", "800", "center", 100, "Nunito", "Sg2"),
            R(104, 44, "pale", 22, "SgOn", "horizontal",
              [T("End", 14, "pri", "800", "center", name="Sg3")],
              align="center", justify="center")],
           padding=5, gap=4, align="center", stroke="line", sw=1),
         SECROW("SUB-STEPS", "2 of 3", "S3"),
         OPTCARD("circle-check", "oksoft", "Open file and music", "Done",
                 "circle-check", False, "F1"),
         OPTCARD("timer", "ssoft", "Sketch hero section",
                 "In progress - 10-min timer", "circle-play", True, "F2"),
         OPTCARD("plus", "pale", "Export PNG", "Up next", "chevron-right",
                 False, "F3"),
         GHOST("Next task - start the 15-sec ritual", "FGo"),
         ], "Focus")

    s3 = SCREEN("03 Reset", 940,
        APPHEAD("Hit a wall?", "Freeze reset - two minutes counts.", "H3"),
        [R(358, 148, "card", 20, "MascBx", "horizontal",
           [IMG(MASCOT, 92, 92, 20, "Mascot"),
            R(222, 118, "card", 0, "MascTx", "vertical",
              [T("HOW IT WORKS", 10, "mut", "800", "left", 222, "Nunito",
                 "RsK"),
               T("Pick the tiniest step.", 17, "ink", "600", "left", 222,
                 "Fredoka", "RsTi"),
               T("Puduu the pudu deer: slow is still moving. Two minutes unsticks most walls.",
                 12, "mut", "400", "left", 222, "Nunito", "RsSb")], gap=4)],
           padding=14, gap=12, align="center", stroke="line", sw=1),
         SECROW("TINY STEPS", "Free 2/day", "S4"),
         OPTCARD("glass-water", "ssoft", "Drink a glass of water",
                 "2 min - raises energy", "circle-play", True, "R1"),
         OPTCARD("footprints", "oksoft", "Clear one surface",
                 "2 min - just the desk corner", "circle-play", False, "R2"),
         OPTCARD("mail-open", "pusoft", "Open the difficult email",
                 "Just open it. Reply later.", "circle-play", False, "R3"),
         OPTCARD("sparkles", "pale", "Sort my inbox",
                 "Rule-based now - assisted later", "chevron-right", False,
                 "R4"),
         R(358, 56, "pale", 14, "RNote", "horizontal",
           [IMG(f"{A}/shield-check.png", 24, 24, 6, "RN Ic"),
            T("Skipping is allowed - Puduu waits.", 12, "mut", "700",
              "left", 290, "Nunito", "RNTx")],
           padding=12, gap=8, align="center"),
         ], "Reset")

    s4 = SCREEN("04 Ritual", 1410,
        APPHEAD("Between tasks", "Transition - fifteen seconds.", "H4"),
        [T("Close, breathe, begin.", 22, "ink", "600", "left", 358, "Fredoka",
           "RiTi"),
         R(358, 30, "bg", 0, "RiBar", "horizontal",
           [R(120, 8, "pri", 4, "RiP1", "none", []),
            R(100, 8, "line", 4, "RiP2", "none", []),
            R(100, 8, "line", 4, "RiP3", "none", [])],
           gap=8, align="center"),
         OPTCARD("check", "oksoft", "1 - Close",
                 "Portfolio file saved. Put it away.", "circle-check",
                 False, "St1"),
         OPTCARD("moon-star", "ssoft", "2 - Breathe",
                 "One slow breath with the ring.", "circle-play", True,
                 "St2"),
         OPTCARD("zap", "asoft", "3 - Begin",
                 "Next up: Admin batch - 30 min.", "circle-play", False,
                 "St3"),
         CTA("Begin Admin batch", "pri", "RiGo"),
         GHOST("Not yet - back to Today", "RiBack"),
         ], "Focus")

    s5 = SCREEN("05 Progress", 1880,
        APPHEAD("Keep growing", "Good days: 5 of 7 - never resets to zero.",
                "H5"),
        [R(358, 150, "card", 20, "ConsBx", "vertical",
           [R(326, 30, "card", 0, "ConsTop", "horizontal",
              [T("CONSISTENCY", 10, "mut", "800", "left", 160, "Nunito",
                 "ConsK"),
               T("71%", 20, "ink", "600", "right", 150, "Fredoka",
                 "ConsV")],
              justify="space_between", align="center"),
            R(326, 14, "bg", 7, "ConsTr", "horizontal",
              [R(232, 14, "sec", 7, "ConsFl", "none", [])]),
            T("5 steady days - 2 slow days - both are fine.", 12, "mut",
              "400", "left", 326, "Nunito", "ConsS")],
           padding=14, gap=8, stroke="line", sw=1),
         SECROW("TROPHIES", "View all", "S5"),
         OPTCARD("trophy", "asoft", "Weekly shelf",
                 "Early starter x3 - Reset used x5 - Focus 25m x8",
                 "chevron-right", False, "G1"),
         OPTCARD("trending-up", "oksoft", "Focus trend",
                 "Up 20% vs last week - mornings work best",
                 "chevron-right", False, "G2"),
         SECROW("MOOD TODAY", "Okay", "S6"),
         R(358, 76, "card", 16, "MoodRow", "horizontal",
           [IMG(f"{A}/smile.png", 40, 40, 12, "Md1"),
            IMG(f"{A}/star.png", 40, 40, 12, "Md2"),
            IMG(f"{A}/heart.png", 40, 40, 12, "Md3")],
           padding=12, gap=12, align="center", justify="center",
           stroke="line", sw=1),
         ], "Progress")

    s6 = SCREEN("06 Sort", 2350,
        APPHEAD("Review the plan", "Drag to reorder - then apply.", "H6"),
        [SECROW("SUGGESTED ORDER", "Rule-based", "S7"),
         OPTCARD("zap", "pale", "Call dentist",
                 "Tiny first - 10 min - 09:00", "chevron-right", True, "P1"),
         OPTCARD("zap", "pale", "Pay electricity bill",
                 "Tiny first - 15 min - 09:15", "chevron-right", False,
                 "P2"),
         OPTCARD("calendar-check", "ssoft", "Deep work: portfolio hero",
                 "Big block - 50 min - 10:00", "chevron-right", False, "P3"),
         CTA("Apply to Today", "pri", "SoGo"),
         R(358, 78, "card", 14, "SoNt", "horizontal",
           [IMG(f"{A}/circle-help.png", 24, 24, 6, "SoNtIc"),
            T("Urgent words first, tiny tasks first, low energy avoids big blocks. Assisted planning slots in here later.",
              12, "mut", "400", "left", 286, "Nunito", "SoNtT")],
           padding=12, gap=8, align="center", stroke="line", sw=1),
         ], "Today")

    s7 = SCREEN("07 Yours", 2820,
        APPHEAD("Make it yours", "Settings, plan, and backup.", "H7"),
        [R(358, 190, "pri", 22, "ProBx", "vertical",
           [R(326, 56, "pri", 0, "ProTx", "horizontal",
              [IMG(f"{A}/crown.png", 42, 42, 13, "ProIc"),
               R(266, 54, "pri", 0, "ProTx2", "vertical",
                 [T("PUDUU PRO", 10, "#FFFFFF", "800", "left", 266,
                    "Nunito", "ProK"),
                  T("$6.99/mo - yearly $49.99", 18, "#FFFFFF", "600",
                    "left", 266, "Fredoka", "ProT")], gap=2)],
              gap=10, align="center"),
            T("Unlimited resets - assisted planning (soon) - widgets on every device.",
              12, "#FFFFFF", "400", "left", 326, "Nunito", "ProS"),
            R(326, 50, "card", 25, "ProGo", "horizontal",
              [T("Try 7 days free", 15, "pri", "800", "center",
                 name="ProLb")], align="center", justify="center")],
           padding=14, gap=10),
         SECROW("PREFERENCES", "", "S8"),
         OPTCARD("bell", "asoft", "Gentle nudges",
                 "Max 6 per day - quiet 22:00-07:00 on", "chevron-right",
                 False, "Y1"),
         OPTCARD("flame", "asoft", "Sounds and haptics",
                 "Calm chime - soft vibration on", "chevron-right", False,
                 "Y2"),
         OPTCARD("languages", "pale", "Language and text",
                 "English - Large text available", "chevron-right", False,
                 "Y3"),
         OPTCARD("wallet", "pusoft", "Backup and export",
                 "On-device first - export anytime", "chevron-right", False,
                 "Y4"),
         ], "Yours")

    screens = [s1, s2, s3, s4, s5, s6, s7]
    doc = {"version": "2.19", "name": "Puduu MVP v3",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": [GLYPH()] + screens + LABELS(screens)}
    json.dump(doc, open("puduu.pen", "w"), indent=1)
    print("wrote puduu.pen v3")

main()
