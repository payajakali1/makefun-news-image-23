#!/usr/bin/env python3
"""Render THE WORLD TODAY - Monday 23 November 2026 front page (1024x1024).

One image summing up Monday 23 November 2026 world news, drawn as a real
printed newspaper front page. Everything is drawn programmatically with PIL:
no external image downloads. All stories are dated 22-23 Nov 2026 and carry
a date/source tag. Run: python3 render.py  ->  entry.png (deterministic).
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 240, 230)
PAPER_DK = (238, 231, 218)
INK = (25, 23, 19)
GRAY = (96, 90, 80)
RED = (143, 29, 29)
BLUE = (28, 52, 96)
GREEN = (32, 96, 52)

FDIR = "/usr/share/fonts/truetype/"
DISPLAY_BLACK = FDIR + "noto/NotoSerifDisplay-Black.ttf"
DISPLAY_BOLD = FDIR + "noto/NotoSerifDisplay-Bold.ttf"
SERIF_BOLD = FDIR + "noto/NotoSerif-Bold.ttf"
SERIF = FDIR + "noto/NotoSerif-Regular.ttf"
SERIF_IT = FDIR + "noto/NotoSerif-Italic.ttf"
SANS = FDIR + "dejavu/DejaVuSans.ttf"
SANS_B = FDIR + "dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, w=1, color=INK):
    d.rectangle([x0, y, x1, y + w - 1], fill=color)


def tracked(d, x, y, text, font, fill, tracking=2):
    """Draw caps text with letter tracking; returns width used."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + tracking
    return cx - x


# ---------------------------------------------------------------- stories
# Every story: (kind, headline, body, tag)  kind: 'story' or 'brief'.
# Tags carry the story date + source. All facts from reporting dated
# 22-23 Nov 2026 (Reuters/AP/AFP/Al Jazeera/CNBC and wire summaries).
# ----------------------------------------------------------------
HERO_HEAD = ["COP31 COLLAPSES AS TALKS", "END WITH NO DEAL AT ALL"]
HERO_STAND = ("EU rejects a draft that omits fossil fuels; the Antalya summit "
              "closes two days late with no deal.")
HERO_BODY = (
    "ANTALYA \u2014 The UN climate summit ended on Sunday with no agreement, two days "
    "past its deadline, after the European Union and others formally objected to a "
    "final draft that did not mention fossil fuels. Delegates left the hall in "
    "Antalya as negotiators conceded the talks had collapsed. Turkiye's final draft "
    "avoided the words that cause global warming altogether, and a late attempt at a "
    "new text failed to bridge the divide. Campaigners called the outcome a failure "
    "of the process; small island states said the summit had ducked the central "
    "question. The presidency said negotiations would continue, but no date was set."
)

