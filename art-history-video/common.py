"""Shared look, helpers and narration timing for the art history video."""
import json
import types
import random
from pathlib import Path

import numpy as np
from manim import *

HERE = Path(__file__).parent
AUDIO = HERE / "build" / "audio"
ART = HERE / "assets" / "artworks"
CREDITS = json.loads((ART / "credits.json").read_text()) if (ART / "credits.json").exists() else {}

FONT = "CMU Serif"
BG = "#1C1C1C"
C_BLUE = "#58C4DD"
C_YELLOW = "#FFFF00"
C_RED = "#FC6255"
C_GREEN = "#83C167"
C_GOLD = "#E1B54A"
C_OCHRE = "#B5562E"
C_GREY = "#888888"
C_DIM = "#444444"

config.background_color = BG


def T(text, size=36, color=WHITE, **kw):
    return Text(text, font=FONT, font_size=size, color=color, **kw)


def TI(text, size=30, color=WHITE, **kw):
    return Text(text, font=FONT, font_size=size, color=color, slant=ITALIC, **kw)


def para(text, size=30, width=11, color=WHITE):
    """Wrapped paragraph of plain text."""
    words, lines, cur = text.split(), [], ""
    per_line = int(width * 62 / size * 2.1)
    for w in words:
        if len(cur) + len(w) + 1 > per_line and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)


class NarratedScene(Scene):
    """Scene whose beats are timed to pre-rendered narration clips."""

    chapter = "ch00"

    def setup(self):
        path = AUDIO / "durations.json"
        self.durations = json.loads(path.read_text()) if path.exists() else {}
        random.seed(self.chapter)
        np.random.seed(abs(hash(self.chapter)) % 2**32)

    def say(self, beat, *steps):
        """Play narration clip `beat` while running `steps`, then hold until it ends.

        A step is an Animation, a list of Animations (played together), a
        number (seconds to wait) or a callable (run immediately, e.g. self.add).
        """
        key = f"{self.chapter}/{beat}"
        dur = self.durations.get(key, {}).get("duration", 3.0)
        wav = AUDIO / self.chapter / f"{beat}.wav"
        if wav.exists():
            self.add_sound(str(wav))
        t0 = self.renderer.time
        for s in steps:
            if isinstance(s, (int, float)):
                self.wait(s)
            elif isinstance(s, (list, tuple)):
                self.play(*s)
            elif isinstance(s, (types.FunctionType, types.MethodType)):
                s()
            else:
                self.play(s)
        remaining = dur - (self.renderer.time - t0)
        if remaining > 0.02:
            self.wait(remaining)

    def clear_all(self, run_time=0.8, keep=()):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)


def chapter_card(number, title):
    num = T(f"Chapter {number}", 28, C_GREY)
    ttl = T(title, 54)
    line = Line(LEFT, RIGHT, color=C_BLUE).set_width(max(ttl.width, 4))
    return VGroup(num, ttl, line).arrange(DOWN, buff=0.3)


def show_chapter_card(scene, number, title, hold=1.2):
    card = chapter_card(number, title)
    scene.play(FadeIn(card[0], shift=0.2 * UP), Write(card[1]), GrowFromCenter(card[2]), run_time=1.4)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=0.3 * UP), run_time=0.7)


# ----------------------------------------------------------------- dials

SPACE_ENDS = ("flat / symbolic", "illusion of depth")


