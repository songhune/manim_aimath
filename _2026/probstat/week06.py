# -*- coding: utf-8 -*-
"""확률과통계 「이산형 확률분포」 장 (Walpole Chapter 5) — 이항 · 초기하 · 음이항 · 기하 · 포아송.

강의 교안 `확률과통계/교육메모/06주차.md`(9차) · `07주차.md`(10차) 의 「영상 태그」 를 옮긴 것이다.
도구와 규칙은 week05.py 와 같다. 개념 영상은 정의 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음 ·
풀이 슬라이드 앞이다(하네스 3.6). 소재는 덱(PS1_05_restyled.pptx, 레이아웃 정리 뒤 64장)의 정의와
예제로 한정한다. 화면 문구는 영어, 여섯 낱말까지.

이 장은 예제 스무 개를 다 그리지 않는다(2026-10-01, 사용자 결정). 그림이 있어야 이해가 달라지는 것만
골랐다 — 분포마다 "식이 어디서 나오는가" 한 편씩(개념 7편)과, 표 읽기 · 근사 · 판정처럼 막대를 칠해야
보이는 예제 6편. 공식에 수만 넣는 예제(5.1 · 5.3 · 5.4 · 5.6 · 5.7 · 5.9–5.11 · 5.13 · 5.15 · 5.16 ·
5.19 · 5.20)는 풀이 판과 교안으로 넘긴다.

이 장의 약속 (`probstat-scene-pacing` 메모):
    개념 영상은 분포의 이름과 기호(b · h · b* · g · p)를 먼저 걸고, 식을 "경우의 수 × 한 경우의 확률" 로 조립한다.
    예제 영상은 풀이 단계를 먼저 목록으로 걸어 두고(`steps_panel`) 한 단계씩 진행한다.
    누적합(표 A.1 · A.2)은 막대를 왼쪽부터 칠해 보이고, 차를 구할 때는 칠한 것에서 덜어 낸다.

덱 삽입 자리 (원본 PS1_05_restyled.pptx 64장 기준 — 2026-10-01 도구/레이아웃_정리_PS1_05.py 로 52장을 정리한 것.
insert_videos.py 의 PS1_05_INSERT 와 같다. "N 앞" 은 개념 영상, "N 뒤" 는 예제 영상(풀이 앞)):
    9차 10/2 — 5.2 이항 · 다항, 5.3 초기하 (원본 1–41)
    BernoulliToBinomial              4 앞    이항분포 정의 (여덟 결과를 x 로 묶어 C(3,x)·p^x q^(3−x))
    Example52TableA1                 9 뒤    예제 5.2 (표 A.1 누적합, 풀이 11)
    BinomialMeanVariance            15 앞    정리 5.1 (X = I₁ + … + Iₙ, μ = np, σ² = npq)
    Example55Chebyshev              18 뒤    예제 5.5 (μ ± 2σ 띠)
    SamplingWithoutReplacement      25 앞    초기하 도입 (복원 · 비복원, 세는 식)
    Example58Acceptance             26 뒤    예제 5.8 (합격판정 표본검사)
    Example512BinomialApproximation 37 뒤    예제 5.12 (n/N ≤ 0.05 이면 이항으로)
    10차 10/6 — 5.4 음이항 · 기하, 5.5 포아송 (원본 42–64)
    NegativeBinomialWaiting         42 앞    음이항분포 정의 (마지막 시행이 k 번째 성공)
    Example514Playoffs              43 뒤    예제 5.14
    GeometricFirstSuccess           45 앞    기하분포 정의 · 정리 5.3 (k = 1, μ = 1/p)
    PoissonCounts                   51 앞    포아송분포 정의 (구간 안 사건 수, μ = 0.1 · 2 · 5 의 모양)
    BinomialToPoisson               52 앞    정리 5.4 · 5.5 (np = μ 를 붙들고 n 을 키운다)
    Example517518Table              56 뒤    예제 5.17 (5.18 은 58·59 — 한 영상이 둘을 겸한다)

참고: legacy/_2023/clt/main.py (ChartBars — 축 위 막대와 값 갱신),
      legacy/_2020/beta/helpers.py (get_binomial_formula), legacy/_2020/beta/beta1.py (ShowBinomialFormula).

렌더 (저장소 루트에서, 한 번에 한 프로세스만):
    ./render.sh check _2026/probstat/week06.py
    ./render.sh ppt   _2026/probstat/week06.py BernoulliToBinomial
"""
from math import comb, exp, factorial

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN,
    label, note, panel, ring, slide_title, bar,
)
from _2026.probstat.week02 import letter_chip
from _2026.probstat.week05 import steps_panel, column, fulcrum_at


# ─────────────────────────────────────────────────────────────
# 도구 — 분포 값, 축, 막대
# ─────────────────────────────────────────────────────────────
def binom_pmf(n, p, upto=None):
    """b(x; n, p), x = 0 … upto. n 을 넘는 자리는 0 이다."""
    upto = n if upto is None else upto
    return [comb(n, x) * p ** x * (1 - p) ** (n - x) if x <= n else 0.0 for x in range(upto + 1)]


def hyper_pmf(N, n, k, upto=None):
    """h(x; N, n, k), x = 0 … upto."""
    upto = min(n, k) if upto is None else upto
    return [comb(k, x) * comb(N - k, n - x) / comb(N, n) if x <= min(n, k) else 0.0
            for x in range(upto + 1)]


def negbin_pmf(k, p, xs):
    """b*(x; k, p) — k 번째 성공이 x 번째 시행에 나올 확률."""
    return [comb(x - 1, k - 1) * p ** k * (1 - p) ** (x - k) if x >= k else 0.0 for x in xs]


def poisson_pmf(mu, upto):
    return [exp(-mu) * mu ** x / factorial(x) for x in range(upto + 1)]


def axis(lo, hi, width, pos, every=1, size=0.5):
    """눈금만 있는 수직선과 숫자 라벨. 막대가 많을 때 숫자를 솎아 적는다."""
    line = NumberLine(x_range=(lo, hi, 1), width=width, include_numbers=False)
    line.set_stroke(GREY_B, 2).move_to(pos)
    nums = VGroup(*[Tex(str(x)).scale(size).set_color(GREY_B).next_to(line.n2p(x), DOWN, buff=0.16)
                    for x in range(lo, hi + 1, every)])
    return line, nums


def chart(line, xs, fs, vmax, color=ACCENT, width=0.36, height=2.6, opacity=0.85):
    """수직선 위 x 자리마다 높이 f 의 막대."""
    bars = VGroup()
    for x, f in zip(xs, fs):
        b = bar(f, vmax, width=width, height=height, color=color, opacity=opacity)
        b.move_to(line.n2p(x), aligned_edge=DOWN).shift(UP * 0.02)
        bars.add(b)
    return bars


def outline(line, xs, fs, vmax, color=MEAN_COLOR, width=0.36, height=2.6):
    """속이 빈 막대. 견줄 분포를 겹쳐 놓을 때 쓴다."""
    bars = chart(line, xs, fs, vmax, color, width, height, opacity=0.0)
    for b in bars:
        b.set_stroke(color, 3)
    return bars


def paint(bars, on, color=MEAN_COLOR, off=MUTED):
    """on 에 든 번호의 막대만 밝히고 나머지는 물린다."""
    anims = []
    for i, b in enumerate(bars):
        if i in on:
            anims.append(b.animate.set_fill(color, 0.9).set_stroke(color, 2))
        else:
            anims.append(b.animate.set_fill(off, 0.3).set_stroke(off, 1))
    return anims


def pivot(point):
    """평균 자리의 받침점. 눈금 숫자를 가리지 않게 숫자 아래에 둔다."""
    return fulcrum_at(point).shift(DOWN * 0.42)


def trials(pattern, size=0.5, good="S", buff=0.1):
    """시행 한 줄. 성공은 파랑, 실패는 빨강."""
    row = VGroup(*[letter_chip(ch, size, ACCENT if ch == good else WARN) for ch in pattern])
    return row.arrange(RIGHT, buff=buff)


