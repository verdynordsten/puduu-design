"""Puduu .pen generator — 7 screens + reusable components, schema 2.19.
Run: python3 gen_puduu_pen.py  ->  puduu.pen
Layout math: 390 wide, 16 side padding -> 358 content. Rows verified by validate-pen.py.
"""
import json, itertools

_uid = itertools.count(1)
_alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def nid():
    # base62 counter, padded to 5 chars -> unique for 900M+ nodes
    n = next(_uid)
    s = ""
    while n > 0:
        n, r = divmod(n, 62)
        s = _alphabet[r] + s
    return s.rjust(5, "0")

C = {
    "pri": "#2563EB", "sec": "#0891B2", "acc": "#EA580C",
    "bg": "#F8FAFC", "ink": "#0F172A", "mut": "#475569",
    "card": "#FFFFFF", "bd": "#E4ECFC", "mutbg": "#F1F5FD",
    "ok": "#16A34A", "pink": "#E11D48", "pur": "#9333EA",
}

def T(content, size=15, color="ink", weight="400", align="left", width=None, family="Nunito", name="Txt"):
    n = {"id": nid(), "type": "text", "name": name, "x": 0, "y": 0,
         "content": content, "fill": C.get(color, color),
         "fontSize": size, "fontFamily": family, "fontWeight": weight, "textAlign": align}
    if width is not None:
        n["width"] = width
        n["textGrowth"] = "fixed-width"
    return n

def IMG(url, w, h, radius=0, name="Img"):
    return {"id": nid(), "type": "rectangle", "name": name, "x": 0, "y": 0,
            "width": w, "height": h, "cornerRadius": radius,
            "fill": {"type": "image", "url": url, "mode": "fill"}}

def R(width=None, height=None, fill="card", radius=14, name="Box", layout=None, children=None,
      padding=None, gap=None, align=None, justify=None, stroke=None, sw=None):
    n = {"id": nid(), "type": "frame", "name": name, "x": 0, "y": 0}
    if width is not None: n["width"] = width
    if height is not None: n["height"] = height
    n["fill"] = C.get(fill, fill)
    n["cornerRadius"] = radius
    if layout: n["layout"] = layout
    if padding is not None: n["padding"] = padding
    if gap is not None: n["gap"] = gap
    if align: n["alignItems"] = align
    if justify: n["justify"] = justify
    if stroke: n["stroke"] = C.get(stroke, stroke)
    if sw: n["strokeWidth"] = sw
    n["children"] = children or []
    return n

def BTN(label, bg="pri", fg="#FFFFFF", icon=None, name="Btn"):
    kids = []
    if icon:
        kids.append(IMG(icon, 22, 22, name="BtnIc"))
    kids.append(T(label, 15, fg if fg.startswith("#") else fg, "700", "center", name="BtnLb"))
    return R(326, 54, bg, 27, name, "horizontal", kids, gap=8, align="center", justify="center")

def TLBAR(active):
    tabs = [("sun", "Today"), ("timer", "Focus"), ("snowflake", "Stuck"),
            ("trophy", "Grows"), ("settings", "Yours")]
    kids = []
    for ic, lb in tabs:
        on = lb == active
        kids.append(R(64, 56, "mutbg" if on else "card", 14, f"Tb{lb}", "vertical",
                       [IMG(f"./assets/icons/{ic}.png", 24, 24, name=f"Tb{lb}Ic"),
                        T(lb, 10, "pri" if on else "mut", "700", "center", name=f"Tb{lb}Lb")],
                       gap=2, align="center", justify="center"))
    return R(390, 84, "card", 0, "TabBar", "horizontal", kids, gap=4, align="center", justify="center")

def TLPILL(time, title, sub, hue, done=False, name="Tl"):
    return R(358, 78, hue, 18, name, "horizontal",
             [T(time, 13, "#FFFFFF", "700", "left", 52, name=f"{name}Tm"),
              R(240, 54, hue, 0, f"{name}Tx", "vertical",
                [T(title, 15, "#FFFFFF", "700", name=f"{name}Ti"),
                 T(sub, 13, "#FFFFFF", "400", name=f"{name}Sb")], gap=2)],
             padding=12, gap=10, align="center")

