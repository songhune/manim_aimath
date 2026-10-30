"""AI기초수학 — 교재 Chapter 9 편미분과 경사 하강법.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 09_편미분과 경사 하강법_강의용.pptx` 의
9.1 편미분 · 9.2 경사 하강법에 붙는 보조 영상 8편. 파일 이름은 앞 장과 같은 규칙이다(week07 = CH06, week10 = CH09).
10주차(2026-11-04 · 11-06) 수업. CH07 미분 · CH08 적분은 다루지 않고 CH06 다음에 바로 이 장을 한다(2026-10-30 결정).

수식보다 곡면과 등고선이 움직이는 그림으로 세운다.
- 다변수함수의 그래프는 곡면이고, 레벨집합 f = k 는 곡면을 높이 k 로 자른 자리를 바닥에 내린 선이다(정의 9-2 · 9-3 · 예제 9-3).
- 편도함수는 변수 하나만 남기고 자른 단면 곡선의 기울기다(정의 9-6).
- 방향도함수 D_u f = ∇f · u 는 그래디언트를 u 에 사영한 길이이고, u 가 ∇f 방향일 때 가장 크다(정리 9-3 · 9-6 · 예제 9-9).
- 연쇄법칙 1: 경로 위에서 f 가 일정하면 ∇f ⊥ 속도, dz/dt = 0 (정리 9-4 · 예제 9-10).
- 라그랑주 승수법: f 의 레벨집합(원)이 제약 g = 0(타원)에 접하는 곳에서 ∇f = λ∇g (정리 9-7 · 예제 9-13).
- 정부호: z = xᵀAx 의 곡면이 그릇(양의 정부호) · 뒤집힌 그릇(음의 정부호) · 안장(부정부호) (정의 9-10 · 정리 9-9 · 예제 9-16).
- 헤시안 판별: f = x² + 2xy + y³ 의 임계점 둘, (0,0) 은 안장점, (-2/3, 2/3) 은 극소점 (정리 9-10 · 예제 9-18).
- 경사 하강법: x_{k+1} = x_k − η∇f(x_k). η 가 크면 튄다 (9.2 · 응용).
값은 예제 9-3 · 9-9 · 9-10 · 9-13 · 9-16 · 9-18 의 것을 그대로 쓴다. 방향도함수 편은 점 (2, 1) 을 새로 골랐다
(예제 9-12 의 (1, 2) 는 ∇f = (2, 12) 라 화면에 들어가지 않는다).

곡면은 `ThreeDAxes.get_graph` 와 `SurfaceMesh` 로 그리고, 등고선은 이 파일의 `contour_lines` (marching squares) 로 그린다.
참고: legacy/_2016/eola 에는 다변수함수 편이 없다. 3차원 틀은 week04.py 의 LinearCombination(예제 3-4)과 같다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week10.py
    ./render.sh check _2026/aimath/week10.py
    ./render.sh ppt   _2026/aimath/week10.py SurfaceAndLevelSets
"""
from manim_imports_ext import *

from _2026.aimath.week04 import (
    INK, ACCENT, CALM, WARN, DONE, title, caption, code, slide_title, tag_under, box, plane, arrow,
)
from _2026.aimath.week07 import footnote


# ─────────────────────────────────────────────────────────────
# 공통 도구
# ─────────────────────────────────────────────────────────────
def axes3d(x_range, y_range, z_range, width=6.0, height=6.0, depth=4.0):
    """3차원 축과 x · y · z 글자."""
    ax = ThreeDAxes(x_range=x_range, y_range=y_range, z_range=z_range, width=width, height=height, depth=depth,
                    axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=False, include_ticks=False))
    labels = VGroup(Tex("x"), Tex("y"), Tex("z")).set_color(GREY_B)
    labels[0].next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
    labels[1].next_to(ax.y_axis.get_end(), UP, buff=0.1)
    labels[2].next_to(ax.z_axis.get_end(), OUT, buff=0.1)
    for lab in labels:
        lab.rotate(PI / 2, RIGHT)
    return ax, labels


def graph_surface(ax, func, u_range, v_range, color=BLUE_D, opacity=0.55, mesh=(17, 17), resolution=(81, 81)):
    """z = f(x, y) 곡면과 그 위의 격자선."""
    surface = ax.get_graph(func, color=color, opacity=opacity, u_range=u_range, v_range=v_range, resolution=resolution)
    lines = SurfaceMesh(surface, resolution=mesh, stroke_color=GREY_B, stroke_width=1)
    return surface, lines


def hud(scene, *mobs):
    """카메라가 돌아도 제자리에 있는 글(제목 · 패널 · 자막)."""
    for m in mobs:
        m.fix_in_frame()
    return mobs


def head3d(scene, text, tag):
    head = slide_title(text)
    t = tag_under(head, tag)
    hud(scene, head, t)
    scene.play(FadeIn(head), FadeIn(t), run_time=0.6)
    return head


def note3d(scene, text, color=GREY_B, shown=None):
    new = caption(text, 24, color).to_edge(DOWN, buff=0.5)
    new.fix_in_frame()
    if shown is None:
        scene.play(FadeIn(new, UP), run_time=0.4)
    else:
        scene.play(FadeOut(shown), FadeIn(new, UP), run_time=0.4)
    return new


def right_panel(scene, rows, width=4.6, shift=ORIGIN, fixed=True):
    panel = VGroup(*rows).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    panel.set_width(width).to_edge(RIGHT, buff=0.5).shift(shift)
    if fixed:
        panel.fix_in_frame()
    return panel