def lot(n_bad, n_good, size=0.46, buff=0.1):
    """로트. 불량 D 는 빨강, 양품 G 는 파랑."""
    chips = VGroup(*[letter_chip("D", size, WARN) for _ in range(n_bad)],
                   *[letter_chip("G", size, ACCENT) for _ in range(n_good)])
    return chips.arrange(RIGHT, buff=buff)


# ─────────────────────────────────────────────────────────────
# 1. 베르누이 시행에서 이항분포로 — 슬라이드 4 (이항분포 정의) 앞
# ─────────────────────────────────────────────────────────────
class BernoulliToBinomial(InteractiveScene):
    """이름을 먼저 건다: b(x; n, p). 슬라이드 3 의 예(세 개를 뽑아 불량 D 를 성공으로, p = 1/4)를 그대로 쓴다.
    여덟 결과를 x = 0 · 1 · 2 · 3 으로 묶으면 묶음마다 결과 수는 C(3, x), 한 결과의 확률은 p^x q^(3−x) 로 같다.
    둘을 곱한 것이 f(x) = 27/64 · 27/64 · 9/64 · 1/64 이고, 일반식은 그 두 조각의 곱이다."""

    def construct(self):
        head = slide_title("Binomial Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"b(x;\, n,\, p)").scale(0.9).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.9)
        self.play(Write(name))

        setup = VGroup(note("3 items, D = success", 22, GREY_B),
                       Tex(R"p = \tfrac14,\quad q = \tfrac34").scale(0.65).set_color(INK))
        setup.arrange(RIGHT, buff=0.5).next_to(head[1], DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(setup))

        # ── 여덟 결과를 x 로 묶는다
        groups = {0: ["NNN"], 1: ["NND", "NDN", "DNN"], 2: ["NDD", "DND", "DDN"], 3: ["DDD"]}
        col_x = [-4.7, -2.85, -1.0, 0.85]
        heads_x, cols = VGroup(), {}
        for x in range(4):
            hx = Tex("x = %d" % x).scale(0.65).set_color(ACCENT).move_to([col_x[x], 1.55, 0])
            heads_x.add(hx)
            ts = VGroup(*[trials(s, 0.36, good="N", buff=0.05) for s in groups[x]]).arrange(DOWN, buff=0.14)
            ts.next_to(hx, DOWN, buff=0.22)
            cols[x] = ts
        every = VGroup(*[t for x in range(4) for t in cols[x]])
        self.play(LaggedStartMap(FadeIn, every, lag_ratio=0.1), run_time=1.6)
        self.play(FadeIn(heads_x))
        self.wait(0.6)

        # 한 결과의 확률: 순서가 달라도 곱은 같다
        ndn = cols[1][1]
        mark = ring(ndn, MEAN_COLOR, 0.06)
        one = Tex(R"P(NDN) = \tfrac34\cdot\tfrac14\cdot\tfrac34 = \tfrac{9}{64}").scale(0.62).set_color(INK)
        one.move_to([4.5, 1.2, 0])
        self.play(ShowCreation(mark), Write(one))
        same = label("same x, same probability", 22, GREY_B).next_to(one, DOWN, buff=0.2)
        marks = VGroup(*[ring(t, MEAN_COLOR, 0.06) for t in cols[1]])
        self.play(ReplacementTransform(mark, marks[1]), FadeIn(marks[0]), FadeIn(marks[2]), FadeIn(same))
        self.wait(0.8)
        self.play(FadeOut(marks))

        # ── 세 줄: 결과 수 · 한 결과의 확률 · 곱
        rows_y = [-0.45, -1.2, -1.95]
        names = VGroup(note("ways", 22, CALM), note("each way", 22, GREY_B), Tex("f(x)").scale(0.65).set_color(MEAN_COLOR))
        for nm, y in zip(names, rows_y):
            nm.move_to([-6.35, y, 0]).align_to([-5.75, 0, 0], RIGHT)
        ways = VGroup(*[Tex(R"\tbinom{3}{%d} = %d" % (x, comb(3, x))).scale(0.6).set_color(CALM).move_to([col_x[x], rows_y[0], 0])
                        for x in range(4)])
        each = VGroup(*[Tex(R"\tfrac{%d}{64}" % v).scale(0.7).set_color(INK).move_to([col_x[x], rows_y[1], 0])
                        for x, v in enumerate([27, 9, 3, 1])])
        prods = [27, 27, 9, 1]
        fx = VGroup(*[Tex(R"\tfrac{%d}{64}" % v).scale(0.75).set_color(MEAN_COLOR).move_to([col_x[x], rows_y[2], 0])
                      for x, v in enumerate(prods)])
        self.play(FadeIn(names[0]), LaggedStartMap(FadeIn, ways, lag_ratio=0.15))
        self.wait(0.4)
        self.play(FadeIn(names[1]), LaggedStartMap(FadeIn, each, lag_ratio=0.15))
        self.wait(0.4)
        self.play(FadeIn(names[2]), LaggedStartMap(FadeIn, fx, lag_ratio=0.15))
        self.wait(0.8)

        # ── 일반식: 두 조각의 곱
        eq = Tex("=").scale(0.8).set_color(MEAN_COLOR)
        piece1 = Tex(R"\binom{n}{x}").scale(0.8).set_color(CALM)
        piece2 = Tex(R"p^{x} q^{\,n-x}").scale(0.8).set_color(INK)
        formula = VGroup(eq, piece1, piece2).arrange(RIGHT, buff=0.18)
        self.play(FadeOut(one), FadeOut(same))
        self.play(name.animate.move_to([3.3, 1.25, 0]))
        formula.next_to(name, RIGHT, buff=0.18)
        tag1 = note("ways", 20, CALM).next_to(piece1, DOWN, buff=0.18)
        tag2 = note("each way", 20, GREY_B).next_to(piece2, DOWN, buff=0.22)
        self.play(Write(formula))
        self.play(FadeIn(tag1), FadeIn(tag2))
        self.wait(0.8)

        # ── 막대로
        line, nums = axis(0, 3, 2.7, [4.6, -2.7, 0])
        bars = chart(line, range(4), [v / 64 for v in prods], 27 / 64, MEAN_COLOR, width=0.5, height=1.7)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(*[TransformFromCopy(fx[x], bars[x]) for x in range(4)], run_time=1.2)
        total = Tex(R"\tfrac{27 + 27 + 9 + 1}{64} = 1").scale(0.55).set_color(GREY_B).next_to(line, UP, buff=1.95)
        self.play(FadeIn(total))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 예제 5.2 표 A.1 읽기 — 슬라이드 9 뒤 (풀이 11 앞)
# ─────────────────────────────────────────────────────────────
class Example52TableA1(InteractiveScene):
    """n = 15, p = 0.4. 표 A.1 은 누적합 B(r) = Σ b(x) 를 준다. 막대를 왼쪽부터 칠한 것이 B(r) 이다.
    (a) X ≥ 10 은 전체에서 B(9) 를 뺀 것 0.0338, (b) 3 ≤ X ≤ 8 은 B(8) − B(2) = 0.8779,
    (c) X = 5 는 B(5) − B(4) = 0.1859."""

    def construct(self):
        head = slide_title("Example 5.2")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        info = Tex(R"n = 15,\quad p = 0.4").scale(0.7).set_color(INK)
        info.next_to(head[1], DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(info))

        steps, steps_box, focus = steps_panel(["1. cumulative sum B(r)", "2. at least 10",
                                               "3. from 3 to 8", "4. exactly 5"], pos=(4.55, 1.75, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        line, nums = axis(0, 15, 7.4, [-3.0, -2.75, 0])
        fs = binom_pmf(15, 0.4)
        bars = chart(line, range(16), fs, 0.21, ACCENT, width=0.36, height=2.7)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.05), run_time=1.2)

        # ── 1. 누적합: 왼쪽부터 r 까지 칠한 것
        self.play(focus(0))
        cum = Tex(R"B(r;\, n,\, p) = \sum_{x=0}^{r} b(x;\, n,\, p)").scale(0.62).set_color(MEAN_COLOR)
        cum.move_to([-3.3, 1.35, 0])
        src = note("Table A.1", 22, GREY_B).next_to(cum, RIGHT, buff=0.35)
        self.play(Write(cum), FadeIn(src))
        for r in (2, 5, 9):
            self.play(*paint(bars, range(r + 1)), run_time=0.6)
            self.wait(0.3)
        b9 = Tex(R"B(9) = 0.9662").scale(0.6).set_color(MEAN_COLOR).next_to(cum, DOWN, buff=0.25).align_to(cum, LEFT)
        self.play(FadeIn(b9))
        self.wait(0.8)

        # ── 2. (a) 10 이상 = 1 − B(9)
        self.play(focus(1))
        col_a = column([R"P(X \ge 10) = 1 - B(9)", R"= 1 - 0.9662 = 0.0338"],
                       steps_box, scale=0.55, gap=0.3).align_to([2.35, 0, 0], LEFT)
        self.play(*paint(bars, range(10, 16), WARN), Write(col_a[0]))
        self.play(Write(col_a[1]))
        self.play(FlashAround(col_a[1], color=MEAN_COLOR, buff=0.08))
        self.wait(1.0)

        # ── 3. (b) 3 에서 8 = B(8) − B(2)
        self.play(focus(2), FadeOut(b9))
        col_b = column([R"P(3 \le X \le 8) = B(8) - B(2)", R"= 0.9050 - 0.0271 = 0.8779"],
                       col_a, scale=0.55, gap=0.3).align_to(col_a, LEFT)
        self.play(*paint(bars, range(0, 9)), Write(col_b[0]))
        self.wait(0.4)
        self.play(*paint(bars, range(3, 9)))
        self.play(Write(col_b[1]))
        self.play(FlashAround(col_b[1], color=MEAN_COLOR, buff=0.08))
        self.wait(1.0)

        # ── 4. (c) 꼭 5 = B(5) − B(4)
        self.play(focus(3))
        col_c = column([R"P(X = 5) = B(5) - B(4)", R"= 0.4032 - 0.2173 = 0.1859"],
                       col_b, scale=0.55, gap=0.3).align_to(col_a, LEFT)
        self.play(*paint(bars, range(0, 6)), Write(col_c[0]))
        self.wait(0.4)
        self.play(*paint(bars, [5]))
        self.play(Write(col_c[1]))
        self.play(FlashAround(col_c[1], color=MEAN_COLOR, buff=0.08))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 이항분포의 평균과 분산 — 슬라이드 15 (정리 5.1) 앞
# ─────────────────────────────────────────────────────────────
class BinomialMeanVariance(InteractiveScene):
    """이름: μ = np, σ² = npq. X 를 시행마다의 지시변수 I_j (성공 1, 실패 0) 의 합으로 쓰면
    E(I_j) = p, 분산은 p − p² = pq 이고, 독립인 n 개를 더하므로 np · npq 가 된다(「수학적 기댓값」 장의 합 정리).
    이어서 덱의 세 분포 — b(x; 3, 1/4), 예제 5.2 의 b(x; 15, 0.4), 예제 5.4 의 b(x; 10, 0.3) — 에 받침점을 세운다."""

    def construct(self):
        head = slide_title("Binomial Mean and Variance")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"\mu = np,\qquad \sigma^2 = npq").scale(0.85).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.8)
        self.play(Write(name))

        # ── 지시변수의 합
        row = trials("SFSSF", 0.5)
        row.move_to([-4.2, 1.5, 0])
        ones = VGroup(*[Tex("1" if ch == "S" else "0").scale(0.7).set_color(ACCENT if ch == "S" else WARN)
                        .next_to(c, DOWN, buff=0.15) for ch, c in zip("SFSSF", row)])
        tag = note("one trial: 1 or 0", 22, GREY_B).next_to(row, RIGHT, buff=0.5)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1), FadeIn(tag))
        self.play(LaggedStartMap(FadeIn, ones, lag_ratio=0.1))
        lines = column([
            R"X = I_1 + I_2 + \cdots + I_n",
            R"E(I_j) = 0\cdot q + 1\cdot p = p",
            R"\sigma^2_{I_j} = E(I_j^2) - p^2 = p - p^2 = pq",
            R"\mu = p + p + \cdots + p = np",
            R"\sigma^2 = pq + pq + \cdots + pq = npq",
        ], ones, scale=0.62, gap=0.4, buff=0.24).align_to(row, LEFT)
        lines[3].set_color(MEAN_COLOR)
        lines[4].set_color(MEAN_COLOR)
        self.play(Write(lines[0]))
        self.wait(0.4)
        self.play(Write(lines[1]))
        self.play(Write(lines[2]), run_time=1.2)
        self.wait(0.5)
        self.play(Write(lines[3]))
        indep = note("independent trials", 22, CALM).next_to(lines[4], RIGHT, buff=0.5)
        self.play(Write(lines[4]), FadeIn(indep))
        self.wait(1.2)

        # ── 덱의 세 분포에 받침점
        self.play(FadeOut(row), FadeOut(ones), FadeOut(tag), FadeOut(lines), FadeOut(indep))
        line, nums = axis(0, 15, 7.4, [-3.0, -2.6, 0])
        cases = [
            (3, 0.25, R"b(x;\, 3,\, \tfrac14)", "three items, p = 1/4",
             [R"\mu = 3\cdot\tfrac14 = 0.75", R"\sigma^2 = 3\cdot\tfrac14\cdot\tfrac34 = 0.5625"]),
            (15, 0.4, R"b(x;\, 15,\, 0.4)", "Example 5.2",
             [R"\mu = (15)(0.4) = 6", R"\sigma^2 = (15)(0.4)(0.6) = 3.6"]),
            (10, 0.3, R"b(x;\, 10,\, 0.3)", "Example 5.4",
             [R"\mu = (10)(0.3) = 3", R"\sigma^2 = (10)(0.3)(0.7) = 2.1"]),
        ]
        self.play(ShowCreation(line), FadeIn(nums))
        bars, ful, shown = None, None, None
        tracker = ValueTracker(0.75)
        for n, p, tex, src_text, eqs in cases:
            new = chart(line, range(16), binom_pmf(n, p, 15), 0.45, ACCENT, width=0.36, height=3.2)
            which = Tex(tex).scale(0.75).set_color(ACCENT).move_to([3.9, 0.9, 0])
            src = note(src_text, 22, GREY_B).next_to(which, DOWN, buff=0.2)
            col = column(eqs, src, scale=0.62, gap=0.35).align_to([2.3, 0, 0], LEFT)
            col.set_color(MEAN_COLOR)
            group = VGroup(which, src, col)
            if bars is None:
                bars = new
                self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.04), FadeIn(which), FadeIn(src))
                ful = pivot(line.n2p(n * p))
                ful.add_updater(lambda m: m.next_to(line.n2p(tracker.get_value()), DOWN, buff=0.44))
                self.play(FadeIn(ful), Write(col))
            else:
                self.play(FadeOut(shown), run_time=0.4)
                self.play(Transform(bars, new), tracker.animate.set_value(n * p), FadeIn(which), FadeIn(src), run_time=1.3)
                self.play(Write(col))
            shown = group
            self.wait(1.2)
        self.wait(0.8)


