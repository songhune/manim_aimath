# -*- coding: utf-8 -*-
"""확률과통계 「확률변수와 확률분포」 장 (Walpole Chapter 3) — 확률변수 · pmf · pdf · cdf · 결합 · 주변 · 조건부 · 독립.

강의 교안 `확률과통계/교육메모/04주차.md` 의 「영상 계획」(2026-09-14) 을 옮긴 것이다. 도구와 규칙은 week02.py 와 같다.
개념 영상은 개념 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음·풀이 슬라이드 앞이다(하네스 3.6).
소재는 덱(PS1_03_restyled.pptx, 46장)의 예제로 한정한다. 화면 문구는 영어, 여섯 낱말까지.

2주차에서 이어 쓰는 그림 셋 — 넓이 모형(정사각형 → 곡선 아래 넓이 → 결합밀도), 조각 하나를 남겨 늘리기
(조건부확률 → 조건부분포), 세어서 고르기(조합 → 예제 3.8 · 3.14). 새로 나오는 그림은 계단(이산 cdf)뿐이다.
사람은 치토다(3.8): 예제 3.2 의 Smith · Jones · Brown.

덱 삽입 자리 (원본 PS1_03_restyled.pptx 기준. insert_videos.py 의 PS1_03 job 과 같다):
    5차 9/15
    RandomVariableAsFunction        3 앞    정의 3.1 (예제 3.1 의 항아리. 결과 → 수)
    DiscreteVsContinuous            7 앞    예제 3.4–3.7 (셀 수 있는 점 · 꽉 찬 구간)
    PmfAsBars                       8 앞    정의 3.4 (예제 3.1 의 값 위에 막대)
    Example38Laptops                9 뒤    예제 3.8 (풀이 10 앞)
    Example32Helmets               11 앞    (다시) 예제 3.2 (치토 셋에게 헬멧 여섯 가지로)
    Example310Cdf                  12 뒤    예제 3.10 (풀이 13 앞. 계단)
    PdfAsArea                      14 앞    정의 3.6 (곡선 아래 넓이, P(X = a) = 0)
    Example311Temperature          15 뒤    예제 3.11 (풀이 16 앞)
    Example312Cdf                  17 뒤    예제 3.12 (풀이 18 앞. 왼쪽부터 쌓은 넓이)
    Example313Bid                  19 뒤    예제 3.13 (풀이 20 앞. 직사각형 밀도)
    6차 9/18
    JointDistributionGrid          21 앞    정의 3.8 (이산 pmf 격자 → 연속 pdf 부피, 2026-09-18 개정)
    Example314Pens                 22 뒤    예제 3.14 (풀이 23 앞. 단계 넷을 걸고 하나씩, 2026-09-18 개정)
    Example315DriveIn              25 뒤    예제 3.15 (그림 26 앞. 단위 정사각형 위의 부피)
    MarginalAsRowSums              27 앞    정의 3.10 (행 합 · 열 합)
    ConditionalDistributionSlice   31 앞    정의 3.11 (한 행만 남기고 늘리기)
    Example319Spectrum             34 뒤    예제 3.19 (풀이 35 앞. 삼각형 정의역)
    Example320Rectangle            37 뒤    예제 3.20 (풀이 38 앞. 직사각형 정의역)
    IndependenceProductCheck       39 앞    정의 3.12 (반례 한 칸, 정의역 둘)
    Example322ShelfLife            44 뒤    예제 3.22 (풀이 45 앞. e^{-x} 셋의 곱)

렌더 (저장소 루트에서):
    ./render.sh check _2026/probstat/week04.py
    ./render.sh ppt   _2026/probstat/week04.py Example32Helmets
"""
from math import comb

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN, BODY_FONT,
    chito, label, note, panel, ring, slide_title, bar,
)
from _2026.probstat.week02 import letter_chip

GREEN_PEN = GREEN_C


# ─────────────────────────────────────────────────────────────
# 도구 — 공, 칸, 격자표, 밀도 곡선
# ─────────────────────────────────────────────────────────────
def ball(color, r=0.19):
    return Circle(radius=r).set_fill(color, 1).set_stroke(WHITE, 1.2)


def frac(num, den, color=INK, scale=0.8):
    return Tex(R"\frac{%s}{%s}" % (num, den)).set_color(color).scale(scale)


def grid_table(vals, x_labels, y_labels, w=1.15, h=0.72, corner=R"f(x,y)", x_name="x", y_name="y"):
    """표 3.1 꼴의 격자. vals[i][j] 는 i번째 행(y), j번째 열(x) 의 LaTeX.
    돌려주는 것: (전체 VGroup, cells[(i,j)] 사각형, texts[(i,j)] 수식, 머리글)."""
    rows, cols = len(vals), len(vals[0])
    cells, texts = {}, {}
    grid = VGroup()
    for i in range(rows):
        for j in range(cols):
            rect = Rectangle(width=w, height=h).set_stroke(GREY_C, 1.5)
            rect.move_to([j * w, -i * h, 0])
            t = Tex(vals[i][j]).scale(0.75).set_color(INK).move_to(rect)
            cells[(i, j)], texts[(i, j)] = rect, t
            grid.add(rect, t)
    heads = VGroup()
    for j, xl in enumerate(x_labels):
        heads.add(Tex(xl).scale(0.75).set_color(ACCENT).move_to([j * w, h * 0.85, 0]))
    for i, yl in enumerate(y_labels):
        heads.add(Tex(yl).scale(0.75).set_color(WARN).move_to([-w * 0.8, -i * h, 0]))
    heads.add(Tex(x_name).scale(0.7).set_color(ACCENT).move_to([(cols - 1) * w / 2, h * 1.55, 0]))
    heads.add(Tex(y_name).scale(0.7).set_color(WARN).move_to([-w * 1.45, -(rows - 1) * h / 2, 0]))
    heads.add(Tex(corner).scale(0.6).set_color(GREY_B).move_to([-w * 0.8, h * 0.85, 0]))
    whole = VGroup(grid, heads)
    return whole, cells, texts, heads


TABLE31 = [[R"\tfrac{3}{28}", R"\tfrac{9}{28}", R"\tfrac{3}{28}"],
           [R"\tfrac{6}{28}", R"\tfrac{6}{28}", R"0"],
           [R"\tfrac{1}{28}", R"0", R"0"]]


def density_axes(x_range, y_range, width=6.0, height=3.4):
    axes = Axes(x_range=x_range, y_range=y_range, width=width, height=height,
                axis_config=dict(include_ticks=False, stroke_width=2, stroke_color=GREY_B))
    return axes


def area_under(axes, graph, a, b, color=ACCENT, opacity=0.4):
    return axes.get_area_under_graph(graph, x_range=(a, b), fill_color=color, fill_opacity=opacity)


def x_marks(axes, xs, texts=None, color=GREY_B):
    texts = texts or [str(x) for x in xs]
    return VGroup(*[Tex(t).scale(0.6).set_color(color).next_to(axes.c2p(x, 0), DOWN, buff=0.12)
                    for x, t in zip(xs, texts)])


# ─────────────────────────────────────────────────────────────
# 1. 확률변수 = 결과에 수를 붙이는 규칙 (3.1) — 슬라이드 3 (정의 3.1) 앞
# ─────────────────────────────────────────────────────────────
class RandomVariableAsFunction(InteractiveScene):
    """예제 3.1 의 항아리. 두 개를 뽑은 결과 넷에 화살표로 2·1·1·0 을 붙인다. 화살표 규칙이 Y, 닿은 수가 y."""

    def construct(self):
        head = slide_title("Random Variable")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        balls = VGroup(*[ball(WARN) for _ in range(4)], *[ball(GREY_B) for _ in range(3)])
        balls.arrange_in_grid(2, 4, buff=0.18).move_to([-4.6, 0.9, 0])
        urn = panel(balls, MUTED, buff=0.3)
        tag = note("4 red, 3 black", 24, GREY_B).next_to(urn, DOWN, buff=0.2)
        self.play(FadeIn(urn), LaggedStartMap(FadeIn, balls, lag_ratio=0.08), FadeIn(tag))
        self.wait(0.4)

        combos = [(WARN, WARN, "RR"), (WARN, GREY_B, "RB"), (GREY_B, WARN, "BR"), (GREY_B, GREY_B, "BB")]
        outcomes = VGroup()
        for c1, c2, name in combos:
            pair = VGroup(ball(c1, 0.17), ball(c2, 0.17)).arrange(RIGHT, buff=0.08)
            txt = note(name, 24, INK).next_to(pair, RIGHT, buff=0.25)
            outcomes.add(VGroup(pair, txt))
        outcomes.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([-0.9, 0.2, 0])
        col_tag = note("outcome", 24, GREY_B).next_to(outcomes, UP, buff=0.35)
        self.play(FadeIn(col_tag), LaggedStartMap(FadeIn, outcomes, lag_ratio=0.2, shift=RIGHT * 0.3), run_time=1.4)
        self.wait(0.4)

        rule = Tex(R"Y = \text{number of red balls}").scale(0.8).set_color(MEAN_COLOR).move_to([3.4, 2.4, 0])
        self.play(Write(rule))
        nums = VGroup()
        arrows = VGroup()
        for row, val in zip(outcomes, [2, 1, 1, 0]):
            n = Tex(str(val)).scale(1.1).set_color(MEAN_COLOR).move_to([3.4, row.get_y(), 0])
            a = Arrow(row.get_right() + RIGHT * 0.1, n.get_left() + LEFT * 0.1, buff=0.05, stroke_width=3).set_color(MEAN_COLOR)
            nums.add(n)
            arrows.add(a)
        for a, n in zip(arrows, nums):
            self.play(GrowArrow(a), FadeIn(n, scale=0.6), run_time=0.5)
        y_tag = note("y", 24, GREY_B).next_to(nums, UP, buff=0.35)
        self.play(FadeIn(y_tag))
        self.wait(0.6)

        brace = Brace(arrows, DOWN, buff=0.25).set_color(MEAN_COLOR)
        rule_tag = label("rule: outcome to number", 26, MEAN_COLOR).next_to(brace, DOWN, buff=0.15)
        self.play(GrowFromCenter(brace), FadeIn(rule_tag))
        self.wait(0.8)
        vals = Tex(R"y = 2, 1, 1, 0").set_color(INK).scale(0.9).next_to(rule_tag, DOWN, buff=0.35)
        self.play(FadeIn(vals))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 이산 vs 연속 — 슬라이드 7 (예제 3.4–3.7) 앞
