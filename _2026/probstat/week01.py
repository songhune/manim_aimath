"""확률과통계 1주차 — 통계와 데이터 분석 개요.

강의 교안 `확률과통계/교안/01주차.md` 의 시각화 보조자료.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/probstat/week01.py
    ./render.sh check _2026/probstat/week01.py            # 전 씬 빠른 점검
    ./render.sh video _2026/probstat/week01.py MeanVsMedian
    ./render.sh ppt   _2026/probstat/week01.py MeanVsMedian   # PPT 삽입용 재인코딩
    ./render.sh all   _2026/probstat/week01.py            # 전부 1080p
"""
from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MED_COLOR, MUTED, WARN, BODY_FONT, TITLE_FONT,
    chito, crowd, counter, freeze, label, note, panel, ring, slide_title,
    swap, swap_pose, sweep, title, under,
)


def mascot(height=0.42):
    """치토 한 마리. 예전 이름을 쓰던 씬들이 아직 있어 남겨 둔다."""
    return chito("front", None, height)


def body(text, size=30, color=INK):
    """화면 문구. ps_common.label 과 같고, 길면 예외를 낸다.

    문장을 넣으려다 걸리면 그 문장은 교안 대본으로 옮기고 화면에는 이름만 남긴다.
    """
    return label(text, size, color)


def caption(text, ref, color=INK, size=28):
    """참조 도형 바로 아래에 놓는 문구."""
    return under(text, ref, color, size)


# ─────────────────────────────────────────────────────────────
# 1. 모집단과 표본 — 학기 내내 재사용하는 핵심 도식
# ─────────────────────────────────────────────────────────────
class PopulationAndSample(InteractiveScene):
    """교안 1주차 1교시 [15–40분]. 모집단 → 표본 → 추론의 순환.

    점 하나가 아니라 마스코트 하나가 사람 한 명이다. "모집단은 사람들의 모임"
    이라는 말이 그림에서 바로 보이도록 한다.
    """
    n_pop = 40                # 10열 × 4행
    n_sample = 12             # 4열 × 3행
    pop_height = 0.42
    sample_height = 0.62

    def construct(self):
        head = slide_title("Population and Sample")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 모집단: 마스코트 한 마리가 개체 하나
        rng = np.random.default_rng(0)
        pop = Group(*[mascot(self.pop_height) for _ in range(self.n_pop)])
        pop.arrange_in_grid(4, 10, buff=0.16)
        for m in pop:                       # 줄이 너무 반듯하면 무리처럼 안 보인다
            m.shift(rng.uniform(-0.035, 0.035, 3) * np.array([1, 1, 0]))

        pop_box = SurroundingRectangle(pop, buff=0.28)
        pop_box.set_stroke(GREY_C, 2).round_corners(0.15)
        pop_panel = Group(pop_box, pop)
        pop_panel.move_to(LEFT * 4.3 + UP * 0.5)

        pop_label = body("Population").next_to(pop_box, UP, buff=0.2)
        pop_param = Tex(R"\mu, \sigma^2").set_color(GREY_A)
        pop_param.next_to(pop_box, DOWN, buff=0.25)
        pop_note = body("usually unknown", 24, GREY_B)
        pop_note.next_to(pop_param, DOWN, buff=0.15)

        self.play(
            LaggedStartMap(FadeIn, pop, lag_ratio=0.02, run_time=1.6),
            FadeIn(pop_box), FadeIn(pop_label),
        )
        self.play(Write(pop_param), FadeIn(pop_note))
        self.wait()

        # ── 표본: 12명만 뽑는다. 나머지는 흐리게, 뽑힌 쪽은 테두리로 표시
        idx = sorted(rng.choice(self.n_pop, self.n_sample, replace=False))
        chosen = Group(*[pop[i] for i in idx])
        rest = Group(*[m for i, m in enumerate(pop) if i not in idx])

        rings = VGroup(*[
            SurroundingRectangle(m, buff=0.045).set_stroke(ACCENT, 3).round_corners(0.08)
            for m in chosen
        ])
        self.play(
            *[m.animate.set_opacity(0.22) for m in rest],
            LaggedStartMap(ShowCreation, rings, lag_ratio=0.06),
            run_time=1.2,
        )

        # 오른쪽 표본 자리 (배치용 기준틀)
        grid = Group(*[m.copy().set_height(self.sample_height) for m in chosen])
        grid.arrange_in_grid(3, 4, buff=0.18)
        smp_box = SurroundingRectangle(grid, buff=0.28)
        smp_box.set_stroke(ACCENT, 2).round_corners(0.15)
        Group(smp_box, grid).move_to(RIGHT * 4.5 + UP * 0.5)

        smp_label = body("Sample").next_to(smp_box, UP, buff=0.2)
        smp_stat = Tex(R"\bar{x}, s^2").set_color(ACCENT)
        smp_stat.next_to(smp_box, DOWN, buff=0.25)
        smp_note = body("computed from the data", 24, GREY_B)
        smp_note.next_to(smp_stat, DOWN, buff=0.15)

        draw_arrow = Arrow(pop_box.get_right(), smp_box.get_left(), buff=0.25)
        draw_arrow.set_color(ACCENT)
        draw_label = body("sampling", 24, ACCENT).next_to(draw_arrow, UP, buff=0.1)

        self.play(GrowArrow(draw_arrow), FadeIn(draw_label))

        flying = Group(*[m.copy() for m in chosen])
        self.add(flying)
        self.play(
            *[f.animate.set_height(self.sample_height).move_to(t)
              for f, t in zip(flying, grid)],
            FadeIn(smp_box), FadeIn(smp_label),
            run_time=1.6,
        )
        self.play(Write(smp_stat), FadeIn(smp_note))
        self.wait()

        # ── 되돌아가는 추론 화살표 (아래쪽 여백 안에서)
        start = smp_note.get_bottom() + DOWN * 0.2
        end = pop_note.get_bottom() + DOWN * 0.2
        back = CubicBezier(start, start + DOWN * 1.0, end + DOWN * 1.0, end)
        back.set_stroke(MEAN_COLOR, 4)
        tip = ArrowTip(angle=PI / 2).set_color(MEAN_COLOR).scale(0.5)
        tip.move_to(end)

        infer = body("inference", 30, MEAN_COLOR)
        infer.next_to(back, DOWN, buff=0.15)

        self.play(ShowCreation(back), FadeIn(tip))
        self.play(FadeIn(infer, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 평균 vs 중앙값 — 극단값 하나가 평균을 끌고 간다
# ─────────────────────────────────────────────────────────────
class MeanVsMedian(InteractiveScene):
    """교안 1주차 2교시 [0–30분]. 시소(무게중심) 비유.

    자료 1.7, 2.2, 3.11, 3.9, 14.7 에서 마지막 값을 오른쪽으로 끌면
    평균은 따라가지만 중앙값은 3.11에 그대로 있다.
    """
    data = [1.7, 2.2, 3.11, 3.9, 14.7]

    def construct(self):
        head = slide_title("Sample Mean and Sample Median")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        line = NumberLine(x_range=(0, 16, 2), width=11, include_numbers=True)
        line.move_to(UP * 0.3)
        self.play(ShowCreation(line), run_time=1.5)

        # 마지막 값만 tracker 로 움직인다
        last = ValueTracker(self.data[-1])
        fixed = self.data[:-1]

        def values():
            return [*fixed, last.get_value()]

        def mean_val():
            return sum(values()) / len(values())

        def med_val():
            s = sorted(values())
            n = len(s)
            return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

        dots = VGroup(*[
            Dot(line.n2p(v), radius=0.11).set_fill(ACCENT, 1) for v in fixed
        ])
        moving = Dot(radius=0.14).set_fill(WARN, 1)
        moving.f_always.move_to(lambda: line.n2p(last.get_value()))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.2), FadeIn(moving))

        # 평균 = 무게중심 받침점
        fulcrum = Triangle().set_height(0.32).rotate(PI)
        fulcrum.set_fill(MEAN_COLOR, 1).set_stroke(width=0)
        fulcrum.add_updater(lambda m: m.next_to(line.n2p(mean_val()), DOWN, buff=0.05))

        # 중앙값 = 순서상의 한가운데
        med_bar = Line(UP * 0.32, DOWN * 0.32).set_stroke(MED_COLOR, 5)
        med_bar.f_always.move_to(lambda: line.n2p(med_val()))

        readout = VGroup(
            VGroup(Tex(R"\bar{x} = ").set_color(MEAN_COLOR),
                   DecimalNumber(0, num_decimal_places=2).set_color(MEAN_COLOR)),
            VGroup(Tex(R"\tilde{x} = ").set_color(MED_COLOR),
                   DecimalNumber(0, num_decimal_places=2).set_color(MED_COLOR)),
        )
        for row in readout:
            row.arrange(RIGHT, buff=0.1)
        readout.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        readout.next_to(head[1], DOWN, buff=0.35).to_edge(RIGHT, buff=1.0)
        readout[0][1].f_always.set_value(mean_val)
        readout[1][1].f_always.set_value(med_val)

        self.play(FadeIn(fulcrum), FadeIn(med_bar), FadeIn(readout))
        self.wait()

        note = caption("largest value moves", line, WARN)
        note.shift(DOWN * 0.6)
        self.play(FadeIn(note, UP))

        self.play(last.animate.set_value(16), run_time=4, rate_func=linear)
        self.wait()

        concl = VGroup(
            body("mean follows", 30, MEAN_COLOR),
            body("median holds", 30, MED_COLOR),
        )
        concl.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(note, LEFT)
        self.play(FadeOut(note), run_time=0.4)
        self.play(FadeIn(concl, UP))
        self.wait(2)

        # 되돌리기 — 강의 중 반복 시연용
        self.play(last.animate.set_value(self.data[-1]), run_time=2)
        self.wait()


