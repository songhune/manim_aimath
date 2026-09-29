# -*- coding: utf-8 -*-
"""기계학습기초 — k-최근접 이웃 회귀의 확률적 해석 (`[0922]Regression.pptx` SECTION 3-1 (4) ~ (14) 보조 영상 2편).

1편 `RandomVariableToVariance`: 확률변수 → 확률분포(pmf) → 기댓값 → 분산.
    치토 6마리의 "잡은 물고기 수" x = 1, 2, 2, 3, 3, 5 로 정의를 세운 뒤(1부), 농어 훈련 세트 42마리의
    무게 W 로 옮겨 경험분포·E[W]·σ_W 를 구한다(2부). 길이를 모를 때의 예측값이 E[W] 임을 마지막에 둔다.
2편 `ConditionalToKNN`: 조건부확률 → 조건부분포·조건부 기댓값 → 최소제곱 → k-최근접 이웃 회귀.
    같은 6마리를 낚싯대 크기 S(작음·큼)로 갈라 2원 표에서 조건부분포와 E[X | S] 를 세우고, 예측값 a 를
    움직여 조건부 기댓값이 제곱오차를 최소로 함을 본 뒤(1부), 농어에서 이웃 k 마리 = 조건부 표본,
    이웃 평균 = 예측, x 를 훑어 회귀 함수, 잔차와 조건부 분산 띠, k 의 영향, 평균·중앙값·분위수 곡선(2부).

정의의 낱말은 확률과통계 덱(PS1_02 정의 2.10, PS1_03 정의 3.1·3.4·3.11, PS1_04 정의 4.1·4.3)과 같다.

소재 규칙(하네스 3.8): 화면의 수치는 전부 여기서 계산한다. 농어 자료는 덱 6쪽의 56마리, 훈련 세트는 덱 8쪽의
`train_test_split(perch_length, perch_weight, random_state=42)` 와 같은 42마리다(numpy
`RandomState(42).permutation` 으로 같은 분할을 재현. sklearn 이 없는 환경에서도 돈다). 50cm 의 이웃이
44·43·43 이고 예측이 1033.33 인 것이 덱과 같다. 개체 아이콘은 치토(하네스 3.6).

긴 `self.wait()`(≥ 0.4초)가 클릭 진행형 페이지의 경계다(`_2026/aimath/slides_common.py`).

렌더 (저장소 루트에서):
    ./render.sh list  _2026/ml/ml_week04.py
    ./render.sh draft _2026/ml/ml_week04.py RandomVariableToVariance ConditionalToKNN
    ./render.sh video _2026/ml/ml_week04.py RandomVariableToVariance ConditionalToKNN
클릭 진행형 페이지:
    python tools/build_slides_site.py --chapter ml_03 --module _2026/ml/slides_ml_03.py
"""
import numpy as np

from manim_imports_ext import *
from _2026.probstat.ps_common import (
    INK, ACCENT, WARN, CALM, MUTED, MEAN_COLOR,
    chito, ring, label, note, slide_title,
)

# ─────────────────────────────────────────────────────────────
# 자료 — 덱 6쪽의 농어 56마리와 덱 8쪽의 훈련 세트 분할
# ─────────────────────────────────────────────────────────────
PERCH_LENGTH = np.array(
    [8.4, 13.7, 15.0, 16.2, 17.4, 18.0, 18.7, 19.0, 19.6, 20.0,
     21.0, 21.0, 21.0, 21.3, 22.0, 22.0, 22.0, 22.0, 22.0, 22.5,
     22.5, 22.7, 23.0, 23.5, 24.0, 24.0, 24.6, 25.0, 25.6, 26.5,
     27.3, 27.5, 27.5, 27.5, 28.0, 28.7, 30.0, 32.8, 34.5, 35.0,
     36.5, 36.0, 37.0, 37.0, 39.0, 39.0, 39.0, 40.0, 40.0, 40.0,
     40.0, 42.0, 43.0, 43.0, 43.5, 44.0])
PERCH_WEIGHT = np.array(
    [5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0,
     110.0, 115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0,
     130.0, 150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0,
     197.0, 218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0,
     514.0, 556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0,
     820.0, 850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0,
     1000.0, 1000.0])


def train_split(seed=42, test_ratio=0.25):
    """sklearn 의 train_test_split 과 같은 분할. 앞 ceil(n·0.25) 개가 테스트, 나머지가 훈련."""
    n = len(PERCH_LENGTH)
    n_test = int(np.ceil(n * test_ratio))
    perm = np.random.RandomState(seed).permutation(n)
    train = perm[n_test:]
    return PERCH_LENGTH[train], PERCH_WEIGHT[train]


TRAIN_L, TRAIN_W = train_split()
N = len(TRAIN_L)

# 1부의 작은 예: 치토 6마리가 잡은 물고기 수와 낚싯대 크기
TOY_X = np.array([1, 2, 2, 3, 3, 5])
TOY_S = np.array(["small", "small", "small", "large", "large", "large"])
TOY_TINT = {"small": "teal", "large": "red"}
TOY_COLOR = {"small": CALM, "large": WARN}
TOY_NAME = {"small": "작음", "large": "큼"}


def neighbors(length, k):
    """길이 length 에 가장 가까운 훈련 샘플 k 개의 인덱스. 거리가 같으면 앞의 것."""
    return np.argsort(np.abs(TRAIN_L - length), kind="stable")[:k]


def knn_predict(length, k):
    return float(TRAIN_W[neighbors(length, k)].mean())


def neighbor_sd(length, k):
    """k − 1 로 나눈 이웃 무게의 표본 표준편차. k = 1 이면 0."""
    if k < 2:
        return 0.0
    return float(TRAIN_W[neighbors(length, k)].std(ddof=1))


def neighbor_stat(length, k, stat):
    ys = TRAIN_W[neighbors(length, k)]
    if stat == "mean":
        return float(ys.mean())
    if stat == "median":
        return float(np.median(ys))
    return float(np.quantile(ys, 0.9))


def fmt(value, places=1):
    return ("%%.%df" % places) % value


# ─────────────────────────────────────────────────────────────
# 공통 그림 요소
# ─────────────────────────────────────────────────────────────
def perch_axes(width=8.6, height=4.6):
    axes = Axes(
        x_range=(0, 55, 10), y_range=(0, 1200, 200),
        width=width, height=height,
        axis_config=dict(stroke_width=2, include_tip=False),
    )
    axes.x_axis.add_numbers(range(10, 51, 10), font_size=20)
    axes.y_axis.add_numbers(range(200, 1201, 200), font_size=20)
    return axes