def contour_lines(func, x_range, y_range, levels, n=90):
    """f(x, y) = k 의 등고선을 marching squares 로 구한다. 결과는 {k: [((x0,y0),(x1,y1)), ...]}."""
    xs = np.linspace(x_range[0], x_range[1], n)
    ys = np.linspace(y_range[0], y_range[1], n)
    X, Y = np.meshgrid(xs, ys)
    Z = func(X, Y)
    out = {}
    for k in levels:
        segs = []
        for i in range(n - 1):
            for j in range(n - 1):
                corners = [(xs[j], ys[i], Z[i, j]), (xs[j + 1], ys[i], Z[i, j + 1]),
                           (xs[j + 1], ys[i + 1], Z[i + 1, j + 1]), (xs[j], ys[i + 1], Z[i + 1, j])]
                pts = []
                for a in range(4):
                    x0, y0, z0 = corners[a]
                    x1, y1, z1 = corners[(a + 1) % 4]
                    if (z0 - k) * (z1 - k) < 0:
                        t = (k - z0) / (z1 - z0)
                        pts.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
                if len(pts) == 2:
                    segs.append((pts[0], pts[1]))
                elif len(pts) == 4:
                    segs.append((pts[0], pts[1]))
                    segs.append((pts[2], pts[3]))
        out[k] = segs
    return out


def contour_group(p, func, x_range, y_range, levels, color=GREY_C, width=1.5, n=90):
    """등고선을 평면 p 위의 선분 묶음으로."""
    segs = contour_lines(func, x_range, y_range, levels, n)
    group = VGroup()
    for k in levels:
        lines = VGroup(*[Line(p.c2p(*a), p.c2p(*b)) for a, b in segs[k]])
        lines.set_stroke(color, width)
        group.add(lines)
    return group


# ─────────────────────────────────────────────────────────────
# 9.1 편미분
# ─────────────────────────────────────────────────────────────
class SurfaceAndLevelSets(InteractiveScene):
    """정의 9-2 · 9-3 · 예제 9-3. 그래프는 곡면, 레벨집합은 높이 k 로 자른 자리를 바닥에 내린 선이다.

    f(x, y) = √(25 − x² − y²) 는 반지름 5 의 반구다. f = k 는 x² + y² = 25 − k² 인 원이고,
    k = 1, 2, 3, 4, 5 에서 반지름은 √24, √21, 4, 3, 0 이다. 위에서 내려다보면 동심원이 된다.
    """
    ks = [1, 2, 3, 4, 5]

    def construct(self):
        head3d(self, "그래프와 레벨집합", "정의 9-2 · 9-3 · 예제 9-3")
        ax, labels = axes3d((-6, 6, 1), (-6, 6, 1), (0, 6, 1), width=6.4, height=6.4, depth=3.2)
        ax.shift(DOWN * 0.3)
        self.frame.reorient(-40, 62, 0, center=(0.2, 0.2, 0.6), height=10.5)
        self.play(FadeIn(ax), FadeIn(labels), run_time=0.6)

        surface = ax.get_parametric_surface(
            lambda r, t: [r * np.cos(t), r * np.sin(t), np.sqrt(max(25 - r * r, 0))],
            u_range=(0, 5), v_range=(0, TAU), color=BLUE_D, opacity=0.5, resolution=(41, 81))
        mesh = SurfaceMesh(surface, resolution=(11, 25), stroke_color=GREY_B, stroke_width=1)
        panel = right_panel(self, [
            Tex(R"f(x,y)=\sqrt{25-x^{2}-y^{2}}").set_color(ACCENT),
            Tex(R"f=k\ \Longleftrightarrow\ x^{2}+y^{2}=25-k^{2}").set_color(INK),
        ], width=4.4, shift=UP * 1.6)
        self.play(ShowCreation(surface), ShowCreation(mesh), FadeIn(panel[0]), run_time=1.6)
        shown = note3d(self, "그래프 · 반지름 5 의 반구")
        self.frame.add_updater(lambda f, dt: f.increment_theta(0.05 * dt))
        self.wait(0.8)

        self.play(FadeIn(panel[1]), run_time=0.5)
        shown = note3d(self, "높이 k 로 자른 자리 · 레벨집합", DONE, shown)
        rows = VGroup()
        rings, floors = VGroup(), VGroup()
        for k in self.ks:
            r = np.sqrt(25 - k * k)
            ring = ParametricCurve(lambda t, r=r, k=k: ax.c2p(r * np.cos(t), r * np.sin(t), k), t_range=(0, TAU, 0.05))
            ring.set_stroke(DONE, 3)
            floor = ParametricCurve(lambda t, r=r: ax.c2p(r * np.cos(t), r * np.sin(t), 0), t_range=(0, TAU, 0.05))
            floor.set_stroke(CALM, 2)
            row = Tex(R"k=%d:\ x^{2}+y^{2}=%d" % (k, 25 - k * k)).set_color(DONE if k == 3 else INK).scale(0.8)
            rows.add(row)
            rings.add(ring)
            floors.add(floor)
        rows.arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(panel, DOWN, buff=0.4).align_to(panel, LEFT)
        rows.fix_in_frame()
        for k, ring, floor, row in zip(self.ks, rings, floors, rows):
            if k == 5:
                dot = Dot(ax.c2p(0, 0, 5), color=DONE, radius=0.08)
                self.play(FadeIn(dot), FadeIn(row), run_time=0.5)
                continue
            self.play(ShowCreation(ring), FadeIn(row), run_time=0.7)
            self.play(TransformFromCopy(ring, floor), run_time=0.6)
        shown = note3d(self, "k = 3 · 반지름 4 인 원", DONE, shown)
        self.wait(1.0)

        self.frame.clear_updaters()
        self.play(self.frame.animate.reorient(0, 0, 0, center=(0.2, 0.2, 0.6), height=10.5), run_time=2.0)
        shown = note3d(self, "위에서 본 레벨집합 · 동심원", CALM, shown)
        self.wait(2)


