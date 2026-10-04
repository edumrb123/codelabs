"""Manim scenes, one per chapter. Render with ./build.sh (or manim -qm scenes.py Ch05)."""
from common import *


# ===================================================================== helpers


def oblique_cube(size=2.0, depth=0.8, color=C_BLUE):
    s, d = size, depth * np.array([1, 0.6, 0])
    f = Square(s, color=color)
    b = f.copy().shift(d)
    edges = VGroup(*[Line(f.get_corner(c), b.get_corner(c), color=color) for c in (UL, UR, DL, DR)])
    return VGroup(f, b, edges)


def egypt_figure(color=C_GOLD, scale=1.0):
    head = Circle(radius=0.32, color=color).shift(2.1 * UP)
    nose = Polygon([0.3, 2.15, 0], [0.48, 2.02, 0], [0.3, 1.97, 0], color=color)
    eye = VGroup(Ellipse(width=0.24, height=0.1, color=WHITE), Dot(radius=0.035, color=WHITE)).move_to([0.1, 2.15, 0])
    neck = Line([0, 1.78, 0], [0, 1.6, 0], color=color)
    shoulders = Polygon([-0.75, 1.6, 0], [0.75, 1.6, 0], [0.35, 0.3, 0], [-0.35, 0.3, 0], color=color)
    arm_l = Line([-0.75, 1.6, 0], [-0.85, 0.4, 0], color=color)
    arm_r = Line([0.75, 1.6, 0], [1.25, 0.6, 0], color=color)
    kilt = Polygon([-0.4, 0.3, 0], [0.45, 0.3, 0], [0.6, -0.4, 0], [-0.45, -0.4, 0], color=color)
    leg_back = VGroup(Line([-0.2, -0.4, 0], [-0.35, -2.0, 0], color=color), Line([-0.35, -2.0, 0], [0.0, -2.0, 0], color=color))
    leg_front = VGroup(Line([0.25, -0.4, 0], [0.75, -2.0, 0], color=color), Line([0.75, -2.0, 0], [1.1, -2.0, 0], color=color))
    parts = {
        "head": VGroup(head, nose), "eye": eye, "torso": VGroup(neck, shoulders, arm_l, arm_r),
        "legs": VGroup(kilt, leg_back, leg_front),
    }
    g = VGroup(*parts.values()).scale(scale)
    g.parts = parts
    return g


def stick_body(contra=0.0, color=WHITE):
    """Standing figure; contra in [0,1] blends from kouros to contrapposto."""
    hip_tilt, sh_tilt = 0.28 * contra, -0.22 * contra
    hip_c = np.array([0.12 * contra, -0.2, 0])
    sh_c = np.array([-0.05 * contra, 1.5, 0])
    hip_l = hip_c + 0.5 * np.array([-np.cos(hip_tilt), -np.sin(hip_tilt), 0])
    hip_r = hip_c + 0.5 * np.array([np.cos(hip_tilt), np.sin(hip_tilt), 0])
    sh_l = sh_c + 0.85 * np.array([-np.cos(sh_tilt), -np.sin(sh_tilt), 0])
    sh_r = sh_c + 0.85 * np.array([np.cos(sh_tilt), np.sin(sh_tilt), 0])
    foot_r = np.array([0.55 - 0.05 * contra, -2.7, 0])  # weight leg
    knee_l = hip_l + np.array([-0.05 + 0.25 * contra, -1.2, 0])
    foot_l = np.array([-0.45 + 0.05 * contra, -2.6 + 0.15 * contra, 0])
    spine = VMobject(color=color).set_points_smoothly([hip_c, (hip_c + sh_c) / 2 + np.array([0.12 * contra, 0, 0]), sh_c])
    head = Circle(radius=0.38, color=color).move_to(sh_c + np.array([0.08 * contra, 0.75, 0]))
    body = VGroup(
        spine, head,
        Line(hip_r, foot_r, color=color), VGroup(Line(hip_l, knee_l, color=color), Line(knee_l, foot_l, color=color)),
        Line(sh_l, sh_l + np.array([-0.15, -1.4, 0]), color=color), Line(sh_r, sh_r + np.array([0.1, -1.4, 0]), color=color),
    )
    hip_line = DashedLine(hip_l + (hip_l - hip_r) * 0.4, hip_r + (hip_r - hip_l) * 0.4, color=C_YELLOW)
    sh_line = DashedLine(sh_l + (sh_l - sh_r) * 0.25, sh_r + (sh_r - sh_l) * 0.25, color=C_BLUE)
    return body, hip_line, sh_line


def robed_figure(color=C_RED):
    halo = Circle(radius=0.55, fill_color=C_GOLD, fill_opacity=0.0, stroke_color="#FFF2B0", stroke_width=4).shift(1.55 * UP)
    head = Circle(radius=0.32, fill_color="#D9B38C", fill_opacity=1, stroke_width=0).shift(1.5 * UP)
    robe = Polygon([-0.25, 1.15, 0], [0.25, 1.15, 0], [0.9, -1.8, 0], [-0.9, -1.8, 0],
                   fill_color=color, fill_opacity=1, stroke_width=0)
    mantle = Polygon([-0.25, 1.15, 0], [0.6, 0.6, 0], [0.2, -1.8, 0], [-0.5, -1.8, 0],
                     fill_color="#2D5DBE", fill_opacity=1, stroke_width=0)
    return VGroup(halo, robe, mantle, head)


def rose_window():
    g = VGroup()
    cols = [C_RED, "#2D5DBE", C_GOLD, C_GREEN]
    for ring, (r0, r1, n) in enumerate([(0.0, 0.35, 1), (0.35, 0.8, 8), (0.8, 1.2, 16)]):
        for i in range(n):
            if n == 1:
                g.add(Circle(radius=r1, fill_color=C_GOLD, fill_opacity=0.9, stroke_color=BLACK))
            else:
                g.add(AnnularSector(inner_radius=r0, outer_radius=r1, angle=TAU / n, start_angle=i * TAU / n,
                                    fill_color=cols[(i + ring) % 4], fill_opacity=0.85, stroke_color=BLACK, stroke_width=2))
    return g


def star_tile(size=1.0, color=C_GOLD):
    a = Square(size, color=color, stroke_width=3)
    b = a.copy().rotate(PI / 4)
    return VGroup(a, b)


def tree(depth=6, color="#8B6B4A"):
    g = VGroup()

    def branch(p, ang, length, d):
        q = p + length * np.array([np.cos(ang), np.sin(ang), 0])
        g.add(Line(p, q, color=color if d > 2 else C_GREEN, stroke_width=1.5 + d))
        if d > 0:
            branch(q, ang + 0.45, length * 0.72, d - 1)
            branch(q, ang - 0.38, length * 0.7, d - 1)

    branch(np.array([0, -2, 0]), PI / 2, 1.3, depth)
    return g


def curvy_tree():
    g = VGroup()
    for k in range(9):
        y = -1.6 + 0.4 * k
        g.add(VMobject(color="#7A7A7A", stroke_width=4).set_points_smoothly(
            [[-1.6, y, 0], [-0.8, y + 0.35, 0], [0, y + 0.1, 0], [0.8, y + 0.35, 0], [1.6, y, 0]]))
    g.add(Line([0, -2, 0], [0, 1.8, 0], color="#7A7A7A", stroke_width=6))
    return g


def plus_minus():
    g = VGroup()
    rng = np.random.default_rng(7)
    for _ in range(40):
        x, y = rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)
        if rng.random() < 0.5:
            g.add(Line([x - 0.15, y, 0], [x + 0.15, y, 0], color="#AAAAAA", stroke_width=4))
        else:
            g.add(Line([x, y - 0.15, 0], [x, y + 0.15, 0], color="#AAAAAA", stroke_width=4))
    return g


def cezanne_shapes():
    cyl = VGroup(Ellipse(width=0.8, height=0.25, color=C_BLUE), Line([-0.4, 0, 0], [-0.4, -0.9, 0], color=C_BLUE),
                 Line([0.4, 0, 0], [0.4, -0.9, 0], color=C_BLUE),
                 Arc(radius=0.4, start_angle=PI, angle=PI, color=C_BLUE).stretch(0.31, 1).shift(0.9 * DOWN))
    sph = Circle(radius=0.45, color=C_YELLOW, fill_opacity=0.2)
    cone = VGroup(Line([0, 0.5, 0], [-0.45, -0.5, 0], color=C_RED), Line([0, 0.5, 0], [0.45, -0.5, 0], color=C_RED),
                  Ellipse(width=0.9, height=0.25, color=C_RED).shift(0.5 * DOWN))
    return VGroup(cyl, sph, cone).arrange(RIGHT, buff=0.3)