class Dials(VGroup):
    """The three recurring dials: Space (0..1), Purpose (label), Medium (label)."""

    def __init__(self, space=0.5, purpose="?", medium="?", width=6.0, **kw):
        super().__init__(**kw)
        self.w = width
        rows = []
        for name, color in [("SPACE", C_BLUE), ("PURPOSE", C_YELLOW), ("MEDIUM", C_RED)]:
            label = T(name, 26, color)
            track = Line(ORIGIN, width * RIGHT, color=C_DIM, stroke_width=6)
            label.next_to(track, LEFT, buff=0.4)
            rows.append(VGroup(label, track))
        VGroup(*rows).arrange(DOWN, buff=0.95, aligned_edge=RIGHT)
        self.rows = rows
        ends = VGroup(
            T(SPACE_ENDS[0], 18, C_GREY).next_to(rows[0][1].get_start(), DOWN, buff=0.15),
            T(SPACE_ENDS[1], 18, C_GREY).next_to(rows[0][1].get_end(), DOWN, buff=0.15),
        )
        self.space_val = space
        self.knob = Dot(radius=0.13, color=C_BLUE).move_to(self._space_point(space))
        self.fill_line = Line(rows[0][1].get_start(), self.knob.get_center(), color=C_BLUE, stroke_width=6)
        self.purpose_tag = self._tag(purpose, 1, C_YELLOW)
        self.medium_tag = self._tag(medium, 2, C_RED)
        self.add(*rows, ends, self.fill_line, self.knob, self.purpose_tag, self.medium_tag)

    def _space_point(self, v):
        tr = self.rows[0][1]
        return tr.get_start() + v * (tr.get_end() - tr.get_start())

    def _tag(self, text, row, color, scale=1.0):
        tr = self.rows[row][1]
        t = T(text, 24, color)
        if t.width > self.w * 0.95:
            t.scale_to_fit_width(self.w * 0.95)
        t.scale(scale)
        return t.next_to(tr, UP, buff=0.1 * scale)

    def set_space(self, v, run_time=1.5):
        target = self._space_point(v)
        start = self.rows[0][1].get_start()
        self.space_val = v
        return AnimationGroup(
            self.knob.animate.move_to(target),
            self.fill_line.animate.put_start_and_end_on(start, target + 1e-4 * RIGHT),
            run_time=run_time,
        )

    def set_label(self, which, text):
        old = self.purpose_tag if which == "purpose" else self.medium_tag
        row, color = (1, C_YELLOW) if which == "purpose" else (2, C_RED)
        new = self._tag(text, row, color, scale=self.rows[row][1].get_length() / self.w)
        self.remove(old)
        self.add(new)
        if which == "purpose":
            self.purpose_tag = new
        else:
            self.medium_tag = new
        return FadeTransform(old, new)


def corner_dials(space, purpose, medium):
    d = Dials(space, purpose, medium)
    d.scale(0.5).to_corner(UR, buff=0.3)
    return d


# ----------------------------------------------------------------- artwork cards


def _icon(kind, w, h):
    s = min(w, h)
    if kind == "sculpture":
        base = Rectangle(width=0.5 * s, height=0.12 * s, color=C_GREY).shift(0.36 * h * DOWN)
        body = VGroup(
            Circle(radius=0.09 * s, color=C_GREY).shift(0.22 * h * UP),
            Line(0.13 * h * UP, 0.1 * h * DOWN, color=C_GREY),
            Line(0.1 * h * DOWN, 0.3 * h * DOWN + 0.08 * s * LEFT, color=C_GREY),
            Line(0.1 * h * DOWN, 0.3 * h * DOWN + 0.06 * s * RIGHT, color=C_GREY),
            Line(0.08 * h * UP + 0.14 * s * LEFT, 0.08 * h * UP + 0.14 * s * RIGHT, color=C_GREY),
        )
        return VGroup(base, body)
    if kind == "building":
        cols = VGroup(*[Line(DOWN, UP, color=C_GREY).set_height(0.42 * h).shift(x * s * RIGHT)
                        for x in np.linspace(-0.3, 0.3, 6)])
        roof = Polygon([-0.4 * s, 0.24 * h, 0], [0.4 * s, 0.24 * h, 0], [0, 0.4 * h, 0], color=C_GREY)
        base = Line(0.4 * s * LEFT, 0.4 * s * RIGHT, color=C_GREY).shift(0.22 * h * DOWN)
        return VGroup(cols, roof, base)
    if kind == "book":
        page = Rectangle(width=0.6 * s, height=0.75 * h, color=C_GREY)
        knot = VGroup(*[Circle(radius=r * s, color=C_GOLD, stroke_width=2) for r in (0.08, 0.14, 0.2)])
        return VGroup(page, knot)
    # painting: landscape-ish
    hills = VMobject(color=C_GREY).set_points_smoothly([
        [-0.45 * w, -0.1 * h, 0], [-0.2 * w, 0.05 * h, 0], [0.05 * w, -0.08 * h, 0],
        [0.25 * w, 0.06 * h, 0], [0.45 * w, -0.05 * h, 0]])
    sun = Circle(radius=0.07 * s, color=C_GREY).shift(0.25 * w * RIGHT + 0.25 * h * UP)
    return VGroup(hills, sun)