class PartialDerivativeSlice(InteractiveScene):
    """정의 9-6. 편도함수는 변수 하나만 남기고 자른 단면 곡선의 기울기다.

    f(x, y) = x² + y² 를 평면 y = 2 로 자르면 z = x² + 4 이고 x = 1 에서 기울기 2 = ∂f/∂x(1, 2).
    평면 x = 1 로 자르면 z = 1 + y² 이고 y = 2 에서 기울기 4 = ∂f/∂y(1, 2). 둘을 모으면 ∇f(1, 2) = (2, 4).
    """

    def construct(self):
        head3d(self, "편도함수 · 단면의 기울기", "정의 9-6 · 예제 9-8 의 함수")
        ax, labels = axes3d((-2, 2, 1), (-2, 2, 1), (0, 9, 1), width=4.8, height=4.8, depth=3.6)
        ax.shift(DOWN * 0.8)
        self.frame.reorient(-50, 64, 0, center=(1.3, 0.2, 0.9), height=12.0)
        self.play(FadeIn(ax), FadeIn(labels), run_time=0.6)
        f = lambda x, y: x * x + y * y
        surface, mesh = graph_surface(ax, f, (-2, 2), (-2, 2), opacity=0.4, mesh=(9, 9))
        panel = right_panel(self, [
            Tex(R"f(x,y)=x^{2}+y^{2}").set_color(ACCENT),
            Tex(R"y=2:\ z=x^{2}+4").set_color(CALM),
            Tex(R"\frac{\partial f}{\partial x}=2x\ \to\ 2").set_color(CALM),
            Tex(R"x=1:\ z=1+y^{2}").set_color(DONE),
            Tex(R"\frac{\partial f}{\partial y}=2y\ \to\ 4").set_color(DONE),
            Tex(R"\nabla f(1,2)=(2,\,4)").set_color(INK),
        ], width=4.0, shift=UP * 0.6)
        self.play(ShowCreation(surface), ShowCreation(mesh), FadeIn(panel[0]), run_time=1.4)
        point = Dot(ax.c2p(1, 2, 5), color=WHITE, radius=0.08)
        self.play(FadeIn(point), run_time=0.4)
        shown = note3d(self, "점 (1, 2, 5) 위의 곡면")
        self.frame.add_updater(lambda fr, dt: fr.increment_theta(0.04 * dt))
        self.wait(0.6)

        # y = 2 로 자른다
        cut_y = ax.get_parametric_surface(lambda u, v: [u, 2, v], u_range=(-2, 2), v_range=(0, 9),
                                          color=CALM, opacity=0.18, resolution=(2, 2))
        curve_y = ParametricCurve(lambda x: ax.c2p(x, 2, x * x + 4), t_range=(-2, 2, 0.05)).set_stroke(CALM, 4)
        tangent_y = Line(ax.c2p(0.1, 2, 5 - 1.8), ax.c2p(1.9, 2, 5 + 1.8)).set_stroke(WHITE, 6)
        self.play(FadeIn(cut_y), FadeIn(panel[1]), run_time=0.7)
        self.play(ShowCreation(curve_y), run_time=0.9)
        shown = note3d(self, "y = 2 로 자른 단면", CALM, shown)
        self.play(ShowCreation(tangent_y), FadeIn(panel[2]), run_time=0.7)
        shown = note3d(self, "x 방향 기울기 2 · ∂f/∂x", CALM, shown)
        self.wait(1.0)

        # x = 1 로 자른다
        cut_x = ax.get_parametric_surface(lambda u, v: [1, u, v], u_range=(-2, 2), v_range=(0, 9),
                                          color=DONE, opacity=0.18, resolution=(2, 2))
        curve_x = ParametricCurve(lambda y: ax.c2p(1, y, 1 + y * y), t_range=(-2, 2, 0.05)).set_stroke(DONE, 4)
        tangent_x = Line(ax.c2p(1, 1.3, 5 - 2.8), ax.c2p(1, 2.0, 5 + 0.0)).set_stroke(WHITE, 6)
        self.play(cut_y.animate.set_opacity(0.06), tangent_y.animate.set_stroke(width=2), FadeIn(cut_x), FadeIn(panel[3]),
                  run_time=0.7)
        self.play(ShowCreation(curve_x), run_time=0.9)
        shown = note3d(self, "x = 1 로 자른 단면", DONE, shown)
        self.play(ShowCreation(tangent_x), FadeIn(panel[4]), run_time=0.7)
        shown = note3d(self, "y 방향 기울기 4 · ∂f/∂y", DONE, shown)
        self.wait(1.0)
        self.play(FadeIn(panel[5]), run_time=0.5)
        shown = note3d(self, "편도함수 둘을 모은 것 · 그래디언트", INK, shown)
        self.wait(2)
        self.frame.clear_updaters()


