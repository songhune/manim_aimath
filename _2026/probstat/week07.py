# -*- coding: utf-8 -*-
"""확률과통계 「연속형 확률분포」 장 (Walpole Chapter 6) — 균등 · 정규 · 정규근사 · 감마 · 지수 · 로그정규.

강의 교안 `확률과통계/교육메모/09주차.md`(12차) · `10주차.md`(13차) 의 「영상 태그」 를 옮긴 것이다.
도구와 규칙은 week06.py 와 같다. 개념 영상은 정의 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음 ·
풀이 슬라이드 앞이다(하네스 3.6). 소재는 덱(PS1_06_restyled.pptx, 레이아웃 정리 뒤 88장)의 정의와
예제로 한정한다. 화면 문구는 영어, 여섯 낱말까지.

이 장은 예제 스물넷을 다 그리지 않는다(2026-10-10, 사용자 결정 — "전부 다 말고 꼭 해야 하는 내용만").
식에 수만 넣는 예제는 풀이 판과 교안으로 넘기고, **그림이 있어야 보이는 것**만 골랐다:
분포마다 모양이 어디서 오는지(개념 8편)와, 표 읽기 · 양쪽 꼬리 · 역방향 · 연속성 보정 · 대기 시간처럼
넓이를 칠해야 보이는 예제 6편. 사용자 요구(2026-10-10): 계산 공식보다 시각화, 명사 나열보다 아이콘.
그래서 사람은 치토, 물건은 아이콘(배터리 · 베어링 · 전화)으로 그리고, 확률은 무리 가운데 색이 바뀐
개체의 비율로 한 번 더 보인다.

이 장의 약속:
    개념 영상은 분포의 이름과 식을 먼저 걸고, 매개변수를 트래커로 움직여 모양이 따라 변하는 것을 보인다.
    예제 영상은 풀이 단계를 먼저 목록으로 걸어 두고(`steps_panel`) 한 단계씩 진행한다.
    정규분포의 넓이는 항상 "왼쪽 넓이" 로 돌아간다(표 A.3). 오른쪽은 1 에서 빼고, 사이는 둘의 차다.

덱 삽입 자리 (원본 PS1_06_restyled.pptx 88장 기준 — 2026-10-10 도구/레이아웃_정리_PS1_06.py 로 67장을 정리한 것.
insert_videos.py 의 PS1_06_INSERT 와 같다. "N 앞" 은 개념 영상, "N 뒤" 는 예제 영상(풀이 앞)):
    12차 10/16 — 6.1 균등, 6.2–6.4 정규, 6.5 정규근사 (원본 1–48)
    UniformDensity                   3 앞    연속균등분포 정의 (평평한 밀도, 넓이 1, 구간 비율)
    NormalCurveShape                 6 앞    정규분포 정의 (μ 가 옮기고 σ 가 벌린다, 변곡점 μ ± σ)
    StandardizeToZ                  12 앞    표준화 · 표 A.3 의 왼쪽 넓이 (6.3 절)
    Example62TableA3                14 뒤    예제 6.2 (표 A.3 읽기, 풀이 15)
    Example67Battery                25 뒤    예제 6.7 (배터리 수명 < 2.3 년, 풀이 26)
    Example69Bearings               29 뒤    예제 6.9 (규격 밖 양쪽 꼬리, 풀이 30)
    Example613Grades                37 뒤    예제 6.13 (위 12 % 의 경계, 풀이 38)
    NormalApproximatesBinomial      41 앞    정리 6.3 (막대 위에 곡선, 연속성 보정)
    Example615Recovery              46 뒤    예제 6.15 (100 명 가운데 30 명 미만, 풀이 47)
    13차 10/27 — 6.6 감마 · 지수, 6.7–6.10 (원본 49–88)
    GammaFamily                     50 앞    감마분포 정의 (α · β 와 모양, α = 1 지수, 카이제곱)
    PoissonToExponential            53 앞    포아송 과정과의 관계 (첫 사건까지의 시간)
    MemorylessExponential           60 앞    무기억성 (꼬리를 잘라 다시 재면 같은 곡선)
    Example618Calls                 63 뒤    예제 6.18 (전화 두 통까지 1분, 풀이 64)
    LognormalFromNormal             76 앞    로그정규분포 정의 (ln X 가 정규)

참고: legacy/_2023/clt/main.py (BuildUpGaussian — 막대 위 곡선, 정규 모양 쌓기),
      legacy/_2020/beta/beta1.py (밀도 곡선과 넓이 칠하기), legacy/_2018/eop (시행 흩뿌리기).

렌더 (저장소 루트에서, 한 번에 한 프로세스만):
    ./render.sh check _2026/probstat/week07.py
    ./render.sh ppt   _2026/probstat/week07.py UniformDensity
"""
import math
from math import comb, exp, sqrt

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN,
    chito, crowd, label, note, panel, ring, slide_title, bar,
)
from _2026.probstat.week04 import density_axes, area_under, x_marks
from _2026.probstat.week05 import steps_panel, column, dashed, fulcrum_at
from _2026.probstat.week06 import binom_pmf, axis, chart, paint


# ─────────────────────────────────────────────────────────────
# 도구 — 분포, 표 조각, 아이콘
# ─────────────────────────────────────────────────────────────
def npdf(x, mu=0.0, sig=1.0):
    return math.exp(-0.5 * ((x - mu) / sig) ** 2) / (sig * math.sqrt(2 * math.pi))


def ncdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def gamma_pdf(x, a, b):
    if x <= 0:
        return 0.0
    return x ** (a - 1) * math.exp(-x / b) / (b ** a * math.gamma(a))


def normal_graph(axes, mu, sig, lo, hi, color=ACCENT, width=3):
    return axes.get_graph(lambda x: npdf(x, mu, sig), x_range=(lo, hi, 0.02)).set_stroke(color, width)


def table_row(z_head, cols, values, hit, pos, scale=0.5, w=0.78, h=0.42):
    """표 A.3 의 한 줄. 머리글 줄(.00 .01 …)과 z 줄, 읽은 칸을 테두리로 표시한다.
    돌려주는 것: (전체 VGroup, 읽은 칸의 사각형)."""
    grid = VGroup()
    heads = [Tex("z").scale(scale).set_color(GREY_B)] + [Tex(c).scale(scale).set_color(GREY_B) for c in cols]
    row = [Tex(z_head).scale(scale).set_color(INK)] + [Tex(v).scale(scale).set_color(INK) for v in values]
    cells = {}
    for r, line in enumerate((heads, row)):
        for c, t in enumerate(line):
            rect = Rectangle(width=w, height=h).set_stroke(GREY_C, 1)
            rect.move_to([c * w, -r * h, 0])
            t.move_to(rect)
            cells[(r, c)] = rect
            grid.add(rect, t)
    grid.move_to(pos)
    box = SurroundingRectangle(cells[(1, hit + 1)], buff=0.0).set_stroke(MEAN_COLOR, 3)
    src = note("Table A.3", 20, GREY_B).next_to(grid, UP, buff=0.12).align_to(grid, LEFT)
    return VGroup(grid, src), box


def battery(height=0.34, color=ACCENT, level=0.75):
    body = RoundedRectangle(width=0.9, height=0.42, corner_radius=0.07).set_stroke(color, 2.5).set_fill(BLACK, 1)
    nub = Rectangle(width=0.09, height=0.18).set_fill(color, 1).set_stroke(width=0)
    nub.next_to(body, RIGHT, buff=0)
    juice = Rectangle(width=0.74 * level, height=0.28).set_fill(color, 0.55).set_stroke(width=0)
    juice.align_to(body, LEFT).shift(RIGHT * 0.08)
    g = VGroup(body, juice, nub)
    return g.scale(height / 0.42)


def bearing(radius=0.2, color=ACCENT):
    outer = Circle(radius=radius).set_stroke(color, 2.5)
    inner = Circle(radius=radius * 0.42).set_stroke(color, 2)
    balls = VGroup(*[Dot(radius=radius * 0.13).set_fill(color, 1).move_to(
        [radius * 0.71 * math.cos(t), radius * 0.71 * math.sin(t), 0]) for t in np.linspace(0, TAU, 7)[:-1]])
    return VGroup(outer, inner, balls)


def phone(height=0.5, color=ACCENT):
    body = RoundedRectangle(width=0.3, height=0.52, corner_radius=0.06).set_stroke(color, 2.5).set_fill(BLACK, 1)
    screen = Rectangle(width=0.22, height=0.36).set_fill(color, 0.45).set_stroke(width=0).move_to(body).shift(UP * 0.02)
    home = Dot(radius=0.025).set_fill(color, 1).move_to(body.get_bottom() + UP * 0.05)
    return VGroup(body, screen, home).scale(height / 0.52)