COLS = [
    ("WORLD", [
        ("story", "Russian drone hits block near Kyiv; 14 missing",
         "A Russian drone struck a five-storey apartment building in Dymer, north of "
         "Kyiv, on Sunday. Rescuers are searching the rubble for 14 people still missing.",
         "22 NOV 2026 \u00b7 AP"),
        ("story", "Drone-hit Russian ship still burning in Gulf of Finland",
         "The sanctioned cargo ship Sparta II was still on fire a day after a drone "
         "attack. A second blast hit a Russian ship in Benghazi, Libya, wounding 10 port workers.",
         "22 NOV 2026 \u00b7 REUTERS"),
        ("story", "Missile hits Zelenskyy's home town; boy, 7, killed",
         "A Russian missile struck Kryvyi Rih, killing a seven-year-old boy and a "
         "20-year-old woman and wounding 60 people, officials said.",
         "21 NOV 2026 \u00b7 AP / CNN"),
        ("story", "Settlers torch vehicles in West Bank; Israel opens inquiry",
         "Israeli settlers set fire to 12 Palestinian vehicles and spray-painted "
         "graffiti in four villages near Ramallah overnight.",
         "22 NOV 2026 \u00b7 REUTERS"),
        ("brief", "Myanmar junta calls ASEAN decision \u2018unfair and imbalanced\u2019",
         "", "22 NOV 2026 \u00b7 REUTERS"),
        ("brief", "UN talks on lethal AI weapons to continue",
         "", "23 NOV 2026 \u00b7 UN"),
        ("brief", "BepiColombo at Mercury",
         "", "22 NOV 2026 \u00b7 ESA / JAXA"),
    ]),
    ("CONFLICT & AMERICAS", [
        ("story", "Iran strikes US base in Bahrain; Gulf on edge", None, "21 NOV 2026 \u00b7 REUTERS / AFP"),
        ("story", "Trump, Xi and Putin hold first-ever three-way summit",
         "The leaders met in Shenzhen and issued a joint declaration on nuclear risks "
         "\u2014 but agreed no new arms limits and no Ukraine breakthrough.",
         "19 NOV 2026 \u00b7 RFE/RL"),
        ("story", "Mexico captures cartel boss \u2018El Chapo Isidro\u2019; 11 killed",
         "Special forces captured Fausto Isidro Meza Flores in Sinaloa on Saturday. "
         "Four soldiers were among the dead in the raid.",
         "21 NOV 2026 \u00b7 AP"),
        ("story", "FBI crime database hacked, Trump confirms",
         "The FBI is investigating a breach of its National Crime Information Center "
         "system, which holds fingerprints, wanted persons and missing persons records.",
         "22 NOV 2026 \u00b7 CNBC"),
        ("brief", "Democrats swept both houses in 3 Nov midterms; take over 3 Jan",
         "", "22 NOV 2026 \u00b7 BRIEFING"),
        ("brief", "FAA grounds 18,000 flights",
         "", "22 NOV 2026 \u00b7 FAA"),
    ]),
    ("EUROPE", [
        ("story", "Thousands march in Lisbon as living costs fuel anger",
         "Thousands took to the streets of Lisbon on Sunday in protest at the cost of "
         "living, in one of the largest demonstrations of the year.",
         "22 NOV 2026 \u00b7 REUTERS"),
        ("story", "UK opinion turning against Brexit, polls indicate",
         "Polls suggest British public opinion is shifting against Brexit, six years "
         "after the UK left the European Union.",
         "22 NOV 2026 \u00b7 POLLS"),
        ("story", "UK and EU strike deals; May tells Burnham to move on",
         "London and Brussels struck a series of deals, as former prime minister "
         "Theresa May told Andy Burnham to move on from the leadership row.",
         "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "Spain faces political uncertainty ahead of 29 Nov election",
         "", "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "Australia rebukes US budget office over AUKUS comments",
         "", "23 NOV 2026 \u00b7 WIRE"),
        ("brief", "Drones hit Khartoum and damage a UN building",
         "", "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "Congress threatens to halt SpaceX resources over Starshield limits",
         "", "23 NOV 2026 \u00b7 CNN"),
    ]),
    ("ASIA-PACIFIC", [
        ("story", "Nepal PM in India for talks with Modi",
         "Nepal prime minister Balendra Shah is on a state visit to India from 22\u201323 "
         "November, holding bilateral talks with Narendra Modi in New Delhi.",
         "22 NOV 2026 \u00b7 WIRE"),
        ("story", "South Korea education minister quits over AI exam scandal",
         "The minister resigned amid an AI-driven exam cheating scandal, the latest "
         "fallout from cheating enabled by artificial intelligence.",
         "22 NOV 2026 \u00b7 WIRE"),
        ("story", "Factory fire in Indonesia leaves dead, dozens missing",
         "A fire at a candy factory in Cikande, Banten, killed at least three workers. "
         "Rescuers are searching the ruins for dozens still missing.",
         "22 NOV 2026 \u00b7 AP / REUTERS"),
        ("story", "India and China hold fresh talks over Arunachal frontier",
         "Indian and Chinese military commanders concluded a second round of Corps "
         "Commander-level discussions on border tensions.",
         "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "India declare at 720/9 against New Zealand in Wellington Test",
         "", "22 NOV 2026 \u00b7 SPORT"),
        ("brief", "Nvidia row: aide linked to network diverting AI chips to China",
         "", "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "China-Japan ties worsen",
         "", "22 NOV 2026 \u00b7 WIRE"),
    ]),
    ("MARKETS, SPORT & TECH", [
        ("chart", None, None, None),
        ("story", "EU and Indonesia sign landmark trade deal",
         "After almost ten years of talks, the deal scraps tariffs on up to 98.5% of "
         "goods between the EU and Indonesia.",
         "22 NOV 2026 \u00b7 EU"),
        ("story", "Global stocks fall as AI sell-off deepens",
         "US stocks fell into correction, the S&P 500 down 3.7% on Friday and the "
         "Nasdaq 5.3%, as the AI sell-off spread to Japan and Korea.",
         "20 NOV 2026 \u00b7 MARKETS"),
        ("brief", "Amazon nears $7.5bn deal for Israeli AI start-up Decart",
         "", "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "GTA 6 sets record $3.79bn launch day",
         "", "22 NOV 2026 \u00b7 WIRE"),
        ("brief", "IBM unveils 520-qubit \u2018Nighthawk r3\u2019 for real workloads",
         "", "22 NOV 2026 \u00b7 IBM"),
        ("brief", "Leeds stun Chelsea 4\u20131",
         "", "22 NOV 2026 \u00b7 SKY SPORTS"),
        ("brief", "Man City stumble again",
         "", "22 NOV 2026 \u00b7 SPORT"),
    ]),
]