class GradientDirection(InteractiveScene):
    """정리 9-3 · 9-6 · 예제 9-9. 방향도함수 D_u f = ∇f · u 는 그래디언트를 u 에 사영한 길이다.

    f(x, y) = x² + y² 의 점 (2, 1) 에서 ∇f = (4, 2). u1 = (1, 0), u2 = (0, 1), u3 = (1, 1)/√2 에서
    D_u f = 4, 2, 3√2 ≈ 4.24. u 를 한 바퀴 돌리면 ∇f 방향에서 최대 |∇f| = 2√5 ≈ 4.47, 반대 방향에서 최소다.
    """
    a = (2.0, 1.0)
    grad = (4.0, 2.0)

    def construct(self):
        head = slide_title("방향도함수와 그래디언트")
        self.add(head)
        self.play(FadeIn(tag_under(head, "정리 9-3 · 9-6 · 예제 9-9 · 점 (2, 1)")))
        p = plane(x_range=(-1, 7, 1), y_range=(-1, 5, 1), height=5.1).move_to(LEFT * 2.9 + DOWN * 0.55)
        self.play(FadeIn(p), run_time=0.5)
        rings = VGroup(*[Circle(radius=np.sqrt(c)).set_stroke(GREY_C, 1.5) for c in (1, 2, 5, 9, 14)])
        for ring in rings:
            ring.scale(p.get_x_unit_size()).move_to(p.c2p(0, 0))
        self.play(FadeIn(rings), run_time=0.6)
        ax, ay = self.a
        gx, gy = self.grad
        point = Dot(p.c2p(ax, ay), color=WHITE, radius=0.07)
        g_arrow = arrow(p, (ax + gx, ay + gy), DONE, start=(ax, ay))
        g_lab = Tex(R"\nabla f=(4,2)").set_color(DONE).scale(0.85).next_to(g_arrow.get_end(), RIGHT, buff=0.12)
        panel = right_panel(self, [
            Tex(R"f=x^{2}+y^{2},\quad \nabla f=(2x,\,2y)").set_color(ACCENT),
            Tex(R"D_{\mathbf{u}}f=\nabla f\cdot\mathbf{u}").set_color(INK),
            Tex(R"\mathbf{u}_1=(1,0):\ 4").set_color(CALM),
            Tex(R"\mathbf{u}_2=(0,1):\ 2").set_color(CALM),
            Tex(R"\mathbf{u}_3=\tfrac{1}{\sqrt2}(1,1):\ 3\sqrt2\approx4.24").set_color(CALM),
            Tex(R"\max D_{\mathbf{u}}f=\lVert\nabla f\rVert=2\sqrt5\approx4.47").set_color(DONE),
        ], width=4.3, shift=UP * 0.3, fixed=False)
        self.play(FadeIn(point), FadeIn(panel[0]), run_time=0.5)
        shown = footnote(self, "레벨집합은 원 · 점 (2, 1)")
        self.play(GrowArrow(g_arrow), FadeIn(g_lab), run_time=0.8)
        shown = footnote(self, "그래디언트 · 원에 수직", DONE, shown)
        self.wait(0.6)

        self.play(FadeIn(panel[1]), run_time=0.5)
        us = [((1, 0), panel[2]), ((0, 1), panel[3]), ((1 / np.sqrt(2), 1 / np.sqrt(2)), panel[4])]
        shown = footnote(self, "단위벡터 u 에 사영한 길이", CALM, shown)
        for (ux, uy), row in us:
            u_arrow = arrow(p, (ax + ux, ay + uy), CALM, start=(ax, ay))
            d = gx * ux + gy * uy
            proj = Line(p.c2p(ax, ay), p.c2p(ax + d * ux, ay + d * uy)).set_stroke(CALM, 8, opacity=0.5)
            drop = DashedLine(p.c2p(ax + gx, ay + gy), p.c2p(ax + d * ux, ay + d * uy)).set_stroke(GREY_B, 2)
            self.play(GrowArrow(u_arrow), run_time=0.5)
            self.play(ShowCreation(drop), ShowCreation(proj), FadeIn(row), run_time=0.7)
            self.wait(0.5)
            self.play(FadeOut(u_arrow), FadeOut(drop), FadeOut(proj), run_time=0.3)

        # u 를 한 바퀴 돌린다
        theta = ValueTracker(0.0)
        norm = np.hypot(gx, gy)

        def unit():
            t = theta.get_value()
            return np.cos(t), np.sin(t)

        u_arrow = always_redraw(lambda: arrow(p, (ax + unit()[0], ay + unit()[1]), CALM, start=(ax, ay)))
        proj = always_redraw(lambda: Line(
            p.c2p(ax, ay), p.c2p(ax + (gx * unit()[0] + gy * unit()[1]) * unit()[0],
                                 ay + (gx * unit()[0] + gy * unit()[1]) * unit()[1])).set_stroke(CALM, 8, opacity=0.5))
        value = DecimalNumber(0, num_decimal_places=2).set_color(CALM)
        value.add_updater(lambda m: m.set_value(gx * unit()[0] + gy * unit()[1]))
        v_lab = Tex(R"D_{\mathbf{u}}f=").set_color(CALM)
        v_group = VGroup(v_lab, value).arrange(RIGHT, buff=0.15).next_to(panel, DOWN, buff=0.4).align_to(panel, LEFT)
        value.add_updater(lambda m: m.next_to(v_lab, RIGHT, buff=0.15))
        self.add(proj, u_arrow, v_group)
        shown = footnote(self, "u 를 돌리면 값이 변함", CALM, shown)
        self.play(theta.animate.set_value(np.arctan2(gy, gx)), run_time=2.0)
        self.play(FadeIn(panel[5]), run_time=0.5)
        shown = footnote(self, "∇f 방향에서 최대 · 값 |∇f|", DONE, shown)
        self.wait(1.0)
        self.play(theta.animate.set_value(np.arctan2(gy, gx) + PI), run_time=2.2)
        shown = footnote(self, "반대 방향에서 최소 · −|∇f|", WARN, shown)
        self.wait(1.0)
        self.play(theta.animate.set_value(np.arctan2(gy, gx) + PI / 2), run_time=1.2)
        shown = footnote(self, "원을 따라가면 0 · 변화 없음", GREY_B, shown)
        self.wait(2)