# ─────────────────────────────────────────────────────────────
# 4. 예제 5.5 평균 ± 2σ — 슬라이드 18 뒤 (풀이 19 앞)
# ─────────────────────────────────────────────────────────────
class Example55Chebyshev(InteractiveScene):
    """예제 5.2 의 분포(n = 15, p = 0.4)에 정리 5.1 을 쓴다. μ = 6, σ² = 3.6, σ = 1.897.
    μ ± 2σ = 2.206 ~ 9.794 를 띠로 덮고, 체비셰프 정리로 그 안의 확률이 3/4 이상임을 읽는다.
    값이 정수뿐이므로 2 에서 10 사이라고 해도 된다(덱의 문장)."""

    def construct(self):
        head = slide_title("Example 5.5")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        info = Tex(R"b(x;\, 15,\, 0.4)").scale(0.7).set_color(INK)
        info.next_to(head[1], DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        src = note("Example 5.2", 22, GREY_B).next_to(info, RIGHT, buff=0.4)
        self.play(FadeIn(info), FadeIn(src))

        steps, steps_box, focus = steps_panel(["1. mean and variance", "2. interval of 2 sigma",
                                               "3. Chebyshev bound"], pos=(4.55, 1.9, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        line, nums = axis(0, 15, 7.4, [-3.0, -2.6, 0])
        bars = chart(line, range(16), binom_pmf(15, 0.4), 0.21, ACCENT, width=0.36, height=2.6)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.05), run_time=1.0)

        # ── 1. 평균과 분산
        self.play(focus(0))
        c1 = column([R"\mu = np = (15)(0.4) = 6",
                     R"\sigma^2 = npq = (15)(0.4)(0.6) = 3.6",
                     R"\sigma = \sqrt{3.6} = 1.897"], steps_box, scale=0.55, gap=0.3).align_to([2.35, 0, 0], LEFT)
        ful = pivot(line.n2p(6))
        self.play(Write(c1[0]), FadeIn(ful))
        self.play(Write(c1[1]))
        self.play(Write(c1[2]))
        self.wait(0.8)

        # ── 2. 2σ 띠
        self.play(focus(1))
        c2 = column([R"\mu \pm 2\sigma = 6 \pm 2(1.897)", R"= 2.206\ \text{to}\ 9.794"],
                    c1, scale=0.55, gap=0.3).align_to(c1, LEFT)
        lo, hi = line.n2p(2.206), line.n2p(9.794)
        band = Rectangle(width=hi[0] - lo[0], height=3.0).set_fill(MEAN_COLOR, 0.18).set_stroke(MEAN_COLOR, 2)
        band.move_to([(lo[0] + hi[0]) / 2, lo[1], 0], aligned_edge=DOWN)
        ends = VGroup(Tex("2.206").scale(0.5).set_color(MEAN_COLOR).next_to(band.get_corner(UL), UP, buff=0.08),
                      Tex("9.794").scale(0.5).set_color(MEAN_COLOR).next_to(band.get_corner(UR), UP, buff=0.08))
        self.play(Write(c2[0]))
        self.play(FadeIn(band), FadeIn(ends), Write(c2[1]))
        self.wait(0.8)

        # ── 3. 체비셰프
        self.play(focus(2))
        c3 = column([R"P(\mu - 2\sigma < X < \mu + 2\sigma) \ge 1 - \tfrac{1}{2^2}",
                     R"P(2 \le X \le 10) \ge \tfrac34"], c2, scale=0.55, gap=0.3).align_to(c1, LEFT)
        c3[1].set_color(MEAN_COLOR)
        self.play(Write(c3[0]), run_time=1.2)
        self.play(*paint(bars, range(3, 10)))
        whole = note("whole numbers only", 22, GREY_B).next_to(c3[1], DOWN, buff=0.2).align_to(c1, LEFT)
        self.play(Write(c3[1]), FadeIn(whole))
        self.play(FlashAround(c3[1], color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 복원 · 비복원 추출과 초기하분포 — 슬라이드 25 (초기하 도입) 앞
# ─────────────────────────────────────────────────────────────
class SamplingWithoutReplacement(InteractiveScene):
    """이름: h(x; N, n, k). 같은 로트에서 뽑아도 되돌려 넣으면 성공 확률이 그대로라 이항분포이고,
    되돌려 넣지 않으면 뽑을 때마다 확률이 바뀌어 시행이 독립이 아니다(2/10 → 2/9 → 2/8).
    그래서 확률을 곱하지 않고 센다 — 성공 k 개에서 x 개, 실패 N − k 개에서 n − x 개, 전체는 C(N, n)."""

    def construct(self):
        head = slide_title("Hypergeometric Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"h(x;\, N,\, n,\, k)").scale(0.9).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.9)
        self.play(Write(name))

        chips = lot(2, 8)
        chips.move_to([-3.3, 1.85, 0])
        box = panel(chips, MUTED, buff=0.16)
        lot_tag = note("N items, k successes", 22, GREY_B).next_to(box, RIGHT, buff=0.35)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, chips, lag_ratio=0.05), FadeIn(lot_tag))
        self.wait(0.5)

        # ── 되돌려 넣는 추출: 확률이 그대로
        w_tag = label("with replacement", 26, ACCENT).move_to([-4.9, 0.55, 0])
        w_p = VGroup(*[Tex(R"\tfrac{2}{10}").scale(0.75).set_color(ACCENT) for _ in range(3)]).arrange(RIGHT, buff=0.9)
        w_p.next_to(w_tag, RIGHT, buff=0.8)
        w_end = label("same p, binomial", 24, GREY_B).next_to(w_p, RIGHT, buff=0.7)
        self.play(FadeIn(w_tag))
        for t in w_p:
            pick = chips[5].copy()
            self.play(pick.animate.next_to(t, UP, buff=0.12).scale(0.8), FadeIn(t), run_time=0.5)
            self.play(FadeOut(pick), run_time=0.25)
        self.play(FadeIn(w_end))
        self.wait(0.6)

        # ── 되돌려 넣지 않는 추출: 뽑을 때마다 분모가 준다
        o_tag = label("without replacement", 26, WARN).move_to([-4.9, -0.75, 0]).align_to(w_tag, LEFT)
        o_p = VGroup(*[Tex(R"\tfrac{2}{%d}" % d).scale(0.75).set_color(WARN) for d in (10, 9, 8)]).arrange(RIGHT, buff=0.9)
        o_p.align_to(w_p, LEFT).set_y(o_tag.get_y())
        o_end = label("p changes, not independent", 24, GREY_B).next_to(o_p, RIGHT, buff=0.7)
        self.play(FadeIn(o_tag))
        for t, gone in zip(o_p, (chips[9], chips[8], chips[7])):
            self.play(FadeIn(t), gone.animate.set_opacity(0.15), run_time=0.6)
        self.play(FadeIn(o_end))
        self.wait(1.0)

        # ── 그래서 센다
        self.play(FadeOut(VGroup(w_tag, w_p, w_end, o_tag, o_p, o_end)),
                  *[c.animate.set_opacity(1) for c in chips[7:]])
        num1 = Tex(R"\binom{k}{x}").scale(0.9).set_color(WARN)
        num2 = Tex(R"\binom{N-k}{n-x}").scale(0.9).set_color(ACCENT)
        top = VGroup(num1, num2).arrange(RIGHT, buff=0.12)
        den = Tex(R"\binom{N}{n}").scale(0.9).set_color(INK)
        rule = Line(LEFT, RIGHT).set_width(top.get_width() + 0.3).set_stroke(INK, 2)
        frac_g = VGroup(top, rule, den).arrange(DOWN, buff=0.14)
        lhs = Tex(R"h(x;\, N,\, n,\, k) =").scale(0.85).set_color(MEAN_COLOR)
        whole = VGroup(lhs, frac_g).arrange(RIGHT, buff=0.25).move_to([-2.4, -1.2, 0])
        tags = VGroup(Tex(R"x\ \text{of the}\ k\ \text{successes}").scale(0.6).set_color(WARN),
                      Tex(R"n - x\ \text{of the}\ N - k\ \text{failures}").scale(0.6).set_color(ACCENT),
                      note("all samples of size n", 22, INK))
        tags.arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(whole, RIGHT, buff=0.9)
        picked = VGroup(ring(chips[0], WARN, 0.05), ring(chips[3], ACCENT, 0.05), ring(chips[6], ACCENT, 0.05))
        self.play(ShowCreation(picked))
        self.play(Write(lhs), FadeIn(num1), FadeIn(tags[0]))
        self.wait(0.4)
        self.play(FadeIn(num2), FadeIn(tags[1]))
        self.wait(0.4)
        self.play(ShowCreation(rule), FadeIn(den), FadeIn(tags[2]))
        self.play(FlashAround(whole, color=MEAN_COLOR, buff=0.15))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 예제 5.8 합격판정 표본검사 — 슬라이드 26 뒤 (풀이 27 앞)
# ─────────────────────────────────────────────────────────────
class Example58Acceptance(InteractiveScene):
    """10 개 로트에 불량이 2 개(받아들일 수 없는 로트)라고 두고, 셋을 뽑아 불량이 없으면 합격시키는 계획을 따진다.
    불량이 없는 표본은 C(2,0)C(8,3) = 56, 전체는 C(10,3) = 120 이라 P(X = 0) = 0.467.
    나쁜 로트가 47 % 로 통과하므로 계획이 제 구실을 못 한다."""

    def construct(self):
        head = slide_title("Example 5.8")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        chips = lot(2, 8)
        chips.move_to([-3.5, 2.0, 0])
        box = panel(chips, MUTED, buff=0.16)
        rule = note("sample 3, accept if none defective", 22, INK).next_to(box, DOWN, buff=0.2)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, chips, lag_ratio=0.05))
        self.play(FadeIn(rule))

        steps, steps_box, focus = steps_panel(["1. assume 2 defectives", "2. samples with none",
                                               "3. all samples of 3", "4. judge the plan"], pos=(4.55, 1.75, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 불량이 둘인 로트
        self.play(focus(0))
        bad = VGroup(ring(chips[0], WARN, 0.05), ring(chips[1], WARN, 0.05))
        given = Tex(R"N = 10,\quad k = 2,\quad n = 3").scale(0.65).set_color(INK).move_to([-3.5, 0.55, 0])
        self.play(ShowCreation(bad), FadeIn(given))
        self.wait(0.6)

        # ── 2. 불량이 없는 표본: 양품 8 에서 3
        self.play(focus(1), FadeOut(bad))
        good = VGroup(*[ring(c, ACCENT, 0.05) for c in (chips[3], chips[6], chips[8])])
        c1 = column([R"\binom{2}{0}\binom{8}{3} = 1\cdot 56 = 56"], given, scale=0.66, gap=0.4).align_to([-5.9, 0, 0], LEFT)
        self.play(ShowCreation(good), Write(c1[0]))
        self.wait(0.7)

        # ── 3. 전체 표본
        self.play(focus(2), FadeOut(good))
        c2 = column([R"\binom{10}{3} = 120"], c1, scale=0.66, gap=0.3).align_to(c1, LEFT)
        self.play(Write(c2[0]))
        ans = column([R"P(X = 0) = \tfrac{56}{120} = 0.467"], c2, scale=0.7, gap=0.35).align_to(c1, LEFT)
        ans.set_color(MEAN_COLOR)
        self.play(Write(ans[0]))
        self.play(FlashAround(ans[0], color=MEAN_COLOR, buff=0.1))
        self.wait(0.8)

        # ── 4. 판정: 나쁜 로트가 절반 가까이 통과
        self.play(focus(3))
        line, nums = axis(0, 2, 2.6, [3.6, -2.75, 0])
        fs = hyper_pmf(10, 3, 2)
        bars = chart(line, range(3), fs, 0.5, ACCENT, width=0.6, height=2.3)
        xname = Tex(R"x\ \text{defectives in sample}").scale(0.5).set_color(GREY_B).next_to(nums, DOWN, buff=0.12)
        self.play(ShowCreation(line), FadeIn(nums), FadeIn(xname))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.15))
        self.play(*paint(bars, [0], WARN))
        verdict = label("bad lot accepted 47% of the time", 22, WARN).next_to(xname, DOWN, buff=0.15)
        self.play(FadeIn(verdict))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 예제 5.12 이항분포로 근사 — 슬라이드 37 뒤 (풀이 38 앞)
