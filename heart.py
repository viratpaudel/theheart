import math
import random
import turtle

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

SCALE = 14
FONT_FAMILY = "Arial"  # Tk falls back to a font with the right glyphs


def heart_points(scale, steps=240):
    pts = []
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x * scale, y * scale))
    return pts


def inside(poly, px, py):
    """Ray-casting point-in-polygon test."""
    c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            c = not c
        j = i
    return c


def pick_positions(n, poly):
    """Random, well-spaced spots inside the heart."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    spots = []
    min_dist = 70
    fails = 0
    while len(spots) < n:
        x = random.uniform(min(xs), max(xs))
        y = random.uniform(min(ys), max(ys))
        if inside(poly, x, y) and all(math.hypot(x - a, y - b) >= min_dist for a, b in spots):
            spots.append((x, y))
            fails = 0
        else:
            fails += 1
            if fails > 400:  # too crowded -> allow tighter spacing
                min_dist -= 3
                fails = 0
    return spots


def main():
    screen = turtle.Screen()
    screen.setup(820, 820)
    screen.bgcolor("black")
    screen.title("Love in 50 languages")
    screen.tracer(0)

    # Heart outline
    outline = turtle.Turtle(visible=False)
    outline.speed(0)
    outline.pensize(5)
    outline.color("red", "#2b0000")
    full = heart_points(SCALE)
    outline.penup()
    outline.goto(full[0])
    outline.pendown()
    outline.begin_fill()
    for p in full[1:]:
        outline.goto(p)
    outline.end_fill()
    screen.update()

    # Words stay a bit inside the outline
    inner = heart_points(SCALE * 0.85)
    spots = pick_positions(len(WORDS), inner)

    pen = turtle.Turtle(visible=False)   # final, permanent text
    pop = turtle.Turtle(visible=False)   # temporary text for the pop animation
    for t in (pen, pop):
        t.penup()
        t.color("red")

    words = WORDS[:]
    random.shuffle(words)

    def write_at(t, text, x, y, size):
        t.goto(x, y - size * 0.7)
        t.write(text, align="center", font=(FONT_FAMILY, size, "bold"))

    def show_word(i):
        if i >= len(words):
            return
        x, y = spots[i]
        target = random.randint(14, 20)
        # grow, overshoot a little, settle -> "pop"
        sizes = [4, 8, 12, target + 6, target + 3, target]
        state = {"k": 0}

        def step():
            pop.clear()
            write_at(pop, words[i], x, y, sizes[state["k"]])
            screen.update()
            state["k"] += 1
            if state["k"] < len(sizes):
                screen.ontimer(step, 35)
            else:
                pop.clear()
                write_at(pen, words[i], x, y, target)
                screen.update()
                screen.ontimer(lambda: show_word(i + 1), 350)

        step()

    show_word(0)
    screen.mainloop()


if __name__ == "__main__":
    main()