def scream():
    face = VGroup(Ellipse(width=0.7, height=1.0, color="#D9C9A0", fill_opacity=0.9),
                  Ellipse(width=0.12, height=0.2, color=BLACK, fill_opacity=1).shift(0.12 * LEFT + 0.12 * UP),
                  Ellipse(width=0.12, height=0.2, color=BLACK, fill_opacity=1).shift(0.12 * RIGHT + 0.12 * UP),
                  Ellipse(width=0.14, height=0.26, color=BLACK, fill_opacity=1).shift(0.25 * DOWN))
    sky = VGroup(*[VMobject(stroke_color=c, stroke_width=5).set_points_smoothly(
        [[-1.4, y, 0], [-0.5, y + 0.2, 0], [0.4, y - 0.15, 0], [1.4, y + 0.1, 0]])
        for y, c in [(1.1, "#E0603A"), (0.85, "#F09A3A"), (0.6, "#E0603A"), (0.35, "#3A6EA5")]])
    rail = Line([-1.4, -1.2, 0], [1.4, -0.2, 0], color="#8B5A2B", stroke_width=6)
    return VGroup(sky, rail, face.shift(0.4 * DOWN + 0.2 * LEFT))


def sunrise():
    water = VGroup(*[Line([-1.3 + 0.1 * (i % 3), -0.2 - 0.18 * i, 0], [1.3 - 0.1 * (i % 2), -0.2 - 0.18 * i, 0],
                          color="#5E7FA8", stroke_width=3) for i in range(6)])
    sun = Circle(radius=0.22, fill_color="#F26B21", fill_opacity=1, stroke_width=0).shift(0.5 * UP + 0.3 * RIGHT)
    refl = VGroup(*[Line([0.15, -0.3 - 0.2 * i, 0], [0.45, -0.3 - 0.2 * i, 0], color="#F26B21", stroke_width=5)
                    for i in range(4)])
    boat = VGroup(Line([-0.7, -0.5, 0], [-0.3, -0.5, 0], color="#223", stroke_width=6),
                  Line([-0.5, -0.5, 0], [-0.5, -0.2, 0], color="#223", stroke_width=3))
    return VGroup(water, refl, sun, boat)


def convex_mirror():
    c = Circle(radius=1.0, color=C_GOLD, stroke_width=6)
    lines = VGroup(*[ParametricFunction(lambda t, k=k: np.array([0.9 * np.sin(t) * (0.3 + 0.7 * abs(k)), 0.9 * t / 1.6 * 1.0, 0]) +
                                         np.array([0.6 * k, 0, 0]),
                                         t_range=[-1.5, 1.5], color=C_GREY, stroke_width=2) for k in (-0.9, -0.3, 0.3, 0.9)])
    figs = VGroup(Dot([-0.25, 0, 0], color=C_RED), Dot([0.25, 0, 0], color=C_GREEN))
    return VGroup(c, lines, figs)


def last_supper():
    vp = np.array([0, 0.25, 0])
    room = VGroup(*[Line(p, vp, color=C_GREY, stroke_width=2) for p in
                    ([-1.4, 1.2, 0], [1.4, 1.2, 0], [-1.4, -1.2, 0], [1.4, -1.2, 0], [-1.4, 0.6, 0], [1.4, 0.6, 0])])
    table = Rectangle(width=2.4, height=0.3, fill_color="#C9B99A", fill_opacity=1, stroke_width=0).shift(0.4 * DOWN)
    heads = VGroup(*[Dot([x, 0.05, 0], radius=0.08, color="#D9B38C") for x in np.linspace(-1.1, 1.1, 13)])
    heads[6].set_color(C_RED).scale(1.3).move_to(vp)
    return VGroup(room, table, heads)


def mona():
    bg = VGroup(*[VMobject(stroke_color="#6E8B74", stroke_width=3).set_points_smoothly(
        [[-1.2, y, 0], [-0.4, y + 0.15, 0], [0.4, y - 0.1, 0], [1.2, y + 0.05, 0]]) for y in (0.9, 0.6)])
    body = Polygon([-1.0, -1.4, 0], [1.0, -1.4, 0], [0.45, 0.1, 0], [-0.45, 0.1, 0], fill_color="#3B2F22", fill_opacity=1, stroke_width=0)
    face = Ellipse(width=0.7, height=0.9, fill_color="#C9A27A", fill_opacity=1, stroke_width=0).shift(0.55 * UP)
    hair = Ellipse(width=0.95, height=1.2, fill_color="#2A2016", fill_opacity=1, stroke_width=0).shift(0.5 * UP)
    return VGroup(bg, body, hair, face)


def sculpture_head(color="#B08D57"):
    head = Ellipse(width=1.0, height=1.35, fill_color=color, fill_opacity=1, stroke_width=0)
    lines = VGroup(*[Line([-0.4, y, 0], [0.4, y, 0], color=BLACK, stroke_width=1.5) for y in np.linspace(-0.5, 0.4, 9)])
    neck = Rectangle(width=0.45, height=0.5, fill_color=color, fill_opacity=1, stroke_width=0).shift(0.85 * DOWN)
    return VGroup(neck, head, lines)


def colossal_head():
    helmet = Arc(radius=0.75, start_angle=0, angle=PI, fill_color="#6E6A60", fill_opacity=1, stroke_width=0).shift(0.2 * UP)
    face = RoundedRectangle(corner_radius=0.3, width=1.5, height=1.4, fill_color="#8A857A", fill_opacity=1, stroke_width=0).shift(0.35 * DOWN)
    eyes = VGroup(Ellipse(width=0.3, height=0.12, color=BLACK, fill_opacity=1).shift(0.3 * LEFT),
                  Ellipse(width=0.3, height=0.12, color=BLACK, fill_opacity=1).shift(0.3 * RIGHT))
    lips = Ellipse(width=0.6, height=0.2, color="#5A564E", fill_opacity=1).shift(0.75 * DOWN)
    return VGroup(helmet, face, eyes, lips)


def spiral_jetty():
    s = ParametricFunction(lambda t: np.array([0.12 * t * np.cos(t), 0.12 * t * np.sin(t), 0]), t_range=[0, 4 * PI],
                           color="#D9C9A0", stroke_width=8)
    line = Line(s.get_end(), s.get_end() + 1.3 * RIGHT + 0.4 * DOWN, color="#D9C9A0", stroke_width=8)
    water = Rectangle(width=3, height=3, fill_color="#8C5A6B", fill_opacity=1, stroke_width=0)
    return VGroup(water, s, line)


def kusama_dots():
    g = VGroup(Rectangle(width=2.8, height=2.8, fill_color=BLACK, fill_opacity=1, stroke_width=0))
    rng = np.random.default_rng(11)
    for _ in range(70):
        g.add(Dot([rng.uniform(-1.3, 1.3), rng.uniform(-1.3, 1.3), 0], radius=rng.uniform(0.03, 0.12),
                  color=[C_RED, C_YELLOW, WHITE][rng.integers(3)]))
    return g


def crown():
    return VGroup(
        Polygon([-0.8, 0, 0], [-0.8, 0.6, 0], [-0.4, 0.2, 0], [0, 0.8, 0], [0.4, 0.2, 0], [0.8, 0.6, 0], [0.8, 0, 0],
                color=C_YELLOW, stroke_width=6),
        T("SAMO©", 22, WHITE).shift(0.6 * DOWN))


def fountain():
    bowl = VGroup(Ellipse(width=1.6, height=2.0, color=WHITE, fill_color="#F0F0F0", fill_opacity=1),
                  Ellipse(width=0.9, height=1.2, color="#CCCCCC", stroke_width=2).shift(0.15 * DOWN))
    sig = T("R. MUTT 1917", 16, BLACK).shift(0.75 * DOWN + 0.3 * LEFT).rotate(0.2)
    return VGroup(bowl, sig)


def pixel_noise(n=12, size=2.6, seed=0, target=None):
    rng = np.random.default_rng(seed)
    g = VGroup()
    s = size / n
    for i in range(n):
        for j in range(n):
            x, y = -size / 2 + (i + 0.5) * s, -size / 2 + (j + 0.5) * s
            if target is None:
                c = interpolate_color(ManimColor(BLACK), ManimColor(WHITE), rng.random())
                c = interpolate_color(c, ManimColor(rng.choice([C_BLUE, C_RED, C_YELLOW, C_GREEN])), 0.5)
            else:
                c = target(x, y)
            g.add(Square(s, fill_color=c, fill_opacity=1, stroke_width=0).move_to([x, y, 0]))
    return g


def ai_target(x, y):
    if (x - 0.5) ** 2 + (y - 0.5) ** 2 < 0.25:
        return ManimColor(C_YELLOW)
    if y < -0.4:
        return ManimColor("#2D5DBE")
    return ManimColor("#1E2A44")


# ===================================================================== chapters


