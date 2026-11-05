# -*- coding: utf-8 -*-
"""확률과통계 「확률변수의 함수」 장 (Walpole Chapter 7) — 변수 변환 · 야코비안 · 일대일이 아닌 변환 · 적률생성함수.

파일 이름이 week07b 인 까닭: week07.py 는 6장(연속형 확률분포), week08.py 는 8장(표본분포)이다. 7장은 계획서의 10주차
자리에 들며 16차(11/6, 가정)에 8장 앞에서 다룬다(2026-11-05). 도구와 규칙은 week08.py 와 같다.
개념 영상 네 편(2026-11-03 결정 — 자리는 그 개념 슬라이드 **앞**)에 **적분이 있는 예제 네 편**을 더했다(2026-11-05 저녁,
사용자: "적분 관련 예제는 전부 영상으로 문제를 풀어야 될 거 같은데, 지나치게 수식 말고 풀이의 예시를 들어서 좀 자세하게 그림들을
그려봐야 될 거 같다. 야코비안도 나오는 거 같고. 개별 하나하나는 치환적분으로 풀면 되는데 그 풀이 자체가 적분이 익숙치 않으면
풀기 어려울 거 같다"). 이산형 예제(7.1 · 7.2 · 7.6)는 영상이 없다.
개념 네 편은 정지 그림으로는 안 보이는 것만 고른 것이다: 일대일 변환에서 확률 막대가 자리만 옮기는 것,
연속형에서 축이 늘어나면 넓이를 지키려고 높이가 줄어드는 것(야코비안), 일대일이 아니면 역상 둘의 밀도가 포개지는 것,
적률생성함수가 e^{tx} 로 다시 잰 무게의 합이고 그 기울기가 평균인 것.
예제 네 편은 그 개념을 교재 예제의 적분으로 끝까지 쓴다. 풀이 단계를 먼저 걸고(steps_panel) 하나씩 켜며, 식보다 그림이 앞선다:
구간의 넓이가 y 축으로 옮겨 가며 띠가 두 배로 넓어지는 것(7.3), 작은 상자가 2x₁² 배로 커지는 것(7.4), 종의 양쪽이 y 축 한 곳으로
포개지는 것(7.5), e^{tx} 로 잰 종이 옮겨 간 종인 것(7.7).
화면 문구는 영어, 여섯 낱말까지(`ps_common.label`). 사람은 나오지 않는다.

덱 삽입 자리 (원본 PS1_07_restyled.pptx 23장 기준. 레이아웃 정리 뒤의 번호는 insert_videos.py 의 PS1_07_INSERT 가 정본이다.
네 편 모두 "N 앞" = 그 개념 슬라이드 바로 앞):
    DiscreteTransformation           3 앞    예제 7.1 (= 정리 7.1 의 이산형 일대일 변환, 제목은 "Example 7.1" — 2026-11-06), g(y) = f(w(y)), 기하분포 막대가 y = x² 자리로
    JacobianStretch                  8 앞    정리 7.3 — 연속형, y = 2x − 3 으로 축이 2 배 늘고 높이가 반이 됨, |J| = 1/2
    NotOneToOne                     13 앞    일대일이 아닌 변환 — y = x² (−1 < x < 2), 0 < y < 1 에 역상 둘, g = f(−√y)|J₁| + f(√y)|J₂|
    MomentGeneratingFunction        17 앞    정의 7.1 · 7.2 — M_X(t) = E(e^{tX}), 이항 b(x; 4, 1/2) 의 무게 e^{tx}, M'(0) = μ, 곱셈 성질
예제 영상 (레이아웃 정리 뒤 원본 28장 기준, "문제 장 뒤 = 책 풀이 장 앞"):
    Example73Linear                 11 뒤    예제 7.3 — ∫₁³ x/12 dx = 1/3 을 x = (y+3)/2 로 치환, dx = dy/2 가 |J|, g = (y+3)/48
    Example74Jacobian2D             13 뒤    예제 7.4 — 꼭짓점 넷 → 영역 B, 역변환, 작은 상자의 넓이 × 2y₁ → |J| = 1/(2y₁), g = 2y₂/y₁
    Example75ChiSquare              18 뒤    예제 7.5 — 표준화, −1 < z < 1 의 양쪽이 0 < y < 1 로 포개짐, z = √u 치환, Γ(1/2) = √π → χ²(1)
    Example77NormalMGF              23 뒤    예제 7.7 — e^{tx} 로 잰 종 = μ + σ²t 로 옮겨 간 종 × e^{μt+σ²t²/2}, 남는 종의 넓이 1

참고: legacy/_2016/eola/chapter3.py (TransformManyVectors · TransformInfiniteGrid — 변환을 "격자와 점이 함께 움직이는 것"
      으로 보이고 변환 뒤의 넓이를 견준다), legacy/_2018/eop (시행 결과를 막대로 쌓는 문법). 전개만 가져오고 코드는 옮기지 않았다.

렌더 (저장소 루트에서, 한 번에 한 프로세스만):
    ./render.sh check _2026/probstat/week07b.py
    ./render.sh ppt   _2026/probstat/week07b.py DiscreteTransformation
"""
import math
from math import comb, exp, sqrt

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN,
    label, note, slide_title,
)
from _2026.probstat.week04 import density_axes, area_under, x_marks
from _2026.probstat.week05 import dashed, steps_panel
from _2026.probstat.week06 import axis, chart
from _2026.probstat.week07 import npdf, normal_graph


# ─────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────
def geom_pmf(x, p=0.75):
    return p * (1 - p) ** (x - 1)


def binom4(x):
    return comb(4, x) / 16


def mgf_binom4(t):
    return ((1 + exp(t)) / 2) ** 4


def tag_bars(bars, texts, scale=0.5, color=GREY_B):
    return VGroup(*[Tex(t).scale(scale).set_color(color).next_to(b, UP, buff=0.07) for b, t in zip(bars, texts)])