class ChainRuleCurve(InteractiveScene):
    """정리 9-4 · 예제 9-10(a). 경로를 따라가면 dz/dt = ∂f/∂x · dx/dt + ∂f/∂y · dy/dt 다.

    z = x² + y², x = cos t, y = sin t. 경로는 단위원이고 그 위에서 f 는 1 로 일정하다.
    ∇f = (2x, 2y) 는 반지름 방향, 속도 (dx/dt, dy/dt) = (−sin t, cos t) 는 접선 방향이라 내적이 0 이다.
    """

    def construct(self):
        head = slide_title("연쇄법칙 · 경로 위의 변화율")
        self.add(head)
        self.play(FadeIn(tag_under(head, "정리 9-4 · 예제 9-10 (a)")))
        p = plane(x_range=(-2, 2, 1), y_range=(-2, 2, 1), height=5.2).move_to(LEFT * 3.2 + DOWN * 0.5)
        self.play(FadeIn(p), run_time=0.5)
        rings = VGroup(*[Circle(radius=np.sqrt(c)).set_stroke(GREY_C, 1.5) for c in (0.25, 1, 2.25, 4)])
        for ring in rings:
            ring.scale(p.get_x_unit_size()).move_to(p.c2p(0, 0))
        path = Circle(radius=1).scale(p.get_x_unit_size()).move_to(p.c2p(0, 0)).set_stroke(DONE, 4)
        panel = right_panel(self, [
            Tex(R"z=f(x,y)=x^{2}+y^{2}").set_color(ACCENT),
            Tex(R"x=\cos t,\quad y=\sin t").set_color(DONE),
            Tex(R"\frac{dz}{dt}=\frac{\partial f}{\partial x}\frac{dx}{dt}+\frac{\partial f}{\partial y}\frac{dy}{dt}").set_color(INK),
            Tex(R"=2x(-\sin t)+2y(\cos t)").set_color(INK),
            Tex(R"=-2\cos t\sin t+2\sin t\cos t=0").set_color(DONE),
        ], width=5.2, shift=UP * 0.4, fixed=False)
        self.play(FadeIn(rings), FadeIn(panel[0]), run_time=0.6)
        shown = footnote(self, "레벨집합 · 원")
        self.play(ShowCreation(path), FadeIn(panel[1]), run_time=0.9)
        shown = footnote(self, "경로 · 단위원 위를 돎", DONE, shown)
        self.wait(0.5)

        t = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(p.c2p(np.cos(t.get_value()), np.sin(t.get_value())), color=WHITE, radius=0.07))
        grad = always_redraw(lambda: arrow(
            p, (2 * np.cos(t.get_value()), 2 * np.sin(t.get_value())), CALM,
            start=(np.cos(t.get_value()), np.sin(t.get_value()))))
        vel = always_redraw(lambda: arrow(
            p, (np.cos(t.get_value()) - np.sin(t.get_value()), np.sin(t.get_value()) + np.cos(t.get_value())), DONE,
            start=(np.cos(t.get_value()), np.sin(t.get_value()))))
        g_lab = Tex(R"\nabla f").set_color(CALM).scale(0.8)
        g_lab.add_updater(lambda m: m.next_to(grad.get_end(), UR, buff=0.05))
        v_lab = Tex(R"(x',y')").set_color(DONE).scale(0.8)
        v_lab.add_updater(lambda m: m.next_to(vel.get_end(), UL, buff=0.05))
        self.add(grad, vel, dot, g_lab, v_lab)
        self.play(FadeIn(panel[2]), run_time=0.5)
        shown = footnote(self, "∇f 는 반지름 · 속도는 접선", CALM, shown)
        self.play(t.animate.set_value(TAU * 0.75), run_time=4.0, rate_func=linear)
        self.play(FadeIn(panel[3]), run_time=0.5)
        self.play(FadeIn(panel[4]), run_time=0.5)
        shown = footnote(self, "∇f ⊥ 속도 · dz/dt = 0", DONE, shown)
        self.play(t.animate.set_value(TAU * 1.25), run_time=2.5, rate_func=linear)
        shown = footnote(self, "경로 위에서 f = 1 로 일정", DONE, shown)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9.2 경사 하강법