class Ch00(NarratedScene):
    chapter = "ch00"

    def construct(self):
        plane = Rectangle(width=4, height=3, color=WHITE, fill_color="#222", fill_opacity=1).shift(3 * LEFT)
        w_arrow = DoubleArrow(plane.get_corner(DL) + 0.3 * DOWN, plane.get_corner(DR) + 0.3 * DOWN, buff=0, color=C_GREY)
        h_arrow = DoubleArrow(plane.get_corner(DL) + 0.3 * LEFT, plane.get_corner(UL) + 0.3 * LEFT, buff=0, color=C_GREY)
        two = T("2D", 40, C_GREY).next_to(plane, UP)
        self.say("q1", Create(plane), [GrowFromCenter(w_arrow), GrowFromCenter(h_arrow)], FadeIn(two))

        cube = oblique_cube().shift(3.3 * RIGHT)
        three = T("3D", 40, C_BLUE).next_to(cube, UP)
        flat = cube.copy().set_color(C_YELLOW).scale(0.6).move_to(plane)
        self.say("q2", Create(cube, run_time=2), FadeIn(three),
                 TransformFromCopy(cube, flat, run_time=2), Indicate(flat))

        stuff = VGroup(plane, w_arrow, h_arrow, two, cube, three, flat)
        q = T("What is a picture for?", 54, C_YELLOW)
        self.say("q3", stuff.animate.scale(0.6).to_edge(UP), Write(q))

        span = NumberLine(x_range=[-70, 0, 10], length=11, include_numbers=False, color=C_GREY).shift(2.4 * DOWN)
        lab0 = T("70,000+ years ago", 22, C_GREY).next_to(span.n2p(-70), DOWN)
        lab1 = T("today", 22, C_GREY).next_to(span.n2p(0), DOWN)
        self.say("q4", Create(span), [FadeIn(lab0), FadeIn(lab1)])

        self.clear_all()
        dials = Dials(0.5, "who is it for?", "what is it made with?", width=7).shift(0.5 * RIGHT)
        self.say("axes", FadeIn(dials.rows[0]), 3.5, FadeIn(dials.rows[1]), 4,
                 [FadeIn(dials.rows[2]), FadeIn(dials[3:])])
        self.say("q5", dials.set_space(0.9), dials.set_space(0.2), dials.set_space(0.7), dials.set_space(0.4))
        self.clear_all()


class Ch01(NarratedScene):
    chapter = "ch01"

    def construct(self):
        show_chapter_card(self, 1, "Prehistory: the first marks")
        dials = corner_dials(0.15, "?", "ochre, stone, ivory")
        self.add(dials)

        tl = Line(6 * LEFT, 6 * RIGHT, color=C_GREY)

        def x(yrs):
            return tl.point_from_proportion(1 - yrs / 100000)

        events = [(75000, "Blombos ochre"), (51200, "Sulawesi"), (40000, "Lion-Man"), (36000, "Chauvet"),
                  (17000, "Lascaux"), (11500, "Göbekli Tepe"), (5000, "writing"), (600, "Renaissance")]
        ticks = VGroup()
        for i, (yrs, name) in enumerate(events):
            tick = Line(0.12 * UP, 0.12 * DOWN, color=WHITE).move_to(x(yrs))
            lab = T(name, 18, C_YELLOW if name == "Renaissance" else WHITE)
            lab.next_to(tick, UP if i % 2 == 0 else DOWN, buff=0.15)
            ticks.add(VGroup(tick, lab))
        ends = VGroup(T("100,000 years ago", 18, C_GREY).next_to(tl.get_start(), DOWN, buff=0.5),
                      T("today", 18, C_GREY).next_to(tl.get_end(), DOWN, buff=0.5))
        timeline = VGroup(tl, ticks, ends)
        bracket = BraceBetweenPoints(x(100000), x(5000), UP, color=C_BLUE).shift(0.6 * UP)
        btext = T("prehistory", 22, C_BLUE).next_to(bracket, UP, buff=0.1)
        self.say("p1", Create(tl), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.2, run_time=3), FadeIn(ends),
                 [GrowFromCenter(bracket), FadeIn(btext)])
        self.play(FadeOut(bracket), FadeOut(btext), timeline.animate.scale(0.8).to_edge(DOWN, buff=0.3), run_time=0.8)

        ochre = crosshatch_ochre().shift(0.6 * UP)
        cap = art_card("Engraved ochre, Blombos Cave", "South Africa", "c. 75,000 years ago").submobjects[-1]
        cap.next_to(ochre, DOWN, buff=0.4)
        self.say("p2", Indicate(ticks[0]), FadeIn(ochre, scale=0.8), Create(ochre[1], run_time=2), FadeIn(cap))
        self.play(FadeOut(ochre), FadeOut(cap), run_time=0.6)

        lion = art_card("Lion-Man of Hohlenstein-Stadel", "mammoth ivory", "c. 40,000 years ago",
                        slug="lion_man", kind="sculpture").shift(0.3 * UP)
        self.say("p3", Indicate(ticks[2]), FadeIn(lion, shift=UP * 0.2))
        sul = art_card("Narrative scene, Leang Karampuang", "Sulawesi, Indonesia", "at least 51,200 years ago*",
                       slug="sulawesi").shift(0.3 * UP)
        note = para("* earliest known, as dated in 2024. Dates keep moving.", 20, 3.2, C_GREY).next_to(sul, RIGHT, buff=0.5)
        self.say("p4", FadeOut(lion), Indicate(ticks[1]), FadeIn(sul), Write(note))
        self.play(FadeOut(sul), FadeOut(note), run_time=0.6)

        rock = VMobject(color="#8A7A66", stroke_width=4).set_points_smoothly(
            [[-5, -0.5, 0], [-3, 0.0, 0], [-1, 1.4, 0], [1, 1.5, 0], [3, 0.2, 0], [5, -0.3, 0]])
        animal = VGroup(
            Ellipse(width=2.4, height=1.2, color=C_OCHRE, fill_opacity=0.35),
            Circle(radius=0.35, color=C_OCHRE, fill_opacity=0.35).shift(1.35 * RIGHT + 0.15 * UP),
            *[Line([dx, -0.5, 0], [dx, -1.2, 0], color=C_OCHRE, stroke_width=5) for dx in (-0.8, -0.5, 0.5, 0.8)],
        ).shift(0.75 * UP)
        bulge = T("the rock's bulge becomes the body's volume", 22, C_GREY).shift(2.2 * UP)
        herd = VGroup(*[animal.copy().set_opacity(0.6).shift(s) for s in (1.0 * LEFT + 0.25 * DOWN, 2 * LEFT + 0.5 * DOWN)])
        caves = T("Chauvet (c. 36,000 yrs)  ·  Lascaux (c. 17,000 yrs)", 22).next_to(rock, DOWN, buff=1.4)
        self.say("p5", Create(rock), FadeIn(bulge), animal.animate.stretch(1.15, 1), FadeIn(caves),
                 LaggedStart(*[FadeIn(h) for h in herd], lag_ratio=0.5, run_time=2))
        self.play(FadeOut(VGroup(rock, animal, herd, bulge, caves)), run_time=0.6)

        hand = hand_stencil().scale(1.1).shift(0.8 * UP)
        self.say("p6", LaggedStart(*[FadeIn(d) for d in hand], lag_ratio=0.002, run_time=3))
        self.play(FadeOut(hand), run_time=0.6)

        cards = card_row(
            art_card("Venus of Willendorf", "limestone", "c. 30,000 years ago", slug="willendorf", kind="sculpture"),
            art_card("Göbekli Tepe pillars", "Turkey", "c. 11,500 years ago", slug="gobekli_tepe", kind="building"),
        ).shift(0.3 * UP)
        self.say("p7", *show_cards(*cards))
        self.play(FadeOut(cards), run_time=0.6)

        hyps = VGroup(*[T(h, 30) for h in ["hunting magic?", "storytelling?", "ritual or initiation?",
                                           "the pleasure of making?"]]).arrange(DOWN, buff=0.35).shift(0.8 * UP)
        self.say("p8", LaggedStart(*[FadeIn(h, shift=RIGHT * 0.2) for h in hyps], lag_ratio=0.6, run_time=4),
                 Indicate(dials.purpose_tag, scale_factor=1.6))
        self.clear_all()