def RESCUECARD(icon, title, detail, hot=False, name="Rs"):
    return R(358, 76, "card", 16, name, "horizontal",
             [IMG(f"./assets/icons/{icon}.png", 40, 40, name=f"{name}Ic"),
              R(280, 56, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, "ink", "700", name=f"{name}Ti"),
                 T(detail, 13, "mut", "400", name=f"{name}Sb")], gap=2)],
             padding=12, gap=10, align="center",
             stroke="acc" if hot else None, sw=2 if hot else None)

def SETROW(icon, title, sub, name="Sr"):
    return R(358, 72, "card", 16, name, "horizontal",
             [IMG(f"./assets/icons/{icon}.png", 32, 32, name=f"{name}Ic"),
              R(288, 52, "card", 0, f"{name}Tx", "vertical",
                [T(title, 15, "ink", "700", name=f"{name}Ti"),
                 T(sub, 13, "mut", "400", name=f"{name}Sb")], gap=2)],
             padding=12, gap=10, align="center")

def SCREEN(name, x, header_kids, body_kids, tab):
    body = R(358, None, "bg", 0, f"{name}Bd", "vertical", body_kids, gap=10)
    col = [R(390, 64, "bg", 0, f"{name}Hd", "horizontal", header_kids,
             padding=[8, 16, 8, 16], gap=10, align="center"),
           body, TLBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x, "y": 0,
            "width": 390, "height": 844, "fill": C["bg"], "layout": "vertical",
            "alignItems": "center", "children": col}

def GLYPH():
    # reusable fluffy card shell used by ref demo (single instance below)
    return {"id": "cmpCard", "type": "frame", "name": "CmpFluffyCard",
            "x": 0, "y": 1200, "width": 358, "height": 76, "fill": C["card"],
            "cornerRadius": 16, "reusable": True, "layout": "horizontal",
            "padding": 12, "gap": 10, "alignItems": "center",
            "slot": ["cmpSlot"],
            "children": [{"id": "cmpSlot", "type": "text", "name": "Slot",
                          "x": 0, "y": 0, "content": "slot",
                          "fill": C["ink"], "fontSize": 15, "fontFamily": "Nunito",
                          "fontWeight": "700", "textAlign": "left",
                          "textGrowth": "fixed-width", "width": 300}]}

