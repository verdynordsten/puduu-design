"""Puduu .pen generator v5 — LEDGER total rebuild.
New language: warm paper, ink serif (Fraunces display), Inter UI,
ONE ember accent, ruled ledger lines, margin italic serif notes,
numbered ledger tabs. Zero pastel, zero toy pills, zero generic blue.
Schema 2.19. Run: python3 gen_puduu_pen.py -> puduu.pen
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
    "paper": "#F6F3EC", "deep": "#EFE8D8", "card": "#FFFDF8",
    "ink": "#1C1917", "soft": "#44403C", "mute": "#78716C",
    "faint": "#6F655C", "line": "#E3DAC7",
    "ember": "#9A3412", "emberDeep": "#7C2D12", "wash": "#F7E8D2",
    "moss": "#5B6B1F",
}
DISP = "Fraunces"
UI = "Inter"

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

def R(width=None, height=None, fill="card", radius=8, name="Box",
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

def CT(content, size, color, weight, family, width, name):
    return T(content, size, color, weight, "center", width, family, name)

# ---------- ledger primitives ----------

def HEAD(eyebrow, headline, stand, name="Hd"):
    return R(350, None, "paper", 0, f"{name}Wrap", "vertical",
             [T(eyebrow.upper(), 10.5, "mute", "700", "left", 350, UI,
                f"{name}Ey"),
              T(headline, 27, "ink", "600", "left", 350, DISP,
                f"{name}Ti"),
              T(stand, 12.5, "mute", "400", "left", 350, UI,
                f"{name}Sb"),
              R(350, 1, "line", 0, f"{name}Rule", "none", [])],
             gap=6)

def SEC(label, action="", name="Sec"):
    kids = [T(label.upper(), 10.5, "mute", "700", "left", 200, UI,
               f"{name}Lb")]
    if action:
        kids.append(T(action, 12.5, "emberDeep", "600", "right", 140, UI,
                      f"{name}Ac"))
    return R(350, 26, "paper", 0, name, "horizontal", kids,
             justify="space_between", align="center")

def NOW(meta, title, pct, name="Now"):
    return R(350, None, "card", 8, name, "vertical",
             [R(318, 20, "card", 0, f"{name}Top", "horizontal",
                [T("NOW", 10.5, "emberDeep", "700", "left", 36, UI,
                   f"{name}K"),
                 T(meta, 12, "mute", "400", "left", 276, UI,
                   f"{name}Mt")],
                gap=8, align="center"),
              T(title, 20, "ink", "600", "left", 318, DISP,
                f"{name}Ti"),
              R(318, 4, "deep", 2, f"{name}Tr", "horizontal",
                [R(pct, 4, "ember", 2, f"{name}Fl", "none", [])]),
              R(318, 48, "wash", 8, f"{name}Go", "horizontal",
                [T("Begin session", 14, "ink", "700", "center",
                   name=f"{name}GoLb")],
                align="center", justify="center",
                stroke="emberDeep", sw=1.2)],
             padding=16, gap=9, stroke="line", sw=1)

def LINE(hour, span, title, note, state="open", name="Ln"):
    """Ledger line: time gutter + spine dot + text + side status.
    state: open | current | done"""
    if state == "done":
        dot = R(9, 9, "moss", 5, f"{name}Dot", "none", [])
        tcol, side = "faint", T("Done", 12, "moss", "600", "right",
                                64, UI, f"{name}Sd")
    elif state == "current":
        dot = R(9, 9, "ember", 5, f"{name}Dot", "none", [])
        tcol, side = "ink", T("Begin", 12.5, "emberDeep", "600",
                              "right", 64, UI, f"{name}Sd")
    else:
        dot = R(9, 9, "card", 5, f"{name}Dot", "none", [],
                stroke="faint", sw=2)
        tcol, side = "ink", T(span, 12, "faint", "400", "right",
                              64, UI, f"{name}Sd")
    spine = R(10, 46, "paper", 0, f"{name}Sp", "vertical",
              [dot, R(2.5, 34, "deep", 1, f"{name}St", "none", [])],
              gap=2, align="center")
    gut = R(48, 44, "paper", 0, f"{name}Gut", "vertical",
            [T(hour, 13.5, tcol, "700", "right", 48, UI, f"{name}Hr"),
             T(span, 10.5, "faint", "400", "right", 48, UI,
               f"{name}Sp2")], gap=1)
    tx = R(200, None, "paper", 0, f"{name}Tx", "vertical",
           [T(title, 14.5, tcol, "600", "left", 200, UI, f"{name}Ti"),
            T(note, 12, "faint", "400", "left", 200, UI,
              f"{name}Nt")], gap=2)
    return R(350, None, "paper", 0, name, "horizontal",
             [gut, spine, tx, side], gap=10, align="center")

def RULE(icon, title, detail, trail="", name="Rr"):
    tx = R(250, None, "paper", 0, f"{name}Tx", "vertical",
           [T(title, 14.5, "ink", "600", "left", 250, UI,
              f"{name}Ti"),
            T(detail, 12, "mute", "400", "left", 250, UI,
              f"{name}Sb")], gap=2)
    side = (T(trail, 12, "faint", "400", "right", 40, UI,
              f"{name}Tr") if trail else
            T("›", 16, "faint", "400", "right", 24, UI, f"{name}Ch"))
    return R(350, None, "paper", 0, name, "horizontal",
             [T(icon, 18, "soft", "400", "left", 26, UI,
                f"{name}Ic"),
              tx, side], gap=10, align="center")

def NOTE(text, name="Nt"):
    return T(text, 12.5, "mute", "400", "left", 250, DISP, name)

def TABBAR(active):
    tabs = [("01", "Today"), ("02", "Focus"), ("03", "Reset"),
            ("04", "Progress"), ("05", "Yours")]
    kids = []
    for num, lb in tabs:
        on = lb == active
        kids.append(R(64, 58, "paper", 0, f"Tb{lb}", "vertical",
                       [T(num, 10, "emberDeep" if on else "faint",
                          "700", "center", 64, UI, f"Tb{lb}Nm"),
                        T(lb, 11, "ink" if on else "faint",
                          "700" if on else "500", "center", 64, UI,
                          f"Tb{lb}Lb")],
                       gap=3, align="center", justify="center"))
    return R(390, 76, "paper", 0, "TabBar", "horizontal", kids,
             gap=2, align="center", justify="center",
             stroke="line", sw=1)

def SCREEN(name, x, head, body, tab):
    col = [head,
           R(350, None, "paper", 0, f"{name}Bd", "vertical",
             body, gap=0, padding=[0, 0, 0, 0]),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x,
            "y": 0, "width": 390, "height": 844, "fill": C["paper"],
            "layout": "vertical", "alignItems": "center",
            "children": col}

def GLYPH():
    return {"id": "cmpLine", "type": "frame", "name": "CmpDayLine",
            "x": 0, "y": 1200, "width": 350, "height": 64,
            "fill": C["paper"], "cornerRadius": 0, "reusable": True,
            "layout": "horizontal", "padding": 0, "gap": 10,
            "alignItems": "center",
            "slot": ["cmpSlot"],
            "children": [
                {"id": "cmpDot", "type": "frame", "name": "CmpDot",
                 "x": 0, "y": 0, "width": 9, "height": 9,
                 "fill": C["ember"], "cornerRadius": 5},
                {"id": "cmpSlot", "type": "text", "name": "Slot",
                 "x": 0, "y": 0, "content": "slot",
                 "fill": C["ink"], "fontSize": 14,
                 "fontFamily": UI, "fontWeight": "600",
                 "textAlign": "left", "textGrowth": "fixed-width",
                 "width": 290}]}

def LABELS(screens):
    return [{"id": nid(), "type": "text", "name": s["name"],
             "x": s["x"], "y": -50, "content": s["name"],
             "fill": C["mute"], "fontSize": 14,
             "fontFamily": UI, "fontWeight": "700",
             "textAlign": "left"}
            for s in screens]

def main():
    s1 = SCREEN("01 Today", 0,
        HEAD("Thursday · September 25", "Good morning, Alex.",
             "Four blocks planned. One thing at a time.", "H1"),
        [NOW("09:00 · 50 min · step 2 of 4",
             "Deep work: portfolio", 195, "Now1"),
         SEC("The day", "See all", "S1"),
         LINE("08:00", "25m", "Morning reset",
              "Meds, water, five-minute tidy", "open", "L1"),
         LINE("09:00", "50m", "Deep work: portfolio",
              "Hero section, timer on, phone away", "current", "L2"),
         LINE("11:00", "15m", "Walk outside",
              "Fifteen minutes, no podcast", "done", "L3"),
         LINE("13:00", "30m", "Admin batch",
              "Bills and inbox, one pass", "open", "L4"),
         SEC("Inbox", "3 waiting", "S2"),
         R(350, None, "card", 8, "InboxBx", "vertical",
           [T("Capture a task, idea, or reminder…", 13.5, "faint",
              "400", "left", 318, UI, "InPh"),
            R(318, 46, "ink", 8, "AddBtn", "horizontal",
              [T("Add to inbox", 13.5, "#FFFDF8", "600", "center",
                 name="AddLb")],
              align="center", justify="center"),
            R(318, 44, "card", 8, "SortBtn", "horizontal",
              [T("Sort into my day", 13, "emberDeep", "700",
                 "center", name="SortLb")],
              align="center", justify="center",
              stroke="emberDeep", sw=1.2)],
           padding=14, gap=10, stroke="line", sw=1),
         SEC("If you stall", "", "S3"),
         RULE("~", "Take a two-minute reset",
              "Water, air, one small surface.", "2 min", "R0"),
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        HEAD("Focus session", "Stay with it.",
             "Deep work: portfolio · step 2 of 4.", "H2"),
        [CT("32:10", 72, "ink", "600", DISP, 350, "DialTm"),
         CT("MINUTES LEFT · GENTLE CHIME AT THE END", 10.5,
            "mute", "700", UI, 350, "DialK"),
         R(350, 4, "deep", 2, "DialTr", "horizontal",
           [R(126, 4, "ember", 2, "DialFl", "none", [])]),
         CT("Sketch the hero section. Phone in another room.", 12.5,
            "mute", "400", UI, 350, "DialSb"),
         R(350, 52, "ink", 8, "PauseBtn", "horizontal",
           [T("Pause", 14, "#FFFDF8", "600", "center",
              name="PauseLb")],
           align="center", justify="center"),
         R(350, 48, "card", 8, "EndBtn", "horizontal",
           [T("End early", 13.5, "ink", "600", "center",
              name="EndLb")],
           align="center", justify="center", stroke="line", sw=1),
         ], "Focus")

    s3 = SCREEN("03 Reset", 940,
        HEAD("Freeze reset", "Hit a wall?",
             "Two minutes counts. Pick the smallest one.", "H3"),
        [RULE("~", "Drink a glass of water",
              "Stand up, sip slowly, look far away.", "2 min", "R1"),
         RULE("~", "Clear one surface",
              "Just the desk corner. Nothing more.", "2 min", "R2"),
         RULE("~", "Open the difficult email",
              "Read it only. Reply comes later.", "2 min", "R3"),
         RULE("~", "Sort the inbox",
              "Rule-based now, assisted later.", "3 min", "R4"),
         SEC("A note", "", "S4"),
         NOTE("Slow is still moving. Skipping is allowed — "
              "Puduu waits.", "Nt1"),
         ], "Reset")

    s4 = SCREEN("04 Progress", 1410,
        HEAD("Progress", "Keep growing.",
             "Good days: 5 of 7. Never resets to zero.", "H4"),
        [RULE("#", "Weekly shelf",
              "Early starter ×3 · Reset used ×5 · Focus 25m ×8.",
              "W39", "G1"),
         RULE("#", "Focus trend",
              "Up 20% vs last week. Mornings work best.",
              "+20%", "G2"),
         RULE("#", "Resets that worked",
              "Water first, then air. Evenings stay hard.",
              "×5", "G3"),
         SEC("A note", "", "S5"),
         NOTE("Done is a direction, not a streak.", "Nt2"),
         ], "Progress")

    s5 = SCREEN("05 Yours", 1880,
        HEAD("Settings", "Make it yours.",
             "Plan, sounds, reminders, and backup.", "H5"),
        [RULE("*", "Puduu Pro · $6.99/mo",
              "Unlimited resets · yearly $49.99.", "", "Y1"),
         RULE("*", "Gentle nudges",
              "Max 6 per day · quiet 22:00–07:00.", "On", "Y2"),
         RULE("*", "Sounds and haptics",
              "Calm chime · soft vibration.", "On", "Y3"),
         ], "Yours")

    screens = [s1, s2, s3, s4, s5]
    doc = {"version": "2.19", "name": "Puduu v5 Ledger",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": [GLYPH()] + screens + LABELS(screens)}
    with open("puduu.pen", "w") as f:
        json.dump(doc, f)
    print("wrote puduu.pen:",
          sum(1 for _ in json.dumps(doc).split('"id"')) - 1, "nodes")

if __name__ == "__main__":
    main()
