# -*- coding: utf-8 -*-
"""확률과통계 「수학적 기댓값」 장 (Walpole Chapter 4) — 기댓값 · 분산 · 공분산 · 상관계수 · 선형결합 · 체비셰프.

강의 교안 `확률과통계/교육메모/05주차.md` 의 「영상 계획」(2026-09-21) 을 옮긴 것이다. 도구와 규칙은 week04.py 와 같다.
개념 영상은 정의 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음·풀이 슬라이드 앞이다(하네스 3.6).
소재는 덱(PS1_04_restyled.pptx, 레이아웃 정리 뒤 62장)의 예제로 한정한다. 화면 문구는 영어, 여섯 낱말까지.

이 장의 약속 (2026-09-18 의 3.14 · 3.15 개정에서 굳힌 것, `probstat-scene-pacing` 메모):
    개념 영상은 이름(기댓값·분산·공분산·상관계수)을 먼저 걸고, 이산(합)과 연속(적분)을 나눈다.
    예제 영상은 풀이 단계를 먼저 목록으로 걸어 두고(`steps_panel`) 한 단계씩 진행한다.
    적분은 (1) 식 세우기 → (2) 피적분함수 정리 → (3) 원시함수 → (4) 위끝·아래끝 대입까지 줄마다 다 적는다.
    합은 (1) 값 목록 → (2) 곱 → (3) 더하기. 곱한 값을 표의 셋째 줄로 보인다(`pmf_table`).

덱 삽입 자리 (원본 PS1_04_restyled.pptx 62장 기준 — 2026-09-21 도구/레이아웃_정리_PS1_04.py 로 51장을 정리한 것.
insert_videos.py 의 PS1_04_INSERT 와 같다. "N 앞" 은 개념 영상, "N 뒤" 는 예제 영상(풀이 N+1 앞)):
    7차 9/22 — 4.1, 4.2 분산까지 (원본 1–32)
    ExpectedValueAsBalance          3 앞    정의 4.1 (막대의 균형점, 합 → 적분)
    Example41Components             4 뒤    예제 4.1
    Example42Salesperson            6 뒤    예제 4.2
    Example43DeviceLife             8 뒤    예제 4.3
    ExpectationOfFunction          10 앞    정리 4.1 (같은 확률, 새 값 g(x))
    Example44CarWash               11 뒤    예제 4.4
    Example45FourXPlus3            13 뒤    예제 4.5
    Example46TableXY               16 뒤    예제 4.6
    Example47RatioYX               18 뒤    예제 4.7
    VarianceAsSpread               20 앞    정의 4.3 · 정리 4.2 (같은 평균, 다른 퍼짐 → σ² = E(X²) − μ² 유도)
    Example48TwoCompanies          22 뒤    예제 4.8 (풀이 23·24)
    Example49Defectives            25 뒤    예제 4.9
    Example410WaterDemand          27 뒤    예제 4.10
    Example411LinearDiscrete       29 뒤    예제 4.11
    Example412LinearContinuous     31 뒤    예제 4.12
    8차 9/29 — 4.2 공분산부터 4.4 까지 (원본 33–62)
    CovarianceSign                 33 앞    정의 4.4 · 정리 4.4 (부호 = 같이 움직이는 방향, 지름길 유도)
    CorrelationScale               34 앞    정의 4.5 (단위를 없앤 공분산, −1 ≤ ρ ≤ 1)
    Example413Covariance           35 뒤    예제 4.13
    Example415Correlation          37 뒤    예제 4.15 (4.16 은 39·40, 예제 4.14 가 덱에 없어 영상 없음)
    LinearShiftScale               41 앞    정리 4.5 · 4.6 (E(aX+b) = aμ + b)
    VarianceOfSum                  43 앞    정리 4.9 (Var(aX+bY) 의 교차항, 독립이면 0)
    Example417418Rework            45 뒤    예제 4.17 (4.18 은 47·48 — 한 영상이 둘을 겸한다)
    Example419ShiftSquare          49 뒤    예제 4.19
    Example420Drink                51 뒤    예제 4.20
    Example421Independent          53 뒤    예제 4.21
    Example422423Variance          55 뒤    예제 4.22 (4.23 은 57·58 — 한 영상이 둘을 겸한다)
    ChebyshevBand                  59 앞    정리 4.10 (μ ± kσ 띠, 최소 1 − 1/k²)
    Example427Chebyshev            60 뒤    예제 4.27

렌더 (저장소 루트에서):
    ./render.sh check _2026/probstat/week05.py
    ./render.sh ppt   _2026/probstat/week05.py Example41Components
"""
from math import comb

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN, BODY_FONT,
    chito, label, note, panel, ring, slide_title, bar,
)
from _2026.probstat.week02 import letter_chip
from _2026.probstat.week04 import grid_table, TABLE31, density_axes, area_under, x_marks, frac

GREEN_PEN = GREEN_C


# ─────────────────────────────────────────────────────────────
# 도구 — 풀이 단계 상자, 수식 열, pmf 표
# ─────────────────────────────────────────────────────────────
def steps_panel(items, pos=(3.5, 2.0, 0), size=24, buff=0.2):
    """풀이 단계 목록을 오른쪽 위에 걸어 둔다. focus(k) 가 k 번째만 노랗게 밝힌다.
    돌려주는 것: (steps VGroup, 테두리 상자, focus)."""
    steps = VGroup(*[label(t, size, INK) for t in items])
    steps.arrange(DOWN, buff=buff, aligned_edge=LEFT).move_to(pos)
    box = panel(steps, GREY_C, buff=buff)

    def focus(k):
        return AnimationGroup(*[st.animate.set_color(MEAN_COLOR if i == k else GREY_C)
                                for i, st in enumerate(steps)])
    return steps, box, focus


def column(lines, ref, color=INK, scale=0.6, buff=0.22, left_x=None, gap=0.5, direction=DOWN):
    """수식 줄을 ref 아래(또는 direction 쪽)에 왼쪽 맞춤으로 쌓는다. 줄마다 Tex 하나."""
    texs = [Tex(t).scale(scale).set_color(color) for t in lines]
    col = VGroup(*texs).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    col.next_to(ref, direction, buff=gap)
    if left_x is not None:
        col.align_to([left_x, 0, 0], LEFT)
    return col


def pmf_table(xs, rows, w=0.95, h=0.6, x_name="x", scale=0.7):
    """Walpole 식 가로 표. 첫 줄은 x 값, 아래 줄들은 rows = [(이름 LaTeX, [칸 LaTeX ...]), ...].
    돌려주는 것: (전체 VGroup, cells[(r, c)] 사각형, texts[(r, c)] 수식, heads). r=0 이 x 줄."""
    all_rows = [(x_name, [str(x) for x in xs])] + list(rows)
    cells, texts, heads = {}, {}, VGroup()
    grid = VGroup()
    for r, (name, vals) in enumerate(all_rows):
        hd = Tex(name).scale(scale).set_color(ACCENT if r == 0 else INK).move_to([-w * 0.9, -r * h, 0])
        heads.add(hd)
        for c, v in enumerate(vals):
            rect = Rectangle(width=w, height=h).set_stroke(GREY_C, 1.2)
            rect.move_to([c * w, -r * h, 0])
            t = Tex(v).scale(scale).set_color(ACCENT if r == 0 else INK).move_to(rect)
            cells[(r, c)], texts[(r, c)] = rect, t
            grid.add(rect, t)
    whole = VGroup(grid, heads)
    return whole, cells, texts, heads


def highlight(rect, color=MEAN_COLOR, opacity=0.35):
    return rect.copy().set_fill(color, opacity).set_stroke(color, 3)


def fulcrum_at(point, color=MEAN_COLOR, height=0.3):
    tri = Triangle().set_height(height).rotate(PI)
    tri.set_fill(color, 1).set_stroke(width=0)
    tri.next_to(point, DOWN, buff=0.02)
    return tri


def pmf_bars(line, xs, fs, vmax, color=ACCENT, width=0.5, height=2.0):
    """수직선 위 x 자리마다 높이 f 의 막대와 값 꼬리표. (bars, tags)."""
    bars = VGroup()
    for x, f in zip(xs, fs):
        b = bar(f, vmax, width=width, height=height, color=color)
        b.move_to(line.n2p(x), aligned_edge=DOWN).shift(UP * 0.02)
        bars.add(b)
    tags = VGroup(*[Tex(str(f)).scale(0.45).set_color(GREY_B).next_to(b, UP, buff=0.06) for b, f in zip(bars, fs)])
    return bars, tags


def cell_tex(cells, key, s, color=INK, scale=0.7):
    return Tex(s).scale(scale).set_color(color).move_to(cells[key])


def tidy_heads(cells, heads):
    """줄 이름을 칸 왼쪽에 오른쪽 맞춤으로 붙인다. 긴 이름이 칸을 덮지 않게."""
    edge = cells[(0, 0)].get_left()[0] - 0.12
    for hd in heads:
        hd.align_to([edge, 0, 0], RIGHT)
    return heads


def dashed(p1, p2, color=GREY_B):
    return DashedLine(p1, p2).set_stroke(color, 2)


