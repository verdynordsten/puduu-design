"""Puduu .pen generator v2 — professional rebuild.
Zero emoji in UI. Icons: 27 real Lucide PNGs + mascot (used sparingly).
7 screens, 390px, schema 2.19. Run: python3 gen_puduu_pen.py -> puduu.pen
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
    "pri": "#2563EB", "pdeep": "#1D4ED8", "sec": "#0E7490",
    "ssoft": "#E0F2F7", "acc": "#EA580C", "adeep": "#C2410C",
    "asoft": "#FFF1E7", "bg": "#F6F8FC", "ink": "#0F172A",
    "mut": "#475569", "line": "#E2E8F0", "card": "#FFFFFF",
    "mutbg": "#EFF4FF", "ok": "#15803D", "oksoft": "#E7F6EC",
    "pink": "#E11D48", "pur": "#9333EA",
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

def TABBAR(active):
    tabs = [("sun", "Today"), ("timer", "Focus"), ("snowflake", "Reset"),
            ("trophy", "Grows"), ("settings", "Yours")]
    kids = []
    for ic, lb in tabs:
        on = lb == active
        kids.append(R(64, 58, "mutbg" if on else "card", 14, f"Tb{lb}",
                       "vertical",
                       [IMG(f"{A}/{ic}.png", 24, 24, 6, f"Tb{lb}Ic"),
                        T(lb, 10, "pri" if on else "mut", "800", "center",
                          name=f"Tb{lb}Lb")],
                       gap=3, align="center", justify="center"))
    return R(390, 86, "card", 0, "TabBar", "horizontal", kids,
             gap=4, align="center", justify="center")

def HEAD(icon, title, sub, name="Hd"):
    return R(390, 76, "bg", 0, f"{name}Bar", "horizontal",
             [IMG(f"{A}/{icon}.png", 40, 40, 13, f"{name}Ic"),
              R(300, 56, "bg", 0, f"{name}Tx", "vertical",
                [T(title, 20, "ink", "600", "left", 300, "Fredoka", f"{name}Ti"),
                 T(sub, 13, "mut", "400", "left", 300, "Nunito", f"{name}Sb")],
                gap=1)],
             padding=[8, 16, 8, 16], gap=10, align="center")

def MICRO(label, name="Cap"):
    return T(label, 11, "mut", "800", "left", 358, "Nunito", name)

def BLOCK(hour, mins, title, detail, hue, icon, done=False, name="Bl"):
    return R(358, 82, hue, 16, name, "horizontal",
             [IMG(f"{A}/{icon}.png", 40, 40, 13, f"{name}Ic"),
              R(230, 58, hue, 0, f"{name}Tx", "vertical",
                [T(f"{hour} - {mins} MIN", 11, "#FFFFFF", "800", "left", 230,
                   "Nunito", f"{name}Tm"),
                 T(title, 15, "#FFFFFF", "800", "left", 230, "Nunito",
                   f"{name}Ti"),
                 T(detail, 12, "#FFFFFF", "400", "left", 230, "Nunito",
                   f"{name}Sb")], gap=1),
              IMG(f"{A}/circle-check.png" if done else f"{A}/chevron-right.png",
                  26, 26, 13, f"{name}St")],
             padding=12, gap=10, align="center")

def OPTROW(icon, tilebg, tilefg, title, detail, hot=False, name="Op"):
    return R(358, 74, "card", 16, name, "horizontal",
             [R(44, 44, tilebg, 14, f"{name}Tile", "none",
                [IMG(f"{A}/{icon}.png", 26, 26, 4, f"{name}Ic")],
                align="center", justify="center"),
              R(272, 54, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, "ink", "800", "left", 272, "Nunito", f"{name}Ti"),
                 T(detail, 12, "mut", "400", "left", 272, "Nunito",
                   f"{name}Sb")], gap=2)],
             padding=12, gap=10, align="center",
             stroke="pri" if hot else None, sw=2 if hot else None)

def CTA(label, bg="pri", name="Cta"):
    return R(326, 54, bg, 27, name, "horizontal",
             [T(label, 15, "#FFFFFF", "800", "center", name=f"{name}Lb")],
             align="center", justify="center")

def SCREEN(name, x, head, body, tab):
    col = [head,
           R(358, None, "bg", 0, f"{name}Bd", "vertical", body, gap=10),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x, "y": 0,
            "width": 390, "height": 844, "fill": C["bg"], "layout": "vertical",
            "alignItems": "center", "children": col}

def GLYPH():
    return {"id": "cmpCard", "type": "frame", "name": "CmpCardShell",
            "x": 0, "y": 1200, "width": 358, "height": 74,
            "fill": C["card"], "cornerRadius": 16, "reusable": True,
            "layout": "horizontal", "padding": 12, "gap": 10,
            "alignItems": "center",
            "stroke": C["line"], "strokeWidth": 1,
            "slot": ["cmpSlot"],
            "children": [
                {"id": "cmpTile", "type": "frame", "name": "SlotTile",
                 "x": 0, "y": 0, "width": 44, "height": 44,
                 "fill": C["mutbg"], "cornerRadius": 14},
                {"id": "cmpSlot", "type": "text", "name": "Slot", "x": 0,
                 "y": 0, "content": "slot", "fill": C["ink"], "fontSize": 15,
                 "fontFamily": "Nunito", "fontWeight": "800",
                 "textAlign": "left", "textGrowth": "fixed-width",
                 "width": 250}]}

def LABELS(screens):
    out = []
    for s in screens:
        out.append({"id": nid(), "type": "text", "name": s["name"], "x": s["x"],
                    "y": -50, "content": s["name"], "fill": C["mut"],
                    "fontSize": 14, "fontFamily": "Nunito", "fontWeight": "800",
                    "textAlign": "left"})
    return out

def main():
    s1 = SCREEN("01 Today", 0,
        HEAD("sun", "Good morning", "Thursday - 4 blocks - small steps count.", "H1"),
        [MICRO("TODAY'S TIMELINE", "C1"),
         BLOCK("08:00", "25", "Morning reset", "Meds - water - 5-min tidy",
               C["pri"], "check", False, "B1"),
         BLOCK("09:00", "50", "Deep work: portfolio", "Timer ready - step 2 of 4",
               C["sec"], "timer", False, "B2"),
         BLOCK("11:00", "15", "Walk outside", "Completed",
               C["ok"], "circle-check", True, "B3"),
         BLOCK("13:00", "30", "Admin batch", "Bills + inbox",
               C["acc"], "zap", False, "B4"),
         MICRO("INBOX - BRAIN DUMP", "C2"),
         R(358, 122, "card", 16, "InboxBx", "vertical",
           [T("Capture it here... e.g. call dentist", 14, "mut", "400", "left",
              326, "Nunito", "InPh"),
            R(326, 54, "pri", 27, "SortBtn", "horizontal",
              [T("Sort for me", 15, "#FFFFFF", "800", "center",
                 name="SortLb")], align="center", justify="center")],
           padding=12, gap=10, stroke="line", sw=1),
         {"id": nid(), "type": "ref", "name": "RescueCta", "x": 0, "y": 0,
          "ref": "cmpCard",
          "descendants": {"cmpSlot": {"content": "Feeling stuck? Get one tiny step"}}},
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        HEAD("timer", "Deep work: portfolio", "Step 2 of 4 - sketch hero section", "H2"),
        [R(358, 196, "card", 18, "DialBx", "vertical",
           [IMG(f"{A}/timer.png", 52, 52, 10, "DialIc"),
            T("32:10 left", 30, "ink", "600", "center", 300, "Fredoka", "DialTm"),
            T("gentle chime at end", 13, "mut", "400", "center", 300, "Nunito",
              "DialSb")],
           padding=14, gap=6, align="center", stroke="line", sw=1),
         R(358, 58, "card", 29, "SegRow", "horizontal",
           [T("Pause", 14, "mut", "800", "center", 100, "Nunito", "Sg1"),
            T("+5 min", 14, "mut", "800", "center", 100, "Nunito", "Sg2"),
            R(104, 44, "mutbg", 22, "SgOn", "horizontal",
              [T("End", 14, "pri", "800", "center", name="Sg3")],
              align="center", justify="center")],
           padding=5, gap=4, align="center", stroke="line", sw=1),
         MICRO("SUB-STEPS", "C3"),
         OPTROW("circle-check", "oksoft", "ok", "Open file and music", "Done",
                False, "F1"),
         OPTROW("play", "ssoft", "sec", "Sketch hero section",
                "In progress - 10-min timer", True, "F2"),
         OPTROW("plus", "card", "mut", "Export PNG", "Up next", False, "F3"),
         ], "Focus")

    s3 = SCREEN("03 Reset", 940,
        HEAD("snowflake", "Feeling stuck?", "Freeze reset - two minutes counts.", "H3"),
        [R(358, 150, "card", 18, "MascBx", "horizontal",
           [IMG(MASCOT, 96, 96, 22, "Mascot"),
            R(220, 120, "card", 0, "MascTx", "vertical",
              [T("Pick the tiniest step.", 17, "ink", "600", "left", 220,
                 "Fredoka", "RsTi"),
               T("Puduu the pudu deer reminds you: slow is still moving.",
                 13, "mut", "400", "left", 220, "Nunito", "RsSb")], gap=4)],
           padding=14, gap=12, align="center", stroke="line", sw=1),
         OPTROW("glass-water", "ssoft", "sec", "Drink a glass of water",
                "2 min - raises energy", True, "R1"),
         OPTROW("footprints", "oksoft", "ok", "Clear one surface",
                "2 min - just the desk corner", False, "R2"),
         OPTROW("mail-open", "card", "pur", "Open the difficult email",
                "Just open it. Reply later.", False, "R3"),
         OPTROW("sparkles", "mutbg", "pri", "Sort my inbox",
                "Rule-based now - assisted later", False, "R4"),
         R(358, 78, "mutbg", 14, "RNote", "vertical",
           [T("Free: 2 resets per day - Pro: unlimited + custom menus.", 12,
              "mut", "400", "left", 326, "Nunito", "RN1"),
            T("Skipping is allowed - Puduu waits.", 12, "mut", "400", "left",
              326, "Nunito", "RN2")], padding=12, gap=4),
         ], "Reset")

    s4 = SCREEN("04 Ritual", 1410,
        HEAD("sparkles", "Close, breathe, begin", "Transition - fifteen seconds.", "H4"),
        [R(358, 70, "card", 16, "St1", "horizontal",
           [R(30, 30, "pri", 15, "St1N", "horizontal",
              [T("1", 14, "#FFFFFF", "800", "center", name="St1T")],
              align="center", justify="center"),
            R(286, 50, "card", 0, "St1Tx", "vertical",
              [T("Close", 15, "ink", "800", "left", 286, "Nunito", "St1H"),
               T("Portfolio file saved. Put it away.", 12, "mut", "400",
                 "left", 286, "Nunito", "St1S")], gap=2)],
           padding=12, gap=10, align="center", stroke="line", sw=1),
         R(358, 70, "card", 16, "St2", "horizontal",
           [R(30, 30, "sec", 15, "St2N", "horizontal",
              [T("2", 14, "#FFFFFF", "800", "center", name="St2T")],
              align="center", justify="center"),
            R(286, 50, "card", 0, "St2Tx", "vertical",
              [T("Breathe", 15, "ink", "800", "left", 286, "Nunito", "St2H"),
               T("One slow breath with the timer ring.", 12, "mut", "400",
                 "left", 286, "Nunito", "St2S")], gap=2)],
           padding=12, gap=10, align="center", stroke="line", sw=1),
         R(358, 70, "card", 16, "St3", "horizontal",
           [R(30, 30, "acc", 15, "St3N", "horizontal",
              [T("3", 14, "#FFFFFF", "800", "center", name="St3T")],
              align="center", justify="center"),
            R(286, 50, "card", 0, "St3Tx", "vertical",
              [T("Begin", 15, "ink", "800", "left", 286, "Nunito", "St3H"),
               T("Next up: Admin batch - 30 min.", 12, "mut", "400", "left",
                 286, "Nunito", "St3S")], gap=2)],
           padding=12, gap=10, align="center", stroke="line", sw=1),
         CTA("Begin Admin batch", "pri", "RiGo"),
         R(326, 50, "card", 25, "RiBack", "horizontal",
           [T("Not yet - back to Today", 14, "pri", "800", "center",
              name="RiBackLb")], align="center", justify="center",
           stroke="pri", sw=1),
         ], "Focus")

    s5 = SCREEN("05 Grows", 1880,
        HEAD("trophy", "Your week", "Good days: 5 of 7 - never resets to zero.", "H5"),
        [R(358, 92, "card", 16, "ConsBx", "vertical",
           [T("Consistency - 71 percent", 15, "ink", "800", "left", 326,
              "Nunito", "ConsT"),
            R(326, 14, "bg", 7, "ConsTr", "horizontal",
              [R(232, 14, "sec", 7, "ConsFl", "none", [])]),
            T("5 steady days - 2 slow days - both are fine.", 12, "mut",
              "400", "left", 326, "Nunito", "ConsS")],
           padding=12, gap=8, stroke="line", sw=1),
         OPTROW("trophy", "asoft", "acc", "Trophies",
                "Early starter x3 - Reset used x5 - 25-min focus x8", False,
                "G1"),
         MICRO("HOW WAS TODAY?", "C4"),
         R(358, 84, "card", 16, "MoodRow", "horizontal",
           [IMG(f"{A}/smile.png", 40, 40, 12, "Md1"),
            IMG(f"{A}/star.png", 40, 40, 12, "Md2"),
            IMG(f"{A}/heart.png", 40, 40, 12, "Md3")],
           padding=12, gap=12, align="center", justify="center",
           stroke="line", sw=1),
         R(358, 50, "mutbg", 14, "MoodCap", "horizontal",
           [T("Low - Flat - Okay (selected) - Good - Great", 12, "mut",
              "400", "center", name="MoodTx")],
           align="center", justify="center"),
         ], "Grows")

    s6 = SCREEN("06 Sort", 2350,
        HEAD("sparkles", "From dump to day", "Rule-based now - assisted later, same slot.", "H6"),
        [OPTROW("zap", "mutbg", "pri", "Call dentist",
                "Tiny first - 10 min - placed 09:00", True, "S1"),
         OPTROW("zap", "mutbg", "pri", "Pay electricity bill",
                "Tiny first - 15 min - placed 09:15", False, "S2"),
         OPTROW("calendar", "ssoft", "sec", "Deep work: portfolio hero",
                "Big block - 50 min - placed 10:00", False, "S3"),
         CTA("Apply to Today", "pri", "SoGo"),
         R(358, 60, "card", 14, "SoNt", "vertical",
           [T("Placement rules: urgent words first, tiny tasks first, low energy avoids big blocks.",
              12, "mut", "400", "left", 326, "Nunito", "SoNtT")],
           padding=12, gap=4, stroke="line", sw=1),
         ], "Today")

    s7 = SCREEN("07 Yours", 2820,
        HEAD("settings", "Settings", "Make Puduu yours.", "H7"),
        [R(358, 168, "card", 18, "ProBx", "vertical",
           [R(326, 60, "card", 0, "ProTx", "horizontal",
              [IMG(f"{A}/crown.png", 40, 40, 12, "ProIc"),
               R(270, 56, "card", 0, "ProTx2", "vertical",
                 [T("Puduu Pro - $6.99/mo", 17, "ink", "800", "left", 270,
                    "Nunito", "ProT"),
                  T("Unlimited resets - widgets - yearly $49.99.", 12, "mut",
                    "400", "left", 270, "Nunito", "ProS")], gap=2)],
              gap=10, align="center"),
            CTA("Try 7 days free", "acc", "ProGo")],
           padding=14, gap=10, stroke="pri", sw=2),
         OPTROW("bell", "asoft", "acc", "Gentle nudges",
                "Max 6 per day - quiet 22:00-07:00 on", False, "Y1"),
         OPTROW("volume-2", "ssoft", "sec", "Sounds and haptics",
                "Calm chime - soft vibration on", False, "Y2"),
         OPTROW("text", "card", "mut", "Text size",
                "Default - Large - XL spacing", False, "Y3"),
         OPTROW("log-out", "card", "mut", "Account",
                "you@puduu.app - Sign out", False, "Y4"),
         ], "Yours")

    screens = [s1, s2, s3, s4, s5, s6, s7]
    doc = {"version": "2.19", "name": "Puduu MVP v2",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": [GLYPH()] + screens + LABELS(screens)}
    json.dump(doc, open("puduu.pen", "w"), indent=1)
    print("wrote puduu.pen v2")

main()
