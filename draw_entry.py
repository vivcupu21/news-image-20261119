"""One-page newspaper renderer for the 19 Nov 2026 news image.

Data-driven: every story lives in a plain dict, and one generic painter
draws them all. Shapes + text only, Pillow, fully deterministic — no
randomness, no timestamps, no network.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 28
RIGHT_EDGE = PAGE_W - MARGIN

PAPER = (250, 247, 238)
INK = (20, 20, 20)
ACCENT = (156, 30, 30)
GREY = (96, 96, 92)
RULE = (70, 70, 70)
PANEL = (216, 229, 240)
PANEL_EDGE = (120, 140, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

_KIND_PATH = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "serif_i": "DejaVuSerif-Italic.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
}

_cache = {}


def get_font(kind, size):
    """Load a DejaVu font, falling back to plain serif if a style is missing."""
    key = (kind, size)
    if key not in _cache:
        path = "%s/%s" % (FONT_DIR, _KIND_PATH[kind])
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _cache[key] = ImageFont.truetype("%s/DejaVuSerif.ttf" % FONT_DIR, size)
    return _cache[key]


def wrap_lines(text, font, width):
    """Greedy word wrap measured with the real font."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if font.getlength(trial) <= width:
                cur = trial
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    return out


def paint_lines(draw, x, y, lines, font, fill=INK, leading=None):
    """Draw lines top-to-bottom; return the y just below the last line."""
    step = leading if leading is not None else int(font.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += step
    return y


def hrule(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def paint_globe(draw, cx, cy, r):
    """Simple wireframe globe: outer circle, two meridians, one parallel."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse(
        [cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
        outline=INK,
        width=2,
    )
    draw.ellipse(
        [cx - int(r * 0.85), cy - int(r * 0.72), cx + int(r * 0.85), cy + int(r * 0.72)],
        outline=INK,
        width=2,
    )
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=2)
    draw.ellipse([cx + 48, cy - 42, cx + 60, cy - 30], fill=ACCENT)


def paint_story(draw, x, y, width, story, head_size=21, body_size=14):
    """Kicker + headline + rule + body for one story; returns bottom y."""
    kicker_f = get_font("sans_b", 13)
    head_f = get_font("serif_b", head_size)
    body_f = get_font("sans", body_size)
    draw.text((x, y), story["kicker"], font=kicker_f, fill=ACCENT)
    y += 22
    head_lines = wrap_lines(story["headline"], head_f, width)
    y = paint_lines(draw, x, y, head_lines, head_f, leading=head_size + 7)
    y += 4
    hrule(draw, x, x + width, y)
    y += 10
    body_lines = wrap_lines(story["body"], body_f, width)
    y = paint_lines(draw, x, y, body_lines, body_f, leading=body_size + 6)
    return y


def paint_also(draw, x, y, width, tag, text):
    """One short item in the ALSO TODAY strip; returns bottom y."""
    tag_f = get_font("sans_b", 13)
    body_f = get_font("sans", 12)
    draw.text((x, y), tag, font=tag_f, fill=ACCENT)
    y += 20
    lines = wrap_lines(text, body_f, width)
    y = paint_lines(draw, x, y, lines, body_f, leading=16)
    return y


MASTHEAD = "THE DAILY GLOBE"
DATE_LINE = "WEDNESDAY, NOVEMBER 19, 2026"
EDITION_LINE = "WORLD EDITION  •  ONE PAGE"

LEAD = {
    "kicker": "APEC  •  SHENZHEN",
    "headline": "Trump, Xi and Putin meet in Shenzhen",
    "dek": "First trilateral summit of the three leaders, held on the sidelines of APEC.",
    "body": (
        "The leaders of the United States, China and Russia met in Shenzhen on "
        "Wednesday for the first trilateral summit of its kind. On the agenda: "
        "nuclear weapons, the war in Ukraine, Iran, trade and artificial intelligence."
    ),
}

COLUMNS = [
    {
        "kicker": "CRIMEA",
        "headline": "Crimea bridge hit again, traffic halted",
        "body": (
            "The Crimea bridge was attacked again on Wednesday and traffic came "
            "to a stop, the BBC reported on 19 November."
        ),
    },
    {
        "kicker": "GAZA",
        "headline": "Israeli tanks cross Gaza ceasefire line",
        "body": "Israeli tanks crossed the Gaza ceasefire line on Wednesday.",
    },
    {
        "kicker": "U.S. – IRAN",
        "headline": "Iran hits U.S. bases; U.S. strikes back",
        "body": (
            "Iran struck U.S. bases in Kuwait and Bahrain, and the United States "
            "hit back on Qeshm Island."
        ),
    },
]

WIDE = [
    {
        "kicker": "WEATHER",
        "headline": "Cyclone Akvan nears India's east coast",
        "body": (
            "Cyclone Akvan is approaching India's east coast, "
            "between Machilipatnam and Puri."
        ),
    },
    {
        "kicker": "GAMES",
        "headline": "GTA VI launches worldwide",
        "body": "Grand Theft Auto VI launched worldwide today, scoring 99 on Metacritic.",
    },
]

ALSO = [
    ("ANTHROPIC", "Anthropic's $81.3bn IPO — the largest ever — debuts today as ANT."),
    ("THE HAGUE", "The ICJ rules today on the Myanmar genocide case."),
    ("BRUSSELS", "The EU proposes a €45bn loan for Ukraine."),
    ("NEW YORK", "A Van Gogh sells for $190.4m — a record."),
    ("TALLINN", "Estonia closes its Russia border on 1 December."),
]


def render_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    title_f = get_font("serif_b", 58)
    tw = draw.textlength(MASTHEAD, font=title_f)
    draw.text(((PAGE_W - tw) / 2, 22), MASTHEAD, font=title_f, fill=INK)
    hrule(draw, MARGIN, RIGHT_EDGE, 100)
    small = get_font("sans", 13)
    draw.text((MARGIN, 108), DATE_LINE, font=small, fill=GREY)
    ew = draw.textlength(EDITION_LINE, font=small)
    draw.text((RIGHT_EDGE - ew, 108), EDITION_LINE, font=small, fill=GREY)
    hrule(draw, MARGIN, RIGHT_EDGE, 132, width=3)
    hrule(draw, MARGIN, RIGHT_EDGE, 137)

    # Lead story, left column.
    lx, lw = MARGIN, 612
    y = 152
    kick_f = get_font("sans_b", 14)
    draw.text((lx, y), LEAD["kicker"], font=kick_f, fill=ACCENT)
    y += 26
    head_f = get_font("serif_b", 40)
    head_lines = wrap_lines(LEAD["headline"], head_f, lw)
    y = paint_lines(draw, lx, y, head_lines, head_f, leading=50)
    y += 8
    dek_f = get_font("serif_i", 17)
    dek_lines = wrap_lines(LEAD["dek"], dek_f, lw)
    y = paint_lines(draw, lx, y, dek_lines, dek_f, leading=24)
    y += 10
    body_f = get_font("sans", 15)
    body_lines = wrap_lines(LEAD["body"], body_f, lw)
    y = paint_lines(draw, lx, y, body_lines, body_f, leading=21)

    # Summit panel, right of the lead.
    px0, py0, px1, py1 = 660, 150, RIGHT_EDGE, 440
    draw.rectangle([px0, py0, px1, py1], fill=PANEL, outline=PANEL_EDGE, width=2)
    panel_f = get_font("sans_b", 13)
    label = "THE SUMMIT"
    lw2 = draw.textlength(label, font=panel_f)
    draw.text(((px0 + px1 - lw2) / 2, py0 + 12), label, font=panel_f, fill=GREY)
    paint_globe(draw, (px0 + px1) // 2, 292, 86)
    cap_f = get_font("sans", 13)
    cap_lines = wrap_lines(
        "The first trilateral meeting of the three leaders.", cap_f, px1 - px0 - 32
    )
    cy = 392
    for line in cap_lines:
        lw3 = draw.textlength(line, font=cap_f)
        draw.text(((px0 + px1 - lw3) / 2, cy), line, font=cap_f, fill=INK)
        cy += 18

    # Three-column row, with hairline rules between columns.
    hrule(draw, MARGIN, RIGHT_EDGE, 452, width=2)
    col_w = 304
    xs = [MARGIN, MARGIN + col_w + 28, MARGIN + 2 * (col_w + 28)]
    bottoms = [paint_story(draw, x, 466, col_w, story) for x, story in zip(xs, COLUMNS)]
    lowest = max(bottoms)
    for gx in (xs[1] - 14, xs[2] - 14):
        draw.line([(gx, 466), (gx, lowest)], fill=GREY, width=1)
    hrule(draw, MARGIN, RIGHT_EDGE, 668)

    # Two-column row, with a hairline rule between columns.
    wide_w = 470
    wide_xs = [MARGIN, MARGIN + wide_w + 28]
    bottoms = [
        paint_story(draw, x, 682, wide_w, story, head_size=22)
        for x, story in zip(wide_xs, WIDE)
    ]
    lowest = max(bottoms)
    draw.line([(wide_xs[1] - 14, 682), (wide_xs[1] - 14, lowest)], fill=GREY, width=1)
    hrule(draw, MARGIN, RIGHT_EDGE, 830)

    # ALSO TODAY strip.
    also_f = get_font("sans_b", 15)
    draw.text((MARGIN, 844), "ALSO TODAY", font=also_f, fill=INK)
    hrule(draw, MARGIN + 130, RIGHT_EDGE, 852)
    item_w = 182
    item_xs = [MARGIN + i * (item_w + 14) for i in range(5)]
    for x, (tag, text) in zip(item_xs, ALSO):
        paint_also(draw, x, 872, item_w, tag, text)

    # Footer.
    foot_f = get_font("sans", 11)
    foot = "THE DAILY GLOBE — WEDNESDAY, NOVEMBER 19, 2026"
    fw = draw.textlength(foot, font=foot_f)
    draw.text(((PAGE_W - fw) / 2, 972), foot, font=foot_f, fill=GREY)
    return img


if __name__ == "__main__":
    render_page().save("entry.png", format="PNG")