# ─────────────────────────────────────────────────────────────
# 3. 분산 — 편차를 정사각형 넓이로
# ─────────────────────────────────────────────────────────────
class VarianceAsSquares(InteractiveScene):
    """교안 1주차 2교시 [30–60분].

    "분산은 편차를 제곱한 것의 평균" 을 말이 아니라 넓이로 보여 준다.
    왜 제곱하는지(부호 상쇄 방지, 큰 편차에 큰 벌점)도 눈에 보인다.
    """
    data = [2, 4, 4, 4, 5, 5, 7, 9]

    def construct(self):
        head = slide_title("Sample Variance as an Average of Squares")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        mean = np.mean(self.data)
        var = np.var(self.data, ddof=1)

        line = NumberLine(x_range=(0, 10, 1), width=8.5, include_numbers=True)
        line.next_to(head[1], DOWN, buff=0.75)
        dots = VGroup(*[
            Dot(line.n2p(v), radius=0.09).set_fill(ACCENT, 1) for v in self.data
        ])
        mean_line = DashedLine(line.n2p(mean) + UP * 0.3, line.n2p(mean) + DOWN * 2.0)
        mean_line.set_stroke(MEAN_COLOR, 3)
        mean_tag = Tex(R"\bar{x}").set_color(MEAN_COLOR).next_to(mean_line, UP, buff=0.1)

        self.play(ShowCreation(line))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.play(ShowCreation(mean_line), FadeIn(mean_tag))
        self.wait()

        # ── ① 편차: 겹치지 않게 한 줄씩 아래로 쌓는다
        devs = VGroup(*[
            Line(line.n2p(mean), line.n2p(v)).shift(DOWN * (0.55 + 0.22 * i)).set_stroke(
                WARN if v < mean else CALM, 4
            )
            for i, v in enumerate(self.data)
        ])
        step = body("1. deviation from the mean", 28)
        step.next_to(devs, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        self.play(FadeIn(step), LaggedStartMap(ShowCreation, devs, lag_ratio=0.15))
        self.wait()

        # ── ② 제곱: 편차를 한 변으로 하는 정사각형
        k = 1.7 / max(abs(v - mean) for v in self.data)   # 가장 큰 사각형이 1.7 이 되도록
        squares = VGroup(*[
            Square(side_length=max(abs(v - mean), 0.12) * k).set_style(
                fill_color=WARN if v < mean else CALM, fill_opacity=0.35,
                stroke_color=WARN if v < mean else CALM, stroke_width=2,
            )
            for v in self.data
        ])
        squares.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        squares.next_to(step, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)

        step2 = body("2. square each deviation", 28)
        step2.move_to(step, LEFT)
        self.play(FadeOut(step), run_time=0.4)
        self.play(FadeIn(step2), run_time=0.4)
        self.play(
            LaggedStart(*[
                TransformFromCopy(d, s) for d, s in zip(devs, squares)
            ], lag_ratio=0.1),
            run_time=2,
        )
        self.wait()

        # ── ③ 평균 넓이 = 분산
        avg_sq = Square(side_length=np.sqrt(var) * k).set_style(
            fill_color=MEAN_COLOR, fill_opacity=0.3,
            stroke_color=MEAN_COLOR, stroke_width=3,
        )
        avg_sq.next_to(squares, RIGHT, buff=1.2, aligned_edge=DOWN)
        arrow = Arrow(squares.get_right(), avg_sq.get_left(), buff=0.25)
        arrow.set_color(MEAN_COLOR)
        avg_tag = body("average area", 24, MEAN_COLOR).next_to(arrow, UP, buff=0.1)

        formula = Tex(R"s^2 = \frac{\sum (x_i-\bar{x})^2}{n-1}").set_color(MEAN_COLOR)
        formula.scale(0.85).next_to(avg_sq, RIGHT, buff=0.5)
        s_tag = body(f"side = s = {np.sqrt(var):.2f}", 24, MEAN_COLOR)
        s_tag.next_to(avg_sq, DOWN, buff=0.2)

        step3 = body("3. average the areas, over n − 1", 28, MEAN_COLOR)
        step3.move_to(step2, LEFT)
        self.play(FadeOut(step2), run_time=0.4)
        self.play(FadeIn(step3), run_time=0.4)
        self.play(GrowArrow(arrow), FadeIn(avg_tag))
        self.play(TransformFromCopy(squares, avg_sq), Write(formula))
        self.play(FadeIn(s_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 막대그래프 vs 히스토그램
# ─────────────────────────────────────────────────────────────
class BarVsHistogram(InteractiveScene):
    """교안 1주차 2교시 [60–85분]. 붙어 있느냐 떨어져 있느냐가 전부."""

    def construct(self):
        head = slide_title("Bar Chart and Histogram")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        def make_bars(values, color, buff):
            bars = VGroup(*[
                Rectangle(width=0.75, height=v).set_style(
                    fill_color=color, fill_opacity=0.8,
                    stroke_color=color, stroke_width=2,
                )
                for v in values
            ])
            bars.arrange(RIGHT, buff=buff, aligned_edge=DOWN)
            return bars

        # 왼쪽: 막대그래프 (범주형 → 떨어뜨린다)
        bars = make_bars([1.9, 2.2, 0.5, 0.25], ACCENT, buff=0.45)
        bar_labels = VGroup(*[
            body(c, 24).next_to(b, DOWN, buff=0.15)
            for c, b in zip(["O", "A", "B", "AB"], bars)
        ])
        bar_panel = VGroup(bars, bar_labels)

        # 오른쪽: 히스토그램 (연속형 → 붙인다)
        hbars = make_bars([0.5, 1.3, 2.4, 1.7, 0.9], CALM, buff=0)
        hbar_labels = VGroup(*[
            body(t, 18).next_to(b, DOWN, buff=0.15)
            for t, b in zip(["0~10", "10~20", "20~30", "30~40", "40~50"], hbars)
        ])
        hist_panel = VGroup(hbars, hbar_labels)

        panels = VGroup(bar_panel, hist_panel)
        panels.arrange(RIGHT, buff=1.6, aligned_edge=DOWN)
        panels.next_to(head[1], DOWN, buff=1.5)

        bar_title = body("Bar chart: categorical data", 28, ACCENT).next_to(bars, UP, buff=0.5)
        hist_title = body("Histogram: continuous data", 28, CALM).next_to(hbars, UP, buff=0.5)

        self.play(
            LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.15),
            FadeIn(bar_labels), FadeIn(bar_title),
        )
        self.play(
            LaggedStartMap(GrowFromEdge, hbars, edge=DOWN, lag_ratio=0.15),
            FadeIn(hbar_labels), FadeIn(hist_title),
        )
        self.wait()

        # 차이를 못 박는다
        gap = Rectangle(
            width=bars[1].get_left()[0] - bars[0].get_right()[0],
            height=bars.get_height(),
        )
        gap.set_style(fill_color=MEAN_COLOR, fill_opacity=0.25, stroke_width=0)
        gap.next_to(bars[0], RIGHT, buff=0).align_to(bars, DOWN)
        gap_note = VGroup(
            body("The bars are separated.", 22, MEAN_COLOR),
            body("The categories are not adjacent.", 22, MEAN_COLOR),
        ).arrange(DOWN, buff=0.15)
        gap_note.next_to(bar_labels, DOWN, buff=0.5)

        seam = Line(hbars[2].get_corner(UL), hbars[2].get_corner(DL))
        seam.set_stroke(MEAN_COLOR, 6)
        seam_note = VGroup(
            body("The bars touch.", 22, MEAN_COLOR),
            body("The classes are adjacent.", 22, MEAN_COLOR),
        ).arrange(DOWN, buff=0.15)
        seam_note.next_to(hbar_labels, DOWN, buff=0.5)

        self.play(FadeIn(gap), FadeIn(gap_note))
        self.play(ShowCreation(seam), FadeIn(seam_note))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 치우침 — 꼬리가 있는 쪽으로 평균이 끌려간다
# ─────────────────────────────────────────────────────────────
class Skewness(InteractiveScene):
    """교안 1주차 2교시 [60–85분] 마무리. 평균·중앙값 위치로 모양을 읽는다."""

    specs = [
        ("Skewed left", -1.0, R"\bar{x} < \tilde{x}"),
        ("Symmetric", 0.0, R"\bar{x} = \tilde{x}"),
        ("Skewed right", 1.0, R"\bar{x} > \tilde{x}"),
    ]

    def construct(self):
        head = slide_title("Skewness")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        panels = VGroup(*[self.make_panel(*spec) for spec in self.specs])
        panels.arrange(RIGHT, buff=0.6).next_to(head[1], DOWN, buff=0.9)

        for p in panels:
            self.play(
                ShowCreation(p[0]), FadeIn(p[1]), ShowCreation(p[2]), FadeIn(p[5]),
                run_time=0.7,
            )
        self.wait()
        self.play(
            *[ShowCreation(p[3]) for p in panels],
            *[ShowCreation(p[4]) for p in panels],
        )
        self.play(*[FadeIn(p[6]) for p in panels])

        legend = VGroup(*[
            VGroup(Line(ORIGIN, RIGHT * 0.45).set_stroke(color, 4), body(name, 24, color))
            for name, color in [("mean", MEAN_COLOR), ("median", MED_COLOR)]
        ])
        for row in legend:
            row.arrange(RIGHT, buff=0.2)
        legend.arrange(RIGHT, buff=1.0).next_to(panels, DOWN, buff=0.5)
        self.play(FadeIn(legend))

        punch = body("mean follows the tail", 30, MEAN_COLOR)
        punch.next_to(legend, DOWN, buff=0.4)
        self.play(FadeIn(punch, UP))
        self.wait(2)

    def make_panel(self, label, skew, relation):
        axes = Axes(
            x_range=(-3, 3, 1), y_range=(0, 0.6, 0.2),
            width=3.5, height=1.9,
            axis_config=dict(include_ticks=False, stroke_width=2),
        )
        axes.y_axis.set_stroke(width=0)      # 세로축은 평균선과 헷갈리므로 감춘다

        def f(x):
            return np.exp(-x ** 2 / 2) * (1 + np.tanh(skew * x * 1.2)) / 2.2

        graph = axes.get_graph(f, x_range=(-3, 3, 0.05)).set_stroke(ACCENT, 3)
        fill = graph.copy()
        fill.add_line_to(axes.c2p(3, 0))
        fill.add_line_to(axes.c2p(-3, 0))
        fill.set_style(fill_color=ACCENT, fill_opacity=0.18, stroke_width=0)

        xs = np.linspace(-3, 3, 601)
        ys = np.array([f(x) for x in xs])
        weights = ys / ys.sum()
        mean = float((xs * weights).sum())
        med = float(xs[np.searchsorted(np.cumsum(weights), 0.5)])

        mean_line = Line(axes.c2p(mean, 0), axes.c2p(mean, f(mean)))
        mean_line.set_stroke(MEAN_COLOR, 4)
        med_line = DashedLine(axes.c2p(med, 0), axes.c2p(med, f(med)))
        med_line.set_stroke(MED_COLOR, 4)

        cap = body(label, 24).next_to(axes, DOWN, buff=0.3)
        rel = Tex(relation).scale(0.75).next_to(cap, DOWN, buff=0.15)

        return VGroup(axes, fill, graph, mean_line, med_line, cap, rel)


# ─────────────────────────────────────────────────────────────
# 6. 변동 — 흩어지지 않으면 통계는 필요 없다
# ─────────────────────────────────────────────────────────────
class WhyVariability(InteractiveScene):
    """교안 1주차 1교시 [15–40분] 도입.

    같은 공정에서 만든 부품 10개의 길이를 잰다. 값이 전부 같다면 한 개만 재면
    되고 통계는 할 일이 없다. 실제로는 흩어지고, 그 흩어짐이 통계학의 대상이다.
    """
    nominal = 50.0
    lengths = [49.82, 50.11, 49.95, 50.24, 49.68,
               50.03, 49.91, 50.17, 49.87, 50.06]

    def construct(self):
        head = slide_title("Variability")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        setup = body("ten parts, one process", 30)
        setup.next_to(head[1], DOWN, buff=0.4)
        self.play(FadeIn(setup, UP))

        line = NumberLine(
            x_range=(49.5, 50.5, 0.25), width=10.5,
            decimal_number_config=dict(num_decimal_places=2),
            include_numbers=True,
        )
        line.move_to(DOWN * 1.0)
        self.play(ShowCreation(line), run_time=1.2)

        # ── ① 흩어짐이 없다면. 한 자리에 열 개를 세로로 쌓아 "전부 같다"를 보인다.
        dots = VGroup(*[
            Dot(line.n2p(self.nominal), radius=0.10).set_fill(ACCENT, 1)
            .shift(UP * 0.24 * (i + 1))
            for i in range(len(self.lengths))
        ])
        step1 = body("1. one value, one answer", 28, GREY_B)
        step1.next_to(line, DOWN, buff=0.9)

        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.08), FadeIn(step1))
        self.wait(1.0)

        # ── ② 실제로는 흩어진다
        step2 = body("2. Measured values scatter.", 28, ACCENT)
        step2.move_to(step1)
        self.play(FadeOut(step1), run_time=0.4)
        self.play(
            *[d.animate.move_to(line.n2p(v)).shift(UP * 0.24 * (i + 1))
              for i, (d, v) in enumerate(zip(dots, self.lengths))],
            FadeIn(step2),
            run_time=2,
        )
        self.wait(1.0)

        # ── ③ 그래서 두 가지를 묻는다: 어디쯤인가 / 얼마나 퍼졌나
        mean = float(np.mean(self.lengths))
        fulcrum = Triangle().set_height(0.30).rotate(PI)
        fulcrum.set_fill(MEAN_COLOR, 1).set_stroke(width=0)
        fulcrum.next_to(line.n2p(mean), DOWN, buff=0.05)
        mean_tag = Tex(R"\bar{x}").set_color(MEAN_COLOR)
        mean_tag.next_to(fulcrum, DOWN, buff=0.12)

        lo, hi = min(self.lengths), max(self.lengths)
        span = Line(line.n2p(lo), line.n2p(hi))
        span.set_y(dots.get_top()[1] + 0.35)      # 점 무리 바로 위
        span.set_stroke(WARN, 4)
        ticks = VGroup(*[
            Line(UP * 0.12, DOWN * 0.12).set_stroke(WARN, 4).move_to(p)
            for p in [span.get_start(), span.get_end()]
        ])
        span_tag = body(f"range R = {hi - lo:.2f}", 24, WARN)
        span_tag.next_to(span, UP, buff=0.12)

        step3 = body("3. location and spread", 28, MEAN_COLOR)
        step3.move_to(step2)
        # 범위 막대가 들어갈 자리라서 위쪽 설명은 여기서 걷는다
        self.play(FadeOut(step2), FadeOut(setup), run_time=0.4)
        self.play(FadeIn(step3), run_time=0.4)
        self.play(FadeIn(fulcrum), Write(mean_tag))
        self.play(ShowCreation(span), ShowCreation(ticks), FadeIn(span_tag))
        self.wait(0.8)

        punch = Tex(R"\bar{x} \qquad s^2").set_color(MEAN_COLOR).scale(1.2)
        punch.next_to(mean_tag, DOWN, buff=0.9)
        self.play(FadeOut(step3), run_time=0.4)
        self.play(FadeIn(punch, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 확률과 통계 — 화살표의 방향이 반대다
# ─────────────────────────────────────────────────────────────
class ProbabilityVsInference(InteractiveScene):
    """교안 1주차 §1.4. 확률은 모집단 → 표본, 통계는 표본 → 모집단.

    `PopulationAndSample` 다음에 이어서 쓴다. 같은 두 상자를 두 번 쓰되
    화살표만 뒤집어, 학기 전반부(확률)와 후반부(통계)의 위치를 못 박는다.
    """

    def construct(self):
        head = slide_title("Probability and Statistical Inference")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        def box(text, sub, color):
            """네 상자의 크기를 같게 고정한다. 글자 길이에 따라 폭이 달라지면
            좌우가 어긋나 '같은 두 상자를 화살표만 뒤집었다'가 흐려진다."""
            inner = VGroup(body(text, 30, color), body(sub, 20, GREY_B))
            inner.arrange(DOWN, buff=0.15)
            frame = RoundedRectangle(width=3.8, height=1.6, corner_radius=0.12)
            frame.set_stroke(color, 2)
            inner.move_to(frame)
            return VGroup(frame, inner)

        def row(left_box, right_box, arrow_label, color, direction):
            left_box.move_to(LEFT * 3.7)
            right_box.move_to(RIGHT * 3.7)
            if direction is RIGHT:
                arrow = Arrow(left_box.get_right(), right_box.get_left(), buff=0.3)
            else:
                arrow = Arrow(right_box.get_left(), left_box.get_right(), buff=0.3)
            arrow.set_color(color)
            tag = body(arrow_label, 26, color).next_to(arrow, UP, buff=0.15)
            return VGroup(left_box, right_box, arrow, tag)

        # ── 위: 확률 (모집단 → 표본)
        prob = row(
            box("Population", "properties known", CALM),
            box("Sample", "what values appear?", CALM),
            "probability", CALM, RIGHT,
        )
        prob.next_to(head[1], DOWN, buff=0.7)

        # ── 아래: 통계 (표본 → 모집단)
        stat = row(
            box("Population", "properties unknown", ACCENT),
            box("Sample", "values observed", ACCENT),
            "statistical inference", ACCENT, LEFT,
        )
        stat.next_to(prob, DOWN, buff=1.3)

        for group, when in [(prob, "Ch. 2–7"), (stat, "Ch. 8–11")]:
            when_tag = body(when, 22, GREY_B).next_to(group, LEFT, buff=0.35)
            group.add(when_tag)

        self.play(FadeIn(prob[0]), FadeIn(prob[1]), FadeIn(prob[4]))
        self.play(GrowArrow(prob[2]), FadeIn(prob[3]))
        self.wait(0.8)

        self.play(FadeIn(stat[0]), FadeIn(stat[1]), FadeIn(stat[4]))
        self.play(GrowArrow(stat[2]), FadeIn(stat[3]))
        self.wait(0.8)

        punch = body("opposite directions", 32, MEAN_COLOR)
        punch.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(punch, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 편향표본 — 크기보다 뽑는 방법이 먼저다
# ─────────────────────────────────────────────────────────────
# 참고: legacy/_2020/med_test.py 의 SamplePopulationBreastCancer
# 아이콘 무리를 이름 붙인 상자로 다시 모으고, 뽑힌 개체마다 테두리를 두르고,
# 훑는 선으로 '조사했다'를 보이는 화면 문법을 여기서 가져왔다. 코드는 옮기지 않았다.
class BiasedSample(InteractiveScene):
    """교안 1주차 1교시 [65–85분]. 슬라이드 6 (Collection of data) 뒤.

    강의 만족도를 마지막 수업에 나온 학생에게만 묻는다. 불만인 학생이 통째로
    빠지므로 답이 계속 틀린다.

    말로 "표본이 크다고 편향이 없어지지 않는다" 고 하면 그 말만 남는다. 그래서
    마지막에 n 을 40 → 400 → 4000 으로 키운다. 구간은 눈에 띄게 좁아지는데
    참값 60% 자리로는 끝내 오지 않는다. 좁아지는 것과 맞는 것이 다르다는 것이
    그림에 남는다.

    불만인 학생은 붉은 치토가 뒤로 돌아선다. 색과 자세를 함께 바꾸면 강의실
    뒷자리에서도, 색을 잘 못 가려도 구분된다.
    """
    n_happy = 24
    n_unhappy = 16
    n_absent = 13             # 불만인 16명 중 결석
    seed = 3

    def construct(self):
        head = slide_title("Biased Sample")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        n_total = self.n_happy + self.n_unhappy
        rng = np.random.default_rng(self.seed)
        unhappy_idx = set(rng.choice(n_total, self.n_unhappy, replace=False).tolist())

        # ── 모집단 40명. 만족은 청록, 불만은 빨강.
        people = Group(*[
            chito("front", "red" if i in unhappy_idx else "teal", 0.62)
            for i in range(n_total)
        ])
        people.arrange_in_grid(4, 10, buff=0.2)
        people.move_to(UP * 0.75)
        for m in people:
            m.shift(rng.uniform(-0.03, 0.03, 3) * np.array([1, 1, 0]))

        n_all = ValueTracker(0)
        all_num = counter(n_all, color=WHITE, size=56)
        all_num.next_to(people, RIGHT, buff=0.6)
        self.add(all_num)
        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.03),
                  n_all.animate.set_value(n_total), run_time=2.0)
        self.wait(0.4)

        # ── 두 무리로 갈라 세운다. 비율이 자리로 보인다.
        happy = Group(*[m for i, m in enumerate(people) if i not in unhappy_idx])
        sad = Group(*[m for i, m in enumerate(people) if i in unhappy_idx])
        for g, cols, x in [(happy, 6, -3.1), (sad, 4, 2.9)]:
            g.generate_target()
            g.target.arrange_in_grid(4, cols, buff=0.2)
            g.target.move_to(np.array([x, 0.75, 0]))

        freeze(all_num)
        self.play(MoveToTarget(happy), MoveToTarget(sad),
                  FadeOut(all_num), run_time=1.6)

        box_h = panel(happy.target, CALM)
        box_s = panel(sad.target, WARN)
        tag_h = label("satisfied", 26, CALM).next_to(box_h, UP, buff=0.18)
        tag_s = label("dissatisfied", 26, WARN).next_to(box_s, UP, buff=0.18)
        num_h = counter(ValueTracker(self.n_happy), color=CALM, size=44)
        num_h.next_to(box_h, DOWN, buff=0.2)
        n_sad = ValueTracker(self.n_unhappy)
        num_s = counter(n_sad, color=WARN, size=44)
        num_s.next_to(box_s, DOWN, buff=0.2)
        self.play(FadeIn(box_h), FadeIn(tag_h), FadeIn(num_h),
                  FadeIn(box_s), FadeIn(tag_s), FadeIn(num_s))

        truth = Tex(R"\frac{24}{40} = 60\%").set_color(MEAN_COLOR).scale(0.95)
        truth.next_to(VGroup(box_h, box_s), DOWN, buff=1.0).set_x(0)
        truth_tag = label("true rate", 26, MEAN_COLOR).next_to(truth, DOWN, buff=0.2)
        self.play(Write(truth), FadeIn(truth_tag))
        self.wait(1.2)

        # ── 불만인 쪽 13명이 뒤로 돌아 나간다
        gone = list(sad)[:self.n_absent]
        turned = swap_pose(self, gone, "back", "red", run_time=1.0)
        self.wait(0.9)          # 등을 돌린 그림이 한 박자 남아야 읽힌다
        self.play(
            LaggedStart(*[FadeOut(m, shift=DOWN * 1.6, scale=0.7) for m in turned],
                        lag_ratio=0.06),
            n_sad.animate.set_value(self.n_unhappy - self.n_absent),
            run_time=1.8,
        )
        self.wait(0.4)

        # ── 남은 사람만 조사한다
        stay = Group(*happy, *list(sad)[self.n_absent:])
        sweep(self, stay, color=CALM, run_time=2.0,
              from_edge=np.array([0, -FRAME_HEIGHT / 2, 0]))
        rings = VGroup(*[ring(m, MEAN_COLOR, buff=0.03, width=2) for m in stay])
        self.play(LaggedStartMap(ShowCreation, rings, lag_ratio=0.02), run_time=1.2)

        observed = Tex(R"\frac{24}{27} = 89\%").set_color(WARN).scale(0.95)
        observed.move_to(truth)
        obs_tag = label("observed rate", 26, WARN).next_to(observed, DOWN, buff=0.2)
        self.play(FadeOut(truth), FadeOut(truth_tag), run_time=0.4)
        self.play(FadeIn(observed), FadeIn(obs_tag), run_time=0.4)
        self.play(FlashAround(observed, color=WARN, buff=0.2), run_time=1.2)
        self.wait(1.4)

        # ── 표본을 키운다. 구간은 좁아지고 자리는 그대로다.
        freeze(num_h, num_s)
        self.play(*[FadeOut(m) for m in [
            people, rings, box_h, box_s, tag_h, tag_s, num_h, num_s,
            observed, obs_tag]], run_time=0.8)

        axis = NumberLine(
            x_range=(50, 100, 10), width=11.0,
            include_numbers=True, decimal_number_config=dict(num_decimal_places=0),
        )
        axis.move_to(DOWN * 0.4)
        axis.numbers.set_color(GREY_B)
        pct = label("percent satisfied", 24, GREY_B).next_to(axis, DOWN, buff=0.5)

        true_x = axis.n2p(60)
        true_line = Line(true_x + UP * 1.5, true_x + DOWN * 0.35)
        true_line.set_stroke(MEAN_COLOR, 4)
        true_lab = Tex("60\\%").set_color(MEAN_COLOR).scale(0.8)
        true_lab.next_to(true_line, UP, buff=0.15)

        self.play(ShowCreation(axis), FadeIn(pct))
        self.play(ShowCreation(true_line), FadeIn(true_lab))

        # 관측값 89% 를 중심으로 한 95% 구간. n 이 커져도 중심은 그대로다.
        p = 24 / 27
        n_size = ValueTracker(40)

        def half_width():
            return 1.96 * np.sqrt(p * (1 - p) / n_size.get_value()) * 100

        band = Rectangle(height=0.55)
        band.set_stroke(WARN, 2).set_fill(WARN, 0.3)
        band.add_updater(lambda m: m.set_width(
            axis.n2p(89 + half_width())[0] - axis.n2p(89 - half_width())[0],
            stretch=True).move_to(axis.n2p(89) + UP * 0.75))

        dot = Dot(radius=0.09).set_fill(WARN, 1).move_to(axis.n2p(89) + UP * 0.75)
        n_tag = label("sample size", 24, GREY_A)
        n_num = counter(n_size, color=WHITE, size=52)
        n_tag.move_to(np.array([-4.4, 2.3, 0]))
        n_num.next_to(n_tag, DOWN, buff=0.15)

        self.add(band, n_num)
        self.play(FadeIn(band), FadeIn(dot), FadeIn(n_tag), run_time=0.8)
        self.wait(0.8)
        for target in (400, 4000):
            self.play(n_size.animate.set_value(target), run_time=1.8)
            self.wait(0.7)

        band.clear_updaters()
        self.play(FlashAround(true_line, color=MEAN_COLOR, buff=0.15),
                  FlashAround(dot, color=WARN, buff=0.25), run_time=1.4)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
class HistogramFromTable(InteractiveScene):
    """교안 1주차 2교시 [60–85분]. PS1_01 슬라이드 12 의 표가 그림이 되는 과정.

    표만 보면 히스토그램은 '숫자를 옮겨 그린 것'으로 남는다. 도수가 막대 높이로
    올라가는 것을 눈으로 보여 준 다음 세로축을 상대도수로 바꾼다. 넓이의 합이 1이
    되는 순간이 6주차 확률밀도함수로 이어지는 자리다.
    """
    classes = ["0–10", "10–20", "20–30", "30–40", "40–50"]
    freqs = [1, 3, 6, 4, 2]
    bar_width = 0.78
    unit = 0.42               # 도수 1 당 세로 길이

    def construct(self):
        head = slide_title("From Frequency Table to Histogram")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table = self.make_table()
        table.next_to(head[1], DOWN, buff=0.6).to_edge(LEFT, buff=0.9)
        self.play(FadeIn(table[0]), ShowCreation(table[1]), run_time=1.2)

        # ── 막대는 붙여 세운다. buff 를 0 으로 둔 것이 이 그림의 요점이다.
        bars = VGroup(*[
            Rectangle(width=self.bar_width, height=f * self.unit).set_style(
                fill_color=CALM, fill_opacity=0.75,
                stroke_color=CALM, stroke_width=2,
            )
            for f in self.freqs
        ])
        bars.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        bars.next_to(head[1], DOWN, buff=1.25).to_edge(RIGHT, buff=1.6)

        base = Line(bars.get_corner(DL), bars.get_corner(DR))
        base.set_stroke(GREY_B, 2)
        axis = Line(bars.get_corner(DL), bars.get_corner(DL) + UP * (7 * self.unit))
        axis.set_stroke(GREY_B, 2)
        edge_labels = VGroup(*[
            body(t, 17, GREY_B).next_to(b, DOWN, buff=0.16)
            for t, b in zip(self.classes, bars)
        ])
        self.play(ShowCreation(axis), ShowCreation(base))

        # 표의 도수가 막대 높이로 올라간다
        for row, bar, lab in zip(table[0][1:-1], bars, edge_labels):
            flying = row[1].deepcopy()
            self.play(
                flying.animate.move_to(bar).set_opacity(0),
                GrowFromEdge(bar, DOWN),
                FadeIn(lab),
                run_time=0.55,
            )
            self.remove(flying)
        self.wait(0.5)

        y_ticks = self.make_y_axis(axis, [0, 2, 4, 6], lambda v: str(v))
        y_name = body("Frequency", 22, GREY_B)
        y_name.next_to(axis, UP, buff=0.25)
        self.play(FadeIn(y_ticks), FadeIn(y_name))
        self.wait(0.8)

        # ── 붙어 있다는 사실을 못 박는다
        seams = VGroup(*[
            Line(b.get_corner(UL), b.get_corner(DL)).set_stroke(MEAN_COLOR, 6)
            for b in bars[1:]
        ])
        seam_note = body("bars touch", 28, MEAN_COLOR)
        seam_note.next_to(edge_labels, DOWN, buff=0.42)
        self.play(LaggedStartMap(ShowCreation, seams, lag_ratio=0.15), FadeIn(seam_note))
        self.wait(1.2)
        self.play(FadeOut(seams), FadeOut(seam_note), run_time=0.4)

        # ── 세로축을 상대도수로 바꾼다. 모양은 그대로, 눈금만 달라진다.
        n = sum(self.freqs)
        rel_note = VGroup(
            Tex(R"\frac{\text{frequency}}{%d}" % n).set_color(ACCENT).scale(0.7),
            body("same shape, new scale", 26, ACCENT),
        ).arrange(DOWN, buff=0.2)
        rel_note.next_to(edge_labels, DOWN, buff=0.42)

        rel_ticks = self.make_y_axis(
            axis, [0, 2, 4, 6], lambda v: f"{v / n:.3f}".lstrip("0"))
        rel_name = body("Relative frequency", 22, ACCENT).move_to(y_name)

        self.play(FadeOut(y_ticks), FadeOut(y_name), run_time=0.3)
        self.play(FadeIn(rel_ticks), FadeIn(rel_name), FadeIn(rel_note))
        self.wait(1.2)

        area = body("Total area = 1", 30, MEAN_COLOR)
        area.next_to(rel_note, DOWN, buff=0.3)
        bridge = note("density, Chapter 6", 24, MEAN_COLOR)
        bridge.next_to(area, DOWN, buff=0.2)
        self.play(bars.animate.set_fill(opacity=0.35), FadeIn(area))
        self.play(FadeIn(bridge, UP))
        self.wait(2)

    def make_y_axis(self, axis, values, fmt):
        """세로축 눈금과 숫자. 값은 도수 단위로 받는다."""
        marks = VGroup()
        for v in values:
            p = axis.get_start() + UP * v * self.unit
            tick = Line(p + LEFT * 0.09, p + RIGHT * 0.09).set_stroke(GREY_B, 2)
            num = body(fmt(v), 18, GREY_B).next_to(tick, LEFT, buff=0.12)
            marks.add(VGroup(tick, num))
        return marks

    def make_table(self):
        """헤더 + 자료 행 + 합계 행. 강의 슬라이드의 인쇄용 표와 같은 모양으로 둔다.

        VGroup(rows, grid) 를 돌려준다. 자료 행은 rows[1:-1] 이다.
        """
        col_w = (2.1, 1.35)
        row_h = 0.52

        def cell_row(left, right, color=INK):
            a = body(left, 24, color)
            b = body(right, 24, color)
            a.move_to(LEFT * col_w[0] / 2)
            b.move_to(RIGHT * col_w[1] / 2)
            return VGroup(a, b)

        rows = VGroup(cell_row("Class", "Freq."))
        rows.add(*[cell_row(c, str(f)) for c, f in zip(self.classes, self.freqs)])
        rows.add(cell_row("Total", str(sum(self.freqs)), MEAN_COLOR))
        rows.arrange(DOWN, buff=row_h - 0.24)

        w, h = sum(col_w), rows.get_height() + 0.4
        grid = VGroup()
        grid.add(Rectangle(width=w, height=h).set_stroke(GREY_B, 2))
        grid.add(Line(UP * h / 2, DOWN * h / 2).shift(
            RIGHT * (col_w[0] / 2 - col_w[1] / 2) * 0 + LEFT * 0 + RIGHT * (w / 2 - col_w[1])
        ).set_stroke(GREY_B, 2))
        for i in range(len(rows) - 1):
            y = (rows[i].get_bottom()[1] + rows[i + 1].get_top()[1]) / 2 - rows.get_center()[1]
            grid.add(Line(LEFT * w / 2, RIGHT * w / 2).shift(UP * y).set_stroke(GREY_B, 2))
        grid.move_to(rows)

        # 한 mobject 를 두 그룹에 넣으면 이동이 두 번 먹어 화면 밖으로 나간다.
        # 자료 행은 rows[1:-1] 로 꺼내 쓴다.
        return VGroup(rows, grid)


# ─────────────────────────────────────────────────────────────
# 10. 정의 1.3 — 표본분산 공식을 조각으로 읽는다
# ─────────────────────────────────────────────────────────────
class VarianceFormula(InteractiveScene):
    """교안 1주차 2교시 [30–60분]. 슬라이드 9 의 정의 1.3 을 조각내어 읽는다.

    `VarianceAsSquares` 가 '왜 제곱인가'를 그림으로 보여 준다면 이 씬은 같은 이야기를
    기호 쪽에서 한 번 더 밟는다. 학생이 시험지에서 만나는 것은 결국 이 한 줄이다.
    """
    data = [2.0, 3.5, 4.0, 6.5, 9.0]

    def construct(self):
        head = slide_title("Definition 1.3  Sample Variance")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 조각을 따로 만들어 늘어놓는다. 한 덩어리로 쓰면 조각마다 상자를 두를 수 없다.
        s2 = Tex(R"s^2")
        eq = Tex(R"=")
        frac = Tex(R"{1 \over n - 1}")
        sigma = Tex(R"\sum_{i=1}^{n}")
        dev = Tex(R"\left( x_i - \bar{x} \right)")
        formula = VGroup(s2, eq, frac, sigma, dev)
        formula.arrange(RIGHT, buff=0.22).scale(1.5)
        sq = Tex(R"2").scale(0.9)
        sq.next_to(dev.get_corner(UR), RIGHT, buff=0.04).shift(DOWN * 0.12)
        whole = VGroup(formula, sq)
        whole.next_to(head[1], DOWN, buff=0.95)

        line, dots, mean_mark = self.make_number_line()
        strip = VGroup(line, dots, mean_mark)
        strip.next_to(whole, DOWN, buff=1.05)

        self.play(ShowCreation(line), LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.play(ShowCreation(mean_mark[0]), FadeIn(mean_mark[1]))
        self.wait(0.4)

        # ── 1) 편차. 그냥 더하면 0 이 되어 버린다.
        self.play(FadeIn(dev))
        self.highlight(dev, "Deviation from the mean", ACCENT, strip)

        zero = Tex(R"\sum (x_i - \bar{x}) = 0").scale(0.9).set_color(WARN)
        zero.next_to(strip, DOWN, buff=0.45)
        zero_note = body("Adding them undoes the work.", 26, WARN)
        zero_note.next_to(zero, DOWN, buff=0.22)
        self.play(FadeIn(zero))
        self.play(FadeIn(zero_note))
        self.wait(1.2)
        self.play(FadeOut(zero), FadeOut(zero_note), run_time=0.4)

        # ── 2) 제곱
        self.play(Write(sq))
        self.highlight(sq, "Square, so nothing cancels", CALM, strip)

        # ── 3) 합
        self.play(Write(sigma))
        self.highlight(sigma, "Add over all n observations", ACCENT, strip)

        # ── 4) n − 1 로 나눈다
        self.play(Write(frac))
        self.highlight(frac, "An average, but over n - 1", MEAN_COLOR, strip)
        # 자유도를 말로 풀면 그 말만 남는다. 편차의 합이 0 이라는 제약을 보인다.
        why = VGroup(
            Tex(R"\sum_{i=1}^{n} (x_i - \bar{x}) = 0").set_color(MEAN_COLOR).scale(0.85),
            body("one constraint", 26, MEAN_COLOR),
        ).arrange(DOWN, buff=0.2).next_to(strip, DOWN, buff=0.45)
        self.play(FadeIn(why))
        self.wait(1.4)
        self.play(FadeOut(why), run_time=0.4)

        self.play(Write(VGroup(s2, eq)))
        self.wait(0.6)

        # ── 마무리: 자료와 단위가 같은 것은 s 다.
        # 수직선은 할 일을 마쳤으므로 거둔다. 두지 않아야 아래 두 줄이 화면에 들어온다.
        self.play(FadeOut(strip), run_time=0.4)
        sd = Tex(R"s = \sqrt{s^2}").scale(1.3).set_color(CALM)
        sd.next_to(whole, DOWN, buff=1.0)
        unit = body("s has the unit of x", 28, CALM)
        unit.next_to(sd, DOWN, buff=0.45)
        self.play(Write(sd))
        self.play(FadeIn(unit, UP))
        self.wait(2)

    def highlight(self, part, text, color, ref):
        """공식 한 조각에 상자를 두르고 이름을 붙였다가 상자만 거둔다."""
        box = SurroundingRectangle(part, buff=0.1).set_stroke(color, 3)
        label = body(text, 28, color).next_to(ref, DOWN, buff=0.45)
        self.play(ShowCreation(box), FadeIn(label))
        self.wait(0.8)
        self.play(FadeOut(box), FadeOut(label), run_time=0.35)

    def make_number_line(self):
        line = NumberLine(x_range=(0, 10, 2), width=8, include_numbers=True)
        line.numbers.set_color(GREY_B)
        line.set_stroke(GREY_B, 2)

        dots = VGroup(*[
            Dot(line.n2p(x), radius=0.09).set_color(ACCENT) for x in self.data
        ])
        xbar = sum(self.data) / len(self.data)
        mark = Line(line.n2p(xbar) + DOWN * 0.3, line.n2p(xbar) + UP * 0.55)
        mark.set_stroke(MEAN_COLOR, 4)
        tag = Tex(R"\bar{x}").set_color(MEAN_COLOR).next_to(mark, UP, buff=0.1)
        return line, dots, VGroup(mark, tag)