# ─────────────────────────────────────────────────────────────
# 1. 이산형 일대일 변환 — 슬라이드 3 (정리 7.1) 앞
# ─────────────────────────────────────────────────────────────
class DiscreteTransformation(InteractiveScene):
    """기하분포 f(x) = (3/4)(1/4)^(x−1) 의 막대 네 개(x = 1 … 4)를 y = x² 자리(1, 4, 9, 16)로 옮긴다.
    일대일이라 막대의 높이(확률)는 그대로이고 자리만 바뀐다. g(y) = f(w(y)), w(y) = √y."""

    def construct(self):
        head = slide_title("Example 7.1")   # 2026-11-06 사용자: 이 영상은 사실상 예제 7.1 이다(정리 7.1 은 수식뿐). 자리는 그대로 정리 7.1 앞
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        fx = Tex(R"f(x) = \tfrac34\left(\tfrac14\right)^{x-1},\quad x = 1, 2, 3, \ldots").scale(0.75).set_color(INK)
        fx.next_to(head[1], DOWN, buff=0.3).align_to(head[0], LEFT)
        self.play(Write(fx))

        xs = [1, 2, 3, 4]
        fs = [geom_pmf(x) for x in xs]
        line, nums = axis(0, 16, 11.6, [0.2, -2.2, 0], every=1, size=0.42)
        xname = Tex("x").scale(0.6).set_color(GREY_B).next_to(line, RIGHT, buff=0.15)
        bars = chart(line, xs, fs, 0.8, color=ACCENT, width=0.42, height=2.6)
        tags = tag_bars(bars, [R"\tfrac34", R"\tfrac{3}{16}", R"\tfrac{3}{64}", R"\tfrac{3}{256}"])
        self.play(ShowCreation(line), FadeIn(nums), FadeIn(xname))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(tags))
        self.wait(2.2)

        # y = x² — 막대가 자리만 옮긴다
        rule = Tex(R"y = x^2").scale(0.9).set_color(MEAN_COLOR).move_to([2.6, 1.7, 0])
        self.play(Write(rule))
        self.wait(0.4)
        yname = Tex("y").scale(0.6).set_color(MEAN_COLOR).next_to(line, RIGHT, buff=0.3)
        moves = []
        for b, t, x in zip(bars, tags, xs):
            y = x * x
            moves.append(b.animate.move_to(line.n2p(y), aligned_edge=DOWN).shift(UP * 0.02).set_fill(MEAN_COLOR, 0.85).set_stroke(MEAN_COLOR, 2))
            moves.append(t.animate.next_to(line.n2p(y) + UP * (b.get_height() + 0.09), UP, buff=0))
        self.play(FadeOut(xname), FadeIn(yname))
        self.play(*moves, run_time=2.2)
        same = label("one-to-one: heights unchanged", 24, MEAN_COLOR).next_to(rule, DOWN, buff=0.35).align_to(rule, LEFT)
        self.play(FadeIn(same))
        self.wait(2.0)

        # 거꾸로 읽는 법
        inv = Tex(R"x = w(y) = \sqrt{y}").scale(0.75).set_color(INK).next_to(same, DOWN, buff=0.35).align_to(rule, LEFT)
        gy = Tex(R"g(y) = f(w(y)) = \tfrac34\left(\tfrac14\right)^{\sqrt{y}-1}").scale(0.75).set_color(MEAN_COLOR)
        gy.next_to(inv, DOWN, buff=0.3).align_to(rule, LEFT)
        dom = Tex(R"y = 1, 4, 9, 16, \ldots").scale(0.65).set_color(GREY_B).next_to(gy, DOWN, buff=0.25).align_to(rule, LEFT)
        self.play(Write(inv))
        self.wait(1.0)
        self.play(Write(gy))
        self.wait(0.8)
        self.play(FadeIn(dom))
        self.play(FlashAround(gy, color=MEAN_COLOR, buff=0.1))
        self.wait(4.5)


# ─────────────────────────────────────────────────────────────
# 2. 야코비안 — 슬라이드 8 (정리 7.3) 앞
# ─────────────────────────────────────────────────────────────
class JacobianStretch(InteractiveScene):
    """f(x) = x/12 (1 < x < 5) 에 y = 2x − 3 을 적용한다. 축이 두 배로 늘어나므로 넓이 1 을 지키려면 높이가 반이 된다.
    g(y) = f(w(y))|J|, J = dx/dy = 1/2, g(y) = (y + 3)/48 (−1 < y < 7). 예제 7.3 과 같은 밀도."""

    def construct(self):
        head = slide_title("Jacobian of a Transformation")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # X 의 밀도
        ax = density_axes((0, 8, 1), (0, 0.5, 0.1), width=5.2, height=2.3).move_to([-3.4, 0.9, 0])
        fg = ax.get_graph(lambda x: x / 12, x_range=(1, 5, 0.05)).set_stroke(ACCENT, 3)
        farea = area_under(ax, fg, 1, 5, ACCENT, 0.4)
        fmarks = x_marks(ax, [1, 5])
        fname = Tex(R"f(x) = \tfrac{x}{12},\ 1 < x < 5").scale(0.65).set_color(ACCENT).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        a1 = label("area = 1", 22, ACCENT).move_to(ax.c2p(3.3, 0.1))
        self.play(ShowCreation(ax), FadeIn(fmarks), Write(fname))
        self.play(ShowCreation(fg), FadeIn(farea), FadeIn(a1))
        self.wait(2.0)

        # 변환 y = 2x − 3: 눈금이 옮겨 간다
        rule = Tex(R"y = 2x - 3").scale(0.9).set_color(MEAN_COLOR).move_to([3.6, 1.9, 0])
        self.play(Write(rule))
        ay = density_axes((-2, 8, 1), (0, 0.5, 0.1), width=6.5, height=2.3).move_to([-2.0, -2.1, 0])
        ymarks = x_marks(ay, [-1, 7])
        self.play(ShowCreation(ay), FadeIn(ymarks))
        arrows = VGroup(
            Arrow(ax.c2p(1, 0), ay.c2p(-1, 0.46), buff=0.05, stroke_width=2).set_color(MEAN_COLOR),
            Arrow(ax.c2p(5, 0), ay.c2p(7, 0.46), buff=0.05, stroke_width=2).set_color(MEAN_COLOR),
        )
        stretch = label("axis stretched by 2", 22, MEAN_COLOR).move_to([3.6, 1.2, 0])
        self.play(ShowCreation(arrows), FadeIn(stretch))
        self.wait(1.8)

        # 넓이를 지키려면 높이가 반 — 영역을 옮겨 보인다
        gg = ay.get_graph(lambda y: (y + 3) / 48, x_range=(-1, 7, 0.05)).set_stroke(MEAN_COLOR, 3)
        garea = area_under(ay, gg, -1, 7, MEAN_COLOR, 0.4)
        moved = farea.copy()
        self.play(Transform(moved, garea), run_time=1.8)
        self.play(ShowCreation(gg))
        half = label("height halved, area kept", 22, MEAN_COLOR).next_to(stretch, DOWN, buff=0.25).align_to(stretch, LEFT)
        a2 = label("area = 1", 22, MEAN_COLOR).move_to(ay.c2p(3.0, 0.07))
        self.play(FadeIn(half), FadeIn(a2))
        self.wait(1.8)

        jac = Tex(R"J = \frac{dx}{dy} = \frac12").scale(0.8).set_color(INK).move_to([3.6, -0.1, 0])
        gform = Tex(R"g(y) = f(w(y))\,|J|").scale(0.8).set_color(MEAN_COLOR).next_to(jac, DOWN, buff=0.35)
        gval = Tex(R"g(y) = \frac{(y+3)/2}{12}\cdot\frac12 = \frac{y+3}{48}").scale(0.7).set_color(MEAN_COLOR).next_to(gform, DOWN, buff=0.3)
        gdom = Tex(R"-1 < y < 7").scale(0.65).set_color(GREY_B).next_to(gval, DOWN, buff=0.2)
        self.play(Write(jac))
        self.wait(0.8)
        self.play(Write(gform))
        self.wait(0.8)
        self.play(Write(gval), FadeIn(gdom))
        self.play(FlashAround(gform, color=MEAN_COLOR, buff=0.1))
        self.wait(4.5)