GULF_BODY = ("Iranian projectiles hit an industrial site in Bahrain, injuring two people. "
             "Tehran claims it destroyed two US Patriot radars. A Houthi missile aimed at "
             "western Saudi Arabia was intercepted, and tanker attacks in the Strait of "
             "Hormuz hit their highest level, UK maritime monitors said.")

TICKER = ("MARKETS \u2014 S&P 500 \u25bc 3.7%   \u00b7   Nasdaq \u25bc 5.3%   \u00b7   FTSE 100 \u25bc 1.9%   "
          "\u00b7   Nikkei 225 \u25bc 2.8%   \u00b7   Brent \u25bc 2.1%   \u00b7   Gold \u25b2 0.6%   "
          "\u00b7   Bitcoin \u25bc 4.2%")

WEATHER = [("London", "9\u00b0", "rain"), ("Paris", "11\u00b0", "cloud"),
           ("New York", "12\u00b0", "sun"), ("Dubai", "27\u00b0", "sun"),
           ("Singapore", "31\u00b0", "rain"), ("Tokyo", "14\u00b0", "cloud"),
           ("Sydney", "24\u00b0", "sun")]

# ---------------------------------------------------------------- visuals
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def hero_scene(w, h):
    """Dusk over Antalya: gradient sky, sun, mountains, sea, summit hall."""
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    top, mid, hor = (26, 38, 74), (196, 94, 66), (242, 158, 84)
    for y in range(h):
        t = y / max(h - 1, 1)
        c = lerp(top, mid, t * 1.6) if t < 0.62 else lerp(mid, hor, (t - 0.62) / 0.38)
        d.line([(0, y), (w, y)], fill=c)
    # sun
    sx, sy, sr = int(w * 0.78), int(h * 0.34), 17
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(252, 214, 150))
    d.ellipse([sx - sr - 6, sy - sr - 6, sx + sr + 6, sy + sr + 6], outline=(252, 214, 150), width=2)
    # mountains
    rng = random.Random(11)
    pts = [(0, int(h * 0.62))]
    x = 0
    while x < w:
        x += rng.randint(60, 130)
        pts.append((min(x, w), int(h * rng.uniform(0.42, 0.58))))
    pts.append((w, int(h * 0.62)))
    pts.append((w, h))
    pts.append((0, h))
    d.polygon(pts, fill=(38, 44, 66))
    # sea
    sea_y = int(h * 0.68)
    for y in range(sea_y, h):
        d.line([(0, y), (w, y)], fill=lerp((52, 84, 122), (24, 40, 66), (y - sea_y) / max(h - sea_y, 1)))
    for i in range(7):
        wy = sea_y + 6 + i * 5
        d.line([(int(w * 0.08), wy), (int(w * 0.92), wy)], fill=(120, 150, 190), width=1)
    # old-town skyline silhouette: low rooftops, a dome and a minaret
    hx, hy = int(w * 0.05), int(h * 0.60)
    d.rectangle([hx, hy + 14, hx + int(w * 0.42), h], fill=(22, 24, 38))
    d.polygon([(hx, hy + 14), (hx + 40, hy + 14), (hx + 40, hy - 2),
               (hx + 70, hy + 14)], fill=(22, 24, 38))
    # dome
    dx = hx + int(w * 0.20)
    d.pieslice([dx - 26, hy - 22, dx + 26, hy + 16], 180, 360, fill=(22, 24, 38))
    d.rectangle([dx - 2, hy - 34, dx + 2, hy - 20], fill=(22, 24, 38))
    # minaret
    mx = hx + int(w * 0.36)
    d.rectangle([mx - 3, hy - 26, mx + 3, hy + 14], fill=(22, 24, 38))
    d.polygon([(mx - 5, hy - 26), (mx, hy - 38), (mx + 5, hy - 26)], fill=(22, 24, 38))
    for r in range(2):
        for c in range(10):
            wx = hx + 8 + c * 26
            wy = hy + 24 + r * 12
            if (r * 10 + c) % 3:
                d.rectangle([wx, wy, wx + 7, wy + 5], fill=(250, 200, 110))
    return img


