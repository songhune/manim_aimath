# -*- coding: utf-8 -*-
"""기계학습기초 — k-최근접 이웃 회귀의 확률적 해석 (`[0922]Regression.pptx` SECTION 3-1 보조 영상).

농어 훈련 세트(42마리)를 확률변수로 읽는다. 무게 W 는 표본에서 한 마리를 고를 때 나오는 값이고,
그 분포는 경험분포 P(W = wᵢ) = 1/42 다. 기댓값과 분산은 길이를 모를 때의 대푯값과 흩어짐이다.
길이를 알면 조건부 분포 P(W | L ≈ ℓ) 로 좁아지고, 그 조건부 기댓값을 이웃 k 마리의 평균으로
추정한 것이 k-최근접 이웃 회귀다.

소재 규칙(하네스 3.8): 화면의 수치는 전부 여기서 계산한다. 자료는 덱 6쪽의 농어 56마리이고,
훈련 세트는 덱 8쪽의 `train_test_split(perch_length, perch_weight, random_state=42)` 와 같은
42마리다(numpy `RandomState(42).permutation` 으로 같은 분할을 재현. sklearn 이 없는 환경에서도 돈다).
50cm 의 이웃이 44·43·43 이고 예측이 1033.33 인 것이 덱 22·24쪽과 같다.

개체 아이콘은 치토(하네스 3.6). 물고기 대신 마스코트 한 마리가 농어 한 마리다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/ml/ml_week04.py
    ./render.sh check _2026/ml/ml_week04.py
    ./render.sh all   _2026/ml/ml_week04.py
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


def neighbors(length, k):
    """길이 length 에 가장 가까운 훈련 샘플 k 개의 인덱스. 거리가 같으면 앞의 것."""
    return np.argsort(np.abs(TRAIN_L - length), kind="stable")[:k]


def knn_predict(length, k):
    return float(TRAIN_W[neighbors(length, k)].mean())


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
    curve = VMobject().set_points_as_corners(pts)
    return curve.set_stroke(MEAN_COLOR, 3)


def fmt(value, places=1):
    return ("%%.%df" % places) % value


# ─────────────────────────────────────────────────────────────
class PerchAsRandomVariable(InteractiveScene):
    """훈련 세트 42마리 → 한 마리를 고르면 무게가 나온다 → 확률변수 W 와 경험분포 → E[W], Var[W].

    덱 SECTION 3-1 (4) 「농어 표본과 확률변수」 바로 앞에 둔다.
    """
    rows, cols = 6, 7
    icon_height = 0.36

    def construct(self):
        head = slide_title("농어 표본과 확률변수")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 훈련 세트: 마스코트 한 마리가 농어 한 마리
        rng = np.random.default_rng(0)
        icons = Group(*[chito("front", None, self.icon_height) for _ in range(N)])
        icons.arrange_in_grid(self.rows, self.cols, buff=0.14)
        for m in icons:
            m.shift(rng.uniform(-0.03, 0.03, 3) * np.array([1, 1, 0]))
        box = SurroundingRectangle(icons, buff=0.25).set_stroke(MUTED, 2).round_corners(0.15)
        Group(box, icons).move_to(LEFT * 3.9 + DOWN * 0.3)
        box_tag = label("훈련 세트 42마리", 26).next_to(box, UP, buff=0.2)
        self.play(LaggedStartMap(FadeIn, icons, lag_ratio=0.02, run_time=1.4),
                  FadeIn(box), FadeIn(box_tag))
        self.wait()

        # ── 한 마리를 고르면 무게 하나가 나온다. 세 번 고른다
        rv = Tex(R"W", font_size=72).set_color(MEAN_COLOR)
        rv_tag = label("무게 확률변수", 26).next_to(rv, DOWN, buff=0.15)
        Group(rv, rv_tag).move_to(RIGHT * 3.2 + UP * 1.6)
        self.play(FadeIn(rv), FadeIn(rv_tag))

        picks = [30, 5, 24]
        marker, value = None, None
        for i in picks:
            new_marker = ring(icons[i], WARN)
            new_value = Tex(R"w = %d\,\mathrm{g}" % TRAIN_W[i], font_size=48)
            new_value.set_color(WARN).move_to(RIGHT * 3.2 + UP * 0.2)
            if marker is None:
                self.play(ShowCreation(new_marker), FadeIn(new_value), run_time=0.6)
            else:
                self.play(Transform(marker, new_marker), FadeOut(value), run_time=0.4)
                self.play(FadeIn(new_value), run_time=0.3)
                new_marker = marker
            marker, value = new_marker, new_value
            self.wait(0.6)
        prob = Tex(R"P(W = w_i) = \tfrac{1}{42}", font_size=42).set_color(INK)
        prob.move_to(RIGHT * 3.2 + DOWN * 1.2)
        self.play(FadeIn(prob))
        self.wait()

        # ── 표본 전체를 무게 축에 늘어놓는다: 경험분포
        self.play(FadeOut(marker), FadeOut(value), FadeOut(rv), FadeOut(rv_tag),
                  FadeOut(box), FadeOut(box_tag),
                  prob.animate.move_to(RIGHT * 4.3 + UP * 2.35))
        line = NumberLine(x_range=(0, 1200, 200), width=11.0, include_numbers=True,
                          font_size=22)
        line.move_to(DOWN * 2.2)
        line_tag = note("무게 (g)", 22).next_to(line, DOWN, buff=0.35)
        self.play(ShowCreation(line), FadeIn(line_tag))

        bin_w, radius = 30.0, 0.075
        stacks = {}
        dots = VGroup()
        order = np.argsort(TRAIN_W)
        for i in order:
            b = int(TRAIN_W[i] // bin_w)
            level = stacks.get(b, 0)
            stacks[b] = level + 1
            p = line.n2p(TRAIN_W[i]) + UP * (0.14 + level * 2 * radius)
            d = Dot(p, radius=radius).set_fill(ACCENT, 0.95).set_stroke(width=0)
            d.icon_index = i
            dots.add(d)
        self.play(*[
            FadeOut(icons[d.icon_index], target_position=d.get_center(), scale=0.2)
            for d in dots], run_time=1.2)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.03, run_time=1.2))
        dist_tag = label("경험분포", 26).next_to(line, UP, buff=2.4).to_edge(LEFT, buff=0.8)
        self.play(FadeIn(dist_tag))
        self.wait()

        # ── 기댓값: 무게의 평균 자리
        mean = float(TRAIN_W.mean())
        mean_line = DashedLine(line.n2p(mean), line.n2p(mean) + UP * 2.6).set_stroke(MEAN_COLOR, 3)
        mean_tex = Tex(R"E[W] = \tfrac{1}{42} \textstyle\sum_i w_i = %s" % fmt(mean), font_size=40)
        mean_tex.set_color(MEAN_COLOR).move_to(RIGHT * 4.3 + UP * 1.45)
        self.play(ShowCreation(mean_line), FadeIn(mean_tex))
        self.wait()

        # ── 분산: 평균에서 얼마나 흩어져 있나. ±σ 띠
        sd = float(TRAIN_W.std())
        band = Rectangle(width=line.n2p(mean + sd)[0] - line.n2p(mean - sd)[0], height=0.4)
        band.set_fill(CALM, 0.25).set_stroke(width=0).move_to(line.n2p(mean) + UP * 0.02)
        band.align_to(line.n2p(mean), DOWN).shift(UP * 0.02)
        var_tex = Tex(R"\mathrm{Var}[W] = E\big[(W - E[W])^2\big]", font_size=36).set_color(CALM)
        sd_tex = Tex(R"\sigma_W = \sqrt{\mathrm{Var}[W]} = %s" % fmt(sd), font_size=36).set_color(CALM)
        VGroup(var_tex, sd_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(var_tex, sd_tex).move_to(RIGHT * 4.3 + UP * 0.45)
        band_tag = Tex(R"\pm\sigma_W", font_size=30).set_color(CALM)
        band_tag.next_to(band.get_corner(UR), UP, buff=0.55)
        self.play(FadeIn(band), FadeIn(var_tex))
        self.play(FadeIn(band_tag), FadeIn(sd_tex))
        self.wait(2)


class ConditionalExpectation(InteractiveScene):
    """길이를 알면 분포가 좁아진다: P(W | L ≈ ℓ) 와 E[W | L ≈ ℓ]. 이웃 k 마리의 평균이 그 추정이다.

    덱 SECTION 3-1 (6) 「조건부 확률과 조건부 기댓값」 바로 앞에 둔다.
    """
    k = 3
    focus = 30.0

    def construct(self):
        head = slide_title("조건부 기댓값과 k-최근접 이웃")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        self.play(ShowCreation(axes), FadeIn(tags))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.02, run_time=1.2))

        # ── 길이를 모를 때: E[W] 한 줄
        mean = float(TRAIN_W.mean())
        mean_line = DashedLine(axes.c2p(0, mean), axes.c2p(55, mean)).set_stroke(MEAN_COLOR, 2)
        mean_tex = Tex(R"E[W] = %s" % fmt(mean), font_size=36).set_color(MEAN_COLOR)
        mean_tex.next_to(mean_line, UP, buff=0.08).align_to(axes.c2p(52, 0), RIGHT)
        self.play(ShowCreation(mean_line), FadeIn(mean_tex))
        self.wait()

        # ── 길이 ℓ 을 알면: 가장 가까운 k 마리
        ell = ValueTracker(self.focus)
        focus_line = DashedLine(axes.c2p(self.focus, 0), axes.c2p(self.focus, 1200)).set_stroke(WARN, 2)
        focus_tag = Tex(R"L \approx %d" % self.focus, font_size=36).set_color(WARN)
        focus_tag.next_to(focus_line, UP, buff=0.08)
        self.play(ShowCreation(focus_line), FadeIn(focus_tag))

        idx = neighbors(self.focus, self.k)
        rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
        self.play(LaggedStartMap(ShowCreation, rings, lag_ratio=0.2))

        # 조건부 분포: 이웃의 무게만 남긴 작은 분포
        panel_x = RIGHT * 4.3
        cline = NumberLine(x_range=(200, 400, 100), width=2.6, include_numbers=True, font_size=20)
        cline.move_to(panel_x + DOWN * 1.6)
        c_tag = Tex(R"P(W \mid L \approx %d)" % self.focus, font_size=34).set_color(WARN)
        c_tag.next_to(cline, UP, buff=1.0)
        cdots = VGroup()
        levels = {}
        for i in idx:
            b = int(TRAIN_W[i] // 10)
            lv = levels.get(b, 0)
            levels[b] = lv + 1
            cdots.add(Dot(cline.n2p(TRAIN_W[i]) + UP * (0.16 + lv * 0.16), radius=0.08)
                      .set_fill(WARN, 0.95).set_stroke(width=0))
        c_prob = Tex(R"\tfrac{1}{%d}" % self.k, font_size=28).set_color(WARN)
        c_prob.next_to(cdots, RIGHT, buff=0.25)
        self.play(ShowCreation(cline), FadeIn(c_tag))
        self.play(*[TransformFromCopy(dots[i], d) for i, d in zip(idx, cdots)], FadeIn(c_prob))

        cmean = knn_predict(self.focus, self.k)
        cmean_line = DashedLine(cline.n2p(cmean), cline.n2p(cmean) + UP * 0.9).set_stroke(MEAN_COLOR, 3)
        cmean_tex = Tex(R"E[W \mid L \approx %d] = \frac{1}{%d}\sum_{i \in N_%d} w_i = %s"
                        % (self.focus, self.k, self.k, fmt(cmean)), font_size=28).set_color(MEAN_COLOR)
        cmean_tex.next_to(cline, DOWN, buff=0.45).to_edge(RIGHT, buff=0.35)
        self.play(ShowCreation(cmean_line), FadeIn(cmean_tex))

        # 그 값이 산점도 위의 예측점
        pred = Triangle().set_fill(MEAN_COLOR, 1).set_stroke(width=0).set_height(0.22)
        pred.move_to(axes.c2p(self.focus, cmean))
        pred_tag = label("k-최근접 이웃 예측", 24, MEAN_COLOR).next_to(pred, RIGHT, buff=0.15)
        self.play(TransformFromCopy(cmean_line, pred), FadeIn(pred_tag))
        self.wait()

        # ── ℓ 을 훑으면 예측점이 계단 곡선을 그린다
        self.play(FadeOut(cline), FadeOut(c_tag), FadeOut(cdots), FadeOut(c_prob),
                  FadeOut(cmean_line), FadeOut(cmean_tex), FadeOut(pred_tag))

        def current_pred():
            return axes.c2p(ell.get_value(), knn_predict(ell.get_value(), self.k))

        pred.add_updater(lambda m: m.move_to(current_pred()))
        focus_line.add_updater(lambda m: m.put_start_and_end_on(
            axes.c2p(ell.get_value(), 0), axes.c2p(ell.get_value(), 1200)))
        focus_tag.add_updater(lambda m: m.become(
            Tex(R"L \approx %s" % fmt(ell.get_value(), 0), font_size=36).set_color(WARN)
            .next_to(focus_line, UP, buff=0.08)))

        def current_rings():
            g = VGroup()
            for i in neighbors(ell.get_value(), self.k):
                g.add(Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]))
            return g
        rings.add_updater(lambda m: m.become(current_rings()))
        trace = TracedPath(pred.get_center, stroke_color=MEAN_COLOR, stroke_width=3)
        self.add(trace)
        self.play(ell.animate.set_value(8.0), run_time=2.0, rate_func=linear)
        self.play(ell.animate.set_value(45.0), run_time=4.5, rate_func=linear)
        curve_tag = Tex(R"\hat{E}[W \mid L = \ell],\ k = %d" % self.k, font_size=36).set_color(MEAN_COLOR)
        curve_tag.move_to(RIGHT * 4.6 + UP * 1.4)
        self.play(FadeIn(curve_tag))
        self.wait()

        # ── 범위 밖 ℓ = 50: 이웃이 44·43·43 에 머물러 예측이 1033 으로 고정 (덱 24쪽)
        self.play(ell.animate.set_value(50.0), run_time=1.5, rate_func=linear)
        far = knn_predict(50.0, self.k)
        far_tex = Tex(R"\hat{E}[W \mid L \approx 50] = %s" % fmt(far, 2), font_size=34).set_color(WARN)
        far_tex.next_to(curve_tag, DOWN, buff=0.4)
        self.play(FadeIn(far_tex))
        self.wait(2)


class NeighborCountAndVariance(InteractiveScene):
    """k 를 바꾸면 조건이 넓어진다: 이웃 수 k 와 조건부 분산, 그리고 예측 곡선의 모양.

    k = 1 이면 이웃 하나의 무게 그대로(분산 0, 곡선이 들쭉날쭉), k 가 크면 먼 농어까지 평균에
    들어와 곡선이 매끈해지는 대신 길이 ℓ 에서 멀어진 값으로 치우친다. 덱 13~15쪽의
    과대적합·과소적합을 조건부 기댓값의 눈으로 다시 본다.
    """
    focus = 30.0
    ks = (1, 3, 10)

    def construct(self):
        head = slide_title("이웃 수 k 와 조건부 분산")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        self.play(ShowCreation(axes), FadeIn(tags), LaggedStartMap(FadeIn, dots, lag_ratio=0.02))

        focus_line = DashedLine(axes.c2p(self.focus, 0), axes.c2p(self.focus, 1200)).set_stroke(WARN, 2)
        focus_tag = Tex(R"L \approx %d" % self.focus, font_size=36).set_color(WARN)
        focus_tag.next_to(focus_line, UP, buff=0.08)
        self.play(ShowCreation(focus_line), FadeIn(focus_tag))

        curve, rings, table = None, None, None
        for k in self.ks:
            idx = neighbors(self.focus, k)
            new_rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
            new_curve = knn_curve(axes, k)
            cmean = knn_predict(self.focus, k)
            # 조건부 표준편차는 k - 1 로 나눈 표본 표준편차. k = 1 이면 정의되지 않는다
            if k > 1:
                sd_tex = Tex(R"\hat{\sigma}_{W \mid L \approx %d} = %s"
                             % (self.focus, fmt(float(TRAIN_W[idx].std(ddof=1)))), font_size=32)
            else:
                sd_tex = Tex(R"\hat{\sigma}_{W \mid L \approx %d}:\ k - 1 = 0" % self.focus, font_size=32)
            rows = VGroup(
                Tex(R"k = %d" % k, font_size=44).set_color(WARN),
                Tex(R"\hat{f}_{%d}(%d) = %s" % (k, self.focus, fmt(cmean)), font_size=32).set_color(MEAN_COLOR),
                sd_tex.set_color(CALM),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            rows.move_to(RIGHT * 4.4 + UP * 0.8)
            if curve is None:
                self.play(LaggedStartMap(ShowCreation, new_rings, lag_ratio=0.2), FadeIn(rows))
                self.play(ShowCreation(new_curve), run_time=1.5)
            else:
                self.play(Transform(rings, new_rings), Transform(curve, new_curve),
                          FadeOut(table), run_time=1.2)
                self.play(FadeIn(rows), run_time=0.4)
                new_rings, new_curve = rings, curve
            rings, curve, table = new_rings, new_curve, rows
            self.wait(1.5)

        wide = label("k 큼: 매끈, 편향 증가", 26, MUTED).move_to(RIGHT * 4.4 + DOWN * 1.4)
        narrow = label("k 작음: 들쭉날쭉, 분산 큼", 26, MUTED).next_to(wide, DOWN, buff=0.2)
        self.play(FadeIn(wide), FadeIn(narrow))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 슬라이드 (9) ~ (13) 의 논증을 그림으로: 최소제곱, 잔차와 조건부 분산 띠, 분포 관점
# ─────────────────────────────────────────────────────────────
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


def stat_curve(axes, k, stat, color, x_min=8.0, x_max=52.0, step=0.1):
    xs = np.arange(x_min, x_max + 1e-9, step)
    pts = [axes.c2p(x, neighbor_stat(x, k, stat)) for x in xs]
    return VMobject().set_points_as_corners(pts).set_stroke(color, 3)


class LeastSquaresPrediction(InteractiveScene):
    """예측값 a 를 움직이면 이웃 세 마리의 제곱오차 넓이가 변하고, a = 이웃 평균에서 그 평균이 가장 작다.

    슬라이드 (9) 「회귀의 확률적 정의」 바로 앞에 둔다. E[(W − a)² | L ≈ x] 의 최소가 조건부 기댓값이다.
    """
    focus = 30.0
    k = 3
    unit = 0.011          # 1 g 을 화면 몇 단위로 그릴지 (정사각형 한 변)

    def construct(self):
        head = slide_title("최소제곱과 조건부 기댓값")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        idx = neighbors(self.focus, self.k)
        ys = np.sort(TRAIN_W[idx])
        mean = float(ys.mean())

        line = NumberLine(x_range=(200, 400, 50), width=7.0, include_numbers=True, font_size=22)
        line.move_to(LEFT * 3.1 + DOWN * 2.4)
        line_tag = note("이웃 무게 (g)", 22).next_to(line, DOWN, buff=0.35)
        dots = VGroup()
        levels = {}
        for w in ys:
            b = int(w // 10)
            lv = levels.get(b, 0)
            levels[b] = lv + 1
            dots.add(Dot(line.n2p(w) + UP * (0.16 + lv * 0.18), radius=0.08).set_fill(WARN, 0.95).set_stroke(width=0))
        cond_tag = Tex(R"P(W \mid L \approx %d):\ \tfrac{1}{3}" % self.focus, font_size=34).set_color(WARN)
        cond_tag.next_to(line, UP, buff=2.4).align_to(line, LEFT)
        self.play(ShowCreation(line), FadeIn(line_tag), LaggedStartMap(FadeIn, dots, lag_ratio=0.2), FadeIn(cond_tag))
        self.wait()

        # 예측값 a: 삼각형. 이웃마다 |w - a| 를 한 변으로 하는 정사각형 = 제곱오차
        a = ValueTracker(230.0)
        marker = Triangle().set_fill(MEAN_COLOR, 1).set_stroke(width=0).set_height(0.22)
        marker.add_updater(lambda m: m.move_to(line.n2p(a.get_value()) + DOWN * 0.18))
        a_tag = always_redraw(lambda: Tex(R"a = %d" % round(a.get_value()), font_size=32)
                              .set_color(MEAN_COLOR).next_to(marker, DOWN, buff=0.1))

        def squares():
            """이웃마다 a 까지의 거리를 밑변으로 하고, 그 거리를 한 변으로 하는 정사각형 = 제곱오차."""
            g = VGroup()
            for j, w in enumerate(ys):
                av = a.get_value()
                base = Line(line.n2p(av), line.n2p(w)).set_stroke(CALM, 4)
                base.shift(UP * (0.5 + 0.55 * j))
                side = abs(w - av) * self.unit
                sq = Square(side_length=max(side, 1e-3)).set_fill(CALM, 0.3).set_stroke(CALM, 1.5)
                sq.move_to(base.get_center(), aligned_edge=DOWN)
                g.add(base, sq)
            return g
        boxes = always_redraw(squares)
        self.play(FadeIn(marker), FadeIn(a_tag))
        self.add(boxes)
        sq_tag = Tex(R"(w_i - a)^2", font_size=30).set_color(CALM).next_to(cond_tag, RIGHT, buff=0.6)
        self.play(FadeIn(sq_tag))
        self.wait()

        # 오른쪽: a 에 따른 제곱오차 평균
        # manimlib 은 y 축을 x = 0 자리에 두므로, a 대신 a - 200 을 좌표로 쓰고 눈금 글자만 200 ~ 360 으로 단다
        OFF = 200
        axes = Axes(x_range=(0, 160, 40), y_range=(0, 6000, 2000), width=4.6, height=3.4,
                    axis_config=dict(stroke_width=2, include_tip=False))
        axes.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.6)
        for v in range(0, 161, 40):
            axes.x_axis.add(Tex(str(v + OFF), font_size=20).next_to(axes.c2p(v, 0), DOWN, buff=0.12))
        axes.y_axis.add_numbers(range(2000, 6001, 2000), font_size=20)
        x_tag = note("a (g)", 22).next_to(axes.x_axis, DOWN, buff=0.1)
        y_tag = Tex(R"\hat{E}[(W - a)^2 \mid L \approx %d]" % self.focus, font_size=28).set_color(INK)
        y_tag.next_to(axes.y_axis, UP, buff=0.1).align_to(axes.y_axis, LEFT)

        def mse(t):
            return float(np.mean((ys - t) ** 2))
        curve = axes.get_graph(lambda t: mse(t + OFF), x_range=(0, 160)).set_stroke(ACCENT, 3)
        point = Dot(radius=0.09).set_fill(MEAN_COLOR, 1)
        point.add_updater(lambda m: m.move_to(axes.c2p(a.get_value() - OFF, mse(a.get_value()))))
        self.play(ShowCreation(axes), FadeIn(x_tag), FadeIn(y_tag))
        self.play(ShowCreation(curve), FadeIn(point))
        self.wait()

        self.play(a.animate.set_value(320.0), run_time=3.0, rate_func=linear)
        self.play(a.animate.set_value(mean), run_time=2.0, rate_func=smooth)
        best = Tex(R"a^* = \hat{E}[W \mid L \approx %d] = %s" % (self.focus, fmt(mean)), font_size=34)
        best.set_color(MEAN_COLOR).move_to(UP * 2.35 + RIGHT * 0.6)
        min_line = DashedLine(axes.c2p(mean - OFF, 0), axes.c2p(mean - OFF, mse(mean))).set_stroke(MEAN_COLOR, 2)
        self.play(ShowCreation(min_line), FadeIn(best))
        self.wait(2)


class ResidualAndConditionalSpread(InteractiveScene):
    """회귀 함수 위의 잔차 ε 와, 위치마다 달라지는 조건부 표준편차 띠 f̂ ± σ̂.

    슬라이드 (11) 「회귀 함수와 잔차」·(12) 「조건부 분산의 추정」 바로 앞에 둔다.
    """
    k = 5
    residual_ids = (3, 9, 20, 27, 33, 38)      # 잔차를 그릴 훈련 샘플 (정렬한 길이 순서에서 고른 자리)
    probes = (20.0, 38.0)

    def construct(self):
        head = slide_title("잔차와 조건부 분산")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        curve = knn_curve(axes, self.k)
        self.play(ShowCreation(axes), FadeIn(tags), LaggedStartMap(FadeIn, dots, lag_ratio=0.02))
        self.play(ShowCreation(curve), run_time=1.5)
        curve_tag = Tex(R"\hat{f}_{%d}(x)" % self.k, font_size=34).set_color(MEAN_COLOR)
        curve_tag.next_to(axes.c2p(46, knn_predict(46, self.k)), UP, buff=0.2)
        self.play(FadeIn(curve_tag))
        self.wait()

        # 잔차: 점에서 곡선까지의 세로 선분
        order = np.argsort(TRAIN_L)
        segs = VGroup()
        for j in self.residual_ids:
            i = order[j]
            top, bottom = TRAIN_W[i], knn_predict(TRAIN_L[i], self.k)
            seg = Line(axes.c2p(TRAIN_L[i], bottom), axes.c2p(TRAIN_L[i], top)).set_stroke(WARN, 3)
            segs.add(seg)
        eps_tag = Tex(R"\varepsilon_i = w_i - \hat{f}(x_i)", font_size=34).set_color(WARN)
        eps_tag.move_to(RIGHT * 4.4 + UP * 2.2)
        self.play(LaggedStartMap(ShowCreation, segs, lag_ratio=0.15), FadeIn(eps_tag))
        zero = Tex(R"E[\varepsilon \mid L] = 0", font_size=30).set_color(INK).next_to(eps_tag, DOWN, buff=0.25)
        self.play(FadeIn(zero))
        self.wait()

        # 조건부 표준편차 띠: f̂ ± σ̂ (k − 1 로 나눔). 위치마다 폭이 다르다
        self.play(FadeOut(segs))
        xs = np.arange(8.0, 52.0 + 1e-9, 0.1)
        upper = [axes.c2p(x, knn_predict(x, self.k) + neighbor_sd(x, self.k)) for x in xs]
        lower = [axes.c2p(x, max(0.0, knn_predict(x, self.k) - neighbor_sd(x, self.k))) for x in xs]
        band = VMobject().set_points_as_corners(upper + lower[::-1] + [upper[0]])
        band.set_fill(CALM, 0.25).set_stroke(width=0)
        band_tag = Tex(R"\hat{f}_{%d}(x) \pm \hat{\sigma}(x)" % self.k, font_size=34).set_color(CALM)
        band_tag.next_to(zero, DOWN, buff=0.45)
        sd_def = Tex(R"\hat{\sigma}^2(x) = \tfrac{1}{k-1}\sum_{i \in N_k(x)} (w_i - \hat{f}_k(x))^2",
                     font_size=26).set_color(CALM).next_to(band_tag, DOWN, buff=0.25)
        self.play(FadeIn(band), FadeIn(band_tag))
        self.play(FadeIn(sd_def))
        self.wait()

        # 좁은 곳과 넓은 곳을 재 본다
        below = sd_def
        for x in self.probes:
            sd = neighbor_sd(x, self.k)
            m = knn_predict(x, self.k)
            bar = Line(axes.c2p(x, m - sd), axes.c2p(x, m + sd)).set_stroke(WARN, 5)
            t = Tex(R"\hat{\sigma}(%d) = %s" % (x, fmt(sd)), font_size=30).set_color(WARN)
            t.next_to(below, DOWN, buff=0.3).align_to(band_tag, LEFT)
            below = t
            self.play(ShowCreation(bar), FadeIn(t), run_time=0.8)
        self.wait(2)


class DistributionView(InteractiveScene):
    """같은 이웃(k = 10)에서 평균·중앙값·90% 분위수를 읽고, 각각을 x 마다 이어 세 곡선으로 그린다.

    슬라이드 (13) 「분포 관점」 바로 앞에 둔다.
    """
    focus = 30.0
    k = 10

    def construct(self):
        head = slide_title("분포 관점: 평균·중앙값·분위수")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = perch_axes()
        axes.to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
        tags = axis_tags(axes)
        dots = train_dots(axes)
        self.play(ShowCreation(axes), FadeIn(tags), LaggedStartMap(FadeIn, dots, lag_ratio=0.02))

        idx = neighbors(self.focus, self.k)
        ys = np.sort(TRAIN_W[idx])
        focus_line = DashedLine(axes.c2p(self.focus, 0), axes.c2p(self.focus, 1200)).set_stroke(WARN, 2)
        rings = VGroup(*[Circle(radius=0.14).set_stroke(WARN, 3).move_to(dots[i]) for i in idx])
        k_tag = Tex(R"k = %d,\ L \approx %d" % (self.k, self.focus), font_size=34).set_color(WARN)
        k_tag.next_to(focus_line, UP, buff=0.08)
        self.play(ShowCreation(focus_line), FadeIn(k_tag), LaggedStartMap(ShowCreation, rings, lag_ratio=0.1))

        # 오른쪽: 이웃 무게의 점그림과 세 통계량
        line = NumberLine(x_range=(100, 900, 200), width=4.6, include_numbers=True, font_size=20)
        line.move_to(RIGHT * 4.4 + DOWN * 1.9)
        cdots = VGroup()
        levels = {}
        for w in ys:
            b = int(w // 40)
            lv = levels.get(b, 0)
            levels[b] = lv + 1
            cdots.add(Dot(line.n2p(w) + UP * (0.15 + lv * 0.17), radius=0.075).set_fill(WARN, 0.95).set_stroke(width=0))
        self.play(ShowCreation(line), *[TransformFromCopy(dots[i], d) for i, d in zip(idx, cdots)])

        stats = [("mean", MEAN_COLOR, R"\text{mean}"), ("median", CALM, R"\text{median}"), ("q90", ACCENT, R"q_{0.9}")]
        marks = VGroup()
        for j, (stat, color, name) in enumerate(stats):
            v = neighbor_stat(self.focus, self.k, stat)
            ln = DashedLine(line.n2p(v), line.n2p(v) + UP * 1.6).set_stroke(color, 3)
            t = Tex(R"%s = %s" % (name, fmt(v)), font_size=28).set_color(color)
            t.next_to(line, UP, buff=1.75 + 0.42 * j).align_to(line, LEFT).shift(RIGHT * (0.2 + 1.5 * j))
            marks.add(VGroup(ln, t))
            self.play(ShowCreation(ln), FadeIn(t), run_time=0.7)
        self.wait()

        # 세 통계량을 x 마다 이으면 세 곡선: 회귀·중앙값 회귀·분위수 회귀
        curves = VGroup()
        for stat, color, name in stats:
            c = stat_curve(axes, self.k, stat, color)
            curves.add(c)
        labels = VGroup(
            label("평균 곡선: 회귀 예측", 24, MEAN_COLOR),
            label("중앙값 곡선: 강건 회귀", 24, CALM),
            label("90% 분위수 곡선: 예측 상한", 24, ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        labels.move_to(RIGHT * 4.4 + UP * 2.0)
        self.play(FadeOut(rings), FadeOut(k_tag), FadeOut(focus_line))
        for c, t in zip(curves, labels):
            self.play(ShowCreation(c), FadeIn(t), run_time=1.3)
        self.wait(2)