# ─────────────────────────────────────────────────────────────
# 1. 기댓값 = 막대의 균형점 — 슬라이드 3 (정의 4.1) 앞
# ─────────────────────────────────────────────────────────────
class ExpectedValueAsBalance(InteractiveScene):
    """이름을 먼저 건다: expected value = mean μ. 「확률변수와 확률분포」 장의 두 분포를 다시 쓴다.
    앞: 예제 3.9 의 에어백 분포(1·4·6·4·1 /16). 막대를 세우고 받침점을 옮겨 균형이 잡히는 곳 2 를 찾는다.
    μ = Σ x f(x) 를 항마다 적는다. 중간: 예제 3.8 의 노트북 분포(136·51·3 /190). 균형점 0.3 은 나올 수 없는 값이다.
    뒤: 연속형은 합이 적분이 된다. 예제 3.11 의 x²/3 (−1<x<2) 에서 ∫ x f(x) dx = 5/4."""

    def construct(self):
        head = slide_title("Expected Value")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\mu = E(X)").scale(0.9).set_color(MEAN_COLOR).next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.8)
        self.play(Write(name))

        # ── 이산 1: 예제 3.9 (에어백) — 대칭이라 균형점이 눈에 보인다
        line = NumberLine(x_range=(0, 4, 1), width=6.0, include_numbers=True).move_to([-3.0, -0.6, 0])
        probs = [(1, 16), (4, 16), (6, 16), (4, 16), (1, 16)]
        bars = VGroup()
        for x, (n, d) in enumerate(probs):
            b = bar(n / d, 6 / 16, width=0.55, height=2.6, color=ACCENT)
            b.move_to(line.n2p(x), aligned_edge=DOWN).shift(UP * 0.02)
            bars.add(b)
        tags = VGroup(*[Tex(R"\tfrac{%d}{%d}" % (n, d)).scale(0.5).set_color(GREY_B).next_to(b, UP, buff=0.08)
                        for b, (n, d) in zip(bars, probs)])
        src = note("Example 3.9, airbags", 22, GREY_B).next_to(line, DOWN, buff=1.05).align_to(line, LEFT)
        self.play(ShowCreation(line), FadeIn(src))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.12), FadeIn(tags), run_time=1.2)
        self.wait(0.5)

        # 받침점을 왼쪽에서 밀어 균형이 잡히는 곳에 세운다
        tracker = ValueTracker(0.6)
        ful = fulcrum_at(line.n2p(0.6))
        ful.add_updater(lambda m: m.next_to(line.n2p(tracker.get_value()), DOWN, buff=0.02))
        beam = Line(line.n2p(0) + LEFT * 0.4, line.n2p(4) + RIGHT * 0.4).set_stroke(MEAN_COLOR, 3)
        beam.add_updater(lambda m: m.set_angle(0.12 * (2 - tracker.get_value())).move_to(line.n2p(2)))
        weights = label("weights are probabilities", 24, GREY_B).next_to(src, DOWN, buff=0.15).align_to(src, LEFT)
        self.play(FadeIn(ful), FadeIn(beam), FadeIn(weights))
        self.play(tracker.animate.set_value(2.0), run_time=1.6)
        bal = label("balance point", 26, MEAN_COLOR).next_to(line.n2p(4), RIGHT, buff=0.4)
        self.play(FadeIn(bal))
        self.wait(0.6)

        # 식: 값 × 확률을 다 더한다
        col = column([
            R"\mu = \sum_x x\,f(x)",
            R"= 0\cdot\tfrac{1}{16} + 1\cdot\tfrac{4}{16} + 2\cdot\tfrac{6}{16} + 3\cdot\tfrac{4}{16} + 4\cdot\tfrac{1}{16}",
            R"= \tfrac{0 + 4 + 12 + 12 + 4}{16} = \tfrac{32}{16} = 2",
        ], name, scale=0.6, gap=0.45).align_to([0.6, 0, 0], LEFT)
        col[0].set_color(ACCENT)
        d_tag = label("discrete: sum", 24, ACCENT).next_to(col, UP, buff=0.15).align_to(col, LEFT)
        self.play(FadeIn(d_tag), Write(col[0]))
        self.play(Write(col[1]), run_time=1.2)
        self.play(Write(col[2]))
        self.play(FlashAround(col[2], color=MEAN_COLOR, buff=0.1))
        self.wait(1.2)

        # ── 이산 2: 예제 3.8 (노트북) — 균형점 0.3 은 나올 수 없는 값
        probs2 = [(136, 190), (51, 190), (3, 190)]
        bars2 = VGroup()
        for x, (n, d) in enumerate(probs2):
            b = bar(n / d, 136 / 190, width=0.55, height=2.6, color=CALM)
            b.move_to(line.n2p(x), aligned_edge=DOWN).shift(UP * 0.02)
            bars2.add(b)
        tags2 = VGroup(*[Tex(R"\tfrac{%d}{%d}" % (n, d)).scale(0.5).set_color(GREY_B).next_to(b, UP, buff=0.08)
                         for b, (n, d) in zip(bars2, probs2)])
        src2 = note("Example 3.8, laptops", 22, GREY_B).move_to(src)
        col2 = column([
            R"\mu = 0\cdot\tfrac{136}{190} + 1\cdot\tfrac{51}{190} + 2\cdot\tfrac{3}{190}",
            R"= \tfrac{51 + 6}{190} = \tfrac{57}{190} = 0.3",
        ], name, scale=0.6, gap=0.45).align_to([0.6, 0, 0], LEFT)
        beam.clear_updaters()
        self.play(FadeOut(bars), FadeOut(tags), FadeOut(src), FadeOut(col), FadeOut(bal), FadeOut(beam))
        self.play(FadeIn(src2), LaggedStartMap(GrowFromEdge, bars2, edge=DOWN, lag_ratio=0.12), FadeIn(tags2), run_time=1.0)
        self.play(Write(col2[0]), run_time=1.0)
        self.play(Write(col2[1]))
        self.play(tracker.animate.set_value(0.3), run_time=1.4)
        nv = label("not a possible value", 26, MEAN_COLOR).next_to(line.n2p(4), RIGHT, buff=0.4)
        self.play(FadeIn(nv), FlashAround(col2[1], color=MEAN_COLOR, buff=0.1))
        self.wait(1.4)

        # ── 연속: 합이 적분으로
        ful.clear_updaters()
        self.play(FadeOut(bars2), FadeOut(tags2), FadeOut(src2), FadeOut(col2), FadeOut(nv), FadeOut(ful),
                  FadeOut(line), FadeOut(weights), FadeOut(d_tag))
        axes = density_axes((-1, 2, 1), (0, 1.4, 1), width=5.2, height=2.6).move_to([-3.2, -0.9, 0])
        g = axes.get_graph(lambda x: x * x / 3, x_range=(-1, 2)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, -1, 2, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [-1, 0, 1, 2])
        f_tag = Tex(R"f(x) = \tfrac{x^2}{3},\ -1 < x < 2").scale(0.6).set_color(ACCENT).next_to(axes, UP, buff=0.1)
        src3 = note("Example 3.11", 22, GREY_B).next_to(axes, DOWN, buff=0.95).align_to(axes, LEFT)
        self.play(ShowCreation(axes), FadeIn(marks), FadeIn(src3))
        self.play(ShowCreation(g), FadeIn(area), FadeIn(f_tag))
        c_tag = label("continuous: integral", 24, CALM).move_to(d_tag).align_to([0.6, 0, 0], LEFT)
        col3 = column([
            R"\mu = \int_{-\infty}^{\infty} x\,f(x)\,dx",
            R"= \int_{-1}^{2} x\cdot\tfrac{x^2}{3}\,dx = \int_{-1}^{2} \tfrac{x^3}{3}\,dx",
            R"= \Big[\tfrac{x^4}{12}\Big]_{-1}^{2} = \tfrac{16}{12} - \tfrac{1}{12} = \tfrac{15}{12} = \tfrac{5}{4}",
        ], name, scale=0.6, gap=0.45).align_to([0.6, 0, 0], LEFT)
        col3[0].set_color(CALM)
        self.play(FadeIn(c_tag), Write(col3[0]))
        self.play(Write(col3[1]), run_time=1.2)
        self.play(Write(col3[2]), run_time=1.2)
        ful2 = fulcrum_at(axes.c2p(1.25, 0))
        bal2 = label("balance point", 24, MEAN_COLOR).next_to(axes.c2p(2, 0), RIGHT, buff=0.45)
        self.play(FadeIn(ful2), FadeIn(bal2), FlashAround(col3[2], color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 예제 4.1 부품 7개 중 3개 — 슬라이드 4 뒤 (5 앞)
# ─────────────────────────────────────────────────────────────
class Example41Components(InteractiveScene):
    """양품 4 · 불량 3 에서 셋을 뽑을 때 양품 수 X 의 기댓값. 단계 넷을 걸고 하나씩:
    1 X 의 값 0·1·2·3 → 2 f(x) 를 세어서(초기하, 「확률변수와 확률분포」 장의 3.8 과 같은 셈) 1·12·18·4 /35
    → 3 x·f(x) 를 셋째 줄로 → 4 더해서 60/35 = 12/7 ≈ 1.7."""

    def construct(self):
        head = slide_title("Example 4.1")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 소재: 부품 일곱, 셋을 고른다
        parts = VGroup(*[letter_chip("G", 0.5, ACCENT) for _ in range(4)],
                       *[letter_chip("D", 0.5, WARN) for _ in range(3)])
        parts.arrange(RIGHT, buff=0.12).move_to([-3.9, 2.15, 0])
        box = panel(parts, MUTED, buff=0.18)
        ask = note("pick 3 of 7", 22, INK).next_to(box, DOWN, buff=0.18)
        xdef = Tex(R"X = \text{good ones}", t2c={R"\text{good ones}": ACCENT}).scale(0.7).next_to(ask, DOWN, buff=0.12)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, parts, lag_ratio=0.06))
        self.play(FadeIn(ask), FadeIn(xdef))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. list the values", "2. count f(x)",
                                               "3. multiply x f(x)", "4. add them up"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 값 목록: 표의 첫 줄
        self.play(focus(0))
        blank = [R"\ "] * 4
        table, cells, texts, heads = pmf_table([0, 1, 2, 3], [(R"f(x)", blank), (R"x\,f(x)", blank)], w=1.25, h=0.62)
        table.move_to([-2.6, -1.0, 0])
        self.play(FadeIn(heads[0]), *[FadeIn(texts[(0, c)]) for c in range(4)],
                  *[ShowCreation(cells[(0, c)]) for c in range(4)])
        self.wait(0.6)

        # ── 2. f(x) 를 센다: 초기하 셈, 첫 칸은 풀어서
        self.play(focus(1))
        formula = Tex(R"f(x) = \frac{\binom{4}{x}\binom{3}{3-x}}{\binom{7}{3}} = \frac{\binom{4}{x}\binom{3}{3-x}}{35}",
                      t2c={R"\binom{4}{x}": ACCENT, R"\binom{3}{3-x}": WARN}).scale(0.72)
        formula.next_to(steps_box, DOWN, buff=0.45).align_to([0.75, 0, 0], LEFT)
        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(heads[1]), *[ShowCreation(cells[(1, c)]) for c in range(4)])
        vals = [(comb(4, x) * comb(3, 3 - x)) for x in range(4)]      # 1, 12, 18, 4
        first = Tex(R"f(0) = \frac{\binom{4}{0}\binom{3}{3}}{35} = \frac{1\cdot 1}{35} = \frac{1}{35}",
                    t2c={R"\binom{4}{0}": ACCENT, R"\binom{3}{3}": WARN}).scale(0.66)
        first.next_to(formula, DOWN, buff=0.3).align_to(formula, LEFT)
        marks = VGroup(*[ring(c, WARN, 0.04) for c in parts[4:]])
        hl = highlight(cells[(1, 0)])
        self.play(FadeIn(hl), ShowCreation(marks), Write(first), run_time=1.2)
        t = Tex(R"\tfrac{1}{35}").scale(0.7).set_color(INK).move_to(cells[(1, 0)])
        self.play(FadeIn(t), FadeOut(marks), FadeOut(hl))
        self.wait(0.6)
        self.play(FadeOut(first))
        for x in range(1, 4):
            marks = VGroup(*[ring(c, ACCENT, 0.04) for c in parts[:x]],
                           *[ring(c, WARN, 0.04) for c in parts[4:4 + (3 - x)]])
            t = Tex(R"\tfrac{%d}{35}" % vals[x]).scale(0.7).set_color(INK).move_to(cells[(1, x)])
            self.play(ShowCreation(marks), FadeIn(t), run_time=0.55)
            self.play(FadeOut(marks), run_time=0.2)
        chk = Tex(R"\tfrac{1 + 12 + 18 + 4}{35} = 1").scale(0.6).set_color(GREY_B).next_to(table, RIGHT, buff=0.5).align_to(cells[(1, 3)], DOWN)
        self.play(FadeIn(chk))
        self.wait(0.7)

        # ── 3. x · f(x) 를 셋째 줄로
        self.play(focus(2), FadeOut(chk))
        self.play(FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        prods = [0 * 1, 1 * 12, 2 * 18, 3 * 4]                          # 0, 12, 36, 12
        for x in range(4):
            hx, hf = highlight(cells[(0, x)], ACCENT, 0.3), highlight(cells[(1, x)], ACCENT, 0.3)
            t = Tex(R"\tfrac{%d}{35}" % prods[x] if prods[x] else "0").scale(0.7).set_color(MEAN_COLOR).move_to(cells[(2, x)])
            self.play(FadeIn(hx), FadeIn(hf), run_time=0.3)
            self.play(FadeIn(t), FadeOut(hx), FadeOut(hf), run_time=0.45)
        self.wait(0.6)

        # ── 4. 더한다
        self.play(focus(3))
        ans = column([
            R"\mu = E(X) = \sum_{x=0}^{3} x\,f(x)",
            R"= \tfrac{0 + 12 + 36 + 12}{35} = \tfrac{60}{35} = \tfrac{12}{7} \approx 1.7",
        ], formula, scale=0.66, gap=0.35).align_to(formula, LEFT)
        ans[1].set_color(MEAN_COLOR)
        self.play(Write(ans[0]))
        self.play(Write(ans[1]), run_time=1.2)
        self.play(FlashAround(ans[1], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 예제 4.2 영업사원의 수수료 — 슬라이드 6 뒤 (7 앞)
# ─────────────────────────────────────────────────────────────
class Example42Salesperson(InteractiveScene):
    """약속 둘, 독립. 첫째 0.7 로 $1000, 둘째 0.4 로 $1500. 단계 셋: 1 합계 넷을 나열 → 2 확률은 곱으로
    (0.3)(0.6)=0.18, (0.7)(0.6)=0.42, (0.3)(0.4)=0.12, (0.7)(0.4)=0.28 → 3 값 × 확률을 더해 $1300."""

    def construct(self):
        head = slide_title("Example 4.2")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 소재: 약속 둘
        deals = VGroup(
            Tex(R"\mathrm{deal\ 1:}\ 0.7,\ \$1000").scale(0.7).set_color(ACCENT),
            Tex(R"\mathrm{deal\ 2:}\ 0.4,\ \$1500").scale(0.7).set_color(CALM),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-4.0, 2.1, 0])
        box = panel(deals, MUTED, buff=0.2)
        ind = note("independent", 22, GREY_B).next_to(box, DOWN, buff=0.15)
        self.play(FadeIn(box), FadeIn(deals), FadeIn(ind))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. list the four totals", "2. multiply the probabilities",
                                               "3. multiply and add"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 합계 넷
        self.play(focus(0))
        blank = [R"\ "] * 4
        table, cells, texts, heads = pmf_table([R"\$0", R"\$1000", R"\$1500", R"\$2500"],
                                               [(R"f", blank), (R"x\,f", blank)],
                                               w=1.35, h=0.62, x_name=R"\mathrm{total}\ x")
        table.move_to([-2.4, -1.0, 0])
        combos = [("no, no", GREY_B), ("yes, no", ACCENT), ("no, yes", CALM), ("yes, yes", MEAN_COLOR)]
        tags = VGroup(*[note(t, 20, c).next_to(cells[(0, k)], UP, buff=0.1) for k, (t, c) in enumerate(combos)])
        self.play(FadeIn(heads[0]), *[ShowCreation(cells[(0, c)]) for c in range(4)])
        for c in range(4):
            self.play(FadeIn(tags[c]), FadeIn(texts[(0, c)]), run_time=0.45)
        self.wait(0.6)

        # ── 2. 확률: 독립이라 곱
        self.play(focus(1))
        self.play(FadeIn(heads[1]), *[ShowCreation(cells[(1, c)]) for c in range(4)])
        prods = column([
            R"f(\$0) = (1 - 0.7)(1 - 0.4) = (0.3)(0.6) = 0.18",
            R"f(\$1000) = (0.7)(1 - 0.4) = (0.7)(0.6) = 0.42",
            R"f(\$1500) = (1 - 0.7)(0.4) = (0.3)(0.4) = 0.12",
            R"f(\$2500) = (0.7)(0.4) = 0.28",
        ], steps_box, scale=0.58, gap=0.4).align_to([0.75, 0, 0], LEFT)
        vals = ["0.18", "0.42", "0.12", "0.28"]
        for c in range(4):
            hl = highlight(cells[(0, c)], ACCENT, 0.3)
            t = Tex(vals[c]).scale(0.7).set_color(INK).move_to(cells[(1, c)])
            self.play(FadeIn(hl), Write(prods[c]), run_time=0.9)
            self.play(FadeIn(t), FadeOut(hl), run_time=0.35)
        chk = Tex(R"0.18 + 0.42 + 0.12 + 0.28 = 1").scale(0.55).set_color(GREY_B)
        chk.next_to(prods, DOWN, buff=0.25).align_to(prods, LEFT)
        self.play(FadeIn(chk))
        self.wait(0.8)

        # ── 3. 값 × 확률을 더한다
        self.play(focus(2), FadeOut(prods), FadeOut(chk))
        self.play(FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        xf = ["0", "420", "180", "700"]
        for c in range(4):
            hx, hf = highlight(cells[(0, c)], ACCENT, 0.3), highlight(cells[(1, c)], ACCENT, 0.3)
            t = Tex(xf[c]).scale(0.7).set_color(MEAN_COLOR).move_to(cells[(2, c)])
            self.play(FadeIn(hx), FadeIn(hf), run_time=0.3)
            self.play(FadeIn(t), FadeOut(hx), FadeOut(hf), run_time=0.45)
        ans = column([
            R"E(X) = 0(0.18) + 1000(0.42) + 1500(0.12) + 2500(0.28)",
            R"= 0 + 420 + 180 + 700 = \$1300",
        ], steps_box, scale=0.52, gap=0.45).align_to([0.75, 0, 0], LEFT)
        ans[1].set_color(MEAN_COLOR)
        self.play(Write(ans[0]), run_time=1.2)
        self.play(Write(ans[1]))
        self.play(FlashAround(ans[1], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 예제 4.3 전자 기기의 수명 — 슬라이드 8 뒤 (9 앞)
# ─────────────────────────────────────────────────────────────
class Example43DeviceLife(InteractiveScene):
    """f(x) = 20000/x³ (x > 100). 단계 넷: 적분 세우기 → 피적분함수 정리(x · 20000/x³ = 20000/x²) → 원시함수 −20000/x
    → 위끝(∞ 에서 0)·아래끝 대입 → 200 시간. 곡선 아래 넓이 위에 받침점을 200 에 세운다."""

    def construct(self):
        head = slide_title("Example 4.3")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((100, 400, 100), (0, 0.025, 0.01), width=5.2, height=2.6).move_to([-3.4, -0.7, 0])
        g = axes.get_graph(lambda x: 20000 / x ** 3, x_range=(100, 400)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, 100, 400, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [100, 200, 300, 400])
        f_tag = Tex(R"f(x) = \tfrac{20000}{x^3},\ x > 100").scale(0.62).set_color(ACCENT).next_to(axes, UP, buff=0.15)
        unit = note("life in hours", 22, GREY_B).next_to(axes, DOWN, buff=0.55).align_to(axes, LEFT)
        self.play(ShowCreation(axes), FadeIn(marks), FadeIn(unit))
        self.play(ShowCreation(g), FadeIn(area), FadeIn(f_tag))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. write the integral", "2. simplify the integrand",
                                               "3. antiderivative", "4. limits, then subtract"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        col = column([
            R"E(X) = \int_{100}^{\infty} x\cdot\frac{20000}{x^3}\,dx",
            R"= \int_{100}^{\infty} \frac{20000}{x^2}\,dx",
            R"= \Big[-\frac{20000}{x}\Big]_{100}^{\infty}",
            R"= 0 - \Big(-\frac{20000}{100}\Big) = 200",
        ], steps_box, scale=0.62, gap=0.45, buff=0.28).align_to([0.75, 0, 0], LEFT)
        col[3].set_color(MEAN_COLOR)

        self.play(focus(0), Write(col[0]), run_time=1.2)
        self.wait(0.8)
        self.play(focus(1), Write(col[1]))
        self.wait(0.8)
        self.play(focus(2), Write(col[2]))
        self.wait(0.8)
        self.play(focus(3))
        inf = note("at infinity the bracket is 0", 22, GREY_B).next_to(col[2], RIGHT, buff=0.35)
        self.play(FadeIn(inf))
        self.play(Write(col[3]), run_time=1.0)
        ful = fulcrum_at(axes.c2p(200, 0))
        bal = label("200 hours, balance point", 24, MEAN_COLOR).next_to(ful, DOWN, buff=0.5)
        self.play(FadeIn(ful), FadeIn(bal), FlashAround(col[3], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. g(X) 의 기댓값 = 같은 확률, 새 값 — 슬라이드 10 (정리 4.1) 앞
# ─────────────────────────────────────────────────────────────
class ExpectationOfFunction(InteractiveScene):
    """예제 4.1 의 표를 다시 쓴다. f(x) 줄은 그대로 두고 값 줄만 g(x) = x² 로 바꾼다. E(X²) = Σ x² f(x) = 24/7.
    g(X) 의 분포를 새로 구할 필요가 없다. 연속형은 합이 적분."""

    def construct(self):
        head = slide_title("Expected Value of g(X)")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"E[g(X)]").scale(0.9).set_color(MEAN_COLOR).next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.8)
        self.play(Write(name))

        fs = [R"\tfrac{1}{35}", R"\tfrac{12}{35}", R"\tfrac{18}{35}", R"\tfrac{4}{35}"]
        blank = [R"\ "] * 4
        table, cells, texts, heads = pmf_table([0, 1, 2, 3], [(R"f(x)", fs), (R"g(x) = x^2", blank),
                                                              (R"g(x)\,f(x)", blank)], w=1.25, h=0.62)
        table.move_to([-2.9, 0.1, 0])
        src = note("Example 4.1", 22, GREY_B).next_to(table, UP, buff=0.35).align_to(cells[(0, 0)], LEFT)
        self.play(FadeIn(src), FadeIn(heads[0]), FadeIn(heads[1]),
                  *[ShowCreation(cells[(r, c)]) for r in range(2) for c in range(4)],
                  *[FadeIn(texts[(r, c)]) for r in range(2) for c in range(4)])
        self.wait(0.6)

        # 같은 확률
        hl_f = VGroup(*[highlight(cells[(1, c)], ACCENT, 0.3) for c in range(4)])
        same = label("same probabilities", 26, ACCENT).next_to(table, DOWN, buff=0.4).align_to(cells[(0, 0)], LEFT)
        self.play(FadeIn(hl_f), FadeIn(same))
        self.wait(0.8)
        self.play(FadeOut(hl_f))

        # 새 값 g(x)
        self.play(FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        new = label("new values g(x)", 26, CALM).next_to(same, DOWN, buff=0.15).align_to(same, LEFT)
        self.play(FadeIn(new))
        for x in range(4):
            t = Tex(str(x * x)).scale(0.7).set_color(CALM).move_to(cells[(2, x)])
            self.play(FadeIn(t), run_time=0.35)
        self.wait(0.5)

        # 곱하고 더한다: 이산형은 합
        d_tag = label("discrete: sum", 24, ACCENT).next_to(name, DOWN, buff=0.5).align_to([0.9, 0, 0], LEFT)
        col = column([
            R"E[g(X)] = \sum_x g(x)\,f(x)",
            R"E(X^2) = 0\cdot\tfrac{1}{35} + 1\cdot\tfrac{12}{35} + 4\cdot\tfrac{18}{35} + 9\cdot\tfrac{4}{35}",
            R"= \tfrac{0 + 12 + 72 + 36}{35} = \tfrac{120}{35} = \tfrac{24}{7}",
        ], d_tag, scale=0.58, gap=0.25).align_to(d_tag, LEFT)
        col[0].set_color(ACCENT)
        self.play(FadeIn(d_tag), Write(col[0]))
        self.play(FadeIn(heads[3]), *[ShowCreation(cells[(3, c)]) for c in range(4)])
        gf = ["0", R"\tfrac{12}{35}", R"\tfrac{72}{35}", R"\tfrac{36}{35}"]
        for x in range(4):
            hg, hf = highlight(cells[(2, x)], CALM, 0.3), highlight(cells[(1, x)], ACCENT, 0.3)
            t = Tex(gf[x]).scale(0.7).set_color(MEAN_COLOR).move_to(cells[(3, x)])
            self.play(FadeIn(hg), FadeIn(hf), run_time=0.25)
            self.play(FadeIn(t), FadeOut(hg), FadeOut(hf), run_time=0.4)
        self.play(Write(col[1]), run_time=1.2)
        self.play(Write(col[2]))
        self.play(FlashAround(col[2], color=MEAN_COLOR, buff=0.1))
        self.wait(0.8)
        nod = label("no new distribution needed", 24, MEAN_COLOR).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        self.play(FadeIn(nod))
        self.wait(1.0)

        # 연속형은 적분
        c_tag = label("continuous: integral", 24, CALM).next_to(nod, DOWN, buff=0.45).align_to(col, LEFT)
        cint = Tex(R"E[g(X)] = \int_{-\infty}^{\infty} g(x)\,f(x)\,dx").scale(0.62).set_color(CALM)
        cint.next_to(c_tag, DOWN, buff=0.2).align_to(col, LEFT)
        self.play(FadeIn(c_tag), Write(cint))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 예제 4.4 세차장 — 슬라이드 11 뒤 (12 앞)
# ─────────────────────────────────────────────────────────────
class Example44CarWash(InteractiveScene):
    """x = 4…9, f = 1/12, 1/12, 1/4, 1/4, 1/6, 1/6. g(x) = 2x − 1. 단계 셋: g(x) 줄 → g(x) f(x) 줄 → 더하기.
    합은 12분의 몇으로 통분해 152/12 = 38/3 ≈ 12.67 달러."""

    def construct(self):
        head = slide_title("Example 4.4")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        gdef = Tex(R"g(X) = 2X - 1").scale(0.85).set_color(CALM).move_to([-4.4, 2.15, 0])
        gbox = panel(gdef, MUTED, buff=0.2)
        ask = note("cars X, earnings g(X) dollars", 22, GREY_B).next_to(gbox, DOWN, buff=0.15)
        self.play(FadeIn(gbox), FadeIn(gdef), FadeIn(ask))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. compute g(x) = 2x - 1", "2. multiply by f(x)", "3. add"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        fs = [R"\tfrac{1}{12}", R"\tfrac{1}{12}", R"\tfrac{1}{4}", R"\tfrac{1}{4}", R"\tfrac{1}{6}", R"\tfrac{1}{6}"]
        blank = [R"\ "] * 6
        table, cells, texts, heads = pmf_table([4, 5, 6, 7, 8, 9], [(R"f(x)", fs), (R"g(x)", blank),
                                                                    (R"g(x)\,f(x)", blank)], w=0.95, h=0.6)
        table.move_to([-2.9, -1.2, 0])
        self.play(FadeIn(heads[0]), FadeIn(heads[1]),
                  *[ShowCreation(cells[(r, c)]) for r in range(2) for c in range(6)],
                  *[FadeIn(texts[(r, c)]) for r in range(2) for c in range(6)])
        self.wait(0.5)

        # ── 1. g(x)
        self.play(focus(0))
        self.play(FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(6)])
        for c, x in enumerate(range(4, 10)):
            hx = highlight(cells[(0, c)], ACCENT, 0.3)
            t = Tex(str(2 * x - 1)).scale(0.7).set_color(CALM).move_to(cells[(2, c)])
            self.play(FadeIn(hx), run_time=0.2)
            self.play(FadeIn(t), FadeOut(hx), run_time=0.35)
        ex = Tex(R"x = 4:\ 2\cdot4 - 1 = 7").scale(0.6).set_color(GREY_B)
        ex.next_to(steps_box, DOWN, buff=0.4).align_to([0.75, 0, 0], LEFT)
        self.play(FadeIn(ex))
        self.wait(0.6)

        # ── 2. g(x) f(x)
        self.play(focus(1), FadeOut(ex))
        self.play(FadeIn(heads[3]), *[ShowCreation(cells[(3, c)]) for c in range(6)])
        gf = [R"\tfrac{7}{12}", R"\tfrac{9}{12}", R"\tfrac{11}{4}", R"\tfrac{13}{4}", R"\tfrac{15}{6}", R"\tfrac{17}{6}"]
        for c in range(6):
            hg, hf = highlight(cells[(2, c)], CALM, 0.3), highlight(cells[(1, c)], ACCENT, 0.3)
            t = Tex(gf[c]).scale(0.65).set_color(MEAN_COLOR).move_to(cells[(3, c)])
            self.play(FadeIn(hg), FadeIn(hf), run_time=0.2)
            self.play(FadeIn(t), FadeOut(hg), FadeOut(hf), run_time=0.35)
        self.wait(0.5)

        # ── 3. 더한다
        self.play(focus(2))
        ans = column([
            R"E[g(X)] = \sum_{x=4}^{9} (2x - 1)\,f(x)",
            R"= \tfrac{7}{12} + \tfrac{9}{12} + \tfrac{11}{4} + \tfrac{13}{4} + \tfrac{15}{6} + \tfrac{17}{6}",
            R"= \tfrac{7 + 9 + 33 + 39 + 30 + 34}{12} = \tfrac{152}{12}",
            R"= \tfrac{38}{3} \approx 12.67 \quad \$12.67",
        ], steps_box, scale=0.6, gap=0.4).align_to([0.75, 0, 0], LEFT)
        ans[3].set_color(MEAN_COLOR)
        self.play(Write(ans[0]))
        self.play(Write(ans[1]), run_time=1.2)
        tw = note("all over 12", 22, GREY_B).next_to(ans[2], RIGHT, buff=0.35)
        self.play(Write(ans[2]), FadeIn(tw), run_time=1.0)
        self.play(Write(ans[3]))
        self.play(FlashAround(ans[3], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 예제 4.5 E(4X + 3) — 슬라이드 13 뒤 (14 앞)
# ─────────────────────────────────────────────────────────────
class Example45FourXPlus3(InteractiveScene):
    """f(x) = x²/3 (−1 < x < 2). 단계 넷: 적분 세우기 → 피적분함수 전개 (4x³ + 3x²)/3 → 원시함수 [x⁴ + x³]/3
    → 대입 (16 + 8) − (1 − 1) = 24, 답 8."""

    def construct(self):
        head = slide_title("Example 4.5")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((-1, 2, 1), (0, 1.4, 1), width=5.2, height=2.6).move_to([-3.4, -0.7, 0])
        g = axes.get_graph(lambda x: x * x / 3, x_range=(-1, 2)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, -1, 2, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [-1, 0, 1, 2])
        f_tag = Tex(R"f(x) = \tfrac{x^2}{3},\ -1 < x < 2").scale(0.62).set_color(ACCENT).next_to(axes, UP, buff=0.15)
        g_tag = Tex(R"g(X) = 4X + 3").scale(0.7).set_color(CALM).next_to(axes, DOWN, buff=0.55).align_to(axes, LEFT)
        self.play(ShowCreation(axes), FadeIn(marks))
        self.play(ShowCreation(g), FadeIn(area), FadeIn(f_tag), FadeIn(g_tag))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. write the integral", "2. expand the integrand",
                                               "3. antiderivative", "4. limits, then subtract"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        col = column([
            R"E(4X + 3) = \int_{-1}^{2} (4x + 3)\cdot\frac{x^2}{3}\,dx",
            R"= \frac{1}{3}\int_{-1}^{2} (4x^3 + 3x^2)\,dx",
            R"= \frac{1}{3}\Big[x^4 + x^3\Big]_{-1}^{2}",
            R"= \frac{1}{3}\big[(16 + 8) - (1 - 1)\big] = \frac{1}{3}\cdot 24 = 8",
        ], steps_box, scale=0.62, gap=0.45, buff=0.28).align_to([0.75, 0, 0], LEFT)
        col[3].set_color(MEAN_COLOR)

        self.play(focus(0), Write(col[0]), run_time=1.2)
        self.wait(0.8)
        self.play(focus(1), Write(col[1]))
        self.wait(0.8)
        self.play(focus(2), Write(col[2]))
        self.wait(0.8)
        self.play(focus(3), Write(col[3]), run_time=1.2)
        self.play(FlashAround(col[3], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 예제 4.6 표 3.1 에서 E(XY) — 슬라이드 16 뒤 (17 앞)
# ─────────────────────────────────────────────────────────────
class Example46TableXY(InteractiveScene):
    """표 3.1 (행 y, 열 x). 단계 셋: 이중합 쓰기 → x = 0 열과 y = 0 행은 곱이 0 이라 사라짐 → 남은 네 칸만 곱해 더하기.
    f(1,1) = 6/28 만 살아남아 3/14."""

    def construct(self):
        head = slide_title("Example 4.6")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells, texts, heads = grid_table(TABLE31, ["0", "1", "2"], ["0", "1", "2"], w=1.2, h=0.8)
        table.move_to([-3.4, -0.6, 0])
        src = note("Table 3.1", 22, GREY_B).next_to(table, DOWN, buff=0.45).align_to(table, LEFT)
        gdef = Tex(R"g(X, Y) = XY").scale(0.8).set_color(CALM).move_to([-3.4, 2.15, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads), FadeIn(src), FadeIn(gdef))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. write the double sum", "2. cells with x=0, y=0 vanish",
                                               "3. multiply the rest"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 이중합
        s1 = Tex(R"E(XY) = \sum_{x=0}^{2}\sum_{y=0}^{2} x\,y\,f(x, y)").scale(0.68).set_color(INK)
        s1.next_to(steps_box, DOWN, buff=0.45).align_to([0.75, 0, 0], LEFT)
        self.play(focus(0), Write(s1), run_time=1.2)
        self.wait(0.8)

        # ── 2. x = 0 열, y = 0 행은 사라진다
        self.play(focus(1))
        gone = [(i, j) for i in range(3) for j in range(3) if i == 0 or j == 0]
        shade = VGroup(*[cells[k].copy().set_fill(GREY_D, 0.85).set_stroke(GREY_C, 1.5) for k in gone])
        zero = Tex(R"x\,y = 0").scale(0.7).set_color(GREY_B).next_to(s1, DOWN, buff=0.3).align_to(s1, LEFT)
        self.play(FadeIn(shade), *[texts[k].animate.set_color(GREY_C) for k in gone], Write(zero), run_time=1.0)
        self.wait(0.8)

        # ── 3. 남은 네 칸
        self.play(focus(2), FadeOut(zero))
        keep = [(1, 1), (1, 2), (2, 1), (2, 2)]
        hls = VGroup(*[highlight(cells[k], MEAN_COLOR, 0.35) for k in keep])
        self.play(FadeIn(hls))
        col = column([
            R"= 1\cdot1\,f(1,1) + 2\cdot1\,f(2,1) + 1\cdot2\,f(1,2) + 2\cdot2\,f(2,2)",
            R"= 1\cdot1\cdot\tfrac{6}{28} + 2\cdot1\cdot 0 + 1\cdot2\cdot 0 + 2\cdot2\cdot 0",
            R"= \tfrac{6}{28} = \tfrac{3}{14}",
        ], s1, scale=0.58, gap=0.35, buff=0.28).align_to(s1, LEFT)
        col[2].set_color(MEAN_COLOR)
        self.play(Write(col[0]), run_time=1.2)
        self.wait(0.5)
        self.play(Write(col[1]), run_time=1.2)
        self.wait(0.4)
        only = highlight(cells[(1, 1)], MEAN_COLOR, 0.55)
        self.play(FadeOut(hls), FadeIn(only), Write(col[2]))
        self.play(FlashAround(col[2], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 예제 4.7 E(Y/X) — 슬라이드 18 뒤 (19 앞)
# ─────────────────────────────────────────────────────────────
class Example47RatioYX(InteractiveScene):
    """f(x, y) = x(1 + 3y²)/4 (0<x<2, 0<y<1). 단계 넷: 이중적분 세우기 → y/x 의 x 와 f 의 x 가 약분 → 안쪽 dx
    (y(1+3y²)/4 · [x]₀² = y(1+3y²)/2) → 바깥 dy ((1/2)[y²/2 + 3y⁴/4]₀¹ = 5/8). 그림은 직사각형 정의역 위 가로 띠 → 띠 쌓기."""

    def construct(self):
        head = slide_title("Example 4.7")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 그림: 직사각형 정의역, 농도 = 높이
        W, H = 3.6, 1.8
        x0, y0 = -6.2, -2.3
        rect = Rectangle(width=W, height=H).set_stroke(GREY_B, 2).move_to([x0 + W / 2, y0 + H / 2, 0])
        n = 8
        cells = VGroup()
        for i in range(n):
            for j in range(2 * n):
                x, y = 2 * (j + 0.5) / (2 * n), (i + 0.5) / n
                v = x * (1 + 3 * y * y) / 4 / 2.0
                c = Rectangle(width=W / (2 * n), height=H / n).set_stroke(width=0).set_fill(ACCENT, 0.12 + 0.6 * v)
                c.move_to([x0 + (j + 0.5) * W / (2 * n), y0 + (i + 0.5) * H / n, 0])
                cells.add(c)
        xl = VGroup(Tex("0").scale(0.6), Tex("2").scale(0.6)).set_color(GREY_B)
        xl[0].next_to(rect.get_corner(DL), DOWN, buff=0.12)
        xl[1].next_to(rect.get_corner(DR), DOWN, buff=0.12)
        yl = Tex("1").scale(0.6).set_color(GREY_B).next_to(rect.get_corner(UL), LEFT, buff=0.12)
        xt = Tex("x").scale(0.7).set_color(GREY_B).next_to(rect, DOWN, buff=0.35)
        yt = Tex("y").scale(0.7).set_color(GREY_B).next_to(rect, LEFT, buff=0.35)
        f_tag = Tex(R"f(x, y) = \frac{x(1 + 3y^2)}{4}").scale(0.7).set_color(CALM).next_to(rect, UP, buff=0.3)
        gdef = Tex(R"g(X, Y) = \frac{Y}{X}").scale(0.7).set_color(MEAN_COLOR).next_to(f_tag, UP, buff=0.25)
        self.play(ShowCreation(rect), FadeIn(cells), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(f_tag), FadeIn(gdef))
        self.wait(0.5)

        steps, steps_box, focus = steps_panel(["1. write the double integral", "2. cancel x",
                                               "3. inner integral, dx", "4. outer integral, dy"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        col = column([
            R"E\Big(\tfrac{Y}{X}\Big) = \int_0^1\int_0^2 \tfrac{y}{x}\cdot\tfrac{x(1 + 3y^2)}{4}\,dx\,dy",
            R"= \int_0^1\int_0^2 \tfrac{y(1 + 3y^2)}{4}\,dx\,dy",
            R"\mathrm{inner:}\ \tfrac{y(1 + 3y^2)}{4}\big[x\big]_{x=0}^{x=2} = \tfrac{y(1 + 3y^2)}{2}",
            R"\mathrm{outer:}\ \int_0^1 \tfrac{y + 3y^3}{2}\,dy = \tfrac{1}{2}\Big[\tfrac{y^2}{2} + \tfrac{3y^4}{4}\Big]_0^1",
            R"= \tfrac{1}{2}\Big(\tfrac{1}{2} + \tfrac{3}{4}\Big) = \tfrac{1}{2}\cdot\tfrac{5}{4} = \tfrac{5}{8}",
        ], steps_box, scale=0.57, gap=0.45, buff=0.24).align_to([0.75, 0, 0], LEFT)
        col[4].set_color(MEAN_COLOR)

        self.play(focus(0), Write(col[0]), run_time=1.3)
        self.wait(0.8)
        self.play(focus(1))
        self.play(FlashAround(col[0], color=WARN, buff=0.08), run_time=0.8)
        self.play(Write(col[1]), run_time=1.0)
        self.wait(0.8)

        # 안쪽: y 를 고정한 가로 띠
        strip = Rectangle(width=W, height=H / n).set_stroke(MEAN_COLOR, 2).set_fill(MEAN_COLOR, 0.45)
        strip.move_to([x0 + W / 2, y0 + H * 0.45, 0])
        s_tag = note("fix y, integrate along x", 22, MEAN_COLOR).next_to(rect, DOWN, buff=0.65)
        self.play(focus(2), FadeIn(strip), FadeOut(xt), FadeIn(s_tag))
        self.play(Write(col[2]), run_time=1.2)
        self.wait(1.0)

        # 바깥: 띠를 y 방향으로 쌓는다
        strips = VGroup(*[Rectangle(width=W, height=H / n).set_stroke(width=0).set_fill(MEAN_COLOR, 0.3)
                          .move_to([x0 + W / 2, y0 + (i + 0.5) * H / n, 0]) for i in range(n)])
        s_tag2 = note("then add the strips in y", 22, MEAN_COLOR).move_to(s_tag)
        self.play(focus(3), FadeOut(s_tag), FadeIn(s_tag2), FadeOut(strip),
                  LaggedStartMap(FadeIn, strips, lag_ratio=0.12), run_time=1.2)
        self.play(Write(col[3]), run_time=1.2)
        self.wait(0.6)
        self.play(Write(col[4]), run_time=1.0)
        self.play(FlashAround(col[4], color=MEAN_COLOR, buff=0.12), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 분산 = 평균에서 떨어진 정도 — 슬라이드 20 (정의 4.3 · 정리 4.2) 앞
# ─────────────────────────────────────────────────────────────
class VarianceAsSpread(InteractiveScene):
    """이름을 먼저 건다: variance σ² = E[(X−μ)²]. 앞: 예제 4.8 의 두 회사(그림 4.1). 평균은 둘 다 2 인데 퍼짐이 다르다.
    가운데: 편차 x−μ 를 화살표로, 제곱해서 확률로 가중. 이산(합)·연속(적분). 뒤: 정리 4.2 의 지름길을 한 줄씩 유도한다."""

    def construct(self):
        head = slide_title("Variance")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\sigma^2 = E[(X - \mu)^2]").scale(0.85).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.8)

        # ── 1. 같은 평균, 다른 퍼짐
        lineA = NumberLine(x_range=(0, 4, 1), width=4.6, include_numbers=True).move_to([-3.6, -0.4, 0])
        lineB = NumberLine(x_range=(0, 4, 1), width=4.6, include_numbers=True).move_to([2.6, -0.4, 0])
        barsA, tagsA = pmf_bars(lineA, [1, 2, 3], [0.3, 0.4, 0.3], 0.4)
        barsB, tagsB = pmf_bars(lineB, [0, 1, 2, 3, 4], [0.2, 0.1, 0.3, 0.3, 0.1], 0.4, color=CALM)
        tA = note("company A", 22, ACCENT).next_to(lineA, UP, buff=2.35)
        tB = note("company B", 22, CALM).next_to(lineB, UP, buff=2.35)
        src = note("Example 4.8, Figure 4.1", 22, GREY_B).move_to([0, -1.6, 0])
        self.play(ShowCreation(lineA), ShowCreation(lineB), FadeIn(tA), FadeIn(tB), FadeIn(src))
        self.play(LaggedStartMap(GrowFromEdge, barsA, edge=DOWN, lag_ratio=0.15), FadeIn(tagsA),
                  LaggedStartMap(GrowFromEdge, barsB, edge=DOWN, lag_ratio=0.15), FadeIn(tagsB), run_time=1.2)
        fulA, fulB = fulcrum_at(lineA.n2p(2)), fulcrum_at(lineB.n2p(2))
        muA = Tex(R"\mu = 2").scale(0.6).set_color(MEAN_COLOR).next_to(fulA, DOWN, buff=0.35)
        muB = Tex(R"\mu = 2").scale(0.6).set_color(MEAN_COLOR).next_to(fulB, DOWN, buff=0.35)
        self.play(FadeIn(fulA), FadeIn(fulB), FadeIn(muA), FadeIn(muB))
        same = label("same mean, different spread", 28, MEAN_COLOR).move_to([0, -2.6, 0])
        self.play(FadeIn(same))
        self.wait(1.2)

        # ── 2. 편차 → 제곱 → 확률로 가중
        self.play(FadeOut(VGroup(lineA, barsA, tagsA, tA, fulA, muA, src, same)),
                  FadeOut(muB))
        grpB = VGroup(lineB, barsB, tagsB, tB, fulB)
        self.play(grpB.animate.shift(LEFT * 6.2), Write(name))
        arrows = VGroup()
        for x in [0, 1, 3, 4]:
            a = Arrow(lineB.n2p(2) + DOWN * 0.55, lineB.n2p(x) + DOWN * 0.55, buff=0.05, stroke_width=3).set_color(WARN)
            arrows.add(a)
        dev = label("deviation from the mean", 24, WARN).next_to(lineB, DOWN, buff=1.0)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.2), FadeIn(dev))
        self.wait(0.5)
        sq = Tex(R"(x - \mu)^2").scale(0.75).set_color(WARN).next_to(dev, DOWN, buff=0.2)
        wt = label("weight by f(x)", 24, GREY_B).next_to(sq, DOWN, buff=0.2)
        self.play(FadeIn(sq))
        self.play(FadeIn(wt))
        col = column([
            R"\sigma^2 = \sum_x (x - \mu)^2 f(x)",
            R"\sigma^2 = \int_{-\infty}^{\infty} (x - \mu)^2 f(x)\,dx",
        ], name, scale=0.7, gap=0.9, buff=0.75).align_to([0.9, 0, 0], LEFT)
        d_tag = label("discrete: sum", 24, ACCENT).next_to(col[0], UP, buff=0.12).align_to(col, LEFT)
        c_tag = label("continuous: integral", 24, CALM).next_to(col[1], UP, buff=0.12).align_to(col, LEFT)
        col[0].set_color(ACCENT)
        col[1].set_color(CALM)
        self.play(FadeIn(d_tag), Write(col[0]))
        self.wait(0.4)
        self.play(FadeIn(c_tag), Write(col[1]))
        self.wait(1.2)

        # ── 3. 지름길 (정리 4.2) — 한 줄씩
        self.play(FadeOut(VGroup(grpB, arrows, dev, sq, wt, col, d_tag, c_tag)))
        sc = label("shortcut", 26, MEAN_COLOR).next_to(head[1], DOWN, buff=0.4).align_to([-6.0, 0, 0], LEFT)
        der = column([
            R"\sigma^2 = E[(X - \mu)^2]",
            R"= E[X^2 - 2\mu X + \mu^2]",
            R"= E(X^2) - 2\mu\,E(X) + \mu^2",
            R"= E(X^2) - 2\mu\cdot\mu + \mu^2",
            R"= E(X^2) - 2\mu^2 + \mu^2",
            R"= E(X^2) - \mu^2",
        ], sc, scale=0.75, gap=0.35, buff=0.28).align_to([-6.0, 0, 0], LEFT)
        der[5].set_color(MEAN_COLOR)
        hints = [None, "expand the square", "E is linear", "E(X) is the mean", None, None]
        self.play(Write(der[0]))
        for k in range(1, 6):
            self.play(Write(der[k]), run_time=0.9)
            if hints[k]:
                h = note(hints[k], 22, GREY_B).next_to(der[k], RIGHT, buff=0.5)
                self.play(FadeIn(h), run_time=0.3)
                self.wait(0.4)
        self.play(FlashAround(der[5], color=MEAN_COLOR, buff=0.12))
        sd = Tex(R"\sigma = \sqrt{\sigma^2}").scale(0.85).set_color(INK).move_to([3.6, -1.6, 0])
        sd_tag = label("standard deviation", 26, INK).next_to(sd, DOWN, buff=0.2)
        self.play(Write(sd), FadeIn(sd_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 예제 4.8 두 회사의 분산 — 슬라이드 24 뒤 (25 앞)
# ─────────────────────────────────────────────────────────────
class Example48TwoCompanies(InteractiveScene):
    """회사 A(1·2·3), B(0…4). 단계 셋: 각각의 평균 → 편차의 제곱 → f(x) 로 가중해 더한다. 0.6 < 1.6."""

    def construct(self):
        head = slide_title("Example 4.8")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        steps, steps_box, focus = steps_panel(["1. mean of each", "2. deviations, squared", "3. weight by f(x), add"],
                                              pos=(3.6, 2.15, 0))
        blankA, blankB = [R"\ "] * 3, [R"\ "] * 5
        tabA, cA, tA, hA = pmf_table([1, 2, 3], [(R"f(x)", ["0.3", "0.4", "0.3"]), (R"(x-\mu)^2", blankA),
                                                  (R"(x-\mu)^2 f(x)", blankA)], w=0.85, h=0.52, scale=0.62)
        tabB, cB, tB, hB = pmf_table([0, 1, 2, 3, 4], [(R"f(x)", ["0.2", "0.1", "0.3", "0.3", "0.1"]),
                                                        (R"(x-\mu)^2", blankB), (R"(x-\mu)^2 f(x)", blankB)],
                                     w=0.85, h=0.52, scale=0.62)
        tidy_heads(cA, hA)
        tidy_heads(cB, hB)
        tabA.move_to([-3.3, 1.35, 0]).align_to([-6.7, 0, 0], LEFT)
        tabB.move_to([-3.3, -1.75, 0]).align_to([-6.7, 0, 0], LEFT)
        filled = VGroup()
        nA = note("company A", 22, ACCENT).next_to(tabA, UP, buff=0.15).align_to(tabA, LEFT)
        nB = note("company B", 22, CALM).next_to(tabB, UP, buff=0.15).align_to(tabB, LEFT)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.play(FadeIn(nA), FadeIn(nB),
                  *[FadeIn(m) for tab, cells, texts, heads in ((tabA, cA, tA, hA), (tabB, cB, tB, hB))
                    for m in (heads[0], heads[1], *[cells[(r, c)] for (r, c) in cells if r < 2],
                              *[texts[(r, c)] for (r, c) in texts if r < 2])])
        self.wait(0.6)

        # ── 1. 평균
        self.play(focus(0))
        col = column([
            R"\mu_A = 1(0.3) + 2(0.4) + 3(0.3) = 2.0",
            R"\mu_B = 0(0.2) + 1(0.1) + 2(0.3) + 3(0.3) + 4(0.1) = 2.0",
        ], steps_box, scale=0.55, gap=0.4, buff=0.2).align_to([0.6, 0, 0], LEFT)
        self.play(Write(col[0]))
        self.play(Write(col[1]), run_time=1.1)
        self.wait(0.6)

        # ── 2. 편차의 제곱
        self.play(focus(1), FadeIn(hA[2]), FadeIn(hB[2]),
                  *[ShowCreation(cA[(2, c)]) for c in range(3)], *[ShowCreation(cB[(2, c)]) for c in range(5)])
        for c, x in enumerate([1, 2, 3]):
            filled.add(cell_tex(cA, (2, c), str((x - 2) ** 2), WARN, 0.62))
            self.play(FadeIn(filled[-1]), run_time=0.3)
        for c, x in enumerate([0, 1, 2, 3, 4]):
            filled.add(cell_tex(cB, (2, c), str((x - 2) ** 2), WARN, 0.62))
            self.play(FadeIn(filled[-1]), run_time=0.3)
        self.wait(0.5)

        # ── 3. 가중해서 더한다
        self.play(focus(2), FadeIn(hA[3]), FadeIn(hB[3]),
                  *[ShowCreation(cA[(3, c)]) for c in range(3)], *[ShowCreation(cB[(3, c)]) for c in range(5)])
        for c, v in enumerate(["0.3", "0", "0.3"]):
            filled.add(cell_tex(cA, (3, c), v, MEAN_COLOR, 0.62))
            self.play(FadeIn(filled[-1]), run_time=0.3)
        ans = column([
            R"\sigma_A^2 = (1-2)^2(0.3) + (2-2)^2(0.4) + (3-2)^2(0.3)",
            R"= 0.3 + 0 + 0.3 = 0.6",
            R"\sigma_B^2 = (0-2)^2(0.2) + (1-2)^2(0.1) + (2-2)^2(0.3)",
            R"\quad + (3-2)^2(0.3) + (4-2)^2(0.1)",
            R"= 0.8 + 0.1 + 0 + 0.3 + 0.4 = 1.6",
        ], col, scale=0.55, gap=0.4, buff=0.2).align_to([0.6, 0, 0], LEFT)
        ans[1].set_color(MEAN_COLOR)
        ans[4].set_color(MEAN_COLOR)
        self.play(Write(ans[0]), run_time=1.0)
        self.play(Write(ans[1]))
        self.wait(0.4)
        for c, v in enumerate(["0.8", "0.1", "0", "0.3", "0.4"]):
            filled.add(cell_tex(cB, (3, c), v, MEAN_COLOR, 0.62))
            self.play(FadeIn(filled[-1]), run_time=0.3)
        self.play(Write(ans[2]), run_time=1.0)
        self.play(Write(ans[3]))
        self.play(Write(ans[4]))
        self.wait(0.6)

        # 결론: 작은 막대 둘
        self.play(FadeOut(VGroup(tabA, tabB, nA, nB, filled)))
        lineA = NumberLine(x_range=(0, 4, 1), width=2.8, include_numbers=True).move_to([-4.6, -1.6, 0])
        lineB = NumberLine(x_range=(0, 4, 1), width=2.8, include_numbers=True).move_to([-1.4, -1.6, 0])
        bA, gA = pmf_bars(lineA, [1, 2, 3], [0.3, 0.4, 0.3], 0.4, width=0.35, height=1.6)
        bB, gB = pmf_bars(lineB, [0, 1, 2, 3, 4], [0.2, 0.1, 0.3, 0.3, 0.1], 0.4, color=CALM, width=0.35, height=1.6)
        vA = Tex(R"\sigma_A^2 = 0.6").scale(0.65).set_color(ACCENT).next_to(lineA, DOWN, buff=0.45)
        vB = Tex(R"\sigma_B^2 = 1.6").scale(0.65).set_color(CALM).next_to(lineB, DOWN, buff=0.45)
        self.play(ShowCreation(lineA), ShowCreation(lineB))
        self.play(LaggedStartMap(GrowFromEdge, bA, edge=DOWN, lag_ratio=0.1), LaggedStartMap(GrowFromEdge, bB, edge=DOWN, lag_ratio=0.1),
                  FadeIn(vA), FadeIn(vB), run_time=1.0)
        gt = Tex(R"\sigma_B^2 > \sigma_A^2").scale(0.9).set_color(MEAN_COLOR).move_to([-3.0, 1.4, 0])
        self.play(Write(gt))
        self.play(FlashAround(gt, color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 예제 4.9 불량 부품 수의 분산 (정리 4.2) — 슬라이드 26 뒤 (27 앞)
# ─────────────────────────────────────────────────────────────
class Example49Defectives(InteractiveScene):
    """x = 0…3, f = 0.51·0.38·0.10·0.01. 지름길: μ → E(X²) → σ² = E(X²) − μ². 표에 x f(x), x² f(x) 줄을 채운다."""

    def construct(self):
        head = slide_title("Example 4.9")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        steps, steps_box, focus = steps_panel(["1. mean μ", "2. E(X²)", "3. σ² = E(X²) − μ²"], pos=(3.9, 2.15, 0))
        blank = [R"\ "] * 4
        tab, cells, texts, heads = pmf_table([0, 1, 2, 3], [(R"f(x)", ["0.51", "0.38", "0.10", "0.01"]),
                                                            (R"x\,f(x)", blank), (R"x^2 f(x)", blank)], w=1.15, h=0.6)
        tidy_heads(cells, heads)
        tab.move_to([-3.1, 0.3, 0])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.play(FadeIn(heads[0]), FadeIn(heads[1]),
                  *[FadeIn(cells[(r, c)]) for (r, c) in cells if r < 2], *[FadeIn(texts[(r, c)]) for (r, c) in texts if r < 2])
        self.wait(0.6)

        # ── 1. μ
        self.play(focus(0), FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        for c, v in enumerate(["0", "0.38", "0.20", "0.03"]):
            hx, hf = highlight(cells[(0, c)], ACCENT, 0.3), highlight(cells[(1, c)], ACCENT, 0.3)
            self.play(FadeIn(hx), FadeIn(hf), run_time=0.25)
            self.play(FadeIn(cell_tex(cells, (2, c), v, MEAN_COLOR)), FadeOut(hx), FadeOut(hf), run_time=0.4)
        col = column([
            R"\mu = 0(0.51) + 1(0.38) + 2(0.10) + 3(0.01)",
            R"= 0 + 0.38 + 0.20 + 0.03 = 0.61",
        ], steps_box, scale=0.58, gap=0.45, buff=0.2).align_to([0.75, 0, 0], LEFT)
        self.play(Write(col[0]), run_time=1.0)
        self.play(Write(col[1]))
        self.wait(0.6)

        # ── 2. E(X²)
        self.play(focus(1), FadeIn(heads[3]), *[ShowCreation(cells[(3, c)]) for c in range(4)])
        for c, v in enumerate(["0", "0.38", "0.40", "0.09"]):
            hx, hf = highlight(cells[(0, c)], CALM, 0.3), highlight(cells[(1, c)], CALM, 0.3)
            self.play(FadeIn(hx), FadeIn(hf), run_time=0.25)
            self.play(FadeIn(cell_tex(cells, (3, c), v, CALM)), FadeOut(hx), FadeOut(hf), run_time=0.4)
        col2 = column([
            R"E(X^2) = 0^2(0.51) + 1^2(0.38) + 2^2(0.10) + 3^2(0.01)",
            R"= 0 + 0.38 + 0.40 + 0.09 = 0.87",
        ], col, scale=0.58, gap=0.4, buff=0.2).align_to([0.75, 0, 0], LEFT)
        self.play(Write(col2[0]), run_time=1.0)
        self.play(Write(col2[1]))
        self.wait(0.6)

        # ── 3. σ²
        self.play(focus(2))
        ans = column([
            R"\sigma^2 = E(X^2) - \mu^2 = 0.87 - (0.61)^2",
            R"= 0.87 - 0.3721 = 0.4979",
        ], col2, scale=0.58, gap=0.4, buff=0.2).align_to([0.75, 0, 0], LEFT)
        ans[1].set_color(MEAN_COLOR)
        self.play(Write(ans[0]), run_time=1.0)
        self.play(Write(ans[1]))
        self.play(FlashAround(ans[1], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13. 예제 4.10 물 수요의 평균과 분산 (연속) — 슬라이드 28 뒤 (29 앞)
# ─────────────────────────────────────────────────────────────
class Example410WaterDemand(InteractiveScene):
    """f(x) = 2(x−1), 1<x<2. 삼각형 밀도. μ = 5/3, E(X²) = 17/6, σ² = 1/18. 적분은 원시함수·대입까지 줄마다."""

    def construct(self):
        head = slide_title("Example 4.10")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((0.6, 2.2, 1), (0, 2.3, 1), width=4.2, height=2.4).move_to([-4.2, 0.9, 0])
        g = axes.get_graph(lambda x: 2 * (x - 1), x_range=(1, 2)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, 1, 2, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [1, 2])
        f_tag = Tex(R"f(x) = 2(x - 1),\ 1 < x < 2").scale(0.6).set_color(ACCENT).next_to(axes, UP, buff=0.05)
        self.play(ShowCreation(axes), FadeIn(marks), FadeIn(f_tag))
        self.play(ShowCreation(g), FadeIn(area))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. mean μ", "2. E(X²)", "3. σ² = E(X²) − μ²"], pos=(4.2, 2.45, 0), size=22, buff=0.14)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. μ
        self.play(focus(0))
        A = column([
            R"\mu = \int_1^2 x\cdot 2(x - 1)\,dx = \int_1^2 (2x^2 - 2x)\,dx",
            R"= \Big[\tfrac{2x^3}{3} - x^2\Big]_1^2 = \Big(\tfrac{16}{3} - 4\Big) - \Big(\tfrac{2}{3} - 1\Big)",
            R"= \tfrac{4}{3} + \tfrac{1}{3} = \tfrac{5}{3}",
        ], steps_box, scale=0.52, gap=0.25, buff=0.12).align_to([0.35, 0, 0], LEFT)
        self.play(Write(A[0]), run_time=1.1)
        self.play(Write(A[1]), run_time=1.1)
        self.play(Write(A[2]))
        ful = fulcrum_at(axes.c2p(5 / 3, 0))
        mu_tag = Tex(R"\mu = \tfrac{5}{3}").scale(0.6).set_color(MEAN_COLOR).next_to(ful, DOWN, buff=0.1)
        self.play(FadeIn(ful), FadeIn(mu_tag))
        self.wait(1.2)

        # ── 2. E(X²)
        self.play(focus(1))
        B = column([
            R"E(X^2) = \int_1^2 x^2\cdot 2(x - 1)\,dx = \int_1^2 (2x^3 - 2x^2)\,dx",
            R"= \Big[\tfrac{x^4}{2} - \tfrac{2x^3}{3}\Big]_1^2 = \Big(8 - \tfrac{16}{3}\Big) - \Big(\tfrac{1}{2} - \tfrac{2}{3}\Big)",
            R"= \tfrac{8}{3} + \tfrac{1}{6} = \tfrac{17}{6}",
        ], A, scale=0.52, gap=0.3, buff=0.12).align_to([0.35, 0, 0], LEFT)
        self.play(Write(B[0]), run_time=1.1)
        self.play(Write(B[1]), run_time=1.1)
        self.play(Write(B[2]))
        self.wait(0.8)

        # ── 3. σ²
        self.play(focus(2))
        C = column([
            R"\sigma^2 = E(X^2) - \mu^2 = \tfrac{17}{6} - \Big(\tfrac{5}{3}\Big)^2 = \tfrac{17}{6} - \tfrac{25}{9}",
            R"= \tfrac{51}{18} - \tfrac{50}{18} = \tfrac{1}{18}",
        ], B, scale=0.52, gap=0.3, buff=0.12).align_to([0.35, 0, 0], LEFT)
        C[1].set_color(MEAN_COLOR)
        self.play(Write(C[0]), run_time=1.1)
        self.wait(0.6)
        self.play(Write(C[1]))
        self.play(FlashAround(C[1], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 14. 예제 4.11 2X+3 의 분산 (이산) — 슬라이드 30 뒤 (31 앞)
# ─────────────────────────────────────────────────────────────
class Example411LinearDiscrete(InteractiveScene):
    """x = 0…3, f = 1/4·1/8·1/2·1/8, g(X) = 2X+3. 표에 2x+3 · (2x+3)f(x) 줄로 μ = 6, (2x+3−6)² · 그 가중 줄로 σ² = 4."""

    def construct(self):
        head = slide_title("Example 4.11")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        steps, steps_box, focus = steps_panel(["1. mean of 2X + 3", "2. deviations from 6, squared", "3. weight by f(x), add"],
                                              pos=(3.5, 2.15, 0))
        blank = [R"\ "] * 4
        tab, cells, texts, heads = pmf_table(
            [0, 1, 2, 3],
            [(R"f(x)", [R"\tfrac14", R"\tfrac18", R"\tfrac12", R"\tfrac18"]),
             (R"2x+3", blank), (R"(2x+3)f(x)", blank),
             (R"(2x+3-6)^2", blank), (R"(2x+3-6)^2 f(x)", blank)], w=1.05, h=0.56, scale=0.62)
        tidy_heads(cells, heads)
        tab.move_to([-2.4, -0.2, 0])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.play(FadeIn(heads[0]), FadeIn(heads[1]),
                  *[FadeIn(cells[(r, c)]) for (r, c) in cells if r < 2], *[FadeIn(texts[(r, c)]) for (r, c) in texts if r < 2])
        self.wait(0.6)

        # ── 1. 평균
        self.play(focus(0), FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        for c, v in enumerate(["3", "5", "7", "9"]):
            self.play(FadeIn(cell_tex(cells, (2, c), v, ACCENT, 0.62)), run_time=0.3)
        self.play(FadeIn(heads[3]), *[ShowCreation(cells[(3, c)]) for c in range(4)])
        for c, v in enumerate([R"\tfrac34", R"\tfrac58", R"\tfrac72", R"\tfrac98"]):
            self.play(FadeIn(cell_tex(cells, (3, c), v, MEAN_COLOR, 0.62)), run_time=0.3)
        col = column([
            R"\mu_{2X+3} = E(2X + 3) = \sum_{x=0}^{3} (2x + 3) f(x)",
            R"= \tfrac{3}{4} + \tfrac{5}{8} + \tfrac{7}{2} + \tfrac{9}{8} = \tfrac{6 + 5 + 28 + 9}{8} = \tfrac{48}{8} = 6",
        ], steps_box, scale=0.55, gap=0.4, buff=0.2).align_to([0.6, 0, 0], LEFT)
        self.play(Write(col[0]), run_time=1.0)
        self.wait(0.5)
        self.play(Write(col[1]), run_time=1.2)
        self.wait(1.0)

        # ── 2. 편차의 제곱
        self.play(focus(1), FadeIn(heads[4]), *[ShowCreation(cells[(4, c)]) for c in range(4)])
        for c, v in enumerate(["9", "1", "1", "9"]):
            self.play(FadeIn(cell_tex(cells, (4, c), v, WARN, 0.62)), run_time=0.3)
        self.wait(0.5)

        # ── 3. 가중해 더한다
        self.play(focus(2), FadeIn(heads[5]), *[ShowCreation(cells[(5, c)]) for c in range(4)])
        for c, v in enumerate([R"\tfrac94", R"\tfrac18", R"\tfrac12", R"\tfrac98"]):
            self.play(FadeIn(cell_tex(cells, (5, c), v, MEAN_COLOR, 0.62)), run_time=0.3)
        ans = column([
            R"\sigma^2_{2X+3} = E[(2X + 3 - 6)^2] = \sum_{x=0}^{3} (2x - 3)^2 f(x)",
            R"= \tfrac{9}{4} + \tfrac{1}{8} + \tfrac{1}{2} + \tfrac{9}{8} = \tfrac{18 + 1 + 4 + 9}{8} = \tfrac{32}{8} = 4",
        ], col, scale=0.55, gap=0.45, buff=0.2).align_to([0.6, 0, 0], LEFT)
        ans[1].set_color(MEAN_COLOR)
        self.play(Write(ans[0]), run_time=1.0)
        self.wait(0.6)
        self.play(Write(ans[1]), run_time=1.2)
        self.play(FlashAround(ans[1], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 15. 예제 4.12 4X+3 의 분산 (연속) — 슬라이드 32 뒤 (33 앞)
# ─────────────────────────────────────────────────────────────
class Example412LinearContinuous(InteractiveScene):
    """f(x) = x²/3 (−1<x<2), g(X) = 4X+3, 예제 4.5 에서 μ = 8. σ² = E[(4X−5)²] 를 전개·원시함수·대입까지 줄마다. 51/5."""

    def construct(self):
        head = slide_title("Example 4.12")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((-1.3, 2.3, 1), (0, 1.5, 1), width=4.2, height=2.2).move_to([-4.3, 1.0, 0])
        g = axes.get_graph(lambda x: x * x / 3, x_range=(-1, 2)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, -1, 2, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [-1, 0, 1, 2])
        f_tag = Tex(R"f(x) = \tfrac{x^2}{3},\ -1 < x < 2").scale(0.6).set_color(ACCENT).next_to(axes, UP, buff=0.05)
        given = Tex(R"\mu_{4X+3} = 8").scale(0.7).set_color(MEAN_COLOR).next_to(axes, DOWN, buff=0.5)
        src = note("from Example 4.5", 22, GREY_B).next_to(given, DOWN, buff=0.15)
        self.play(ShowCreation(axes), FadeIn(marks), FadeIn(f_tag))
        self.play(ShowCreation(g), FadeIn(area))
        self.play(FadeIn(given), FadeIn(src))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. deviation (4X + 3) - 8", "2. write the integral",
                                               "3. expand, antiderivative", "4. limits, then subtract"], pos=(3.6, 2.2, 0), size=22, buff=0.16)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        L = column([
            R"g(X) - \mu_{g(X)} = (4X + 3) - 8 = 4X - 5",
            R"\sigma^2_{4X+3} = E[(4X - 5)^2] = \int_{-1}^{2} (4x - 5)^2\,\tfrac{x^2}{3}\,dx",
            R"= \tfrac{1}{3}\int_{-1}^{2} (16x^4 - 40x^3 + 25x^2)\,dx",
            R"= \tfrac{1}{3}\Big[\tfrac{16x^5}{5} - 10x^4 + \tfrac{25x^3}{3}\Big]_{-1}^{2}",
            R"= \tfrac{1}{3}\Big[\Big(\tfrac{512}{5} - 160 + \tfrac{200}{3}\Big) - \Big(-\tfrac{16}{5} - 10 - \tfrac{25}{3}\Big)\Big]",
            R"= \tfrac{1}{3}\Big[\tfrac{528}{5} - 150 + 75\Big] = \tfrac{1}{3}\cdot\tfrac{153}{5} = \tfrac{51}{5} = 10.2",
        ], steps_box, scale=0.55, gap=0.35, buff=0.18).align_to([0.35, 0, 0], LEFT)
        L[5].set_color(MEAN_COLOR)
        self.play(focus(0), Write(L[0]), run_time=1.0)
        self.wait(1.0)
        self.play(focus(1), Write(L[1]), run_time=1.2)
        self.wait(1.0)
        self.play(focus(2), Write(L[2]), run_time=1.0)
        self.wait(0.6)
        self.play(Write(L[3]), run_time=1.0)
        self.wait(1.0)
        self.play(focus(3), Write(L[4]), run_time=1.3)
        self.wait(0.8)
        self.play(Write(L[5]), run_time=1.2)
        self.play(FlashAround(L[5], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C1. 공분산 — 부호는 같이 움직이는 방향 — 슬라이드 22 (정의 4.4 · 정리 4.4) 앞
# ─────────────────────────────────────────────────────────────
class CovarianceSign(InteractiveScene):
    """점 몇 개를 평균선 둘로 네 칸으로 가른다. 오른쪽 위·왼쪽 아래 칸은 곱이 양수, 나머지는 음수.
    같이 오르는 점들이면 양수가 많아 σ_XY > 0, 반대면 < 0. 정의(이중 합·이중 적분) 뒤 정리 4.4 를 네 줄로 유도."""

    def construct(self):
        head = slide_title("Covariance")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\sigma_{XY}").scale(0.9).set_color(MEAN_COLOR).next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.8)
        self.play(Write(name))

        axes = Axes(x_range=(0, 6, 1), y_range=(0, 6, 1), width=4.4, height=3.6,
                    axis_config=dict(include_ticks=False, stroke_width=2, stroke_color=GREY_B))
        axes.move_to([-4.2, -0.9, 0])
        mx, my = 3.0, 3.2
        vline = dashed(axes.c2p(mx, 0), axes.c2p(mx, 6))
        hline = dashed(axes.c2p(0, my), axes.c2p(6, my))
        mx_tag = Tex(R"\mu_X").scale(0.6).set_color(GREY_B).next_to(axes.c2p(mx, 0), DOWN, buff=0.1)
        my_tag = Tex(R"\mu_Y").scale(0.6).set_color(GREY_B).next_to(axes.c2p(0, my), LEFT, buff=0.1)
        self.play(ShowCreation(axes), ShowCreation(vline), ShowCreation(hline), FadeIn(mx_tag), FadeIn(my_tag))

        # 네 칸: 오른쪽 위·왼쪽 아래는 곱이 양수(CALM), 나머지는 음수(WARN)
        def quad(x0, x1, y0, y1, color):
            r = Polygon(axes.c2p(x0, y0), axes.c2p(x1, y0), axes.c2p(x1, y1), axes.c2p(x0, y1))
            return r.set_stroke(width=0).set_fill(color, 0.12)
        quads = VGroup(quad(mx, 6, my, 6, CALM), quad(0, mx, 0, my, CALM),
                       quad(0, mx, my, 6, WARN), quad(mx, 6, 0, my, WARN))
        plus = VGroup(Tex("+").set_color(CALM).move_to(axes.c2p(4.6, 5.3)), Tex("+").set_color(CALM).move_to(axes.c2p(1.2, 0.9)))
        minus = VGroup(Tex("-").set_color(WARN).move_to(axes.c2p(1.2, 5.3)), Tex("-").set_color(WARN).move_to(axes.c2p(4.6, 0.9)))
        prod = Tex(R"(x - \mu_X)(y - \mu_Y)").scale(0.6).set_color(INK).next_to(axes, UP, buff=0.15)
        self.play(FadeIn(quads), FadeIn(plus), FadeIn(minus), FadeIn(prod))
        self.wait(0.5)

        pos_pts = [(1, 1.4), (2, 2.3), (3, 3.0), (4, 4.1), (5, 5.2)]
        neg_pts = [(1, 5.1), (2, 4.2), (3, 3.3), (4, 2.1), (5, 1.3)]
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.09).set_color(ACCENT) for x, y in pos_pts])
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.15, scale=0.5))
        pos_tag = label("positive: move together", 24, CALM).next_to(axes, DOWN, buff=0.45)
        sign = Tex(R"\sigma_{XY} > 0").scale(0.7).set_color(CALM).next_to(pos_tag, DOWN, buff=0.12)
        self.play(FadeIn(pos_tag), FadeIn(sign))
        self.wait(0.8)

        # 정의: 이산·연속
        col = column([
            R"\sigma_{XY} = E[(X - \mu_X)(Y - \mu_Y)]",
            R"= \sum_x \sum_y (x - \mu_X)(y - \mu_Y)\,f(x, y)",
            R"= \int_{-\infty}^{\infty}\int_{-\infty}^{\infty} (x - \mu_X)(y - \mu_Y)\,f(x, y)\,dx\,dy",
        ], name, scale=0.55, gap=0.4).align_to([0.2, 0, 0], LEFT)
        col[0].set_color(MEAN_COLOR)
        d_tag = note("discrete: double sum", 22, ACCENT).next_to(col[1], DOWN, buff=0.08).align_to(col, LEFT)
        c_tag = note("continuous: double integral", 22, CALM).next_to(col[2], DOWN, buff=0.08).align_to(col, LEFT)
        self.play(Write(col[0]))
        self.play(Write(col[1]), FadeIn(d_tag))
        self.play(Write(col[2]), FadeIn(c_tag))
        self.wait(0.8)

        # 반대로 움직이는 점들
        new_dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.09).set_color(WARN) for x, y in neg_pts])
        neg_tag = label("negative: move opposite", 24, WARN).move_to(pos_tag)
        sign2 = Tex(R"\sigma_{XY} < 0").scale(0.7).set_color(WARN).move_to(sign)
        self.play(FadeOut(dots), FadeOut(pos_tag), FadeOut(sign))
        self.play(LaggedStartMap(FadeIn, new_dots, lag_ratio=0.15, scale=0.5), FadeIn(neg_tag), FadeIn(sign2))
        self.wait(0.8)

        # 정리 4.4 유도
        self.play(FadeOut(col[1]), FadeOut(col[2]), FadeOut(d_tag), FadeOut(c_tag))
        der = column([
            R"= E[XY - \mu_Y X - \mu_X Y + \mu_X \mu_Y]",
            R"= E(XY) - \mu_Y E(X) - \mu_X E(Y) + \mu_X \mu_Y",
            R"= E(XY) - \mu_Y \mu_X - \mu_X \mu_Y + \mu_X \mu_Y",
            R"\sigma_{XY} = E(XY) - \mu_X \mu_Y",
        ], col[0], scale=0.55, gap=0.3).align_to(col[0], LEFT)
        der[3].set_color(MEAN_COLOR)
        short = note("shortcut, Theorem 4.4", 22, GREY_B).next_to(der[3], DOWN, buff=0.12).align_to(der, LEFT)
        for k in range(3):
            self.play(Write(der[k]))
            self.wait(0.3)
        self.play(Write(der[3]), FadeIn(short))
        self.play(FlashAround(der[3], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C2. 상관계수 — 단위를 없앤 공분산 — 슬라이드 23 (정의 4.5) 앞
# ─────────────────────────────────────────────────────────────
class CorrelationScale(InteractiveScene):
    """X 를 cm 에서 m 로 바꾸면 σ_XY 도 σ_X 도 1/100 이 된다. 둘의 비 ρ 는 그대로. −1 ≤ ρ ≤ 1, ρ = 0 은 직선 관계가 없다는 뜻."""

    def construct(self):
        head = slide_title("Correlation Coefficient")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\rho_{XY}").scale(0.9).set_color(MEAN_COLOR).next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.8)
        self.play(Write(name))

        # 단위가 바뀌면 공분산도 바뀐다
        unit = label("same data, X in cm", 26, INK).move_to([-3.6, 1.6, 0])
        cm = column([R"\sigma_{XY} = 250", R"\sigma_X = 20,\quad \sigma_Y = 25"], unit, scale=0.7, gap=0.35).align_to(unit, LEFT)
        self.play(FadeIn(unit), Write(cm[0]), Write(cm[1]))
        self.wait(0.6)
        unit2 = label("X in m", 26, ACCENT).move_to([2.6, 1.6, 0])
        m = column([R"\sigma_{XY} = 2.5", R"\sigma_X = 0.2,\quad \sigma_Y = 25"], unit2, scale=0.7, gap=0.35).align_to(unit2, LEFT)
        arrow = Arrow(cm.get_right() + RIGHT * 0.2, m.get_left() + LEFT * 0.2, buff=0.1, stroke_width=3).set_color(ACCENT)
        scale_tag = Tex(R"\times \tfrac{1}{100}").scale(0.7).set_color(ACCENT).next_to(arrow, UP, buff=0.1)
        self.play(FadeIn(unit2), GrowArrow(arrow), FadeIn(scale_tag))
        self.play(Write(m[0]), Write(m[1]))
        dep = label("covariance depends on units", 24, WARN).next_to(cm, DOWN, buff=0.5).align_to(cm, LEFT)
        self.play(FadeIn(dep))
        self.wait(0.8)

        # 둘 다 표준편차로 나누면 단위가 사라진다
        rho = Tex(R"\rho_{XY} = \frac{\sigma_{XY}}{\sigma_X\,\sigma_Y}").scale(0.95).set_color(MEAN_COLOR).move_to([-3.6, -1.6, 0])
        div = label("divide by both spreads", 24, GREY_B).next_to(rho, DOWN, buff=0.25).align_to(rho, LEFT)
        self.play(Write(rho), FadeIn(div))
        chk = column([
            R"\mathrm{cm:}\ \tfrac{250}{20 \cdot 25} = \tfrac{250}{500} = 0.5",
            R"\mathrm{m:}\ \tfrac{2.5}{0.2 \cdot 25} = \tfrac{2.5}{5} = 0.5",
        ], m, scale=0.65, gap=0.55).align_to(m, LEFT)
        chk.shift(DOWN * 0.3)
        self.play(Write(chk[0]))
        self.play(Write(chk[1]))
        same = label("no units, same value", 24, CALM).next_to(chk, DOWN, buff=0.25).align_to(chk, LEFT)
        self.play(FadeIn(same))
        self.wait(0.8)

        # 범위와 0 의 뜻
        rng = Tex(R"-1 \le \rho_{XY} \le 1").scale(0.85).set_color(INK).next_to(div, DOWN, buff=0.45).align_to(rho, LEFT)
        zero = label("ρ = 0: no linear relation", 24, GREY_B).next_to(rng, DOWN, buff=0.2).align_to(rho, LEFT)
        self.play(Write(rng))
        self.play(FadeIn(zero))
        self.play(FlashAround(rho, color=MEAN_COLOR, buff=0.15))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C3. 예제 4.13 표 3.1 의 공분산 — 슬라이드 34 뒤 (35 앞)
# ─────────────────────────────────────────────────────────────
def table31_with_margins(pos, w=1.0, h=0.62):
    """표 3.1 과 열 합 g(x)·행 합 h(y) 자리. 돌려주는 것: (표, cells, texts, heads, g 값들, h 값들)."""
    table, cells, texts, heads = grid_table(TABLE31, ["0", "1", "2"], ["0", "1", "2"], w=w, h=h)
    table.move_to(pos)
    g_vals = VGroup(*[Tex(t).scale(0.7).set_color(ACCENT).move_to(cells[(2, j)].get_center() + DOWN * h)
                      for j, t in enumerate([R"\tfrac{5}{14}", R"\tfrac{15}{28}", R"\tfrac{3}{28}"])])
    h_vals = VGroup(*[Tex(t).scale(0.7).set_color(WARN).move_to(cells[(i, 2)].get_center() + RIGHT * w)
                      for i, t in enumerate([R"\tfrac{15}{28}", R"\tfrac{3}{7}", R"\tfrac{1}{28}"])])
    g_tag = Tex("g(x)").scale(0.65).set_color(ACCENT).next_to(g_vals, LEFT, buff=0.35)
    h_tag = Tex("h(y)").scale(0.65).set_color(WARN).next_to(h_vals, UP, buff=0.25)
    return table, cells, texts, heads, g_vals, h_vals, g_tag, h_tag


class Example413Covariance(InteractiveScene):
    """표 3.1(파랑 X, 빨강 Y). 단계 넷: E(XY) 는 예제 4.6 의 한 칸 → g(x) 로 μ_X → h(y) 로 μ_Y → 정리 4.4 로 −9/56."""

    def construct(self):
        head = slide_title("Example 4.13")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells, texts, heads, g_vals, h_vals, g_tag, h_tag = table31_with_margins([-4.3, 0.4, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads))
        xy = Tex(R"X = \mathrm{blue},\quad Y = \mathrm{red}", t2c={R"\mathrm{blue}": ACCENT, R"\mathrm{red}": WARN}).scale(0.65)
        xy.next_to(table, UP, buff=0.5)
        self.play(FadeIn(xy))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. E(XY) from Example 4.6", "2. mean of X from g(x)",
                                               "3. mean of Y from h(y)", "4. E(XY) minus the product"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. E(XY): xy ≠ 0 인 칸 가운데 f ≠ 0 은 (1,1) 뿐
        self.play(focus(0))
        hl = highlight(cells[(1, 1)])
        l1 = column([
            R"E(XY) = \sum_x\sum_y xy\,f(x, y) = (1)(1)\,f(1, 1) = \tfrac{6}{28} = \tfrac{3}{14}",
        ], steps_box, scale=0.55, gap=0.45).align_to([0.3, 0, 0], LEFT)
        zero_tag = note("other cells: xy f = 0", 20, GREY_B).next_to(l1, DOWN, buff=0.08).align_to(l1, LEFT)
        self.play(FadeIn(hl), Write(l1[0]), FadeIn(zero_tag))
        self.wait(0.8)
        self.play(FadeOut(hl), FadeOut(zero_tag))

        # ── 2. 열을 아래로 더해 g(x), μ_X
        self.play(focus(1))
        cols = VGroup(*[highlight(cells[(i, j)], ACCENT, 0.25) for j in range(3) for i in range(3)])
        self.play(FadeIn(cols), FadeIn(g_tag), LaggedStartMap(FadeIn, g_vals, lag_ratio=0.2))
        l2 = column([
            R"\mu_X = 0\cdot\tfrac{5}{14} + 1\cdot\tfrac{15}{28} + 2\cdot\tfrac{3}{28} = \tfrac{15 + 6}{28} = \tfrac{21}{28} = \tfrac{3}{4}",
        ], l1, scale=0.55, gap=0.3).align_to(l1, LEFT)
        self.play(Write(l2[0]), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(cols))

        # ── 3. 행을 옆으로 더해 h(y), μ_Y
        self.play(focus(2))
        rows = VGroup(*[highlight(cells[(i, j)], WARN, 0.25) for i in range(3) for j in range(3)])
        self.play(FadeIn(rows), FadeIn(h_tag), LaggedStartMap(FadeIn, h_vals, lag_ratio=0.2))
        l3 = column([
            R"\mu_Y = 0\cdot\tfrac{15}{28} + 1\cdot\tfrac{3}{7} + 2\cdot\tfrac{1}{28} = \tfrac{12 + 2}{28} = \tfrac{14}{28} = \tfrac{1}{2}",
        ], l2, scale=0.55, gap=0.3).align_to(l1, LEFT)
        self.play(Write(l3[0]), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(rows))

        # ── 4. 정리 4.4
        self.play(focus(3))
        l4 = column([
            R"\sigma_{XY} = E(XY) - \mu_X\mu_Y = \tfrac{3}{14} - \tfrac{3}{4}\cdot\tfrac{1}{2} = \tfrac{3}{14} - \tfrac{3}{8}",
            R"= \tfrac{12}{56} - \tfrac{21}{56} = -\tfrac{9}{56}",
        ], l3, scale=0.55, gap=0.3).align_to(l1, LEFT)
        l4[1].set_color(MEAN_COLOR)
        self.play(Write(l4[0]))
        self.play(Write(l4[1]))
        why = label("negative: more blue, fewer red", 24, MEAN_COLOR).next_to(table, DOWN, buff=1.0).align_to(table, LEFT)
        self.play(FlashAround(l4[1], color=MEAN_COLOR, buff=0.12), FadeIn(why))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C4. 예제 4.15 상관계수 — 슬라이드 36 뒤 (37 앞)
# ─────────────────────────────────────────────────────────────
class Example415Correlation(InteractiveScene):
    """예제 4.13 의 σ_XY = −9/56 에 σ_X, σ_Y 를 붙인다. E(X²)·E(Y²) → 분산 둘(정리 4.2) → 나누어 −1/√5."""

    def construct(self):
        head = slide_title("Example 4.15")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells, texts, heads, g_vals, h_vals, g_tag, h_tag = table31_with_margins([-4.3, 0.4, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads), FadeIn(g_vals), FadeIn(h_vals), FadeIn(g_tag), FadeIn(h_tag))
        given = Tex(R"\mu_X = \tfrac{3}{4},\quad \mu_Y = \tfrac{1}{2},\quad \sigma_{XY} = -\tfrac{9}{56}").scale(0.62).set_color(GREY_B)
        given.next_to(table, UP, buff=0.5)
        src = note("from Example 4.13", 20, GREY_B).next_to(given, UP, buff=0.08).align_to(given, LEFT)
        self.play(FadeIn(given), FadeIn(src))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. E(X²) and E(Y²)", "2. the two variances", "3. divide by both spreads"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 제곱의 기댓값
        self.play(focus(0))
        gh = ring(g_vals, ACCENT, 0.08)
        l1 = column([
            R"E(X^2) = 0^2\cdot\tfrac{5}{14} + 1^2\cdot\tfrac{15}{28} + 2^2\cdot\tfrac{3}{28} = \tfrac{15 + 12}{28} = \tfrac{27}{28}",
            R"E(Y^2) = 0^2\cdot\tfrac{15}{28} + 1^2\cdot\tfrac{3}{7} + 2^2\cdot\tfrac{1}{28} = \tfrac{12 + 4}{28} = \tfrac{4}{7}",
        ], steps_box, scale=0.52, gap=0.45).align_to([0.3, 0, 0], LEFT)
        self.play(FadeIn(gh), Write(l1[0]))
        self.play(FadeOut(gh))
        hh = ring(h_vals, WARN, 0.08)
        self.play(FadeIn(hh), Write(l1[1]))
        self.play(FadeOut(hh))
        self.wait(0.6)

        # ── 2. 분산 둘 (정리 4.2)
        self.play(focus(1))
        l2 = column([
            R"\sigma_X^2 = E(X^2) - \mu_X^2 = \tfrac{27}{28} - \big(\tfrac{3}{4}\big)^2 = \tfrac{108}{112} - \tfrac{63}{112} = \tfrac{45}{112}",
            R"\sigma_Y^2 = E(Y^2) - \mu_Y^2 = \tfrac{4}{7} - \big(\tfrac{1}{2}\big)^2 = \tfrac{16}{28} - \tfrac{7}{28} = \tfrac{9}{28}",
        ], l1, scale=0.52, gap=0.35).align_to(l1, LEFT)
        self.play(Write(l2[0]))
        self.play(Write(l2[1]))
        self.wait(0.6)

        # ── 3. 나눈다
        self.play(focus(2), FadeOut(l1))
        self.play(l2.animate.move_to(l1, aligned_edge=UL))
        l3 = column([
            R"\rho_{XY} = \frac{\sigma_{XY}}{\sigma_X\sigma_Y} = \frac{-9/56}{\sqrt{(45/112)(9/28)}} = \frac{-9/56}{\sqrt{405/3136}}",
            R"= \frac{-9/56}{\sqrt{405}/56} = \frac{-9}{\sqrt{405}} = \frac{-9}{9\sqrt{5}} = -\frac{1}{\sqrt{5}} \approx -0.447",
        ], l2, scale=0.52, gap=0.35).align_to(l1, LEFT)
        l3[1].set_color(MEAN_COLOR)
        self.play(Write(l3[0]), run_time=1.2)
        self.play(Write(l3[1]), run_time=1.2)
        why = label("no units, between −1 and 1", 24, MEAN_COLOR).next_to(table, DOWN, buff=1.0).align_to(table, LEFT)
        self.play(FlashAround(l3[1], color=MEAN_COLOR, buff=0.12), FadeIn(why))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C5. 선형결합의 평균 — 슬라이드 40 (정리 4.5 · 4.6) 앞
# ─────────────────────────────────────────────────────────────
class LinearShiftScale(InteractiveScene):
    """예제 4.11 의 분포(0·1·2·3, 1/4·1/8·1/2·1/8, μ = 1.5). +3 옮기면 균형점도 3 만큼, 2배 늘리면 균형점도 2배.
    E(aX+b) = aμ + b 를 정의에서 두 줄로. 합은 갈라진다: E[g ± h] = E[g] ± E[h]."""
    probs = [(1, 4), (1, 8), (1, 2), (1, 8)]

    def make_bars(self, line, xs, color):
        bars = VGroup()
        for x, (n, d) in zip(xs, self.probs):
            b = bar(n / d, 0.5, width=0.45, height=2.0, color=color)
            b.move_to(line.n2p(x), aligned_edge=DOWN).shift(UP * 0.02)
            bars.add(b)
        return bars

    def construct(self):
        head = slide_title("Linear Combinations")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        line = NumberLine(x_range=(0, 8, 1), width=7.0, include_numbers=True).move_to([-2.9, -0.5, 0])
        src = note("Example 4.11 distribution", 22, GREY_B).next_to(line, DOWN, buff=1.35).align_to(line, LEFT)
        bars = self.make_bars(line, [0, 1, 2, 3], ACCENT)
        ful = fulcrum_at(line.n2p(1.5))
        mu = Tex(R"\mu = 1.5").scale(0.7).set_color(MEAN_COLOR).next_to(line.n2p(1.5), DOWN, buff=0.8)
        self.play(ShowCreation(line), FadeIn(src))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.12), FadeIn(ful), FadeIn(mu))
        self.wait(0.6)

        # 옮기기: X + 3
        shift_tag = label("shift: mean moves by b", 24, CALM).move_to([3.6, 2.0, 0])
        e1 = Tex(R"E(X + 3) = 1.5 + 3 = 4.5").scale(0.7).set_color(CALM).next_to(shift_tag, DOWN, buff=0.2)
        self.play(FadeIn(shift_tag))
        self.play(bars.animate.shift(line.n2p(3) - line.n2p(0)), ful.animate.next_to(line.n2p(4.5), DOWN, buff=0.02),
                  Transform(mu, Tex(R"\mu = 4.5").scale(0.7).set_color(MEAN_COLOR).next_to(line.n2p(4.5), DOWN, buff=0.8)),
                  run_time=1.4)
        self.play(Write(e1))
        self.wait(0.8)

        # 되돌리고 늘리기: 2X
        self.play(bars.animate.shift(line.n2p(0) - line.n2p(3)), ful.animate.next_to(line.n2p(1.5), DOWN, buff=0.02),
                  Transform(mu, Tex(R"\mu = 1.5").scale(0.7).set_color(MEAN_COLOR).next_to(line.n2p(1.5), DOWN, buff=0.8)),
                  run_time=0.8)
        scale_tag = label("scale: mean times a", 24, WARN).next_to(e1, DOWN, buff=0.4).align_to(shift_tag, LEFT)
        e2 = Tex(R"E(2X) = 2 \cdot 1.5 = 3").scale(0.7).set_color(WARN).next_to(scale_tag, DOWN, buff=0.2)
        self.play(FadeIn(scale_tag))
        moves = [b.animate.move_to(line.n2p(2 * x), aligned_edge=DOWN).shift(UP * 0.02) for b, x in zip(bars, [0, 1, 2, 3])]
        self.play(*moves, ful.animate.next_to(line.n2p(3), DOWN, buff=0.02),
                  Transform(mu, Tex(R"\mu = 3").scale(0.7).set_color(MEAN_COLOR).next_to(line.n2p(3), DOWN, buff=0.8)),
                  run_time=1.4)
        self.play(Write(e2))
        self.wait(0.8)

        # 정리 4.5 를 정의에서
        thm = column([
            R"E(aX + b) = \sum_x (ax + b)\,f(x)",
            R"= a\sum_x x\,f(x) + b\sum_x f(x)",
            R"= a\mu + b\cdot 1 = a\mu + b",
        ], e2, scale=0.6, gap=0.45).align_to(shift_tag, LEFT)
        thm[2].set_color(MEAN_COLOR)
        self.play(Write(thm[0]))
        self.play(Write(thm[1]))
        self.play(Write(thm[2]))
        self.play(FlashAround(thm[2], color=MEAN_COLOR, buff=0.1))
        self.wait(0.6)

        # 합은 갈라진다
        split = Tex(R"E[g(X) \pm h(X)] = E[g(X)] \pm E[h(X)]").scale(0.6).set_color(INK).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        split_tag = label("sums split", 24, GREY_B).next_to(split, RIGHT, buff=0.4)
        self.play(Write(split), FadeIn(split_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C6. 선형결합의 분산 — 슬라이드 42 (정리 4.9) 앞
# ─────────────────────────────────────────────────────────────
class VarianceOfSum(InteractiveScene):
    """σ²_{aX+bY} 의 교차항 2abσ_XY. 독립이면 0. b = −1 이어도 (−1)² = 1 이라 빼기도 더해진다.
    상수는 퍼짐을 바꾸지 않고, a 배는 a² 배."""

    def construct(self):
        head = slide_title("Variance of aX + bY")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        main = Tex(R"\sigma^2_{aX + bY} = a^2\sigma_X^2 + b^2\sigma_Y^2 + 2ab\,\sigma_{XY}",
                   t2c={R"2ab\,\sigma_{XY}": WARN}).scale(0.95).move_to([0, 1.9, 0])
        self.play(Write(main), run_time=1.2)
        brace = Brace(main[R"2ab\,\sigma_{XY}"], DOWN, buff=0.1).set_color(WARN)
        cross = label("the cross term", 24, WARN).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), FadeIn(cross))
        self.wait(0.8)

        # 독립이면 교차항이 0
        ind = label("independent: cross term 0", 24, CALM).move_to([-3.6, 0.2, 0])
        ind_f = column([
            R"\sigma_{XY} = 0 \ \Rightarrow\ \sigma^2_{aX + bY} = a^2\sigma_X^2 + b^2\sigma_Y^2",
        ], ind, scale=0.62, gap=0.25).align_to(ind, LEFT)
        self.play(FadeIn(ind), Write(ind_f[0]))
        self.wait(0.8)

        # 빼기도 더해진다
        trap = label("minus still adds", 24, MEAN_COLOR).next_to(ind_f, DOWN, buff=0.45).align_to(ind, LEFT)
        trap_f = column([
            R"a = 1,\ b = -1:\quad \sigma^2_{X - Y} = 1^2\sigma_X^2 + (-1)^2\sigma_Y^2 = \sigma_X^2 + \sigma_Y^2",
        ], trap, scale=0.62, gap=0.25).align_to(ind, LEFT)
        self.play(FadeIn(trap), Write(trap_f[0]))
        self.play(FlashAround(trap_f[0], color=MEAN_COLOR, buff=0.1))
        self.wait(0.8)

        # 상수와 배수
        sh = label("shift: spread unchanged", 24, GREY_B).next_to(trap_f, DOWN, buff=0.45).align_to(ind, LEFT)
        sh_f = Tex(R"\sigma^2_{X + c} = \sigma_X^2").scale(0.62).set_color(INK).next_to(sh, RIGHT, buff=0.5)
        sc = label("scale: spread times a²", 24, GREY_B).next_to(sh, DOWN, buff=0.3).align_to(ind, LEFT)
        sc_f = Tex(R"\sigma^2_{aX} = a^2\sigma_X^2").scale(0.62).set_color(INK).next_to(sc, RIGHT, buff=0.5)
        self.play(FadeIn(sh), Write(sh_f))
        self.play(FadeIn(sc), Write(sc_f))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C7. 예제 4.17 · 4.18 정리 4.5 로 다시 풀기 — 슬라이드 44 뒤 (45 앞)
# ─────────────────────────────────────────────────────────────
class Example417418Rework(InteractiveScene):
    """4.17: E(2X−1) = 2μ − 1, 예제 4.4 의 μ = 41/6 → 38/3 ≈ 12.67. 4.18: E(4X+3) = 4μ + 3, 예제 4.5 의 μ = 5/4 → 8.
    예제 4.4 · 4.5 와 같은 답을 더 짧게."""

    def construct(self):
        head = slide_title("Example 4.17, 4.18")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        steps, steps_box, focus = steps_panel(["1. pull out 2 and −1", "2. μ from Example 4.4",
                                               "3. pull out 4 and 3", "4. μ from Example 4.5"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. 4.17: 상수를 밖으로
        self.play(focus(0))
        a1 = Tex(R"E(2X - 1) = 2E(X) - 1").scale(0.7).set_color(INK).move_to([-3.9, 2.2, 0])
        self.play(Write(a1))
        self.wait(0.5)

        # ── 2. 예제 4.4 의 μ: 표
        self.play(focus(1))
        xs = [4, 5, 6, 7, 8, 9]
        fs = [R"\tfrac{1}{12}", R"\tfrac{1}{12}", R"\tfrac{1}{4}", R"\tfrac{1}{4}", R"\tfrac{1}{6}", R"\tfrac{1}{6}"]
        xf = [R"\tfrac{4}{12}", R"\tfrac{5}{12}", R"\tfrac{6}{4}", R"\tfrac{7}{4}", R"\tfrac{8}{6}", R"\tfrac{9}{6}"]
        table, cells, texts, heads = pmf_table(xs, [(R"f(x)", fs), (R"x\,f(x)", [R"\ "] * 6)], w=0.85, h=0.58, scale=0.62)
        table.move_to([-3.6, 0.9, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads))
        for c in range(6):
            t = Tex(xf[c]).scale(0.62).set_color(MEAN_COLOR).move_to(cells[(2, c)])
            self.play(FadeIn(t), run_time=0.25)
        m1 = column([
            R"\mu = \sum_x x\,f(x) = \tfrac{4 + 5 + 18 + 21 + 16 + 18}{12} = \tfrac{82}{12} = \tfrac{41}{6}",
            R"\mu_{2X - 1} = 2\cdot\tfrac{41}{6} - 1 = \tfrac{41}{3} - \tfrac{3}{3} = \tfrac{38}{3} \approx 12.67",
        ], table, scale=0.58, gap=0.4).align_to([-6.4, 0, 0], LEFT)
        m1[1].set_color(MEAN_COLOR)
        self.play(Write(m1[0]), run_time=1.0)
        self.play(Write(m1[1]), run_time=1.0)
        same1 = note("same as Example 4.4", 22, GREY_B).next_to(m1[1], DOWN, buff=0.12).align_to(m1, LEFT)
        self.play(FlashAround(m1[1], color=MEAN_COLOR, buff=0.1), FadeIn(same1))
        self.wait(1.0)

        # ── 3. 4.18: 상수를 밖으로
        self.play(focus(2))
        a2 = Tex(R"E(4X + 3) = 4E(X) + 3").scale(0.7).set_color(INK).next_to(steps_box, DOWN, buff=0.5).align_to([0.6, 0, 0], LEFT)
        self.play(Write(a2))
        self.wait(0.5)

        # ── 4. 예제 4.5 의 μ: 적분
        self.play(focus(3))
        m2 = column([
            R"f(x) = \tfrac{x^2}{3},\ -1 < x < 2",
            R"E(X) = \int_{-1}^{2} x\cdot\tfrac{x^2}{3}\,dx = \int_{-1}^{2}\tfrac{x^3}{3}\,dx",
            R"= \Big[\tfrac{x^4}{12}\Big]_{-1}^{2} = \tfrac{16}{12} - \tfrac{1}{12} = \tfrac{15}{12} = \tfrac{5}{4}",
            R"E(4X + 3) = 4\cdot\tfrac{5}{4} + 3 = 5 + 3 = 8",
        ], a2, scale=0.58, gap=0.3).align_to(a2, LEFT)
        m2[3].set_color(MEAN_COLOR)
        for k in range(3):
            self.play(Write(m2[k]), run_time=0.9)
        self.play(Write(m2[3]))
        same2 = note("same as Example 4.5", 22, GREY_B).next_to(m2[3], DOWN, buff=0.12).align_to(m2, LEFT)
        self.play(FlashAround(m2[3], color=MEAN_COLOR, buff=0.1), FadeIn(same2))
        less = label("same answers, less work", 26, MEAN_COLOR).next_to(same1, DOWN, buff=0.35).align_to(m1, LEFT)
        self.play(FadeIn(less))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C8. 예제 4.19 E[(X−1)²] — 슬라이드 48 뒤 (49 앞)
# ─────────────────────────────────────────────────────────────
class Example419ShiftSquare(InteractiveScene):
    """(X−1)² 을 펼쳐 E(X²) − 2E(X) + 1. 표 셋째·넷째 줄에 x f(x), x² f(x). 답 1."""

    def construct(self):
        head = slide_title("Example 4.19")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        fs = [R"\tfrac{1}{3}", R"\tfrac{1}{2}", "0", R"\tfrac{1}{6}"]
        table, cells, texts, heads = pmf_table([0, 1, 2, 3], [(R"f(x)", fs), (R"x\,f(x)", [R"\ "] * 4), (R"x^2 f(x)", [R"\ "] * 4)],
                                               w=1.1, h=0.6)
        table.move_to([-3.6, 0.6, 0])
        ask = Tex(R"Y = (X - 1)^2,\quad E(Y) = ?").scale(0.7).set_color(INK).next_to(table, UP, buff=0.5)
        self.play(ShowCreation(VGroup(*[cells[(r, c)] for r in (0, 1) for c in range(4)])), FadeIn(heads[0]), FadeIn(heads[1]),
                  *[FadeIn(texts[(r, c)]) for r in (0, 1) for c in range(4)], FadeIn(ask))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. expand (X − 1)²", "2. E(X) and E(X²)", "3. combine"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. 펼친다
        self.play(focus(0))
        l1 = column([
            R"E[(X - 1)^2] = E(X^2 - 2X + 1)",
            R"= E(X^2) - 2E(X) + E(1) = E(X^2) - 2E(X) + 1",
        ], steps_box, scale=0.58, gap=0.45).align_to([0.4, 0, 0], LEFT)
        self.play(Write(l1[0]))
        self.play(Write(l1[1]))
        self.wait(0.6)

        # ── 2. 두 기댓값: 표의 줄 둘
        self.play(focus(1))
        self.play(FadeIn(heads[2]), *[ShowCreation(cells[(2, c)]) for c in range(4)])
        xf = ["0", R"\tfrac{1}{2}", "0", R"\tfrac{3}{6}"]
        for c in range(4):
            self.play(FadeIn(Tex(xf[c]).scale(0.7).set_color(MEAN_COLOR).move_to(cells[(2, c)])), run_time=0.3)
        ex = Tex(R"E(X) = 0 + \tfrac{1}{2} + 0 + \tfrac{3}{6} = \tfrac{1}{2} + \tfrac{1}{2} = 1").scale(0.58).set_color(INK)
        ex.next_to(l1, DOWN, buff=0.4).align_to(l1, LEFT)
        self.play(Write(ex))
        self.play(FadeIn(heads[3]), *[ShowCreation(cells[(3, c)]) for c in range(4)])
        x2f = ["0", R"\tfrac{1}{2}", "0", R"\tfrac{9}{6}"]
        for c in range(4):
            self.play(FadeIn(Tex(x2f[c]).scale(0.7).set_color(CALM).move_to(cells[(3, c)])), run_time=0.3)
        ex2 = Tex(R"E(X^2) = 0 + \tfrac{1}{2} + 0 + \tfrac{9}{6} = \tfrac{1}{2} + \tfrac{3}{2} = 2").scale(0.58).set_color(INK)
        ex2.next_to(ex, DOWN, buff=0.25).align_to(l1, LEFT)
        self.play(Write(ex2))
        self.wait(0.6)

        # ── 3. 합친다
        self.play(focus(2))
        ans = Tex(R"E[(X - 1)^2] = 2 - 2\cdot 1 + 1 = 1").scale(0.65).set_color(MEAN_COLOR)
        ans.next_to(ex2, DOWN, buff=0.4).align_to(l1, LEFT)
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C9. 예제 4.20 음료 수요 — 슬라이드 50 뒤 (51 앞)
# ─────────────────────────────────────────────────────────────
class Example420Drink(InteractiveScene):
    """g(X) = X² + X − 2, f(x) = 2(x−1) (1<x<2). 기댓값을 갈라 E(X²) + E(X) − 2. 적분 둘을 원시함수·대입까지. 답 5/2 → 2500 L."""

    def construct(self):
        head = slide_title("Example 4.20")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((0.8, 2.2, 1), (0, 2.2, 1), width=3.8, height=2.4).move_to([-4.4, -1.4, 0])
        g = axes.get_graph(lambda x: 2 * (x - 1), x_range=(1, 2)).set_stroke(ACCENT, 3)
        area = area_under(axes, g, 1, 2, color=ACCENT, opacity=0.3)
        marks = x_marks(axes, [1, 2])
        f_tag = Tex(R"f(x) = 2(x - 1),\ 1 < x < 2").scale(0.6).set_color(ACCENT).next_to(axes, UP, buff=0.15)
        ask = Tex(R"g(X) = X^2 + X - 2").scale(0.7).set_color(INK).move_to([-4.4, 2.1, 0])
        unit = note("thousands of liters", 20, GREY_B).next_to(ask, DOWN, buff=0.1)
        self.play(ShowCreation(axes), FadeIn(marks), ShowCreation(g), FadeIn(area), FadeIn(f_tag), FadeIn(ask), FadeIn(unit))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. split the expectation", "2. E(X)", "3. E(X²)", "4. combine"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. 가른다
        self.play(focus(0))
        l1 = column([R"E(X^2 + X - 2) = E(X^2) + E(X) - 2"], unit, scale=0.55, gap=0.3).align_to(ask, LEFT)
        self.play(Write(l1[0]))
        self.wait(0.5)

        # ── 2. E(X)
        self.play(focus(1))
        l2 = column([
            R"E(X) = \int_1^2 x\cdot 2(x - 1)\,dx = \int_1^2 (2x^2 - 2x)\,dx",
            R"= \Big[\tfrac{2x^3}{3} - x^2\Big]_1^2 = \big(\tfrac{16}{3} - 4\big) - \big(\tfrac{2}{3} - 1\big) = \tfrac{4}{3} + \tfrac{1}{3} = \tfrac{5}{3}",
        ], steps_box, scale=0.55, gap=0.45).align_to([0.2, 0, 0], LEFT)
        self.play(Write(l2[0]))
        self.play(Write(l2[1]), run_time=1.2)
        self.wait(0.5)

        # ── 3. E(X²)
        self.play(focus(2))
        l3 = column([
            R"E(X^2) = \int_1^2 x^2\cdot 2(x - 1)\,dx = \int_1^2 (2x^3 - 2x^2)\,dx",
            R"= \Big[\tfrac{x^4}{2} - \tfrac{2x^3}{3}\Big]_1^2 = \big(8 - \tfrac{16}{3}\big) - \big(\tfrac{1}{2} - \tfrac{2}{3}\big) = \tfrac{8}{3} + \tfrac{1}{6} = \tfrac{17}{6}",
        ], l2, scale=0.55, gap=0.3).align_to(l2, LEFT)
        self.play(Write(l3[0]))
        self.play(Write(l3[1]), run_time=1.2)
        self.wait(0.5)

        # ── 4. 합친다
        self.play(focus(3))
        l4 = column([
            R"E(X^2 + X - 2) = \tfrac{17}{6} + \tfrac{5}{3} - 2 = \tfrac{17}{6} + \tfrac{10}{6} - \tfrac{12}{6} = \tfrac{15}{6} = \tfrac{5}{2}",
        ], l3, scale=0.55, gap=0.35).align_to(l2, LEFT)
        l4[0].set_color(MEAN_COLOR)
        self.play(Write(l4[0]), run_time=1.2)
        lit = label("2500 liters a week", 26, MEAN_COLOR).next_to(axes, DOWN, buff=0.55)
        self.play(FlashAround(l4[0], color=MEAN_COLOR, buff=0.1), FadeIn(lit))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C10. 예제 4.21 독립이면 E(XY) = E(X)E(Y) — 슬라이드 52 뒤 (53 앞)
# ─────────────────────────────────────────────────────────────
class Example421Independent(InteractiveScene):
    """x(1+3y²)/4 가 (x/2)·((1+3y²)/2) 로 갈라진다(직사각형 정의역). E(X) = 4/3, E(Y) = 5/8, E(XY) = 5/6 = (4/3)(5/8)."""

    def construct(self):
        head = slide_title("Example 4.21")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 정의역: 직사각형 0<x<2, 0<y<1
        W, H = 3.2, 1.6
        x0, y0 = -6.0, -2.6
        rect = Rectangle(width=W, height=H).set_stroke(GREY_B, 2).set_fill(ACCENT, 0.2).move_to([x0 + W / 2, y0 + H / 2, 0])
        xl = VGroup(Tex("0").scale(0.55), Tex("2").scale(0.55)).set_color(GREY_B)
        xl[0].next_to(rect.get_corner(DL), DOWN, buff=0.1)
        xl[1].next_to(rect.get_corner(DR), DOWN, buff=0.1)
        yl = Tex("1").scale(0.55).set_color(GREY_B).next_to(rect.get_corner(UL), LEFT, buff=0.1)
        f_tag = Tex(R"f(x, y) = \tfrac{x(1 + 3y^2)}{4}").scale(0.65).set_color(ACCENT).next_to(rect, UP, buff=0.25)
        dom = note("rectangle domain", 20, GREY_B).next_to(rect, DOWN, buff=0.35).align_to(rect, LEFT)
        self.play(ShowCreation(rect), FadeIn(xl), FadeIn(yl), FadeIn(f_tag), FadeIn(dom))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. factor f into g(x)h(y)", "2. E(X)", "3. E(Y)", "4. E(XY), then compare"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. 인수분해
        self.play(focus(0))
        l1 = column([
            R"f(x, y) = \tfrac{x}{2}\cdot\tfrac{1 + 3y^2}{2} = g(x)\,h(y)",
        ], steps_box, scale=0.6, gap=0.45).align_to([0.2, 0, 0], LEFT)
        ind = label("independent", 24, CALM).next_to(l1[0], RIGHT, buff=0.4)
        self.play(Write(l1[0]), FadeIn(ind))
        self.wait(0.5)

        # ── 2. E(X)
        self.play(focus(1))
        l2 = column([
            R"E(X) = \int_0^2 x\cdot\tfrac{x}{2}\,dx = \Big[\tfrac{x^3}{6}\Big]_0^2 = \tfrac{8}{6} = \tfrac{4}{3}",
        ], l1, scale=0.58, gap=0.35).align_to(l1, LEFT)
        self.play(Write(l2[0]), run_time=1.0)
        self.wait(0.4)

        # ── 3. E(Y)
        self.play(focus(2))
        l3 = column([
            R"E(Y) = \int_0^1 y\cdot\tfrac{1 + 3y^2}{2}\,dy = \tfrac{1}{2}\Big[\tfrac{y^2}{2} + \tfrac{3y^4}{4}\Big]_0^1 = \tfrac{1}{2}\big(\tfrac{1}{2} + \tfrac{3}{4}\big) = \tfrac{5}{8}",
        ], l2, scale=0.55, gap=0.35).align_to(l1, LEFT)
        self.play(Write(l3[0]), run_time=1.4)
        self.wait(0.4)

        # ── 4. E(XY): 적분이 둘로 갈라진다
        self.play(focus(3))
        l4 = column([
            R"E(XY) = \int_0^1\int_0^2 xy\cdot\tfrac{x(1 + 3y^2)}{4}\,dx\,dy",
            R"= \Big(\int_0^2 \tfrac{x^2}{2}\,dx\Big)\Big(\int_0^1 \tfrac{y(1 + 3y^2)}{2}\,dy\Big) = \tfrac{4}{3}\cdot\tfrac{5}{8} = \tfrac{5}{6} = E(X)\,E(Y)",
        ], l3, scale=0.55, gap=0.35).align_to(l1, LEFT)
        l4[1].set_color(MEAN_COLOR)
        self.play(Write(l4[0]), run_time=1.4)
        self.play(Write(l4[1]))
        thm = label("Theorem 4.8 holds", 24, MEAN_COLOR).next_to(dom, DOWN, buff=0.3).align_to(rect, LEFT)
        self.play(FlashAround(l4[1], color=MEAN_COLOR, buff=0.1), FadeIn(thm))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C11. 예제 4.22 · 4.23 선형결합의 분산 — 슬라이드 54 뒤 (55 앞)
# ─────────────────────────────────────────────────────────────
class Example422423Variance(InteractiveScene):
    """4.22: Z = 3X − 4Y + 8, σ_XY = −2 → 130. 4.23: 독립, Z = 3X − 2Y + 5 → 30. 상수는 버리고 a²·b²·2ab 를 채운다."""

    def construct(self):
        head = slide_title("Example 4.22, 4.23")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        steps, steps_box, focus = steps_panel(["1. drop the constant", "2. a², b², 2ab", "3. plug in"], pos=(-3.9, 2.05, 0))
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))

        g22 = Tex(R"\mathrm{4.22:}\ \sigma_X^2 = 2,\ \sigma_Y^2 = 4,\ \sigma_{XY} = -2").scale(0.6).set_color(GREY_B).move_to([3.2, 2.45, 0])
        g23 = Tex(R"\mathrm{4.23:}\ \sigma_X^2 = 2,\ \sigma_Y^2 = 3,\ \mathrm{independent}").scale(0.6).set_color(GREY_B).next_to(g22, DOWN, buff=0.3).align_to(g22, LEFT)
        self.play(FadeIn(g22), FadeIn(g23))
        self.wait(0.5)

        left_x, right_x = -6.6, 0.6
        # ── 1. 상수를 버린다
        self.play(focus(0))
        a = column([R"Z = 3X - 4Y + 8", R"\sigma_Z^2 = \sigma^2_{3X - 4Y}"], steps_box, scale=0.62, gap=0.5).align_to([left_x, 0, 0], LEFT)
        b = column([R"Z = 3X - 2Y + 5", R"\sigma_Z^2 = \sigma^2_{3X - 2Y}"], steps_box, scale=0.62, gap=0.5).align_to([right_x, 0, 0], LEFT)
        ta = note("Example 4.22", 22, ACCENT).next_to(a, UP, buff=0.1).align_to(a, LEFT)
        tb = note("Example 4.23, independent", 22, CALM).next_to(b, UP, buff=0.1).align_to(b, LEFT)
        self.play(FadeIn(ta), FadeIn(tb), Write(a[0]), Write(b[0]))
        self.play(Write(a[1]), Write(b[1]))
        self.wait(0.5)

        # ── 2. 계수
        self.play(focus(1))
        a2 = column([R"= 3^2\sigma_X^2 + (-4)^2\sigma_Y^2 + 2(3)(-4)\,\sigma_{XY}",
                     R"= 9\sigma_X^2 + 16\sigma_Y^2 - 24\,\sigma_{XY}"], a, scale=0.6, gap=0.3).align_to(a, LEFT)
        b2 = column([R"= 3^2\sigma_X^2 + (-2)^2\sigma_Y^2 + 2(3)(-2)\cdot 0",
                     R"= 9\sigma_X^2 + 4\sigma_Y^2"], b, scale=0.6, gap=0.3).align_to(b, LEFT)
        self.play(Write(a2[0]), Write(b2[0]))
        cross_a = note("cross term: sign matters", 20, WARN).next_to(a2[0], DOWN, buff=0.08).align_to(a, LEFT)
        cross_b = note("cross term 0", 20, CALM).next_to(b2[0], DOWN, buff=0.08).align_to(b, LEFT)
        self.play(FadeIn(cross_a), FadeIn(cross_b))
        self.wait(0.5)
        a2[1].next_to(cross_a, DOWN, buff=0.15).align_to(a, LEFT)
        b2[1].next_to(cross_b, DOWN, buff=0.15).align_to(b, LEFT)
        self.play(Write(a2[1]), Write(b2[1]))
        self.wait(0.5)

        # ── 3. 대입
        self.play(focus(2))
        a3 = column([R"= 9(2) + 16(4) - 24(-2)", R"= 18 + 64 + 48 = 130"], a2[1], scale=0.6, gap=0.3).align_to(a, LEFT)
        b3 = column([R"= 9(2) + 4(3)", R"= 18 + 12 = 30"], b2[1], scale=0.6, gap=0.3).align_to(b, LEFT)
        a3[1].set_color(MEAN_COLOR)
        b3[1].set_color(MEAN_COLOR)
        self.play(Write(a3[0]), Write(b3[0]))
        self.play(Write(a3[1]), Write(b3[1]))
        self.play(FlashAround(a3[1], color=MEAN_COLOR, buff=0.1), FlashAround(b3[1], color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C12. 체비셰프 — 분포를 몰라도 되는 띠 — 슬라이드 58 (정리 4.10) 앞
# ─────────────────────────────────────────────────────────────
class ChebyshevBand(InteractiveScene):
    """모양이 울퉁불퉁한 밀도 하나. μ ± kσ 띠가 k 와 함께 넓어진다. 어떤 분포든 띠 안에 최소 1 − 1/k², 밖에 최대 1/k²."""

    def construct(self):
        head = slide_title("Chebyshev's Theorem")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((0, 10, 1), (0, 0.5, 1), width=7.0, height=2.8).move_to([-2.8, -0.8, 0])
        mu, sig = 5.0, 1.3

        def f(x):
            return 0.42 * math.exp(-((x - 5.2) ** 2) / 2.2) + 0.16 * math.exp(-((x - 2.6) ** 2) / 0.9) + 0.06 * math.exp(-((x - 8.2) ** 2) / 1.2)
        g = axes.get_graph(f, x_range=(0, 10)).set_stroke(ACCENT, 3)
        mu_line = dashed(axes.c2p(mu, 0), axes.c2p(mu, f(mu) + 0.03))
        mu_tag = Tex(R"\mu").scale(0.7).set_color(MEAN_COLOR).next_to(axes.c2p(mu, 0), DOWN, buff=0.1)
        any_tag = label("any distribution", 24, GREY_B).next_to(axes, UP, buff=0.15).align_to(axes, LEFT)
        self.play(ShowCreation(axes), ShowCreation(g), FadeIn(any_tag))
        self.play(ShowCreation(mu_line), FadeIn(mu_tag))
        self.wait(0.5)

        k = ValueTracker(1.0)
        band = always_redraw(lambda: area_under(axes, g, mu - k.get_value() * sig, mu + k.get_value() * sig, color=MEAN_COLOR, opacity=0.45))
        lo = always_redraw(lambda: Line(axes.c2p(mu - k.get_value() * sig, 0), axes.c2p(mu - k.get_value() * sig, 0.42)).set_stroke(MEAN_COLOR, 2))
        hi = always_redraw(lambda: Line(axes.c2p(mu + k.get_value() * sig, 0), axes.c2p(mu + k.get_value() * sig, 0.42)).set_stroke(MEAN_COLOR, 2))
        lo_tag = Tex(R"\mu - k\sigma").scale(0.6).set_color(MEAN_COLOR)
        hi_tag = Tex(R"\mu + k\sigma").scale(0.6).set_color(MEAN_COLOR)
        lo_tag.add_updater(lambda m: m.next_to(axes.c2p(mu - k.get_value() * sig, 0.42), UP, buff=0.08))
        hi_tag.add_updater(lambda m: m.next_to(axes.c2p(mu + k.get_value() * sig, 0.42), UP, buff=0.08))
        self.play(FadeIn(band), FadeIn(lo), FadeIn(hi), FadeIn(lo_tag), FadeIn(hi_tag))

        thm = column([
            R"P(\mu - k\sigma < X < \mu + k\sigma) \ge 1 - \tfrac{1}{k^2}",
        ], head[1], scale=0.7, gap=0.5).align_to([1.2, 0, 0], LEFT)
        thm[0].set_color(MEAN_COLOR)
        inside = label("inside: at least 1 − 1/k²", 24, MEAN_COLOR).next_to(thm, DOWN, buff=0.2).align_to(thm, LEFT)
        self.play(Write(thm[0]), FadeIn(inside))
        self.wait(0.6)

        rows = column([
            R"k = 2:\ 1 - \tfrac{1}{4} = \tfrac{3}{4}",
            R"k = 3:\ 1 - \tfrac{1}{9} = \tfrac{8}{9}",
        ], inside, scale=0.65, gap=0.4).align_to(thm, LEFT)
        self.play(k.animate.set_value(2.0), run_time=1.2)
        self.play(Write(rows[0]))
        self.wait(0.5)
        self.play(k.animate.set_value(3.0), run_time=1.2)
        self.play(Write(rows[1]))
        self.wait(0.5)

        outside = label("outside: at most 1/k²", 24, WARN).next_to(rows, DOWN, buff=0.35).align_to(thm, LEFT)
        out_f = Tex(R"P(|X - \mu| \ge k\sigma) \le \tfrac{1}{k^2}").scale(0.65).set_color(WARN).next_to(outside, DOWN, buff=0.15).align_to(thm, LEFT)
        self.play(FadeIn(outside), Write(out_f))
        no = label("no shape needed", 24, GREY_B).next_to(axes, DOWN, buff=0.5).align_to(axes, LEFT)
        self.play(FadeIn(no), FlashAround(thm[0], color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# C13. 예제 4.27 μ = 8, σ² = 9 — 슬라이드 59 뒤 (60 앞)
# ─────────────────────────────────────────────────────────────
class Example427Chebyshev(InteractiveScene):
    """σ = 3. (a) −4 와 20 은 8 ∓ 4·3 이라 k = 4 → ≥ 15/16. (b) |X − 8| ≥ 6 은 띠 밖, k = 2 → ≤ 1/4."""

    def construct(self):
        head = slide_title("Example 4.27")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        line = NumberLine(x_range=(-4, 20, 4), width=6.2, include_numbers=True).move_to([-3.5, -0.9, 0])
        mu_dot = Dot(line.n2p(8), radius=0.1).set_color(MEAN_COLOR)
        mu_tag = Tex(R"\mu = 8").scale(0.65).set_color(MEAN_COLOR).next_to(mu_dot, UP, buff=0.15)
        given = Tex(R"\mu = 8,\quad \sigma^2 = 9,\quad \mathrm{distribution\ unknown}").scale(0.65).set_color(GREY_B).move_to([-3.4, 2.2, 0])
        self.play(FadeIn(given), ShowCreation(line), FadeIn(mu_dot), FadeIn(mu_tag))
        self.wait(0.4)

        steps, steps_box, focus = steps_panel(["1. σ from σ²", "2. ends as μ ± kσ", "3. apply 1 − 1/k²", "4. (b): the outside"])
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.5)

        # ── 1. σ
        self.play(focus(0))
        l1 = column([R"\sigma = \sqrt{9} = 3"], steps_box, scale=0.62, gap=0.45).align_to([0.1, 0, 0], LEFT)
        self.play(Write(l1[0]))
        self.wait(0.4)

        # ── 2. 양 끝을 μ ± kσ 로
        self.play(focus(1))
        band_a = Rectangle(width=line.n2p(20)[0] - line.n2p(-4)[0], height=0.5).set_stroke(width=0).set_fill(MEAN_COLOR, 0.3)
        band_a.move_to(line.n2p(8))
        l2 = column([
            R"(a)\ \ -4 = 8 - (4)(3),\quad 20 = 8 + (4)(3)\ \ \Rightarrow\ k = 4",
        ], l1, scale=0.58, gap=0.35).align_to(l1, LEFT)
        self.play(FadeIn(band_a), Write(l2[0]), run_time=1.2)
        self.wait(0.5)

        # ── 3. 정리 적용
        self.play(focus(2))
        l3 = column([
            R"P(-4 < X < 20) = P[8 - (4)(3) < X < 8 + (4)(3)]",
            R"\ge 1 - \tfrac{1}{4^2} = \tfrac{15}{16}",
        ], l2, scale=0.55, gap=0.28).align_to(l1, LEFT)
        l3[1].set_color(MEAN_COLOR)
        self.play(Write(l3[0]), run_time=1.0)
        self.play(Write(l3[1]), run_time=0.8)
        self.play(FlashAround(l3[1], color=MEAN_COLOR, buff=0.1))
        self.wait(0.8)

        # ── 4. (b) 띠 밖
        self.play(focus(3))
        band_b = Rectangle(width=line.n2p(14)[0] - line.n2p(2)[0], height=0.5).set_stroke(WARN, 2).set_fill(CALM, 0.35)
        band_b.move_to(line.n2p(8))
        ends = VGroup(Tex("2").scale(0.6).set_color(WARN).next_to(line.n2p(2), DOWN, buff=0.45),
                      Tex("14").scale(0.6).set_color(WARN).next_to(line.n2p(14), DOWN, buff=0.45))
        self.play(FadeOut(band_a), FadeIn(band_b), FadeIn(ends))
        l4 = column([
            R"(b)\ \ P(|X - 8| \ge 6) = 1 - P(|X - 8| < 6)",
            R"= 1 - P(2 < X < 14),\qquad 6 = (2)(3),\ k = 2",
            R"P(2 < X < 14) \ge 1 - \tfrac{1}{4} = \tfrac{3}{4}\ \ \Rightarrow\ P(|X - 8| \ge 6) \le \tfrac{1}{4}",
        ], l3, scale=0.55, gap=0.28).align_to(l1, LEFT)
        l4[2].set_color(MEAN_COLOR)
        self.play(Write(l4[0]), run_time=1.2)
        self.play(Write(l4[1]), run_time=1.0)
        self.play(Write(l4[2]), run_time=0.8)
        out_tag = label("outside the band: at most 1/4", 24, WARN).next_to(line, DOWN, buff=0.85).align_to(line, LEFT)
        self.play(FlashAround(l4[2], color=MEAN_COLOR, buff=0.1), FadeIn(out_tag))
        self.wait(2)
