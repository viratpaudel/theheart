import argparse
import math
import random
import turtle
import tkinter.font as tkfont

# "Love" in 50 language
WORDS = [
    "love", "amor", "amour", "Liebe", "amore", "liefde", "kärlek",
    "kjærlighet", "kærlighed", "rakkaus", "miłość", "láska", "любовь",
    "любов", "αγάπη", "aşk", "אהבה", "حب", "عشق", "प्यार", "ভালোবাসা",
    "محبت", "माया", "காதல்", "ప్రేమ", "प्रेम", "ความรัก", "tình yêu",
    "cinta", "pag-ibig", "愛", "사랑", "爱", "upendo", "uthando", "ìfẹ́",
    "soyayya", "ፍቅር", "szerelem", "dragoste", "љубав", "ljubav", "meilė",
    "mīlestība", "armastus", "grá", "cariad", "ást", "amo", "aroha",
]

SCALE = 46
FONT_FAMILY = "Georgia"
FONT_STYLE = "italic"
MAX_FONT_SIZE = 34
MIN_FONT_SIZE = 22

# Color palettes: (background, text_color)
PALETTES = [
    ("black", "#ff4f91"),    # Classic pink on black
    ("black", "#ff6b6b"),    # Coral on black
    ("#1a0a2e", "#e040fb"),  # Purple neon
    ("#0d1b2a", "#00d4ff"),  # Cyan on dark navy
    ("#1b0000", "#ff2222"),  # Deep red
]


def heart_points(scale, steps=240):
    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x * scale, y * scale))
    return pts


def outline_positions(words, poly, screen):
    """Fit words edge-to-edge around the outline using their rendered widths."""
    if not poly:
        return [], MAX_FONT_SIZE

    lengths = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        lengths.append(math.hypot(x2 - x1, y2 - y1))

    total = sum(lengths)
    font = tkfont.Font(root=screen.getcanvas(), family=FONT_FAMILY, size=MAX_FONT_SIZE, slant=FONT_STYLE)

    def point_at(distance):
        distance %= total
        traversed = 0.0
        for idx, seg_len in enumerate(lengths):
            if distance <= traversed + seg_len:
                x1, y1 = poly[idx]
                x2, y2 = poly[(idx + 1) % len(poly)]
                ratio = 0.0 if seg_len == 0 else (distance - traversed) / seg_len
                return x1 + (x2 - x1) * ratio, y1 + (y2 - y1) * ratio
            traversed += seg_len
        return poly[0]

    for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -1):
        font.configure(size=size)
        widths = [font.measure(word) for word in words]
        gap = 1
        if sum(widths) + gap * len(words) <= total:
            break
    else:
        font.configure(size=MIN_FONT_SIZE)
        widths = [font.measure(word) for word in words]
        gap = 0
        if sum(widths) > total:
            raise ValueError("The words do not fit around the heart outline at the minimum font size.")
        size = MIN_FONT_SIZE

    distance = random.random() * total
    spots = []
    angles = []
    for width in widths:
        middle = distance + width / 2
        x, y = point_at(middle)
        before_x, before_y = point_at(middle - 2)
        after_x, after_y = point_at(middle + 2)
        spots.append((x, y))
        angles.append(math.degrees(math.atan2(after_y - before_y, after_x - before_x)))
        distance += width + gap
    return spots, size, angles


def main():
    parser = argparse.ArgumentParser(description="Love in 50 languages — heart animation")
    parser.add_argument("--palette", type=int, default=None,
                        help=f"Color palette index (0-{len(PALETTES)-1}). Random if omitted.")
    args = parser.parse_args()

    if args.palette is not None:
        bg_color, text_color = PALETTES[args.palette % len(PALETTES)]
    else:
        bg_color, text_color = random.choice(PALETTES)

    screen = turtle.Screen()
    screen.setup(1800, 1800)
    screen.bgcolor(bg_color)
    screen.title("Love in 50 languages")
    screen.tracer(0)

    # Build the heart only from the words themselves.
    full = heart_points(SCALE)

    pen = turtle.Turtle(visible=False)   # final, permanent text
    pop = turtle.Turtle(visible=False)   # temporary text for the pop animation
    for t in (pen, pop):
        t.penup()
        t.color(text_color)

    words = WORDS[:]
    random.shuffle(words)
    spots, text_size, angles = outline_positions(words, full, screen)

    def write_at(t, text, x, y, size, angle):
        t.setheading(angle)
        t.goto(x, y)
        t.write(text, align="center", font=(FONT_FAMILY, max(1, round(size)), FONT_STYLE))

    def show_word(i):
        if i >= len(words):
            return
        x, y = spots[i]
        angle = angles[i]
        size = text_size
        steps = 24

        def step(frame):
            if frame > steps:
                pop.clear()
                write_at(pen, words[i], x, y, size, angle)
                screen.update()
                screen.ontimer(lambda: show_word(i + 1), 140)
                return

            eased = 1 - (1 - frame / steps) ** 3
            px_size = 1 + (size - 1) * eased
            pop.clear()
            write_at(pop, words[i], x, y, px_size, angle)
            screen.update()
            screen.ontimer(lambda: step(frame + 1), 16)

        step(0)

    show_word(0)
    screen.mainloop()


if __name__ == "__main__":
    main()