# ─────────────────────────────────────────────────────────────
class LagrangeTangency(InteractiveScene):
    """정리 9-7 · 예제 9-13. 제약 g = 0 위에서 f 의 최댓값 · 최솟값은 f 의 레벨집합이 제약 곡선에 접하는 곳이다.

    f = x² + y² 의 레벨집합은 원, g = 3x² + 4y² − 5 = 0 은 타원. 원을 키우면 (0, ±√5/2) 에서 처음 닿고(최솟값 5/4),
    (±√(5/3), 0) 에서 마지막으로 닿는다(최댓값 5/3). 접점에서 ∇f = λ∇g 이고 λ = 1/4, 1/3 이다.
    """

    def construct(self):
        head = slide_title("라그랑주 승수법 · 접하는 자리")
        self.add(head)
        self.play(FadeIn(tag_under(head, "정리 9-7 · 예제 9-13")))
        p = plane(x_range=(-2, 2, 1), y_range=(-1.5, 1.5, 0.5), height=4.6).move_to(LEFT * 3.1 + DOWN * 0.5)
        self.play(FadeIn(p), run_time=0.5)
        unit = p.get_x_unit_size()
        ellipse = Ellipse(width=2 * np.sqrt(5 / 3) * unit, height=2 * np.sqrt(5 / 4) * unit).move_to(p.c2p(0, 0))
        ellipse.set_stroke(DONE, 4)
        panel = right_panel(self, [
            Tex(R"f(x,y)=x^{2}+y^{2}").set_color(ACCENT),
            Tex(R"g(x,y)=3x^{2}+4y^{2}-5=0").set_color(DONE),
            Tex(R"\nabla f=\lambda\nabla g").set_color(INK),
            Tex(R"(2x,2y)=\lambda(6x,8y)").set_color(INK),
            Tex(R"\min f=\tfrac54:\ (0,\pm\tfrac{\sqrt5}{2}),\ \lambda=\tfrac14").set_color(CALM),
            Tex(R"\max f=\tfrac53:\ (\pm\sqrt{\tfrac53},0),\ \lambda=\tfrac13").set_color(WARN),
        ], width=5.0, shift=UP * 0.3, fixed=False)
        self.play(ShowCreation(ellipse), FadeIn(panel[0]), FadeIn(panel[1]), run_time=0.9)
        shown = footnote(self, "제약 g = 0 · 타원", DONE)

        r = ValueTracker(0.5)
        circle = always_redraw(lambda: Circle(radius=r.get_value() * unit).move_to(p.c2p(0, 0)).set_stroke(ACCENT, 3))
        r_lab = Tex(R"x^{2}+y^{2}=r^{2}").set_color(ACCENT).scale(0.8)
        r_lab.add_updater(lambda m: m.next_to(circle, DOWN, buff=0.1).shift(RIGHT * 0.2))
        self.add(circle, r_lab)
        shown = footnote(self, "f 의 레벨집합 · 원을 키움", ACCENT, shown)
        rmin, rmax = np.sqrt(5 / 4), np.sqrt(5 / 3)
        self.play(r.animate.set_value(rmin), run_time=2.0)
        pts_min = [p.c2p(0, rmin), p.c2p(0, -rmin)]
        dots_min = VGroup(*[Dot(q, color=CALM, radius=0.08) for q in pts_min])
        gf = arrow(p, (0, rmin + 0.35), CALM, start=(0, rmin))
        gg = arrow(p, (0, rmin + 0.7), DONE, start=(0, rmin)).set_stroke(opacity=0.6)
        self.play(FadeIn(dots_min), run_time=0.4)
        shown = footnote(self, "처음 닿는 곳 · 최솟값 5/4", CALM, shown)
        self.play(GrowArrow(gg), GrowArrow(gf), FadeIn(panel[2]), FadeIn(panel[3]), run_time=0.8)
        shown = footnote(self, "접점에서 ∇f ∥ ∇g · λ = 1/4", CALM, shown)
        self.play(FadeIn(panel[4]), run_time=0.5)
        self.wait(1.0)

        self.play(FadeOut(gf), FadeOut(gg), run_time=0.3)
        self.play(r.animate.set_value(rmax), run_time=2.0)
        dots_max = VGroup(*[Dot(p.c2p(s * rmax, 0), color=WARN, radius=0.08) for s in (1, -1)])
        gf2 = arrow(p, (rmax + 0.35, 0), WARN, start=(rmax, 0))
        gg2 = arrow(p, (rmax + 0.7, 0), DONE, start=(rmax, 0)).set_stroke(opacity=0.6)
        self.play(FadeIn(dots_max), run_time=0.4)
        shown = footnote(self, "마지막으로 닿는 곳 · 최댓값 5/3", WARN, shown)
        self.play(GrowArrow(gg2), GrowArrow(gf2), FadeIn(panel[5]), run_time=0.8)
        shown = footnote(self, "∇f = λ∇g · λ = 1/3", WARN, shown)
        self.wait(1.0)
        self.play(r.animate.set_value(rmax + 0.4), run_time=1.0)
        shown = footnote(self, "더 키우면 타원과 떨어짐", GREY_B, shown)
        self.wait(2)


