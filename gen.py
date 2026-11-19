#!/usr/bin/env python3
"""Draw THE WORLD — the front page of Thursday 19 November 2026.

A one-page newspaper summing up the day's world news in a single
1024x1024 PNG: the Trump-Xi-Putin handshake in Shenzhen leads, a
globe marks where the news happened, the day in numbers counts the
stories, and 32 more stories run in three columns by continent.

Deterministic: fixed text, fixed fonts, no network, no clock.
Run:  python3 gen.py   -> writes entry.png next to this file.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (244, 239, 228)
INK = (22, 22, 22)
RED = (176, 32, 32)
GREY = (112, 106, 96)
RULE = (196, 188, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, font, fill=INK, leading=None):
    """Draw wrapped lines, return the y below them."""
    lh = leading if leading is not None else int(font.size * 1.22)
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def rule(d, x0, x1, y, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories

LEAD_HEAD = ["TRUMP, XI AND PUTIN", "SHAKE HANDS IN SHENZHEN"]
LEAD_DECK = (
    "The three leaders meet for the first time at APEC, talking world "
    "peace, nuclear arms and two wars \u2014 as Trump wraps up his Asia "
    "tour in China."
)

NUMBERS = [
    ("33", "STORIES"),
    ("6", "CONTINENTS"),
    ("3", "LEADERS"),
    ("1", "LIGHT-DAY"),
]
NUMBERS_LINE = (
    "A day of handshakes in Shenzhen, a bridge hit in Crimea, "
    "and a probe a light-day from home."
)

# (section title, [(headline, deck), ...])
COLUMNS = [
    [
        ("ASIA-PACIFIC", [
            ("Xi calls for open trade at APEC",
             "China urges open markets as Asia-Pacific leaders gather in Shenzhen."),
            ("Putin blasts Western sanctions",
             "Russia's leader says curbs have failed to weaken Moscow."),
            ("Cyclone Akvan bears down on India",
             "Storm set to strike the coast between Machilipatnam and Puri."),
            ("India and Japan review defence ties",
             "Ministers meet in Tokyo for the 2+2 security dialogue."),
            ("Modi meets Prince and Princess of Wales",
             "Talks on boosting UK-India ties in New Delhi."),
            ("Congress targets Modi over inflation",
             "Opposition seeks a white paper on rising prices."),
            ("Australia sanctions Israeli settlers",
             "Canberra acts over expansion in the West Bank."),
            ("Islam set to be world's largest faith",
             "Pew report charts a historic shift by 2035."),
        ]),
        ("AFRICA", [
            ("South Sudan braces for Ebola",
             "UN launches $7m plan to plug preparedness gaps."),
            ("Nigeria, Kenya, Sudan join forces",
             "Ministers seek a united front on misinformation."),
        ]),
    ],
    [
        ("EUROPE", [
            ("Crimean Bridge attacked again",
             "Blast hits the link between Russia and Crimea."),
            ("EU proposes \u20ac45bn Ukraine loan",
             "Kyiv to be repaid once Russia pays reparations."),
            ("M\u00e9lenchon could win French presidency",
             "Justice minister's warning shakes Paris."),
            ("France: fourth weekend of protests",
             "Cost-of-living marches roll on nationwide."),
            ("Van Gogh sells for record $190.4m",
             "Painting fetches a fortune after Nazi-history row."),
            ("LPG tanker sunk off Bulgaria hit by projectiles",
             "Official confirms the vessel was struck."),
        ]),
        ("MIDDLE EAST", [
            ("Israeli tanks cross Gaza ceasefire line",
             "Rare ground operation goes beyond the Yellow Line."),
            ("Four nations call for aid to flooded Gaza",
             "Australia, Canada, Italy and UK urge access."),
            ("Eisenkot tapped to form Israeli government",
             "President bypasses Netanyahu for ex-army chief."),
            ("NGO: 1,100 child amputees face treatment limits",
             "Gaza's young wounded struggle for care."),
            ("Saudi Arabia: danger has passed",
             "Alerts lifted in three southern cities."),
        ]),
    ],
    [
        ("AMERICAS", [
            ("Jeffries set to be first Black House Speaker",
             "Democrat nominated to lead the House."),
            ("Peltola wins Alaska, Senate 56-44",
             "Democrats pad their majority."),
            ("Senators warn AI cyber threats outpacing defences",
             "White House urged to act on the danger."),
            ("US proposes tougher green-card rules",
             "Longer hiring process for employers."),
            ("Canada adjusts China ties, eyes US deal",
             "Carney seeks the right bargain."),
            ("US details $12bn Venezuelan oil revenue",
             "Report traces funds a year after Maduro's capture."),
        ]),
        ("SPORT & BUSINESS", [
            ("Anthropic poised for $1.4tn market debut",
             "Claude-maker heads for a giant listing."),
            ("Crystal Palace 45% stake bid worth ~\u00a3200m",
             "Financier Harris leads the offer."),
            ("Duckett's 133 puts England on top",
             "Tourists strong in third ODI in Australia."),
            ("India women open hockey trophy vs Malaysia",
             "Champions Trophy starts in Bhopal."),
        ]),
    ],
]

FINALLY = (
    "AND FINALLY: Gamers enter Vice City as GTA VI rolls out worldwide "
    "\u2014 after a 13-year wait, the most anticipated game ever arrives."
)


# ---------------------------------------------------------------- drawing

def draw_globe(d, cx, cy, r):
    """Wire-frame globe with red dots where the news happened."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    for k in (0.45, 0.85):
        rx = r * k
        d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=GREY, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=GREY, width=1)
    for dy in (-r * 0.5, r * 0.5):
        half = int(math.sqrt(max(r * r - dy * dy, 0)))
        d.line([(cx - half, cy + dy), (cx + half, cy + dy)], fill=GREY, width=1)
    dots = [
        (0.62, -0.10),
        (-0.30, -0.42),
        (-0.08, 0.05),
        (0.42, 0.18),
        (-0.78, 0.10),
    ]
    for fx, fy in dots:
        px, py = cx + r * fx, cy + r * fy
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)


