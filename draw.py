#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news summary image (1024x1024 PNG).

Deterministic: fixed layout, fixed colours, no randomness, no network,
no external images. Only Pillow + DejaVu fonts (build-time only).
The scoring entrypoint (main.py) does NOT import Pillow; it just copies
the entry.png this script produces.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (11, 37, 69)          # header background
GOLD = (255, 201, 60)        # date line / divider
WHITE = (255, 255, 255)
INK = (20, 33, 61)           # title text
BODY = (51, 51, 51)          # caption text

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def bold(size):
    return ImageFont.truetype(FONT_BOLD, size)


def reg(size):
    return ImageFont.truetype(FONT_REG, size)


def fit_font(text, start, minimum, max_width, font_fn):
    """Largest font size (<= start, >= minimum) that fits max_width."""
    size = start
    while size > minimum:
        f = font_fn(size)
        if f.getlength(text) <= max_width:
            return f
        size -= 2
    return font_fn(minimum)


def wrap_lines(draw, text, font, max_width, max_lines=2):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:max_lines]


# ---------------------------------------------------------------- icons
# Every icon is drawn from basic shapes only, centred on (cx, top) and
# fitting inside a ~150 x 92 box. `c` is the accent colour.

def icon_summit(d, cx, top, c):
    # Three leaders at one table: three heads + shoulders, table line.
    cols = [(192, 57, 43), (31, 78, 156), (160, 120, 10)]
    for i, col in enumerate(cols):
        x = cx + (i - 1) * 56
        d.ellipse([x - 17, top + 4, x + 17, top + 38], fill=col)
        d.pieslice([x - 26, top + 40, x + 26, top + 92], 180, 360, fill=col)
    d.line([cx - 88, top + 88, cx + 88, top + 88], fill=c, width=5)


def icon_controller(d, cx, top, c):
    # Game controller.
    d.rounded_rectangle([cx - 72, top + 22, cx + 72, top + 74], radius=22,
                        fill=c)
    # D-pad (left)
    d.rectangle([cx - 52, top + 38, cx - 34, top + 58], fill=WHITE)
    d.rectangle([cx - 46, top + 32, cx - 40, top + 64], fill=WHITE)
    # Buttons (right)
    for bx, by in ((cx + 36, top + 38), (cx + 50, top + 48), (cx + 36, top + 58)):
        d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=WHITE)
    # Sticks
    d.ellipse([cx - 12, top + 52, cx + 2, top + 66], fill=WHITE)
    d.ellipse([cx + 8, top + 52, cx + 22, top + 66], fill=WHITE)


def icon_quake(d, cx, top, c):
    # Seismograph zig-zag over cracked ground.
    pts = []
    xs = [cx - 84, cx - 62, cx - 44, cx - 28, cx - 12, cx + 4, cx + 20,
          cx + 36, cx + 52, cx + 68, cx + 84]
    ys = [top + 34, top + 34, top + 12, top + 58, top + 22, top + 48,
          top + 16, top + 56, top + 30, top + 44, top + 34]
    d.line(list(zip(xs, ys)), fill=c, width=6, joint="curve")
    # Cracks in the ground.
    d.line([cx - 70, top + 84, cx - 40, top + 68, cx - 18, top + 84],
           fill=c, width=5, joint="curve")
    d.line([cx + 10, top + 84, cx + 38, top + 66, cx + 66, top + 84],
           fill=c, width=5, joint="curve")


def icon_shield(d, cx, top, c):
    # Shield with a star: defence pact.
    shield = [(cx, top + 86), (cx - 52, top + 58), (cx - 52, top + 18),
              (cx, top + 2), (cx + 52, top + 18), (cx + 52, top + 58)]
    d.polygon(shield, fill=c)
    # Star.
    sx, sy, r_out, r_in = cx, top + 40, 24, 10
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    d.polygon(pts, fill=WHITE)