class Ch02(NarratedScene):
    chapter = "ch02"

    def construct(self):
        show_chapter_card(self, 2, "The first civilizations: art as order")
        dials = corner_dials(0.15, "?", "ochre, stone, ivory")
        self.add(dials)
        self.say("e1", dials.set_label("purpose", "gods & kings"), dials.set_label("medium", "stone, paint, bronze"),
                 dials.set_space(0.2))

        fig = egypt_figure().shift(2 * LEFT + 0.3 * DOWN)
        p = fig.parts
        labels = VGroup(
            T("head: profile", 22, C_YELLOW).next_to(p["head"], RIGHT, buff=1.5),
            T("eye: front", 22, C_BLUE).next_to(p["eye"], RIGHT, buff=1.5).shift(0.45 * DOWN),
            T("shoulders: front", 22, C_BLUE).next_to(p["torso"], RIGHT, buff=1.3),
            T("legs: profile", 22, C_YELLOW).next_to(p["legs"], RIGHT, buff=1.2),
        )
        self.say("e2", Create(p["head"]), [FadeIn(p["eye"]), FadeIn(labels[0])], FadeIn(labels[1]),
                 [Create(p["torso"]), FadeIn(labels[2])], [Create(p["legs"]), FadeIn(labels[3])])
        idea = para("Each part from its most recognizable angle: a list of permanent facts, not a snapshot.", 28, 5)
        idea.to_edge(RIGHT, buff=0.6).shift(0.8 * DOWN)
        self.say("e3", labels.animate.shift(0.5 * UP).set_opacity(0.5), FadeIn(idea))
        self.play(FadeOut(labels), FadeOut(idea), run_time=0.6)

        small = VGroup(*[egypt_figure(C_GREY, 0.45) for _ in range(3)]).arrange(RIGHT, buff=0.4)
        small.next_to(fig, RIGHT, buff=0.8, aligned_edge=DOWN)
        hs = T("hierarchical scale: size = importance", 26, C_YELLOW).to_edge(UP, buff=1.0)
        narmer = T("Narmer Palette, c. 3100 BCE", 22, C_GREY).next_to(hs, DOWN)
        self.say("e4", LaggedStart(*[FadeIn(s) for s in small], lag_ratio=0.3), Write(hs), FadeIn(narmer))

        grid = NumberPlane(x_range=[-2, 2, 0.25], y_range=[-2.5, 2.5, 0.25], background_line_style={
            "stroke_color": C_BLUE, "stroke_opacity": 0.35, "stroke_width": 1}, axis_config={"stroke_opacity": 0})
        grid.scale_to_fit_height(fig.height * 1.1).move_to(fig)
        self.say("e5", FadeOut(VGroup(small, hs, narmer)), Create(grid, run_time=2), Indicate(fig, color=C_YELLOW))
        self.play(FadeOut(grid), FadeOut(fig), run_time=0.6)

        nef = art_card("Bust of Nefertiti", "Thutmose (attrib.)", "c. 1345 BCE", slug="nefertiti",
                       motif=sculpture_head("#C9A27A")).shift(0.2 * UP)
        self.say("e6", FadeIn(nef))
        self.play(FadeOut(nef), run_time=0.5)
        cards = card_row(
            art_card("Standard of Ur", "Mesopotamia", "c. 2600 BCE", slug="standard_of_ur", w=2.2, h=2.2),
            art_card("Stele of Hammurabi", "Babylon", "c. 1754 BCE", slug="hammurabi", kind="sculpture", w=2.2, h=2.2),
            art_card("Shang ritual bronze", "China", "c. 1600-1046 BCE", slug="shang_bronze", kind="sculpture", w=2.2, h=2.2),
            art_card("Olmec colossal head", "Mexico", "c. 1200-900 BCE", slug="olmec", motif=colossal_head(), w=2.2, h=2.2),
            art_card("Nok terracotta", "Nigeria", "1st millennium BCE", slug="nok", motif=sculpture_head("#A0522D"), w=2.2, h=2.2),
            buff=0.5).shift(0.2 * UP)
        self.say("e7", LaggedStart(*show_cards(*cards), lag_ratio=0.5, run_time=4))
        self.clear_all()