# ─────────────────────────────────────────────────────────────
# 3. 일대일이 아닌 변환 — 슬라이드 13 앞
# ─────────────────────────────────────────────────────────────
class NotOneToOne(InteractiveScene):
    """y = x² (−1 < x < 2). 0 < y < 1 인 y 는 역상이 ±√y 둘, 1 < y < 4 인 y 는 √y 하나. 구간을 (−1, 0), (0, 1), (1, 2) 로
    갈라 역함수를 하나씩 두고, g(y) = f(−√y)|J₁| + f(√y)|J₂| 로 두 몫이 포개진다. 밀도는 f(x) = 2(x + 1)/9."""

    def construct(self):
        head = slide_title("Transformation That Is Not One-to-One")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        ax = Axes(x_range=(-1.6, 2.6, 1), y_range=(0, 4.6, 1), width=5.6, height=4.0,
                  axis_config=dict(include_ticks=True, stroke_width=2, stroke_color=GREY_B)).move_to([-3.1, -0.7, 0])
        par = ax.get_graph(lambda x: x * x, x_range=(-1, 2, 0.02)).set_stroke(ACCENT, 3)
        rule = Tex(R"y = x^2,\quad -1 < x < 2").scale(0.75).set_color(ACCENT).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        xm = x_marks(ax, [-1, 0, 1, 2])
        self.play(ShowCreation(ax), FadeIn(xm), Write(rule))
        self.play(ShowCreation(par))
        self.wait(1.6)

        # y = 0.5 → 역상 둘
        y1 = 0.5
        hline1 = dashed(ax.c2p(-1.3, y1), ax.c2p(1.3, y1), WARN)
        d1 = VGroup(Dot(ax.c2p(-sqrt(y1), y1), radius=0.07).set_fill(WARN, 1), Dot(ax.c2p(sqrt(y1), y1), radius=0.07).set_fill(WARN, 1))
        ar1 = VGroup(Arrow(ax.c2p(-sqrt(y1), y1), ax.c2p(-sqrt(y1), 0), buff=0.08, stroke_width=2).set_color(WARN),
                     Arrow(ax.c2p(sqrt(y1), y1), ax.c2p(sqrt(y1), 0), buff=0.08, stroke_width=2).set_color(WARN))
        t1 = VGroup(Tex(R"-\sqrt{y}").scale(0.55).set_color(WARN).next_to(ax.c2p(-sqrt(y1), 0), DOWN, buff=0.45),
                    Tex(R"\sqrt{y}").scale(0.55).set_color(WARN).next_to(ax.c2p(sqrt(y1), 0), DOWN, buff=0.45))
        two = label("0 < y < 1: two inverses", 24, WARN).move_to([3.6, 2.0, 0])
        self.play(ShowCreation(hline1), FadeIn(d1))
        self.play(ShowCreation(ar1), FadeIn(t1), FadeIn(two))
        self.wait(2.0)

        # y = 2.5 → 역상 하나
        y2 = 2.5
        hline2 = dashed(ax.c2p(-1.3, y2), ax.c2p(2.3, y2), CALM)
        d2 = Dot(ax.c2p(sqrt(y2), y2), radius=0.07).set_fill(CALM, 1)
        ar2 = Arrow(ax.c2p(sqrt(y2), y2), ax.c2p(sqrt(y2), 0), buff=0.08, stroke_width=2).set_color(CALM)
        one = label("1 < y < 4: one inverse", 24, CALM).next_to(two, DOWN, buff=0.25).align_to(two, LEFT)
        self.play(ShowCreation(hline2), FadeIn(d2))
        self.play(ShowCreation(ar2), FadeIn(one))
        self.wait(2.0)

        # 구간 가르기
        seg = VGroup(
            Line(ax.c2p(-1, 0), ax.c2p(0, 0)).set_stroke(WARN, 8),
            Line(ax.c2p(0, 0), ax.c2p(1, 0)).set_stroke(WARN, 8).set_opacity(0.55),
            Line(ax.c2p(1, 0), ax.c2p(2, 0)).set_stroke(CALM, 8),
        )
        part = label("partition: (−1, 0), (0, 1), (1, 2)", 22, INK).next_to(one, DOWN, buff=0.35).align_to(two, LEFT)
        self.play(ShowCreation(seg), FadeIn(part))
        self.wait(1.6)

        # 두 몫이 포개진다
        gform = Tex(R"g(y) = f(-\sqrt{y})\,|J_1| + f(\sqrt{y})\,|J_2|").scale(0.7).set_color(MEAN_COLOR).next_to(part, DOWN, buff=0.35).align_to(two, LEFT)
        jform = Tex(R"|J_1| = |J_2| = \frac{1}{2\sqrt{y}}").scale(0.7).set_color(INK).next_to(gform, DOWN, buff=0.25).align_to(two, LEFT)
        self.play(Write(gform))
        self.wait(0.8)
        self.play(Write(jform))
        self.wait(1.0)

        # 작은 밀도 그림: f(x) = 2(x+1)/9 → g(y) 의 두 몫 (0 < y < 1)
        gy = density_axes((0, 4.4, 1), (0, 1.6, 0.5), width=3.6, height=1.6).move_to([4.3, -2.2, 0])
        f = lambda x: 2 * (x + 1) / 9
        left = lambda y: f(-sqrt(y)) / (2 * sqrt(y))
        right = lambda y: f(sqrt(y)) / (2 * sqrt(y))
        g_lo = gy.get_graph(lambda y: left(y) + right(y), x_range=(0.09, 1, 0.02)).set_stroke(MEAN_COLOR, 3)
        g_hi = gy.get_graph(right, x_range=(1, 4, 0.02)).set_stroke(MEAN_COLOR, 3)
        a_right = gy.get_area_under_graph(gy.get_graph(right, x_range=(0.09, 1, 0.02)), x_range=(0.09, 1), fill_color=CALM, fill_opacity=0.55)
        a_both = gy.get_area_under_graph(g_lo, x_range=(0.09, 1), fill_color=WARN, fill_opacity=0.35)
        gm = x_marks(gy, [1, 4])
        gname = Tex(R"g(y)").scale(0.6).set_color(MEAN_COLOR).next_to(gy, UP, buff=0.05).align_to(gy, LEFT)
        self.play(ShowCreation(gy), FadeIn(gm), FadeIn(gname))
        self.play(FadeIn(a_right), FadeIn(a_both), ShowCreation(g_lo), ShowCreation(g_hi))
        stack = label("two branches add up", 22, MEAN_COLOR).next_to(gm, DOWN, buff=0.18)
        self.play(FadeIn(stack))
        self.wait(0.8)
        self.play(FlashAround(gform, color=MEAN_COLOR, buff=0.1))
        self.wait(4.5)


