import argparse
import math
import os
import random
import turtle
import tkinter.font as tkfont

# "Love" in 50 languages
WORDS = [
    "love", "amor", "amour", "Liebe", "amore", "liefde", "kärlek",
    "kjærlighet", "kærlighed", "rakkaus", "miłość", "láska", "любовь",
    "любов", "αγάπη", "aşk", "אהבה", "حب", "عشق", "प्यार", "ভালোবাসা",
    "محبت", "माया", "காதல்", "ప్రేమ", "प्रेम", "ความรัก", "tình yêu",
    "cinta", "pag-ibig", "愛", "사랑", "爱", "upendo", "uthando", "ìfẹ́",
    "soyayya", "ፍቅር", "szerelem", "dragoste", "љубав", "ljubav", "meilė",
    "mīlestība", "armastus", "grá", "cariad", "ást", "amo", "aroha",
]

LANGUAGE_GROUPS = {
    "romance": ["amor", "amour", "amore", "dragoste", "amo"],
    "germanic": ["love", "Liebe", "liefde", "kärlek", "kjærlighet", "kærlighed", "ást"],
    "slavic": ["miłość", "láska", "любовь", "любов", "љубав", "ljubav"],
    "asian": ["愛", "사랑", "爱", "ความรัก", "tình yêu", "cinta", "pag-ibig", "aroha"],
    "indic": ["प्यार", "ভালোবাসা", "محبت", "माया", "காதல்", "ప్రేమ", "प्रेम"],
    "african": ["upendo", "uthando", "ìfẹ́", "soyayya", "ፍቅር"],
    "semitic": ["אהבה", "حب", "عشق"],
    "finno-ugric": ["rakkaus", "szerelem", "armastus"],
    "baltic": ["meilė", "mīlestība"],
    "celtic": ["grá", "cariad"],
}


def resolve_word_list(words_arg=None, family_arg=None):
    """Resolve word collection based on CLI overrides or language family filters."""
    if words_arg:
        if os.path.exists(words_arg):
            with open(words_arg, "r", encoding="utf-8") as f:
                loaded = [w.strip() for w in f.read().splitlines() if w.strip()]
        else:
            loaded = [w.strip() for w in words_arg.split(",") if w.strip()]
        if loaded:
            result = loaded[:]
            while len(result) < 40:
                result.extend(loaded)
            return result[:50]

    if family_arg and family_arg in LANGUAGE_GROUPS:
        subset = LANGUAGE_GROUPS[family_arg]
        result = subset[:]
        while len(result) < 40:
            result.extend(subset)
        return result[:50]

    return WORDS[:]

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


def generate_sparkle_points(poly, count=40, jitter=35, rng=None):
    """Generate ambient sparkle coordinates radiating along the heart contour."""
    if not poly or count <= 0:
        return []
    if rng is None:
        rng = random.Random()
    sparkles = []
    poly_len = len(poly)
    for _ in range(count):
        idx = rng.randint(0, poly_len - 1)
        base_x, base_y = poly[idx]
        offset_dist = rng.uniform(8, jitter)
        angle = rng.uniform(0, 2 * math.pi)
        sx = base_x + offset_dist * math.cos(angle)
        sy = base_y + offset_dist * math.sin(angle)
        sparkles.append((sx, sy, rng.choice(["✦", "•", "✨", "*"]), rng.randint(8, 14)))
    return sparkles


def compute_pulse_scale(t_phase):
    """Simulate a cardiac lub-dub waveform for rhythmic pulsation (0.0 <= t_phase < 1.0)."""
    t = t_phase % 1.0
    if t < 0.2:
        return 1.0 + 0.15 * math.sin(t / 0.2 * math.pi)
    elif 0.25 <= t < 0.45:
        return 1.0 + 0.09 * math.sin((t - 0.25) / 0.2 * math.pi)
    return 1.0