def frozen(mob):
    """always_redraw 개체의 정지 사본. 트래커를 따라가는 개체를 그대로 FadeIn · ShowCreation 하면 애니메이션 도중
    점 개수가 바뀌어 broadcast 오류가 난다(2026-10-10). 사본을 보이고 나서 진짜를 add 한다."""
    c = mob.copy()
    c.clear_updaters()
    return c


def tails(axes, graph, lo, hi, a, b, color=WARN, opacity=0.6):
    """a 왼쪽과 b 오른쪽, 양쪽 꼬리."""
    return VGroup(area_under(axes, graph, lo, a, color, opacity), area_under(axes, graph, b, hi, color, opacity))


# ─────────────────────────────────────────────────────────────
# 1. 연속균등분포 — 슬라이드 3 (6.1 정의) 앞
# ─────────────────────────────────────────────────────────────
class UniformDensity(InteractiveScene):
    """이름: f(x; A, B) = 1/(B − A). 교재 그림 6.1 의 [1, 3] 에서 시작한다. 높이 1/(B−A) 인 직사각형이라
    넓이가 1 이고, 구간을 넓히면 그만큼 낮아진다(트래커). 확률은 밑변의 비율, 평균은 가운데(정리 6.1)."""

    def construct(self):
        head = slide_title("Continuous Uniform Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"f(x;\,A,B) = \frac{1}{B - A},\quad A \le x \le B").scale(0.8).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.7)
        self.play(Write(name))

        axes = density_axes((0, 5, 1), (0, 1.1, 0.5), width=8.0, height=3.4).move_to([-2.6, -0.9, 0])
        A, B = ValueTracker(1.0), ValueTracker(3.0)

        def box():
            a, b = A.get_value(), B.get_value()
            r = Polygon(axes.c2p(a, 0), axes.c2p(a, 1 / (b - a)), axes.c2p(b, 1 / (b - a)), axes.c2p(b, 0))
            return r.set_stroke(ACCENT, 3).set_fill(ACCENT, 0.3)
        rect = always_redraw(box)
        a_tag = Tex("A").scale(0.7).set_color(GREY_B)
        b_tag = Tex("B").scale(0.7).set_color(GREY_B)
        a_tag.add_updater(lambda m: m.next_to(axes.c2p(A.get_value(), 0), DOWN, buff=0.12))
        b_tag.add_updater(lambda m: m.next_to(axes.c2p(B.get_value(), 0), DOWN, buff=0.12))
        h_tag = Tex(R"\tfrac{1}{B-A}").scale(0.7).set_color(ACCENT)
        h_tag.add_updater(lambda m: m.next_to(axes.c2p(A.get_value(), 1 / (B.get_value() - A.get_value())), LEFT, buff=0.15))
        r0 = frozen(rect)
        self.play(ShowCreation(axes), FadeIn(r0), FadeIn(a_tag), FadeIn(b_tag), FadeIn(h_tag))
        self.remove(r0); self.add(rect)
        flat = note("flat density", 24, GREY_B).next_to(axes, UP, buff=0.1).align_to(axes, LEFT)
        self.play(FadeIn(flat))
        self.wait(0.5)

        area = Tex(R"(B - A)\cdot\frac{1}{B-A} = 1").scale(0.75).set_color(INK).move_to([4.2, 0.6, 0])
        area_tag = note("area 1", 24, MEAN_COLOR).next_to(area, UP, buff=0.2)
        self.play(FadeIn(area_tag), Write(area))
        self.wait(0.4)
        # 구간을 넓히면 낮아진다
        self.play(B.animate.set_value(4.6), run_time=1.6)
        self.play(A.animate.set_value(0.4), run_time=1.2)
        self.wait(0.3)
        self.play(A.animate.set_value(1.0), B.animate.set_value(3.0), run_time=1.4)
        self.wait(0.4)

        # 확률 = 밑변의 비율
        a, b = 1.5, 2.5
        piece = Polygon(axes.c2p(a, 0), axes.c2p(a, 0.5), axes.c2p(b, 0.5), axes.c2p(b, 0)).set_fill(MEAN_COLOR, 0.7).set_stroke(width=0)
        marks = x_marks(axes, [a, b], ["a", "b"], MEAN_COLOR)
        prob = Tex(R"P(a < X < b) = \frac{b - a}{B - A}").scale(0.75).set_color(MEAN_COLOR).next_to(area, DOWN, buff=0.5)
        self.play(FadeIn(piece), FadeIn(marks), Write(prob))
        self.wait(0.8)

        # 평균은 가운데 (정리 6.1)
        ful = fulcrum_at(axes.c2p(2.0, 0)).shift(DOWN * 0.42)
        mv = Tex(R"\mu = \frac{A+B}{2},\quad \sigma^2 = \frac{(B-A)^2}{12}").scale(0.7).set_color(INK).next_to(prob, DOWN, buff=0.5)
        thm = note("Theorem 6.1", 22, GREY_B).next_to(mv, DOWN, buff=0.15)
        self.play(FadeIn(ful), Write(mv), FadeIn(thm))
        self.play(FlashAround(name, color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 정규곡선의 모양 — 슬라이드 6 (6.2 정의) 앞
# ─────────────────────────────────────────────────────────────
class NormalCurveShape(InteractiveScene):
    """이름: n(x; μ, σ). 종 모양 하나를 세우고 μ 를 밀면 곡선이 통째로 옮겨 가고, σ 를 키우면 벌어지며 낮아진다
    (넓이 1 그대로). 변곡점은 μ ± σ 에 있다(성질 3). 덱 7 쪽의 세 그림이 트래커 하나로 이어진다."""

    def construct(self):
        head = slide_title("Normal Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"n(x;\,\mu,\sigma) = \frac{1}{\sqrt{2\pi}\,\sigma}\,e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}").scale(0.75).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.6)
        self.play(Write(name))

        axes = density_axes((-2, 12, 1), (0, 0.45, 0.1), width=9.0, height=3.4).move_to([-1.6, -1.0, 0])
        mu, sig = ValueTracker(5.0), ValueTracker(1.0)
        curve = always_redraw(lambda: normal_graph(axes, mu.get_value(), sig.get_value(), -2, 12))
        fill = always_redraw(lambda: area_under(axes, curve, -2, 12, ACCENT, 0.2))
        mu_line = always_redraw(lambda: dashed(axes.c2p(mu.get_value(), 0), axes.c2p(mu.get_value(), npdf(0, 0, sig.get_value())), MEAN_COLOR))
        mu_tag = Tex(R"\mu").scale(0.7).set_color(MEAN_COLOR)
        mu_tag.add_updater(lambda m: m.next_to(axes.c2p(mu.get_value(), 0), DOWN, buff=0.12))
        c0, f0, m0 = frozen(curve), frozen(fill), frozen(mu_line)
        self.play(ShowCreation(axes), ShowCreation(c0), FadeIn(f0), FadeIn(m0), FadeIn(mu_tag))
        self.remove(c0, f0, m0); self.add(curve, fill, mu_line)
        bell = note("bell-shaped curve", 24, GREY_B).next_to(axes, UP, buff=0.1).align_to(axes, LEFT)
        self.play(FadeIn(bell))
        self.wait(0.5)

        # 변곡점 μ ± σ
        def inflection():
            m, s = mu.get_value(), sig.get_value()
            return VGroup(*[Dot(axes.c2p(m + k * s, npdf(m + k * s, m, s)), radius=0.07).set_fill(WARN, 1) for k in (-1, 1)])
        dots = always_redraw(inflection)
        s_tag = Tex(R"\mu - \sigma \qquad \mu + \sigma").scale(0.6).set_color(WARN)
        s_tag.add_updater(lambda m: m.next_to(axes.c2p(mu.get_value(), npdf(sig.get_value(), 0, sig.get_value())), UP, buff=0.12))
        infl = label("inflection points", 24, WARN).move_to([4.4, 0.6, 0])
        d0 = frozen(dots)
        self.play(FadeIn(d0), FadeIn(s_tag), FadeIn(infl))
        self.remove(d0); self.add(dots)
        self.wait(0.6)

        # μ 가 옮긴다
        mu_note = label("μ moves the center", 24, MEAN_COLOR).next_to(infl, DOWN, buff=0.35).align_to(infl, LEFT)
        self.play(FadeIn(mu_note))
        self.play(mu.animate.set_value(8.0), run_time=1.6)
        self.play(mu.animate.set_value(3.0), run_time=1.6)
        self.wait(0.3)
        # σ 가 벌린다
        sig_note = label("σ sets the spread", 24, WARN).next_to(mu_note, DOWN, buff=0.3).align_to(infl, LEFT)
        self.play(FadeIn(sig_note))
        self.play(sig.animate.set_value(2.2), run_time=1.8)
        self.play(sig.animate.set_value(0.6), run_time=1.4)
        self.play(sig.animate.set_value(1.0), mu.animate.set_value(5.0), run_time=1.2)
        one = Tex(R"\int_{-\infty}^{\infty} n(x;\mu,\sigma)\,dx = 1").scale(0.7).set_color(INK).next_to(sig_note, DOWN, buff=0.4).align_to(infl, LEFT)
        self.play(Write(one))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 표준화와 표 A.3 — 슬라이드 12 (6.3 절 · 정의 6.1) 앞
# ─────────────────────────────────────────────────────────────
class StandardizeToZ(InteractiveScene):
    """P(x₁ < X < x₂) 는 곡선 아래 넓이. 자를 z = (x − μ)/σ 로 바꾸면 n(z; 0, 1) 아래 같은 넓이가 된다.
    표 A.3 은 z 왼쪽 넓이 P(Z < z) 만 준다. 오른쪽은 1 에서 빼고, 사이는 두 왼쪽 넓이의 차다."""

    def construct(self):
        head = slide_title("Areas under the Normal Curve")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 왼쪽: x 자. 오른쪽: z 자.
        ax = density_axes((20, 80, 10), (0, 0.045, 0.01), width=5.8, height=2.6).move_to([-3.6, 0.3, 0])
        az = density_axes((-3, 3, 1), (0, 0.45, 0.1), width=5.8, height=2.6).move_to([3.4, 0.3, 0])
        gx = normal_graph(ax, 50, 10, 20, 80)
        gz = normal_graph(az, 0, 1, -3, 3, CALM)
        x1, x2 = 45, 62
        shade_x = area_under(ax, gx, x1, x2, MEAN_COLOR, 0.6)
        mx = x_marks(ax, [x1, 50, x2], ["x_1", R"\mu", "x_2"])
        x_tag = Tex(R"n(x;\,\mu,\sigma)").scale(0.65).set_color(ACCENT).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        self.play(ShowCreation(ax), ShowCreation(gx), FadeIn(mx), FadeIn(x_tag))
        self.play(FadeIn(shade_x))
        self.wait(0.5)

        rule = Tex(R"z = \frac{x - \mu}{\sigma}").scale(0.8).set_color(MEAN_COLOR).move_to([0.0, 0.3, 0])
        arrow = Arrow([-0.7, -0.4, 0], [0.7, -0.4, 0], buff=0).set_color(MEAN_COLOR)
        self.play(Write(rule), GrowArrow(arrow))
        z1, z2 = (x1 - 50) / 10, (x2 - 50) / 10
        shade_z = area_under(az, gz, z1, z2, MEAN_COLOR, 0.6)
        mz = x_marks(az, [z1, 0, z2], ["z_1", "0", "z_2"])
        z_tag = Tex(R"n(z;\,0,1)").scale(0.65).set_color(CALM).next_to(az, UP, buff=0.1).align_to(az, LEFT)
        self.play(ShowCreation(az), ShowCreation(gz), FadeIn(mz), FadeIn(z_tag))
        self.play(TransformFromCopy(shade_x, shade_z), run_time=1.2)
        same = label("same area", 24, MEAN_COLOR).next_to(arrow, DOWN, buff=0.15)
        self.play(FadeIn(same))
        eq = Tex(R"P(x_1 < X < x_2) = P(z_1 < Z < z_2)").scale(0.7).set_color(INK).move_to([0, -1.5, 0])
        self.play(Write(eq))
        self.wait(0.8)

        # 표 A.3 은 왼쪽 넓이만 준다
        self.play(FadeOut(VGroup(ax, gx, shade_x, mx, x_tag, rule, arrow, same, eq)))
        big = density_axes((-3.5, 3.5, 1), (0, 0.45, 0.1), width=8.0, height=3.0).move_to([-2.4, -0.9, 0])
        g = normal_graph(big, 0, 1, -3.5, 3.5, CALM)
        self.play(ReplacementTransform(VGroup(az, gz), VGroup(big, g)), FadeOut(VGroup(shade_z, mz, z_tag)), run_time=1.0)
        zt = ValueTracker(0.8)
        left = always_redraw(lambda: area_under(big, g, -3.5, zt.get_value(), MEAN_COLOR, 0.6))
        z_mark = Tex("z").scale(0.7).set_color(MEAN_COLOR)
        z_mark.add_updater(lambda m: m.next_to(big.c2p(zt.get_value(), 0), DOWN, buff=0.12))
        tbl = label("Table A.3: area to the left", 26, MEAN_COLOR).move_to([3.3, 1.2, 0])
        pz = Tex(R"P(Z < z)").scale(0.8).set_color(MEAN_COLOR).next_to(tbl, DOWN, buff=0.25)
        l0 = frozen(left)
        self.play(FadeIn(l0), FadeIn(z_mark), FadeIn(tbl), Write(pz))
        self.remove(l0); self.add(left)
        self.play(zt.animate.set_value(-1.2), run_time=1.4)
        self.play(zt.animate.set_value(1.5), run_time=1.4)
        self.wait(0.4)

        # 오른쪽 = 1 − 왼쪽, 사이 = 차
        right = area_under(big, g, 1.5, 3.5, WARN, 0.6)
        r_eq = Tex(R"P(Z > z) = 1 - P(Z < z)").scale(0.65).set_color(WARN).next_to(pz, DOWN, buff=0.5).align_to(tbl, LEFT)
        self.play(FadeIn(right), Write(r_eq))
        self.wait(0.8)
        self.play(FadeOut(right))
        between = area_under(big, g, -1.0, 1.5, CALM, 0.7)
        b_eq = Tex(R"P(a < Z < b) = P(Z < b) - P(Z < a)").scale(0.55).set_color(CALM).next_to(r_eq, DOWN, buff=0.4).align_to(tbl, LEFT)
        a_mark = Tex("a").scale(0.7).set_color(CALM).next_to(big.c2p(-1.0, 0), DOWN, buff=0.12)
        self.play(FadeIn(between), FadeIn(a_mark), Write(b_eq))
        self.play(FlashAround(tbl, color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 예제 6.2 — 슬라이드 14 뒤 (풀이 15 앞)
# ─────────────────────────────────────────────────────────────
class Example62TableA3(InteractiveScene):
    """표준정규. (a) z = 1.84 오른쪽: 표 A.3 의 1.8 줄 .04 칸 0.9671 → 1 − 0.9671 = 0.0329.
    (b) −1.97 과 0.86 사이: 0.86 왼쪽 0.8051 에서 −1.97 왼쪽 0.0244 를 뺀 0.7807."""

    def construct(self):
        head = slide_title("Example 6.2")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. draw the area", "2. read Table A.3", "3. right: 1 − left",
                                         "4. between: difference"], pos=(4.6, 1.75, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        axes = density_axes((-3.5, 3.5, 1), (0, 0.45, 0.1), width=7.6, height=2.8).move_to([-2.9, -1.2, 0])
        g = normal_graph(axes, 0, 1, -3.5, 3.5, CALM)
        self.play(ShowCreation(axes), ShowCreation(g))

        # (a)
        self.play(focus(0))
        want = area_under(axes, g, 1.84, 3.5, WARN, 0.7)
        m1 = x_marks(axes, [0, 1.84], ["0", "1.84"])
        qa = Tex(R"\text{(a)}\ P(Z > 1.84)").scale(0.7).set_color(WARN).move_to([-5.2, 0.9, 0])
        self.play(FadeIn(want), FadeIn(m1), Write(qa))
        self.wait(0.6)
        self.play(focus(1))
        left = area_under(axes, g, -3.5, 1.84, MEAN_COLOR, 0.55)
        row, hit = table_row("1.8", [".02", ".03", ".04", ".05"], ["0.9656", "0.9664", "0.9671", "0.9678"], 2, [3.2, -0.3, 0])
        self.play(FadeIn(left), FadeIn(row))
        self.play(ShowCreation(hit))
        read = Tex(R"P(Z < 1.84) = 0.9671").scale(0.65).set_color(MEAN_COLOR).next_to(row, DOWN, buff=0.3)
        self.play(Write(read))
        self.wait(0.6)
        self.play(focus(2))
        ans_a = Tex(R"1 - 0.9671 = 0.0329").scale(0.7).set_color(WARN).next_to(read, DOWN, buff=0.3)
        self.play(FadeOut(left), Write(ans_a))
        self.play(FlashAround(ans_a, color=WARN, buff=0.08))
        self.wait(1.0)

        # (b)
        self.play(focus(3), FadeOut(VGroup(want, m1, qa, row, hit, read, ans_a)))
        qb = Tex(R"\text{(b)}\ P(-1.97 < Z < 0.86)").scale(0.7).set_color(CALM).move_to([-4.6, 0.9, 0])
        m2 = x_marks(axes, [-1.97, 0, 0.86], ["-1.97", "0", "0.86"])
        self.play(Write(qb), FadeIn(m2))
        left_b = area_under(axes, g, -3.5, 0.86, MEAN_COLOR, 0.55)
        row_b, hit_b = table_row("0.8", [".05", ".06", ".07"], ["0.8023", "0.8051", "0.8078"], 1, [3.2, 0.4, 0])
        self.play(FadeIn(left_b), FadeIn(row_b), ShowCreation(hit_b))
        r1 = Tex(R"P(Z < 0.86) = 0.8051").scale(0.6).set_color(MEAN_COLOR).next_to(row_b, DOWN, buff=0.2)
        self.play(Write(r1))
        self.wait(0.4)
        cut = area_under(axes, g, -3.5, -1.97, WARN, 0.8)
        row_c, hit_c = table_row("-1.9", [".06", ".07", ".08"], ["0.0250", "0.0244", "0.0239"], 1, [3.2, -1.9, 0])
        self.play(FadeIn(cut), FadeIn(row_c), ShowCreation(hit_c))
        r2 = Tex(R"P(Z < -1.97) = 0.0244").scale(0.6).set_color(WARN).next_to(row_c, DOWN, buff=0.2)
        self.play(Write(r2))
        self.wait(0.4)
        between = area_under(axes, g, -1.97, 0.86, CALM, 0.75)
        ans_b = Tex(R"0.8051 - 0.0244 = 0.7807").scale(0.7).set_color(CALM).next_to(qb, DOWN, buff=0.3).align_to(qb, LEFT)
        self.play(FadeOut(left_b), FadeOut(cut), FadeIn(between), Write(ans_b))
        self.play(FlashAround(ans_b, color=CALM, buff=0.08))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 예제 6.7 배터리 — 슬라이드 25 뒤 (풀이 26 앞)
# ─────────────────────────────────────────────────────────────
class Example67Battery(InteractiveScene):
    """수명 μ = 3.0 년, σ = 0.5 년. 2.3 년 전에 닳을 확률. z = (2.3 − 3)/0.5 = −1.4, 표 A.3 → 0.0808.
    배터리 25 개 가운데 둘(8 %)이 먼저 닳는다 — 확률을 개수로 한 번 더 보인다."""

    def construct(self):
        head = slide_title("Example 6.7")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. picture the area", "2. standardize", "3. read Table A.3"],
                                        pos=(4.7, 1.9, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        cells = VGroup(*[battery(0.3, ACCENT) for _ in range(25)]).arrange_in_grid(5, 5, buff=0.14).move_to([-4.6, 1.3, 0])
        info = Tex(R"\mu = 3.0\ \text{yr},\quad \sigma = 0.5\ \text{yr}").scale(0.65).set_color(INK).next_to(cells, DOWN, buff=0.25)
        self.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.03), run_time=1.2)
        self.play(FadeIn(info))
        self.wait(0.4)

        self.play(focus(0))
        axes = density_axes((1.4, 4.6, 0.5), (0, 0.9, 0.2), width=5.6, height=2.4).move_to([0.9, -1.9, 0])
        g = normal_graph(axes, 3.0, 0.5, 1.4, 4.6)
        want = area_under(axes, g, 1.4, 2.3, WARN, 0.7)
        marks = x_marks(axes, [2.3, 3.0], ["2.3", "3"])
        self.play(ShowCreation(axes), ShowCreation(g), FadeIn(marks))
        q = Tex(R"P(X < 2.3)").scale(0.75).set_color(WARN).move_to([4.5, -0.1, 0])
        self.play(FadeIn(want), Write(q))
        self.wait(0.6)

        self.play(focus(1))
        z = Tex(R"z = \frac{2.3 - 3}{0.5} = -1.4").scale(0.7).set_color(MEAN_COLOR).next_to(q, DOWN, buff=0.35).align_to(q, LEFT)
        self.play(Write(z))
        self.wait(0.5)

        self.play(focus(2))
        row, hit = table_row("-1.4", [".00", ".01"], ["0.0808", "0.0793"], 0, [5.0, -3.0, 0], scale=0.45, w=0.72, h=0.38)
        ans = Tex(R"P(Z < -1.4) = 0.0808").scale(0.7).set_color(WARN).next_to(z, DOWN, buff=0.3).align_to(q, LEFT)
        self.play(FadeIn(row), ShowCreation(hit))
        self.play(Write(ans))
        self.play(FlashAround(ans, color=WARN, buff=0.08))
        # 25 개 중 둘
        picked = [cells[7], cells[18]]
        self.play(*[c.animate.set_color(WARN) for c in picked], run_time=0.8)
        two = label("about 2 of 25", 24, WARN).next_to(info, DOWN, buff=0.2)
        self.play(FadeIn(two))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 예제 6.9 볼 베어링 — 슬라이드 29 뒤 (풀이 30 앞)
# ─────────────────────────────────────────────────────────────
class Example69Bearings(InteractiveScene):
    """규격 3.0 ± 0.01, σ = 0.005. 규격 밖은 양쪽 꼬리. z = ±2.0, 한쪽 0.0228, 둘 0.0456.
    베어링 100 개를 늘어놓고 다섯 개가 빨갛게 — 평균 4.56 개가 버려진다."""

    def construct(self):
        head = slide_title("Example 6.9")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. specification limits", "2. standardize both", "3. two tails",
                                         "4. scrapped per 100"], pos=(4.6, 1.75, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        self.play(focus(0))
        axes = density_axes((2.98, 3.02, 0.01), (0, 90, 20), width=7.4, height=2.6).move_to([-2.9, -1.5, 0])
        g = normal_graph(axes, 3.0, 0.005, 2.98, 3.02)
        marks = x_marks(axes, [2.99, 3.0, 3.01], ["2.99", "3.0", "3.01"])
        lim = VGroup(dashed(axes.c2p(2.99, 0), axes.c2p(2.99, 80), WARN), dashed(axes.c2p(3.01, 0), axes.c2p(3.01, 80), WARN))
        spec = Tex(R"3.0 \pm 0.01,\quad \sigma = 0.005").scale(0.7).set_color(INK).move_to([-4.0, 1.4, 0])
        self.play(Write(spec), ShowCreation(axes), ShowCreation(g), FadeIn(marks), ShowCreation(lim))
        out = tails(axes, g, 2.98, 3.02, 2.99, 3.01, WARN, 0.7)
        out_tag = label("outside: scrapped", 24, WARN).next_to(spec, DOWN, buff=0.2).align_to(spec, LEFT)
        self.play(FadeIn(out), FadeIn(out_tag))
        self.wait(0.6)

        self.play(focus(1))
        zs = column([R"z_1 = \frac{2.99 - 3.0}{0.005} = -2.0", R"z_2 = \frac{3.01 - 3.0}{0.005} = +2.0"],
                    box, scale=0.6, gap=0.3).align_to([2.4, 0, 0], LEFT)
        self.play(Write(zs[0]))
        self.play(Write(zs[1]))
        self.wait(0.5)

        self.play(focus(2))
        tl = column([R"P(Z < -2.0) = 0.0228", R"P(Z > 2.0) = 0.0228", R"0.0228 + 0.0228 = 0.0456"],
                    zs, scale=0.6, gap=0.35).align_to(zs, LEFT)
        self.play(Write(tl[0]), out[0].animate.set_fill(MEAN_COLOR, 0.8))
        self.play(Write(tl[1]), out[0].animate.set_fill(WARN, 0.7), out[1].animate.set_fill(MEAN_COLOR, 0.8))
        self.play(out[1].animate.set_fill(WARN, 0.7), Write(tl[2]))
        self.play(FlashAround(tl[2], color=WARN, buff=0.08))
        self.wait(0.8)

        # 100 개 중 4.56 개
        self.play(focus(3), FadeOut(VGroup(axes, g, marks, lim, out, spec, out_tag)))
        grid = VGroup(*[bearing(0.17) for _ in range(100)]).arrange_in_grid(5, 20, buff=0.1).move_to([-2.4, -1.4, 0])
        self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.01), run_time=1.5)
        old = [grid[k] for k in (3, 27, 48, 71, 94)]
        bad = [bearing(0.21, WARN).move_to(m) for m in old]
        self.play(*[FadeOut(m, scale=0.8) for m in old], *[FadeIn(b, scale=1.2) for b in bad], run_time=0.8)
        per = label("4.56 scrapped per 100", 26, WARN).next_to(grid, UP, buff=0.3).align_to(grid, LEFT)
        self.play(FadeIn(per))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 예제 6.13 성적 — 슬라이드 37 뒤 (풀이 38 앞)
# ─────────────────────────────────────────────────────────────
class Example613Grades(InteractiveScene):
    """μ = 74, σ = 7, 위 12 % 가 A. 역방향: 넓이에서 z 를 찾는다. 왼쪽 0.88 → z = 1.18 (표 A.3 의 0.8810),
    x = 74 + 7(1.18) = 82.26 → A 의 최저 83, B 의 최고 82. 학생 25 명이면 셋이 A 다."""

    def construct(self):
        head = slide_title("Example 6.13")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. area to the right", "2. left area 0.88", "3. z from Table A.3",
                                         "4. back to x"], pos=(4.6, 1.75, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        students = crowd(25, 5, 5, height=0.36, buff=0.1, seed=3).move_to([-5.0, 1.2, 0])
        info = Tex(R"\mu = 74,\quad \sigma = 7").scale(0.65).set_color(INK).next_to(students, DOWN, buff=0.2)
        self.play(FadeIn(students), FadeIn(info))

        self.play(focus(0))
        axes = density_axes((50, 98, 10), (0, 0.065, 0.02), width=5.2, height=2.0).move_to([-1.0, -2.5, 0])
        g = normal_graph(axes, 74, 7, 50, 98)
        marks = x_marks(axes, [74], ["74"])
        self.play(ShowCreation(axes), ShowCreation(g), FadeIn(marks))
        xa = 82.26
        top = area_under(axes, g, xa, 98, MEAN_COLOR, 0.75)
        a_tag = label("A: top 12%", 24, MEAN_COLOR).move_to([3.3, -0.1, 0]).align_to([2.6, 0, 0], LEFT)
        self.play(FadeIn(top), FadeIn(a_tag))
        self.wait(0.5)

        self.play(focus(1))
        rest = area_under(axes, g, 50, xa, ACCENT, 0.35)
        left = Tex(R"1 - 0.12 = 0.88").scale(0.6).set_color(ACCENT).next_to(a_tag, DOWN, buff=0.25).align_to(a_tag, LEFT)
        self.play(FadeIn(rest), Write(left))
        self.wait(0.5)

        self.play(focus(2))
        row, hit = table_row("1.1", [".07", ".08", ".09"], ["0.8790", "0.8810", "0.8830"], 1, [4.6, -3.1, 0], scale=0.45, w=0.72, h=0.38)
        z = Tex(R"P(Z < 1.18) \approx 0.88 \Rightarrow z = 1.18").scale(0.55).set_color(MEAN_COLOR).next_to(left, DOWN, buff=0.25).align_to(a_tag, LEFT)
        self.play(FadeIn(row), ShowCreation(hit), Write(z))
        self.wait(0.5)

        self.play(focus(3), FadeOut(row), FadeOut(hit))
        x = Tex(R"x = 74 + 7(1.18) = 82.26").scale(0.6).set_color(MEAN_COLOR).next_to(z, DOWN, buff=0.25).align_to(a_tag, LEFT)
        cut = x_marks(axes, [xa], ["82.26"], MEAN_COLOR)
        self.play(Write(x), FadeIn(cut))
        verdict = label("lowest A 83, highest B 82", 22, INK).next_to(x, DOWN, buff=0.25).align_to(a_tag, LEFT)
        self.play(Write(verdict))
        # 25 명 중 셋
        picks = [students[4], students[12], students[21]]
        fresh = Group(*[chito("front", "gold", m.get_height()).move_to(m) for m in picks])
        self.play(*[FadeOut(m) for m in picks], *[FadeIn(f) for f in fresh], run_time=0.8)
        self.play(*[ShowCreation(ring(f, MEAN_COLOR)) for f in fresh])
        three = label("3 of 25", 24, MEAN_COLOR).next_to(info, DOWN, buff=0.2)
        self.play(FadeIn(three))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 이항분포의 정규근사 — 슬라이드 41 (정리 6.3) 앞
# ─────────────────────────────────────────────────────────────
class NormalApproximatesBinomial(InteractiveScene):
    """b(x; n, 0.2) 막대 위에 μ = np, σ² = npq 인 정규곡선을 얹는다. n = 6 은 치우치고, 15 · 50 으로 커지면
    곡선이 막대 끝을 지난다(덱 43 쪽의 두 히스토그램). 한 막대의 확률 P(X = 4) 는 밑변 3.5 ~ 4.5 의 넓이 —
    그래서 ±0.5 를 보정한다(덱 42 쪽, n = 15, p = 0.4)."""

    def construct(self):
        head = slide_title("Normal Approximation to the Binomial")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\mu = np,\quad \sigma^2 = np(1-p)").scale(0.8).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.7)
        self.play(Write(name))

        axes = density_axes((-1, 24, 5), (0, 0.42, 0.1), width=9.6, height=3.2).move_to([-1.4, -1.2, 0])
        self.play(ShowCreation(axes))

        def bars_for(n, p):
            fs = binom_pmf(n, p)
            g = VGroup()
            for x, f in enumerate(fs):
                r = Polygon(axes.c2p(x - 0.5, 0), axes.c2p(x - 0.5, f), axes.c2p(x + 0.5, f), axes.c2p(x + 0.5, 0))
                g.add(r.set_fill(ACCENT, 0.5).set_stroke(ACCENT, 1.5))
            return g

        shown, curve, tag = None, None, None
        for n, p in ((6, 0.2), (15, 0.2), (50, 0.2)):
            mu, sig = n * p, sqrt(n * p * (1 - p))
            new = bars_for(n, p)
            new_curve = normal_graph(axes, mu, sig, -1, 24, MEAN_COLOR, 3)
            new_tag = Tex(R"b(x;\,%d,\,0.2),\quad \mu = %g,\ \sigma = %.2f" % (n, mu, sig)).scale(0.6).set_color(INK).move_to([3.0, 1.1, 0])
            if shown is None:
                self.play(LaggedStartMap(GrowFromEdge, new, edge=DOWN, lag_ratio=0.05), FadeIn(new_tag))
                self.play(ShowCreation(new_curve))
            else:
                self.play(FadeOut(shown), FadeOut(curve), FadeOut(tag), FadeIn(new), FadeIn(new_curve), FadeIn(new_tag), run_time=1.2)
            shown, curve, tag = new, new_curve, new_tag
            self.wait(0.9)
        ok = label("np ≥ 5 and n(1−p) ≥ 5", 24, CALM).next_to(tag, DOWN, buff=0.25).align_to(tag, LEFT)
        self.play(FadeIn(ok))
        self.wait(0.8)

        # 한 막대 = 밑변 ±0.5 의 넓이 (n = 15, p = 0.4, x = 4)
        self.play(FadeOut(VGroup(shown, curve, tag, ok)))
        ax2 = density_axes((-1, 16, 1), (0, 0.24, 0.05), width=9.6, height=3.2).move_to([-1.4, -1.2, 0])
        fs = binom_pmf(15, 0.4)
        bars = VGroup()
        for x, f in enumerate(fs):
            r = Polygon(ax2.c2p(x - 0.5, 0), ax2.c2p(x - 0.5, f), ax2.c2p(x + 0.5, f), ax2.c2p(x + 0.5, 0))
            bars.add(r.set_fill(ACCENT, 0.5).set_stroke(ACCENT, 1.5))
        g2 = normal_graph(ax2, 6, sqrt(3.6), -1, 16, MEAN_COLOR, 3)
        nums = VGroup(*[Tex(str(x)).scale(0.45).set_color(GREY_B).next_to(ax2.c2p(x, 0), DOWN, buff=0.12) for x in range(0, 16)])
        t2 = Tex(R"b(x;\,15,\,0.4),\quad \mu = 6,\ \sigma = 1.897").scale(0.6).set_color(INK).move_to([2.6, 1.1, 0])
        self.play(FadeOut(axes), FadeIn(ax2), FadeIn(bars), FadeIn(nums), ShowCreation(g2), FadeIn(t2))
        self.wait(0.4)
        one = bars[4].copy().set_fill(WARN, 0.85)
        exact = Tex(R"P(X = 4) = b(4;15,0.4) = 0.1268").scale(0.55).set_color(WARN).next_to(t2, DOWN, buff=0.3).align_to(t2, LEFT)
        self.play(FadeIn(one), Write(exact))
        strip = area_under(ax2, g2, 3.5, 4.5, MEAN_COLOR, 0.8)
        ends = x_marks(ax2, [3.5, 4.5], ["3.5", "4.5"], MEAN_COLOR).shift(DOWN * 0.3)
        self.play(FadeIn(strip), FadeIn(ends))
        approx = Tex(R"\approx P(3.5 < X < 4.5) = P(-1.32 < Z < -0.79) = 0.1214").scale(0.48).set_color(MEAN_COLOR).next_to(exact, DOWN, buff=0.25).align_to(t2, LEFT)
        self.play(Write(approx))
        cc = label("continuity correction ±0.5", 24, MEAN_COLOR).next_to(approx, DOWN, buff=0.3).align_to(t2, LEFT)
        self.play(FadeIn(cc), FlashAround(strip, color=MEAN_COLOR, buff=0.05))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 예제 6.15 환자 100 명 — 슬라이드 46 뒤 (풀이 47 앞)
# ─────────────────────────────────────────────────────────────
class Example615Recovery(InteractiveScene):
    """회복 확률 0.4, 환자 100 명. 30 명 미만이 회복할 확률. μ = 40, σ = 4.899. X ≤ 29 는 막대 29 까지,
    곡선으로는 29.5 왼쪽. z = −2.14 → 0.0162. 치토 100 명 가운데 회복한 29 명을 청록으로."""

    def construct(self):
        head = slide_title("Example 6.15")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. binomial n = 100", "2. μ = np, σ = √npq", "3. fewer than 30: x < 29.5",
                                         "4. standardize, Table A.3"], pos=(4.5, 1.75, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        self.play(focus(0))
        people = crowd(100, 5, 20, height=0.3, buff=0.06, seed=7).move_to([-2.6, 1.3, 0])
        self.play(FadeIn(people), run_time=1.0)
        fresh = Group(*[chito("front", "teal", m.get_height()).move_to(m) for m in list(people)[:29]])
        self.play(*[FadeOut(m) for m in list(people)[:29]], *[FadeIn(f) for f in fresh], run_time=0.8)
        few = label("fewer than 30 recover", 24, CALM).next_to(people, DOWN, buff=0.15).align_to(people, LEFT)
        self.play(FadeIn(few))
        self.wait(0.5)

        self.play(focus(1))
        axes = density_axes((18, 62, 10), (0, 0.095, 0.02), width=7.4, height=2.4).move_to([-2.8, -2.0, 0])
        fs = binom_pmf(100, 0.4)
        bars = VGroup()
        for x in range(18, 63):
            r = Polygon(axes.c2p(x - 0.5, 0), axes.c2p(x - 0.5, fs[x]), axes.c2p(x + 0.5, fs[x]), axes.c2p(x + 0.5, 0))
            bars.add(r.set_fill(ACCENT, 0.5).set_stroke(ACCENT, 1))
        g = normal_graph(axes, 40, 4.899, 18, 62, MEAN_COLOR, 3)
        marks = x_marks(axes, [40], ["40"])
        mv = Tex(R"\mu = 40,\quad \sigma = \sqrt{100(0.4)(0.6)} = 4.899").scale(0.6).set_color(INK).move_to([3.9, -0.1, 0])
        self.play(ShowCreation(axes), FadeIn(bars), FadeIn(marks), ShowCreation(g), Write(mv))
        self.wait(0.5)

        self.play(focus(2))
        want = VGroup(*[b.copy().set_fill(CALM, 0.85) for b in bars[:12]])
        strip = area_under(axes, g, 18, 29.5, CALM, 0.6)
        edge = x_marks(axes, [29.5], ["29.5"], CALM)
        self.play(FadeIn(want))
        self.play(FadeIn(strip), FadeIn(edge))
        self.wait(0.5)

        self.play(focus(3))
        col = column([R"z = \frac{29.5 - 40}{4.899} = -2.14", R"P(X < 30) \approx P(Z < -2.14) = 0.0162"],
                     mv, scale=0.6, gap=0.35).align_to(mv, LEFT)
        self.play(Write(col[0]))
        self.play(Write(col[1]))
        self.play(FlashAround(col[1], color=CALM, buff=0.08))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 감마분포의 모양 — 슬라이드 50 (감마분포 정의) 앞
# ─────────────────────────────────────────────────────────────
class GammaFamily(InteractiveScene):
    """이름: f(x; α, β). α 를 1 → 2 → 4 로 밀면 모양이 치우친 종으로 바뀌고(덱 50 쪽 그림), β 는 가로 자다.
    평균 αβ 의 받침점이 따라간다. α = 1 이 지수분포, α = v/2, β = 2 가 카이제곱분포."""

    def construct(self):
        head = slide_title("Gamma Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"f(x;\,\alpha,\beta) = \frac{1}{\beta^{\alpha}\Gamma(\alpha)}\,x^{\alpha-1}e^{-x/\beta},\quad x > 0").scale(0.7).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.6)
        self.play(Write(name))

        axes = density_axes((0, 12, 1), (0, 1.05, 0.5), width=8.4, height=3.4).move_to([-2.4, -1.1, 0])
        al, be = ValueTracker(1.0), ValueTracker(1.0)
        curve = always_redraw(lambda: axes.get_graph(lambda x: gamma_pdf(x, al.get_value(), be.get_value()),
                                                      x_range=(0.02, 12, 0.03)).set_stroke(ACCENT, 3))
        ful = always_redraw(lambda: fulcrum_at(axes.c2p(al.get_value() * be.get_value(), 0)).shift(DOWN * 0.42))
        a_num = DecimalNumber(1.0, num_decimal_places=1).scale(0.7).set_color(MEAN_COLOR)
        b_num = DecimalNumber(1.0, num_decimal_places=1).scale(0.7).set_color(CALM)
        a_num.f_always.set_value(al.get_value)
        b_num.f_always.set_value(be.get_value)
        a_lab = Tex(R"\alpha =").scale(0.7).set_color(MEAN_COLOR).move_to([3.4, 0.9, 0])
        b_lab = Tex(R"\beta =").scale(0.7).set_color(CALM).next_to(a_lab, DOWN, buff=0.35).align_to(a_lab, LEFT)
        a_num.next_to(a_lab, RIGHT, buff=0.2)
        b_num.next_to(b_lab, RIGHT, buff=0.2)
        mean = Tex(R"\mu = \alpha\beta").scale(0.7).set_color(INK).next_to(b_lab, DOWN, buff=0.4).align_to(a_lab, LEFT)
        c0 = frozen(curve)
        self.play(ShowCreation(axes), ShowCreation(c0), FadeIn(a_lab), FadeIn(a_num), FadeIn(b_lab), FadeIn(b_num))
        self.remove(c0); self.add(curve)
        f0 = frozen(ful)
        self.play(FadeIn(f0), Write(mean))
        self.remove(f0); self.add(ful)
        exp_tag = label("α = 1: exponential", 24, ACCENT).next_to(axes, UP, buff=0.1).align_to(axes, LEFT)
        self.play(FadeIn(exp_tag))
        self.wait(0.8)

        shape = label("α shapes the curve", 24, MEAN_COLOR).next_to(mean, DOWN, buff=0.4).align_to(a_lab, LEFT)
        self.play(FadeOut(exp_tag), FadeIn(shape))
        self.play(al.animate.set_value(2.0), run_time=1.5)
        self.wait(0.3)
        self.play(al.animate.set_value(4.0), run_time=1.5)
        self.wait(0.5)
        scale_tag = label("β stretches the axis", 24, CALM).next_to(shape, DOWN, buff=0.3).align_to(a_lab, LEFT)
        self.play(al.animate.set_value(2.0), run_time=0.8)
        self.play(FadeIn(scale_tag))
        self.play(be.animate.set_value(2.0), run_time=1.5)
        self.wait(0.4)
        chi = label("α = v/2, β = 2: chi-squared", 24, GREY_B).next_to(scale_tag, DOWN, buff=0.3).align_to(a_lab, LEFT)
        self.play(FadeIn(chi))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 포아송 과정에서 지수분포로 — 슬라이드 53 (포아송 과정과의 관계) 앞
# ─────────────────────────────────────────────────────────────
class PoissonToExponential(InteractiveScene):
    """같은 시간선을 두 번 본다. 길이 t 의 창 안의 사건 수는 포아송(5 장). 이번에는 첫 사건까지의 시간 X 를 잰다.
    X > x 는 "x 동안 사건 0 번" 과 같은 사건이므로 e^{−λx}. 간격을 많이 재어 쌓으면 막대가 λe^{−λx} 를 따른다.
    두 번째 사건까지의 시간은 감마(α = 2)."""

    def construct(self):
        head = slide_title("Poisson Process and Exponential")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        rng = np.random.default_rng(11)
        lam = 1.0
        gaps = rng.exponential(1 / lam, 14)
        times = np.cumsum(gaps)
        tline = Line([-6.4, 1.6, 0], [1.4, 1.6, 0]).set_stroke(GREY_B, 2)
        x0 = -6.2
        dots = VGroup(*[Dot([x0 + t * 0.55, 1.6, 0], radius=0.07).set_fill(ACCENT, 1) for t in times if x0 + t * 0.55 < 1.3])
        t_tag = note("time", 22, GREY_B).next_to(tline, RIGHT, buff=0.2)
        self.play(ShowCreation(tline), FadeIn(t_tag))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.08, scale=0.5), run_time=1.2)
        count = label("count in a window: Poisson", 24, GREY_B).next_to(tline, UP, buff=0.35).align_to(tline, LEFT)
        self.play(FadeIn(count))
        self.wait(0.4)

        # 첫 사건까지의 시간
        start = Dot([x0, 1.6, 0], radius=0.09).set_fill(MEAN_COLOR, 1)
        first = dots[0]
        brace = Brace(Line(start.get_center(), first.get_center()), DOWN, buff=0.12).set_color(MEAN_COLOR)
        x_tag = Tex("X").scale(0.8).set_color(MEAN_COLOR).next_to(brace, DOWN, buff=0.1)
        wait_tag = label("time to the first event", 24, MEAN_COLOR).next_to(tline, UP, buff=0.35).align_to(tline, LEFT)
        self.play(FadeOut(count), FadeIn(start), GrowFromCenter(brace), FadeIn(x_tag), FadeIn(wait_tag))
        self.wait(0.5)
        eq = column([R"P(X > x) = P(\text{no event in } x) = e^{-\lambda x}",
                     R"F(x) = 1 - e^{-\lambda x}",
                     R"f(x) = \lambda e^{-\lambda x},\qquad \beta = 1/\lambda"],
                    tline, scale=0.55, gap=1.2)
        eq.move_to([4.3, 0.3, 0])
        self.play(Write(eq[0]))
        self.wait(0.6)

        # 간격을 많이 재어 쌓는다
        axes = density_axes((0, 5, 1), (0, 1.1, 0.5), width=7.0, height=2.6).move_to([-2.9, -1.8, 0])
        self.play(ShowCreation(axes), FadeOut(brace), FadeOut(x_tag))
        sample = rng.exponential(1 / lam, 400)
        width = 0.25
        edges = np.arange(0, 5 + width, width)
        hist, _ = np.histogram(sample, bins=edges)
        heights = hist / (len(sample) * width)
        bars = VGroup()
        for lo, h in zip(edges[:-1], heights):
            r = Polygon(axes.c2p(lo, 0), axes.c2p(lo, h), axes.c2p(lo + width, h), axes.c2p(lo + width, 0))
            bars.add(r.set_fill(MEAN_COLOR, 0.45).set_stroke(MEAN_COLOR, 1))
        many = label("400 measured gaps", 22, GREY_B).next_to(axes, UP, buff=0.1).align_to(axes, LEFT)
        self.play(FadeIn(many), LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.04), run_time=1.6)
        f = axes.get_graph(lambda x: lam * math.exp(-lam * x), x_range=(0, 5, 0.02)).set_stroke(ACCENT, 3)
        self.play(ShowCreation(f), Write(eq[1]))
        self.play(Write(eq[2]))
        expo = label("exponential distribution", 26, ACCENT).next_to(eq[2], DOWN, buff=0.3).align_to(eq[2], LEFT)
        self.play(FadeIn(expo))
        self.wait(0.8)

        # 두 번째 사건까지는 감마
        second = dots[1]
        brace2 = Brace(Line(start.get_center(), second.get_center()), DOWN, buff=0.12).set_color(CALM)
        g2 = axes.get_graph(lambda x: gamma_pdf(x, 2, 1 / lam), x_range=(0.01, 5, 0.02)).set_stroke(CALM, 3)
        gam = label("second event: gamma, α = 2", 24, CALM).next_to(expo, DOWN, buff=0.3).align_to(eq[2], LEFT)
        self.play(GrowFromCenter(brace2), ShowCreation(g2), FadeIn(gam))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 무기억성 — 슬라이드 60 (무기억성) 앞