# ─────────────────────────────────────────────────────────────
# 4. 적률생성함수 — 슬라이드 17 (정의 7.1 · 7.2) 앞
# ─────────────────────────────────────────────────────────────
class MomentGeneratingFunction(InteractiveScene):
    """M_X(t) = E(e^{tX}). 이항 b(x; 4, 1/2) 의 막대에 무게 e^{tx} 를 곱하면 t 가 커질수록 오른쪽 막대가 자란다.
    그 합이 M(t) = ((1 + e^t)/2)^4 이고, t = 0 에서의 기울기가 μ = 2, 둘째 도함수가 E(X²) = 5 다.
    독립이면 M_{X+Y} = M_X · M_Y — 정규 두 개의 합이 다시 정규(정리 7.11 예고)."""

    def construct(self):
        head = slide_title("Moment-Generating Function")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        mdef = Tex(R"M_X(t) = E\left(e^{tX}\right) = \sum_x e^{tx} f(x)").scale(0.75).set_color(MEAN_COLOR)
        mdef.next_to(head[1], DOWN, buff=0.25).align_to(head[0], LEFT)
        self.play(Write(mdef))

        # 막대 — 이항 b(x; 4, 1/2), 무게 e^{tx}
        xs = [0, 1, 2, 3, 4]
        fs = [binom4(x) for x in xs]
        line, nums = axis(0, 4, 4.2, [-3.8, -2.3, 0], every=1, size=0.45)
        pname = Tex(R"f(x) = b(x;\,4,\tfrac12)").scale(0.6).set_color(ACCENT).next_to(line, DOWN, buff=0.45)
        vmax = 1.0
        bars = chart(line, xs, fs, vmax, color=ACCENT, width=0.5, height=2.4)
        self.play(ShowCreation(line), FadeIn(nums), FadeIn(pname))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.15))
        self.wait(0.6)

        ttag = Tex(R"t = 0.00").scale(0.7).set_color(WARN).next_to(line, UP, buff=2.75).align_to(line, LEFT)
        wtag = Tex(R"\text{weights } e^{tx}").scale(0.65).set_color(WARN).next_to(ttag, RIGHT, buff=0.5)
        self.play(FadeIn(ttag), FadeIn(wtag))
        # M(t) 곡선
        ax = density_axes((-1, 0.8, 0.5), (0, 4.6, 1), width=5.0, height=2.9).move_to([3.3, -0.9, 0])
        mg = ax.get_graph(mgf_binom4, x_range=(-1, 0.7, 0.02)).set_stroke(MEAN_COLOR, 3)
        am = x_marks(ax, [-1, 0, 0.5])
        mname = Tex(R"M_X(t) = \left(\tfrac{1+e^{t}}{2}\right)^{4}").scale(0.65).set_color(MEAN_COLOR).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        self.play(ShowCreation(ax), FadeIn(am), Write(mname))
        self.play(ShowCreation(mg))
        pt = Dot(ax.c2p(0, 1), radius=0.08).set_fill(WARN, 1)
        self.play(FadeIn(pt))
        self.wait(0.4)
        prev = bars
        for t in (0.2, 0.4, 0.6):
            ws = [fx * exp(t * x) for x, fx in zip(xs, fs)]
            nb = chart(line, xs, ws, vmax, color=WARN, width=0.5, height=2.4)
            nt = Tex(R"t = %.2f" % t).scale(0.7).set_color(WARN).move_to(ttag)
            self.play(Transform(prev, nb), Transform(ttag, nt), pt.animate.move_to(ax.c2p(t, mgf_binom4(t))), run_time=0.9)
            self.wait(0.3)
        total = label("sum of weighted bars = M(t)", 22, MEAN_COLOR).next_to(pname, DOWN, buff=0.25).align_to(line, LEFT)
        self.play(FadeIn(total))
        self.wait(1.0)

        # 기울기 = 평균, 둘째 도함수 = E(X²)
        self.play(pt.animate.move_to(ax.c2p(0, 1)), run_time=0.7)
        tan = Line(ax.c2p(-0.5, 1 - 2 * 0.5), ax.c2p(0.5, 1 + 2 * 0.5)).set_stroke(CALM, 3)
        slope = Tex(R"M'_X(0) = \mu = 2").scale(0.7).set_color(CALM).move_to([3.3, 1.55, 0])
        self.play(ShowCreation(tan), Write(slope))
        self.wait(0.5)
        second = Tex(R"M''_X(0) = E(X^2) = 5").scale(0.7).set_color(CALM).next_to(slope, DOWN, buff=0.2)
        self.play(Write(second))
        self.wait(1.2)

        # 곱셈 성질 — 정규 둘의 합
        self.wait(0.8)
        self.play(FadeOut(VGroup(prev, line, nums, pname, ttag, wtag, total, ax, am, mg, mname, pt, tan, slope, second)))
        prod = Tex(R"X,\,Y\ \text{independent:}\quad M_{X+Y}(t) = M_X(t)\,M_Y(t)").scale(0.75).set_color(MEAN_COLOR).move_to([-1.2, 1.2, 0])
        self.play(Write(prod))
        nx = density_axes((-2, 12, 2), (0, 0.45, 0.1), width=8.0, height=2.4).move_to([-1.4, -1.9, 0])
        gX = normal_graph(nx, 2, 1.0, -2, 12, ACCENT)
        gY = normal_graph(nx, 5, 1.5, -2, 12, CALM)
        gS = normal_graph(nx, 7, sqrt(1 + 2.25), -2, 12, MEAN_COLOR)
        lx = Tex(R"X \sim n(2, 1)").scale(0.6).set_color(ACCENT).next_to(nx.c2p(2, npdf(2, 2, 1)), UP, buff=0.1)
        ly = Tex(R"Y \sim n(5, 1.5)").scale(0.6).set_color(CALM).next_to(nx.c2p(5, npdf(5, 5, 1.5)), UP, buff=0.1)
        ls = Tex(R"X + Y \sim n(7, \sqrt{3.25})").scale(0.6).set_color(MEAN_COLOR).next_to(nx.c2p(9.5, 0.28), UP, buff=0.1)
        self.play(ShowCreation(nx), FadeIn(x_marks(nx, [2, 5, 7])))
        self.play(ShowCreation(gX), FadeIn(lx))
        self.play(ShowCreation(gY), FadeIn(ly))
        self.play(ShowCreation(gS), FadeIn(ls))
        sumnote = label("sum of normals is normal", 24, MEAN_COLOR).move_to([3.4, 0.4, 0])
        self.play(FadeIn(sumnote))
        self.play(FlashAround(prod, color=MEAN_COLOR, buff=0.1))
        self.wait(4.0)