class Ch03(NarratedScene):
    chapter = "ch03"

    def construct(self):
        show_chapter_card(self, 3, "Greece and Rome: the body in motion")
        dials = corner_dials(0.2, "gods & kings", "stone, paint, bronze")
        self.add(dials)

        body, hip, sh = stick_body(0)
        fig = VGroup(body, hip, sh).shift(2.5 * LEFT + 0.2 * DOWN)
        kouros = T("Kouros, c. 600 BCE", 24, C_GREY).next_to(fig, DOWN)
        self.say("g1", Create(body, run_time=2), FadeIn(kouros))
        self.say("g2", Create(hip), Create(sh), [Indicate(hip), Indicate(sh)])

        body2, hip2, sh2 = stick_body(1)
        fig2 = VGroup(body2, hip2, sh2).move_to(fig)
        name = T("contrapposto", 44, C_YELLOW).shift(2.5 * RIGHT + 1 * UP)
        expl = para("weight on one leg: the hip rises, the shoulders tilt the other way", 26, 5).next_to(name, DOWN)
        self.say("g3", Transform(fig, fig2, run_time=3), Write(name), FadeIn(expl))
        self.play(FadeOut(VGroup(name, expl, kouros)), run_time=0.5)

        cards = card_row(
            art_card("Kritios Boy", "", "c. 480 BCE", slug="kritios_boy", kind="sculpture", w=2.4, h=3),
            art_card("Doryphoros (Spear Bearer)", "Polykleitos, Roman copy", "c. 440 BCE", slug="doryphoros",
                     kind="sculpture", w=2.4, h=3)).shift(3.0 * RIGHT + 0.1 * DOWN)
        self.say("g4", *show_cards(*cards), dials.set_space(0.55))
        self.play(FadeOut(cards), FadeOut(fig), run_time=0.6)

        statue = VGroup(
            Circle(radius=0.45, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(1.9 * UP),
            Polygon([-0.9, 1.4, 0], [0.9, 1.4, 0], [0.7, -0.3, 0], [-0.7, -0.3, 0], fill_color=WHITE, fill_opacity=1, stroke_width=0),
            Polygon([-0.7, -0.3, 0], [0.7, -0.3, 0], [0.9, -2.2, 0], [-0.9, -2.2, 0], fill_color=WHITE, fill_opacity=1, stroke_width=0),
            Polygon([-0.9, 1.4, 0], [-0.3, 1.4, 0], [-0.6, -0.4, 0], fill_color=WHITE, fill_opacity=1, stroke_width=0),
        )
        colored = statue.copy()
        for m, c in zip(colored, ["#C9A27A", "#2D5DBE", C_RED, C_GREEN]):
            m.set_fill(c)
        border = VGroup(*[Line([-0.85 + 0.17 * i, -2.0, 0], [-0.75 + 0.17 * i, -1.8, 0], color=C_GOLD, stroke_width=5)
                          for i in range(10)])
        myth = T("Myth: Greek statues were pure white", 28, C_GREY).to_edge(UP, buff=1.0)
        self.say("g5", FadeIn(statue), Write(myth), Transform(statue, colored, run_time=2.5), Create(border))
        self.play(FadeOut(VGroup(statue, border, myth)), run_time=0.6)

        par = parthenon(5).shift(0.2 * DOWN)
        gr = golden_rect(5).move_to(par)
        cross = Cross(gr, stroke_color=C_RED, stroke_width=8)
        ev = T("no good evidence the builders used the golden ratio", 26, C_RED).next_to(par, DOWN, buff=0.6)
        self.say("g6", FadeIn(par), Create(gr, run_time=2), Create(cross), Write(ev))
        self.play(FadeOut(VGroup(par, gr, cross, ev)), run_time=0.6)

        cards = card_row(
            art_card("Augustus of Prima Porta", "", "early 1st c. CE", slug="augustus", kind="sculpture", w=2.4, h=2.6),
            art_card("Pantheon dome", "Rome", "c. 113-125 CE", slug="pantheon", kind="building", w=2.4, h=2.6),
            art_card("Wall painting, Pompeii", "", "before 79 CE", slug="pompeii", w=2.4, h=2.6),
        ).shift(0.2 * UP)
        self.say("g7", LaggedStart(*show_cards(*cards), lag_ratio=0.4, run_time=3))
        self.play(FadeOut(cards), run_time=0.5)
        cards = card_row(
            art_card("Terracotta Army", "Qin dynasty, China", "c. 210 BCE", slug="terracotta_army", kind="sculpture"),
            art_card("Standing Buddha", "Gandhara", "c. 2nd-3rd c. CE", slug="gandhara_buddha", kind="sculpture"),
        ).shift(0.2 * UP)
        self.say("g8", *show_cards(*cards), dials.set_space(0.65, run_time=2))
        self.clear_all()


class Ch04(NarratedScene):
    chapter = "ch04"

    def construct(self):
        show_chapter_card(self, 4, "Faith and the flattened world")
        dials = corner_dials(0.65, "gods & kings", "stone, paint, bronze")
        self.add(dials)
        self.say("f1", dials.set_space(0.25, run_time=3))

        win = T("a window onto heaven,", 40, C_GOLD)
        win2 = T("not onto the physical world", 40, C_GREY)
        VGroup(win, win2).arrange(DOWN)
        self.say("f2", Write(win), FadeIn(win2))
        self.play(FadeOut(win), FadeOut(win2), run_time=0.5)

        gold = Rectangle(width=4, height=5, fill_color=C_GOLD, fill_opacity=1, stroke_width=0).shift(0.3 * DOWN)
        tess = VGroup(*[Square(0.25, stroke_color="#C79A30", stroke_width=1) .move_to(
            gold.get_corner(UL) + np.array([0.125 + 0.25 * i, -0.125 - 0.25 * j, 0])) for i in range(16) for j in range(20)])
        saint = robed_figure().scale(0.9).move_to(gold)
        lbl = T("gold = non-space, the divine", 24, C_GREY).next_to(gold, RIGHT)
        self.say("f3", FadeIn(gold), FadeIn(tess), FadeIn(saint, scale=0.9), FadeIn(lbl))
        self.play(FadeOut(VGroup(gold, tess, saint, lbl)), run_time=0.5)

        cards = card_row(
            art_card("Book of Kells", "Insular", "c. 800", slug="book_of_kells", kind="book"),
            art_card("Chartres Cathedral glass", "France", "c. 1194-1220", slug="chartres", motif=rose_window()),
        ).shift(0.2 * UP)
        self.say("f4", dials.set_label("purpose", "the Church"), *show_cards(*cards))
        self.play(FadeOut(cards), run_time=0.5)

        sq = Square(1.4, color=C_GOLD, stroke_width=4)
        rot = sq.copy().rotate(PI / 4).set_color(C_BLUE)
        tiles = VGroup(*[star_tile(0.8).move_to([x, y, 0]) for x in np.arange(-5.6, 5.7, 1.13) for y in np.arange(-3.0, 2.0, 1.13)])
        self.say("f5", Create(sq), TransformFromCopy(sq, rot), [FadeOut(sq), FadeOut(rot)],
                 LaggedStart(*[Create(t) for t in tiles], lag_ratio=0.01, run_time=3))
        self.play(FadeOut(tiles), run_time=0.5)

        cards = card_row(
            art_card("Travelers among Mountains and Streams", "Fan Kuan", "c. 1000", slug="fan_kuan", w=2.0, h=3.2),
            art_card("Ajanta cave paintings", "India", "c. 2nd c. BCE-5th c. CE", slug="ajanta", w=2.4, h=2.4),
            art_card("Shiva Nataraja", "Chola bronze", "c. 11th c.", slug="nataraja", kind="sculpture", w=2.4, h=2.4),
            art_card("Ife head", "Nigeria", "c. 12th-15th c.", slug="ife_head", motif=sculpture_head(), w=2.4, h=2.4),
        ).shift(0.2 * UP)
        self.say("f6", LaggedStart(*show_cards(*cards), lag_ratio=0.6, run_time=5))
        self.clear_all()


class Ch05(NarratedScene):
    chapter = "ch05"

    def construct(self):
        show_chapter_card(self, 5, "The Renaissance: the window")
        dials = corner_dials(0.25, "the Church", "fresco, tempera")
        self.add(dials)
        giotto = art_card("Arena (Scrovegni) Chapel frescoes", "Giotto", "c. 1305", slug="giotto").shift(0.2 * UP)
        self.say("r1", FadeIn(giotto), dials.set_space(0.4))
        self.play(FadeOut(giotto), run_time=0.5)

        names = VGroup(T("Brunelleschi's demonstration, c. 1415-20", 30),
                       T("Alberti, On Painting, 1435", 30)).arrange(DOWN, buff=0.4)
        self.say("r2", FadeIn(names[0]), FadeIn(names[1]))
        self.play(FadeOut(names), FadeOut(dials), run_time=0.5)

        hy, by = 1.2, -3.2
        vp = np.array([0, hy, 0])
        horizon = Line([-7, hy, 0], [7, hy, 0], color=C_BLUE)
        vpd = Dot(vp, color=C_YELLOW, radius=0.1)
        vpl = T("vanishing point", 24, C_YELLOW).next_to(vpd, UP)
        hl = T("horizon = eye level", 22, C_BLUE).next_to(horizon.get_start(), UR, buff=0.1).shift(0.6 * RIGHT)
        self.say("r3", Create(horizon), FadeIn(hl), [GrowFromCenter(vpd), FadeIn(vpl)])

        xs = np.linspace(-4, 4, 9)
        orth = VGroup(*[Line([x, by, 0], vp, color=WHITE, stroke_width=2) for x in xs])
        ol = T("orthogonals", 24).next_to(orth[-1].get_start(), RIGHT).shift(0.5 * UP)
        self.say("r4", LaggedStart(*[Create(o) for o in orth], lag_ratio=0.15, run_time=3), FadeIn(ol))

        wrong = VGroup(*[Line([-4 + 4 * (y - by) / (hy - by), y, 0], [4 - 4 * (y - by) / (hy - by), y, 0], color=C_RED)
                         for y in np.linspace(by, by + 3.2, 7)])
        q = T("evenly spaced? wrong!", 26, C_RED).to_edge(RIGHT).shift(1.5 * DOWN)
        self.say("r5", Create(wrong, run_time=2), FadeIn(q), [FadeOut(wrong), FadeOut(q)])

        dist = np.array([7.5, hy, 0])

        def inter(p1, p2, p3, p4):
            d1, d2 = p2 - p1, p4 - p3
            A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
            t = np.linalg.solve(A, (p3 - p1)[:2])[0]
            return p1 + t * d1

        ys = [by]
        for x in xs[1:]:
            ys.append(inter(np.array([-4, by, 0]), dist, np.array([x, by, 0]), vp)[1])
        diag = Line([-4, by, 0], inter(np.array([-4, by, 0]), dist, np.array([xs[-1], by, 0]), vp), color=C_YELLOW)
        rows = VGroup()
        for y in ys:
            k = (y - by) / (hy - by)
            rows.add(Line([-4 * (1 - k), y, 0], [4 * (1 - k), y, 0], color=WHITE, stroke_width=2))
        crosses = VGroup(*[Dot(inter(np.array([-4, by, 0]), dist, np.array([x, by, 0]), vp), color=C_YELLOW, radius=0.06)
                           for x in xs[1:]])

        def pt(i, j):
            y = ys[j]
            k = (y - by) / (hy - by)
            return np.array([xs[i] * (1 - k), y, 0])

        tiles = VGroup()
        for i in range(8):
            for j in range(len(ys) - 1):
                if (i + j) % 2 == 0:
                    tiles.add(Polygon(pt(i, j), pt(i + 1, j), pt(i + 1, j + 1), pt(i, j + 1),
                                      fill_color=C_BLUE, fill_opacity=0.35, stroke_width=0))
        self.say("r6", Create(diag), LaggedStart(*[GrowFromCenter(c) for c in crosses], lag_ratio=0.2),
                 LaggedStart(*[Create(r) for r in rows], lag_ratio=0.15, run_time=2), FadeIn(tiles))

        top = ys[-1]
        colL = Rectangle(width=0.5, height=3.6, fill_color="#555", fill_opacity=1, stroke_width=0).move_to([-3.2, by + 2.6, 0])
        colR = colL.copy().move_to([3.2, by + 2.6, 0])
        arch = Arc(radius=3.2, start_angle=0, angle=PI, color=WHITE).stretch(0.7, 1, about_point=ORIGIN).shift([0, by + 4.4, 0])
        vault = VGroup(*[Line(arch.point_from_proportion(p), vp + (arch.point_from_proportion(p) - vp) * 0.55, color=C_GREY,
                              stroke_width=2) for p in np.linspace(0, 1, 9)])
        cap = T("Masaccio, Holy Trinity, c. 1427", 26, C_YELLOW).to_edge(DOWN, buff=0.15)
        persp = VGroup(horizon, vpd, vpl, hl, orth, ol, diag, crosses, rows, tiles)
        self.say("r7", FadeOut(ol), FadeOut(hl), [FadeIn(colL), FadeIn(colR), Create(arch)], Create(vault), Write(cap))
        self.play(FadeOut(VGroup(persp, colL, colR, arch, vault, cap)), run_time=0.7)

        dials = corner_dials(0.85, "the Church", "fresco, tempera")
        self.add(dials)
        arn = art_card("Arnolfini Portrait", "Jan van Eyck", "1434", slug="arnolfini", motif=convex_mirror()).shift(0.2 * UP)
        self.say("r8", FadeIn(arn), dials.set_label("medium", "oil paint, fresco"))
        self.play(FadeOut(arn), run_time=0.5)

        cards = card_row(
            art_card("The Last Supper", "Leonardo", "c. 1495-98", slug="last_supper", motif=last_supper(), w=2.6, h=2.0),
            art_card("Mona Lisa", "Leonardo", "c. 1503-19", slug="mona_lisa", motif=mona(), w=1.8, h=2.4),
            art_card("David", "Michelangelo", "1501-04", slug="david", kind="sculpture", w=1.8, h=2.4),
            art_card("Sistine Chapel ceiling", "Michelangelo", "1508-12", slug="sistine", w=2.4, h=2.0),
            art_card("The School of Athens", "Raphael", "1509-11", slug="school_of_athens", w=2.4, h=2.0),
            buff=0.4).shift(0.5 * UP)
        self.say("r9", LaggedStart(*show_cards(*cards), lag_ratio=0.8, run_time=8), dials.set_space(0.9))
        self.play(FadeOut(cards), run_time=0.5)
        durer = art_card("Draughtsman drawing a reclining nude", "Albrecht Dürer, woodcut", "1525", slug="durer").shift(0.2 * UP)
        self.say("r10", dials.set_label("purpose", "Church & merchants"), FadeIn(durer),
                 dials.set_label("medium", "oil, fresco, print"))
        self.clear_all()


class Ch06(NarratedScene):
    chapter = "ch06"

    def construct(self):
        show_chapter_card(self, 6, "Baroque: drama and light")
        dials = corner_dials(0.9, "Church & merchants", "oil, fresco, print")
        self.add(dials)
        drama = T("drama", 72, C_RED)
        self.say("b1", Write(drama))
        self.play(FadeOut(drama), run_time=0.4)

        stage = Rectangle(width=9, height=5, fill_color="#0A0A0A", fill_opacity=1, stroke_width=0).shift(0.4 * DOWN)
        figs = VGroup(*[VGroup(Circle(radius=0.3), Polygon([-0.5, -0.3, 0], [0.5, -0.3, 0], [0.6, -1.8, 0], [-0.6, -1.8, 0]))
                        .set_stroke(width=0).set_fill("#1A1A1A", 1).move_to([x, -0.6, 0]) for x in (-2.5, -1.2, 0.2)])
        beam = Polygon([4.5, 2.1, 0], [3.3, 2.1, 0], [-3.4, -2.8, 0], [-0.2, -2.8, 0], fill_color=C_YELLOW,
                       fill_opacity=0.12, stroke_width=0)
        lit = figs.copy()
        for f, c in zip(lit, ["#C9A27A", "#B08D57", "#8A6E4B"]):
            f.set_fill(c, 1)
        cap = T("The Calling of Saint Matthew, Caravaggio, 1599-1600", 22, C_GREY).next_to(stage, DOWN, buff=0.15)
        self.say("b2", FadeIn(stage), FadeIn(figs), FadeIn(beam), Transform(figs, lit, run_time=2), FadeIn(cap))
        self.play(FadeOut(VGroup(stage, figs, beam, cap)), run_time=0.5)

        bern = art_card("Ecstasy of Saint Teresa", "Gian Lorenzo Bernini", "1647-52", slug="bernini_teresa",
                        kind="sculpture").shift(0.2 * UP)
        self.say("b3", FadeIn(bern), dials.set_label("purpose", "Church (Counter-Reformation)"))
        self.play(FadeOut(bern), run_time=0.5)
        cards = card_row(
            art_card("The Night Watch", "Rembrandt", "1642", slug="night_watch", w=3.4, h=2.6),
            art_card("Girl with a Pearl Earring", "Johannes Vermeer", "c. 1665", slug="vermeer_pearl", w=2.2, h=2.6),
        ).shift(0.2 * UP)
        self.say("b4", dials.set_label("purpose", "an open art market"), *show_cards(*cards))
        self.play(FadeOut(cards), run_time=0.5)

        room = Rectangle(width=7, height=4.2, color=C_GREY).shift(0.6 * UP)
        back = T("back wall", 18, C_GREY).next_to(room, UP, buff=0.05)
        mirror = Rectangle(width=0.6, height=0.12, fill_color=C_BLUE, fill_opacity=1, stroke_width=0).move_to(room.get_top() + 0.06 * DOWN)
        canvas = Rectangle(width=0.15, height=1.6, fill_color="#6B4A2B", fill_opacity=1, stroke_width=0).move_to([-2.5, 0.6, 0])
        painter = Dot([-2.0, 0.6, 0], color=C_YELLOW, radius=0.14)
        princess = Dot([0.3, 0.0, 0], color=C_RED, radius=0.14)
        viewer = Dot([0.2, -2.4, 0], color=WHITE, radius=0.16)
        labs = VGroup(T("Velázquez", 20, C_YELLOW).next_to(painter, UP), T("canvas", 18, C_GREY).next_to(canvas, LEFT),
                      T("Infanta Margarita", 20, C_RED).next_to(princess, RIGHT), T("mirror", 20, C_BLUE).next_to(mirror, DOWN))
        cap = T("Las Meninas, Diego Velázquez, 1656  (plan view)", 22, C_GREY).to_corner(UL, buff=0.3)
        self.say("b5", FadeIn(cap), Create(room), FadeIn(back), [FadeIn(canvas), FadeIn(painter), FadeIn(labs[0]), FadeIn(labs[1])],
                 [FadeIn(princess), FadeIn(labs[2])], [FadeIn(mirror), FadeIn(labs[3])])

        rays = VGroup(Arrow(painter.get_center(), viewer.get_center(), buff=0.2, color=C_YELLOW, stroke_width=3),
                      Arrow(princess.get_center(), viewer.get_center(), buff=0.2, color=C_RED, stroke_width=3),
                      DashedLine(mirror.get_center(), viewer.get_center(), color=C_BLUE))
        you = T("king & queen ... and you", 24).next_to(viewer, RIGHT)
        self.say("b6", FadeIn(viewer), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.5, run_time=3), Write(you),
                 Flash(viewer, color=WHITE))
        self.clear_all()