def art_card(title, artist="", date="", slug=None, motif=None, kind="painting", w=3.8, h=4.2):
    """A framed artwork with a museum-style label.

    Uses assets/artworks/<slug>.jpg|png if present (public-domain image you
    add yourself); otherwise a vector `motif`, otherwise a generic icon.
    """
    frame = Rectangle(width=w, height=h, stroke_color=C_GOLD, stroke_width=3)
    inner = Rectangle(width=w - 0.16, height=h - 0.16, stroke_color=C_DIM, stroke_width=1,
                      fill_color="#151515", fill_opacity=1)
    content = None
    if slug:
        for ext in ("jpg", "jpeg", "png"):
            p = ART / f"{slug}.{ext}"
            if p.exists():
                img = ImageMobject(str(p))
                img.scale_to_fit_height(h - 0.2)
                if img.width > 1.7 * w:  # let landscape images run wider than the default box
                    img.scale_to_fit_width(1.7 * w)
                frame = Rectangle(width=img.width + 0.16, height=img.height + 0.16,
                                  stroke_color=C_GOLD, stroke_width=3)
                inner = Rectangle(width=img.width, height=img.height, stroke_width=0)
                content = img
                meta = CREDITS.get(slug)
                if meta:  # caption must describe the object actually shown
                    title, artist, date = meta["title"], meta["artist"], meta["date"] + "  ·  The Met"
                break
    if content is None:
        content = motif if motif is not None else _icon(kind, w - 0.3, h - 0.3)
        if content.width > w - 0.3:
            content.scale_to_fit_width(w - 0.3)
        if content.height > h - 0.3:
            content.scale_to_fit_height(h - 0.3)
    content.move_to(inner)
    label = VGroup(TI(title, 22))
    if artist or date:
        label.add(T(", ".join(x for x in (artist, date) if x), 18, C_GREY))
    label.arrange(DOWN, buff=0.08)
    for m in label:
        if m.width > w + 1.2:
            m.scale_to_fit_width(w + 1.2)
    label.next_to(frame, DOWN, buff=0.18)
    if isinstance(content, ImageMobject):
        return Group(inner, content, frame, label)
    return VGroup(inner, content, frame, label)


def card_row(*cards, buff=0.6):
    g = Group(*cards).arrange(RIGHT, buff=buff, aligned_edge=UP)
    if g.width > 13:
        g.scale_to_fit_width(13)
    return g


def show_cards(*cards):
    return [FadeIn(c, shift=0.2 * UP) for c in cards]


# ----------------------------------------------------------------- motifs


def hand_stencil(color=C_OCHRE, n=1800):
    """Sprayed-pigment halo around a hand silhouette, like Paleolithic stencils."""
    fingers = [((-0.45, -0.35), (-1.05, 0.25), 0.16), ((-0.35, 0.3), (-0.5, 1.35), 0.14),
               ((-0.1, 0.4), (-0.1, 1.55), 0.14), ((0.17, 0.38), (0.3, 1.4), 0.14), ((0.4, 0.25), (0.65, 1.05), 0.12)]

    def in_hand(x, y):
        if (x / 0.55) ** 2 + ((y + 0.3) / 0.7) ** 2 < 1 or (-0.4 < x < 0.4 and -1.7 < y < -0.8):
            return True
        for (ax, ay), (bx, by), r in fingers:
            dx, dy = bx - ax, by - ay
            t = np.clip(((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy), 0, 1)
            if (x - ax - t * dx) ** 2 + (y - ay - t * dy) ** 2 < r * r:
                return True
        return False

    rng = np.random.default_rng(3)
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-3.2, 3.2), rng.uniform(-3.0, 3.2)
        if in_hand(x, y):
            continue
        if rng.random() < np.exp(-(x * x + (y - 0.1) ** 2) / (2 * 0.95 ** 2)):
            pts.append([x, y, 0])
    return VGroup(*[Dot(p, radius=0.024, color=color, fill_opacity=0.45 + 0.5 * rng.random()) for p in pts])


def crosshatch_ochre():
    block = RoundedRectangle(corner_radius=0.3, width=3.2, height=1.1, fill_color=C_OCHRE,
                             fill_opacity=1, stroke_width=0)
    lines = VGroup()
    for x in np.linspace(-1.2, 1.0, 7):
        lines.add(Line([x, -0.4, 0], [x + 0.35, 0.4, 0]))
        lines.add(Line([x + 0.35, -0.4, 0], [x, 0.4, 0]))
    lines.add(Line([-1.35, 0.05, 0], [1.4, 0.05, 0]), Line([-1.35, 0.35, 0], [1.4, 0.35, 0]),
              Line([-1.35, -0.3, 0], [1.4, -0.3, 0]))
    lines.set_stroke("#F4D3B5", 2.5)
    return VGroup(block, lines)