# ─────────────────────────────────────────────────────────────
# 예제 영상 (2026-11-05 저녁, 사용자 요구 — "적분 관련 예제는 전부 영상으로 … 수식 말고 풀이의 예시를 들어서 그림을")
# 네 편 모두 "문제 장 뒤, 책 풀이 장 앞". 풀이 단계를 먼저 걸고(steps_panel) 하나씩 켠다. 수식은 치환적분 한 줄씩이고
# 그림이 먼저다: 구간의 넓이가 옮겨 가는 것, 작은 상자가 2x₁² 배로 커지는 것, 종의 양쪽이 포개지는 것, e^{tx} 로 잰 종이
# 옮겨 간 종인 것. 그림은 왼쪽, 단계 상자와 식은 오른쪽 한 열(x ≥ 1.6)에 쌓는다 — 첫 렌더(2026-11-06 00:03)에서 왼쪽에 둔
# 식이 화살표·축과 겹치고 긴 줄이 화면 밖으로 나갔다.
# ─────────────────────────────────────────────────────────────
def _lines(texts, ref, scale=0.6, color=INK, buff=0.16, gap=0.3, left_x=None):
    """수식 줄을 ref 아래에 왼쪽 맞춤으로 쌓는다(week05.column 과 같되 색을 줄마다 줄 수 있다)."""
    texs = []
    for t in texts:
        c = color
        if isinstance(t, tuple):
            t, c = t
        texs.append(Tex(t).scale(scale).set_color(c))
    col = VGroup(*texs).arrange(DOWN, buff=buff, aligned_edge=LEFT).next_to(ref, DOWN, buff=gap)
    if left_x is not None:
        col.align_to([left_x, 0, 0], LEFT)
    return col


def _strip(axes, a, b, h, color):
    return Polygon(axes.c2p(a, 0), axes.c2p(b, 0), axes.c2p(b, h), axes.c2p(a, h)).set_fill(color, 0.9).set_stroke(WHITE, 1.5)


COL_X = 1.6          # 오른쪽 식 열의 왼쪽 끝


# ─────────────────────────────────────────────────────────────
# 5. 예제 7.3 — 슬라이드 11 (문제) 뒤, 12 (풀이) 앞
# ─────────────────────────────────────────────────────────────
class Example73Linear(InteractiveScene):
    """f(x) = x/12 (1 < x < 5), Y = 2X − 3. 구간 1 < x < 3 의 넓이 1/3 을 적분으로 먼저 구하고, x = (y + 3)/2 로 치환하면
    dx = dy/2 라서 같은 넓이가 −1 < y < 3 위에 반 높이로 펼쳐진다. 폭 dx 의 띠가 폭 2dx 의 띠가 되는 그림이 야코비안이고,
    g(y) = f((y+3)/2)·(1/2) = (y + 3)/48 이다. JacobianStretch 가 개념이면 이 편은 그 적분을 끝까지 쓴다."""

    def construct(self):
        head = slide_title("Example 7.3")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. area of an interval", "2. substitute x = (y+3)/2",
                                         "3. dx = dy/2 is |J|", "4. write g(y)"], pos=(4.6, 2.1, 0), size=20)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        ax = density_axes((0, 8, 1), (0, 0.5, 0.1), width=5.2, height=1.9).move_to([-3.6, 1.2, 0])
        fg = ax.get_graph(lambda x: x / 12, x_range=(1, 5, 0.05)).set_stroke(ACCENT, 3)
        fname = Tex(R"f(x) = \tfrac{x}{12},\ 1 < x < 5").scale(0.6).set_color(ACCENT).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        self.play(ShowCreation(ax), FadeIn(x_marks(ax, [1, 3, 5])), Write(fname))
        self.play(ShowCreation(fg))
        self.wait(0.5)

        # 1. 구간의 넓이를 적분으로
        self.play(focus(0))
        a13 = area_under(ax, fg, 1, 3, WARN, 0.6)
        self.play(FadeIn(a13))
        l1 = _lines([R"P(1 < X < 3) = \int_1^3 \frac{x}{12}\,dx = \left[\frac{x^2}{24}\right]_1^3 = \frac13"],
                    box, scale=0.56, color=WARN, gap=0.3, left_x=COL_X)
        self.play(Write(l1))
        self.wait(1.6)

        # 2. 치환 — 같은 구간이 y 축에서는 두 배로
        self.play(focus(1))
        l2 = _lines([(R"y = 2x - 3\ \Rightarrow\ x = \frac{y+3}{2}", MEAN_COLOR),
                     (R"1 < x < 3\ \Rightarrow\ -1 < y < 3", MEAN_COLOR)],
                    l1, scale=0.6, gap=0.25, left_x=COL_X)
        self.play(Write(l2[0]))
        ay = density_axes((-2, 8, 1), (0, 0.5, 0.1), width=6.5, height=1.9).move_to([-2.95, -2.4, 0])
        ymarks = x_marks(ay, [-1, 3, 7])
        self.play(ShowCreation(ay), FadeIn(ymarks))
        arrows = VGroup(Arrow(ax.c2p(1, 0) + DOWN * 0.4, ay.c2p(-1, 0.48), buff=0.05, stroke_width=2).set_color(MEAN_COLOR),
                        Arrow(ax.c2p(3, 0) + DOWN * 0.4, ay.c2p(3, 0.48), buff=0.05, stroke_width=2).set_color(MEAN_COLOR))
        self.play(ShowCreation(arrows), Write(l2[1]))
        self.wait(1.4)

        # 3. 폭 dx 의 띠가 폭 2dx 의 띠로 — 넓이를 지키려면 높이가 반
        self.play(focus(2))
        s_x = _strip(ax, 1.8, 2.2, 2 / 12, WARN)
        dx = Tex("dx").scale(0.5).set_color(WARN).next_to(s_x, UP, buff=0.08)
        self.play(FadeIn(s_x), FadeIn(dx))
        self.wait(0.4)
        s_y = _strip(ay, 0.6, 1.4, 1 / 12, MEAN_COLOR)
        dy = Tex(R"dy = 2\,dx").scale(0.5).set_color(MEAN_COLOR).next_to(s_y, UP, buff=0.08)
        moved = s_x.copy()
        self.play(Transform(moved, s_y), run_time=1.4)
        self.play(FadeIn(dy))
        wide = label("twice as wide, half as tall", 21, MEAN_COLOR).next_to(l2, DOWN, buff=0.28).align_to(l2, LEFT)
        jac = Tex(R"dx = \tfrac12\,dy,\qquad |J| = \tfrac12").scale(0.62).set_color(INK).next_to(wide, DOWN, buff=0.2).align_to(l2, LEFT)
        self.play(FadeIn(wide))
        self.play(Write(jac))
        self.wait(1.6)

        # 4. 치환한 적분을 끝까지 — 같은 1/3, 그러므로 g(y)
        self.play(focus(3))
        gg = ay.get_graph(lambda y: (y + 3) / 48, x_range=(-1, 7, 0.05)).set_stroke(MEAN_COLOR, 3)
        g13 = area_under(ay, gg, -1, 3, WARN, 0.6)
        self.play(FadeOut(moved), FadeOut(dy), FadeOut(s_x), FadeOut(dx))
        moved_area = a13.copy()
        self.play(Transform(moved_area, g13), run_time=1.4)
        self.play(ShowCreation(gg))
        l4 = _lines([R"\int_{-1}^{3} \frac{(y+3)/2}{12}\cdot\frac12\,dy = \int_{-1}^{3}\frac{y+3}{48}\,dy = \frac13",
                     (R"g(y) = \frac{y+3}{48},\quad -1 < y < 7", MEAN_COLOR)],
                    jac, scale=0.56, color=INK, gap=0.28, left_x=COL_X)
        self.play(Write(l4[0]))
        self.wait(0.6)
        self.play(Write(l4[1]))
        self.play(FlashAround(l4[1], color=MEAN_COLOR, buff=0.08))
        self.wait(4.0)