class Ch07(NarratedScene):
    chapter = "ch07"

    def construct(self):
        show_chapter_card(self, 7, "Revolutions")
        dials = corner_dials(0.9, "an open art market", "oil, fresco, print")
        self.add(dials)
        david = art_card("Oath of the Horatii", "Jacques-Louis David", "1784", slug="horatii").shift(0.2 * UP)
        self.say("v1", FadeIn(david), dials.set_label("purpose", "the nation, the public"))
        self.play(FadeOut(david), run_time=0.5)
        cards = card_row(
            art_card("The Third of May 1808", "Francisco Goya", "1814", slug="goya_third_may", w=2.6, h=2.0),
            art_card("Wanderer above the Sea of Fog", "Caspar David Friedrich", "c. 1818", slug="friedrich_wanderer", w=1.8, h=2.3),
            art_card("The Raft of the Medusa", "Théodore Géricault", "1818-19", slug="raft_medusa", w=2.6, h=2.0),
            art_card("Liberty Leading the People", "Eugène Delacroix", "1830", slug="delacroix_liberty", w=2.6, h=2.0),
            buff=0.4).shift(0.2 * UP)
        self.say("v2", LaggedStart(*show_cards(*cards), lag_ratio=0.9, run_time=8))
        self.play(FadeOut(cards), run_time=0.5)
        cour = art_card("The Stone Breakers", "Gustave Courbet", "1849 (destroyed 1945)", slug="courbet_stonebreakers").shift(0.2 * UP)
        self.say("v3", FadeIn(cour))
        self.play(FadeOut(cour), run_time=0.5)

        year = T("1839", 120, C_YELLOW)
        photo = T("photography", 40).next_to(year, DOWN)
        self.say("v4", Write(year), FadeIn(photo), dials.set_label("medium", "+ photography"))
        self.play(FadeOut(year), FadeOut(photo), run_time=0.5)

        box = Rectangle(width=4, height=2.6, color=WHITE).shift(1.8 * RIGHT)
        hole = Dot(box.get_left(), color=BG, radius=0.08)
        trunk = Line([-4.5, -1.3, 0], [-4.5, -0.6, 0], color="#8B6B4A", stroke_width=8)
        crown_ = Triangle(color=C_GREEN, fill_opacity=0.7).scale(0.9).move_to([-4.5, 0.4, 0])
        tree_ = VGroup(trunk, crown_)
        top, bot = crown_.get_top(), trunk.get_bottom()
        p = box.get_left()

        def through(src):
            d = p - src
            t = (box.get_right()[0] - p[0]) / d[0]
            return p + t * d

        rays = VGroup(Line(top, through(top), color=C_YELLOW, stroke_width=2), Line(bot, through(bot), color=C_YELLOW, stroke_width=2))
        img = tree_.copy().rotate(PI).scale(0.6)
        img.move_to([box.get_right()[0] - 0.3, (through(top)[1] + through(bot)[1]) / 2, 0])
        lbl = T("camera obscura: light through a small hole", 24, C_GREY).to_edge(UP, buff=1.0)
        self.say("v5", FadeIn(tree_), Create(box), FadeIn(hole), FadeIn(lbl), Create(rays, run_time=2), FadeIn(img))
        self.play(FadeOut(VGroup(box, hole, tree_, rays, img, lbl)), run_time=0.5)
        q = T("So, what is painting for now?", 48, C_YELLOW)
        self.say("v6", Write(q))
        self.clear_all()


