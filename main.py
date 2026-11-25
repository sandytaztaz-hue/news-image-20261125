#!/usr/bin/env python3
"""Sum 25 — news-image-20261125. Pure-stdlib program: draws a 1024x1024
broadsheet of Wednesday 25 November 2026 world news and writes it to
/output/entry.png. No network, no third-party modules, deterministic output.
"""
import math
import os
import struct
import sys
import zlib

W = 1024
H = 1024

PAPER = (251, 247, 239)
INK = (26, 26, 26)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (46, 125, 107)
GREEN = (39, 110, 66)
GOLD = (176, 132, 34)
GREY = (120, 118, 112)
LIGHT = (238, 232, 220)
LIGHT2 = (244, 240, 230)
SKY = (178, 214, 232)
NIGHT = (16, 28, 54)
ORANGE = (214, 96, 32)
WHITE = (255, 255, 255)
CREAM = (246, 238, 220)

# ---------------------------------------------------------------- font: 5x7
# Each glyph is 7 rows; each row is a 5-bit int, bit 4 = leftmost pixel.
FONT = {
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '!': (4, 4, 4, 4, 4, 0, 4),
    '"': (10, 10, 10, 0, 0, 0, 0),
    '#': (10, 10, 31, 10, 31, 10, 10),
    '$': (4, 15, 20, 14, 5, 30, 4),
    '%': (25, 26, 4, 8, 13, 19, 0),
    '&': (12, 18, 20, 8, 21, 18, 13),
    "'": (4, 4, 8, 0, 0, 0, 0),
    '(': (2, 4, 8, 8, 8, 4, 2),
    ')': (8, 4, 2, 2, 2, 4, 8),
    '*': (4, 21, 14, 21, 4, 0, 0),
    '+': (0, 4, 4, 31, 4, 4, 0),
    ',': (0, 0, 0, 0, 4, 4, 8),
    '-': (0, 0, 0, 31, 0, 0, 0),
    '.': (0, 0, 0, 0, 0, 12, 12),
    '/': (1, 2, 2, 4, 8, 8, 16),
    '0': (14, 17, 19, 21, 25, 17, 14),
    '1': (4, 12, 4, 4, 4, 4, 14),
    '2': (14, 17, 1, 6, 8, 16, 31),
    '3': (31, 2, 4, 2, 1, 17, 14),
    '4': (2, 6, 10, 18, 31, 2, 2),
    '5': (31, 16, 30, 1, 1, 17, 14),
    '6': (6, 8, 16, 30, 17, 17, 14),
    '7': (31, 1, 2, 4, 8, 8, 8),
    '8': (14, 17, 17, 14, 17, 17, 14),
    '9': (14, 17, 17, 15, 1, 2, 12),
    ':': (0, 12, 12, 0, 12, 12, 0),
    ';': (0, 12, 12, 0, 12, 4, 8),
    '<': (2, 4, 8, 16, 8, 4, 2),
    '=': (0, 0, 31, 0, 31, 0, 0),
    '>': (8, 4, 2, 1, 2, 4, 8),
    '?': (14, 17, 1, 2, 4, 0, 4),
    '@': (14, 17, 23, 21, 23, 16, 14),
    'A': (14, 17, 17, 31, 17, 17, 17),
    'B': (30, 17, 17, 30, 17, 17, 30),
    'C': (14, 17, 16, 16, 16, 17, 14),
    'D': (30, 17, 17, 17, 17, 17, 30),
    'E': (31, 16, 16, 30, 16, 16, 31),
    'F': (31, 16, 16, 30, 16, 16, 16),
    'G': (14, 17, 16, 23, 17, 17, 15),
    'H': (17, 17, 17, 31, 17, 17, 17),
    'I': (14, 4, 4, 4, 4, 4, 14),
    'J': (7, 2, 2, 2, 2, 18, 12),
    'K': (17, 18, 20, 24, 20, 18, 17),
    'L': (16, 16, 16, 16, 16, 16, 31),
    'M': (17, 27, 21, 21, 17, 17, 17),
    'N': (17, 25, 21, 19, 17, 17, 17),
    'O': (14, 17, 17, 17, 17, 17, 14),
    'P': (30, 17, 17, 30, 16, 16, 16),
    'Q': (14, 17, 17, 17, 21, 18, 13),
    'R': (30, 17, 17, 30, 20, 18, 17),
    'S': (15, 16, 16, 14, 1, 1, 30),
    'T': (31, 4, 4, 4, 4, 4, 4),
    'U': (17, 17, 17, 17, 17, 17, 14),
    'V': (17, 17, 17, 17, 17, 10, 4),
    'W': (17, 17, 17, 21, 21, 21, 10),
    'X': (17, 17, 10, 4, 10, 17, 17),
    'Y': (17, 17, 10, 4, 4, 4, 4),
    'Z': (31, 1, 2, 4, 8, 16, 31),
    '[': (14, 8, 8, 8, 8, 8, 14),
    '\\': (16, 8, 8, 4, 2, 2, 1),
    ']': (14, 2, 2, 2, 2, 2, 14),
    '^': (4, 10, 17, 0, 0, 0, 0),
    '_': (0, 0, 0, 0, 0, 0, 31),
    '`': (8, 4, 2, 0, 0, 0, 0),
    'a': (0, 0, 14, 1, 15, 17, 15),
    'b': (16, 16, 30, 17, 17, 17, 30),
    'c': (0, 0, 14, 16, 16, 17, 14),
    'd': (1, 1, 15, 17, 17, 17, 15),
    'e': (0, 0, 14, 17, 31, 16, 14),
    'f': (6, 8, 8, 30, 8, 8, 8),
    'g': (0, 15, 17, 17, 15, 1, 14),
    'h': (16, 16, 30, 17, 17, 17, 17),
    'i': (4, 0, 12, 4, 4, 4, 14),
    'j': (2, 0, 6, 2, 2, 18, 12),
    'k': (16, 16, 18, 20, 24, 20, 18),
    'l': (12, 4, 4, 4, 4, 4, 14),
    'm': (0, 0, 26, 21, 21, 21, 21),
    'n': (0, 0, 30, 17, 17, 17, 17),
    'o': (0, 0, 14, 17, 17, 17, 14),
    'p': (0, 0, 30, 17, 17, 30, 16),
    'q': (0, 15, 17, 17, 15, 1, 1),
    'r': (0, 0, 22, 28, 16, 16, 16),
    's': (0, 0, 15, 16, 14, 1, 30),
    't': (8, 8, 30, 8, 8, 9, 6),
    'u': (0, 0, 17, 17, 17, 19, 13),
    'v': (0, 0, 17, 17, 17, 10, 4),
    'w': (0, 0, 17, 17, 21, 21, 10),
    'x': (0, 0, 17, 10, 4, 10, 17),
    'y': (0, 0, 17, 17, 15, 1, 14),
    'z': (0, 0, 31, 2, 4, 8, 31),
    '{': (6, 8, 8, 28, 8, 8, 6),
    '|': (4, 4, 4, 4, 4, 4, 4),
    '}': (12, 2, 2, 7, 2, 2, 12),
    '~': (0, 0, 0, 8, 21, 0, 0),
}