# ─────────────────────────────────────────────────────────────
# 6. 예제 7.4 — 슬라이드 13 (문제) 뒤, 14 (풀이) 앞
# ─────────────────────────────────────────────────────────────
def _map74(x1, x2):
    return x1 * x1, x1 * x2


class Example74Jacobian2D(InteractiveScene):
    """f(x₁, x₂) = 4x₁x₂ (단위 정사각형), Y₁ = X₁², Y₂ = X₁X₂. 꼭짓점 넷을 옮겨 영역 B(y₂² < y₁ < 1) 를 그리고,
    역변환 x₁ = √y₁, x₂ = y₂/√y₁ 을 쓴다. 작은 상자 하나를 옮기면 넓이가 2x₁² = 2y₁ 배가 되므로 밀도는 그만큼 나눈다 —
    그것이 |J| = 1/(2y₁) 이다. g = 2y₂/y₁, 이중적분이 1 임을 끝에 적는다."""

    def construct(self):
        head = slide_title("Example 7.4")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. move the corners", "2. invert the map",
                                         "3. a small box scales", "4. write g(y1, y2)"], pos=(5.0, 2.1, 0), size=20)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        cfg = dict(include_ticks=True, stroke_width=2, stroke_color=GREY_B)
        axx = Axes(x_range=(0, 1.3, 0.5), y_range=(0, 1.3, 0.5), width=3.0, height=3.0, axis_config=cfg).move_to([-4.9, -0.5, 0])
        axy = Axes(x_range=(0, 1.3, 0.5), y_range=(0, 1.3, 0.5), width=3.0, height=3.0, axis_config=cfg).move_to([-0.6, -0.5, 0])
        nx = VGroup(Tex("x_1").scale(0.55).set_color(GREY_B).next_to(axx.c2p(1.3, 0), RIGHT, buff=0.1),
                    Tex("x_2").scale(0.55).set_color(GREY_B).next_to(axx.c2p(0, 1.3), UP, buff=0.1))
        ny = VGroup(Tex("y_1").scale(0.55).set_color(GREY_B).next_to(axy.c2p(1.3, 0), RIGHT, buff=0.1),
                    Tex("y_2").scale(0.55).set_color(GREY_B).next_to(axy.c2p(0, 1.3), UP, buff=0.1))
        sq = Polygon(axx.c2p(0, 0), axx.c2p(1, 0), axx.c2p(1, 1), axx.c2p(0, 1)).set_fill(ACCENT, 0.3).set_stroke(ACCENT, 2)
        fname = Tex(R"f = 4x_1x_2\ \text{on the unit square}").scale(0.52).set_color(ACCENT).next_to(axx, UP, buff=0.35).align_to(axx, LEFT)
        rule = Tex(R"y_1 = x_1^2,\quad y_2 = x_1x_2").scale(0.6).set_color(MEAN_COLOR).next_to(axy, UP, buff=0.35).align_to(axy, LEFT)
        ones = VGroup(*[Tex("1").scale(0.5).set_color(GREY_B).next_to(a.c2p(*p), d, buff=0.1)
                        for a in (axx, axy) for p, d in (((1, 0), DOWN), ((0, 1), LEFT))])
        self.play(ShowCreation(axx), FadeIn(nx), FadeIn(ones[:2]), Write(fname))
        self.play(FadeIn(sq))
        self.play(ShowCreation(axy), FadeIn(ny), FadeIn(ones[2:]), Write(rule))
        self.wait(0.6)

        # 1. 꼭짓점 넷을 옮긴다 — 위 변 x₂ = 1 은 곡선 y₁ = y₂² 으로
        self.play(focus(0))
        corners = [(0, 0), (1, 0), (1, 1), (0, 1)]
        dots = VGroup(*[Dot(axx.c2p(*c), radius=0.07).set_fill(WARN, 1) for c in corners])
        self.play(FadeIn(dots))
        imgs = VGroup(*[Dot(axy.c2p(*_map74(*c)), radius=0.07).set_fill(WARN, 1) for c in corners])
        tags = VGroup(*[Tex(t).scale(0.42).set_color(WARN) for t in ("(0,0)", "(1,0)", "(1,1)", "(0,1)")])
        for tg, c, d in zip(tags, corners, (DL, DR, UR, UL)):
            tg.next_to(axx.c2p(*c), d, buff=0.08)
        self.play(FadeIn(tags))
        self.play(*[Transform(d.copy(), i) for d, i in zip(dots, imgs)], run_time=1.6)
        collapse = Tex(R"(0,1)\to(0,0)").scale(0.42).set_color(WARN).next_to(axy.c2p(0, 0), DL, buff=0.08)
        self.play(FadeIn(collapse))
        self.wait(0.5)
        top = Line(axx.c2p(0, 1), axx.c2p(1, 1)).set_stroke(CALM, 6)
        curve = ParametricCurve(lambda s: axy.c2p(s * s, s), t_range=(0, 1, 0.02)).set_stroke(CALM, 4)
        ctag = Tex(R"x_2 = 1\ \Rightarrow\ y_1 = y_2^2").scale(0.52).set_color(CALM).next_to(axy, DOWN, buff=0.5).align_to(axy, LEFT)
        self.play(ShowCreation(top))
        self.play(ShowCreation(curve), FadeIn(ctag))
        pts = [axy.c2p(s * s, s) for s in np.linspace(0, 1, 40)] + [axy.c2p(1, 0)]
        region = Polygon(*pts).set_fill(MEAN_COLOR, 0.3).set_stroke(MEAN_COLOR, 2)
        btag = Tex(R"B:\ 0 < y_2 < 1,\ y_2^2 < y_1 < 1").scale(0.52).set_color(MEAN_COLOR).next_to(ctag, DOWN, buff=0.12).align_to(ctag, LEFT)
        self.play(FadeIn(region), FadeIn(btag))
        self.wait(1.6)

        # 2. 역변환
        self.play(focus(1))
        inv = Tex(R"x_1 = \sqrt{y_1},\qquad x_2 = \frac{y_2}{\sqrt{y_1}}").scale(0.6).set_color(INK)
        inv.next_to(box, DOWN, buff=0.3).align_to([2.4, 0, 0], LEFT)
        self.play(Write(inv))
        self.wait(1.2)

        # 3. 작은 상자 하나를 옮기면 넓이가 2x₁² 배
        self.play(focus(2))
        c1, c2, s = 0.55, 0.55, 0.16
        bx = [(c1, c2), (c1 + s, c2), (c1 + s, c2 + s), (c1, c2 + s)]
        small = Polygon(*[axx.c2p(*p) for p in bx]).set_fill(WARN, 0.8).set_stroke(WHITE, 1.5)
        image = Polygon(*[axy.c2p(*_map74(*p)) for p in bx]).set_fill(WARN, 0.8).set_stroke(WHITE, 1.5)
        self.play(FadeIn(small))
        self.play(Transform(small.copy(), image), run_time=1.4)
        l3 = _lines([(R"\text{area}\times 2x_1^2 = \text{area}\times 2y_1", WARN),
                     R"|J| = \left|\frac{\partial(x_1,x_2)}{\partial(y_1,y_2)}\right| = \frac{1}{2y_1}"],
                    inv, scale=0.56, color=INK, gap=0.3, left_x=2.4)
        self.play(Write(l3[0]))
        self.wait(0.5)
        self.play(Write(l3[1]))
        self.wait(1.4)

        # 4. g 와 넓이 1
        self.play(focus(3))
        g = _lines([(R"g(y_1,y_2) = 4\sqrt{y_1}\,\frac{y_2}{\sqrt{y_1}}\cdot\frac{1}{2y_1} = \frac{2y_2}{y_1}", MEAN_COLOR),
                    R"\iint_B g\,dy_1\,dy_2 = \int_0^1 -4y_2\ln y_2\,dy_2 = 1"],
                   l3, scale=0.52, color=INK, gap=0.3, left_x=2.4)
        self.play(Write(g[0]))
        self.play(FlashAround(g[0], color=MEAN_COLOR, buff=0.08))
        self.wait(0.6)
        self.play(Write(g[1]))
        self.wait(4.0)