# ─────────────────────────────────────────────────────────────
class DiscreteVsContinuous(InteractiveScene):
    """수직선 둘. 위는 셀 수 있는 점(불량품 수 0…10), 아래는 꽉 찬 구간(온도 오차)."""

    def construct(self):
        head = slide_title("Discrete, Continuous")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        top = NumberLine(x_range=(0, 10, 1), width=9, include_numbers=True).move_to([0, 1.2, 0])
        top_tag = label("defectives in 10 items", 26, ACCENT).next_to(top, UP, buff=0.4)
        dots = VGroup(*[Dot(top.n2p(k), radius=0.09).set_color(ACCENT) for k in range(11)])
        self.play(ShowCreation(top), FadeIn(top_tag))
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.08, scale=0.5), run_time=1.0)
        d_tag = note("countable points", 24, ACCENT).next_to(top, DOWN, buff=0.45)
        self.play(FadeIn(d_tag))
        self.wait(0.8)

        bot = NumberLine(x_range=(-1, 2, 1), width=9, include_numbers=True).move_to([0, -1.6, 0])
        bot_tag = label("temperature error", 26, CALM).next_to(bot, UP, buff=0.4)
        band = Line(bot.n2p(-1), bot.n2p(2)).set_stroke(CALM, 14, opacity=0.6)
        self.play(ShowCreation(bot), FadeIn(bot_tag))
        self.play(ShowCreation(band), run_time=1.0)
        c_tag = note("every value in between", 24, CALM).next_to(bot, DOWN, buff=0.45)
        self.play(FadeIn(c_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. pmf = 값 위에 세운 막대, 높이 합 1 — 슬라이드 8 (정의 3.4) 앞
# ─────────────────────────────────────────────────────────────
class PmfAsBars(InteractiveScene):
    """예제 3.1 의 Y 값 0·1·2 위에 막대 3/21·12/21·6/21. 세 조건."""
    probs = [(3, 21), (12, 21), (6, 21)]

    def construct(self):
        head = slide_title("Probability Mass Function")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        base = Line(LEFT * 3.2, RIGHT * 3.2).set_stroke(GREY_B, 2).move_to([-2.6, -2.2, 0])
        xs = [-4.4, -2.6, -0.8]
        ticks = VGroup(*[Tex(str(k)).scale(0.8).set_color(GREY_B).move_to([x, -2.6, 0]) for k, x in enumerate(xs)])
        y_tag = Tex("y").scale(0.8).set_color(GREY_B).next_to(base, RIGHT, buff=0.2)
        self.play(ShowCreation(base), FadeIn(ticks), FadeIn(y_tag))

        bars = VGroup()
        labels = VGroup()
        for (n, d), x in zip(self.probs, xs):
            b = bar(n / d, 1.0, width=1.1, height=4.2, color=ACCENT)
            b.move_to([x, -2.2, 0], aligned_edge=DOWN)
            f = frac(n, d, INK, 0.7).next_to(b, UP, buff=0.12)
            bars.add(b)
            labels.add(f)
        for b, f in zip(bars, labels):
            self.play(GrowFromEdge(b, DOWN), FadeIn(f), run_time=0.6)
        name = Tex(R"f(y) = P(Y = y)").set_color(ACCENT).scale(0.9).move_to([3.6, 1.6, 0])
        self.play(Write(name))
        self.wait(0.6)

        total = Tex(R"\frac{3}{21} + \frac{12}{21} + \frac{6}{21} = 1").scale(0.85).set_color(MEAN_COLOR)
        total.next_to(name, DOWN, buff=0.6)
        self.play(TransformFromCopy(labels, total), run_time=1.2)
        self.wait(0.6)

        conds = VGroup(
            Tex(R"1.\ f(y) \ge 0"),
            Tex(R"2.\ \sum_y f(y) = 1"),
            Tex(R"3.\ P(Y = y) = f(y)"),
        ).scale(0.75).set_color(INK).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conds.next_to(total, DOWN, buff=0.6).align_to(name, LEFT)
        for c in conds:
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FlashAround(total, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 예제 3.8 노트북 20대 중 불량 3, 2대 구입 — 슬라이드 9 뒤 (풀이 10 앞)
# ─────────────────────────────────────────────────────────────
class Example38Laptops(InteractiveScene):
    """20 칸 중 D 셋. 두 자리를 고르는 방법 C(20,2)=190. 불량 x 대는 C(3,x)C(17,2−x)."""

    def construct(self):
        head = slide_title("Example 3.8")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        kinds = ["D"] * 3 + ["N"] * 17
        chips = VGroup(*[letter_chip(k, 0.5, WARN if k == "D" else MUTED) for k in kinds])
        chips.arrange_in_grid(2, 10, buff=0.12).move_to([-2.4, 1.7, 0])
        box = panel(chips, MUTED, buff=0.2)
        tag = note("20 laptops, 3 defective", 22, GREY_B).next_to(box, DOWN, buff=0.15)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, chips, lag_ratio=0.03), FadeIn(tag), run_time=1.2)

        pick = Tex(R"\binom{20}{2} = 190").scale(0.9).set_color(INK).move_to([4.6, 1.7, 0])
        pick_tag = note("choose 2", 22, GREY_B).next_to(pick, UP, buff=0.15)
        self.play(FadeIn(pick_tag), Write(pick))
        self.wait(0.5)

        formula = Tex(R"f(x) = \frac{\binom{3}{x}\binom{17}{2-x}}{\binom{20}{2}}",
                      t2c={R"\binom{3}{x}": WARN, R"\binom{17}{2-x}": MUTED}).scale(0.9)
        formula.move_to([-3.6, -0.9, 0])
        self.play(Write(formula))
        self.wait(0.4)

        rows = [("0", R"\frac{1 \cdot 136}{190}", R"\frac{68}{95}"),
                ("1", R"\frac{3 \cdot 17}{190}", R"\frac{51}{190}"),
                ("2", R"\frac{3 \cdot 1}{190}", R"\frac{3}{190}")]
        lines = VGroup()
        for x, mid, val in rows:
            t = Tex(R"f(%s) = %s = %s" % (x, mid, val)).scale(0.8).set_color(INK)
            lines.add(t)
        lines.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([2.9, -1.1, 0])
        for x, t in zip([0, 1, 2], lines):
            marks = VGroup(*[ring(c, WARN, 0.04) for c in chips[:x]], *[ring(c, MUTED, 0.04) for c in chips[3:5 - x]])
            self.play(ShowCreation(marks), FadeIn(t, shift=RIGHT * 0.2), run_time=0.7)
            self.wait(0.3)
            self.play(FadeOut(marks), run_time=0.25)

        total = Tex(R"\frac{136 + 51 + 3}{190} = 1").scale(0.85).set_color(MEAN_COLOR)
        total.next_to(lines, DOWN, buff=0.4).align_to(lines, LEFT)
        self.play(Write(total))
        self.play(FlashAround(total, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 예제 3.2 헬멧 — 슬라이드 11 ((다시) 예제 3.2) 앞. 치토 셋
# ─────────────────────────────────────────────────────────────
class Example32Helmets(InteractiveScene):
    """Smith·Jones·Brown 이 헬멧 S·J·B 를 여섯 가지 순서로 돌려받는다. 제 것을 받은 수 M."""
    orders = ["SJB", "SBJ", "BJS", "JSB", "JBS", "BSJ"]

    def construct(self):
        head = slide_title("Example 3.2")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        names = ["Smith", "Jones", "Brown"]
        tints = ["teal", "red", "gold"]
        people = Group(*[chito("front", t, 1.0) for t in tints]).arrange(RIGHT, buff=1.3).move_to([-2.9, -0.6, 0])
        tags = VGroup(*[note(n, 22, GREY_B).next_to(p, DOWN, buff=0.12) for n, p in zip(names, people)])
        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.2), FadeIn(tags))

        colors = {"S": CALM, "J": WARN, "B": MEAN_COLOR}
        helmets = {ch: letter_chip(ch, 0.62, colors[ch]) for ch in "SJB"}
        slots = [p.get_top() + UP * 0.55 for p in people]
        for ch, p in zip("SJB", people):
            helmets[ch].move_to(p.get_top() + UP * 0.55)
        own = VGroup(*helmets.values())
        own_tag = note("own helmet", 22, GREY_B).next_to(own, UP, buff=0.25)
        self.play(FadeIn(own, shift=DOWN * 0.2), FadeIn(own_tag))
        self.wait(0.6)
        self.play(FadeOut(own_tag))

        m_tex = Tex("M").scale(0.9).set_color(MEAN_COLOR).move_to([3.2, 2.2, 0])
        m_tag = note("correct matches", 22, GREY_B).next_to(m_tex, RIGHT, buff=0.25)
        self.play(FadeIn(m_tex), FadeIn(m_tag))

        tally = VGroup()
        for k, order in enumerate(self.orders):
            targets = {ch: slots[i] for i, ch in enumerate(order)}
            self.play(*[helmets[ch].animate.move_to(targets[ch]) for ch in "SJB"], run_time=0.7)
            hits = [i for i, ch in enumerate(order) if ch == "SJB"[i]]
            marks = VGroup(*[ring(helmets["SJB"[i]], MEAN_COLOR, 0.05) for i in hits])
            m = len(hits)
            row = VGroup(note(order, 22, INK), Tex(str(m)).scale(0.8).set_color(MEAN_COLOR)).arrange(RIGHT, buff=0.5)
            row.move_to([3.6, 1.4 - k * 0.5, 0])
            self.play(ShowCreation(marks), FadeIn(row, shift=RIGHT * 0.2), run_time=0.45)
            tally.add(row)
            self.wait(0.2)
            self.play(FadeOut(marks), run_time=0.2)
        self.wait(0.5)

        dist = VGroup(
            Tex(R"f(0) = \frac{2}{6}"), Tex(R"f(1) = \frac{3}{6}"), Tex(R"f(3) = \frac{1}{6}"),
        ).scale(0.8).set_color(INK).arrange(RIGHT, buff=0.6).move_to([-2.9, -2.9, 0])
        self.play(TransformFromCopy(tally, dist), run_time=1.2)
        none = label("no order with M = 2", 26, WARN).move_to([3.6, -2.2, 0])
        self.play(FadeIn(none))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 예제 3.10 이산 cdf = 계단 — 슬라이드 12 뒤 (풀이 13 앞)
# ─────────────────────────────────────────────────────────────
class Example310Cdf(InteractiveScene):
    """예제 3.9 의 막대 1·4·6·4·1 (/16) 을 왼쪽부터 쌓아 계단. F(2)−F(1) = 6/16 = f(2)."""
    probs = [1, 4, 6, 4, 1]

    def construct(self):
        head = slide_title("Example 3.10")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 왼쪽: pmf 막대
        xs = [-6.0 + 0.9 * k for k in range(5)]
        base = Line([-6.5, -2.4, 0], [-2.0, -2.4, 0]).set_stroke(GREY_B, 2)
        ticks = VGroup(*[Tex(str(k)).scale(0.7).set_color(GREY_B).move_to([x, -2.75, 0]) for k, x in enumerate(xs)])
        bars = VGroup()
        labs = VGroup()
        for p, x in zip(self.probs, xs):
            b = bar(p, 16, width=0.7, height=3.2, color=ACCENT).move_to([x, -2.4, 0], aligned_edge=DOWN)
            bars.add(b)
            labs.add(frac(p, 16, INK, 0.55).next_to(b, UP, buff=0.08))
        f_tag = Tex(R"f(x)").scale(0.8).set_color(ACCENT).move_to([-4.2, 1.6, 0])
        self.play(ShowCreation(base), FadeIn(ticks), FadeIn(f_tag))
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.15), FadeIn(labs), run_time=1.2)
        self.wait(0.5)

        # 오른쪽: 계단
        x0, y0 = 0.4, -2.4
        unit_x, unit_y = 1.1, 3.2
        base2 = Line([x0 - 0.4, y0, 0], [x0 + 5 * unit_x, y0, 0]).set_stroke(GREY_B, 2)
        axis2 = Line([x0, y0, 0], [x0, y0 + unit_y + 0.3, 0]).set_stroke(GREY_B, 2)
        ticks2 = VGroup(*[Tex(str(k)).scale(0.7).set_color(GREY_B).move_to([x0 + k * unit_x, y0 - 0.35, 0]) for k in range(5)])
        F_tag = Tex(R"F(x)").scale(0.8).set_color(MEAN_COLOR).move_to([x0 + 0.9, y0 + unit_y + 0.3, 0])
        self.play(ShowCreation(base2), ShowCreation(axis2), FadeIn(ticks2), FadeIn(F_tag))

        cum = 0
        steps = VGroup()
        step_labels = VGroup()
        for k, p in enumerate(self.probs):
            cum += p
            y = y0 + unit_y * cum / 16
            seg = Line([x0 + k * unit_x, y, 0], [x0 + (k + 1) * unit_x, y, 0]).set_stroke(MEAN_COLOR, 5)
            riser = DashedLine([x0 + k * unit_x, y0 + unit_y * (cum - p) / 16, 0], [x0 + k * unit_x, y, 0]).set_stroke(MEAN_COLOR, 2)
            lab = frac(cum, 16, MEAN_COLOR, 0.55).next_to(seg, UP, buff=0.08)
            flying = bars[k].copy()
            self.play(flying.animate.set_opacity(0).move_to(seg), ShowCreation(riser), ShowCreation(seg), FadeIn(lab), run_time=0.6)
            self.remove(flying)
            steps.add(seg, riser)
            step_labels.add(lab)
        self.wait(0.6)

        # F(2) − F(1) = f(2)
        y1 = y0 + unit_y * 5 / 16
        y2 = y0 + unit_y * 11 / 16
        brace = Brace(Line([x0 + 2 * unit_x, y1, 0], [x0 + 2 * unit_x, y2, 0]), RIGHT, buff=0.1).set_color(WARN)
        diff = Tex(R"F(2) - F(1) = \frac{11}{16} - \frac{5}{16} = \frac{3}{8} = f(2)").scale(0.8).set_color(WARN)
        diff.move_to([3.2, 2.5, 0])
        self.play(GrowFromCenter(brace), bars[2].animate.set_fill(WARN, 0.9).set_stroke(WARN, 2), Write(diff))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. pdf = 곡선 아래 넓이, 폭 0 인 띠는 넓이 0 — 슬라이드 14 (정의 3.6) 앞