def char_w(scale):
    return 6 * scale


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def wrap_text(s, max_w, scale):
    """Greedy word wrap; returns list of lines, each <= max_w px wide."""
    cw = 6 * scale
    max_chars = max(1, max_w // cw)
    lines = []
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        for wd in words:
            if not cur:
                cur = wd
            elif len(cur) + 1 + len(wd) <= max_chars:
                cur = cur + " " + wd
            else:
                lines.append(cur)
                cur = wd
        if cur != "" or not lines:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- framebuffer
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = c[0]
            self.px[i + 1] = c[1]
            self.px[i + 2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + (x1 - x0) * 3] = row

    def hline(self, x0, x1, y, c):
        self.fill_rect(min(x0, x1), y, abs(x1 - x0) + 1, 1, c)

    def vline(self, x, y0, y1, c):
        self.fill_rect(x, min(y0, y1), 1, abs(y1 - y0) + 1, c)

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int(math.sqrt(max(0, r * r - (yy - cy) * (yy - cy))))
            self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, c)

    def ring(self, cx, cy, r, c, t=2):
        for yy in range(cy - r, cy + r + 1):
            d2 = (yy - cy) * (yy - cy)
            if d2 > r * r:
                continue
            dx = int(math.sqrt(max(0, r * r - d2)))
            dx2 = int(math.sqrt(max(0, (r - t) * (r - t) - d2))) if r - t > 0 else 0
            self.fill_rect(cx - dx, yy, dx - dx2, 1, c)
            self.fill_rect(cx + dx2 + 1, yy, dx - dx2, 1, c)

    def poly(self, pts, c):
        """Scanline fill of a simple polygon (list of (x, y))."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        y0 = max(0, min(ys))
        y1 = min(self.h - 1, max(ys))
        n = len(pts)
        for yy in range(y0, y1 + 1):
            xs = []
            for i in range(n):
                x0, y0p = pts[i]
                x1, y1p = pts[(i + 1) % n]
                if (y0p <= yy < y1p) or (y1p <= yy < y0p):
                    t = (yy - y0p) / (y1p - y0p)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[k]), yy, int(xs[k + 1]) - int(xs[k]) + 1, 1, c)

    def tri(self, ax, ay, bx, by, cx, cy, c):
        self.poly([(ax, ay), (bx, by), (cx, cy)], c)

    # ---- text ----
    def glyph(self, x, y, scale, c, ch):
        g = FONT.get(ch)
        if g is None:
            return
        for r in range(7):
            row = g[r]
            if row == 0:
                continue
            for col in range(5):
                if row & (16 >> col):
                    self.fill_rect(x + col * scale, y + r * scale, scale, scale, c)

    def text(self, x, y, scale, c, s):
        cx = x
        for ch in s:
            self.glyph(cx, y, scale, c, ch)
            cx += 6 * scale
        return cx

    def text_center(self, x0, x1, y, scale, c, s):
        w = text_w(s, scale)
        self.text(x0 + (x1 - x0 - w) // 2, y, scale, c, s)

    def para(self, x, y, max_w, scale, c, s, leading=None):
        """Draw wrapped paragraph; returns y just below last line."""
        lh = (leading if leading is not None else 7 * scale + 2)
        for ln in wrap_text(s, max_w, scale):
            self.text(x, y, scale, c, ln)
            y += lh
        return y


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# ---------------------------------------------------------------- scenes
def scene_rocket(cv, x, y, w, h):
    """Lead scene: night launch over Jiuquan. Big rocket, flame, Tiangong ring."""
    cv.fill_rect(x, y, w, h, NIGHT)
    for (sx, sy, r) in [(18, 12, 2), (70, 26, 1), (140, 8, 2), (210, 30, 1),
                        (300, 14, 2), (380, 34, 1), (450, 10, 2), (500, 40, 1),
                        (250, 48, 1), (120, 44, 1), (470, 58, 1), (40, 60, 1)]:
        cv.circle(x + sx % w, y + sy, r, WHITE)
    # ground
    cv.fill_rect(x, y + h - 26, w, 26, (38, 32, 26))
    cv.fill_rect(x, y + h - 26, w, 2, (90, 82, 60))
    # launch tower
    cv.fill_rect(x + 92, y + 22, 10, h - 48, (120, 118, 110))
    cv.fill_rect(x + 84, y + 30, 26, 4, (120, 118, 110))
    cv.fill_rect(x + 84, y + 58, 26, 4, (120, 118, 110))
    # rocket body
    rx = x + 150
    cv.fill_rect(rx, y + 34, 34, 92, WHITE)
    cv.fill_rect(rx, y + 34, 6, 92, (210, 210, 205))
    cv.tri(rx, y + 34, rx + 17, y + 10, rx + 34, y + 34, RED)
    cv.fill_rect(rx + 8, y + 62, 18, 16, RED)
    cv.text(rx + 11, y + 64, 1, WHITE, "24")
    # fins
    cv.tri(rx - 12, y + 126, rx, y + 104, rx, y + 126, RED)
    cv.tri(rx + 34, y + 126, rx + 34, y + 104, rx + 46, y + 126, RED)
    # flame
    cv.tri(rx + 4, y + 126, rx + 17, y + h - 26, rx + 30, y + 126, ORANGE)
    cv.tri(rx + 10, y + 126, rx + 17, y + h - 34, rx + 24, y + 126, (255, 214, 90))
    # smoke puffs
    for (sx, sy, r) in [(120, h - 34, 12), (210, h - 30, 15), (250, h - 38, 10)]:
        cv.circle(x + sx, y + sy, r, (200, 196, 188))
    # Tiangong station ring, upper right
    sx0 = x + w - 150
    sy0 = y + 30
    cv.ring(sx0, sy0, 26, (200, 210, 225), 5)
    cv.fill_rect(sx0 - 52, sy0 - 5, 26, 10, (150, 160, 175))
    cv.fill_rect(sx0 + 26, sy0 - 5, 26, 10, (150, 160, 175))
    cv.circle(sx0, sy0, 8, (230, 235, 240))
    cv.text(sx0 - 34, sy0 + 34, 1, WHITE, "TIANGONG")


def scene_fire(cv, x, y, w, h):
    """Flinders Island bushfire: flame over scrub hills, smoke sky."""
    cv.fill_rect(x, y, w, h, (246, 226, 196))
    cv.fill_rect(x, y, w, 16, (240, 200, 150))
    # hills
    cv.poly([(x, y + h), (x, y + h - 34), (x + w // 3, y + h - 52),
             (x + 2 * w // 3, y + h - 30), (x + w, y + h - 44), (x + w, y + h)],
            (122, 96, 52))
    cv.poly([(x, y + h), (x, y + h - 18), (x + w // 2, y + h - 30),
             (x + w, y + h - 14), (x + w, y + h)], (88, 70, 38))
    # flame
    fx = x + w // 2
    fy = y + h - 52
    cv.tri(fx - 34, fy + 34, fx, fy - 34, fx + 34, fy + 34, ORANGE)
    cv.tri(fx - 20, fy + 34, fx, fy - 12, fx + 20, fy + 34, (255, 190, 60))
    cv.tri(fx - 9, fy + 34, fx, fy + 4, fx + 9, fy + 34, (255, 240, 160))
    # smoke
    for (sx, sy, r) in [(w // 4, 14, 10), (w // 2 + 26, 8, 12), (3 * w // 4, 16, 9)]:
        cv.circle(x + sx, y + sy, r, (150, 140, 128))
    # trees
    for tx in (12, w - 22, w // 5):
        cv.fill_rect(x + tx, y + h - 26, 3, 12, (60, 50, 30))
        cv.tri(x + tx - 6, y + h - 14, x + tx + 1, y + h - 34, x + tx + 9, y + h - 14,
               (46, 110, 62))


def scene_chart(cv, x, y, w, h):
    """US data pile: rising bars + capitol dome."""
    cv.fill_rect(x, y, w, h, (232, 238, 246))
    if w < 120:
        # mini thumb: plain rising bars only, no text, no dome
        base = y + h - 6
        vals = [14, 22, 18, 28, 36, 30, 44]
        bw = w // len(vals)
        for i, v in enumerate(vals):
            bx = x + 3 + i * bw
            col = RED if i == len(vals) - 1 else NAVY
            cv.fill_rect(bx, base - v, bw - 2, v, col)
        return
    # dome
    dx = x + w - 74
    dy = y + h - 40
    cv.fill_rect(dx, dy, 56, 26, WHITE)
    cv.rect(dx, dy, 56, 26, NAVY, 2)
    cv.circle(dx + 28, dy, 16, WHITE)
    cv.circle(dx + 28, dy, 16, NAVY)
    cv.circle(dx + 28, dy, 12, WHITE)
    cv.fill_rect(dx + 26, dy - 22, 4, 8, NAVY)
    cv.circle(dx + 28, dy - 24, 3, GOLD)
    # bars (scaled to fit the panel height)
    base = y + h - 14
    vals = [26, 40, 34, 52, 66, 58, 80]
    bw = (w - 110) // len(vals)
    for i, v in enumerate(vals):
        vh = int(v * (h - 30) / 80)
        bx = x + 10 + i * bw
        col = RED if i == len(vals) - 1 else NAVY
        cv.fill_rect(bx, base - vh, bw - 6, vh, col)
    # trend arrow
    cv.line(x + 12, base - 30, x + w - 96, base - 82, RED)
    cv.tri(x + w - 96, base - 82, x + w - 112, base - 80, x + w - 98, base - 66, RED)
    cv.text(x + 10, y + 6, 1, NAVY, "Q3 GDP ~3.4%")


def scene_ship(cv, x, y, w, h, sinking=False):
    """Grey warship at sea, drone above."""
    cv.fill_rect(x, y, w, h, SKY)
    if w < 120:
        # mini thumb: small ship centred in the thumb, nothing escapes it
        cv.fill_rect(x, y + h - 14, w, 14, (64, 110, 150))
        hx = x + 6
        hy = y + h - 26
        cv.poly([(hx, hy), (hx + 50, hy), (hx + 44, hy + 12), (hx + 6, hy + 12)],
                (90, 96, 104))
        cv.fill_rect(hx + 8, hy - 10, 22, 10, (70, 76, 84))
        cv.fill_rect(hx + 34, hy - 6, 10, 6, (70, 76, 84))
        cv.circle(hx + 44, hy - 14, 4, (120, 118, 112))
        cv.circle(hx + 48, hy - 20, 3, (140, 138, 132))
        dx = x + w - 14
        dy = y + 6
        cv.fill_rect(dx, dy, 8, 4, INK)
        cv.fill_rect(dx - 4, dy + 1, 16, 1, INK)
        return
    cv.fill_rect(x, y + h - 30, w, 30, (64, 110, 150))
    cv.fill_rect(x, y + h - 30, w, 3, (40, 84, 120))
    # waves
    for wx in range(0, w, 26):
        cv.line(x + wx, y + h - 18, x + wx + 12, y + h - 14, WHITE)
    # hull
    hx = x + w // 2 - 90
    hy = y + h - 58
    cv.poly([(hx, hy), (hx + 180, hy), (hx + 162, hy + 28), (hx + 18, hy + 28)],
            (90, 96, 104))
    cv.fill_rect(hx + 20, hy - 22, 60, 22, (70, 76, 84))
    cv.fill_rect(hx + 96, hy - 14, 34, 14, (70, 76, 84))
    cv.fill_rect(hx + 130, hy - 30, 6, 30, (70, 76, 84))
    cv.text(hx + 34, hy - 18, 1, WHITE, "07")
    if sinking:
        cv.tri(hx + 150, hy, hx + 170, hy - 44, hx + 180, hy, (90, 90, 88))
        cv.circle(hx + 168, hy - 52, 10, (120, 118, 112))
        cv.circle(hx + 178, hy - 66, 7, (140, 138, 132))
        cv.tri(hx + 60, hy + 28, hx + 90, hy + 6, hx + 120, hy + 28, (64, 110, 150))
    # drone
    dx = x + w - 60
    dy = y + 16
    cv.fill_rect(dx, dy, 16, 8, INK)
    cv.fill_rect(dx - 8, dy + 2, 32, 2, INK)
    cv.fill_rect(dx + 6, dy + 8, 4, 6, INK)


def scene_tower(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (240, 232, 214))
    tx = x + w // 2 - 16
    cv.fill_rect(tx, y + 8, 32, h - 8, (150, 140, 120))
    cv.fill_rect(tx - 6, y + 2, 44, 8, (120, 110, 92))
    for fy in range(y + 16, y + h - 6, 12):
        cv.fill_rect(tx + 5, fy, 22, 6, (250, 244, 220))
    cv.fill_rect(x + 8, y + h - 12, w - 16, 12, (110, 96, 70))
    dx = x + 14
    dy = y + 12
    cv.fill_rect(dx, dy, 12, 6, INK)
    cv.fill_rect(dx - 6, dy + 2, 24, 2, INK)
    cv.circle(x + w - 20, y + 14, 6, GOLD)


def scene_dunes(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (244, 222, 180))
    cv.circle(x + w - 18, y + 14, 10, (255, 214, 90))
    cv.poly([(x, y + h), (x, y + h - 22), (x + w // 2, y + h - 40),
             (x + w, y + h - 20), (x + w, y + h)], (222, 190, 130))
    cv.poly([(x, y + h), (x, y + h - 10), (x + w // 2, y + h - 22),
             (x + w, y + h - 8), (x + w, y + h)], (200, 164, 100))
    cv.fill_rect(x + w // 2 - 2, y + 8, 3, 26, (90, 70, 50))
    cv.tri(x + w // 2 + 1, y + 8, x + w // 2 + 22, y + 14, x + w // 2 + 1, y + 20, RED)


def scene_block(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (226, 226, 222))
    bx = x + 10
    cv.fill_rect(bx, y + 10, w - 20, h - 26, (150, 140, 128))
    for wy in range(y + 16, y + h - 30, 14):
        for wx in range(bx + 6, x + w - 14, 16):
            cv.fill_rect(wx, wy, 9, 8, (60, 60, 58))
    # broken corner + rubble
    cv.tri(bx, y + 10, bx + 34, y + 10, bx, y + 44, (226, 226, 222))
    cv.fill_rect(bx, y + h - 16, 26, 8, (110, 104, 96))
    cv.fill_rect(bx + 30, y + h - 12, 18, 6, (130, 124, 116))
    cv.fill_rect(bx + 52, y + h - 14, 12, 6, (110, 104, 96))


def scene_medal(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (238, 232, 220))
    cx = x + w // 2
    cv.tri(cx - 12, y + 4, cx + 12, y + 4, cx, y + h // 2, RED)
    cv.tri(cx - 6, y + 4, cx + 6, y + 4, cx, y + h // 2 - 8, WHITE)
    cv.circle(cx, y + h // 2 + 12, 16, GOLD)
    cv.ring(cx, y + h // 2 + 12, 16, (140, 104, 26), 2)
    cv.text(cx - 4, y + h // 2 + 6, 1, (120, 88, 20), "1")


def scene_lock(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (232, 236, 242))
    cx = x + w // 2
    cy = y + h // 2 + 4
    cv.ring(cx, cy - 14, 12, NAVY, 4)
    cv.fill_rect(cx - 16, cy - 8, 32, 26, NAVY)
    cv.circle(cx, cy + 2, 4, WHITE)
    cv.fill_rect(cx - 2, cy + 2, 4, 8, WHITE)
    cv.line(cx - 16, cy - 8, cx + 16, cy + 18, RED)
    cv.line(cx - 16, cy + 18, cx + 16, cy - 8, RED)


def scene_chip(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (226, 236, 228))
    cx = x + w // 2
    cy = y + h // 2
    cv.fill_rect(cx - 16, cy - 14, 32, 28, INK)
    cv.fill_rect(cx - 9, cy - 7, 18, 14, TEAL)
    for px in (-22, -16, -10, 10, 16, 22):
        cv.fill_rect(cx + px - 1, cy - 20, 3, 6, INK)
        cv.fill_rect(cx + px - 1, cy + 14, 3, 6, INK)
    for py in (-10, 0, 10):
        cv.fill_rect(cx - 22, cy + py - 1, 6, 3, INK)
        cv.fill_rect(cx + 16, cy + py - 1, 6, 3, INK)


def scene_stars(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, NAVY)
    for (sx, sy) in [(10, 8), (26, 18), (w - 12, 10), (w - 28, 22), (w // 2, 6),
                     (14, h - 12), (w - 16, h - 14), (w // 2 + 8, h - 10)]:
        cv.circle(x + sx, y + sy, 2, GOLD)
    cv.circle(x + w // 2, y + h // 2, 12, GOLD)
    cv.ring(x + w // 2, y + h // 2, 12, (200, 170, 80), 2)


# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-85, 66), (-75, 62),
     (-55, 52), (-60, 45), (-75, 35), (-80, 25), (-85, 15), (-90, 14),
     (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58),
     (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -10), (-35, -20),
     (-45, -30), (-55, -35), (-65, -40), (-70, -50), (-70, -30), (-70, -20),
     (-80, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (48, 10), (40, 0), (35, -15), (30, -25), (20, -35), (15, -30),
     (12, -18), (8, 0), (8, 4), (-8, 4), (-13, 8)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 70), (5, 60), (0, 55), (-5, 50), (-10, 44)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (90, 75), (110, 73), (130, 72), (150, 70),
     (170, 66), (162, 60), (158, 52), (142, 45), (140, 40), (130, 35),
     (127, 33), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (80, 15), (75, 10), (70, 20), (60, 25), (55, 26),
     (50, 30), (45, 30), (40, 36), (35, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]

# (number, label, lat, lon, colour) — numbers are the story numbers
PINS = [
    (1, "Jiuquan", 39.8, 98.5, RED),
    (2, "Flinders I.", -40.0, 148.0, ORANGE),
    (3, "Washington", 38.9, -77.0, NAVY),
    (4, "Canberra", -35.3, 149.1, ORANGE),
    (5, "Benghazi", 32.1, 20.07, NAVY),
    (6, "Riyadh", 24.7, 46.7, RED),
    (7, "Aden", 12.8, 45.0, ORANGE),
    (8, "Kyiv", 50.45, 30.52, NAVY),
    (9, "New York", 40.7, -74.0, NAVY),
    (12, "Brussels", 50.85, 4.35, NAVY),
    (13, "Accra", 5.6, -0.19, TEAL),
    (15, "Stockholm", 59.3, 18.07, NAVY),
]


def draw_map(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (233, 240, 242))
    cv.rect(x, y, w, h, GREY, 1)
    lon0, lon1 = -170.0, 190.0
    lat0, lat1 = -58.0, 84.0

    def proj(lon, lat):
        px = x + int((lon - lon0) / (lon1 - lon0) * w)
        py = y + int((lat1 - lat) / (lat1 - lat0) * h)
        return px, py

    for cont in CONTINENTS:
        cv.poly([proj(lon, lat) for lon, lat in cont], (178, 184, 178))
    # graticule
    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        cv.vline(px, y + 2, y + h - 3, (210, 216, 220))
    for lat in (-30, 0, 30, 60):
        _, py = proj(0, lat)
        cv.hline(x + 2, x + w - 3, py, (210, 216, 220))
    for (num, label, lat, lon, col) in PINS:
        px, py = proj(lon, lat)
        cv.circle(px, py, 6, col)
        cv.ring(px, py, 6, WHITE, 1)
        if num < 10:
            cv.text(px - 2, py - 3, 1, WHITE, str(num))
        else:
            cv.text(px - 5, py - 3, 1, WHITE, str(num))


# ---------------------------------------------------------------- layout
MX = 14
RX = 1010
STATUS_COL = {
    "CONFIRMED": GREEN,
    "OFFICIAL": NAVY,
    "REPORTED": INK,
    "SCHEDULED": TEAL,
    "FORECAST": (150, 110, 20),
    "CLAIM": RED,
}

STATS = [
    ("18th", "CREWED CHINA FLIGHT"),
    ("3,000 ha", "FLINDERS FIRE HA"),
    ("11", "WOUNDED RIYADH"),
    ("700,000+", "RUSSIANS KILLED"),
    ("47,000", "WOMEN KILLED 2025"),
    ("98%", "DEC FED HIKE ODDS"),
    ("$237.5bn", "VENEZUELA DEBT"),
    ("3.4%", "Q3 GDP EST"),
]

TIMELINE_EVENTS = [
    (0, 18, "00:18 SHENZHOU LIFTS OFF"),
    (0, 30, "00:30 AU CPI"),
    (1, 23, "01:23 TFS WATCH AND ACT"),
    (7, 0, "07:00 GERMANY GDP FINAL"),
    (13, 30, "13:30 US DATA PILE"),
    (15, 0, "15:00 US HOME SALES"),
    (19, 0, "19:00 BEIGE BOOK"),
    (20, 0, "20:00 UCL NIGHT"),
]

CARDS = [
    (4, "CANBERRA", "FORECAST", "October CPI due",
     "CPI due today; Sep 4.3% y/y, trimmed mean 3.6%.", "chart"),
    (5, "KYIV", "CLAIM", "Warship sunk off Benghazi",
     "Ukraine says it sank a Russian warship off Benghazi.", "ship2"),
    (6, "RIYADH", "CONFIRMED", "Riyadh tower hit, 11 hurt",
     "Houthi drone hits tallest tower; 11 wounded.", "tower"),
    (7, "ADEN", "REPORTED", "Houthis 60 km from Aden",
     "Houthis 60 km out; army says the city will not fall.", "dunes"),
    (8, "KYIV REGION", "CONFIRMED", "11 killed near Kyiv",
     "Bodies pulled from a block hit by drones; toll 11.", "block"),
    (9, "WASHINGTON", "CONFIRMED", "Giuliani honoured",
     "Trump awards Giuliani the Medal of Freedom.", "medal"),
    (10, "WASHINGTON", "REPORTED", "CIA, ODNI cyber breach",
     "Spy agencies breached; unclassified data taken.", "lock"),
    (11, "NEW YORK", "CONFIRMED", "Huawei guilty of theft",
     "Guilty of stealing trade secrets in a US trial.", "chip"),
    (12, "BRUSSELS", "SCHEDULED", "EU-Balkans summit opens",
     "EU-Western Balkans summit opens in Brussels today.", "stars"),
    (13, "ACCRA", "SCHEDULED", "Africa summit ends in Accra",
     "German-African summit ends; Steinmeier meets Mahama, then Nairobi.", None),
    (14, "WORLD", "OFFICIAL", "47,000 women killed in 2025",
     "UN: 47,000 women and girls killed by partners or relatives in 2025.", None),
    (15, "STOCKHOLM", "SCHEDULED", "Swedish vote on PM today",
     "Parliament votes on Moderates leader Kristersson staying prime minister.", None),
]

ALSO = [
    (16, "SCHED - Germany Q3 GDP final due 07:00 UTC."),
    (17, "SCHED - US new-home sales Oct, about 645-650K pace."),
    (18, "SCHED - Fed Beige Book 19:00 UTC."),
    (19, "SCHED - UCL Matchday 5 tonight, 9 games: PSG v Roma."),
    (20, "SCHED - Spain snap election Sunday 29 Nov."),
    (21, "SCHED - OPEC+ ministers meet Sunday on output."),
    (22, "REPORTED - Over 700,000 Russian soldiers killed in Ukraine war."),
    (23, "REPORTED - Iran braces for winter gas shortages; rationing."),
    (24, "REPORTED - Kushner: Trump may weigh NATO-like Ukraine guarantees."),
    (25, "REPORTED - NATO plans early-warning aircraft in Poland."),
    (26, "REPORTED - EU announces further sanctions on Russia."),
    (27, "CLAIM - Iran: three tankers hit by mines in Hormuz."),
    (28, "REPORTED - Russia, Ukraine trade accusations at UN."),
    (29, "REPORTED - UN raises concerns over Gaza conditions."),
    (30, "REPORTED - BJP, Akali Dal ally for 2027 Punjab vote."),
    (31, "SCHED - US markets shut Thu; Fri early close 13:00 ET."),
    (32, "SPORT - England beat Australia by 8 wickets, 2nd T20I."),
    (33, "MKT - Wall St rebounds Monday led by Nvidia."),
    (34, "MKT - Dell lifts forecasts after record AI quarter."),
    (35, "MKT - Venezuela public debt $237.5bn."),
    (36, "MKT - Dutch gas benchmark up 8.6% on cold snap."),
]

DATE_CHECK = [
    "19 Nov - GTA 6 released worldwide",
    "23 Nov - COP31 collapses with no deal",
    "20 Nov - Russian attack kills 11 in Kyiv",
    "3 Nov - Man Utd come back 2-0 to beat Roma 3-2",
    "22-23 Nov - Nepal PM ends India visit",
]

SCENES = {
    "chart": scene_chart,
    "ship2": lambda cv, x, y, w, h: scene_ship(cv, x, y, w, h, sinking=True),
    "tower": scene_tower,
    "dunes": scene_dunes,
    "block": scene_block,
    "medal": scene_medal,
    "lock": scene_lock,
    "chip": scene_chip,
    "stars": scene_stars,
}


def draw_masthead(cv):
    cv.text(MX, 16, 2, RED, "WEDNESDAY")
    cv.text(MX, 34, 8, INK, "25 NOVEMBER 2026")
    cv.fill_rect(790, 16, 220, 30, INK)
    cv.text_center(790, 1010, 25, 1, WHITE, "THE WHOLE WORLD - ONE DAY")
    cv.text(836, 52, 1, GREY, "UTC day 2026-11-25")
    cv.fill_rect(MX, 94, RX - MX, 16, RED)
    cv.text_center(MX, RX, 99, 1, WHITE,
                   "36 STORIES - 7 REGIONS - EVERY ONE FROM THIS WEDNESDAY")


def draw_stats(cv):
    cw = (RX - MX) / 8
    for i, (num, lab) in enumerate(STATS):
        x = int(MX + i * cw)
        if i > 0:
            cv.vline(x, 114, 146, (200, 194, 182))
        cv.text(x + 6, 118, 2, NAVY if i % 2 else RED, num)
        cv.text(x + 6, 136, 1, GREY, lab)


def draw_timeline(cv):
    cv.text(MX, 152, 1, RED, "THE DAY IN UTC")
    y = 168
    cv.hline(MX, RX, y, GREY)
    for h in (0, 6, 12, 18, 24):
        tx = int(MX + (h / 24.0) * (RX - MX))
        cv.vline(tx, y - 3, y + 3, INK)
        lab = "%02d:00" % h
        lx = min(max(tx - 14, MX), RX - 29)
        cv.text(lx, y + 6, 1, GREY, lab)
    for (hh, mm, _lab) in TIMELINE_EVENTS:
        tx = int(MX + ((hh + mm / 60.0) / 24.0) * (RX - MX))
        cv.circle(tx, y, 3, RED)
    cv.text(MX, 184, 1, INK,
            "00:18 SHENZHOU LIFTS OFF - 00:30 AU CPI - 01:23 TFS WATCH AND ACT - 07:00 GERMANY GDP FINAL")
    cv.text(MX, 193, 1, INK,
            "13:30 US DATA PILE - 15:00 US HOME SALES - 19:00 BEIGE BOOK - 20:00 UCL NIGHT")


def draw_lead(cv):
    y0, y1 = 200, 360
    scene_rocket(cv, MX, y0, 546, y1 - y0)
    cv.rect(MX, y0, 546, y1 - y0, INK, 1)
    tx = 572
    cv.text(tx, 204, 2, RED, "1 - JIUQUAN, CHINA - ASIA")
    cv.para(tx, 226, 438, 3, INK,
            "Shenzhou-24 lifts off carrying China's first foreign astronaut",
            leading=24)
    cv.para(tx, 306, 438, 1, INK,
            "Long March 2F rose at 00:18 UTC with Tang Hongbo, Wu Yi and "
            "Pakistan's Muhammad Zeeshan Ali, 40, payload specialist. First "
            "Pakistani in orbit; first foreign astronaut on Tiangong. He stays "
            "5-10 days for four science projects.", leading=9)
    cv.fill_rect(tx, 346, 60, 12, GREEN)
    cv.text(tx + 4, 348, 1, WHITE, "CONFIRMED")
    cv.text(tx + 68, 348, 1, INK, "Xinhua / CMSA - 00:18 UTC")


def draw_row_b(cv):
    panels = [
        (MX, scene_fire, "2 - FLINDERS ISLAND, TASMANIA - OCEANIA",
         "Bushfire emergency: 'too late to leave'",
         "Emergency Warning for Killiecrankie, Leeka and Mount Tanner; "
         "lightning-sparked fire, about 3,000 ha.",
         "OFFICIAL - Tas Fire Service"),
        (350, scene_chart, "3 - WASHINGTON, USA - NORTH AMERICA",
         "Thanksgiving-eve data pile: GDP, PCE, claims",
         "13:30 UTC: Q3 GDP about 3.4%, core PCE about 3.2% y/y, "
         "claims about 200K.",
         "FORECAST - BEA / Labor Dept"),
        (686, lambda cv, x, y, w, h: scene_ship(cv, x, y, w, h),
         "4 - GULF OF FINLAND - EUROPE",
         "Zelenskyy confirms Ukraine hit Russian ship",
         "Kyiv claims a Saturday drone strike on a Russian cargo ship; "
         "Norway urges caution.",
         "CONFIRMED"),
    ]
    for (x, fn, kicker, head, deck, tag) in panels:
        y0 = 364
        fn(cv, x, y0, 324, 80)
        cv.rect(x, y0, 324, 160, INK, 1)
        cv.text(x + 6, y0 + 84, 1, RED, kicker)
        cv.para(x + 6, y0 + 96, 312, 2, INK, head, leading=16)
        cv.para(x + 6, y0 + 130, 312, 1, INK, deck, leading=9)
        cv.text(x + 6, y0 + 150, 1, GREY, tag)


def draw_cards(cv):
    col_x = [MX, 265, 516, 767]
    row_y = [528, 603, 678]
    for idx, (num, place, status, head, deck, scene) in enumerate(CARDS):
        x = col_x[idx % 4]
        y = row_y[idx // 4]
        cv.fill_rect(x, y, 243, 70, WHITE)
        cv.rect(x, y, 243, 70, (200, 194, 182), 1)
        if scene is not None:
            SCENES[scene](cv, x + 4, y + 4, 62, 62)
            cv.rect(x + 4, y + 4, 62, 62, (200, 194, 182), 1)
            tx = x + 72
            tw = 167
        else:
            cv.fill_rect(x, y, 243, 4, STATUS_COL[status])
            tx = x + 6
            tw = 231
        cv.text(tx, y + 4, 1, INK, "%d - %s" % (num, place))
        st = status
        cv.text(tx + tw - text_w(st, 1), y + 4, 1, STATUS_COL[status], st)
        cv.para(tx, y + 14, tw, 2, INK, head, leading=16)
        cv.para(tx, y + 46, tw, 1, INK, deck, leading=9)


def draw_also(cv):
    cv.text(MX, 752, 2, RED, "ALSO TODAY")
    cv.text(150, 754, 1, GREY, "numbered briefs 16-36")
    col_x = [MX, 232, 450]
    for ci in range(3):
        x = col_x[ci]
        yy = 774
        for (num, txt) in ALSO[ci * 7:(ci + 1) * 7]:
            lines = wrap_text(txt, 190, 1)
            cv.text(x, yy, 1, RED, str(num))
            ly = yy
            for ln in lines:
                cv.text(x + 18, ly, 1, INK, ln)
                ly += 9
            yy = ly + 4


def draw_right(cv):
    x = 668
    cv.text(x, 752, 2, NAVY, "WHERE")
    cv.text(760, 754, 1, GREY, "pins = story numbers")
    draw_map(cv, x, 770, 342, 102)
    cv.text(x, 876, 1, INK, "Asia 2 - Europe 11 - N. America 10 - Middle East 6")
    cv.text(x, 885, 1, INK, "Oceania 3 - Africa 1 - Lat. America 1 - Global 2")
    cv.text(x, 898, 1, RED, "HOW SURE")
    cv.text(x + 54, 898, 1, INK, "CONFIRMED 2+ outlets - OFFICIAL on the record")
    cv.text(x, 907, 1, INK, "REPORTED one outlet - SCHED calendar - CLAIM 1 side")
    cv.fill_rect(x, 916, 342, 62, LIGHT2)
    cv.rect(x, 916, 342, 62, INK, 1)
    cv.text(x + 4, 920, 1, RED, "DATE CHECK - LEFT OUT, NOT FROM WED 25 NOV 2026:")
    yy = 930
    for item in DATE_CHECK:
        cv.text(x + 4, yy, 1, INK, item)
        yy += 9


def draw_footer(cv):
    cv.hline(MX, RX, 982, GREY)
    cv.text(MX, 988, 1, GREY,
            "SOURCES: Xinhua, CMSA, Tas Fire Service, ABC, BEA, US Labor Dept, "
            "Reuters, UN, UEFA, ABS, Fed - checked vs reports dated 25 Nov 2026.")
    cv.text(MX, 997, 1, GREY,
            "Wires as of about 02:00 UTC, Wednesday 25 November 2026 - 36 stories, 7 regions.")
    cv.text(RX - text_w("Sum 25 - news-image-20261125", 1), 997, 1, GREY,
            "Sum 25 - news-image-20261125")


def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_stats(cv)
    draw_timeline(cv)
    draw_lead(cv)
    draw_row_b(cv)
    draw_cards(cv)
    draw_also(cv)
    draw_right(cv)
    draw_footer(cv)
    return cv


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    data = png_bytes(build())
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