# ─────────────────────────────────────────────────────────────
# 7. 예제 7.5 — 슬라이드 18 (문제) 뒤, 19 (풀이) 앞
# ─────────────────────────────────────────────────────────────
def _chi1(y):
    return exp(-y / 2) / sqrt(2 * math.pi * y)


class Example75ChiSquare(InteractiveScene):
    """Y = (X − μ)²/σ² = Z². 표준화한 종에서 −1 < z < 1 의 양쪽(0.6826)이 y 축의 0 < y < 1 한 곳으로 포개진다.
    P(Y ≤ y) = 2∫₀^√y φ(z)dz 에 z = √u 를 넣으면 dz = du/(2√u) 라 g(y) = φ(√y)/√y = (1/√2π) y^{−1/2} e^{−y/2}.
    Γ(1/2) = √π 이므로 감마(1/2, 2), 곧 χ²(1) 이다. NotOneToOne 의 '두 몫이 더해진다' 를 이 예제로 끝까지 쓴다."""

    def construct(self):
        head = slide_title("Example 7.5")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. standardize to Z", "2. fold z = ±√y",
                                         "3. substitute z = √u", "4. gamma(1/2, 2) = χ²(1)"], pos=(4.8, 2.15, 0), size=19)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        axz = density_axes((-3.5, 3.5, 1), (0, 0.5, 0.1), width=5.6, height=2.0).move_to([-3.6, 1.3, 0])
        bell = normal_graph(axz, 0, 1, -3.5, 3.5, ACCENT)
        marks = x_marks(axz, [-1, 0, 1], [R"\mu-\sigma", R"\mu", R"\mu+\sigma"])
        xname = Tex(R"X \sim n(x;\,\mu,\sigma)").scale(0.6).set_color(ACCENT).next_to(axz, UP, buff=0.05).align_to(axz, LEFT)
        self.play(ShowCreation(axz), FadeIn(marks), Write(xname))
        self.play(ShowCreation(bell))
        self.wait(0.5)

        # 1. 표준화 — 같은 종, 눈금만 −1, 0, 1
        self.play(focus(0))
        zdef = Tex(R"Z = \frac{X-\mu}{\sigma},\qquad Y = \frac{(X-\mu)^2}{\sigma^2} = Z^2").scale(0.6).set_color(MEAN_COLOR)
        zdef.next_to(box, DOWN, buff=0.25).align_to([COL_X, 0, 0], LEFT)
        self.play(Write(zdef))
        zmarks = x_marks(axz, [-1, 0, 1], ["-1", "0", "1"])
        zname = Tex(R"Z \sim n(z;\,0,1)").scale(0.6).set_color(ACCENT).move_to(xname).align_to(xname, LEFT)
        self.play(Transform(marks, zmarks), Transform(xname, zname))
        self.wait(1.2)

        # 2. y = 1 은 −1 < z < 1 — 두 쪽이 한 곳으로
        self.play(focus(1))
        left = area_under(axz, bell, -1, 0, WARN, 0.6)
        right = area_under(axz, bell, 0, 1, CALM, 0.6)
        self.play(FadeIn(left), FadeIn(right))
        p1 = Tex(R"P(Y < 1) = P(-1 < Z < 1) = 0.6826").scale(0.58).set_color(INK).next_to(zdef, DOWN, buff=0.2).align_to(zdef, LEFT)
        self.play(Write(p1))
        axy = density_axes((0, 4, 1), (0, 1.2, 0.5), width=4.2, height=1.7).move_to([4.5, -1.5, 0])
        gy = axy.get_graph(_chi1, x_range=(0.12, 4, 0.02)).set_stroke(MEAN_COLOR, 3)
        half = axy.get_graph(lambda y: _chi1(y) / 2, x_range=(0.12, 1, 0.02))
        a_half = axy.get_area_under_graph(half, x_range=(0.12, 1), fill_color=CALM, fill_opacity=0.6)
        a_full = axy.get_area_under_graph(gy, x_range=(0.12, 1), fill_color=WARN, fill_opacity=0.35)
        ymk = x_marks(axy, [1, 4])
        yname = Tex(R"g(y)").scale(0.6).set_color(MEAN_COLOR).move_to(axy.c2p(3.0, 1.0))
        self.play(ShowCreation(axy), FadeIn(ymk), FadeIn(yname))
        self.play(Transform(right.copy(), a_half), Transform(left.copy(), a_full), run_time=1.6)
        self.play(ShowCreation(gy))
        fold = label("two branches, one y", 20, MEAN_COLOR).move_to(axy.c2p(2.9, 0.6))
        self.play(FadeIn(fold))
        self.wait(1.6)

        # 3. 치환 z = √u
        self.play(focus(2))
        l3 = _lines([R"P(Y \le y) = 2\int_0^{\sqrt{y}}\phi(z)\,dz",
                     (R"z = \sqrt{u},\qquad dz = \frac{du}{2\sqrt{u}}", MEAN_COLOR),
                     R"= \int_0^{y}\frac{\phi(\sqrt{u})}{\sqrt{u}}\,du",
                     (R"g(y) = \frac{\phi(\sqrt{y})}{\sqrt{y}} = \frac{1}{\sqrt{2\pi}}\,y^{-1/2}e^{-y/2}", MEAN_COLOR)],
                    axz, scale=0.56, color=INK, buff=0.14, gap=0.45, left_x=-6.4)
        for t in l3:
            self.play(Write(t))
            self.wait(0.4)
        self.wait(1.2)

        # 4. 감마(1/2, 2) 와 같다
        self.play(focus(3))
        l4 = _lines([R"\text{gamma}(\alpha=\tfrac12,\ \beta=2):\ \frac{1}{\Gamma(1/2)\sqrt{2}}\,y^{-1/2}e^{-y/2}",
                     (R"\Gamma(\tfrac12) = \sqrt{\pi}\ \Rightarrow\ \text{same}\ \Rightarrow\ Y \sim \chi^2(1)", WARN)],
                    ymk, scale=0.52, color=INK, buff=0.12, gap=0.25, left_x=COL_X + 0.3)
        self.play(Write(l4[0]))
        self.wait(0.6)
        self.play(Write(l4[1]))
        self.play(FlashAround(l4[1], color=WARN, buff=0.08))
        self.wait(4.0)