def axis_tags(axes):
    x_tag = note("길이 (cm)", 22).next_to(axes.x_axis, DOWN, buff=0.1)
    y_tag = note("무게 (g)", 22).next_to(axes.y_axis, UP, buff=0.1)
    return VGroup(x_tag, y_tag)


def train_dots(axes, color=ACCENT, radius=0.055):
    return VGroup(*[
        Dot(axes.c2p(l, w), radius=radius).set_fill(color, 0.9).set_stroke(width=0)
        for l, w in zip(TRAIN_L, TRAIN_W)
    ])


def knn_curve(axes, k, x_min=8.0, x_max=52.0, step=0.1):
    """k-최근접 이웃 회귀 함수. 이웃이 바뀌는 자리에서 계단이 생긴다."""
    xs = np.arange(x_min, x_max + 1e-9, step)
    pts = [axes.c2p(x, knn_predict(x, k)) for x in xs]
    return VMobject().set_points_as_corners(pts).set_stroke(MEAN_COLOR, 3)


def stat_curve(axes, k, stat, color, x_min=8.0, x_max=52.0, step=0.1):
    xs = np.arange(x_min, x_max + 1e-9, step)
    pts = [axes.c2p(x, neighbor_stat(x, k, stat)) for x in xs]
    return VMobject().set_points_as_corners(pts).set_stroke(color, 3)