def draw_section(d, x, y, w, title, stories, head_f, deck_f):
    rule(d, x, x + w, y, width=1)
    y += 6
    d.text((x, y), title, font=f(SANS_B, 13), fill=RED)
    y += 20
    for headline, deck in stories:
        lines = wrap(headline, head_f, w)[:2]
        y = block(d, x, y, lines, head_f, leading=16)
        lines = wrap(deck, deck_f, w)[:2]
        y = block(d, x, y, lines, deck_f, fill=(60, 58, 52), leading=12)
        y += 5
    return y - 7


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([7, 7, W - 8, H - 8], outline=INK, width=3)

    # Masthead
    mast = f(SERIF_B, 86)
    title = "THE WORLD"
    d.text(((W - mast.getlength(title)) / 2, 18), title, font=mast, fill=INK)
    rule(d, 28, W - 28, 112, width=4, fill=RED)

    # Dateline row
    small_b = f(SANS_B, 14)
    small = f(SANS, 14)
    d.text((28, 120), "THURSDAY, 19 NOVEMBER 2026", font=small_b, fill=INK)
    mid = "ONE DAY \u2022 ONE PAGE \u2022 THE WHOLE WORLD"
    d.text(((W - small.getlength(mid)) / 2, 120), mid, font=small, fill=GREY)
    right = "33 STORIES \u2022 6 CONTINENTS"
    d.text((W - 28 - small_b.getlength(right), 120), right, font=small_b, fill=INK)
    rule(d, 28, W - 28, 142, width=2)

    # Lead story
    d.text((28, 152), "THE LEAD \u2022 ASIA-PACIFIC", font=f(SANS_B, 13), fill=RED)
    lead_f = f(SERIF_B, 40)
    y = 172
    for ln in LEAD_HEAD:
        d.text((28, y), ln, font=lead_f, fill=INK)
        y += 48
    deck_f = f(SERIF, 17)
    y = block(d, 28, y + 2, wrap(LEAD_DECK, deck_f, W - 56), deck_f,
              leading=22)
    rule(d, 28, W - 28, y + 8, width=1, fill=RULE)

    # Middle band: globe + day in numbers
    band_y = y + 18
    draw_globe(d, 118, band_y + 62, 62)
    nx = 216
    d.text((nx, band_y), "THE DAY IN NUMBERS", font=f(SANS_B, 13), fill=RED)
    num_f = f(SERIF_B, 46)
    lab_f = f(SANS, 11)
    seg = (W - 28 - nx) / 4
    for i, (num, lab) in enumerate(NUMBERS):
        x = nx + i * seg
        d.text((x, band_y + 22), num, font=num_f, fill=INK)
        d.text((x, band_y + 74), lab, font=lab_f, fill=GREY)
    sum_f = f(SERIF, 15)
    block(d, nx, band_y + 96, wrap(NUMBERS_LINE, sum_f, W - 28 - nx),
          sum_f, leading=19)
    rule(d, 28, W - 28, band_y + 128, width=2)

    # Three columns
    col_y = band_y + 140
    col_w = 304
    xs = [28, 360, 692]
    head_f = f(SERIF_B, 13)
    deck_s = f(SANS, 10)
    ends = []
    for x, sections in zip(xs, COLUMNS):
        cy = col_y
        for title, stories in sections:
            cy = draw_section(d, x, cy, col_w, title, stories, head_f, deck_s)
            cy += 10
        ends.append(cy)
    for x in (352, 684):
        d.line([(x, col_y), (x, max(ends) - 4)], fill=RULE, width=1)
    print("column end y:", [round(e) for e in ends])

    # And finally + footer
    rule(d, 28, W - 28, 962, width=2)
    fin_f = f(SERIF_B, 13)
    block(d, 28, 972, wrap(FINALLY, fin_f, W - 56), fin_f, leading=17)
    rule(d, 28, W - 28, 998, width=1, fill=RULE)
    foot = f(SANS, 10)
    d.text((28, 1003), "Compiled from wire reports  \u2022  Thursday 19 November 2026",
           font=foot, fill=GREY)
    tag = "THE WORLD \u2022 ONE PAGE"
    d.text((W - 28 - foot.getlength(tag), 1003), tag, font=foot, fill=GREY)

    im.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