# ─────────────────────────────────────────────────────────────
# 8. 예제 7.7 — 슬라이드 23 (문제) 뒤, 24 (풀이) 앞
# ─────────────────────────────────────────────────────────────
class Example77NormalMGF(InteractiveScene):
    """M_X(t) = ∫ e^{tx} n(x; μ, σ) dx. e^{tx} 로 잰 종은 μ + σ²t 로 옮겨 간 종을 e^{μt + σ²t²/2} 배 한 것이다(완전제곱).
    옮겨 간 종의 넓이는 1 이므로 남는 것이 M(t) 다. μ = 2, σ = 1, t = 0.5 로 그려 e^{1.125} = 3.08 이 잰 종의 넓이임을 보인다."""

    def construct(self):
        head = slide_title("Example 7.7")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. weight the bell", "2. complete the square",
                                         "3. leftover bell has area 1", "4. read off M(t)"], pos=(4.8, 2.15, 0), size=20)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        mdef = Tex(R"M_X(t) = E\left(e^{tX}\right) = \int_{-\infty}^{\infty} e^{tx}\,n(x;\mu,\sigma)\,dx").scale(0.62).set_color(MEAN_COLOR)
        mdef.next_to(head[1], DOWN, buff=0.25).align_to(head[0], LEFT)
        self.play(Write(mdef))

        mu, sig = 2.0, 1.0
        ax = density_axes((-1, 7, 1), (0, 1.5, 0.5), width=6.8, height=3.0).move_to([-3.4, -1.3, 0])
        f = normal_graph(ax, mu, sig, -1, 7, ACCENT)
        fname = Tex(R"f(x) = n(x;\,2,\,1)").scale(0.6).set_color(ACCENT).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        self.play(ShowCreation(ax), FadeIn(x_marks(ax, [2], [R"\mu"])), Write(fname))
        self.play(ShowCreation(f))
        self.wait(0.5)

        # 1. e^{tx} 로 잰 종 — 오른쪽으로 옮겨 가며 커진다
        self.play(focus(0))
        ttag = Tex(R"t = 0.00").scale(0.62).set_color(WARN).move_to([COL_X + 0.5, 1.15, 0])
        self.play(FadeIn(ttag))
        prev = ax.get_graph(lambda x: npdf(x, mu, sig), x_range=(-1, 7, 0.02)).set_stroke(WARN, 3)
        prev_area = area_under(ax, prev, -1, 7, WARN, 0.3)
        self.play(ShowCreation(prev), FadeIn(prev_area))
        for t in (0.2, 0.35, 0.5):
            g = ax.get_graph(lambda x, t=t: exp(t * x) * npdf(x, mu, sig), x_range=(-1, 7, 0.02)).set_stroke(WARN, 3)
            ga = area_under(ax, g, -1, 7, WARN, 0.3)
            nt = Tex(R"t = %.2f" % t).scale(0.62).set_color(WARN).move_to(ttag)
            self.play(Transform(prev, g), Transform(prev_area, ga), Transform(ttag, nt), run_time=0.9)
            self.wait(0.2)
        peak_line = dashed(ax.c2p(2.5, 0), ax.c2p(2.5, 1.3), WARN)
        peak = Tex(R"\mu+\sigma^2 t").scale(0.55).set_color(WARN).next_to(ax.c2p(2.5, 1.3), UP, buff=0.08)
        wtag = Tex(R"e^{tx}f(x):\ \text{a taller bell at } \mu+\sigma^2 t").scale(0.56).set_color(WARN)
        wtag.next_to(ttag, DOWN, buff=0.3).align_to([COL_X, 0, 0], LEFT)
        atag = Tex(R"\text{area} = M(t)").scale(0.58).set_color(WARN).next_to(wtag, DOWN, buff=0.15).align_to(wtag, LEFT)
        self.play(ShowCreation(peak_line), FadeIn(peak), Write(wtag))
        self.play(FadeIn(atag))
        self.wait(1.4)

        # 2. 완전제곱
        self.play(focus(1))
        sqr = _lines([R"tx - \frac{(x-\mu)^2}{2\sigma^2}",
                      (R"= -\frac{(x-\mu-\sigma^2 t)^2}{2\sigma^2} + \mu t + \frac{\sigma^2 t^2}{2}", MEAN_COLOR)],
                     atag, scale=0.58, color=INK, buff=0.12, gap=0.3, left_x=COL_X)
        self.play(Write(sqr[0]))
        self.wait(0.4)
        self.play(Write(sqr[1]))
        self.wait(1.4)

        # 3. 남는 종의 넓이는 1 — 잰 종(윤곽)은 두고 옮겨 간 종을 칠한다
        self.play(focus(2))
        unit = normal_graph(ax, mu + sig * sig * 0.5, sig, -1, 7, CALM)
        ua = area_under(ax, unit, -1, 7, CALM, 0.5)
        self.play(FadeOut(prev_area), ShowCreation(unit), FadeIn(ua), run_time=1.2)
        one = Tex(R"\int n(x;\,\mu+\sigma^2 t,\,\sigma)\,dx = 1").scale(0.58).set_color(CALM).next_to(sqr, DOWN, buff=0.28).align_to(sqr, LEFT)
        self.play(Write(one))
        self.wait(1.4)

        # 4. M(t)
        self.play(focus(3))
        ans = Tex(R"M_X(t) = e^{\mu t + \sigma^2 t^2/2}").scale(0.68).set_color(MEAN_COLOR).next_to(one, DOWN, buff=0.28).align_to(sqr, LEFT)
        chk = Tex(R"t = 0.5:\ e^{1.125} = 3.08 = \text{area}").scale(0.5).set_color(GREY_B).next_to(ans, DOWN, buff=0.18).align_to(sqr, LEFT)
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.1))
        self.play(FadeIn(chk))
        self.wait(4.0)