def main():
    H = lambda kids: kids  # header passthrough
    s1 = SCREEN("01 Today", 0,
        H([IMG("./assets/icons/sun.png", 32, 32, name="HdIc"),
           T("Puduu - Today", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [T("Good morning", 26, "ink", "600", "left", 358, "Fredoka", "Gr"),
         T("Thursday - 4 blocks planned - Small steps count.", 14, "mut", "400", "left", 358, "Sub"),
         TLPILL("08:00", "Morning reset", "Meds - water - 5-min tidy - 25m", C["pri"], name="Tl1"),
         TLPILL("09:00", "Deep work: portfolio", "50m - timer ready", C["sec"], name="Tl2"),
         TLPILL("11:00", "Walk outside", "15m - done", C["ok"], True, "Tl3"),
         TLPILL("13:00", "Admin batch", "Bills + inbox - 30m", C["acc"], name="Tl4"),
         T("INBOX - BRAIN DUMP", 12, "mut", "700", "left", 358, "Cap"),
         R(358, 118, "card", 16, "InboxBx", "vertical",
           [T("Dump it here... e.g. call dentist", 14, "mut", "400", "left", 326, "Ph"),
            R(326, 52, "pri", 26, "SortBtn", "horizontal",
              [T("Sort for me", 15, "#FFFFFF", "700", "center", name="SortLb")],
              align="center", justify="center")], padding=12, gap=10),
         {"id": nid(), "type": "ref", "name": "RescueCta", "x": 0, "y": 0,
          "ref": "cmpCard", "descendants": {"cmpSlot": {"content": "Frozen? - I'm Stuck, rescue me"}}},
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        H([IMG("./assets/icons/timer.png", 32, 32, name="HdIc"),
           T("Focus", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [T("Deep work: portfolio", 22, "ink", "600", "left", 358, "Fredoka", "FTi"),
         T("Step 2 of 4 - Sketch hero section", 14, "mut", "400", "left", 358, "FSub"),
         R(358, 190, "card", 18, "DialBx", "vertical",
           [IMG("./assets/icons/timer.png", 56, 56, name="DialIc"),
            T("32:10 left", 30, "ink", "600", "center", 300, "Fredoka", "DialTm"),
            T("gentle chime at end", 13, "mut", "400", "center", 300, "DialSb")],
           padding=14, gap=6, align="center"),
         R(358, 56, "mutbg", 28, "FRow", "horizontal",
           [T("Pause", 14, "sec", "700", "center", 100, "FR1"),
            T("+5 min", 14, "sec", "700", "center", 100, "FR2"),
            T("Done", 14, "sec", "700", "center", 100, "FR3")],
           align="center", justify="center"),
         T("SUB-STEPS", 12, "mut", "700", "left", 358, "Cap"),
         SETROW("circle-check", "Open file & music", "done", "Fs1"),
         SETROW("play", "Sketch hero section", "now - 10m timer", "Fs2"),
         SETROW("plus", "Export PNG", "up next", "Fs3"),
         ], "Focus")

    s3 = SCREEN("03 Rescue", 940,
        H([IMG("./assets/icons/snowflake.png", 32, 32, name="HdIc"),
           T("I'm Stuck", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [IMG("./assets/puduu-mascot.png", 120, 120, 30, "Mascot"),
         T("Frozen? Let's thaw.", 24, "ink", "600", "center", 358, "Fredoka", "RTi"),
         T("Pick the tiniest one. 2 minutes counts.", 14, "mut", "400", "center", 358, "RSub"),
         RESCUECARD("glass-water", "Drink a glass of water", "2 min - energy +1", True, "Rs1"),
         RESCUECARD("footprints", "Clear one surface", "2 min - just the desk corner", False, "Rs2"),
         RESCUECARD("mail-open", "Open the scary email", "just open it. Reply later.", False, "Rs3"),
         R(358, 96, "mutbg", 14, "RNote", "vertical",
           [T("Free: 2 rescues/day - Pro: unlimited + custom menus.", 13, "mut", "400", "left", 326, "RNt"),
            T("Skipping is allowed - Puduu waits.", 13, "mut", "400", "left", 326, "RN2")],
           padding=12, gap=4),
         ], "Stuck")

    s4 = SCREEN("04 Ritual", 1410,
        H([IMG("./assets/icons/sparkles.png", 32, 32, name="HdIc"),
           T("Switch Ritual", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [T("Close - Breathe - Begin", 24, "ink", "600", "center", 358, "Fredoka", "RiTi"),
         T("15 seconds. Then we start.", 14, "mut", "400", "center", 358, "RiSub"),
         R(358, 64, "card", 16, "Ri1", "horizontal",
           [IMG("./assets/icons/check.png", 32, 32, name="Ri1Ic"),
            T("1 - Close: portfolio file saved?", 15, "ink", "700", "left", 280, "Ri1Tx")],
           padding=12, gap=10, align="center"),
         R(358, 64, "card", 16, "Ri2", "horizontal",
           [IMG("./assets/icons/smile.png", 32, 32, name="Ri2Ic"),
            T("2 - Breathe: one slow breath...", 15, "ink", "700", "left", 280, "Ri2Tx")],
           padding=12, gap=10, align="center"),
         R(358, 64, "card", 16, "Ri3", "horizontal",
           [IMG("./assets/icons/zap.png", 32, 32, name="Ri3Ic"),
            T("3 - Begin: Admin batch - 30m", 15, "ink", "700", "left", 280, "Ri3Tx")],
           padding=12, gap=10, align="center"),
         BTN("Begin admin batch", "pri", "#FFFFFF", "./assets/icons/play.png", "RiGo"),
         ], "Focus")

    s5 = SCREEN("05 Grows", 1880,
        H([IMG("./assets/icons/trophy.png", 32, 32, name="HdIc"),
           T("Your week", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [T("Good days: 5/7", 24, "ink", "600", "left", 358, "Fredoka", "GTi"),
         T("never resets to zero - slow days are fine too", 14, "mut", "400", "left", 358, "GSub"),
         R(358, 84, "card", 16, "ConsBx", "vertical",
           [T("Consistency 71%", 15, "ink", "700", "left", 326, "ConsT"),
            R(326, 14, "bd", 7, "ConsTr", "none", [], name2 := None) if False else
            R(326, 14, "bd", 7, "ConsTr", "horizontal",
              [R(232, 14, "sec", 7, "ConsFl", "none", [])])], padding=12, gap=8),
         R(358, 76, "card", 16, "TroBx", "horizontal",
           [IMG("./assets/icons/trophy.png", 40, 40, name="TroIc"),
            T("Early starter x3 - Thawed x5 - Focus 25m x8", 14, "ink", "700", "left", 270, "TroTx")],
           padding=12, gap=10, align="center"),
         T("HOW WAS TODAY?", 12, "mut", "700", "left", 358, "Cap"),
         R(358, 64, "card", 16, "MoodRow", "horizontal",
           [IMG("./assets/icons/smile.png", 36, 36, name="Md1"),
            IMG("./assets/icons/star.png", 36, 36, name="Md2"),
            IMG("./assets/icons/heart.png", 36, 36, name="Md3")],
           align="center", justify="center"),
         ], "Grows")

    s6 = SCREEN("06 InboxSort", 2350,
        H([IMG("./assets/icons/sparkles.png", 32, 32, name="HdIc"),
           T("Sort for me", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [T("From dump to day", 24, "ink", "600", "left", 358, "Fredoka", "STi"),
         T("rule-based now - magic AI later, same slot", 14, "mut", "400", "left", 358, "SSub"),
         SETROW("zap", "Call dentist", "tiny first - 10m - 09:00", "So1"),
         SETROW("zap", "Pay electricity bill", "tiny first - 15m - 09:15", "So2"),
         SETROW("calendar", "Deep work: portfolio hero", "big block - 50m - 10:00", "So3"),
         BTN("Apply to Today", "pri", "#FFFFFF", "./assets/icons/check.png", "SoGo"),
         ], "Today")

    s7 = SCREEN("07 Yours", 2820,
        H([IMG("./assets/icons/settings.png", 32, 32, name="HdIc"),
           T("Settings", 20, "ink", "600", "left", 280, "Fredoka", "HdTi")]),
        [R(358, 120, "card", 18, "ProBx", "vertical",
           [T("Puduu Pro - $6.99/mo", 17, "ink", "700", "left", 326, "ProT"),
            T("Unlimited rescue - magic AI (soon) - widgets - yearly $49.99", 13, "mut", "400", "left", 326, "ProS"),
            R(326, 48, "acc", 24, "ProBtn", "horizontal",
              [T("Try 7 days free", 15, "#FFFFFF", "700", "center", name="ProLb")],
              align="center", justify="center")], padding=14, gap=8),
         SETROW("bell", "Gentle nudges", "Max 6/day - quiet 22:00-07:00 ON", "Sr1"),
         SETROW("volume-2", "Sounds & haptics", "Calm chime - soft vibration ON", "Sr2"),
         SETROW("text", "Text size", "Default - Large - XL spacing", "Sr3"),
         SETROW("log-out", "Account", "you@puduu.app - Sign out", "Sr4"),
         ], "Yours")

    labels = []
    for s, lb in [(s1, "01 Today"), (s2, "02 Focus"), (s3, "03 Rescue"),
                  (s4, "04 Ritual"), (s5, "05 Grows"), (s6, "06 InboxSort"), (s7, "07 Yours")]:
        labels.append({"id": nid(), "type": "text", "name": lb, "x": s["x"], "y": -50,
                       "content": lb, "fill": C["mut"], "fontSize": 14,
                       "fontFamily": "Nunito", "fontWeight": "700", "textAlign": "left"})

    doc = {"version": "2.19", "name": "Puduu MVP",
           "variables": {k: {"type": "color", "value": v} for k, v in C.items()},
           "children": [GLYPH(), s1, s2, s3, s4, s5, s6, s7] + labels}
    json.dump(doc, open("puduu.pen", "w"), indent=1)
    print("wrote puduu.pen")

main()