# ─────────────────────────────────────────────────────────────
class MemorylessExponential(InteractiveScene):
    """수명 곡선 P(X > t) = e^{−t/β}. 이미 t₀ 만큼 버틴 부품의 남은 수명 — 꼬리를 잘라 t₀ 를 0 으로 끌어오고
    P(X > t₀) 로 나누어 높이를 1 로 세우면 처음 곡선과 포개진다. 감마(α = 2)는 포개지지 않는다 — 닳는 것."""

    def construct(self):
        head = slide_title("Memoryless Property")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"P(X \ge t_0 + t \mid X \ge t_0) = P(X \ge t)").scale(0.75).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        self.play(Write(name))

        beta, t0 = 2.0, 1.5
        axes = density_axes((0, 8, 1), (0, 1.1, 0.5), width=8.4, height=3.2).move_to([-2.4, -1.0, 0])
        surv = lambda t: math.exp(-t / beta)
        g = axes.get_graph(surv, x_range=(0, 8, 0.02)).set_stroke(ACCENT, 3)
        s_tag = Tex(R"P(X > t) = e^{-t/\beta}").scale(0.7).set_color(ACCENT).next_to(axes, UP, buff=0.1).align_to(axes, LEFT)
        self.play(ShowCreation(axes), ShowCreation(g), FadeIn(s_tag))
        self.wait(0.4)

        # t0 까지 버틴 부품
        t0_line = dashed(axes.c2p(t0, 0), axes.c2p(t0, surv(t0)), WARN)
        t0_tag = Tex("t_0").scale(0.7).set_color(WARN).next_to(axes.c2p(t0, 0), DOWN, buff=0.12)
        tail = axes.get_graph(surv, x_range=(t0, 8, 0.02)).set_stroke(WARN, 4)
        lasted = label("already lasted t₀", 24, WARN).move_to([4.2, 0.6, 0])
        self.play(ShowCreation(t0_line), FadeIn(t0_tag), ShowCreation(tail), FadeIn(lasted))
        self.wait(0.5)

        # 꼬리를 끌어와 다시 잰다: 가로로 t0 만큼, 세로로 1/P(X>t0) 배
        moved = axes.get_graph(lambda t: surv(t + t0) / surv(t0), x_range=(0, 8 - t0, 0.02)).set_stroke(WARN, 4)
        rescale = label("shift to 0, rescale to 1", 24, WARN).next_to(lasted, DOWN, buff=0.25).align_to(lasted, LEFT)
        self.play(FadeIn(rescale))
        self.play(Transform(tail, moved), run_time=1.8)
        same = label("same curve", 26, MEAN_COLOR).next_to(rescale, DOWN, buff=0.3).align_to(lasted, LEFT)
        self.play(FadeIn(same), FlashAround(name, color=MEAN_COLOR, buff=0.1))
        self.wait(1.0)

        # 닳는 부품: 감마 α = 2 는 포개지지 않는다
        self.play(FadeOut(VGroup(tail, t0_line, t0_tag, lasted, rescale, same)))
        gsurv = lambda t: (1 + t / beta) * math.exp(-t / beta)
        g2 = axes.get_graph(gsurv, x_range=(0, 8, 0.02)).set_stroke(CALM, 3)
        g2_tag = label("gamma α = 2: wear", 24, CALM).next_to(s_tag, RIGHT, buff=0.6)
        self.play(ShowCreation(g2), FadeIn(g2_tag))
        tail2 = axes.get_graph(gsurv, x_range=(t0, 8, 0.02)).set_stroke(WARN, 4)
        moved2 = axes.get_graph(lambda t: gsurv(t + t0) / gsurv(t0), x_range=(0, 8 - t0, 0.02)).set_stroke(WARN, 4)
        self.play(ShowCreation(tail2))
        self.play(Transform(tail2, moved2), run_time=1.8)
        diff = label("not the same: memory", 26, WARN).move_to([4.2, 0.4, 0])
        self.play(FadeIn(diff))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13. 예제 6.18 전화 두 통 — 슬라이드 63 뒤 (풀이 64 앞)