# ─────────────────────────────────────────────────────────────
class PdfAsArea(InteractiveScene):
    """정사각형(2장의 넓이 모형)이 곡선 아래 넓이가 된다. P(a<X<b) 는 색칠한 넓이.
    a 에서 띠를 좁히면 0. 그래서 P(a<X≤b) = P(a<X<b)."""

    def construct(self):
        head = slide_title("Probability Density Function")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 단위 정사각형 → 넓이 1
        sq = Square(side_length=2.6).set_stroke(GREY_B, 2).set_fill(ACCENT, 0.25).move_to([-4.2, -0.4, 0])
        one = Tex("1").set_color(INK).move_to(sq)
        sq_tag = note("area = 1", 24, GREY_B).next_to(sq, DOWN, buff=0.2)
        self.play(ShowCreation(sq), FadeIn(one), FadeIn(sq_tag))
        self.wait(0.5)

        axes = density_axes((-0.2, 4.2, 1), (0, 1.0, 0.5), width=7.2, height=3.4).move_to([2.2, -0.6, 0])
        f = lambda x: 0.75 * np.exp(-((x - 2) ** 2) / 0.9)
        graph = axes.get_graph(f, x_range=(0, 4, 0.02)).set_stroke(CALM, 3)
        whole = area_under(axes, graph, 0, 4, ACCENT, 0.25)
        f_tag = Tex("f(x)").scale(0.8).set_color(CALM).next_to(graph.get_top(), UP, buff=0.15)
        self.play(ShowCreation(axes), ShowCreation(graph), FadeIn(f_tag))
        self.play(ReplacementTransform(sq, whole), FadeOut(one), FadeOut(sq_tag), run_time=1.2)
        total = Tex(R"\int_{-\infty}^{\infty} f(x)\,dx = 1").scale(0.8).set_color(INK).move_to([-4.2, 0.2, 0])
        self.play(Write(total))
        self.wait(0.6)

        # a<X<b
        a, b = 1.3, 2.6
        piece = area_under(axes, graph, a, b, MEAN_COLOR, 0.6)
        marks = x_marks(axes, [a, b], ["a", "b"])
        prob = Tex(R"P(a < X < b) = \int_a^b f(x)\,dx").scale(0.8).set_color(MEAN_COLOR).move_to([-4.2, -1.4, 0])
        self.play(FadeOut(whole), FadeIn(piece), FadeIn(marks), Write(prob))
        self.wait(0.8)

        # 띠를 좁힌다
        w = ValueTracker(0.6)
        strip = always_redraw(lambda: area_under(axes, graph, a - w.get_value() / 2, a + w.get_value() / 2, WARN, 0.8))
        self.play(FadeOut(piece), FadeIn(strip))
        self.play(w.animate.set_value(0.01), run_time=2.0)
        zero = Tex(R"P(X = a) = 0").scale(0.8).set_color(WARN).next_to(prob, DOWN, buff=0.35).align_to(prob, LEFT)
        self.play(Write(zero))
        self.wait(0.6)
        same = Tex(R"P(a < X \le b) = P(a < X < b)").scale(0.8).set_color(INK).next_to(zero, DOWN, buff=0.35).align_to(prob, LEFT)
        self.play(FadeOut(strip), FadeIn(piece), Write(same))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 예제 3.11 f(x) = x²/3 (−1<x<2) — 슬라이드 15 뒤 (풀이 16 앞)
