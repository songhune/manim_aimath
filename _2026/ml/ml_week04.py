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
            csd = float(TRAIN_W[idx].std())
            rows = VGroup(
                Tex(R"k = %d" % k, font_size=44).set_color(WARN),
                Tex(R"E[W \mid L \approx %d] = %s" % (self.focus, fmt(cmean)), font_size=32).set_color(MEAN_COLOR),
                Tex(R"\sigma_{W \mid L \approx %d} = %s" % (self.focus, fmt(csd)), font_size=32).set_color(CALM),
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

        wide = label("k 큼: 매끈하고 치우침", 26, MUTED).move_to(RIGHT * 4.4 + DOWN * 1.4)
        narrow = label("k 작음: 들쭉날쭉, 분산 큼", 26, MUTED).next_to(wide, DOWN, buff=0.2)
        self.play(FadeIn(wide), FadeIn(narrow))
        self.wait(2)