def icon_aid(d, cx, top, c):
    # Aid box with a red cross, above flood waves.
    d.rectangle([cx - 34, top + 2, cx + 34, top + 48], fill=WHITE,
                outline=c, width=4)
    d.rectangle([cx - 6, top + 10, cx + 6, top + 40], fill=(200, 40, 40))
    d.rectangle([cx - 16, top + 20, cx + 16, top + 30], fill=(200, 40, 40))
    for k, y in enumerate((top + 62, top + 76, top + 88)):
        pts = []
        for x in range(cx - 84, cx + 85, 4):
            pts.append((x, y + 5 * math.sin((x - cx) / 18.0 + k)))
        d.line(pts, fill=c, width=5)


def icon_voyager(d, cx, top, c):
    # Satellite with solar panels, dish and a star.
    d.rectangle([cx - 46, top + 30, cx - 14, top + 56], fill=c)
    d.rectangle([cx + 14, top + 30, cx + 46, top + 56], fill=c)
    d.rectangle([cx - 12, top + 26, cx + 12, top + 60], fill=(255, 201, 60),
                outline=c, width=3)
    d.polygon([(cx - 12, top + 60), (cx + 12, top + 60), (cx, top + 76)],
              fill=c)
    # Orbit arc + star.
    d.arc([cx - 84, top - 6, cx + 84, top + 92], 200, 330, fill=c, width=4)
    sx, sy, r = cx + 66, top + 8, 7
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((sx + rr * math.cos(a), sy + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 201, 60), outline=c)


ICONS = [icon_summit, icon_controller, icon_quake,
         icon_shield, icon_aid, icon_voyager]

# (title, caption, cell tint, accent)
STORIES = [
    ("TRUMP\u2013XI\u2013PUTIN SUMMIT", "First-ever summit in Shenzhen",
     (234, 240, 251), (31, 78, 156)),
    ("GTA VI LAUNCHES", "Global launch in Vice City",
     (252, 228, 236), (194, 24, 91)),
    ("JAPAN EARTHQUAKE", "5.7 quake hits Kumamoto",
     (253, 235, 208), (178, 84, 0)),
    ("US\u2013VENEZUELA PACT", "Defence deal after Caracas visit",
     (230, 244, 234), (30, 123, 52)),
    ("GAZA FLOOD AID CALL", "Four nations: let aid into Gaza",
     (224, 242, 247), (11, 114, 133)),
    ("VOYAGER 1 MILESTONE", "One light-day from Earth",
     (232, 234, 246), (61, 52, 139)),
]


def draw_cell(d, x, y, w, h, title, caption, tint, accent, icon_fn):
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=tint,
                        outline=accent, width=3)
    cx = x + w // 2
    icon_fn(d, cx, y + 18, accent)
    title_font = fit_font(title, 38, 28, w - 36, bold)
    d.text((cx, y + 146), title, font=title_font, fill=INK, anchor="mm")
    cap_font = reg(27)
    lines = wrap_lines(d, caption, cap_font, w - 36, max_lines=2)
    if len(lines) == 1:
        d.text((cx, y + 202), lines[0], font=cap_font, fill=BODY,
               anchor="mm")
    else:
        d.text((cx, y + 188), lines[0], font=cap_font, fill=BODY,
               anchor="mm")
        d.text((cx, y + 222), lines[1], font=cap_font, fill=BODY,
               anchor="mm")


def build():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # Header.
    d.rectangle([0, 0, W, 170], fill=NAVY)
    d.text((W // 2, 60), "WORLD NEWS", font=bold(88), fill=WHITE,
           anchor="mm")
    d.text((W // 2, 130), "Thursday 19 November 2026", font=bold(48),
           fill=GOLD, anchor="mm")
    d.rectangle([0, 170, W, 178], fill=GOLD)

    # 2 x 3 grid of stories.
    margin, gap = 24, 16
    cw, ch = 480, 260
    for i, (title, caption, tint, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (cw + gap)
        y = 194 + row * (ch + gap)
        draw_cell(d, x, y, cw, ch, title, caption, tint, accent, ICONS[i])

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