# ─────────────────────────────────────────────────────────────
class Example512BinomialApproximation(InteractiveScene):
    """N = 5000 중 흠 있는 타이어 k = 1000, n = 10 개를 산다. n/N = 0.002 로 0.05 보다 훨씬 작아
    한 개를 빼도 확률이 0.2000 → 0.1998 로 거의 그대로다. p = k/N = 0.2 인 이항분포로 보고
    표 A.1 에서 b(3; 10, 0.2) = 0.8791 − 0.6778 = 0.2013. 정확한 초기하 값 0.2015 를 겹쳐 본다."""

    def construct(self):
        head = slide_title("Example 5.12")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        info = Tex(R"N = 5000,\quad k = 1000,\quad n = 10,\quad x = 3").scale(0.65).set_color(INK)
        info.next_to(head[1], DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(info))

        steps, steps_box, focus = steps_panel(["1. check n / N", "2. binomial, p = k / N",
                                               "3. Table A.1 difference", "4. exact value"], pos=(4.55, 1.75, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. n 이 N 에 견주어 작은가
        self.play(focus(0))
        c1 = column([R"\tfrac{n}{N} = \tfrac{10}{5000} = 0.002 \le 0.05",
                     R"\tfrac{1000}{5000} = 0.2000,\quad \tfrac{999}{4999} = 0.1998"],
                    info, scale=0.6, gap=0.4).align_to(info, LEFT)
        self.play(Write(c1[0]))
        draws = note("first draw, second draw", 22, GREY_B).next_to(c1[1], RIGHT, buff=0.35)
        self.play(Write(c1[1]), FadeIn(draws))
        self.wait(1.0)

        # ── 2. 이항분포로
        self.play(focus(1))
        line, nums = axis(0, 10, 5.6, [-3.6, -2.75, 0])
        fb = binom_pmf(10, 0.2)
        bars = chart(line, range(11), fb, 0.32, ACCENT, width=0.38, height=2.3)
        which = Tex(R"b(x;\, 10,\, 0.2)").scale(0.65).set_color(ACCENT).next_to(line.n2p(8), UP, buff=1.6)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.06), FadeIn(which))
        self.wait(0.6)

        # ── 3. 표 A.1 의 차
        self.play(focus(2))
        c3 = column([R"b(3;\, 10,\, 0.2) = B(3) - B(2)", R"= 0.8791 - 0.6778 = 0.2013"],
                    steps_box, scale=0.55, gap=0.3).align_to([2.35, 0, 0], LEFT)
        self.play(*paint(bars, range(0, 4)), Write(c3[0]))
        self.wait(0.3)
        self.play(*paint(bars, [3]))
        self.play(Write(c3[1]))
        self.wait(0.8)

        # ── 4. 정확한 값: 초기하 막대를 겹친다
        self.play(focus(3))
        fh = hyper_pmf(5000, 10, 1000, 10)
        over = outline(line, range(11), fh, 0.32, WHITE, width=0.38, height=2.3)
        c4 = column([R"h(3;\, 5000,\, 10,\, 1000) = 0.2015"], c3, scale=0.55, gap=0.35).align_to(c3, LEFT)
        c4.set_color(MEAN_COLOR)
        tag = note("hypergeometric outline", 22, WHITE).next_to(which, DOWN, buff=0.15)
        self.play(LaggedStartMap(ShowCreation, over, lag_ratio=0.05), FadeIn(tag), run_time=1.2)
        self.play(Write(c4[0]))
        self.play(FlashAround(VGroup(c3[1], c4[0]), color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 음이항분포 — 슬라이드 42 (음이항분포 정의) 앞
# ─────────────────────────────────────────────────────────────
class NegativeBinomialWaiting(InteractiveScene):
    """이름: b*(x; k, p). 이항은 시행 수 n 을 고정하고 성공 수를 세지만, 음이항은 성공 수 k 를 고정하고
    시행 수 X 를 센다. k 번째 성공이 x 번째 시행에 나오려면 마지막 시행은 성공이고, 앞 x − 1 번 가운데
    k − 1 번이 성공이면 된다 — C(x−1, k−1) 가지, 한 가지의 확률은 p^k q^(x−k)."""

    def construct(self):
        head = slide_title("Negative Binomial Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"b^{*}(x;\, k,\, p)").scale(0.9).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.9)
        self.play(Write(name))

        two = VGroup(label("binomial: trials fixed, count successes", 24, GREY_B),
                     label("negative binomial: successes fixed, count trials", 24, INK))
        two.arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head[1], DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(two[0]))
        self.play(FadeIn(two[1]))
        self.wait(0.8)

        # ── x = 6 번째 시행에 k = 4 번째 성공
        patterns = ["SSFSFS", "FSSSFS", "SFSFSS"]
        row = trials(patterns[0], 0.6, buff=0.14).move_to([-3.2, -0.25, 0])
        nums = VGroup(*[Tex(str(i + 1)).scale(0.5).set_color(GREY_B).next_to(c, DOWN, buff=0.12)
                        for i, c in enumerate(row)])
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1), FadeIn(nums))
        last = ring(row[5], MEAN_COLOR, 0.07)
        last_tag = note("k-th success, trial x", 22, MEAN_COLOR).next_to(last, RIGHT, buff=0.35)
        self.play(ShowCreation(last), FadeIn(last_tag))
        self.wait(0.6)

        brace = Brace(VGroup(*row[:5]), UP, buff=0.12).set_color(CALM)
        ways = Tex(R"\binom{x-1}{k-1}").scale(0.7).set_color(CALM).next_to(brace, UP, buff=0.12)
        ways_tag = note("k - 1 successes before", 22, CALM).next_to(ways, RIGHT, buff=0.3)
        self.play(GrowFromCenter(brace), FadeIn(ways), FadeIn(ways_tag))
        for pat in patterns[1:]:
            new = trials(pat, 0.6, buff=0.14).move_to(row)
            self.play(*[FadeTransform(row[i], new[i]) for i in range(5)], run_time=0.7)
            row = VGroup(*new[:5], row[5])
            self.wait(0.35)
        count = Tex(R"\binom{5}{3} = 10").scale(0.65).set_color(CALM).next_to(ways_tag, RIGHT, buff=0.4)
        self.play(FadeIn(count))
        self.wait(0.6)

        each = Tex(R"p^{k} q^{\,x-k}").scale(0.75).set_color(INK).next_to(nums, DOWN, buff=0.4)
        each_tag = note("each arrangement", 22, GREY_B).next_to(each, RIGHT, buff=0.3)
        self.play(FadeIn(each), FadeIn(each_tag))
        self.wait(0.6)

        # ── 조립
        formula = Tex(R"b^{*}(x;\, k,\, p) = \binom{x-1}{k-1}\, p^{k} q^{\,x-k},\quad x = k,\ k+1,\ \ldots")
        formula.scale(0.75).set_color(MEAN_COLOR).move_to([0, -2.75, 0])
        self.play(Write(formula), run_time=1.4)
        self.play(FlashAround(formula, color=MEAN_COLOR, buff=0.12))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 예제 5.14 7전 4선승 — 슬라이드 43 뒤 (풀이 44 앞)