class QuadraticFormBowl(InteractiveScene):
    """정의 9-10 · 정리 9-9 · 예제 9-16 · 9-17. z = xᵀAx 의 곡면으로 정부호를 본다.

    A = [[1,0],[0,2]] 는 z = x² + 2y² 그릇(고윳값 1, 2 > 0 · 양의 정부호),
    B = [[−1,1],[1,−2]] 는 z = −x² + 2xy − 2y² 뒤집힌 그릇(고윳값 (−3 ± √5)/2 < 0 · 음의 정부호),
    C = [[1,0],[0,−1]] 은 z = x² − y² 안장(고윳값 1, −1 · 부정부호). 정리 9-9 는 고윳값의 부호가 곧 곡면의 모양이라는 말이다.
    """

    def construct(self):
        head3d(self, "정부호 행렬 · 곡면의 모양", "정의 9-10 · 정리 9-9 · 예제 9-16")
        ax, labels = axes3d((-1.2, 1.2, 1), (-1.2, 1.2, 1), (-5, 3.5, 1), width=4.6, height=4.6, depth=4.8)
        ax.shift(DOWN * 0.3)
        self.frame.reorient(-45, 66, 0, center=(1.0, 0.6, -0.6), height=11.5)
        self.play(FadeIn(ax), FadeIn(labels), run_time=0.6)
        self.frame.add_updater(lambda fr, dt: fr.increment_theta(0.05 * dt))

        cases = [
            (lambda x, y: x * x + 2 * y * y, ACCENT,
             [Tex(R"A=\begin{bmatrix}1&0\\0&2\end{bmatrix}").set_color(ACCENT),
              Tex(R"\mathbf{x}^{T}A\mathbf{x}=x^{2}+2y^{2}>0").set_color(INK),
              Tex(R"\lambda=1,\,2>0").set_color(INK)],
             "양의 정부호 · 그릇", "고윳값 모두 양수 (정리 9-9)"),
            (lambda x, y: -x * x + 2 * x * y - 2 * y * y, WARN,
             [Tex(R"B=\begin{bmatrix}-1&1\\1&-2\end{bmatrix}").set_color(WARN),
              Tex(R"\mathbf{x}^{T}B\mathbf{x}=-(x-y)^{2}-y^{2}<0").set_color(INK),
              Tex(R"\lambda=\tfrac{-3\pm\sqrt5}{2}<0").set_color(INK)],
             "음의 정부호 · 뒤집힌 그릇", "고윳값 모두 음수"),
            (lambda x, y: x * x - y * y, CALM,
             [Tex(R"C=\begin{bmatrix}1&0\\0&-1\end{bmatrix}").set_color(CALM),
              Tex(R"\mathbf{x}^{T}C\mathbf{x}=x^{2}-y^{2}").set_color(INK),
              Tex(R"\lambda=1,\,-1").set_color(INK)],
             "부정부호 · 안장", "부호가 섞임 · 정리 9-10 (3)"),
        ]
        surface = mesh = panel = shown = None
        for func, color, rows, cap1, cap2 in cases:
            new_s, new_m = graph_surface(ax, func, (-1, 1), (-1, 1), color=color, opacity=0.55, mesh=(11, 11))
            new_panel = right_panel(self, rows, width=4.2, shift=UP * 1.4)
            if surface is None:
                self.play(ShowCreation(new_s), ShowCreation(new_m), FadeIn(new_panel), run_time=1.4)
                shown = note3d(self, cap1, color)
            else:
                self.play(Transform(surface, new_s), Transform(mesh, new_m), FadeOut(panel), FadeIn(new_panel), run_time=1.6)
                shown = note3d(self, cap1, color, shown)
                new_s, new_m = surface, mesh
            surface, mesh, panel = new_s, new_m, new_panel
            self.wait(0.8)
            shown = note3d(self, cap2, GREY_B, shown)
            self.wait(1.4)
        self.wait(1.0)
        self.frame.clear_updaters()


class HessianCritical(InteractiveScene):
    """정리 9-10 · 예제 9-18. ∇f = 0 인 점에서 헤시안의 정부호가 극대 · 극소 · 안장점을 가른다.

    f = x² + 2xy + y³. ∇f = (2x + 2y, 2x + 3y²) = 0 → (0, 0), (−2/3, 2/3).
    H = [[2, 2], [2, 6y]]. (0, 0) 에서 det H = −4 < 0 → 안장점. (−2/3, 2/3) 에서 H = [[2,2],[2,4]], 양의 정부호 → 극소점.
    등고선으로 보면 안장점은 X 자로 교차하는 선, 극소점은 닫힌 고리다. 등고선은 씬 안에서 계산한다(하네스 3.8).
    """

    def construct(self):
        head = slide_title("헤시안 판별 · 안장점과 극소점")
        self.add(head)
        self.play(FadeIn(tag_under(head, "정리 9-10 · 예제 9-18")))
        xr, yr = (-1.5, 0.9), (-0.9, 1.5)
        p = plane(x_range=(-1.5, 1.0, 0.5), y_range=(-1.0, 1.5, 0.5), height=5.2).move_to(LEFT * 3.2 + DOWN * 0.5)
        self.play(FadeIn(p), run_time=0.5)
        f = lambda x, y: x * x + 2 * x * y + y ** 3
        levels = [-0.13, -0.1, -0.06, 0.0, 0.1, 0.3, 0.6, 1.0, 1.6]
        contours = contour_group(p, f, xr, yr, levels, color=GREY_C, width=1.5, n=110)
        zero = contour_group(p, f, xr, yr, [0.0], color=WARN, width=2.5, n=110)
        panel = right_panel(self, [
            Tex(R"f=x^{2}+2xy+y^{3}").set_color(ACCENT),
            Tex(R"\nabla f=(2x+2y,\ 2x+3y^{2})=\mathbf{0}").set_color(INK),
            Tex(R"(0,0),\quad(-\tfrac23,\tfrac23)").set_color(DONE),
            Tex(R"H=\begin{bmatrix}2&2\\2&6y\end{bmatrix}").set_color(INK),
            Tex(R"(0,0):\ \det H=-4<0").set_color(WARN),
            Tex(R"(-\tfrac23,\tfrac23):\ H=\begin{bmatrix}2&2\\2&4\end{bmatrix}>0").set_color(CALM),
        ], width=5.3, shift=UP * 0.3, fixed=False)
        self.play(FadeIn(contours), FadeIn(panel[0]), run_time=0.9)
        shown = footnote(self, "등고선 · f 의 레벨집합")
        self.play(FadeIn(panel[1]), run_time=0.5)
        self.play(FadeIn(panel[2]), run_time=0.5)
        saddle = Dot(p.c2p(0, 0), color=WARN, radius=0.09)
        minimum = Dot(p.c2p(-2 / 3, 2 / 3), color=CALM, radius=0.09)
        self.play(FadeIn(saddle), FadeIn(minimum), run_time=0.5)
        shown = footnote(self, "임계점 둘 · ∇f = 0", DONE, shown)
        self.wait(0.6)

        self.play(FadeIn(panel[3]), run_time=0.5)
        self.play(ShowCreation(zero), FadeIn(panel[4]), run_time=1.0)
        shown = footnote(self, "X 자 교차 · 안장점", WARN, shown)
        self.wait(1.0)
        ring = contour_group(p, f, xr, yr, [-0.13, -0.1], color=CALM, width=2.5, n=110)
        self.play(ShowCreation(ring), FadeIn(panel[5]), run_time=1.0)
        shown = footnote(self, "닫힌 고리 · 극소점 (−2/3, 2/3)", CALM, shown)
        self.wait(1.0)
        shown = footnote(self, "헤시안의 정부호가 모양을 정함", INK, shown)
        self.wait(2)