class Ch08(NarratedScene):
    chapter = "ch08"

    def construct(self):
        show_chapter_card(self, 8, "Breaking the window")
        dials = corner_dials(0.9, "the nation, the public", "+ photography")
        self.add(dials)
        cards = card_row(
            art_card("Le Déjeuner sur l'herbe", "Édouard Manet", "1863", slug="manet_dejeuner", w=3.0, h=2.3),
            art_card("Olympia", "Édouard Manet", "1863", slug="manet_olympia", w=3.0, h=2.0),
        ).shift(0.2 * UP)
        self.say("m1", *show_cards(*cards), dials.set_space(0.6))
        self.play(FadeOut(cards), run_time=0.5)

        tube = VGroup(RoundedRectangle(corner_radius=0.2, width=3, height=0.8, fill_color="#BBBBBB", fill_opacity=1, stroke_width=0),
                      Rectangle(width=0.4, height=0.4, fill_color=C_GREY, fill_opacity=1, stroke_width=0).shift(1.7 * RIGHT),
                      Rectangle(width=1.2, height=0.5, fill_color=C_BLUE, fill_opacity=1, stroke_width=0).shift(0.3 * LEFT))
        tl = T("paint tube, patented 1841", 26, C_GREY).next_to(tube, DOWN)
        self.say("m2", FadeIn(tube, shift=RIGHT), FadeIn(tl), dials.set_label("medium", "tube paint, outdoors"))
        self.play(FadeOut(tube), FadeOut(tl), run_time=0.5)

        imp = art_card("Impression, Sunrise", "Claude Monet", "1872", slug="monet_impression", motif=sunrise()).shift(0.2 * UP)
        self.say("m3", FadeIn(imp), dials.set_label("purpose", "the artist's eye"))
        self.play(FadeOut(imp), run_time=0.5)

        hues = ["#FF3B30", "#FF9500", "#FFCC00", "#4CD964", "#5AC8FA", "#5856D6"]
        wheel = VGroup(*[AnnularSector(inner_radius=0.9, outer_radius=2.0, angle=TAU / 6, start_angle=i * TAU / 6 + PI / 2,
                                       fill_color=c, fill_opacity=1, stroke_color=BG, stroke_width=4) for i, c in enumerate(hues)])
        pairs = VGroup(*[Line(wheel[i].get_center(), wheel[i + 3].get_center(), color=WHITE) for i in range(3)])
        cl = T("complementary pairs", 26).next_to(wheel, DOWN)
        self.say("m4", FadeIn(wheel, scale=0.8), LaggedStart(*[Create(p) for p in pairs], lag_ratio=0.5), FadeIn(cl))
        self.play(FadeOut(VGroup(wheel, pairs, cl)), run_time=0.5)

        rng = np.random.default_rng(2)
        dots = VGroup()
        for i in range(30):
            for j in range(18):
                x, y = -4.35 + 0.3 * i, -2.55 + 0.3 * j
                in_sun = (x - 1.5) ** 2 + (y - 0.8) ** 2 < 1.0
                pal = ["#FF9500", "#FFCC00", "#FF3B30"] if in_sun else (["#5AC8FA", "#4CD964", "#5856D6"] if y < -0.5 else ["#5AC8FA", "#5856D6", "#FFFFFF"])
                dots.add(Dot([x, y, 0], radius=0.11, color=pal[rng.integers(3)]))
        dots.shift(0.3 * DOWN)
        jatte = T("A Sunday on La Grande Jatte, Georges Seurat, 1884-86", 22, C_GREY).to_edge(DOWN, buff=0.15)
        self.say("m5", LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.003, run_time=3), FadeIn(jatte),
                 dots.animate(run_time=2.5).scale(0.25))
        self.play(FadeOut(dots), FadeOut(jatte), run_time=0.5)

        wave = art_card("The Great Wave off Kanagawa", "Katsushika Hokusai", "c. 1831", slug="hokusai_wave",
                        motif=great_wave()).shift(0.2 * UP)
        self.say("m6", FadeIn(wave), dials.set_space(0.45))
        self.play(FadeOut(wave), run_time=0.5)
        cards = card_row(
            art_card("The Starry Night", "Vincent van Gogh", "1889", slug="starry_night", motif=starry_night(), w=2.8, h=2.3),
            art_card("Mont Sainte-Victoire", "Paul Cézanne", "c. 1902-06", slug="cezanne", motif=cezanne_shapes(), w=2.8, h=2.3),
            art_card("The Scream", "Edvard Munch", "1893", slug="munch_scream", motif=scream(), w=2.2, h=2.6),
        ).shift(0.2 * UP)
        self.say("m7", LaggedStart(*show_cards(*cards), lag_ratio=1.0, run_time=9))
        self.clear_all()


class Ch09(NarratedScene):
    chapter = "ch09"

    def construct(self):
        show_chapter_card(self, 9, "The picture becomes the idea")
        dials = corner_dials(0.45, "the artist's eye", "tube paint, outdoors")
        self.add(dials)
        dem = art_card("Les Demoiselles d'Avignon", "Pablo Picasso", "1907", slug="demoiselles").shift(0.2 * UP)
        self.say("c1", FadeIn(dem))
        self.play(FadeOut(dem), run_time=0.5)

        def mug_front():
            return VGroup(Rectangle(width=1.4, height=1.8, color=C_BLUE), Arc(radius=0.45, start_angle=-PI / 2, angle=PI,
                                                                            color=C_BLUE).shift(0.7 * RIGHT))

        def mug_top():
            return VGroup(Circle(radius=0.75, color=C_YELLOW), Circle(radius=0.6, color=C_YELLOW),
                          Rectangle(width=0.5, height=0.2, color=C_YELLOW).shift(1.0 * RIGHT))

        def mug_side():
            return VGroup(Ellipse(width=1.4, height=0.4, color=C_RED).shift(0.9 * UP), Line([-0.7, 0.9, 0], [-0.7, -0.9, 0], color=C_RED),
                          Line([0.7, 0.9, 0], [0.7, -0.9, 0], color=C_RED),
                          Arc(radius=0.7, start_angle=PI, angle=PI, color=C_RED).stretch(0.28, 1).shift(0.9 * DOWN))

        views = VGroup(mug_front(), mug_top(), mug_side()).arrange(RIGHT, buff=1.2).shift(0.3 * UP)
        vl = VGroup(*[T(t, 24, C_GREY).next_to(v, DOWN) for t, v in zip(["front", "above", "three-quarter"], views)])
        self.say("c2", *[[Create(v), FadeIn(l)] for v, l in zip(views, vl)])

        frame = Rectangle(width=4, height=4, color=C_GOLD).shift(0.2 * DOWN)
        targets = [views[0].copy().scale(0.8).rotate(0.15).move_to(frame.get_center() + 0.6 * LEFT + 0.5 * DOWN),
                   views[1].copy().scale(0.7).rotate(-0.2).move_to(frame.get_center() + 0.5 * RIGHT + 0.7 * UP),
                   views[2].copy().scale(0.7).rotate(0.3).move_to(frame.get_center() + 0.8 * RIGHT + 0.6 * DOWN)]
        self.say("c3", FadeOut(vl), Create(frame), *[Transform(v, t, run_time=1.3) for v, t in zip(views, targets)],
                 dials.set_space(0.3))
        self.play(FadeOut(views), FadeOut(frame), run_time=0.5)

        t1 = tree()
        t2 = curvy_tree()
        t3 = plus_minus()
        t4 = mondrian(3.2, 3.2)
        years = ["c. 1908", "c. 1911", "c. 1915", "1920s"]
        ylab = T(years[0], 26, C_GREY).to_edge(DOWN, buff=0.6)
        self.say("c4", Create(t1, run_time=2), [Transform(t1, t2), Transform(ylab, T(years[1], 26, C_GREY).move_to(ylab))],
                 1, [Transform(t1, t3), Transform(ylab, T(years[2], 26, C_GREY).move_to(ylab))],
                 1, [FadeTransform(t1, t4), Transform(ylab, T(years[3], 26, C_GREY).move_to(ylab))])
        self.play(FadeOut(t4), FadeOut(ylab), run_time=0.5)

        cards = card_row(
            art_card("The Ten Largest (series)", "Hilma af Klint", "1907", slug="af_klint", w=2.2, h=2.8),
            art_card("Composition VII", "Wassily Kandinsky", "1913", slug="kandinsky", w=2.8, h=2.2),
            art_card("Black Square", "Kazimir Malevich", "1915", slug="black_square", motif=black_square(), w=2.4, h=2.4),
        ).shift(0.2 * UP)
        self.say("c5", LaggedStart(*show_cards(*cards), lag_ratio=0.8, run_time=6), dials.set_space(0.0, run_time=2))
        self.play(FadeOut(cards), run_time=0.5)

        fnt = art_card("Fountain", "Marcel Duchamp (attribution debated)", "1917", slug="fountain", motif=fountain()).shift(0.2 * UP)
        self.say("c6", FadeIn(fnt), dials.set_label("purpose", "the idea"), dials.set_label("medium", "anything at all"))
        self.play(FadeOut(fnt), run_time=0.5)
        pp = art_card("The Treachery of Images", "René Magritte", "1929", slug="magritte_pipe", motif=pipe(), w=3.6, h=3.0).shift(0.2 * UP)
        self.say("c7", FadeIn(pp))
        self.play(FadeOut(pp), run_time=0.5)
        cards = card_row(
            art_card("The Persistence of Memory", "Salvador Dalí", "1931", slug="dali", w=2.6, h=2.0),
            art_card("The Two Fridas", "Frida Kahlo", "1939", slug="kahlo", w=2.4, h=2.4),
            art_card("Guernica", "Pablo Picasso", "1937", slug="guernica", w=3.4, h=1.6),
        ).shift(0.2 * UP)
        self.say("c8", LaggedStart(*show_cards(*cards), lag_ratio=1.0, run_time=7))
        self.clear_all()