# ─────────────────────────────────────────────────────────────
class Example514Playoffs(InteractiveScene):
    """A 팀이 한 경기를 이길 확률 p = 0.55. (a) 6차전에서 우승 = 4 번째 승리가 6 번째 경기:
    C(5,3)(0.55)⁴(0.45)² = 0.1853. (b) 우승 = 4 · 5 · 6 · 7 차전 어느 것에서든:
    0.0915 + 0.1647 + 0.1853 + 0.1668 = 0.6083. (c) 5전 3선승이면 0.1664 + 0.2246 + 0.2021 = 0.5931."""

    def construct(self):
        head = slide_title("Example 5.14")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        info = Tex(R"p = 0.55,\quad q = 0.45").scale(0.7).set_color(INK)
        info.next_to(head[1], DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        who = note("W = team A wins", 22, GREY_B).next_to(info, RIGHT, buff=0.4)
        self.play(FadeIn(info), FadeIn(who))

        steps, steps_box, focus = steps_panel(["1. win in 6 games", "2. win the series",
                                               "3. best of five"], pos=(4.7, 1.9, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 1. 6차전 우승
        self.play(focus(0))
        row = trials("WLWWLW", 0.55, good="W", buff=0.12).move_to([-3.6, 1.2, 0])
        last = ring(row[5], MEAN_COLOR, 0.06)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.08))
        self.play(ShowCreation(last))
        a = column([R"b^{*}(6;\, 4,\, 0.55) = \binom{5}{3}(0.55)^4(0.45)^2", R"= 0.1853"],
                   row, scale=0.6, gap=0.3).align_to(info, LEFT)
        a[1].set_color(MEAN_COLOR)
        self.play(Write(a[0]), run_time=1.2)
        self.play(Write(a[1]))
        self.wait(0.9)

        # ── 2. 시리즈 우승: x = 4, 5, 6, 7
        self.play(focus(1), FadeOut(row), FadeOut(last), FadeOut(a))
        line, nums = axis(3, 7, 4.6, [-3.6, -2.75, 0])
        xname = Tex(R"x = \text{game that ends the series}").scale(0.5).set_color(GREY_B).next_to(nums, DOWN, buff=0.12)
        f7 = negbin_pmf(4, 0.55, range(3, 8))
        bars = chart(line, range(3, 8), f7, 0.25, ACCENT, width=0.6, height=2.5)
        vals = ["", "0.0915", "0.1647", "0.1853", "0.1668"]
        tags = VGroup(*[Tex(v).scale(0.5).set_color(INK).next_to(b, UP, buff=0.08) for v, b in zip(vals, bars) if v])
        self.play(ShowCreation(line), FadeIn(nums), FadeIn(xname))
        self.play(LaggedStartMap(GrowFromEdge, VGroup(*bars[1:]), edge=DOWN, lag_ratio=0.15), FadeIn(tags))
        b_col = column([R"b^{*}(4) + b^{*}(5) + b^{*}(6) + b^{*}(7)",
                        R"= 0.0915 + 0.1647 + 0.1853 + 0.1668", R"= 0.6083"],
                       steps_box, scale=0.52, gap=0.3).align_to([2.3, 0, 0], LEFT)
        b_col[2].set_color(MEAN_COLOR)
        self.play(Write(b_col[0]))
        self.play(Write(b_col[1]), run_time=1.2)
        self.play(Write(b_col[2]))
        self.play(FlashAround(b_col[2], color=MEAN_COLOR, buff=0.1))
        self.wait(1.0)

        # ── 3. 5전 3선승: k = 3, x = 3, 4, 5
        self.play(focus(2))
        f5 = negbin_pmf(3, 0.55, range(3, 6)) + [0.0, 0.0]          # 5차전까지만 있다
        new = chart(line, range(3, 8), f5, 0.25, CALM, width=0.6, height=2.5)
        vals5 = ["0.1664", "0.2246", "0.2021"]
        tags5 = VGroup(*[Tex(v).scale(0.5).set_color(INK).next_to(b, UP, buff=0.08) for v, b in zip(vals5, new)])
        self.play(FadeOut(tags), run_time=0.3)
        self.play(Transform(bars, new), FadeIn(tags5), run_time=1.2)
        c_col = column([R"k = 3:\quad 0.1664 + 0.2246 + 0.2021", R"= 0.5931"],
                       b_col, scale=0.52, gap=0.35).align_to(b_col, LEFT)
        c_col[1].set_color(MEAN_COLOR)
        self.play(Write(c_col[0]), run_time=1.2)
        self.play(Write(c_col[1]))
        self.play(FlashAround(c_col[1], color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 기하분포 — 슬라이드 45 (기하분포 정의 · 정리 5.3) 앞
# ─────────────────────────────────────────────────────────────
class GeometricFirstSuccess(InteractiveScene):
    """이름: g(x; p). 음이항에서 k = 1 로 두면 C(x−1, 0) = 1 이라 식이 p·q^(x−1) 만 남는다 —
    실패 x − 1 번 뒤에 첫 성공. 막대는 q 배씩 줄어든다. 평균은 1/p (정리 5.3): 예제 5.16 의 p = 0.05 이면
    평균 20 번째 시도에 연결된다."""

    def construct(self):
        head = slide_title("Geometric Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"g(x;\, p)").scale(0.9).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.9)
        self.play(Write(name))

        row = trials("FFFFS", 0.6, buff=0.14).move_to([-4.0, 1.6, 0])
        first = ring(row[4], MEAN_COLOR, 0.07)
        tag = note("first success on trial x", 22, GREY_B).next_to(row, RIGHT, buff=0.5)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1), FadeIn(tag))
        self.play(ShowCreation(first))
        under_row = VGroup(*[Tex("q" if i < 4 else "p").scale(0.65).set_color(WARN if i < 4 else ACCENT)
                             .next_to(c, DOWN, buff=0.14) for i, c in enumerate(row)])
        self.play(LaggedStartMap(FadeIn, under_row, lag_ratio=0.1))
        self.wait(0.5)

        col = column([R"b^{*}(x;\, 1,\, p) = \binom{x-1}{0}\, p\, q^{\,x-1}", R"g(x;\, p) = p\, q^{\,x-1},\quad x = 1,\ 2,\ 3,\ \ldots"],
                     under_row, scale=0.65, gap=0.4).align_to(row, LEFT)
        col[1].set_color(MEAN_COLOR)
        k1 = note("negative binomial, k = 1", 22, GREY_B).next_to(col[0], RIGHT, buff=0.4)
        self.play(Write(col[0]), FadeIn(k1))
        self.play(Write(col[1]))
        self.wait(1.0)

        # ── 막대: 예제 5.16 의 p = 0.05
        line, _ = axis(1, 40, 8.2, [-2.6, -3.0, 0])
        nums = VGroup(*[Tex(str(x)).scale(0.42).set_color(GREY_B).next_to(line.n2p(x), DOWN, buff=0.16)
                        for x in (1, 5, 10, 15, 20, 25, 30, 35, 40)])
        fs = [0.05 * 0.95 ** (x - 1) for x in range(1, 41)]
        bars = chart(line, range(1, 41), fs, 0.05, ACCENT, width=0.15, height=1.5)
        src = note("Example 5.16, p = 0.05", 22, GREY_B).next_to(line.n2p(30), UP, buff=1.35)
        self.play(ShowCreation(line), FadeIn(nums), FadeIn(src))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.02), run_time=1.4)
        ratio = note("ratio q between bars", 22, CALM).next_to(src, DOWN, buff=0.15)
        self.play(FadeIn(ratio))
        self.wait(0.6)

        ful = pivot(line.n2p(20))
        thm = column([R"\mu = \tfrac{1}{p} = \tfrac{1}{0.05} = 20", R"\sigma^2 = \tfrac{1-p}{p^2} = \tfrac{0.95}{0.0025} = 380"],
                     name, scale=0.6, gap=0.5).align_to([3.1, 0, 0], LEFT)
        thm.set_color(MEAN_COLOR)
        t53 = note("Theorem 5.3", 22, GREY_B).next_to(thm, UP, buff=0.15).align_to(thm, LEFT)
        self.play(FadeIn(ful), FadeIn(t53), Write(thm[0]))
        self.play(Write(thm[1]))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 포아송분포 — 슬라이드 51 (포아송분포 정의 · 표 A.2) 앞