def mondrian(w=3, h=3):
    """After Composition with Red, Blue and Yellow (1930): fractions measured from bottom-left."""
    bg = Rectangle(width=w, height=h, fill_color="#F2F0E6", fill_opacity=1, stroke_width=0)
    g = VGroup(bg)

    def at(x, y):
        return np.array([(x - 0.5) * w, (y - 0.5) * h, 0])

    for (x0, x1), (y0, y1), c in [((0.3, 1), (0.3, 1), C_RED), ((0, 0.3), (0, 0.3), "#2D5DBE"),
                                  ((0.9, 1), (0, 0.15), C_YELLOW)]:
        g.add(Rectangle(width=(x1 - x0) * w, height=(y1 - y0) * h, fill_color=c, fill_opacity=1,
                        stroke_width=0).move_to(at((x0 + x1) / 2, (y0 + y1) / 2)))
    for p, q in [((0.3, 0), (0.3, 1)), ((0, 0.3), (1, 0.3)), ((0, 0.65), (0.3, 0.65)),
                 ((0.9, 0), (0.9, 0.3)), ((0.9, 0.15), (1, 0.15))]:
        g.add(Line(at(*p), at(*q), color=BLACK, stroke_width=10))
    return g


def black_square():
    return VGroup(Rectangle(width=2.6, height=2.6, fill_color="#EDE6D6", fill_opacity=1, stroke_width=0),
                  Square(1.9, fill_color=BLACK, fill_opacity=1, stroke_width=0))


def great_wave():
    wave = VMobject(stroke_color="#2D5DBE", stroke_width=5).set_points_smoothly([
        [-1.3, -0.9, 0], [-0.9, -0.2, 0], [-0.4, 0.6, 0], [0.2, 0.9, 0], [0.6, 0.7, 0], [0.7, 0.35, 0], [0.45, 0.3, 0]])
    foam = VGroup(*[Circle(radius=0.06, color=WHITE, stroke_width=2).move_to([0.1 + 0.18 * i, 0.82 - 0.12 * i ** 1.4, 0])
                    for i in range(4)])
    fuji = Polygon([0.4, -0.8, 0], [0.9, -0.3, 0], [1.4, -0.8, 0], stroke_color=WHITE, stroke_width=2)
    sea = VMobject(stroke_color="#2D5DBE", stroke_width=3).set_points_smoothly(
        [[-1.4, -0.9, 0], [-0.5, -0.75, 0], [0.4, -0.95, 0], [1.4, -0.85, 0]])
    return VGroup(sea, fuji, wave, foam)


def starry_night():
    swirls = VGroup(*[
        ParametricFunction(lambda t, c=c, r=r: np.array([c[0] + r * t / 6 * np.cos(t), c[1] + r * t / 6 * np.sin(t), 0]),
                           t_range=[0, 6], color=C_YELLOW if i % 2 else C_BLUE, stroke_width=3)
        for i, (c, r) in enumerate([((-0.6, 0.4), 0.45), ((0.3, 0.6), 0.35), ((0.9, 0.2), 0.25)])])
    moon = Circle(radius=0.22, color=C_YELLOW, fill_opacity=0.8).move_to([1.0, 0.85, 0])
    cypress = Polygon([-1.1, -1.1, 0], [-0.75, 0.9, 0], [-0.55, -1.1, 0], fill_color="#1F3B2A", fill_opacity=1,
                      stroke_color="#0E2016")
    town = VGroup(*[Rectangle(width=0.18, height=0.15 + 0.1 * (i % 3), fill_color="#334", fill_opacity=1,
                              stroke_width=1).move_to([-0.3 + 0.22 * i, -0.95, 0]) for i in range(7)])
    return VGroup(swirls, moon, town, cypress)


def soup_can():
    body = Rectangle(width=1.4, height=2.0, stroke_color=WHITE, fill_color="#EEEEEE", fill_opacity=1)
    top = Rectangle(width=1.4, height=0.95, fill_color="#C8102E", fill_opacity=1, stroke_width=0).align_to(body, UP)
    word = T("SOUP", 22, "#C8102E").move_to(body.get_center() + 0.45 * DOWN)
    name = TI("Campbell's", 18, WHITE).move_to(top)
    return VGroup(body, top, word, name)