class Ch10(NarratedScene):
    chapter = "ch10"

    def construct(self):
        show_chapter_card(self, 10, "After 1945: art about art")
        dials = corner_dials(0.0, "the idea", "anything at all")
        self.add(dials)
        d = drips()
        cap = T("Jackson Pollock, drip paintings, 1947-50", 22, C_GREY).next_to(d, DOWN)
        self.say("a1", FadeIn(d[0]), Create(d[1], lag_ratio=0.15, run_time=5), FadeIn(cap))
        self.play(FadeOut(d), FadeOut(cap), run_time=0.5)
        r = art_card("Color field painting", "Mark Rothko", "1950s", slug="rothko", motif=rothko()).shift(0.2 * UP)
        self.say("a2", FadeIn(r))
        self.play(FadeOut(r), run_time=0.5)

        cans = VGroup(*[soup_can().scale(0.28) for _ in range(32)]).arrange_in_grid(4, 8, buff=0.15).shift(0.8 * UP)
        cl = T("Campbell's Soup Cans, Andy Warhol, 1962  (32 canvases)", 22, C_GREY).next_to(cans, DOWN)
        ben = VGroup(*[Dot([0.35 * i + 0.175 * (j % 2), 0.3 * j, 0], radius=0.11, color=C_RED)
                       for i in range(-5, 6) for j in range(-4, 5)]).shift(2.5 * RIGHT)
        seu = VGroup(*[Dot([0.3 * i, 0.3 * j, 0], radius=0.11, color=[C_BLUE, C_YELLOW, C_GREEN][(i * 7 + j * 3) % 3])
                       for i in range(-5, 6) for j in range(-4, 5)]).shift(3.2 * LEFT)
        bl = VGroup(T("Seurat, 1880s", 24).next_to(seu, DOWN), T("Lichtenstein's Ben-Day dots, 1960s", 24).next_to(ben, DOWN))
        self.say("a3", LaggedStart(*[FadeIn(c) for c in cans], lag_ratio=0.05, run_time=2.5), FadeIn(cl), 3,
                 [FadeOut(cans), FadeOut(cl)], [FadeIn(seu), FadeIn(ben), FadeIn(bl)])
        self.play(FadeOut(VGroup(seu, ben, bl)), run_time=0.5)

        box = Cube(side_length=1.6, fill_color=C_GREY, fill_opacity=0.6, stroke_color=WHITE).rotate(0.5, UP).rotate(0.3, RIGHT)
        box.shift(3.5 * LEFT)
        instr = para("Wall drawing instructions: draw fifty straight lines, each from edge to edge of the wall.", 24, 5)
        instr.shift(1.5 * RIGHT + 1.8 * UP)
        wall = Rectangle(width=5, height=2.6, color=C_GREY).next_to(instr, DOWN, buff=0.4)
        rng = np.random.default_rng(5)

        def edge_pt():
            s = rng.integers(4)
            u = rng.random()
            w, h, c = wall.width, wall.height, wall.get_center()
            return c + [np.array([-w / 2 + u * w, h / 2, 0]), np.array([-w / 2 + u * w, -h / 2, 0]),
                        np.array([-w / 2, -h / 2 + u * h, 0]), np.array([w / 2, -h / 2 + u * h, 0])][s]

        lines = VGroup(*[Line(edge_pt(), edge_pt(), color=WHITE, stroke_width=1.2) for _ in range(50)])
        self.say("a4", FadeIn(box), FadeIn(instr), Create(wall), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05, run_time=3))
        self.play(FadeOut(VGroup(box, instr, wall, lines)), run_time=0.5)

        cards = card_row(
            art_card("Performance", "Marina Abramović", "from 1970s", slug="abramovic", kind="sculpture", w=2.3, h=2.3),
            art_card("Spiral Jetty", "Robert Smithson", "1970", slug="spiral_jetty", motif=spiral_jetty(), w=2.3, h=2.3),
            art_card("Infinity Mirror Rooms", "Yayoi Kusama", "from 1965", slug="kusama", motif=kusama_dots(), w=2.3, h=2.3),
            art_card("Paintings", "Jean-Michel Basquiat", "early 1980s", slug="basquiat", motif=crown(), w=2.3, h=2.3),
            buff=0.5).shift(0.2 * UP)
        self.say("a5", LaggedStart(*show_cards(*cards), lag_ratio=0.9, run_time=7))
        self.clear_all()


class Ch11(NarratedScene):
    chapter = "ch11"

    def construct(self):
        show_chapter_card(self, 11, "Now")
        dials = corner_dials(0.0, "the idea", "anything at all")
        self.add(dials)
        self.say("n1", dials.set_label("purpose", "ideas, markets, the public"), dials.set_label("medium", "video, digital, internet"))

        frame = Rectangle(width=2.6, height=3.2, color=C_GOLD, stroke_width=6).shift(0.9 * UP)
        bal = heart_balloon().move_to(frame).shift(0.2 * UP)
        canvas = VGroup(Rectangle(width=2.5, height=3.1, fill_color="#EEE", fill_opacity=1, stroke_width=0).move_to(frame), bal)
        strips = VGroup(*[canvas.copy() for _ in range(1)])
        cap = T("Girl with Balloon / Love Is in the Bin, Banksy, 2018", 22, C_GREY).to_edge(DOWN, buff=0.3)
        shreds = VGroup(*[Rectangle(width=0.12, height=1.6, fill_color="#EEE", fill_opacity=1, stroke_width=0)
                          .move_to(frame.get_bottom() + np.array([-1.15 + 0.2 * i, -0.8, 0])) for i in range(12)])
        self.say("n2", FadeIn(canvas), Create(frame), FadeIn(cap), [canvas.animate.shift(1.6 * DOWN).set_opacity(0),
                                                                    LaggedStart(*[FadeIn(s, shift=0.6 * DOWN) for s in shreds],
                                                                                lag_ratio=0.1)])
        self.play(FadeOut(VGroup(frame, canvas, shreds, cap)), run_time=0.5)

        val = ValueTracker(0)
        price = always_redraw(lambda: T(f"${int(val.get_value()):,}", 90, C_YELLOW).shift(0.5 * UP))
        cap = T("Everydays: The First 5000 Days, Beeple, sold as an NFT, 2021", 22, C_GREY).shift(1.5 * DOWN)
        self.say("n3", FadeIn(price), val.animate(run_time=3, rate_func=rush_from).set_value(69346250), FadeIn(cap))
        price.clear_updaters()
        self.play(FadeOut(VGroup(price, cap)), run_time=0.5)

        noise = pixel_noise(seed=1).shift(0.6 * UP)
        clean = pixel_noise(target=ai_target).shift(0.6 * UP)
        cap = T("Théâtre D'opéra Spatial, Jason M. Allen (made with Midjourney), 2022", 22, C_GREY).next_to(noise, DOWN, buff=0.4)
        self.say("n4", FadeIn(noise), Transform(noise, pixel_noise(seed=2).shift(0.6 * UP), run_time=1),
                 Transform(noise, clean, run_time=2.5), FadeIn(cap))
        self.play(FadeOut(noise), FadeOut(cap), run_time=0.5)

        items = VGroup(T("Photography, 1839", 32), T("Fountain, 1917", 32), T("AI images, 2022", 32)).arrange(RIGHT, buff=1.2)
        q = T("Is it art?", 44, C_YELLOW).next_to(items, UP, buff=1.0)
        arrows = VGroup(*[Arrow(q.get_bottom(), it.get_top(), buff=0.15, color=C_GREY) for it in items])
        self.say("n5", Write(q), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.6), Create(arrows))
        self.clear_all()


class Ch12(NarratedScene):
    chapter = "ch12"

    def construct(self):
        dials = Dials(0.15, "spirits?", "ochre", width=7).shift(0.3 * RIGHT + 0.8 * DOWN)
        self.say("z1", FadeIn(dials))

        era = T("Prehistory", 36, C_BLUE).to_edge(UP, buff=0.8)
        seq = [("Prehistory", 0.15), ("Egypt", 0.2), ("Greece & Rome", 0.65), ("Middle Ages", 0.25),
               ("Renaissance", 0.9), ("Baroque", 0.92), ("Photography arrives", 0.85), ("Impressionism", 0.5),
               ("Cubism", 0.3), ("Abstraction", 0.0)]
        steps = [FadeIn(era)]
        for name, v in seq[1:]:
            steps.append([dials.set_space(v, run_time=1.1), FadeTransform(era, era := T(name, 36, C_BLUE).move_to(era), run_time=1.1)])
        self.say("z2", *steps)

        purposes = ["gods & kings", "the Church", "merchants", "the artist", "ideas, markets, the public"]
        self.say("z3", *[[dials.set_label("purpose", p), FadeTransform(era, era := T(p, 36, C_YELLOW).move_to(era))] for p in purposes])
        media = ["ochre", "bronze & marble", "oil paint", "photography", "industrial materials", "code"]
        self.say("z4", *[[dials.set_label("medium", m), FadeTransform(era, era := T(m, 36, C_RED).move_to(era))] for m in media])

        hand = hand_stencil().scale(1.1)
        self.say("z5", FadeOut(dials), FadeOut(era), LaggedStart(*[FadeIn(d) for d in hand], lag_ratio=0.002, run_time=3))
        screen = RoundedRectangle(corner_radius=0.2, width=4.5, height=2.8, color=C_BLUE, stroke_width=4)
        q = T("What should a picture do?", 48, C_YELLOW).to_edge(DOWN, buff=1.0)
        self.say("z6", Transform(hand, screen, run_time=2), Write(q))
        self.wait(1.5)
        self.play(FadeOut(hand), FadeOut(q), run_time=1.5)
        self.wait(1)