# ─────────────────────────────────────────────────────────────
class Example311Temperature(InteractiveScene):
    """전체 넓이 1 을 적분으로 확인하고, 0~1 조각 1/9 를 색칠한다. 부정적분 → 위끝·아래끝 대입."""

    def construct(self):
        head = slide_title("Example 3.11")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((-1.6, 2.6, 1), (0, 1.5, 0.5), width=6.4, height=3.6).move_to([-3.4, -0.6, 0])
        f = lambda x: x ** 2 / 3
        graph = axes.get_graph(f, x_range=(-1, 2, 0.02)).set_stroke(CALM, 3)
        zero_l = axes.get_graph(lambda x: 0, x_range=(-1.6, -1, 0.1)).set_stroke(CALM, 3)
        zero_r = axes.get_graph(lambda x: 0, x_range=(2, 2.6, 0.1)).set_stroke(CALM, 3)
        marks = x_marks(axes, [-1, 0, 1, 2])
        f_tag = Tex(R"f(x) = \frac{x^2}{3}").scale(0.8).set_color(CALM).move_to(axes.c2p(0.3, 1.25))
        self.play(ShowCreation(axes), FadeIn(marks))
        self.play(ShowCreation(graph), ShowCreation(zero_l), ShowCreation(zero_r), FadeIn(f_tag))

        whole = area_under(axes, graph, -1, 2, ACCENT, 0.3)
        self.play(FadeIn(whole))
        s1 = Tex(R"\int_{-1}^{2} \frac{x^2}{3}\,dx = \left[\frac{x^3}{9}\right]_{-1}^{2}").scale(0.8).set_color(INK)
        s2 = Tex(R"= \frac{8}{9} - \left(-\frac{1}{9}\right) = 1").scale(0.8).set_color(MEAN_COLOR)
        steps = VGroup(s1, s2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.4, 1.3, 0])
        self.play(Write(s1))
        self.wait(0.4)
        self.play(Write(s2))
        self.wait(0.8)

        piece = area_under(axes, graph, 0, 1, MEAN_COLOR, 0.7)
        self.play(FadeOut(whole), FadeIn(piece))
        p1 = Tex(R"P(0 < X \le 1) = \int_{0}^{1} \frac{x^2}{3}\,dx").scale(0.8).set_color(INK)
        p2 = Tex(R"= \left[\frac{x^3}{9}\right]_{0}^{1} = \frac{1}{9}").scale(0.8).set_color(MEAN_COLOR)
        ps = VGroup(p1, p2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(steps, DOWN, buff=0.7).align_to(steps, LEFT)
        self.play(Write(p1))
        self.play(Write(p2))
        self.play(FlashAround(p2, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 예제 3.12 연속 cdf = 왼쪽부터 쌓은 넓이 — 슬라이드 17 뒤 (풀이 18 앞)
# ─────────────────────────────────────────────────────────────
class Example312Cdf(InteractiveScene):
    """x 가 −1 에서 2 로 가는 동안 왼쪽 넓이가 쌓이고 오른쪽 F(x) = (x³+1)/9 가 매끄럽게 오른다."""

    def construct(self):
        head = slide_title("Example 3.12")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((-1.6, 2.6, 1), (0, 1.5, 0.5), width=6.0, height=3.2).move_to([-3.6, -0.8, 0])
        f = lambda x: x ** 2 / 3
        graph = axes.get_graph(f, x_range=(-1, 2, 0.02)).set_stroke(CALM, 3)
        f_tag = Tex(R"f(x)").scale(0.8).set_color(CALM).move_to(axes.c2p(-0.6, 1.2))
        self.play(ShowCreation(axes), FadeIn(x_marks(axes, [-1, 0, 1, 2])), ShowCreation(graph), FadeIn(f_tag))

        axes2 = density_axes((-1.6, 2.6, 1), (0, 1.2, 0.5), width=6.0, height=3.2).move_to([3.6, -0.8, 0])
        F = lambda x: (x ** 3 + 1) / 9
        F_tag = Tex(R"F(x) = \frac{x^3 + 1}{9}").scale(0.8).set_color(MEAN_COLOR).move_to(axes2.c2p(-0.5, 0.72))
        one_line = DashedLine(axes2.c2p(-1.6, 1), axes2.c2p(2.6, 1)).set_stroke(GREY_C, 1.5)
        self.play(ShowCreation(axes2), FadeIn(x_marks(axes2, [-1, 0, 1, 2])), ShowCreation(one_line),
                  FadeIn(Tex("1").scale(0.6).set_color(GREY_B).next_to(axes2.c2p(-1.6, 1), LEFT, buff=0.1)))

        t = ValueTracker(-1.0)
        area = always_redraw(lambda: area_under(axes, graph, -1, max(t.get_value(), -0.999), ACCENT, 0.5))
        curve = always_redraw(lambda: axes2.get_graph(F, x_range=(-1, max(t.get_value(), -0.999), 0.02)).set_stroke(MEAN_COLOR, 4))
        dot = always_redraw(lambda: Dot(axes2.c2p(t.get_value(), F(t.get_value())), radius=0.08).set_color(MEAN_COLOR))
        self.add(area, curve, dot)
        self.play(t.animate.set_value(2.0), run_time=3.0, rate_func=linear)
        self.play(FadeIn(F_tag))
        self.wait(0.5)

        deriv = Tex(R"F(x) = \int_{-1}^{x} \frac{t^2}{3}\,dt = \left[\frac{t^3}{9}\right]_{-1}^{x}").scale(0.75).set_color(INK)
        deriv.move_to([0, 2.15, 0])
        self.play(Write(deriv))
        self.wait(0.6)

        # F(1) − F(0)
        self.play(t.animate.set_value(1.0), run_time=0.8)
        area.clear_updaters()
        curve.clear_updaters()
        dot.clear_updaters()
        piece = area_under(axes, graph, 0, 1, MEAN_COLOR, 0.8)
        h1 = DashedLine(axes2.c2p(1, 0), axes2.c2p(1, F(1))).set_stroke(MEAN_COLOR, 2)
        h0 = DashedLine(axes2.c2p(0, 0), axes2.c2p(0, F(0))).set_stroke(MEAN_COLOR, 2)
        ans = Tex(R"F(1) - F(0) = \frac{2}{9} - \frac{1}{9} = \frac{1}{9}").scale(0.8).set_color(MEAN_COLOR)
        ans.move_to([0, -3.3, 0])
        self.play(FadeIn(piece), ShowCreation(h0), ShowCreation(h1), Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 예제 3.13 높이 5/8 의 직사각형 밀도 (b = 1) — 슬라이드 19 뒤 (풀이 20 앞)
# ─────────────────────────────────────────────────────────────
class Example313Bid(InteractiveScene):
    """f(y) = 5/8 on [2/5, 2]. F(y) 는 직선으로 오르고 P(Y<1) = (5/8)(3/5) = 3/8."""

    def construct(self):
        head = slide_title("Example 3.13")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = density_axes((0, 2.4, 1), (0, 1.0, 0.5), width=6.4, height=3.2).move_to([-3.4, -0.8, 0])
        f = lambda y: 5 / 8
        graph = axes.get_graph(f, x_range=(0.4, 2, 0.1)).set_stroke(CALM, 3)
        marks = x_marks(axes, [0.4, 1, 2], [R"\tfrac{2}{5}", "1", "2"])
        f_tag = Tex(R"f(y) = \frac{5}{8}").scale(0.8).set_color(CALM).move_to(axes.c2p(1.2, 0.85))
        b_tag = note("b = 1", 22, GREY_B).next_to(f_tag, RIGHT, buff=0.5)
        self.play(ShowCreation(axes), FadeIn(marks), ShowCreation(graph), FadeIn(f_tag), FadeIn(b_tag))
        whole = area_under(axes, graph, 0.4, 2, ACCENT, 0.3)
        one = Tex(R"\frac{8}{5} \cdot \frac{5}{8} = 1").scale(0.75).set_color(INK).move_to(axes.c2p(1.2, 0.3))
        self.play(FadeIn(whole), Write(one))
        self.wait(0.6)

        piece = area_under(axes, graph, 0.4, 1, MEAN_COLOR, 0.7)
        self.play(FadeOut(one), FadeOut(whole), FadeIn(piece))
        s1 = Tex(R"F(y) = \int_{2/5}^{y} \frac{5}{8}\,dt = \frac{5y}{8} - \frac{1}{4}").scale(0.8).set_color(INK)
        s2 = Tex(R"P(Y < 1) = F(1) = \frac{5}{8} - \frac{1}{4} = \frac{3}{8}").scale(0.8).set_color(MEAN_COLOR)
        s3 = Tex(R"\text{width } \frac{3}{5} \times \text{height } \frac{5}{8} = \frac{3}{8}").scale(0.75).set_color(GREY_B)
        steps = VGroup(s1, s2, s3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.5, 0.3, 0])
        self.play(Write(s1))
        self.wait(0.3)
        self.play(Write(s2))
        self.wait(0.3)
        self.play(FadeIn(s3))
        self.play(FlashAround(s2, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 결합분포 = 격자 — 슬라이드 21 (정의 3.8) 앞
# ─────────────────────────────────────────────────────────────
class JointDistributionGrid(InteractiveScene):
    """결합분포를 이산·연속 둘로 나눠 보인다 (2026-09-18 개정. 전에는 격자만 보이고 pmf 라는 말도 pdf 예도 없었다).
    앞: 이산 — 3×3 격자가 결합확률질량함수. 칸 하나 = 사건 (X=x, Y=y), 조건 셋, 영역 A 의 확률 = 칸의 합.
    뒤: 연속 — 단위 정사각형 위의 높이가 결합확률밀도함수. 전체 부피 1, 영역 A 위의 부피 = 이중적분."""

    def construct(self):
        head = slide_title("Joint Probability Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 1. 이산: 결합 pmf ───────────────────────────────────
        kind = label("discrete: joint probability mass function", 26, ACCENT).next_to(head, DOWN, buff=0.3).align_to(head[0], LEFT)
        self.play(FadeIn(kind))

        vals = [[R"\ ", R"\ ", R"\ "] for _ in range(3)]
        table, cells, texts, heads = grid_table(vals, ["0", "1", "2"], ["0", "1", "2"], w=1.3, h=0.9)
        table.move_to([-2.4, -0.9, 0])
        x_tag = label("x = blue pens", 24, ACCENT).next_to(table, UP, buff=0.45)
        y_tag = label("y = red pens", 24, WARN).next_to(table, LEFT, buff=0.5)
        self.play(ShowCreation(table[0]), FadeIn(heads), FadeIn(x_tag), FadeIn(y_tag))
        self.wait(0.4)

        # 칸 하나 = 사건 하나
        one = cells[(0, 1)]
        hl = one.copy().set_fill(MEAN_COLOR, 0.5).set_stroke(MEAN_COLOR, 3)
        ev = Tex(R"f(1, 0) = P(X = 1,\ Y = 0)").scale(0.8).set_color(MEAN_COLOR).move_to([3.5, 1.5, 0])
        ev_tag = note("one cell, one event", 22, MEAN_COLOR).next_to(ev, DOWN, buff=0.15).align_to(ev, LEFT)
        self.play(FadeIn(hl), Write(ev), FadeIn(ev_tag))
        self.wait(1.0)

        # 조건 셋: 0 이상, 다 더하면 1
        all_cells = VGroup(*[c.copy().set_fill(ACCENT, 0.35).set_stroke(ACCENT, 2) for c in cells.values()])
        c1 = Tex(R"f(x, y) \ge 0").scale(0.85).set_color(INK)
        c2 = Tex(R"\sum_x \sum_y f(x, y) = 1").scale(0.85).set_color(INK)
        C = VGroup(c1, c2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.5, -0.3, 0]).align_to(ev, LEFT)
        self.play(FadeOut(hl), FadeOut(ev_tag), Write(c1))
        self.play(LaggedStartMap(FadeIn, all_cells, lag_ratio=0.08), Write(c2), run_time=1.4)
        self.wait(1.0)

        # 영역 A 의 확률 = 그 칸들의 합
        region = [(0, 0), (0, 1), (1, 0)]
        hls = VGroup(*[cells[k].copy().set_fill(MEAN_COLOR, 0.5).set_stroke(MEAN_COLOR, 3) for k in region])
        c3 = Tex(R"P[(X, Y) \in A] = \sum_{A} f(x, y)").scale(0.85).set_color(MEAN_COLOR).next_to(C, DOWN, buff=0.45).align_to(ev, LEFT)
        a_tag = Tex(R"A:\ x + y \le 1").scale(0.7).set_color(MEAN_COLOR).next_to(c3, DOWN, buff=0.15).align_to(ev, LEFT)
        self.play(FadeOut(all_cells), FadeIn(hls), Write(c3), FadeIn(a_tag))
        self.wait(1.6)

        # ── 2. 연속: 결합 pdf ───────────────────────────────────
        discrete = VGroup(kind, table, x_tag, y_tag, ev, C, c3, a_tag, hls)
        kind2 = label("continuous: joint probability density function", 26, CALM).move_to(kind).align_to(head[0], LEFT)
        self.play(FadeOut(discrete), FadeIn(kind2))

        S = 3.4
        x0, y0 = -5.4, -2.9
        sq = Square(side_length=S).set_stroke(GREY_B, 2).move_to([x0 + S / 2, y0 + S / 2, 0])
        shade = VGroup()
        n = 10
        for i in range(n):
            for j in range(n):
                x, y = (j + 0.5) / n, (i + 0.5) / n
                v = (x + y) / 2.0
                c = Square(side_length=S / n).set_stroke(width=0).set_fill(CALM, 0.12 + 0.65 * v)
                c.move_to([x0 + (j + 0.5) * S / n, y0 + (i + 0.5) * S / n, 0])
                shade.add(c)
        xl = VGroup(Tex("0").scale(0.6), Tex("1").scale(0.6)).set_color(GREY_B)
        xl[0].next_to(sq.get_corner(DL), DOWN, buff=0.12)
        xl[1].next_to(sq.get_corner(DR), DOWN, buff=0.12)
        yl = Tex("1").scale(0.6).set_color(GREY_B).next_to(sq.get_corner(UL), LEFT, buff=0.12)
        xt = Tex("x").scale(0.7).set_color(GREY_B).next_to(sq, DOWN, buff=0.35)
        yt = Tex("y").scale(0.7).set_color(GREY_B).next_to(sq, LEFT, buff=0.35)
        f_tag = Tex(R"f(x, y)").scale(0.85).set_color(CALM).next_to(sq, UP, buff=0.3)
        h_tag = note("shade = height = density", 22, CALM).next_to(f_tag, RIGHT, buff=0.5)
        self.play(ShowCreation(sq), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(f_tag))
        self.play(LaggedStartMap(FadeIn, shade, lag_ratio=0.01), FadeIn(h_tag), run_time=1.2)
        self.wait(0.6)

        d1 = Tex(R"f(x, y) \ge 0").scale(0.85).set_color(INK)
        d2 = Tex(R"\int_{-\infty}^{\infty}\!\int_{-\infty}^{\infty} f(x, y)\,dx\,dy = 1").scale(0.85).set_color(INK)
        D = VGroup(d1, d2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.3, 0.9, 0])
        v_tag = note("total volume 1", 22, GREY_B).next_to(d2, DOWN, buff=0.15).align_to(d1, LEFT)
        self.play(Write(d1))
        self.play(Write(d2), FadeIn(v_tag))
        self.wait(0.8)

        rect = Rectangle(width=S * 0.5, height=S * 0.3).set_stroke(MEAN_COLOR, 3).set_fill(MEAN_COLOR, 0.35)
        rect.move_to([x0 + S * 0.3, y0 + S * 0.55, 0])
        a_lab = Tex("A").scale(0.8).set_color(MEAN_COLOR).move_to(rect)
        d3 = Tex(R"P[(X, Y) \in A] = \iint_{A} f(x, y)\,dx\,dy").scale(0.85).set_color(MEAN_COLOR).next_to(D, DOWN, buff=0.7).align_to(d1, LEFT)
        vol_tag = note("volume over A", 22, MEAN_COLOR).next_to(d3, DOWN, buff=0.15).align_to(d1, LEFT)
        self.play(FadeIn(rect), FadeIn(a_lab))
        self.play(Write(d3), FadeIn(vol_tag))
        self.wait(1.2)

        # 나란히: 합 ↔ 적분
        pair = VGroup(note("discrete: sum over cells", 22, ACCENT), note("continuous: volume over region", 22, CALM))
        pair.arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(vol_tag, DOWN, buff=0.5).align_to(d1, LEFT)
        self.play(FadeIn(pair))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 예제 3.14 볼펜 — 슬라이드 22 뒤 (풀이 23 앞)
# ─────────────────────────────────────────────────────────────
class Example314Pens(InteractiveScene):
    """파랑 3·빨강 2·초록 3 에서 둘. 2026-09-18 개정: 풀이 단계 넷을 먼저 목록으로 걸어 두고 한 단계씩 진행한다.
    1 전체 경우 C(8,2)=28 → 2 칸 하나의 셈(세 조합의 곱, 인자를 하나씩) → 3 표 3.1 채우기(첫 칸은 풀어서, 나머지는 빠르게)
    → 4 영역 A 의 칸을 더해 9/14. 전에는 첫 장면에 상자·개수·공식이 한꺼번에 나왔다."""

    def construct(self):
        head = slide_title("Example 3.14")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 소재: 볼펜 여덟 자루, 둘을 고른다
        pens = VGroup(*[letter_chip("B", 0.5, ACCENT) for _ in range(3)],
                      *[letter_chip("R", 0.5, WARN) for _ in range(2)],
                      *[letter_chip("G", 0.5, GREEN_PEN) for _ in range(3)])
        pens.arrange(RIGHT, buff=0.12).move_to([-3.6, 2.15, 0])
        box = panel(pens, MUTED, buff=0.18)
        ask = note("pick 2 pens", 22, INK).next_to(box, DOWN, buff=0.18)
        xy = Tex(R"X = \text{blue},\quad Y = \text{red}", t2c={R"\text{blue}": ACCENT, R"\text{red}": WARN}).scale(0.7).next_to(ask, DOWN, buff=0.12)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, pens, lag_ratio=0.06))
        self.play(FadeIn(ask), FadeIn(xy))
        self.wait(0.6)

        # 풀이 단계 넷을 먼저 걸어 둔다
        steps = VGroup(label("1. count all pairs", 24, INK),
                       label("2. count pairs per cell", 24, INK),
                       label("3. fill Table 3.1", 24, INK),
                       label("4. add the region A", 24, INK))
        steps.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.4, 1.75, 0])
        steps_box = panel(steps, GREY_C, buff=0.22)
        self.play(FadeIn(steps_box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        self.wait(0.8)

        def focus(k):
            anims = []
            for i, st in enumerate(steps):
                anims.append(st.animate.set_color(MEAN_COLOR if i == k else GREY_C))
            return AnimationGroup(*anims)

        # ── 1. 전체 경우의 수
        self.play(focus(0))
        two = VGroup(ring(pens[1], MEAN_COLOR, 0.04), ring(pens[6], MEAN_COLOR, 0.04))
        pick = Tex(R"\binom{8}{2} = 28").scale(0.9).set_color(INK).next_to(box, RIGHT, buff=0.5)
        self.play(ShowCreation(two))
        self.play(Write(pick))
        self.play(FadeOut(two))
        self.wait(0.8)

        # ── 2. 칸 하나의 셈: 인자를 하나씩
        self.play(focus(1))
        formula = Tex(R"f(x, y) = \frac{\binom{3}{x}\binom{2}{y}\binom{3}{2-x-y}}{28}",
                      t2c={R"\binom{3}{x}": ACCENT, R"\binom{2}{y}": WARN, R"\binom{3}{2-x-y}": GREEN_PEN}).scale(0.85)
        formula.move_to([3.4, -0.35, 0])
        self.play(Write(formula), run_time=1.2)
        self.wait(0.3)
        for chips, key, color, words in ((pens[:3], R"\binom{3}{x}", ACCENT, "x blue from 3"),
                                         (pens[3:5], R"\binom{2}{y}", WARN, "y red from 2"),
                                         (pens[5:], R"\binom{3}{2-x-y}", GREEN_PEN, "the rest, green")):
            marks = VGroup(*[ring(c, color, 0.04) for c in chips])
            fl = FlashAround(formula[key], color=color, buff=0.08)
            tag = note(words, 22, color).next_to(formula, DOWN, buff=0.25)
            self.play(ShowCreation(marks), fl, FadeIn(tag), run_time=1.0)
            self.wait(0.5)
            self.play(FadeOut(marks), FadeOut(tag), run_time=0.25)
        self.wait(0.4)

        # ── 3. 표 3.1 채우기 — 첫 칸은 풀어서, 나머지는 빠르게
        self.play(focus(2))
        blank = [[R"\ "] * 3 for _ in range(3)]
        table, cells, texts, heads = grid_table(blank, ["0", "1", "2"], ["0", "1", "2"], w=1.2, h=0.8)
        table.move_to([-2.9, -1.55, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads))

        first = Tex(R"f(0, 0) = \frac{\binom{3}{0}\binom{2}{0}\binom{3}{2}}{28} = \frac{3}{28}",
                    t2c={R"\binom{3}{0}": ACCENT, R"\binom{2}{0}": WARN, R"\binom{3}{2}": GREEN_PEN}).scale(0.75)
        first.next_to(formula, DOWN, buff=0.35).align_to(formula, LEFT)
        marks = VGroup(*[ring(c, GREEN_PEN, 0.04) for c in pens[5:7]])
        hl0 = cells[(0, 0)].copy().set_fill(MEAN_COLOR, 0.4).set_stroke(MEAN_COLOR, 3)
        self.play(FadeIn(hl0), ShowCreation(marks), Write(first), run_time=1.2)
        t00 = Tex(R"\tfrac{3}{28}").scale(0.75).set_color(INK).move_to(cells[(0, 0)])
        self.play(FadeIn(t00), FadeOut(marks), FadeOut(hl0))
        self.wait(0.8)
        self.play(FadeOut(first))

        order = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (1, 2), (2, 1), (2, 2)]
        for (i, j) in order:
            x, y = j, i
            g = 2 - x - y
            if g < 0:
                t = Tex("0").scale(0.75).set_color(MUTED).move_to(cells[(i, j)])
                self.play(FadeIn(t), run_time=0.3)
                continue
            marks = VGroup(*[ring(c, ACCENT, 0.04) for c in pens[:x]],
                           *[ring(c, WARN, 0.04) for c in pens[3:3 + y]],
                           *[ring(c, GREEN_PEN, 0.04) for c in pens[5:5 + g]])
            n = comb(3, x) * comb(2, y) * comb(3, g)
            t = Tex(R"\tfrac{%d}{28}" % n).scale(0.75).set_color(INK).move_to(cells[(i, j)])
            self.play(ShowCreation(marks), FadeIn(t), run_time=0.5)
            self.play(FadeOut(marks), run_time=0.2)
        self.wait(0.6)

        # ── 4. 영역 A 의 칸을 더한다
        self.play(focus(3))
        want = [(0, 0), (0, 1), (1, 0)]
        hls = VGroup(*[cells[k].copy().set_fill(MEAN_COLOR, 0.45).set_stroke(MEAN_COLOR, 3) for k in want])
        cond = Tex(R"A:\ x + y \le 1").scale(0.85).set_color(MEAN_COLOR).next_to(formula, DOWN, buff=0.4).align_to(formula, LEFT)
        ans = Tex(R"\frac{3}{28} + \frac{9}{28} + \frac{6}{28} = \frac{18}{28} = \frac{9}{14}").scale(0.8).set_color(MEAN_COLOR)
        ans.next_to(cond, DOWN, buff=0.35).align_to(formula, LEFT)
        self.play(FadeIn(hls), Write(cond))
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13. 예제 3.15 단위 정사각형 위의 밀도 — 슬라이드 25 뒤 (26 앞)
# ─────────────────────────────────────────────────────────────
class Example315DriveIn(InteractiveScene):
    """정사각형 [0,1]² 위에서 높이가 (2/5)(2x+3y). 전체 부피 1, 작은 직사각형 위의 부피 13/160. 안쪽 적분부터."""

    def construct(self):
        head = slide_title("Example 3.15")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        S = 3.6
        x0, y0 = -6.0, -2.6
        sq = Square(side_length=S).set_stroke(GREY_B, 2).move_to([x0 + S / 2, y0 + S / 2, 0])
        # 높이를 색 농도로: 오른쪽 위가 진하다
        cells = VGroup()
        n = 8
        for i in range(n):
            for j in range(n):
                x, y = (j + 0.5) / n, (i + 0.5) / n
                v = 0.4 * (2 * x + 3 * y) / 2.0
                c = Square(side_length=S / n).set_stroke(width=0).set_fill(ACCENT, 0.15 + 0.6 * v)
                c.move_to([x0 + (j + 0.5) * S / n, y0 + (i + 0.5) * S / n, 0])
                cells.add(c)
        xl = VGroup(Tex("0").scale(0.6), Tex("1").scale(0.6)).set_color(GREY_B)
        xl[0].next_to(sq.get_corner(DL), DOWN, buff=0.12)
        xl[1].next_to(sq.get_corner(DR), DOWN, buff=0.12)
        yl = Tex("1").scale(0.6).set_color(GREY_B).next_to(sq.get_corner(UL), LEFT, buff=0.12)
        xt = Tex("x").scale(0.7).set_color(GREY_B).next_to(sq, DOWN, buff=0.35)
        yt = Tex("y").scale(0.7).set_color(GREY_B).next_to(sq, LEFT, buff=0.35)
        f_tag = Tex(R"f(x, y) = \frac{2}{5}(2x + 3y)").scale(0.8).set_color(CALM).next_to(sq, UP, buff=0.3)
        self.play(ShowCreation(sq), FadeIn(cells), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(f_tag))
        self.wait(0.4)

        a1 = Tex(R"\int_0^1\int_0^1 \frac{2}{5}(2x + 3y)\,dx\,dy").scale(0.68).set_color(INK)
        a2 = Tex(R"\mathrm{inner:}\  \frac{2}{5}\left[x^2 + 3yx\right]_0^1 = \frac{2}{5}(1 + 3y)").scale(0.68).set_color(INK)
        a3 = Tex(R"\mathrm{outer:}\  \frac{2}{5}\left[y + \frac{3y^2}{2}\right]_0^1 = 1").scale(0.68).set_color(MEAN_COLOR)
        A = VGroup(a1, a2, a3).arrange(DOWN, buff=0.24, aligned_edge=LEFT).move_to([3.3, 1.45, 0])
        vol_tag = note("(a) total volume", 22, GREY_B).next_to(A, UP, buff=0.15).align_to(A, LEFT)
        self.play(FadeIn(vol_tag), Write(a1))
        self.play(Write(a2))
        self.play(Write(a3))
        self.wait(0.8)

        # (b) 작은 직사각형
        rect = Rectangle(width=S * 0.5, height=S * 0.25).set_stroke(MEAN_COLOR, 3).set_fill(MEAN_COLOR, 0.35)
        rect.move_to([x0 + S * 0.25, y0 + S * 0.375, 0])
        r_tag = Tex(R"0 < x < \tfrac12,\ \tfrac14 < y < \tfrac12").scale(0.65).set_color(MEAN_COLOR).next_to(sq, DOWN, buff=0.75)
        self.play(FadeOut(xt), FadeIn(rect), FadeIn(r_tag))
        b1 = Tex(R"\int_{1/4}^{1/2}\int_0^{1/2} \frac{2}{5}(2x + 3y)\,dx\,dy").scale(0.68).set_color(INK)
        b2 = Tex(R"\mathrm{inner:}\  \frac{1}{10} + \frac{3y}{5}").scale(0.68).set_color(INK)
        b3 = Tex(R"\mathrm{outer:}\  \left[\frac{y}{10} + \frac{3y^2}{10}\right]_{1/4}^{1/2} = \frac{13}{160}").scale(0.68).set_color(MEAN_COLOR)
        B = VGroup(b1, b2, b3).arrange(DOWN, buff=0.24, aligned_edge=LEFT).next_to(A, DOWN, buff=0.45).align_to(A, LEFT)
        b_tag = note("(b) volume over A", 22, GREY_B).next_to(B, UP, buff=0.15).align_to(A, LEFT)
        self.play(FadeIn(b_tag), Write(b1))
        self.play(Write(b2))
        self.play(Write(b3))
        self.play(FlashAround(b3, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 14. 주변분포 = 행 합·열 합 — 슬라이드 27 (정의 3.10) 앞
# ─────────────────────────────────────────────────────────────
class MarginalAsRowSums(InteractiveScene):
    """표 3.1 의 행을 옆으로 더해 h(y) 가 가장자리에, 열을 아래로 더해 g(x)."""

    def construct(self):
        head = slide_title("Marginal Distributions")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells, texts, heads = grid_table(TABLE31, ["0", "1", "2"], ["0", "1", "2"], w=1.3, h=0.85)
        table.move_to([-1.6, -0.3, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads))
        self.wait(0.4)

        # 행 합 → h(y)
        h_vals = [R"\tfrac{15}{28}", R"\tfrac{12}{28}", R"\tfrac{1}{28}"]
        h_tag = Tex("h(y)").scale(0.75).set_color(WARN).move_to([cells[(0, 2)].get_center()[0] + 1.6, cells[(0, 0)].get_center()[1] + 0.85 * 0.85, 0])
        self.play(FadeIn(h_tag))
        for i in range(3):
            row = VGroup(*[texts[(i, j)] for j in range(3)])
            hl = VGroup(*[cells[(i, j)].copy().set_fill(WARN, 0.3).set_stroke(width=0) for j in range(3)])
            target = Tex(h_vals[i]).scale(0.8).set_color(WARN).move_to([h_tag.get_x(), cells[(i, 0)].get_y(), 0])
            self.play(FadeIn(hl), run_time=0.25)
            self.play(TransformFromCopy(row, target), run_time=0.6)
            self.play(FadeOut(hl), run_time=0.2)
        h_def = Tex(R"h(y) = \sum_x f(x, y)").scale(0.8).set_color(WARN).move_to([4.4, 1.6, 0])
        self.play(Write(h_def))
        self.wait(0.5)

        # 열 합 → g(x)
        g_vals = [R"\tfrac{10}{28}", R"\tfrac{15}{28}", R"\tfrac{3}{28}"]
        g_tag = Tex("g(x)").scale(0.75).set_color(ACCENT).move_to([cells[(0, 0)].get_center()[0] - 1.3 * 0.8, cells[(2, 0)].get_y() - 1.1, 0])
        self.play(FadeIn(g_tag))
        for j in range(3):
            col = VGroup(*[texts[(i, j)] for i in range(3)])
            hl = VGroup(*[cells[(i, j)].copy().set_fill(ACCENT, 0.3).set_stroke(width=0) for i in range(3)])
            target = Tex(g_vals[j]).scale(0.8).set_color(ACCENT).move_to([cells[(0, j)].get_x(), g_tag.get_y(), 0])
            self.play(FadeIn(hl), run_time=0.25)
            self.play(TransformFromCopy(col, target), run_time=0.6)
            self.play(FadeOut(hl), run_time=0.2)
        g_def = Tex(R"g(x) = \sum_y f(x, y)").scale(0.8).set_color(ACCENT).next_to(h_def, DOWN, buff=0.5).align_to(h_def, LEFT)
        self.play(Write(g_def))
        cont = Tex(R"g(x) = \int_{-\infty}^{\infty} f(x, y)\,dy").scale(0.75).set_color(GREY_B).next_to(g_def, DOWN, buff=0.5).align_to(h_def, LEFT)
        cont_tag = note("continuous case", 22, GREY_B).next_to(cont, DOWN, buff=0.15).align_to(h_def, LEFT)
        self.play(FadeIn(cont), FadeIn(cont_tag))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 15. 조건부분포 = 한 행만 남기고 늘리기 — 슬라이드 31 (정의 3.11) 앞
# ─────────────────────────────────────────────────────────────
class ConditionalDistributionSlice(InteractiveScene):
    """표 3.1 에서 Y=1 행만 남기고 h(1)=12/28 로 나눠 늘린다. (6/28, 6/28, 0) → (1/2, 1/2, 0)."""

    def construct(self):
        head = slide_title("Conditional Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells, texts, heads = grid_table(TABLE31, ["0", "1", "2"], ["0", "1", "2"], w=1.3, h=0.85)
        table.move_to([-2.4, -0.2, 0])
        self.play(ShowCreation(table[0]), FadeIn(heads))
        self.wait(0.4)

        given = Tex(R"\text{given } Y = 1").scale(0.85).set_color(WARN).move_to([3.6, 2.0, 0])
        self.play(Write(given))
        others = VGroup(*[cells[(i, j)] for i in (0, 2) for j in range(3)], *[texts[(i, j)] for i in (0, 2) for j in range(3)])
        self.play(others.animate.set_opacity(0.15), run_time=0.8)
        row_hl = VGroup(*[cells[(1, j)].copy().set_fill(WARN, 0.25).set_stroke(WARN, 3) for j in range(3)])
        self.play(FadeIn(row_hl))
        total = Tex(R"h(1) = \frac{6}{28} + \frac{6}{28} + 0 = \frac{12}{28}").scale(0.8).set_color(WARN)
        total.next_to(given, DOWN, buff=0.4).align_to(given, LEFT)
        self.play(Write(total))
        self.wait(0.6)

        # 늘리기: 12/28 → 1
        stretch = Tex(R"f(x \mid 1) = \frac{f(x, 1)}{h(1)}").scale(0.85).set_color(INK).next_to(total, DOWN, buff=0.5).align_to(given, LEFT)
        self.play(Write(stretch))
        new_vals = [R"\tfrac{1}{2}", R"\tfrac{1}{2}", "0"]
        new_row = VGroup()
        for j in range(3):
            t = Tex(new_vals[j]).scale(0.8).set_color(MEAN_COLOR).move_to([cells[(1, j)].get_x(), cells[(2, j)].get_y() - 1.2, 0])
            new_row.add(t)
        arrow = Arrow(cells[(1, 1)].get_bottom() + DOWN * 0.9, new_row[1].get_top() + UP * 0.05, buff=0.05, stroke_width=3).set_color(MEAN_COLOR)
        times = Tex(R"\times \frac{28}{12}").scale(0.7).set_color(MEAN_COLOR).next_to(arrow, RIGHT, buff=0.1)
        new_tag = Tex(R"f(x \mid 1)").scale(0.75).set_color(MEAN_COLOR).next_to(new_row, LEFT, buff=0.5)
        self.play(GrowArrow(arrow), FadeIn(times))
        self.play(TransformFromCopy(VGroup(*[texts[(1, j)] for j in range(3)]), new_row), FadeIn(new_tag), run_time=1.0)
        sum1 = Tex(R"\frac{1}{2} + \frac{1}{2} + 0 = 1").scale(0.75).set_color(MEAN_COLOR).next_to(new_row, RIGHT, buff=0.6)
        self.play(FadeIn(sum1))
        ans = Tex(R"P(X = 0 \mid Y = 1) = \frac{1}{2}").scale(0.85).set_color(MEAN_COLOR).next_to(stretch, DOWN, buff=0.5).align_to(given, LEFT)
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 16. 예제 3.19 삼각형 정의역 — 슬라이드 34 뒤 (풀이 35 앞)
# ─────────────────────────────────────────────────────────────
class Example319Spectrum(InteractiveScene):
    """10xy² 의 정의역 0<x<y<1 은 삼각형. x=¼ 자리에서 세로로 잘라 3y²/(1−x³) 로 늘리고 P(Y>½ | X=¼) = 8/9."""

    def construct(self):
        head = slide_title("Example 3.19")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        S = 3.8
        x0, y0 = -6.0, -2.8
        sq = Square(side_length=S).set_stroke(GREY_C, 1.5).move_to([x0 + S / 2, y0 + S / 2, 0])
        tri = Polygon([x0, y0, 0], [x0, y0 + S, 0], [x0 + S, y0 + S, 0]).set_stroke(CALM, 2.5).set_fill(ACCENT, 0.3)
        f_tag = Tex(R"f(x, y) = 10xy^2,\quad 0 < x < y < 1").scale(0.75).set_color(CALM).next_to(sq, UP, buff=0.25)
        xl = VGroup(Tex("0").scale(0.6).next_to(sq.get_corner(DL), DOWN, buff=0.1), Tex("1").scale(0.6).next_to(sq.get_corner(DR), DOWN, buff=0.1)).set_color(GREY_B)
        yl = Tex("1").scale(0.6).set_color(GREY_B).next_to(sq.get_corner(UL), LEFT, buff=0.1)
        xt = Tex("x").scale(0.7).set_color(GREY_B).next_to(sq, DOWN, buff=0.35)
        yt = Tex("y").scale(0.7).set_color(GREY_B).next_to(sq, LEFT, buff=0.35)
        self.play(ShowCreation(sq), FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt))
        self.play(FadeIn(tri), FadeIn(f_tag))
        dom = label("triangle, not rectangle", 24, WARN).next_to(sq, DOWN, buff=0.7)
        self.play(FadeIn(dom))
        self.wait(0.6)

        # x 를 고정하면 y 는 x 부터 1 까지
        xv = 0.25
        px = x0 + xv * S
        slice_line = Line([px, y0 + xv * S, 0], [px, y0 + S, 0]).set_stroke(MEAN_COLOR, 6)
        x_mark = Tex(R"x = \tfrac14").scale(0.65).set_color(MEAN_COLOR).next_to([px, y0, 0], DOWN, buff=0.1)
        lim_lo = Tex("y = x").scale(0.6).set_color(GREY_B).next_to(slice_line.get_bottom(), RIGHT, buff=0.1)
        lim_hi = Tex("y = 1").scale(0.6).set_color(GREY_B).next_to(slice_line.get_top(), RIGHT, buff=0.1)
        self.play(FadeOut(xl[0]), ShowCreation(slice_line), FadeIn(x_mark), FadeIn(lim_lo), FadeIn(lim_hi))
        g1 = Tex(R"g(x) = \int_x^1 10xy^2\,dy = \frac{10}{3}x(1 - x^3)").scale(0.75).set_color(INK)
        g2 = Tex(R"f(y \mid x) = \frac{10xy^2}{\frac{10}{3}x(1 - x^3)} = \frac{3y^2}{1 - x^3}").scale(0.75).set_color(INK)
        G = VGroup(g1, g2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.3, 1.5, 0])
        self.play(Write(g1))
        self.wait(0.3)
        self.play(Write(g2))
        self.wait(0.6)

        # y > 1/2 조각
        upper = Line([px, y0 + 0.5 * S, 0], [px, y0 + S, 0]).set_stroke(WARN, 8)
        half = Tex(R"y = \tfrac12").scale(0.6).set_color(WARN).next_to(upper.get_bottom(), LEFT, buff=0.1)
        self.play(ShowCreation(upper), FadeIn(half))
        p1 = Tex(R"P(Y > \tfrac12 \mid X = \tfrac14) = \int_{1/2}^{1} \frac{3y^2}{1 - \frac{1}{64}}\,dy").scale(0.72).set_color(INK)
        p2 = Tex(R"= \frac{64}{63}\left[y^3\right]_{1/2}^{1} = \frac{64}{63} \cdot \frac{7}{8} = \frac{8}{9}").scale(0.75).set_color(MEAN_COLOR)
        P = VGroup(p1, p2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(G, DOWN, buff=0.6).align_to(G, LEFT)
        self.play(Write(p1))
        self.play(Write(p2))
        self.play(FlashAround(p2, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 17. 예제 3.20 직사각형 정의역 — 슬라이드 37 뒤 (풀이 38 앞)
# ─────────────────────────────────────────────────────────────
class Example320Rectangle(InteractiveScene):
    """직사각형 위의 x(1+3y²)/4. g(x) = x/2, h(y) = (1+3y²)/2, f(x|y) = x/2 = g(x). P = 3/64."""

    def construct(self):
        head = slide_title("Example 3.20")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        W, H = 4.4, 2.2
        x0, y0 = -6.2, -2.4
        rect = Rectangle(width=W, height=H).set_stroke(CALM, 2.5).set_fill(ACCENT, 0.3).move_to([x0 + W / 2, y0 + H / 2, 0])
        xl = VGroup(Tex("0").scale(0.6).next_to(rect.get_corner(DL), DOWN, buff=0.1), Tex("2").scale(0.6).next_to(rect.get_corner(DR), DOWN, buff=0.1)).set_color(GREY_B)
        yl = Tex("1").scale(0.6).set_color(GREY_B).next_to(rect.get_corner(UL), LEFT, buff=0.1)
        f_tag = Tex(R"f(x, y) = \frac{x(1 + 3y^2)}{4}").scale(0.75).set_color(CALM).next_to(rect, UP, buff=0.3)
        dom = label("rectangle domain", 24, GREY_B).next_to(rect, DOWN, buff=0.5)
        self.play(ShowCreation(rect), FadeIn(xl), FadeIn(yl), FadeIn(f_tag), FadeIn(dom))
        self.wait(0.4)

        # y 를 고정한 가로 조각
        yv = 1 / 3
        py = y0 + yv * H
        sl = Line([x0, py, 0], [x0 + W, py, 0]).set_stroke(MEAN_COLOR, 6)
        y_mark = Tex(R"y = \tfrac13").scale(0.65).set_color(MEAN_COLOR).next_to(sl, LEFT, buff=0.1)
        self.play(FadeOut(yl), ShowCreation(sl), FadeIn(y_mark))

        s1 = Tex(R"g(x) = \int_0^1 \frac{x(1 + 3y^2)}{4}\,dy = \frac{x}{2}").scale(0.75).set_color(INK)
        s2 = Tex(R"h(y) = \int_0^2 \frac{x(1 + 3y^2)}{4}\,dx = \frac{1 + 3y^2}{2}").scale(0.75).set_color(INK)
        s3 = Tex(R"f(x \mid y) = \frac{x(1 + 3y^2)/4}{(1 + 3y^2)/2} = \frac{x}{2} = g(x)").scale(0.75).set_color(WARN)
        s4 = Tex(R"P(\tfrac14 < X < \tfrac12 \mid Y = \tfrac13) = \int_{1/4}^{1/2} \frac{x}{2}\,dx = \frac{3}{64}").scale(0.72).set_color(MEAN_COLOR)
        steps = VGroup(s1, s2, s3, s4).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([3.2, 0.2, 0])
        for s in steps[:3]:
            self.play(Write(s))
            self.wait(0.3)
        same = note("y drops out", 22, WARN).next_to(s4, DOWN, buff=0.3).align_to(s4, LEFT)
        self.play(FadeIn(same))
        self.wait(0.4)
        piece = Line([x0 + 0.125 * W, py, 0], [x0 + 0.25 * W, py, 0]).set_stroke(WARN, 10)
        self.play(ShowCreation(piece), Write(s4))
        self.play(FlashAround(s4, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 18. 독립 = 곱셈이 모든 칸에서 맞는 것. 반례 한 칸 — 슬라이드 39 (정의 3.12) 앞
# ─────────────────────────────────────────────────────────────
class IndependenceProductCheck(InteractiveScene):
    """칸 (0,1): f = 6/28, g(0)h(1) = (10/28)(12/28) = 15/98 ≠ 21/98. 이어서 정의역 둘 — 직사각형이면 갈라지고 삼각형이면 아니다."""

    def construct(self):
        head = slide_title("Statistical Independence")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        defn = Tex(R"f(x, y) = g(x)\,h(y)\quad \text{for all } (x, y)").scale(0.85).set_color(INK).next_to(head[1], DOWN, buff=0.3)
        self.play(Write(defn))

        table, cells, texts, heads = grid_table(TABLE31, ["0", "1", "2"], ["0", "1", "2"], w=1.2, h=0.8)
        table.move_to([-3.2, -1.0, 0])
        g_row = VGroup(*[Tex(v).scale(0.7).set_color(ACCENT).move_to([cells[(0, j)].get_x(), cells[(2, 0)].get_y() - 0.9, 0])
                         for j, v in enumerate([R"\tfrac{10}{28}", R"\tfrac{15}{28}", R"\tfrac{3}{28}"])])
        h_col = VGroup(*[Tex(v).scale(0.7).set_color(WARN).move_to([cells[(0, 2)].get_x() + 1.4, cells[(i, 0)].get_y(), 0])
                         for i, v in enumerate([R"\tfrac{15}{28}", R"\tfrac{12}{28}", R"\tfrac{1}{28}"])])
        g_tag = Tex("g(x)").scale(0.6).set_color(ACCENT).next_to(g_row, LEFT, buff=0.3)
        h_tag = Tex("h(y)").scale(0.6).set_color(WARN).next_to(h_col, UP, buff=0.15)
        self.play(ShowCreation(table[0]), FadeIn(heads), FadeIn(g_row), FadeIn(h_col), FadeIn(g_tag), FadeIn(h_tag))
        self.wait(0.4)

        hl = cells[(1, 0)].copy().set_fill(MEAN_COLOR, 0.45).set_stroke(MEAN_COLOR, 3)
        c1 = Tex(R"f(0, 1) = \frac{6}{28} = \frac{21}{98}").scale(0.8).set_color(MEAN_COLOR)
        c2 = Tex(R"g(0)\,h(1) = \frac{10}{28} \cdot \frac{12}{28} = \frac{15}{98}").scale(0.8).set_color(INK)
        c3 = Tex(R"\frac{21}{98} \ne \frac{15}{98}").scale(0.9).set_color(WARN)
        C = VGroup(c1, c2, c3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.6, 0.3, 0])
        self.play(FadeIn(hl), Write(c1))
        r_g, r_h = ring(g_row[0], ACCENT, 0.06), ring(h_col[1], WARN, 0.06)
        self.play(ShowCreation(r_g), ShowCreation(r_h), Write(c2))
        self.play(Write(c3))
        verdict = label("one cell is enough", 26, WARN).next_to(C, DOWN, buff=0.4).align_to(C, LEFT)
        self.play(FadeIn(verdict))
        self.wait(1.0)

        # 정의역 둘
        self.play(FadeOut(table), FadeOut(g_row), FadeOut(h_col), FadeOut(g_tag), FadeOut(h_tag), FadeOut(hl),
                  FadeOut(r_g), FadeOut(r_h), FadeOut(C), FadeOut(verdict), run_time=0.5)
        rect = Rectangle(width=3.0, height=1.6).set_stroke(CALM, 2.5).set_fill(ACCENT, 0.3).move_to([-3.6, -0.6, 0])
        tri = Polygon([1.6, -1.6, 0], [1.6, 0.6, 0], [3.8, 0.6, 0]).set_stroke(CALM, 2.5).set_fill(ACCENT, 0.3)
        r_f = Tex(R"\frac{x(1 + 3y^2)}{4}").scale(0.7).set_color(INK).next_to(rect, UP, buff=0.2)
        t_f = Tex(R"10xy^2,\ 0 < x < y < 1").scale(0.7).set_color(INK).next_to(tri, UP, buff=0.2)
        r_ok = Tex(R"f(x \mid y) = g(x)\ \checkmark").scale(0.75).set_color(MEAN_COLOR).next_to(rect, DOWN, buff=0.3)
        t_no = Tex(R"\text{limits depend on } x\ \times").scale(0.75).set_color(WARN).next_to(tri, DOWN, buff=0.3)
        self.play(FadeIn(rect), FadeIn(r_f), FadeIn(tri), FadeIn(t_f))
        self.play(Write(r_ok))
        self.play(Write(t_no))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 19. 예제 3.22 독립인 e^{-x} 셋 — 슬라이드 44 뒤 (풀이 45 앞)
# ─────────────────────────────────────────────────────────────
class Example322ShelfLife(InteractiveScene):
    """세 상자의 유통기한이 독립. 넓이 (1−e⁻²) · (e⁻¹−e⁻³) · e⁻² 를 곱한다."""

    def construct(self):
        head = slide_title("Example 3.22")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        f = lambda x: np.exp(-x)
        specs = [("X_1 < 2", 0, 2, R"1 - e^{-2}"), ("1 < X_2 < 3", 1, 3, R"e^{-1} - e^{-3}"), ("X_3 > 2", 2, 4.5, R"e^{-2}")]
        panels = VGroup()
        for k, (ev, a, b, val) in enumerate(specs):
            axes = density_axes((0, 4.6, 1), (0, 1.1, 0.5), width=3.9, height=2.2)
            graph = axes.get_graph(f, x_range=(0, 4.5, 0.05)).set_stroke(CALM, 3)
            area = area_under(axes, graph, a, b, MEAN_COLOR, 0.6)
            marks = x_marks(axes, [a] + ([b] if b < 4 else []))
            ev_t = Tex(ev).scale(0.7).set_color(INK).next_to(axes, UP, buff=0.15)
            v_t = Tex(val).scale(0.7).set_color(MEAN_COLOR).next_to(axes, DOWN, buff=0.55)
            panels.add(VGroup(axes, graph, area, marks, ev_t, v_t))
        panels.arrange(RIGHT, buff=0.5).move_to([0, 0.4, 0])
        f_tag = Tex(R"f(x) = e^{-x},\ x > 0").scale(0.75).set_color(CALM).next_to(head[1], DOWN, buff=0.25)
        self.play(FadeIn(f_tag))
        for p in panels:
            self.play(ShowCreation(p[0]), ShowCreation(p[1]), FadeIn(p[3]), FadeIn(p[4]), run_time=0.6)
        self.wait(0.3)
        for p in panels:
            self.play(FadeIn(p[2]), Write(p[5]), run_time=0.6)
        indep = label("independent: multiply areas", 24, GREY_B).move_to([0, -2.0, 0])
        self.play(FadeIn(indep))
        ans = Tex(R"P = (1 - e^{-2})(e^{-1} - e^{-3})\,e^{-2} \approx 0.0372").scale(0.85).set_color(MEAN_COLOR).move_to([0, -2.9, 0])
        self.play(TransformFromCopy(VGroup(*[p[5] for p in panels]), ans), run_time=1.2)
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.15), run_time=1.2)
        self.wait(2)