# ─────────────────────────────────────────────────────────────
class PoissonCounts(InteractiveScene):
    """이름: p(x; λt). 시간(또는 영역) 위에 흩어진 사건을 길이 t 의 구간으로 떠서 그 안의 개수 X 를 센다.
    λ 는 단위 구간의 평균 발생 수이고, 구간 길이를 곱한 λt 가 평균이자 분산이다(정리 5.4).
    슬라이드 55 의 세 그림 — μ = 0.1 · 2 · 5 — 을 차례로 세워, μ 가 커지면 종 모양에 가까워짐을 본다."""

    def construct(self):
        head = slide_title("Poisson Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"p(x;\, \lambda t) = \frac{e^{-\lambda t}(\lambda t)^{x}}{x!}").scale(0.8).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.7)
        self.play(Write(name))

        # ── 흩어진 사건과 구간
        rng = np.random.default_rng(5)
        tline = Line([-6.2, 1.2, 0], [1.6, 1.2, 0]).set_stroke(GREY_B, 2)
        xs = np.sort(rng.uniform(-6.0, 1.4, 14))
        dots = VGroup(*[Dot([x, 1.2, 0], radius=0.07).set_fill(ACCENT, 1) for x in xs])
        tl_tag = note("time or region", 22, GREY_B).next_to(tline, UP, buff=0.5).align_to(tline, LEFT)
        self.play(ShowCreation(tline), FadeIn(tl_tag))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.08, scale=0.5), run_time=1.2)

        width = 2.4
        tracker = ValueTracker(-5.8)
        window = Rectangle(width=width, height=0.7).set_stroke(MEAN_COLOR, 3).set_fill(MEAN_COLOR, 0.12)
        window.add_updater(lambda m: m.move_to([tracker.get_value() + width / 2, 1.2, 0]))
        t_tag = Tex("t").scale(0.7).set_color(MEAN_COLOR)
        t_tag.add_updater(lambda m: m.next_to(window, DOWN, buff=0.1))
        count = Integer(0).scale(0.9).set_color(MEAN_COLOR)
        count.add_updater(lambda m: m.set_value(int(sum(tracker.get_value() <= x <= tracker.get_value() + width for x in xs))))
        x_tag = Tex("X =").scale(0.8).set_color(MEAN_COLOR).move_to([-5.6, 0.0, 0])
        count.next_to(x_tag, RIGHT, buff=0.2)
        cnt_tag = note("outcomes in the interval", 22, GREY_B).next_to(count, RIGHT, buff=0.5)
        self.play(FadeIn(window), FadeIn(t_tag), FadeIn(x_tag), FadeIn(count), FadeIn(cnt_tag))
        self.play(tracker.animate.set_value(-1.2), run_time=3.0, rate_func=linear)
        self.wait(0.4)
        rate = Tex(R"\lambda = \text{average per unit},\qquad \lambda t = \text{average in the interval}")
        rate.scale(0.6).set_color(INK).move_to([-2.3, -0.8, 0])
        self.play(Write(rate), run_time=1.4)
        self.wait(1.0)

        # ── 모양: μ = 0.1, 2, 5
        for m in (window, t_tag, count):
            m.clear_updaters()
        self.play(FadeOut(VGroup(tline, dots, tl_tag, window, t_tag, x_tag, count, cnt_tag, rate)))
        line, nums = axis(0, 10, 6.6, [-3.2, -2.7, 0])
        self.play(ShowCreation(line), FadeIn(nums))
        cases = [(0.1, 1.0), (2, 0.3), (5, 0.3)]
        bars, shown, ful = None, None, None
        mu_t = ValueTracker(0.1)
        for mu, vmax in cases:
            new = chart(line, range(11), poisson_pmf(mu, 10), vmax, ACCENT, width=0.42, height=2.9)
            tag = Tex(R"\mu = \sigma^2 = \lambda t = %s" % mu).scale(0.75).set_color(MEAN_COLOR).move_to([3.8, 0.2, 0])
            if bars is None:
                bars = new
                self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.05), FadeIn(tag))
                ful = pivot(line.n2p(mu))
                ful.add_updater(lambda m: m.next_to(line.n2p(mu_t.get_value()), DOWN, buff=0.44))
                self.play(FadeIn(ful))
                t54 = note("Theorem 5.4", 22, GREY_B).next_to(tag, UP, buff=0.2)
                self.play(FadeIn(t54))
            else:
                self.play(FadeOut(shown), run_time=0.3)
                self.play(Transform(bars, new), mu_t.animate.set_value(mu), FadeIn(tag), run_time=1.4)
            shown = tag
            self.wait(1.1)
        shape = note("larger mean, more symmetric", 22, CALM).next_to(shown, DOWN, buff=0.3)
        self.play(FadeIn(shape))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 이항분포의 포아송 극한 — 슬라이드 52 (정리 5.4 · 5.5) 앞