def stacked_dots(line, values, bin_w, radius, color, base=0.14):
    """수직선 위의 점그림. 가까운 값은 위로 쌓는다. 점마다 src_index 에 원래 자리를 적어 둔다."""
    dots = VGroup()
    levels = {}
    for i in np.argsort(values, kind="stable"):
        b = int(values[i] // bin_w)
        lv = levels.get(b, 0)
        levels[b] = lv + 1
        d = Dot(line.n2p(values[i]) + UP * (base + lv * 2 * radius), radius=radius)
        d.set_fill(color, 0.95).set_stroke(width=0)
        d.src_index = int(i)
        dots.add(d)
    return dots


def toy_crowd(height=0.62):
    """치토 6마리와 각자의 물고기 수. 낚싯대 크기(작음 teal · 큼 red)로 색을 가른다."""
    icons = Group(*[chito("front", TOY_TINT[s], height) for s in TOY_S])
    icons.arrange(RIGHT, buff=0.38)
    tags = VGroup(*[Tex(str(x), font_size=34).set_color(TOY_COLOR[s]).next_to(m, DOWN, buff=0.12)
                    for x, s, m in zip(TOY_X, TOY_S, icons)])
    return icons, tags


def bars_on(axes, values, probs, color, width=0.5):
    """pmf 막대. values 의 자리마다 높이 probs."""
    g = VGroup()
    for v, p in zip(values, probs):
        bar = Rectangle(width=width, height=max(axes.c2p(0, p)[1] - axes.c2p(0, 0)[1], 1e-3))
        bar.set_fill(color, 0.55).set_stroke(color, 1.5)
        bar.move_to(axes.c2p(v, 0), aligned_edge=DOWN)
        g.add(bar)
    return g


def frac_tex(num, den, font_size=28, color=INK):
    return Tex(R"\tfrac{%d}{%d}" % (num, den), font_size=font_size).set_color(color)


def balance_marker(point, color=MEAN_COLOR, height=0.24):
    tri = Triangle().set_fill(color, 1).set_stroke(width=0).set_height(height)
    return tri.move_to(point, aligned_edge=UP)


def deviation_squares(axes, values, probs, mu, unit, color=CALM):
    """값마다 |x − μ| 를 한 변으로 하는 정사각형. 넓이가 편차의 제곱이다."""
    g = VGroup()
    for v, p in zip(values, probs):
        side = abs(v - mu) * unit
        sq = Square(side_length=max(side, 1e-3)).set_fill(color, 0.3).set_stroke(color, 1.5)
        sq.move_to(axes.c2p(v, p), aligned_edge=DOWN).shift(UP * 0.05)
        g.add(sq)
    return g


class PartScene(InteractiveScene):
    """단(段)별 메서드로 나눈 씬. `clear_part` 로 앞 단의 그림을 걷는다."""

    def clear_part(self, *mobs, run_time=0.6):
        alive = [m for m in mobs if m is not None]
        if alive:
            self.play(*[FadeOut(m) for m in alive], run_time=run_time)


# ─────────────────────────────────────────────────────────────
class RandomVariableToVariance(PartScene):
    """1편. 확률변수 → pmf → 기댓값·분산을 작은 예로 세우고 농어 무게 W 로 옮긴다. 덱 (4) 「확률변수」 앞."""
    rows, cols = 6, 7
    icon_height = 0.36

    def construct(self):
        head = slide_title("확률변수·분포·기댓값·분산")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.part_random_variable()
        self.part_pmf()
        self.part_mean_variance()
        self.part_perch()
        self.part_bridge()

    # 1-1 확률변수: 표본공간의 원소마다 실수 하나
    def part_random_variable(self):
        icons, tags = toy_crowd()
        Group(icons, tags).move_to(UP * 1.6)
        box = SurroundingRectangle(Group(icons, tags), buff=0.25).set_stroke(MUTED, 2).round_corners(0.15)
        box_tag = label("표본공간 S: 치토 6마리", 26).next_to(box, UP, buff=0.2)
        self.play(LaggedStartMap(FadeIn, icons, lag_ratio=0.1), FadeIn(box), FadeIn(box_tag))
        self.wait(0.8)
        rv = VGroup(Tex(R"X", font_size=44), label("= 잡은 물고기 수", 28, MEAN_COLOR)).arrange(RIGHT, buff=0.2)
        rv[0].set_color(MEAN_COLOR)
        rv.next_to(box, DOWN, buff=0.35)
        self.play(LaggedStartMap(FadeIn, tags, lag_ratio=0.1), FadeIn(rv))
        self.wait(1.5)

        line = NumberLine(x_range=(0, 6, 1), width=7.0, include_numbers=True, font_size=24)
        line.move_to(DOWN * 2.2)
        line_tag = note("x", 26).next_to(line, RIGHT, buff=0.3)
        self.play(ShowCreation(line), FadeIn(line_tag))
        dots = stacked_dots(line, TOY_X.astype(float), 1.0, 0.09, ACCENT, base=0.18)
        self.play(*[TransformFromCopy(tags[d.src_index], d) for d in dots], run_time=1.2)
        def_tag = label("확률변수: 원소 → 실수 하나", 26).next_to(line, UP, buff=1.1).align_to(line, LEFT)
        self.play(FadeIn(def_tag))
        self.wait(1.5)
        self.toy = Group(icons, tags, box, box_tag, rv)
        self.line, self.dots, self.def_tag, self.line_tag = line, dots, def_tag, line_tag

    # 1-2 확률분포: 값마다 확률, 합은 1
    def part_pmf(self):
        self.clear_part(self.toy, self.def_tag, self.line_tag)
        axes = Axes(x_range=(0, 6, 1), y_range=(0, 1, 0.5), width=7.0, height=3.2,
                    axis_config=dict(stroke_width=2, include_tip=False))
        axes.to_edge(LEFT, buff=0.8).shift(DOWN * 0.5)
        axes.x_axis.add_numbers(range(1, 6), font_size=24)
        axes.y_axis.add_numbers([0.5, 1.0], font_size=22, num_decimal_places=1)
        values = [1, 2, 3, 5]
        counts = [int((TOY_X == v).sum()) for v in values]
        probs = [c / len(TOY_X) for c in counts]
        bars = bars_on(axes, values, probs, ACCENT)
        fracs = VGroup(*[frac_tex(c, 6).next_to(b, UP, buff=0.08) for c, b in zip(counts, bars)])
        self.play(ReplacementTransform(self.line, axes.x_axis), ShowCreation(axes.y_axis))
        self.play(*[FadeOut(d) for d in self.dots], LaggedStartMap(FadeIn, bars, lag_ratio=0.15), run_time=1.0)
        self.play(LaggedStartMap(FadeIn, fracs, lag_ratio=0.15))
        pmf_tag = Tex(R"f(x) = P(X = x)", font_size=36).set_color(INK).move_to(RIGHT * 4.2 + UP * 2.0)
        self.play(FadeIn(pmf_tag))
        self.wait(1.2)

        stack = VGroup()
        y = 0.0
        for c, b in zip(counts, bars):
            piece = b.copy()
            piece.set_height(axes.c2p(0, c / 6)[1] - axes.c2p(0, 0)[1], stretch=True)
            piece.move_to(axes.c2p(6.6, y), aligned_edge=DOWN).shift(RIGHT * 0.8)
            stack.add(piece)
            y += c / 6
        one = DashedLine(axes.c2p(0, 1), stack[-1].get_top() + RIGHT * 0.4).set_stroke(MEAN_COLOR, 2)
        conds = VGroup(
            Tex(R"f(x) \geq 0", font_size=32),
            Tex(R"\textstyle\sum_x f(x) = 1", font_size=32),
            Tex(R"P(X = x) = f(x)", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).set_color(INK)
        conds.next_to(pmf_tag, DOWN, buff=0.5).align_to(pmf_tag, LEFT)
        self.play(*[TransformFromCopy(b, p) for b, p in zip(bars, stack)], run_time=1.2)
        self.play(ShowCreation(one), FadeIn(conds))
        self.wait(1.5)
        self.axes, self.bars, self.fracs = axes, bars, fracs
        self.pmf_group = VGroup(pmf_tag, conds, stack, one)
        self.values, self.probs = values, probs

    # 1-3 기댓값과 분산: 균형점과 편차 제곱의 평균
    def part_mean_variance(self):
        axes, values, probs = self.axes, self.values, self.probs
        self.clear_part(self.pmf_group)
        mu = float(np.dot(values, probs))
        tri = balance_marker(axes.c2p(mu, 0) + DOWN * 0.05)
        mu_tex = Tex(R"\mu = E[X] = \textstyle\sum_x x f(x) = %s" % fmt(mu, 2), font_size=34).set_color(MEAN_COLOR)
        mu_tex.move_to(RIGHT * 4.0 + UP * 2.0)
        mu_note = label("균형점", 24, MEAN_COLOR).next_to(tri, DOWN, buff=0.3)
        self.play(FadeIn(tri), FadeIn(mu_note), FadeIn(mu_tex))
        self.wait(1.2)

        squares = deviation_squares(axes, values, probs, mu, 0.45)
        dev_tex = Tex(R"(x - \mu)^2", font_size=30).set_color(CALM).next_to(mu_tex, DOWN, buff=0.4).align_to(mu_tex, LEFT)
        self.play(LaggedStartMap(FadeIn, squares, lag_ratio=0.15), FadeIn(dev_tex))
        var = float(np.dot([(v - mu) ** 2 for v in values], probs))
        var_tex = Tex(R"\sigma^2 = \textstyle\sum_x (x-\mu)^2 f(x) = %s" % fmt(var, 2), font_size=32).set_color(CALM)
        sd_tex = Tex(R"\sigma = \sqrt{\sigma^2} = %s" % fmt(np.sqrt(var), 2), font_size=32).set_color(CALM)
        VGroup(var_tex, sd_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(dev_tex, DOWN, buff=0.3).align_to(dev_tex, LEFT)
        self.play(FadeIn(var_tex))
        self.play(FadeIn(sd_tex))
        self.wait(1.5)
        self.concept_group = VGroup(axes, self.bars, self.fracs, tri, mu_note, mu_tex, squares, dev_tex, var_tex, sd_tex)

    # 1-4·1-5 농어: 훈련 세트 42마리 → W → 경험분포 → E[W], σ_W
    def part_perch(self):
        self.clear_part(self.concept_group)
        rng = np.random.default_rng(0)
        icons = Group(*[chito("front", None, self.icon_height) for _ in range(N)])
        icons.arrange_in_grid(self.rows, self.cols, buff=0.14)
        for m in icons:
            m.shift(rng.uniform(-0.03, 0.03, 3) * np.array([1, 1, 0]))
        box = SurroundingRectangle(icons, buff=0.25).set_stroke(MUTED, 2).round_corners(0.15)
        Group(box, icons).move_to(LEFT * 3.9 + DOWN * 0.3)
        box_tag = label("농어 훈련 세트 42마리", 26).next_to(box, UP, buff=0.2)
        self.play(LaggedStartMap(FadeIn, icons, lag_ratio=0.02, run_time=1.4), FadeIn(box), FadeIn(box_tag))
        rv = VGroup(Tex(R"W", font_size=48), label("= 농어의 무게", 28, MEAN_COLOR)).arrange(RIGHT, buff=0.2)
        rv[0].set_color(MEAN_COLOR)
        rv.move_to(RIGHT * 3.4 + UP * 1.6)
        self.play(FadeIn(rv))
        self.wait(0.8)

        marker, value = None, None
        for i in (30, 5, 24):
            new_marker = ring(icons[i], WARN)
            new_value = Tex(R"w = %d\,\mathrm{g}" % TRAIN_W[i], font_size=44).set_color(WARN).move_to(RIGHT * 3.4 + UP * 0.4)
            if marker is None:
                self.play(ShowCreation(new_marker), FadeIn(new_value), run_time=0.6)
            else:
                self.play(Transform(marker, new_marker), FadeOut(value), run_time=0.4)
                self.play(FadeIn(new_value), run_time=0.3)
                new_marker = marker
            marker, value = new_marker, new_value
            self.wait(0.5)
        prob = Tex(R"f(w_i) = P(W = w_i) = \tfrac{1}{42}", font_size=36).set_color(INK).move_to(RIGHT * 3.4 + DOWN * 1.0)
        self.play(FadeIn(prob))
        self.wait(1.5)

        self.play(FadeOut(marker), FadeOut(value), FadeOut(rv), FadeOut(box), FadeOut(box_tag),
                  prob.animate.move_to(RIGHT * 4.3 + UP * 2.35))
        axes = Axes(x_range=(0, 1200, 200), y_range=(0, 0.4, 0.1), width=8.0, height=3.4,
                    axis_config=dict(stroke_width=2, include_tip=False))
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.9)
        axes.x_axis.add_numbers(range(200, 1201, 200), font_size=20)
        axes.y_axis.add_numbers([0.1, 0.2, 0.3, 0.4], font_size=20, num_decimal_places=1)
        x_tag = note("무게 (g)", 22).next_to(axes.x_axis, DOWN, buff=0.1)
        y_tag = note("P(칸)", 22).next_to(axes.y_axis, UP, buff=0.1)
        self.play(ShowCreation(axes), FadeIn(x_tag), FadeIn(y_tag))
        dots = VGroup(*[Dot(axes.c2p(TRAIN_W[i], 0.012), radius=0.06).set_fill(ACCENT, 0.9).set_stroke(width=0)
                        for i in range(N)])
        self.play(*[FadeOut(icons[i], target_position=dots[i].get_center(), scale=0.2) for i in range(N)], run_time=1.0)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.02, run_time=0.8))
        edges = np.arange(0, 1201, 100)
        counts, _ = np.histogram(TRAIN_W, edges)
        bars, labels = VGroup(), VGroup()
        for e, c in zip(edges[:-1], counts):
            if c == 0:
                continue
            h = axes.c2p(0, c / N)[1] - axes.c2p(0, 0)[1]
            w = axes.c2p(100, 0)[0] - axes.c2p(0, 0)[0]
            bar = Rectangle(width=w, height=h).set_fill(ACCENT, 0.4).set_stroke(ACCENT, 1.5)
            bar.move_to(axes.c2p(e, 0), aligned_edge=DL)
            bars.add(bar)
            labels.add(Tex(R"\tfrac{%d}{42}" % c, font_size=22).set_color(ACCENT).next_to(bar, UP, buff=0.05))
        self.play(FadeOut(dots), LaggedStartMap(FadeIn, bars, lag_ratio=0.08), run_time=1.0)
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.08))
        hist_tag = label("경험분포: 확률 히스토그램", 26).next_to(prob, DOWN, buff=0.35).align_to(prob, LEFT)
        self.play(FadeIn(hist_tag))
        self.wait(1.5)

        mean, sd = float(TRAIN_W.mean()), float(TRAIN_W.std())
        mean_line = DashedLine(axes.c2p(mean, 0), axes.c2p(mean, 0.4)).set_stroke(MEAN_COLOR, 3)
        tri = balance_marker(axes.c2p(mean, 0) + DOWN * 0.04)
        mean_tex = Tex(R"E[W] = \tfrac{1}{42}\textstyle\sum_i w_i = %s" % fmt(mean), font_size=34).set_color(MEAN_COLOR)
        mean_tex.next_to(hist_tag, DOWN, buff=0.45).align_to(prob, LEFT)
        self.play(ShowCreation(mean_line), FadeIn(tri), FadeIn(mean_tex))
        self.wait(1.2)
        band = Rectangle(width=axes.c2p(mean + sd, 0)[0] - axes.c2p(mean - sd, 0)[0],
                         height=axes.c2p(0, 0.4)[1] - axes.c2p(0, 0)[1])
        band.set_fill(CALM, 0.18).set_stroke(width=0).move_to(axes.c2p(mean, 0), aligned_edge=DOWN)
        sd_tex = Tex(R"\sigma_W = \sqrt{E[(W - E[W])^2]} = %s" % fmt(sd), font_size=32).set_color(CALM)
        sd_tex.next_to(mean_tex, DOWN, buff=0.3).align_to(prob, LEFT)
        self.play(FadeIn(band), FadeIn(sd_tex))
        self.wait(1.5)
        self.perch_group = VGroup(prob, axes, x_tag, y_tag, bars, labels, hist_tag, mean_line, tri, mean_tex, band, sd_tex)
        self.mean = mean

    # 1-6 다리: 길이를 모르면 E[W] 하나. 길이를 알면 조건부 기댓값 (2편)
    def part_bridge(self):
        self.clear_part(self.perch_group)
        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        mean_line = DashedLine(axes.c2p(0, self.mean), axes.c2p(55, self.mean)).set_stroke(MEAN_COLOR, 3)
        mean_tex = Tex(R"E[W] = %s" % fmt(self.mean), font_size=36).set_color(MEAN_COLOR)
        mean_tex.next_to(mean_line, UP, buff=0.08).align_to(axes.c2p(52, 0), RIGHT)
        self.play(ShowCreation(axes), FadeIn(tags), LaggedStartMap(FadeIn, dots, lag_ratio=0.02))
        self.play(ShowCreation(mean_line), FadeIn(mean_tex))
        pred_tag = label("길이를 모를 때의 예측값", 26, MEAN_COLOR).move_to(RIGHT * 4.4 + UP * 1.8)
        self.play(FadeIn(pred_tag))
        self.wait(1.0)
        next_tex = Tex(R"E[W \mid L = x]", font_size=40).set_color(WARN).move_to(RIGHT * 4.4 + DOWN * 0.2)
        next_tag = label("길이를 알 때: 2편", 26, WARN).next_to(next_tex, DOWN, buff=0.25)
        focus = DashedLine(axes.c2p(30, 0), axes.c2p(30, 1200)).set_stroke(WARN, 2)
        self.play(ShowCreation(focus), FadeIn(next_tex), FadeIn(next_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
class ConditionalToKNN(PartScene):
    """2편. 조건부확률·조건부분포·조건부 기댓값·최소제곱을 작은 예로 세우고, 농어에서 k-최근접 이웃 회귀로 잇는다.

    덱 (8) 「조건부확률과 조건부분포」 앞.
    """
    focus = 30.0
    k = 3
    ks = (1, 3, 10)
    probes = (20.0, 38.0)
    residual_ids = (3, 9, 20, 27, 33, 38)

    def construct(self):
        head = slide_title("조건부 기댓값과 k-최근접 이웃 회귀")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.part_conditional_probability()
        self.part_conditional_expectation()
        self.part_least_squares()
        self.part_perch_neighbors()
        self.part_regression_function()
        self.part_residual_band()
        self.part_k()
        self.part_distribution_view()

    # 2-1 조건부확률: 2원 표에서 한 행만 남기고 다시 나눈다
    def part_conditional_probability(self):
        icons, tags = toy_crowd(0.56)
        Group(icons, tags).move_to(UP * 1.9 + LEFT * 2.8)
        legend = VGroup(label("낚싯대 작음: S = 0", 22, CALM), label("낚싯대 큼: S = 1", 22, WARN)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(Group(icons, tags), RIGHT, buff=0.7)
        self.play(LaggedStartMap(FadeIn, icons, lag_ratio=0.1), LaggedStartMap(FadeIn, tags, lag_ratio=0.1), FadeIn(legend))
        self.wait(1.0)

        values = [1, 2, 3, 5]
        sizes = ["small", "large"]
        cell_w, cell_h = 1.05, 0.62
        table = VGroup()
        cells = {}
        origin = DOWN * 1.2 + LEFT * 3.6
        for r, s in enumerate(sizes):
            for c, v in enumerate(values):
                n = int(((TOY_X == v) & (TOY_S == s)).sum())
                rect = Rectangle(width=cell_w, height=cell_h).set_stroke(MUTED, 1.5)
                rect.move_to(origin + RIGHT * (c * cell_w) + DOWN * (r * cell_h))
                txt = frac_tex(n, 6, 26, INK if n else MUTED).move_to(rect)
                cells[(s, v)] = (rect, txt, n)
                table.add(rect, txt)
        col_heads = VGroup(*[Tex(R"x = %d" % v, font_size=24).set_color(INK).next_to(cells[("small", v)][0], UP, buff=0.12)
                             for v in values])
        row_heads = VGroup(*[label(TOY_NAME[s], 24, TOY_COLOR[s]).next_to(cells[(s, 1)][0], LEFT, buff=0.2) for s in sizes])
        row_sums = VGroup(*[frac_tex(int((TOY_S == s).sum()), 6, 26, TOY_COLOR[s]).next_to(cells[(s, 5)][0], RIGHT, buff=0.35)
                            for s in sizes])
        g_tag = Tex(R"g(s)", font_size=24).set_color(INK).next_to(row_sums, UP, buff=0.15)
        joint_tag = Tex(R"f(s, x)", font_size=28).set_color(INK).next_to(col_heads, UP, buff=0.25).align_to(table, LEFT)
        self.play(FadeIn(table), FadeIn(col_heads), FadeIn(row_heads), FadeIn(joint_tag))
        self.play(FadeIn(row_sums), FadeIn(g_tag))
        self.wait(1.2)

        big_row = SurroundingRectangle(VGroup(*[cells[("large", v)][0] for v in values]), buff=0.04).set_stroke(WARN, 3)
        cond_def = Tex(R"P(B \mid A) = \frac{P(A \cap B)}{P(A)}", font_size=34).set_color(INK).move_to(RIGHT * 4.0 + UP * 1.0)
        self.play(ShowCreation(big_row), FadeIn(cond_def))
        self.play(*[m.animate.set_opacity(0.25) for m in list(icons[:3]) + list(tags[:3])], run_time=0.5)
        ex = Tex(R"P(X{=}3 \mid S{=}1) = \frac{2/6}{3/6} = \frac{2}{3}", font_size=32).set_color(WARN)
        ex.next_to(cond_def, DOWN, buff=0.45)
        self.play(Indicate(cells[("large", 3)][1], color=WARN), Indicate(row_sums[1], color=WARN), FadeIn(ex))
        self.wait(1.5)
        self.toy = Group(icons, tags, legend)
        self.table_group = VGroup(table, col_heads, row_heads, row_sums, g_tag, joint_tag, big_row)
        self.cond_group = VGroup(cond_def, ex)
        self.cells = cells

    # 2-2 조건부분포와 조건부 기댓값: 큼 행을 다시 나눠 분포로, 그 균형점
    def part_conditional_expectation(self):
        self.clear_part(self.toy, self.cond_group)
        axes = Axes(x_range=(0, 6, 1), y_range=(0, 1, 0.5), width=4.8, height=2.6,
                    axis_config=dict(stroke_width=2, include_tip=False))
        axes.to_edge(RIGHT, buff=0.7).shift(UP * 0.9)
        axes.x_axis.add_numbers(range(1, 6), font_size=22)
        axes.y_axis.add_numbers([0.5, 1.0], font_size=20, num_decimal_places=1)
        bars = bars_on(axes, [3, 5], [2 / 3, 1 / 3], WARN, width=0.5)
        fracs = VGroup(frac_tex(2, 3, 26, WARN).next_to(bars[0], UP, buff=0.06),
                       frac_tex(1, 3, 26, WARN).next_to(bars[1], UP, buff=0.06))
        cond_tex = Tex(R"f(x \mid S{=}1) = \frac{f(1, x)}{g(1)}", font_size=32).set_color(WARN)
        cond_tex.next_to(axes, DOWN, buff=0.35)
        self.play(ShowCreation(axes), FadeIn(cond_tex))
        self.play(TransformFromCopy(self.cells[("large", 3)][1], bars[0]),
                  TransformFromCopy(self.cells[("large", 5)][1], bars[1]), run_time=1.0)
        self.play(FadeIn(fracs))
        self.wait(1.2)

        mu_big = float(TOY_X[TOY_S == "large"].mean())
        tri = balance_marker(axes.c2p(mu_big, 0) + DOWN * 0.04, WARN)
        e_tex = Tex(R"E[X \mid S{=}1] = \textstyle\sum_x x\,f(x \mid S{=}1) = %s" % fmt(mu_big, 2), font_size=30).set_color(WARN)
        e_tex.next_to(cond_tex, DOWN, buff=0.3)
        self.play(FadeIn(tri), FadeIn(e_tex))
        self.wait(1.0)
        mu_small = float(TOY_X[TOY_S == "small"].mean())
        mu_all = float(TOY_X.mean())
        compare = VGroup(
            Tex(R"E[X \mid S{=}0] = %s" % fmt(mu_small, 2), font_size=28).set_color(CALM),
            Tex(R"E[X] = %s" % fmt(mu_all, 2), font_size=28).set_color(MEAN_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(e_tex, DOWN, buff=0.3).align_to(e_tex, LEFT)
        self.play(FadeIn(compare))
        self.wait(1.5)
        self.cond_axes_group = VGroup(axes, bars, fracs, cond_tex, tri, e_tex, compare)
        self.mu_big = mu_big

    # 2-3 최소제곱: 예측값 a 를 움직이면 제곱오차 평균이 조건부 기댓값에서 최소
    def part_least_squares(self):
        self.clear_part(self.table_group, self.cond_axes_group)
        ys = TOY_X[TOY_S == "large"].astype(float)
        line = NumberLine(x_range=(2, 6, 1), width=5.0, include_numbers=True, font_size=22)
        line.move_to(LEFT * 3.6 + DOWN * 2.3)
        line_tag = note("S = 1 집단의 x", 22).next_to(line, DOWN, buff=0.35)
        dots = stacked_dots(line, ys, 1.0, 0.08, WARN, base=0.16)
        cond_tag = Tex(R"f(x \mid S{=}1)", font_size=30).set_color(WARN).next_to(line, UP, buff=2.6).align_to(line, LEFT)
        self.play(ShowCreation(line), FadeIn(line_tag), LaggedStartMap(FadeIn, dots, lag_ratio=0.2), FadeIn(cond_tag))

        a = ValueTracker(2.4)
        marker = balance_marker(line.n2p(a.get_value()) + DOWN * 0.02, MEAN_COLOR)
        marker.add_updater(lambda m: m.move_to(line.n2p(a.get_value()) + DOWN * 0.02, aligned_edge=UP))
        a_tag = always_redraw(lambda: Tex(R"a = %s" % fmt(a.get_value(), 2), font_size=30)
                              .set_color(MEAN_COLOR).next_to(marker, DOWN, buff=0.08))
        unit = 0.55

        def squares():
            g = VGroup()
            for j, w in enumerate(ys):
                av = a.get_value()
                base = Line(line.n2p(av), line.n2p(w)).set_stroke(CALM, 4).shift(UP * (0.45 + 0.5 * j))
                sq = Square(side_length=max(abs(w - av) * unit, 1e-3)).set_fill(CALM, 0.3).set_stroke(CALM, 1.5)
                sq.move_to(base.get_center(), aligned_edge=DOWN)
                g.add(base, sq)
            return g
        boxes = always_redraw(squares)
        sq_tag = Tex(R"(x_i - a)^2", font_size=30).set_color(CALM).next_to(cond_tag, RIGHT, buff=0.6)
        self.play(FadeIn(marker), FadeIn(a_tag))
        self.add(boxes)
        self.play(FadeIn(sq_tag))
        self.wait(0.8)

        OFF = 2.0
        axes = Axes(x_range=(0, 4, 1), y_range=(0, 6, 2), width=4.4, height=3.2,
                    axis_config=dict(stroke_width=2, include_tip=False))
        axes.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.7)
        for v in range(0, 5):
            axes.x_axis.add(Tex(str(int(v + OFF)), font_size=20).next_to(axes.c2p(v, 0), DOWN, buff=0.12))
        axes.y_axis.add_numbers(range(2, 7, 2), font_size=20)
        x_tag = note("a", 22).next_to(axes.x_axis, DOWN, buff=0.1)
        y_tag = Tex(R"E[(X - a)^2 \mid S{=}1]", font_size=26).set_color(INK).next_to(axes.y_axis, UP, buff=0.1).align_to(axes.y_axis, LEFT)

        def mse(t):
            return float(np.mean((ys - t) ** 2))
        curve = axes.get_graph(lambda t: mse(t + OFF), x_range=(0, 4)).set_stroke(ACCENT, 3)
        point = Dot(radius=0.09).set_fill(MEAN_COLOR, 1)
        point.add_updater(lambda m: m.move_to(axes.c2p(a.get_value() - OFF, mse(a.get_value()))))
        self.play(ShowCreation(axes), FadeIn(x_tag), FadeIn(y_tag))
        self.play(ShowCreation(curve), FadeIn(point))
        self.wait(0.8)
        self.play(a.animate.set_value(5.4), run_time=2.5, rate_func=linear)
        self.play(a.animate.set_value(self.mu_big), run_time=1.8, rate_func=smooth)
        best = Tex(R"a^* = E[X \mid S{=}1] = %s" % fmt(self.mu_big, 2), font_size=32).set_color(MEAN_COLOR)
        best.move_to(UP * 2.3 + RIGHT * 1.2)
        min_line = DashedLine(axes.c2p(self.mu_big - OFF, 0), axes.c2p(self.mu_big - OFF, mse(self.mu_big))).set_stroke(MEAN_COLOR, 2)
        self.play(ShowCreation(min_line), FadeIn(best))
        reg = Tex(R"f^*(x) = E[Y \mid X = x]", font_size=34).set_color(MEAN_COLOR).next_to(best, DOWN, buff=0.25)
        reg_tag = label("회귀 함수", 24, MEAN_COLOR).next_to(reg, DOWN, buff=0.12)
        self.play(FadeIn(reg), FadeIn(reg_tag))
        self.wait(1.5)
        for m in (boxes, marker, a_tag, point):
            m.clear_updaters()
        self.ls_group = VGroup(line, line_tag, dots, cond_tag, marker, a_tag, boxes, sq_tag, axes, x_tag, y_tag,
                               curve, point, best, min_line, reg, reg_tag)

    # 2-4 농어: 이웃 k 마리 = 조건부 표본, 그 평균 = 예측
    def part_perch_neighbors(self):
        self.clear_part(self.ls_group)
        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        self.play(ShowCreation(axes), FadeIn(tags))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.02, run_time=1.0))
        mean = float(TRAIN_W.mean())
        mean_line = DashedLine(axes.c2p(0, mean), axes.c2p(55, mean)).set_stroke(MEAN_COLOR, 2)
        mean_tex = Tex(R"E[W] = %s" % fmt(mean), font_size=32).set_color(MEAN_COLOR)
        mean_tex.next_to(mean_line, UP, buff=0.08).align_to(axes.c2p(52, 0), RIGHT)
        self.play(ShowCreation(mean_line), FadeIn(mean_tex))
        self.wait(1.0)

        focus_line = DashedLine(axes.c2p(self.focus, 0), axes.c2p(self.focus, 1200)).set_stroke(WARN, 2)
        focus_tag = Tex(R"L \approx %d" % self.focus, font_size=34).set_color(WARN).next_to(focus_line, UP, buff=0.08)
        self.play(ShowCreation(focus_line), FadeIn(focus_tag))
        idx = neighbors(self.focus, self.k)
        rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
        near_tag = label("가장 가까운 3마리 = 조건부 표본", 24, WARN).move_to(RIGHT * 4.3 + UP * 2.3)
        self.play(LaggedStartMap(ShowCreation, rings, lag_ratio=0.2), FadeIn(near_tag))
        self.wait(0.8)

        line = NumberLine(x_range=(200, 400, 100), width=2.6, include_numbers=True, font_size=20)
        line.move_to(RIGHT * 4.3 + DOWN * 1.6)
        c_tag = Tex(R"\widehat{P}_3(W \mid L \approx %d)" % self.focus, font_size=30).set_color(WARN).next_to(line, UP, buff=1.0)
        cdots = stacked_dots(line, TRAIN_W[idx], 10.0, 0.08, WARN, base=0.16)
        c_prob = frac_tex(1, 3, 28, WARN).next_to(cdots, RIGHT, buff=0.25)
        self.play(ShowCreation(line), FadeIn(c_tag))
        self.play(*[TransformFromCopy(dots[idx[d.src_index]], d) for d in cdots], FadeIn(c_prob))
        cmean = knn_predict(self.focus, self.k)
        cmean_line = DashedLine(line.n2p(cmean), line.n2p(cmean) + UP * 0.9).set_stroke(MEAN_COLOR, 3)
        cmean_tex = Tex(R"\hat{f}_3(%d) = \tfrac{1}{3}\textstyle\sum_{i \in N_3} w_i = %s" % (self.focus, fmt(cmean)),
                        font_size=28).set_color(MEAN_COLOR)
        cmean_tex.next_to(line, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        self.play(ShowCreation(cmean_line), FadeIn(cmean_tex))
        pred = Triangle().set_fill(MEAN_COLOR, 1).set_stroke(width=0).set_height(0.22).move_to(axes.c2p(self.focus, cmean))
        pred_tag = label("k-최근접 이웃 예측", 22, MEAN_COLOR).next_to(pred, RIGHT, buff=0.15)
        self.play(TransformFromCopy(cmean_line, pred), FadeIn(pred_tag))
        self.wait(1.5)
        self.axes, self.dots, self.mean_line, self.mean_tex = axes, dots, mean_line, mean_tex
        self.focus_line, self.focus_tag, self.rings, self.pred = focus_line, focus_tag, rings, pred
        self.panel = VGroup(line, c_tag, cdots, c_prob, cmean_line, cmean_tex, near_tag, pred_tag)

    # 2-5 회귀 함수: x 를 훑으면 예측점이 계단 곡선을 그린다. 범위 밖 50 은 고정
    def part_regression_function(self):
        axes, dots, pred, rings = self.axes, self.dots, self.pred, self.rings
        focus_line, focus_tag = self.focus_line, self.focus_tag
        self.clear_part(self.panel)
        ell = ValueTracker(self.focus)
        pred.add_updater(lambda m: m.move_to(axes.c2p(ell.get_value(), knn_predict(ell.get_value(), self.k))))
        focus_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(ell.get_value(), 0), axes.c2p(ell.get_value(), 1200)))
        focus_tag.add_updater(lambda m: m.become(
            Tex(R"L \approx %s" % fmt(ell.get_value(), 0), font_size=34).set_color(WARN).next_to(focus_line, UP, buff=0.08)))

        def current_rings():
            return VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i])
                            for i in neighbors(ell.get_value(), self.k)])
        rings.add_updater(lambda m: m.become(current_rings()))
        trace = TracedPath(pred.get_center, stroke_color=MEAN_COLOR, stroke_width=3)
        self.add(trace)
        self.play(ell.animate.set_value(8.0), run_time=2.0, rate_func=linear)
        self.play(ell.animate.set_value(45.0), run_time=4.5, rate_func=linear)
        curve_tag = Tex(R"\hat{f}_3(x) = \hat{E}[W \mid L \approx x]", font_size=32).set_color(MEAN_COLOR)
        curve_tag.move_to(RIGHT * 4.4 + UP * 1.6)
        self.play(FadeIn(curve_tag))
        self.wait(1.0)
        self.play(ell.animate.set_value(50.0), run_time=1.5, rate_func=linear)
        far_tex = Tex(R"\hat{f}_3(50) = %s" % fmt(knn_predict(50.0, self.k), 2), font_size=32).set_color(WARN)
        far_tex.next_to(curve_tag, DOWN, buff=0.35)
        far_tag = label("범위 밖: 이웃이 그대로", 24, WARN).next_to(far_tex, DOWN, buff=0.15)
        self.play(FadeIn(far_tex), FadeIn(far_tag))
        self.wait(1.5)
        # 자취(TracedPath)는 자체 updater 로 점을 계속 더하므로 지우기 전에 멈춘다 (점 개수가 어긋나면 broadcast 오류)
        for m in (pred, focus_line, focus_tag, rings, trace):
            m.clear_updaters()
        self.play(FadeOut(trace), FadeOut(pred), FadeOut(focus_line), FadeOut(focus_tag), FadeOut(rings),
                  FadeOut(far_tex), FadeOut(far_tag), FadeOut(curve_tag), FadeOut(self.mean_line), FadeOut(self.mean_tex),
                  run_time=0.6)

    # 2-6 잔차와 조건부 분산 띠
    def part_residual_band(self):
        axes, dots = self.axes, self.dots
        curve = knn_curve(axes, self.k)
        self.play(ShowCreation(curve), run_time=1.2)
        order = np.argsort(TRAIN_L)
        segs = VGroup()
        for j in self.residual_ids:
            i = order[j]
            segs.add(Line(axes.c2p(TRAIN_L[i], knn_predict(TRAIN_L[i], self.k)),
                          axes.c2p(TRAIN_L[i], TRAIN_W[i])).set_stroke(WARN, 3))
        eps_tag = Tex(R"\varepsilon_i = w_i - \hat{f}(x_i)", font_size=34).set_color(WARN).move_to(RIGHT * 4.4 + UP * 2.2)
        self.play(LaggedStartMap(ShowCreation, segs, lag_ratio=0.15), FadeIn(eps_tag))
        zero = Tex(R"E[\varepsilon \mid L] = 0", font_size=30).set_color(INK).next_to(eps_tag, DOWN, buff=0.25)
        self.play(FadeIn(zero))
        self.wait(1.5)

        self.play(FadeOut(segs))
        xs = np.arange(8.0, 52.0 + 1e-9, 0.1)
        upper = [axes.c2p(x, knn_predict(x, self.k) + neighbor_sd(x, self.k)) for x in xs]
        lower = [axes.c2p(x, max(0.0, knn_predict(x, self.k) - neighbor_sd(x, self.k))) for x in xs]
        band = VMobject().set_points_as_corners(upper + lower[::-1] + [upper[0]]).set_fill(CALM, 0.25).set_stroke(width=0)
        band_tag = Tex(R"\hat{f}_%d(x) \pm \hat{\sigma}(x)" % self.k, font_size=34).set_color(CALM).next_to(zero, DOWN, buff=0.45)
        sd_def = Tex(R"\hat{\sigma}^2(x) = \tfrac{1}{k-1}\sum_{i \in N_k(x)} (w_i - \hat{f}_k(x))^2",
                     font_size=26).set_color(CALM).next_to(band_tag, DOWN, buff=0.25)
        self.play(FadeIn(band), FadeIn(band_tag))
        self.play(FadeIn(sd_def))
        self.wait(1.0)
        below = sd_def
        bars = VGroup()
        for x in self.probes:
            sd = neighbor_sd(x, self.k)
            m = knn_predict(x, self.k)
            bar = Line(axes.c2p(x, m - sd), axes.c2p(x, m + sd)).set_stroke(WARN, 5)
            t = Tex(R"\hat{\sigma}(%d) = %s" % (x, fmt(sd)), font_size=30).set_color(WARN)
            t.next_to(below, DOWN, buff=0.3).align_to(band_tag, LEFT)
            below = t
            bars.add(bar, t)
            self.play(ShowCreation(bar), FadeIn(t), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(band), FadeOut(band_tag), FadeOut(sd_def), FadeOut(bars), FadeOut(eps_tag), FadeOut(zero),
                  FadeOut(curve), run_time=0.6)

    # 2-7 이웃 수 k: 조건이 넓어지면 곡선이 매끈해지고 값이 치우친다
    def part_k(self):
        axes, dots = self.axes, self.dots
        focus_line = DashedLine(axes.c2p(self.focus, 0), axes.c2p(self.focus, 1200)).set_stroke(WARN, 2)
        focus_tag = Tex(R"L \approx %d" % self.focus, font_size=34).set_color(WARN).next_to(focus_line, UP, buff=0.08)
        self.play(ShowCreation(focus_line), FadeIn(focus_tag))
        curve, rings, table = None, None, None
        for k in self.ks:
            idx = neighbors(self.focus, k)
            new_rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
            new_curve = knn_curve(axes, k)
            cmean = knn_predict(self.focus, k)
            if k > 1:
                sd_tex = Tex(R"\hat{\sigma}_{W \mid L \approx %d} = %s" % (self.focus, fmt(neighbor_sd(self.focus, k))), font_size=32)
            else:
                sd_tex = Tex(R"\hat{\sigma}_{W \mid L \approx %d}:\ k - 1 = 0" % self.focus, font_size=32)
            rows = VGroup(
                Tex(R"k = %d" % k, font_size=44).set_color(WARN),
                Tex(R"\hat{f}_{%d}(%d) = %s" % (k, self.focus, fmt(cmean)), font_size=32).set_color(MEAN_COLOR),
                sd_tex.set_color(CALM),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 4.4 + UP * 0.8)
            if curve is None:
                self.play(LaggedStartMap(ShowCreation, new_rings, lag_ratio=0.2), FadeIn(rows))
                self.play(ShowCreation(new_curve), run_time=1.5)
            else:
                self.play(Transform(rings, new_rings), Transform(curve, new_curve), FadeOut(table), run_time=1.2)
                self.play(FadeIn(rows), run_time=0.4)
                new_rings, new_curve = rings, curve
            rings, curve, table = new_rings, new_curve, rows
            self.wait(1.5)
        wide = label("k 큼: 매끈, 편향 증가", 26, MUTED).move_to(RIGHT * 4.4 + DOWN * 1.4)
        narrow = label("k 작음: 들쭉날쭉, 분산 큼", 26, MUTED).next_to(wide, DOWN, buff=0.2)
        self.play(FadeIn(wide), FadeIn(narrow))
        self.wait(1.5)
        self.play(FadeOut(curve), FadeOut(rings), FadeOut(table), FadeOut(wide), FadeOut(narrow), FadeOut(focus_tag),
                  run_time=0.6)
        self.focus_line = focus_line

    # 2-8 분포 관점: 같은 이웃에서 평균·중앙값·분위수, 각각을 이은 세 곡선
    def part_distribution_view(self):
        axes, dots, focus_line = self.axes, self.dots, self.focus_line
        k = 10
        idx = neighbors(self.focus, k)
        rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
        k_tag = Tex(R"k = %d,\ L \approx %d" % (k, self.focus), font_size=34).set_color(WARN).next_to(focus_line, UP, buff=0.08)
        self.play(FadeIn(k_tag), LaggedStartMap(ShowCreation, rings, lag_ratio=0.1))
        line = NumberLine(x_range=(100, 900, 200), width=4.6, include_numbers=True, font_size=20)
        line.move_to(RIGHT * 4.4 + DOWN * 1.9)
        cdots = stacked_dots(line, TRAIN_W[idx], 40.0, 0.075, WARN, base=0.15)
        self.play(ShowCreation(line), *[TransformFromCopy(dots[idx[d.src_index]], d) for d in cdots])
        stats = [("mean", MEAN_COLOR, R"\text{mean}"), ("median", CALM, R"\text{median}"), ("q90", ACCENT, R"q_{0.9}")]
        marks = VGroup()
        for j, (stat, color, name) in enumerate(stats):
            v = neighbor_stat(self.focus, k, stat)
            ln = DashedLine(line.n2p(v), line.n2p(v) + UP * 1.6).set_stroke(color, 3)
            t = Tex(R"%s = %s" % (name, fmt(v)), font_size=28).set_color(color)
            t.next_to(line, UP, buff=1.75 + 0.42 * j).align_to(line, LEFT).shift(RIGHT * (0.2 + 1.5 * j))
            marks.add(ln, t)
            self.play(ShowCreation(ln), FadeIn(t), run_time=0.7)
        self.wait(1.5)

        curves = VGroup(*[stat_curve(axes, k, stat, color) for stat, color, _ in stats])
        labels = VGroup(
            label("평균 곡선: 회귀 예측", 24, MEAN_COLOR),
            label("중앙값 곡선: 강건 회귀", 24, CALM),
            label("90% 분위수 곡선: 예측 상한", 24, ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 4.4 + UP * 2.0)
        self.play(FadeOut(rings), FadeOut(k_tag), FadeOut(focus_line))
        for c, t in zip(curves, labels):
            self.play(ShowCreation(c), FadeIn(t), run_time=1.3)
        self.wait(2)
