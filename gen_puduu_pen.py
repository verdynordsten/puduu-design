"""Puduu .pen generator v7 — mirrors the Flutter render 1:1.

Source of truth: /opt/data/puduu/puduu-app/lib/main.dart + puduu_theme.dart.
- NOW button = wash bg + ink text + ink play icon + Skip text beside it
- DayLine rows: 56px time gutter (14/11), dot 9 + stem 34, Inter 15 titles
  (done = faint + strike), side: "N min" / Begin TextButton / check+Done
- RuleRow: bare 20px soft icons (NO tiles), Inter 15/12.5, dividers
- Inbox card: TextField + ember Add (white plus) + Sort outline w/ ember icon
- Focus: FRAUNCES 76 timer, Pause ink w/ WHITE icon + End early side-by-side
- Nav: MONOCHROME outlined/filled pairs, no numbers, badge 3 on Today
- Note rows: A NOTE sec + italic Fraunces note (Reset/Progress had it)
- stalk copy: "Freeze reset" eyebrow on Reset (matches app)
Schema 2.19. validator must print errors=0. emoji scan must print 0.
Run: python3 gen_puduu_pen.py -> puduu.pen
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
    "paper": "#F6F3EC", "deep": "#EFE8D8", "card": "#FFFDF8",
    "ink": "#1C1917", "soft": "#44403C", "mute": "#78716C",
    "faint": "#6F655C", "line": "#E3DAC7",
    "ember": "#9A3412", "emberDeep": "#7C2D12", "wash": "#F7E8D2",
    "moss": "#5B6B1F", "white": "#FFFFFF",
}
DISP = "Fraunces"
UI = "Inter"
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

def IMG(url, w, h, radius=8, name="Img"):
    return {"id": nid(), "type": "rectangle", "name": name, "x": 0, "y": 0,
            "width": w, "height": h, "cornerRadius": radius,
            "fill": {"type": "image", "url": url, "mode": "fill"}}

def CT(content, size, color, weight, family, width, name):
    return T(content, size, color, weight, "center", width, family, name)

def DIV(name):
    return R(350, 1, "line", 0, name, "none", [])

# ---------- app-faithful primitives ----------

def HEAD(eyebrow, headline, stand, name="Hd"):
    # LedgerHead: eyebrow 11/700/1.6ls, headline Fraunces 30, stand 13.5 meta
    return R(350, None, "paper", 0, f"{name}Wrap", "vertical",
             [T(eyebrow.upper(), 11, "mute", "700", "left", 350, UI,
                f"{name}Ey"),
              T(headline, 30, "ink", "600", "left", 350, DISP,
                f"{name}Ti"),
              T(stand, 13.5, "mute", "400", "left", 350, UI,
                f"{name}Sb"),
              R(350, 1, "line", 0, f"{name}Rule", "none", [])],
             gap=7)

def SEC(label, action="", name="Sec"):
    kids = [T(label.upper(), 11, "mute", "700", "left", 200, UI,
               f"{name}Lb")]
    if action:
        kids.append(T(action, 13.5, "emberDeep", "600", "right", 140, UI,
                      f"{name}Ac"))
    return R(350, 26, "paper", 0, name, "horizontal", kids,
             justify="space_between", align="center")

def NOW(meta, title, pct, name="Now"):
    # NowPanel: wash OutlinedButton (ink text + ink play icon) + Skip text
    return R(350, None, "card", 8, name, "vertical",
             [R(314, 20, "card", 0, f"{name}Top", "horizontal",
                [T("NOW", 11, "emberDeep", "700", "left", 34, UI,
                   f"{name}K"),
                 T(meta, 12.5, "mute", "400", "left", 266, UI,
                   f"{name}Mt")],
                gap=8, align="center"),
              T(title, 21, "ink", "600", "left", 314, DISP,
                f"{name}Ti"),
              R(314, 4, "deep", 2, f"{name}Tr", "horizontal",
                [R(pct, 4, "ember", 2, f"{name}Fl", "none", [])]),
              R(314, None, "card", 0, f"{name}BtnRow", "horizontal",
                [R(236, 50, "wash", 8, f"{name}Go", "horizontal",
                   [IMG(f"{A}/play-ink.png", 18, 18, 9,
                        f"{name}GoIc"),
                    T("Begin session", 14, "ink", "700", "left",
                      126, UI, f"{name}GoLb")],
                   gap=8, align="center", justify="center",
                   stroke="emberDeep", sw=1.2),
                 T("Skip", 13.5, "emberDeep", "600", "center",
                   58, UI, f"{name}Skip")],
                gap=6, align="center")],
             padding=16, gap=11, stroke="line", sw=1)

def LINE(hour, span, title, note, state="open", name="Ln"):
    """DayLine mirror: 56 gutter, 9px dot + 34 stem, side per state."""
    if state == "done":
        dot = R(9, 9, "moss", 5, f"{name}Dot", "none", [])
        tcol = "faint"
        side = R(64, 20, "paper", 0, f"{name}SdW", "horizontal",
                 [IMG(f"{A}/check-moss.png", 15, 15, 4, f"{name}Ck"),
                  T("Done", 12.5, "moss", "600", "left", 42, UI,
                    f"{name}Sd")],
                 gap=4, align="center")
    elif state == "current":
        dot = R(9, 9, "ember", 5, f"{name}Dot", "none", [])
        tcol = "ink"
        side = T("Begin", 13.5, "emberDeep", "600", "right",
                 64, UI, f"{name}Sd")
    else:
        dot = R(9, 9, "card", 5, f"{name}Dot", "none", [],
                stroke="faint", sw=1.6)
        tcol = "ink"
        side = T(span.replace("m", "") + " min" if "m" in span else span,
                 12, "faint", "400", "right", 64, UI, f"{name}Sd")
    spine = R(10, 46, "paper", 0, f"{name}Sp", "vertical",
              [dot, R(2.5, 34, "deep", 1, f"{name}St", "none", [])],
              gap=2, align="center")
    gut = R(56, 44, "paper", 0, f"{name}Gut", "vertical",
            [T(hour, 14, tcol, "700", "right", 56, UI, f"{name}Hr"),
             T(span, 11, "faint", "400", "right", 56, UI,
               f"{name}Sp2")], gap=2)
    tx = R(188, None, "paper", 0, f"{name}Tx", "vertical",
           [T(title, 15, tcol,
              "600", "left", 188, UI, f"{name}Ti"),
            T(note, 12.5, "faint", "400", "left", 188, UI,
              f"{name}Nt")], gap=2)
    return R(350, None, "paper", 0, name, "horizontal",
             [gut, spine, tx, side], gap=8, align="center")

def RULE(icon, title, detail, trail=None, name="Rr", chev=False):
    """RuleRow mirror: bare 20px soft icon, Inter 15/12.5, faint trail.
    Done historically renders strike by pen.dev? No — keep plain, note state
    via color only (PIL preview can't strike; app uses lineThrough for done
    DayLine titles, RuleRows never strike)."""
    tx = R(236, None, "paper", 0, f"{name}Tx", "vertical",
           [T(title, 15, "ink", "600", "left", 236, UI,
              f"{name}Ti"),
            T(detail, 12.5, "mute", "400", "left", 236, UI,
              f"{name}Sb")], gap=2)
    if chev:
        side = IMG(f"{A}/chevron-right-faint.png", 20, 20, 5,
                   f"{name}Ch")
    elif trail is not None:
        side = T(trail, 12, "faint", "400", "right", 56, UI,
                 f"{name}Tr")
    else:
        side = T("", 12, "faint", "400", "right", 20, UI,
                 f"{name}Tr")
    return R(350, None, "paper", 0, name, "horizontal",
             [IMG(f"{A}/{icon}.png", 20, 20, 4, f"{name}Ic"),
              tx, side], gap=12, align="center")

def ANOTE(text, name="Nt"):
    # italic Fraunces 13.5 mute (margin-note voice)
    n = T(text, 13.5, "mute", "400", "left", 350, DISP, name)
    return n

def TABBAR(active):
    # M3 NavigationBar mirror: monochrome outlined/filled, no numbers,
    # ember badge dot with "3" on Today (inboxProvider has 3 items).
    tabs = [("Today", "calendar-days"), ("Focus", "timer"),
            ("Reset", "refresh-ccw"), ("Progress", "bar-chart-3"),
            ("Yours", "settings")]
    kids = []
    for lb, ic in tabs:
        on = lb == active
        iconf = f"{A}/{ic}-{'ink' if on else 'faint'}.png"
        cell = [IMG(iconf, 23, 23, 5, f"Tb{lb}Ic"),
                T(lb, 11, "ink" if on else "faint",
                  "700" if on else "500", "center", 62, UI,
                  f"Tb{lb}Lb")]
        if lb == "Today":
            cell = [R(46, 30, "paper", 0, "TbBadgeRow", "horizontal",
                      [IMG(iconf, 23, 23, 5, "TbTodayIc"),
                       R(18, 18, "ember", 9, "TbBadge", "none",
                         [T("3", 10, "white", "700", "center", 18, UI,
                            "TbBadgeN")])],
                      gap=2, align="center", justify="center"),
                    T(lb, 11, "ink" if on else "faint",
                      "700" if on else "500", "center", 62, UI,
                      f"Tb{lb}Lb")]
        kids.append(R(68, 60, "paper", 0, f"Tb{lb}", "vertical",
                      cell, gap=3, align="center", justify="center"))
    return R(358, 76, "paper", 0, "TabBar", "horizontal", kids,
             gap=2, align="center", justify="center",
             stroke="line", sw=1)

def SCREEN(name, x, head, body, tab):
    col = [head,
           R(358, None, "paper", 0, f"{name}Bd", "vertical",
             body, gap=0, padding=[0, 4, 0, 4]),
           TABBAR(tab)]
    return {"id": nid(), "type": "frame", "name": name, "x": x,
            "y": 0, "width": 390,
            "height": {"01 Today": 1250, "02 Focus": 980,
                       "03 Reset": 844, "04 Progress": 844,
                       "05 Yours": 844}.get(name, 844),
            "fill": C["paper"],
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
             "Deep work: portfolio", 192, "Now1"),
         SEC("The day", "See all", "S1"),
         LINE("08:00", "25m", "Morning reset",
              "Meds, water, five-minute tidy", "open", "L1"),
         DIV("D1"),
         LINE("09:00", "50m", "Deep work: portfolio",
              "Hero section, timer on, phone away", "current", "L2"),
         DIV("D2"),
         LINE("11:00", "15m", "Walk outside",
              "Fifteen minutes, no podcast", "done", "L3"),
         DIV("D3"),
         LINE("13:00", "30m", "Admin batch",
              "Bills and inbox, one pass", "open", "L4"),
         SEC("Inbox", "3 waiting", "S2"),
         R(350, None, "card", 8, "InboxBx", "vertical",
           [R(318, 48, "card", 10, "InField", "horizontal",
              [T("Capture a task, idea, or reminder…", 14, "faint",
                 "400", "left", 210, UI, "InPh"),
               R(86, 40, "ember", 8, "AddBtn", "horizontal",
                 [IMG(f"{A}/plus-white.png", 17, 17, 4, "AddIc"),
                  T("Add", 13.5, "white", "700", "left", 40, UI,
                    "AddLb")],
                 gap=5, align="center", justify="center")],
              gap=8, align="center", stroke="line", sw=1),
            R(318, 46, "card", 8, "SortBtn", "horizontal",
              [IMG(f"{A}/sparkles-ember.png", 17, 17, 4, "SortIc"),
               T("Sort into my day", 13.5, "emberDeep", "700",
                 "center", 200, UI, name="SortLb")],
              gap=8, align="center", justify="center",
              stroke="emberDeep", sw=1.2)],
           padding=14, gap=10, stroke="line", sw=1),
         SEC("If you stall", "", "S3"),
         RULE("refresh-ccw-soft", "Take a two-minute reset",
              "Water, air, one small surface.", "2 min", "R0"),
         ], "Today")

    s2 = SCREEN("02 Focus", 470,
        HEAD("Focus session", "Stay with it.",
             "Deep work: portfolio · step 2 of 4.", "H2"),
        [CT("32:10", 76, "ink", "600", DISP, 350, "DialTm"),
         CT("MINUTES LEFT · GENTLE CHIME AT THE END", 11,
            "mute", "700", UI, 350, "DialK"),
         R(350, 4, "deep", 2, "DialTr", "horizontal",
           [R(126, 4, "ember", 2, "DialFl", "none", [])]),
         CT("Sketch the hero section. Phone in another room.", 12.5,
            "mute", "400", UI, 350, "DialSb"),
         R(350, None, "paper", 0, "FocusBtns", "horizontal",
           [R(150, 52, "ink", 8, "PauseBtn", "horizontal",
              [IMG(f"{A}/pause-white.png", 18, 18, 9, "PauseIc"),
               T("Pause", 14, "white", "600", "left", 70, UI,
                 name="PauseLb")],
              gap=8, align="center", justify="center"),
            R(150, 52, "card", 10, "EndBtn", "horizontal",
              [T("End early", 14, "ink", "600", "center",
                 130, UI, name="EndLb")],
              align="center", justify="center",
              stroke="line", sw=1)],
           gap=10, align="center", justify="center"),
         ], "Focus")

    s3 = SCREEN("03 Reset", 940,
        HEAD("Freeze reset", "Hit a wall?",
             "Two minutes counts. Pick the smallest one.", "H3"),
        [RULE("droplet-soft", "Drink a glass of water",
              "Stand up, sip slowly, look far away.", "2 min", "R1"),
         DIV("D4"),
         RULE("footprints-soft", "Clear one surface",
              "Just the desk corner. Nothing more.", "2 min", "R2"),
         DIV("D5"),
         RULE("mail-open-soft", "Open the difficult email",
              "Read it only. Reply comes later.", "2 min", "R3"),
         DIV("D6"),
         RULE("list-checks-soft", "Sort the inbox",
              "Rule-based now, assisted later.", "3 min", "R4"),
         SEC("A note", "", "S4"),
         ANOTE("Slow is still moving. Skipping is allowed — "
               "Puduu waits.", "Nt1"),
         ], "Reset")

    s4 = SCREEN("04 Progress", 1410,
        HEAD("Progress", "Keep growing.",
             "Good days: 5 of 7. Never resets to zero.", "H4"),
        [RULE("bar-chart-3-soft", "Weekly shelf",
              "Early starter ×3 · Reset used ×5 · Focus 25m ×8.",
              "W39", "G1"),
         DIV("D7"),
         RULE("timer-soft", "Focus trend",
              "Up 20% vs last week. Mornings work best.",
              "+20%", "G2"),
         DIV("D8"),
         RULE("heart-soft", "Resets that worked",
              "Water first, then air. Evenings stay hard.",
              "×5", "G3"),
         SEC("A note", "", "S5"),
         ANOTE("Done is a direction, not a streak.", "Nt2"),
         ], "Progress")

    s5 = SCREEN("05 Yours", 1880,
        HEAD("Settings", "Make it yours.",
             "Plan, sounds, reminders, and backup.", "H5"),
        [RULE("crown-ember", "Puduu Pro · $6.99/mo",
              "Unlimited resets · yearly $49.99.", None, "Y1",
              chev=True),
         DIV("D9"),
         RULE("bell-soft", "Gentle nudges",
              "Max 6 per day · quiet 22:00–07:00.", "On", "Y2"),
         DIV("D10"),
         RULE("volume-2-soft", "Sounds and haptics",
              "Calm chime · soft vibration.", "On", "Y3"),
         ], "Yours")

    screens = [s1, s2, s3, s4, s5]
    doc = {"version": "2.19",
           "variables": {k: {"type": "color", "value": v}
                         for k, v in C.items()},
           "children": [GLYPH()] + screens + LABELS(screens)}
    with open("puduu.pen", "w") as f:
        json.dump(doc, f)
    blob = json.dumps(doc)
    print("wrote puduu.pen:",
          sum(1 for _ in blob.split('"id"')) - 1, "nodes")
    print("emoji hits:", len(re.findall(
        r'[\U0001F000-\U0001FAFF\u2600-\u27BF]', blob)))
    # image census: every url must exist on disk
    import pathlib
    urls = sorted(set(re.findall(r'"url": "([^"]+)"', blob)))
    miss = [u for u in urls if not pathlib.Path(u).exists()]
    print("images:", len(urls), "| MISSING:", miss if miss else "none")

if __name__ == "__main__":
    main()