class GradientDescentSteps(InteractiveScene):
    """9.2 · 응용. 경사 하강법 x_{k+1} = x_k − η∇f(x_k) 는 −∇f 쪽으로 한 걸음씩 간다.

    f = x² + 4y², ∇f = (2x, 8y). x_0 = (4, 2). η = 0.1 이면 x 는 0.8 배, y 는 0.2 배씩 줄어 (0, 0) 으로 간다.
    η = 0.3 이면 y 는 −1.4 배가 되어 튄다. 정리 9-6 의 '가장 빨리 감소하는 방향' 이 −∇f 다. 값은 씬 안에서 계산한다.
    """
    x0 = np.array([4.0, 2.0])
    steps = 8

    def construct(self):
        head = slide_title("경사 하강법 · 한 걸음씩")
        self.add(head)
        self.play(FadeIn(tag_under(head, "정리 9-6 · 응용 · f = x² + 4y²")))
        p = plane(x_range=(-1, 5, 1), y_range=(-3, 3, 1), height=5.2).move_to(LEFT * 3.1 + DOWN * 0.5)
        self.play(FadeIn(p), run_time=0.5)
        unit = p.get_x_unit_size()
        rings = VGroup(*[Ellipse(width=2 * np.sqrt(c) * unit, height=np.sqrt(c) * unit).move_to(p.c2p(0, 0))
                         .set_stroke(GREY_C, 1.5) for c in (1, 4, 9, 16, 25, 32)])
        self.play(FadeIn(rings), run_time=0.6)
        panel = right_panel(self, [
            Tex(R"f=x^{2}+4y^{2},\quad \nabla f=(2x,\,8y)").set_color(ACCENT),
            Tex(R"\mathbf{x}_{k+1}=\mathbf{x}_k-\eta\,\nabla f(\mathbf{x}_k)").set_color(INK),
            Tex(R"\eta=0.1:\ (4,2)\to(3.2,0.4)\to(2.56,0.08)").set_color(DONE),
            Tex(R"\eta=0.3:\ (4,2)\to(1.6,-2.8)\to(0.64,3.92)").set_color(WARN),
        ], width=5.4, shift=UP * 0.8, fixed=False)
        self.play(FadeIn(panel[0]), FadeIn(panel[1]), run_time=0.6)
        shown = footnote(self, "레벨집합 · 타원")

        def run(eta, color, n):
            x = self.x0.copy()
            trail = VGroup()
            dot = Dot(p.c2p(*x), color=color, radius=0.08)
            self.play(FadeIn(dot), run_time=0.3)
            for _ in range(n):
                g = np.array([2 * x[0], 8 * x[1]])
                nx = x - eta * g
                if abs(nx[1]) > 2.9 or abs(nx[0]) > 4.9:
                    break
                step = arrow(p, tuple(nx), color, start=tuple(x))
                self.play(GrowArrow(step), dot.animate.move_to(p.c2p(*nx)), run_time=0.5)
                trail.add(step)
                x = nx
            return VGroup(trail, dot)

        shown = footnote(self, "η = 0.1 · −∇f 쪽으로 한 걸음", DONE, shown)
        first = run(0.1, DONE, self.steps)
        self.play(FadeIn(panel[2]), run_time=0.5)
        shown = footnote(self, "원점으로 다가감 · 최솟값", DONE, shown)
        self.wait(1.0)
        self.play(first.animate.set_opacity(0.3), run_time=0.4)

        shown = footnote(self, "η = 0.3 · 걸음이 큼", WARN, shown)
        run(0.3, WARN, 4)
        self.play(FadeIn(panel[3]), run_time=0.5)
        shown = footnote(self, "y 방향이 튐 · η 는 작게", WARN, shown)
        self.wait(2)