# ─────────────────────────────────────────────────────────────
class BinomialToPoisson(InteractiveScene):
    """정리 5.5: n → ∞, p → 0 이고 np = μ 가 그대로이면 b(x; n, p) → p(x; μ).
    μ = 2 의 포아송을 빈 막대로 세워 두고 이항 막대를 n = 4 · 10 · 40 · 400 으로 바꿔 가며 겹친다.
    마지막 n = 400, p = 0.005 는 예제 5.19 의 값이다."""

    def construct(self):
        head = slide_title("Poisson Limit of the Binomial")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        name = Tex(R"b(x;\, n,\, p) \to p(x;\, \mu)").scale(0.85).set_color(MEAN_COLOR)
        name.next_to(head[1], DOWN, buff=0.3).to_edge(RIGHT, buff=0.8)
        cond = Tex(R"n \to \infty,\quad p \to 0,\quad np = \mu").scale(0.65).set_color(INK)
        cond.next_to(name, DOWN, buff=0.25).align_to(name, RIGHT)
        self.play(Write(name))
        self.play(FadeIn(cond))
        t55 = note("Theorem 5.5", 22, GREY_B).next_to(cond, DOWN, buff=0.2).align_to(name, RIGHT)
        self.play(FadeIn(t55))

        line, nums = axis(0, 8, 6.4, [-3.2, -2.7, 0])
        target = outline(line, range(9), poisson_pmf(2, 8), 0.4, MEAN_COLOR, width=0.5, height=3.6)
        t_tag = Tex(R"p(x;\, 2)").scale(0.65).set_color(MEAN_COLOR).next_to(line.n2p(7), UP, buff=1.2)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(LaggedStartMap(ShowCreation, target, lag_ratio=0.06), FadeIn(t_tag), run_time=1.2)
        self.wait(0.6)

        cases = [(4, "0.5"), (10, "0.2"), (40, "0.05"), (400, "0.005")]
        bars, shown = None, None
        for n, p_text in cases:
            p = float(p_text)
            new = chart(line, range(9), binom_pmf(n, p, 8), 0.4, ACCENT, width=0.42, height=3.6, opacity=0.75)
            info = VGroup(Tex(R"n = %d,\quad p = %s" % (n, p_text)).scale(0.75).set_color(ACCENT),
                          Tex(R"np = 2").scale(0.75).set_color(INK))
            info.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.9, -0.6, 0])
            if bars is None:
                bars = new
                self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.06), FadeIn(info))
            else:
                self.play(FadeOut(shown), run_time=0.3)
                self.play(Transform(bars, new), FadeIn(info), run_time=1.3)
            self.add(target)
            shown = info
            self.wait(1.0)
        src = note("Example 5.19", 22, GREY_B).next_to(shown, DOWN, buff=0.25).align_to(shown, LEFT)
        approx = Tex(R"b(x;\, 400,\, 0.005) \approx p(x;\, 2)").scale(0.65).set_color(MEAN_COLOR)
        approx.next_to(src, DOWN, buff=0.25).align_to(shown, LEFT)
        self.play(FadeIn(src), Write(approx))
        self.play(FlashAround(approx, color=MEAN_COLOR, buff=0.1))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13. 예제 5.17 · 5.18 표 A.2 읽기 — 슬라이드 56 뒤 (풀이 57 앞)