def outline_positions_headless(words, poly, font_size=26):
    """Headless word positioning without GUI/Tkinter dependencies."""
    if not poly:
        return [], font_size, []
    lengths = []
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        lengths.append(math.hypot(x2 - x1, y2 - y1))
    total = sum(lengths)

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

    widths = [max(18, len(word) * (font_size * 0.58)) for word in words]
    distance = 0.0
    spots = []
    angles = []
    gap = 2
    for width in widths:
        middle = distance + width / 2
        x, y = point_at(middle)
        before_x, before_y = point_at(middle - 2)
        after_x, after_y = point_at(middle + 2)
        spots.append((x, y))
        angles.append(math.degrees(math.atan2(after_y - before_y, after_x - before_x)))
        distance += width + gap
    return spots, font_size, angles


def render_to_svg(words, scale, bg_color, text_color, message=None, include_sparkles=False):
    """Render heart graphic and words into an SVG vector string."""
    width, height = 1600, 1600
    cx, cy = width / 2, height / 2
    poly = heart_points(scale)
    spots, size, angles = outline_positions_headless(words, poly, font_size=26)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        f'  <rect width="100%" height="100%" fill="{bg_color}" />',
        f'  <g transform="translate({cx}, {cy}) scale(1, -1)">',
    ]

    if include_sparkles:
        sparkle_pts = generate_sparkle_points(poly, count=45, jitter=45)
        for sx, sy, sym, sz in sparkle_pts:
            svg_parts.append(
                f'    <text x="{sx:.1f}" y="{sy:.1f}" fill="{text_color}" opacity="0.6" '
                f'font-family="{FONT_FAMILY}" font-size="{sz}" text-anchor="middle">{sym}</text>'
            )

    for word, (x, y), angle in zip(words, spots, angles):
        clean_word = word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(
            f'    <text transform="translate({x:.2f}, {y:.2f}) rotate({angle:.2f})" '
            f'fill="{text_color}" font-family="{FONT_FAMILY}" font-style="italic" '
            f'font-size="{size}" text-anchor="middle" dominant-baseline="central">{clean_word}</text>'
        )

    if message:
        clean_msg = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(
            f'    <text x="0" y="15" fill="{text_color}" font-family="{FONT_FAMILY}" '
            f'font-size="32" font-weight="bold" text-anchor="middle" dominant-baseline="central">{clean_msg}</text>'
        )

    svg_parts.append('  </g>')
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


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
    parser.add_argument("--speed", choices=["slow", "normal", "fast", "instant"], default="normal",
                        help="Animation playback speed (slow, normal, fast, instant)")
    parser.add_argument("--scale", type=float, default=1.0,
                        help="Scale multiplier for heart outline (0.5 to 2.0, default 1.0)")
    parser.add_argument("--message", type=str, default=None,
                        help="Optional message or dedication displayed in the center of the heart")
    parser.add_argument("--sparkles", action="store_true",
                        help="Render twinkling ambient particle sparkles around the heart perimeter")
    parser.add_argument("--pulse", action="store_true",
                        help="Enable continuous rhythmic cardiac lub-dub pulsing animation")
    parser.add_argument("--words", type=str, default=None,
                        help="Custom comma-separated words or path to text file")
    parser.add_argument("--family", choices=["all"] + list(LANGUAGE_GROUPS.keys()), default="all",
                        help="Filter word list by linguistic family")
    parser.add_argument("--export-svg", type=str, default=None,
                        help="Export high-resolution vector SVG to specified file path and exit")
    args = parser.parse_args()

    scale = int(SCALE * max(0.5, min(args.scale, 2.0)))
    speed_delays = {
        "slow": (220, 24),
        "normal": (140, 16),
        "fast": (60, 8),
        "instant": (0, 0),
    }
    word_delay, frame_delay = speed_delays[args.speed]

    if args.palette is not None:
        bg_color, text_color = PALETTES[args.palette % len(PALETTES)]
    else:
        bg_color, text_color = random.choice(PALETTES)

    if args.export_svg:
        words = resolve_word_list(args.words, args.family)
        random.shuffle(words)
        svg_content = render_to_svg(
            words=words,
            scale=scale,
            bg_color=bg_color,
            text_color=text_color,
            message=args.message,
            include_sparkles=args.sparkles,
        )
        with open(args.export_svg, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Exported heart vector graphics to {args.export_svg}")
        return

    screen = turtle.Screen()
    screen.setup(1800, 1800)
    screen.bgcolor(bg_color)
    screen.title("Love in 50 languages (Press Esc or Q to exit)")
    screen.tracer(0)

    def close_app(*_):
        try:
            screen.bye()
        except turtle.Terminator:
            pass

    screen.listen()
    screen.onkey(close_app, "Escape")
    screen.onkey(close_app, "q")
    screen.onkey(close_app, "Q")
    screen.onscreenclick(close_app)

    # Build the heart only from the words themselves.
    full = heart_points(scale)

    if args.sparkles:
        sparkle_pen = turtle.Turtle(visible=False)
        sparkle_pen.penup()
        sparkle_pen.color(text_color)
        sparkle_pts = generate_sparkle_points(full, count=36, jitter=40)
        for sx, sy, sym, sz in sparkle_pts:
            sparkle_pen.goto(sx, sy)
            sparkle_pen.write(sym, align="center", font=(FONT_FAMILY, sz, "normal"))

    pen = turtle.Turtle(visible=False)   # final, permanent text
    pop = turtle.Turtle(visible=False)   # temporary text for the pop animation
    for t in (pen, pop):
        t.penup()
        t.color(text_color)

    words = resolve_word_list(args.words, args.family)
    random.shuffle(words)
    spots, text_size, angles = outline_positions(words, full, screen)

    def write_at(t, text, x, y, size, angle):
        t.setheading(angle)
        t.goto(x, y)
        t.write(text, align="center", font=(FONT_FAMILY, max(1, round(size)), FONT_STYLE))

    def show_word(i):
        if i >= len(words):
            msg_pen = turtle.Turtle(visible=False)
            msg_pen.penup()
            msg_pen.color(text_color)
            center_text = args.message if args.message else "♥"
            base_msg_size = max(18, int(26 * (scale / SCALE))) if args.message else max(24, int(34 * (scale / SCALE)))

            def draw_center(scale_multiplier):
                try:
                    msg_pen.clear()
                    msg_pen.goto(0, -15 if args.message else -20)
                    msg_pen.write(
                        center_text,
                        align="center",
                        font=(FONT_FAMILY, max(1, int(base_msg_size * scale_multiplier)), "bold")
                    )
                    screen.update()
                except turtle.Terminator:
                    return

            draw_center(1.0)

            if args.pulse:
                pulse_step = [0]
                def run_pulse():
                    try:
                        pulse_step[0] = (pulse_step[0] + 1) % 40
                        factor = compute_pulse_scale(pulse_step[0] / 40.0)
                        draw_center(factor)
                        screen.ontimer(run_pulse, 35)
                    except turtle.Terminator:
                        return
                screen.ontimer(run_pulse, 200)
            return
        x, y = spots[i]
        angle = angles[i]
        size = text_size

        if args.speed == "instant":
            write_at(pen, words[i], x, y, size, angle)
            screen.update()
            show_word(i + 1)
            return

        steps = 24

        def step(frame):
            try:
                if frame > steps:
                    pop.clear()
                    write_at(pen, words[i], x, y, size, angle)
                    screen.update()
                    screen.ontimer(lambda: show_word(i + 1), word_delay)
                    return

                eased = 1 - (1 - frame / steps) ** 3
                px_size = 1 + (size - 1) * eased
                pop.clear()
                write_at(pop, words[i], x, y, px_size, angle)
                screen.update()
                screen.ontimer(lambda: step(frame + 1), frame_delay)
            except turtle.Terminator:
                return

        step(0)

    show_word(0)
    screen.mainloop()


if __name__ == "__main__":
    main()