# ─────────────────────────────────────────────────────────────
class Example618Calls(InteractiveScene):
    """분당 평균 5 통(λ = 5, β = 1/5). 두 번째 전화까지의 시간 X 는 감마(α = 2, β = 1/5).
    P(X ≤ 1) = ∫₀¹ 25 x e^{−5x} dx — 부분적분으로 −5xe^{−5x} − e^{−5x} — = 1 − 6e^{−5} = 0.96."""

    def construct(self):
        head = slide_title("Example 6.18")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. gamma, α = 2, β = 1/5", "2. area up to 1 minute", "3. integrate by parts",
                                         "4. evaluate"], pos=(4.5, 1.75, 0), size=22)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        # 시간선 위 전화
        tline = Line([-6.4, 1.5, 0], [1.2, 1.5, 0]).set_stroke(GREY_B, 2)
        ticks = VGroup(*[Line(UP * 0.08, DOWN * 0.08).move_to([-6.4 + k * 7.6 / 4, 1.5, 0]).set_stroke(GREY_B, 2) for k in range(5)])
        lab = VGroup(*[Tex(t).scale(0.5).set_color(GREY_B).next_to(ticks[k], DOWN, buff=0.1) for k, t in enumerate(["0", "", "", "", "1\\ \\text{min}"])])
        self.play(ShowCreation(tline), FadeIn(ticks), FadeIn(lab))
        rate = label("5 calls per minute", 24, GREY_B).next_to(tline, UP, buff=0.95).align_to(tline, LEFT)
        self.play(FadeIn(rate))
        p1 = phone(0.42).move_to([-6.4 + 0.27 * 7.6, 1.95, 0])
        p2 = phone(0.42, MEAN_COLOR).move_to([-6.4 + 0.61 * 7.6, 1.95, 0])
        self.play(FadeIn(p1, shift=DOWN * 0.2))
        self.play(FadeIn(p2, shift=DOWN * 0.2))
        brace = Brace(Line([-6.4, 1.5, 0], [p2.get_x(), 1.5, 0]), DOWN, buff=0.35).set_color(MEAN_COLOR)
        x_tag = label("X: time to the 2nd call", 22, MEAN_COLOR).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), FadeIn(x_tag))
        self.wait(0.5)

        self.play(focus(0))
        axes = density_axes((0, 2.0, 0.5), (0, 2.0, 1), width=6.4, height=2.2).move_to([-3.0, -2.2, 0])
        g = axes.get_graph(lambda x: gamma_pdf(x, 2, 0.2), x_range=(0.001, 2.0, 0.01)).set_stroke(ACCENT, 3)
        marks = x_marks(axes, [1.0], ["1"])
        f = Tex(R"f(x) = 25\,x\,e^{-5x}").scale(0.65).set_color(ACCENT).next_to(axes, UP, buff=0.05).align_to(axes, LEFT)
        self.play(FadeOut(VGroup(brace, x_tag)), ShowCreation(axes), ShowCreation(g), FadeIn(marks), Write(f))
        self.wait(0.4)

        self.play(focus(1))
        area = area_under(axes, g, 0.001, 1.0, MEAN_COLOR, 0.6)
        q = Tex(R"P(X \le 1) = \int_0^1 25\,x\,e^{-5x}\,dx").scale(0.62).set_color(MEAN_COLOR).move_to([4.0, 0.2, 0])
        self.play(FadeIn(area), Write(q))
        self.wait(0.5)

        self.play(focus(2))
        parts = column([R"u = x,\quad dv = 25e^{-5x}dx", R"= \big[-5xe^{-5x}\big]_0^1 + \int_0^1 5e^{-5x}dx",
                        R"= -5e^{-5} - \big[e^{-5x}\big]_0^1"], q, scale=0.55, gap=0.3).align_to(q, LEFT)
        for line in parts:
            self.play(Write(line))
            self.wait(0.3)

        self.play(focus(3))
        ans = Tex(R"= 1 - e^{-5}(1 + 5) = 0.96").scale(0.65).set_color(MEAN_COLOR).next_to(parts, DOWN, buff=0.3).align_to(q, LEFT)
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.08))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 14. 로그정규분포 — 슬라이드 76 (로그정규분포 정의) 앞
# ─────────────────────────────────────────────────────────────
class LognormalFromNormal(InteractiveScene):
    """Y = ln X 가 정규(μ, σ) 이면 X 는 로그정규. 왼쪽 정규곡선의 점을 x = e^y 로 보내면 오른쪽에 오른꼬리가 긴
    곡선이 쌓인다. 확률은 ln 을 취해 정규 넓이로 돌아간다(예제 6.22 의 방식). 평균 e^{μ+σ²/2}."""

    def construct(self):
        head = slide_title("Lognormal Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"Y = \ln X \sim n(y;\,\mu,\sigma)").scale(0.8).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.7)
        self.play(Write(name))

        mu, sig = 0.0, 0.5
        ay = density_axes((-2, 2, 1), (0, 0.9, 0.5), width=5.0, height=2.6).move_to([-4.2, -0.6, 0])
        ax = density_axes((0, 5, 1), (0, 0.9, 0.5), width=6.0, height=2.6).move_to([2.6, -0.6, 0])
        gy = normal_graph(ay, mu, sig, -2, 2)
        lnpdf = lambda x: math.exp(-0.5 * ((math.log(x) - mu) / sig) ** 2) / (x * sig * math.sqrt(2 * math.pi))
        gx = ax.get_graph(lnpdf, x_range=(0.05, 5, 0.02)).set_stroke(CALM, 3)
        y_tag = Tex(R"y = \ln x").scale(0.65).set_color(ACCENT).next_to(ay, UP, buff=0.1).align_to(ay, LEFT)
        x_tag = Tex(R"x = e^{y}").scale(0.65).set_color(CALM).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        self.play(ShowCreation(ay), ShowCreation(gy), FadeIn(y_tag))
        self.wait(0.3)
        arrow = Arrow([-1.4, -0.6, 0], [-0.4, -0.6, 0], buff=0).set_color(MEAN_COLOR)
        exp_tag = Tex(R"e^{\,y}").scale(0.7).set_color(MEAN_COLOR).next_to(arrow, UP, buff=0.1)
        self.play(ShowCreation(ax), GrowArrow(arrow), FadeIn(exp_tag), FadeIn(x_tag))

        # 점을 보낸다
        yt = ValueTracker(-1.2)
        dy = always_redraw(lambda: Dot(ay.c2p(yt.get_value(), 0), radius=0.08).set_fill(MEAN_COLOR, 1))
        dx = always_redraw(lambda: Dot(ax.c2p(math.exp(yt.get_value()), 0), radius=0.08).set_fill(MEAN_COLOR, 1))
        y0, x0 = frozen(dy), frozen(dx)
        self.play(FadeIn(y0), FadeIn(x0))
        self.remove(y0, x0); self.add(dy, dx)
        self.play(yt.animate.set_value(1.4), run_time=2.4, rate_func=linear)
        self.play(ShowCreation(gx), run_time=1.2)
        skew = label("right-skewed, x > 0", 24, CALM).next_to(x_tag, RIGHT, buff=0.6)
        self.play(FadeIn(skew))
        self.wait(0.6)

        # 확률은 ln 으로 되돌린다
        a = 1.8
        px = area_under(ax, gx, a, 5, MEAN_COLOR, 0.6)
        py = area_under(ay, gy, math.log(a), 2, MEAN_COLOR, 0.6)
        ma = x_marks(ax, [a], ["a"], MEAN_COLOR)
        mb = x_marks(ay, [math.log(a)], [R"\ln a"], MEAN_COLOR)
        rule = Tex(R"P(X > a) = P\left(Z > \frac{\ln a - \mu}{\sigma}\right)").scale(0.6).set_color(MEAN_COLOR).move_to([0.2, -2.9, 0])
        self.play(FadeIn(px), FadeIn(ma))
        self.play(TransformFromCopy(px, py), FadeIn(mb), Write(rule))
        self.wait(0.5)
        mean = Tex(R"\mu_X = e^{\mu + \sigma^2/2},\quad \sigma_X^2 = e^{2\mu+\sigma^2}(e^{\sigma^2}-1)").scale(0.55).set_color(INK).next_to(rule, DOWN, buff=0.2)
        thm = note("Theorem 6.7", 22, GREY_B).next_to(mean, RIGHT, buff=0.3)
        self.play(Write(mean), FadeIn(thm))
        self.wait(2)
