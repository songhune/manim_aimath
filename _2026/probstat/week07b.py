# -*- coding: utf-8 -*-
"""확률과통계 「확률변수의 함수」 장 (Walpole Chapter 7) — 변수 변환 · 야코비안 · 일대일이 아닌 변환 · 적률생성함수.

파일 이름이 week07b 인 까닭: week07.py 는 6장(연속형 확률분포), week08.py 는 8장(표본분포)이다. 7장은 계획서의 10주차
자리에 들며 16차(11/6, 가정)에 8장 앞에서 다룬다(2026-11-05). 도구와 규칙은 week08.py 와 같다.
이 장도 **개념 영상 네 편뿐**이고 예제 영상은 없다(2026-11-03 사용자 결정 — 영상은 꼭 필요한 곳에만, 자리는 그 개념
슬라이드 **앞**). 네 편은 정지 그림으로는 안 보이는 것만 고른 것이다: 일대일 변환에서 확률 막대가 자리만 옮기는 것,
연속형에서 축이 늘어나면 넓이를 지키려고 높이가 줄어드는 것(야코비안), 일대일이 아니면 역상 둘의 밀도가 포개지는 것,
적률생성함수가 e^{tx} 로 다시 잰 무게의 합이고 그 기울기가 평균인 것.
화면 문구는 영어, 여섯 낱말까지(`ps_common.label`). 사람은 나오지 않는다.

덱 삽입 자리 (원본 PS1_07_restyled.pptx 23장 기준. 레이아웃 정리 뒤의 번호는 insert_videos.py 의 PS1_07_INSERT 가 정본이다.
네 편 모두 "N 앞" = 그 개념 슬라이드 바로 앞):
    DiscreteTransformation           3 앞    정리 7.1 — 이산형 일대일 변환, g(y) = f(w(y)), 기하분포 막대가 y = x² 자리로
    JacobianStretch                  8 앞    정리 7.3 — 연속형, y = 2x − 3 으로 축이 2 배 늘고 높이가 반이 됨, |J| = 1/2
    NotOneToOne                     13 앞    일대일이 아닌 변환 — y = x² (−1 < x < 2), 0 < y < 1 에 역상 둘, g = f(−√y)|J₁| + f(√y)|J₂|
    MomentGeneratingFunction        17 앞    정의 7.1 · 7.2 — M_X(t) = E(e^{tX}), 이항 b(x; 4, 1/2) 의 무게 e^{tx}, M'(0) = μ, 곱셈 성질

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
from _2026.probstat.week05 import dashed
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
        head = slide_title("Transformation of a Discrete Variable")
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