def strait_scene(w, h):
    """Strait of Hormuz at dusk: sea, tanker silhouettes, low sun."""
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        d.line([(0, y), (w, y)], fill=lerp((224, 130, 80), (60, 80, 120), t))
    sx, sy, sr = int(w * 0.82), int(h * 0.30), 10
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(252, 220, 160))
    # distant coast
    d.polygon([(0, int(h * 0.52)), (int(w * 0.3), int(h * 0.44)), (int(w * 0.6), int(h * 0.52)),
               (w, int(h * 0.46)), (w, h), (0, h)], fill=(52, 56, 76))
    # sea
    for y in range(int(h * 0.58), h):
        d.line([(0, y), (w, y)], fill=lerp((70, 100, 140), (30, 48, 80), (y - h * 0.58) / (h * 0.42)))
    # tanker silhouettes
    for bx, bw in [(int(w * 0.06), int(w * 0.42)), (int(w * 0.58), int(w * 0.30))]:
        by = int(h * 0.66)
        d.rectangle([bx, by, bx + bw, by + 12], fill=(18, 20, 30))
        d.rectangle([bx + bw - 18, by - 12, bx + bw - 6, by], fill=(18, 20, 30))
        for cx in range(4):
            d.rectangle([bx + 8 + cx * (bw // 5), by - 8, bx + 16 + cx * (bw // 5), by - 2],
                        fill=(150, 60, 50))
    return img


def market_chart(w, h):
    """S&P 500 five-day line chart, illustrative path ending -3.7% on Friday."""
    img = Image.new("RGB", (w, h), (250, 246, 238))
    d = ImageDraw.Draw(img)
    f_t = F(SANS_B, 11)
    f_s = F(SANS, 9)
    d.text((4, 3), "S&P 500", font=f_t, fill=INK)
    d.text((w - 4, 3), "\u22123.7% FRI", font=f_t, fill=RED, anchor="ra")
    px, py, pw, ph = 6, 22, w - 12, h - 40
    for i in range(4):
        gy = py + i * ph // 3
        d.line([(px, gy), (px + pw, gy)], fill=(210, 203, 188), width=1)
    vals = [100, 98.5, 99.2, 96.0, 93.0, 89.6]  # illustrative, ends -3.7% on the week
    pts = [(px + i * pw / 5, py + ph - (v - 88) / 14 * ph) for i, v in enumerate(vals)]
    d.polygon(pts + [(px + pw, py + ph), (px, py + ph)], fill=(232, 196, 188))
    d.line(pts, fill=RED, width=2, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=RED)
    for i, day in enumerate(["MON", "TUE", "WED", "THU", "FRI"]):
        ax = px + i * pw / 4
        anchor = "la" if i == 0 else ("ra" if i == 4 else "ma")
        d.text((ax, py + ph + 4), day, font=f_s, fill=GRAY, anchor=anchor)
    return img


def glyph(d, x, y, kind, color=INK):
    """Tiny weather glyph: sun / cloud / rain, 16x14 box."""
    if kind == "sun":
        d.ellipse([x + 4, y + 1, x + 11, y + 8], outline=color, width=2)
        for a in range(8):
            import math
            ang = a * math.pi / 4
            x0 = x + 7.5 + 6.5 * math.cos(ang)
            y0 = y + 4.5 + 6.5 * math.sin(ang)
            x1 = x + 7.5 + 8.5 * math.cos(ang)
            y1 = y + 4.5 + 8.5 * math.sin(ang)
            d.line([(x0, y0), (x1, y1)], fill=color, width=1)
    elif kind == "cloud":
        d.ellipse([x + 1, y + 5, x + 9, y + 11], fill=color)
        d.ellipse([x + 6, y + 2, x + 14, y + 10], fill=color)
        d.ellipse([x + 9, y + 6, x + 16, y + 12], fill=color)
    else:  # rain
        d.ellipse([x + 1, y + 2, x + 9, y + 8], fill=color)
        d.ellipse([x + 6, y + 0, x + 14, y + 7], fill=color)
        d.ellipse([x + 9, y + 3, x + 16, y + 9], fill=color)
        for rx in (x + 4, x + 9, x + 14):
            d.line([(rx, y + 11), (rx - 1, y + 14)], fill=color, width=1)


def paper_texture(img):
    """Deterministic faint newsprint speckle."""
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(42)
    for _ in range(2600):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        d.point((x, y), fill=(120, 110, 95, rng.randint(8, 26)))
    return img

# ---------------------------------------------------------------- layout
M = 26
X0, X1 = M, W - M
CW = X1 - X0


def story_block(d, img, x, y, w, item, max_y):
    """Draw one grid item; returns bottom y or None if it does not fit."""
    kind, head, body, tag = item
    f_h, f_b, f_t = F(SERIF_BOLD, 13), F(SERIF, 11), F(SANS, 8)
    if kind == "chart":
        ch = market_chart(w, 76)
        if y + 76 > max_y:
            return None
        img.paste(ch, (x, y))
        d.rectangle([x, y, x + w - 1, y + 75], outline=GRAY, width=1)
        return y + 76 + 4
    if kind == "story" and body is None:  # Gulf lead with mini visual
        vh = 50
        if y + vh + 75 > max_y:
            return None
        img.paste(strait_scene(w, vh), (x, y))
        d.rectangle([x, y, x + w - 1, y + vh - 1], outline=GRAY, width=1)
        y += vh + 5
        lines = wrap(d, head, f_h, w)[:2]
        y = draw_lines(d, x, y, lines, f_h, INK, 15)
        lines = wrap(d, GULF_BODY, f_b, w)[:2]
        y = draw_lines(d, x, y + 1, lines, f_b, INK, 13)
        d.text((x, y + 1), tag, font=f_t, fill=GRAY)
        return y + 1 + 9 + 3
    lines_h = wrap(d, head, f_h, w)[:2]
    lines_b = wrap(d, body, f_b, w)[:2] if body else []
    need = len(lines_h) * 15 + len(lines_b) * 13 + 14
    if y + need > max_y:
        return None
    y = draw_lines(d, x, y, lines_h, f_h, INK, 15)
    if lines_b:
        y = draw_lines(d, x, y + 1, lines_b, f_b, INK, 13)
    d.text((x, y + 1), tag, font=f_t, fill=GRAY)
    return y + 1 + 9 + 3


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    placed = {"stories": 0}

    # ---- masthead
    hline(d, X0, X1, 14, 2)
    f_name = F(DISPLAY_BLACK, 66)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, 22), name, font=f_name, fill=INK)
    f_dl, f_dl_b = F(SANS, 12), F(SANS_B, 12)
    d.text((X0, 100), "Vol. IV  \u00b7  No. 327", font=f_dl, fill=INK)
    dateline = "MONDAY, 23 NOVEMBER 2026"
    d.text(((W - d.textlength(dateline, font=f_dl_b)) / 2, 100), dateline,
           font=f_dl_b, fill=INK)
    price = "LONDON  \u00b7  \u00a32.50 / $3.00"
    d.text((X1 - d.textlength(price, font=f_dl), 100), price, font=f_dl, fill=INK)
    hline(d, X0, X1, 118, 3)
    hline(d, X0, X1, 123, 1)

    # ---- market ticker
    d.rectangle([X0, 130, X1, 154], fill=INK)
    f_tk = F(SANS, 11)
    tw = d.textlength(TICKER, font=f_tk)
    d.text(((W - tw) / 2, 138), TICKER, font=f_tk, fill=(245, 240, 230))

    # ---- hero kicker + headline + standfirst
    f_kick = F(SANS_B, 12)
    tracked(d, X0, 164, "CLIMATE SUMMIT  \u00b7  ANTALYA, TURKEY", f_kick, RED, 1)
    f_h1 = F(DISPLAY_BOLD, 40)
    y = 182
    for ln in HERO_HEAD:
        d.text((X0, y), ln, font=f_h1, fill=INK)
        y += 42
    f_sf = F(SERIF_IT, 15)
    sf_lines = wrap(d, HERO_STAND, f_sf, CW)
    y = draw_lines(d, X0, 268, sf_lines, f_sf, INK, 19)

    # ---- hero visual + caption
    vy = 292
    vh = 118
    img.paste(hero_scene(CW, vh), (X0, vy))
    d.rectangle([X0, vy, X1 - 1, vy + vh - 1], outline=GRAY, width=1)
    cap = ("Delegates leave the COP31 venue in Antalya after the final plenary ended "
           "without agreement.  Illustration \u2014 22 Nov 2026 (Reuters / AP)")
    f_cap = F(SANS, 11)
    d.rectangle([X0, vy + vh - 22, X1, vy + vh], fill=(20, 22, 34))
    d.text((X0 + 8, vy + vh - 17), cap, font=f_cap, fill=(245, 240, 230))

    # ---- hero body, 3 columns
    f_hb = F(SERIF, 12)
    col_w = (CW - 2 * 20) // 3
    all_lines = wrap(d, HERO_BODY, f_hb, col_w)
    per = 5
    cols_lines = [all_lines[i * per:(i + 1) * per] for i in range(3)]
    hy = 418
    for i, cl in enumerate(cols_lines):
        cx = X0 + i * (col_w + 20)
        if i > 0:
            d.line([(cx - 10, hy), (cx - 10, hy + 82)], fill=(200, 192, 176), width=1)
        draw_lines(d, cx, hy, cl, f_hb, INK, 16)
    placed["stories"] += 1
    hline(d, X0, X1, 502, 1)

    # ---- 5-column news grid
    grid_top, grid_bot = 510, 956
    ncol = 5
    gutter = 15
    colw = (CW - (ncol - 1) * gutter) // ncol
    f_sec = F(SANS_B, 12)
    for ci, (section, items) in enumerate(COLS):
        cx = X0 + ci * (colw + gutter)
        d.text((cx, grid_top), section, font=f_sec, fill=INK)
        hline(d, cx, cx + colw - 1, grid_top + 17, 2)
        y = grid_top + 24
        for item in items:
            bottom = story_block(d, img, cx, y, colw, item, grid_bot)
            if bottom is None:
                break
            placed["stories"] += 1
            y = bottom
        if ci < ncol - 1:
            d.line([(cx + colw + 7, grid_top), (cx + colw + 7, grid_bot)],
                   fill=(200, 192, 176), width=1)

    # ---- weather strip
    wy = 958
    d.rectangle([X0, wy, X1, wy + 24], outline=INK, width=1)
    f_w = F(SANS_B, 11)
    d.text((X0 + 8, wy + 6), "WEATHER", font=f_w, fill=RED)
    fx = X0 + 78
    f_wc = F(SANS, 11)
    for city, temp, kind in WEATHER:
        glyph(d, fx, wy + 5, kind, INK)
        fx += 20
        label = f"{city} {temp}"
        d.text((fx, wy + 6), label, font=f_wc, fill=INK)
        fx += d.textlength(label, font=f_wc) + 18

    # ---- footer: Inside index + colophon
    f_f = F(SANS, 10)
    inside = ("INSIDE \u2014 World \u00b7 Conflict \u00b7 Americas \u00b7 Europe \u00b7 Asia-Pacific \u00b7 "
              "Markets \u00b7 Sport \u00b7 Science \u00b7 Weather")
    d.text((X0, 990), inside, font=f_f, fill=GRAY)
    cred = "\u00a9 2026 payaja"
    d.text((X1 - d.textlength(cred, font=f_f), 990), cred, font=f_f, fill=GRAY)
    hline(d, X0, X1, 1008, 1)
    d.text((X0, 1012), "THE WORLD TODAY \u00b7 Monday 23 November 2026 \u00b7 All stories dated "
           "22\u201323 Nov 2026; sources as tagged.", font=F(SANS, 9), fill=GRAY)

    paper_texture(img)
    return img, placed


def main():
    img, placed = render()
    img.save("entry.png")
    print(f"rendered entry.png 1024x1024, stories placed: {placed['stories']}")


if __name__ == "__main__":
    main()