def pipe():
    bowl = Polygon([-0.2, 0, 0], [0.25, 0, 0], [0.2, -0.65, 0], [-0.15, -0.65, 0],
                   fill_color="#6B3E1F", fill_opacity=1, stroke_width=0)
    stem = VMobject(stroke_color="#2A1A10", stroke_width=12).set_points_smoothly(
        [[0.2, -0.45, 0], [0.8, -0.35, 0], [1.4, -0.1, 0]])
    cap = TI("Ceci n'est pas une pipe.", 18, BLACK).shift(1.0 * DOWN + 0.4 * RIGHT)
    bg = Rectangle(width=2.6, height=2.2, fill_color="#E8DFC8", fill_opacity=1, stroke_width=0).shift(0.4 * RIGHT + 0.4 * DOWN)
    return VGroup(bg, stem, bowl, cap)


def drips(n=26, seed=4):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        pts = [np.array([*rng.uniform(-1.3, 1.3, 2), 0]) for _ in range(6)]
        c = [WHITE, BLACK, "#C9A86A", "#7A8A99"][i % 4]
        g.add(VMobject(stroke_color=c, stroke_width=rng.uniform(1, 4)).set_points_smoothly(pts))
    bg = Rectangle(width=2.8, height=2.8, fill_color="#B8A98C", fill_opacity=1, stroke_width=0)
    return VGroup(bg, g)


def rothko():
    bg = Rectangle(width=2.2, height=3.0, fill_color="#5A1E1E", fill_opacity=1, stroke_width=0)
    a = RoundedRectangle(corner_radius=0.1, width=1.8, height=1.3, fill_color="#C2452D", fill_opacity=0.9,
                         stroke_width=0).shift(0.65 * UP)
    b = RoundedRectangle(corner_radius=0.1, width=1.8, height=1.0, fill_color="#E08A2E", fill_opacity=0.85,
                         stroke_width=0).shift(0.8 * DOWN)
    return VGroup(bg, a, b)


def heart_balloon():
    heart = VMobject(fill_color=C_RED, fill_opacity=1, stroke_width=0).set_points_smoothly([
        [0, -0.5, 0], [-0.45, 0, 0], [-0.3, 0.4, 0], [0, 0.25, 0], [0.3, 0.4, 0], [0.45, 0, 0], [0, -0.5, 0]])
    string = Line([0, -0.5, 0], [-0.4, -1.4, 0], color=WHITE, stroke_width=2)
    return VGroup(string, heart)


def golden_rect(width=3.0):
    phi = (1 + 5 ** 0.5) / 2
    r = Rectangle(width=width, height=width / phi, color=C_YELLOW)
    g = VGroup(r)
    x0, y0, w, h = -width / 2, -width / phi / 2, width, width / phi
    for i in range(5):
        if i % 2 == 0:
            g.add(Line([x0 + h, y0, 0], [x0 + h, y0 + h, 0], color=C_YELLOW, stroke_width=2))
            x0, w = x0 + h, w - h
        else:
            g.add(Line([x0, y0 + h - w, 0], [x0 + w, y0 + h - w, 0], color=C_YELLOW, stroke_width=2))
            h = h - w
    return g


def parthenon(width=4.0):
    cols = VGroup(*[Rectangle(width=0.16, height=1.5, fill_color="#D8D2C2", fill_opacity=1, stroke_width=0)
                    .move_to([x, 0, 0]) for x in np.linspace(-1.7, 1.7, 8)])
    stylobate = Rectangle(width=4.0, height=0.2, fill_color="#C9C2B0", fill_opacity=1, stroke_width=0).shift(0.85 * DOWN)
    step2 = Rectangle(width=4.3, height=0.2, fill_color="#B9B2A0", fill_opacity=1, stroke_width=0).shift(1.05 * DOWN)
    entab = Rectangle(width=4.0, height=0.35, fill_color="#C9C2B0", fill_opacity=1, stroke_width=0).shift(0.92 * UP)
    pedi = Polygon([-2.0, 1.1, 0], [2.0, 1.1, 0], [0, 1.6, 0], fill_color="#D8D2C2", fill_opacity=1, stroke_width=0)
    g = VGroup(step2, stylobate, cols, entab, pedi)
    return g.scale_to_fit_width(width)