# ─────────────────────────────────────────────────────────────
class Example517518Table(InteractiveScene):
    """표 A.2 도 누적합 P(r; λt) 다. 5.17: 평균 4, x = 6 → P(6; 4) − P(5; 4) = 0.8893 − 0.7851 = 0.1042.
    5.18: 평균 10, 15 척을 넘는 날 → 1 − P(15; 10) = 1 − 0.9513 = 0.0487. 표 A.1 과 같은 읽기다."""

    def construct(self):
        head = slide_title("Examples 5.17, 5.18")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        cum = Tex(R"P(r;\, \lambda t) = \sum_{x=0}^{r} p(x;\, \lambda t)").scale(0.62).set_color(MEAN_COLOR)
        cum.next_to(head[1], DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        src = note("Table A.2", 22, GREY_B).next_to(cum, RIGHT, buff=0.35)
        self.play(Write(cum), FadeIn(src))

        steps, steps_box, focus = steps_panel(["1. mean 4, x = 6", "2. difference of two sums",
                                               "3. mean 10, over 15", "4. complement of a sum"],
                                              pos=(4.5, 1.75, 0), size=22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.6)

        # ── 5.17
        self.play(focus(0))
        line, nums = axis(0, 12, 6.6, [-3.3, -2.75, 0])
        bars = chart(line, range(13), poisson_pmf(4, 12), 0.2, ACCENT, width=0.4, height=2.6)
        which = Tex(R"p(x;\, 4)").scale(0.65).set_color(ACCENT).next_to(line.n2p(10), UP, buff=1.5)
        ex = note("particles per millisecond", 22, GREY_B).next_to(which, UP, buff=0.15)
        self.play(ShowCreation(line), FadeIn(nums))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.05), FadeIn(which), FadeIn(ex))
        self.wait(0.5)

        self.play(focus(1))
        c1 = column([R"p(6;\, 4) = P(6;\, 4) - P(5;\, 4)", R"= 0.8893 - 0.7851 = 0.1042"],
                    steps_box, scale=0.55, gap=0.3).align_to([2.35, 0, 0], LEFT)
        c1[1].set_color(MEAN_COLOR)
        self.play(*paint(bars, range(0, 7)), Write(c1[0]))
        self.wait(0.4)
        self.play(*paint(bars, [6]))
        self.play(Write(c1[1]))
        self.play(FlashAround(c1[1], color=MEAN_COLOR, buff=0.08))
        self.wait(1.0)

        # ── 5.18
        self.play(focus(2), FadeOut(VGroup(bars, which, ex, line, nums)))
        line2, _ = axis(0, 22, 6.8, [-3.2, -2.75, 0])
        nums2 = VGroup(*[Tex(str(x)).scale(0.45).set_color(GREY_B).next_to(line2.n2p(x), DOWN, buff=0.16)
                         for x in (0, 5, 10, 15, 20)])
        bars2 = chart(line2, range(23), poisson_pmf(10, 22), 0.13, ACCENT, width=0.24, height=2.6)
        which2 = Tex(R"p(x;\, 10)").scale(0.65).set_color(ACCENT).next_to(line2.n2p(3), UP, buff=1.5)
        ex2 = note("tankers per day", 22, GREY_B).next_to(which2, UP, buff=0.15)
        self.play(ShowCreation(line2), FadeIn(nums2))
        self.play(LaggedStartMap(GrowFromEdge, bars2, edge=DOWN, lag_ratio=0.03), FadeIn(which2), FadeIn(ex2))
        cap_x = (line2.n2p(15)[0] + line2.n2p(16)[0]) / 2
        cap = DashedLine([cap_x, -2.75, 0], [cap_x, 0.0, 0]).set_stroke(WARN, 2)
        cap_tag = note("capacity 15", 22, WARN).next_to(cap, UP, buff=0.1)
        self.play(ShowCreation(cap), FadeIn(cap_tag))
        self.wait(0.5)

        self.play(focus(3))
        c2 = column([R"P(X > 15) = 1 - P(15;\, 10)", R"= 1 - 0.9513 = 0.0487"],
                    c1, scale=0.55, gap=0.35).align_to(c1, LEFT)
        c2[1].set_color(MEAN_COLOR)
        self.play(*paint(bars2, range(0, 16)), Write(c2[0]))
        self.wait(0.4)
        self.play(*paint(bars2, range(16, 23), WARN))
        self.play(Write(c2[1]))
        self.play(FlashAround(c2[1], color=MEAN_COLOR, buff=0.08))
        self.wait(2)
