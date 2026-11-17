"""AI기초수학 — 교재 Chapter 10 확률과 확률분포.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 10_확률과 확률분포_강의용.pptx` 의
10.1 조건부 확률과 베이즈 정리 · 10.2 이산확률분포 · 10.3 연속확률분포에 붙는 보조 영상 9편.
파일 이름은 앞 장과 같은 규칙이다(week10 = CH09, week11 = CH10). 2026-11-18 수업.

식보다 세는 그림과 막대가 움직이는 그림으로 세운다.
- 조건부 확률은 표본공간을 A 로 줄인 뒤의 비율이다(정의 10-2 · 보충 10-A). 수강생 20명은 치토로 그린다.
- 독립은 전체에서 B 의 비율과 A 안에서 B 의 비율이 같은 것이다(정의 10-4 · 예제 10-4).
- 베이즈 정리는 사전확률로 가른 정사각형에서 가능도 조각의 넓이 비다(정리 10-1 · 보충 10-B).
- 기댓값은 막대의 균형점, 분산은 균형점까지 거리 제곱의 평균이다(표 10-1).
- 이항분포의 nCx 는 성공 수가 같은 결과의 개수다(정의 10-5 · 예제 10-6).
- n 이 크고 p 가 작으면 B(n, λ/n) 의 막대가 푸아송분포 P(λ) 에 겹친다(정리 10-2).
- 정규분포는 μ 가 자리, σ 가 폭이다. Z = (X − μ)/σ 는 축의 눈금을 바꾼다(정의 10-7 · 10-8 · 정리 10-4 · 예제 10-9).
- B(100, 1/2) 의 막대는 N(50, 5²) 곡선을 따른다(정리 10-5 · 10-6 · 예제 10-10).
- 주사위 n 개의 표본평균은 n 이 커지면 종 모양이 된다(정리 10-7).
값은 모두 씬 안에서 계산한다(하네스 3.8).

참고: legacy/_2019/bayes/part1.py (사전확률 · 가능도로 가른 정사각형), legacy/_2018/eop/chapter1/ (동전 던지기 결과를 성공 수로 묶기),
legacy/_2023/clt/main.py (주사위 합의 분포). 전개 순서만 읽었고 코드는 새로 썼다. 사람 아이콘은 치토(ps_common)다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week11.py
    ./render.sh check _2026/aimath/week11.py
    ./render.sh ppt   _2026/aimath/week11.py ConditionalProbabilityCrowd
"""
from math import comb, erf, exp, factorial, sqrt

from manim_imports_ext import *

from _2026.aimath.week04 import (
    INK, ACCENT, CALM, WARN, DONE, title, caption, slide_title, tag_under,
)
from _2026.aimath.week07 import footnote
from _2026.probstat.ps_common import chito, crowd, ring


# ─────────────────────────────────────────────────────────────
# 공통 도구
# ─────────────────────────────────────────────────────────────
def head_of(scene, text, tag):
    head = slide_title(text)
    scene.add(head)
    scene.play(FadeIn(tag_under(head, tag)), run_time=0.5)
    return head


def panel_of(rows, width=4.8, shift=ORIGIN, buff=0.3):
    """오른쪽 식 묶음. 폭이 넘치면 줄이고, 좁으면 그대로 둔다."""
    panel = VGroup(*rows).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    if panel.get_width() > width:
        panel.set_width(width)
    panel.to_edge(RIGHT, buff=0.5).shift(shift)
    return panel


def number_axis(x_min, x_max, step, width, numbers=None, font_size=22):
    """가로축 하나. 세로 눈금은 두지 않고 막대 높이는 scale 로 직접 준다."""
    axis = NumberLine(x_range=(x_min, x_max, step), width=width, stroke_color=GREY_B, stroke_width=2,
                      include_tip=False, tick_size=0.05)
    if numbers is None:
        numbers = np.arange(x_min, x_max + step / 2, step)
    labels = VGroup()
    for v in numbers:
        text = "%d" % v if abs(v - round(v)) < 1e-9 else "%g" % v
        lab = Tex(text, font_size=font_size).set_color(GREY_B)
        lab.next_to(axis.n2p(v), DOWN, buff=0.15)
        labels.add(lab)
    axis.add(labels)          # 축을 옮기면 눈금 숫자도 함께 간다
    axis.labels = VGroup()    # 예전 호출 자리(FadeIn(axis.labels))를 위한 빈 묶음
    return axis


def bars_on(axis, xs, heights, unit_h, bar_w, color=ACCENT, opacity=0.8):
    """축 위의 막대 묶음. heights * unit_h 가 화면 높이다."""
    group = VGroup()
    for x, h in zip(xs, heights):
        r = Rectangle(width=bar_w, height=max(h * unit_h, 1e-3))
        r.set_fill(color, opacity).set_stroke(color, 1)
        r.move_to(axis.n2p(x), DOWN)
        group.add(r)
    return group


def curve_on(axis, func, x_min, x_max, unit_h, color=DONE, width=3):
    return ParametricCurve(lambda t: axis.n2p(t) + UP * func(t) * unit_h, t_range=(x_min, x_max, (x_max - x_min) / 200.0)
                           ).set_stroke(color, width)


def area_on(axis, func, a, b, unit_h, color=CALM, opacity=0.45):
    ts = np.linspace(a, b, 80)
    pts = [axis.n2p(a)] + [axis.n2p(t) + UP * func(t) * unit_h for t in ts] + [axis.n2p(b)]
    poly = Polygon(*pts)
    return poly.set_fill(color, opacity).set_stroke(color, 0)


def normal_pdf(x, mu, sigma):
    return exp(-0.5 * ((x - mu) / sigma) ** 2) / (sqrt(2 * PI) * sigma)


def binom_pmf(n, p, k):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


# ─────────────────────────────────────────────────────────────
# 10.1 조건부 확률과 베이즈 정리
# ─────────────────────────────────────────────────────────────
class ConditionalProbabilityCrowd(InteractiveScene):
    """정의 10-2 · 보충 10-A. 조건부 확률은 표본공간을 A 로 줄인 뒤 B 가 차지하는 비율이다.

    수강생 20명(4 × 5). A = 과제 제출 8명(왼쪽 두 열, 금색 앞모습), B = 퀴즈 통과 10명(테두리), A ∩ B = 6명.
    P(B) = 10/20, P(B | A) = 6/8 = 3/4, P(A | B) = 6/10 = 3/5. 제출하지 않은 치토는 등을 돌린다.
    """
    rows, cols = 4, 5
    a_cols = (0, 1)
    b_cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (3, 1), (0, 3), (1, 4), (2, 2), (3, 3)]

    def construct(self):
        head_of(self, "조건부 확률 · 표본공간의 축소", "정의 10-2 · 보충 10-A")
        n = self.rows * self.cols
        people = crowd(n, self.rows, self.cols, height=0.95, buff=0.3, jitter=0.0)
        people.move_to(LEFT * 3.3 + DOWN * 0.55)
        idx = lambda r, c: r * self.cols + c
        a_idx = [idx(r, c) for r in range(self.rows) for c in self.a_cols]
        b_idx = [idx(r, c) for r, c in self.b_cells]
        ab_idx = [i for i in b_idx if i in a_idx]
        n_a, n_b, n_ab = len(a_idx), len(b_idx), len(ab_idx)
        assert (n, n_a, n_b, n_ab) == (20, 8, 10, 6)

        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.04), run_time=1.2)
        shown = footnote(self, "수강생 20명 · 표본공간 S")
        self.wait(1.2)

        # A — 금색 앞모습. 나머지는 등을 돌린다.
        gold = Group(*[chito("front", "gold", people[i].get_height()).move_to(people[i]) for i in a_idx])
        back = Group(*[chito("back", None, people[i].get_height()).move_to(people[i]) for i in range(n) if i not in a_idx])
        self.play(*[FadeOut(people[i]) for i in range(n)], FadeIn(gold), FadeIn(back), run_time=0.9)
        cell = {}
        for i, m in zip(a_idx, gold):
            cell[i] = m
        for i, m in zip([i for i in range(n) if i not in a_idx], back):
            cell[i] = m
        shown = footnote(self, "A · 과제 제출 8명", DONE, shown)
        self.wait(1.2)

        rings = {i: ring(cell[i], color=CALM, buff=0.05, width=4) for i in b_idx}
        self.play(LaggedStart(*[ShowCreation(rings[i]) for i in b_idx], lag_ratio=0.08), run_time=1.2)
        shown = footnote(self, "B · 퀴즈 통과 10명", CALM, shown)

        panel = panel_of([
            Tex(R"P(B)=\frac{|B|}{|S|}=\frac{%d}{%d}=\frac{1}{2}" % (n_b, n)).set_color(INK),
            Tex(R"P(B\mid A)=\frac{|A\cap B|}{|A|}=\frac{%d}{%d}=\frac{3}{4}" % (n_ab, n_a)).set_color(DONE),
            Tex(R"P(A\mid B)=\frac{|A\cap B|}{|B|}=\frac{%d}{%d}=\frac{3}{5}" % (n_ab, n_b)).set_color(CALM),
        ], width=5.2, shift=UP * 0.2, buff=0.55)
        self.play(FadeIn(panel[0]), run_time=0.6)
        self.wait(1.9)

        # 표본공간을 A 로 줄인다
        not_a = [i for i in range(n) if i not in a_idx]
        self.play(*[cell[i].animate.set_opacity(0.15) for i in not_a],
                  *[rings[i].animate.set_stroke(opacity=0.15) for i in b_idx if i not in a_idx], run_time=0.9)
        frame_a = SurroundingRectangle(Group(*[cell[i] for i in a_idx]), buff=0.15).set_stroke(DONE, 3)
        self.play(ShowCreation(frame_a), run_time=0.6)
        shown = footnote(self, "표본공간을 A 로 축소", DONE, shown)
        self.play(FadeIn(panel[1]), run_time=0.6)
        shown = footnote(self, "A 의 8명 중 통과 6명", DONE, shown)
        self.wait(2.9)

        # 표본공간을 B 로 줄인다
        self.play(FadeOut(frame_a),
                  *[cell[i].animate.set_opacity(1.0 if i in b_idx else 0.15) for i in range(n)],
                  *[rings[i].animate.set_stroke(opacity=1.0) for i in b_idx], run_time=0.9)
        shown = footnote(self, "표본공간을 B 로 축소", CALM, shown)
        self.play(FadeIn(panel[2]), run_time=0.6)
        shown = footnote(self, "B 의 10명 중 제출 6명", CALM, shown)
        self.wait(3)


class IndependenceDiceGrid(InteractiveScene):
    """정의 10-4 · 예제 10-4. 주사위 두 개. A = 합이 짝수, B = 합이 3의 배수.

    |S| = 36, |A| = 18, |B| = 12, |A ∩ B| = 6. 전체에서 B 의 비율 12/36 과 A 안에서 B 의 비율 6/18 이 모두 1/3 이다.
    P(B | A) = P(B) 이므로 독립이고 P(A ∩ B) = 1/6 = P(A) P(B).
    """

    def construct(self):
        head_of(self, "독립사건 · 주사위 두 개", "정의 10-4 · 예제 10-4")
        side = 0.72
        cells, sums = {}, {}
        grid = VGroup()
        for i in range(1, 7):
            for j in range(1, 7):
                sq = Square(side_length=side).set_stroke(GREY_C, 1.5).set_fill(BLACK, 0)
                sq.move_to(RIGHT * (j - 3.5) * side + DOWN * (i - 3.5) * side)
                num = Tex(str(i + j), font_size=26).set_color(INK).move_to(sq)
                cells[(i, j)], sums[(i, j)] = sq, num
                grid.add(sq, num)
        heads = VGroup()
        for k in range(1, 7):
            top = Tex(str(k), font_size=24).set_color(GREY_B).move_to(RIGHT * (k - 3.5) * side + UP * 3.5 * side + UP * 0.05)
            left = Tex(str(k), font_size=24).set_color(GREY_B).move_to(LEFT * 3.5 * side + DOWN * (k - 3.5) * side + LEFT * 0.05)
            heads.add(top, left)
        board = VGroup(grid, heads).move_to(LEFT * 3.4 + DOWN * 0.6)
        self.play(FadeIn(board), run_time=0.8)
        shown = footnote(self, "두 눈의 합 · 36칸")

        A = [k for k in cells if (k[0] + k[1]) % 2 == 0]
        B = [k for k in cells if (k[0] + k[1]) % 3 == 0]
        AB = [k for k in A if k in B]
        assert (len(A), len(B), len(AB)) == (18, 12, 6)

        self.play(*[cells[k].animate.set_fill(BLUE_D, 0.6) for k in A], run_time=0.8)
        shown = footnote(self, "A · 합이 짝수 18칸", ACCENT, shown)
        self.wait(1.2)
        marks = {k: Circle(radius=side * 0.4).set_stroke(DONE, 4).move_to(cells[k]) for k in B}
        self.play(LaggedStart(*[ShowCreation(marks[k]) for k in B], lag_ratio=0.06), run_time=1.2)
        shown = footnote(self, "B · 합이 3의 배수 12칸", DONE, shown)

        panel = panel_of([
            Tex(R"P(B)=\frac{%d}{36}=\frac{1}{3}" % len(B)).set_color(DONE),
            Tex(R"P(B\mid A)=\frac{%d}{%d}=\frac{1}{3}" % (len(AB), len(A))).set_color(ACCENT),
            Tex(R"P(B\mid A)=P(B)").set_color(INK),
            Tex(R"P(A\cap B)=\frac{%d}{36}=\frac{1}{2}\cdot\frac{1}{3}" % len(AB)).set_color(CALM),
        ], width=4.6, shift=UP * 0.1, buff=0.5)
        self.play(FadeIn(panel[0]), run_time=0.6)
        self.wait(1.9)

        not_a = [k for k in cells if k not in A]
        self.play(*[sums[k].animate.set_opacity(0.2) for k in not_a],
                  *[cells[k].animate.set_stroke(opacity=0.3) for k in not_a],
                  *[marks[k].animate.set_stroke(opacity=0.15) for k in B if k not in AB], run_time=0.9)
        shown = footnote(self, "A 의 18칸 중 B 는 6칸", ACCENT, shown)
        self.play(FadeIn(panel[1]), run_time=0.6)
        self.wait(2.4)
        self.play(FadeIn(panel[2]), run_time=0.6)
        shown = footnote(self, "두 비율이 같음 · 독립", INK, shown)
        self.wait(1.9)
        self.play(FadeIn(panel[3]), run_time=0.6)
        self.wait(4.5)


class BayesAreaSpam(InteractiveScene):
    """정리 10-1 · 보충 10-B. 메일 20통: 스팸 5 · 정상 15. '무료' 가 든 메일은 스팸 4 · 정상 2.

    정사각형을 사전확률 1/4 | 3/4 로 세로로 가르고, 각 열을 가능도 4/5 · 2/15 높이까지 칠한다.
    칠한 넓이는 1/4 · 4/5 = 1/5, 3/4 · 2/15 = 1/10. P(스팸 | 무료) = (1/5) / (1/5 + 1/10) = 2/3.
    """
    spam, normal = 5, 15
    free_spam, free_normal = 4, 2

    def construct(self):
        head_of(self, "베이즈 정리 · 스팸 필터", "정리 10-1 · 보충 10-B")
        total = self.spam + self.normal
        prior = self.spam / total
        like_s = self.free_spam / self.spam
        like_n = self.free_normal / self.normal
        joint_s, joint_n = prior * like_s, (1 - prior) * like_n
        post = joint_s / (joint_s + joint_n)
        assert abs(post - 2 / 3) < 1e-12 and abs(joint_s - 0.2) < 1e-12 and abs(joint_n - 0.1) < 1e-12

        L = 4.6
        origin = LEFT * 5.9 + DOWN * 2.85
        col_s = Rectangle(width=L * prior, height=L).set_stroke(WARN, 2).set_fill(WARN, 0.12)
        col_n = Rectangle(width=L * (1 - prior), height=L).set_stroke(ACCENT, 2).set_fill(ACCENT, 0.12)
        col_s.move_to(origin, DL)
        col_n.move_to(origin + RIGHT * L * prior, DL)
        name_s = caption("스팸", 24, WARN).next_to(col_s, UP, buff=0.12)
        name_n = caption("정상", 24, ACCENT).next_to(col_n, UP, buff=0.12)
        w_s = Tex(R"\tfrac14", font_size=30).set_color(WARN).next_to(col_s, DOWN, buff=0.12)
        w_n = Tex(R"\tfrac34", font_size=30).set_color(ACCENT).next_to(col_n, DOWN, buff=0.12)
        self.play(FadeIn(col_s), FadeIn(col_n), FadeIn(name_s), FadeIn(name_n), FadeIn(w_s), FadeIn(w_n), run_time=0.9)
        shown = footnote(self, "사전확률 · 스팸 5통, 정상 15통")
        self.wait(1.4)

        part_s = Rectangle(width=L * prior, height=L * like_s).set_stroke(WARN, 2).set_fill(WARN, 0.75).move_to(origin, DL)
        part_n = Rectangle(width=L * (1 - prior), height=L * like_n).set_stroke(ACCENT, 2).set_fill(ACCENT, 0.75)
        part_n.move_to(origin + RIGHT * L * prior, DL)
        h_s = Tex(R"\tfrac45", font_size=30).set_color(WARN).next_to(part_s, LEFT, buff=0.12)
        h_n = Tex(R"\tfrac{2}{15}", font_size=30).set_color(ACCENT).next_to(part_n, RIGHT, buff=0.12)
        self.play(GrowFromEdge(part_s, DOWN), FadeIn(h_s), run_time=0.8)
        shown = footnote(self, "스팸 5통 중 '무료' 4통", WARN, shown)
        self.wait(1)
        self.play(GrowFromEdge(part_n, DOWN), FadeIn(h_n), run_time=0.8)
        shown = footnote(self, "정상 15통 중 '무료' 2통", ACCENT, shown)
        self.wait(1.4)

        panel = panel_of([
            Tex(R"P(S)=\tfrac14,\quad P(F\mid S)=\tfrac45,\quad P(F\mid N)=\tfrac{2}{15}").set_color(INK),
            Tex(R"P(S\cap F)=\tfrac14\cdot\tfrac45=\tfrac15").set_color(WARN),
            Tex(R"P(N\cap F)=\tfrac34\cdot\tfrac{2}{15}=\tfrac{1}{10}").set_color(ACCENT),
            Tex(R"P(S\mid F)=\frac{\frac15}{\frac15+\frac{1}{10}}=\frac{2}{3}").set_color(DONE),
        ], width=5.8, shift=UP * 0.75, buff=0.35)
        legend = VGroup(caption("S 스팸", 20, WARN), caption("N 정상", 20, ACCENT), caption("F '무료' 포함", 20, GREY_B))
        legend.arrange(RIGHT, buff=0.5).next_to(panel, UP, buff=0.3).align_to(panel, LEFT)
        self.play(FadeIn(legend), FadeIn(panel[0]), run_time=0.6)
        self.wait(1.5)
        self.play(FadeIn(panel[1]), FadeIn(panel[2]), run_time=0.7)
        shown = footnote(self, "칠한 넓이 · '무료' 가 든 메일", INK, shown)
        self.wait(1.9)

        # 칠한 두 조각만 꺼내 나란히 놓는다 — 넓이 비 2 : 1
        out_s, out_n = part_s.copy(), part_n.copy()
        pair = VGroup(out_s, out_n)
        target = pair.copy().arrange(RIGHT, buff=0, aligned_edge=DOWN).scale(0.42)
        target.next_to(panel, DOWN, buff=0.45).align_to(panel, LEFT).shift(RIGHT * 0.3)
        self.play(Transform(pair, target), run_time=1.0)
        ratio = Tex(R"\tfrac15 : \tfrac{1}{10}=2:1", font_size=34).set_color(INK).next_to(pair, RIGHT, buff=0.4)
        self.play(FadeIn(ratio), FadeIn(panel[3]), run_time=0.7)
        shown = footnote(self, "사전확률 1/4 → 사후확률 2/3", DONE, shown)
        self.wait(4.5)


# ─────────────────────────────────────────────────────────────
# 10.2 이산확률분포
# ─────────────────────────────────────────────────────────────
class ExpectationBalance(InteractiveScene):
    """표 10-1. X = 동전 두 개의 앞면 수. P(X = 0, 1, 2) = 1/4, 1/2, 1/4.

    E(X) = 1 은 막대를 올린 판의 균형점이다. 받침을 0.3 에 두면 판이 기울고 1 로 옮기면 수평이 된다.
    V(X) = Σ (x − 1)² p = 1/4 + 0 + 1/4 = 1/2, SD(X) = 1/√2.
    """
    xs = [0, 1, 2]
    ps = [0.25, 0.5, 0.25]

    def construct(self):
        head_of(self, "기댓값과 분산 · 막대의 균형점", "표 10-1 · 동전 2개의 앞면 수 X")
        mean = sum(x * p for x, p in zip(self.xs, self.ps))
        var = sum((x - mean) ** 2 * p for x, p in zip(self.xs, self.ps))
        assert abs(mean - 1) < 1e-12 and abs(var - 0.5) < 1e-12

        unit_x, unit_h = 2.3, 5.6
        base = LEFT * 5.9 + DOWN * 1.7

        def board(pivot):
            """받침이 pivot 에 있을 때의 판 · 막대. 기울기는 (평균 − 받침) 에 비례한다."""
            beam = Line(base + LEFT * 0.6, base + RIGHT * (2 * unit_x + 0.6)).set_stroke(GREY_A, 4)
            g = VGroup(beam)
            for x, p, tex in zip(self.xs, self.ps, (R"\tfrac14", R"\tfrac12", R"\tfrac14")):
                r = Rectangle(width=1.1, height=p * unit_h).set_fill(ACCENT, 0.8).set_stroke(ACCENT, 1)
                r.move_to(base + RIGHT * x * unit_x, DOWN)
                lab = Tex(tex, font_size=30).set_color(INK).next_to(r, UP, buff=0.1)
                tick = Tex(str(x), font_size=30).set_color(GREY_A).move_to(base + RIGHT * x * unit_x + UP * 0.0)
                tick.next_to(r, DOWN, buff=0.12)
                g.add(r, lab, tick)
            g.rotate(-0.28 * (mean - pivot), about_point=base + RIGHT * pivot * unit_x)
            return g

        def fulcrum(pivot):
            tri = Triangle().set_fill(DONE, 1).set_stroke(DONE, 0).set_height(0.45)
            tri.move_to(base + RIGHT * pivot * unit_x + DOWN * 0.62, UP)
            return tri

        s = ValueTracker(1.0)
        b = always_redraw(lambda: board(s.get_value()))
        f = always_redraw(lambda: fulcrum(s.get_value()))
        self.play(FadeIn(b), run_time=0.8)
        shown = footnote(self, "확률분포 · 막대의 높이 = 확률")
        self.wait(1.4)
        s.set_value(0.3)
        self.play(FadeIn(f), run_time=0.5)
        shown = footnote(self, "받침 0.3 · 오른쪽으로 기욺", WARN, shown)
        self.wait(1.9)
        self.play(s.animate.set_value(1.6), run_time=1.4)
        shown = footnote(self, "받침 1.6 · 왼쪽으로 기욺", WARN, shown)
        self.wait(1.4)
        self.play(s.animate.set_value(1.0), run_time=1.2)
        panel = panel_of([
            Tex(R"E(X)=0\cdot\tfrac14+1\cdot\tfrac12+2\cdot\tfrac14=1").set_color(DONE),
            Tex(R"V(X)=(0-1)^{2}\tfrac14+(1-1)^{2}\tfrac12+(2-1)^{2}\tfrac14=\tfrac12").set_color(CALM),
            Tex(R"SD(X)=\sqrt{V(X)}=\tfrac{1}{\sqrt2}\approx %.2f" % sqrt(var)).set_color(INK),
        ], width=6.3, shift=UP * 0.6, buff=0.6)
        self.play(FadeIn(panel[0]), run_time=0.6)
        shown = footnote(self, "균형점 1 · 기댓값 E(X)", DONE, shown)
        self.wait(2.4)

        b.clear_updaters()
        f.clear_updaters()
        y = base + UP * 3.45
        arrows = VGroup(
            Arrow(y + RIGHT * unit_x, y + RIGHT * 0.05, buff=0, thickness=3).set_color(CALM),
            Arrow(y + RIGHT * unit_x, y + RIGHT * (2 * unit_x - 0.05), buff=0, thickness=3).set_color(CALM),
        )
        dist = VGroup(Tex(R"(0-1)^{2}=1", font_size=28), Tex(R"(2-1)^{2}=1", font_size=28)).set_color(CALM)
        dist[0].next_to(arrows[0], UP, buff=0.1)
        dist[1].next_to(arrows[1], UP, buff=0.1)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(dist), run_time=0.8)
        shown = footnote(self, "균형점까지 거리의 제곱", CALM, shown)
        self.play(FadeIn(panel[1]), run_time=0.6)
        shown = footnote(self, "거리 제곱의 기댓값 · 분산 V(X)", CALM, shown)
        self.wait(2.4)
        self.play(FadeIn(panel[2]), run_time=0.6)
        self.wait(3)


class BinomialCounting(InteractiveScene):
    """정의 10-5 · 예제 10-6. 베르누이 시행 3번의 결과 8가지를 성공 수로 묶으면 1 · 3 · 3 · 1 = 3Cx 다.

    치토 앞모습(금색) = 성공(p), 뒷모습 = 실패(q). 이어서 p = 1/2 의 B(3) → B(10) → B(100) 막대와 np 자리.
    B(100, 1/2): E = 50, V = 25, σ = 5 (예제 10-6).
    """

    def construct(self):
        head_of(self, "이항분포 · 성공 수가 같은 결과", "정의 10-5 · 예제 10-6")
        outcomes = [(a, b, c) for a in (1, 0) for b in (1, 0) for c in (1, 0)]
        groups = {k: [o for o in outcomes if sum(o) == k] for k in range(4)}
        assert [len(groups[k]) for k in range(4)] == [comb(3, k) for k in range(4)]

        h = 0.62
        col_x = [-6.3, -4.2, -2.1, 0.0]
        all_trios = Group()
        count_tex = VGroup()
        for k in range(4):
            trios = Group()
            for o in groups[k]:
                trio = Group(*[chito("front", "gold", h) if v else chito("back", None, h) for v in o]).arrange(RIGHT, buff=0.05)
                trios.add(trio)
            trios.arrange(DOWN, buff=0.22)
            trios.move_to(RIGHT * (col_x[k] + 0.7) + UP * 0.2, UP).shift(UP * 0.9)
            all_trios.add(trios)
            c = VGroup(Tex(R"x=%d" % k, font_size=30).set_color(INK),
                       Tex(R"{}_{3}C_{%d}=%d" % (k, comb(3, k)), font_size=30).set_color(DONE)).arrange(DOWN, buff=0.18)
            c.move_to(RIGHT * (col_x[k] + 0.7) + DOWN * 2.0)
            count_tex.add(c)
        # 처음에는 8가지를 한 줄씩 보인 뒤(성공 수 순), 열 아래에 개수를 적는다
        self.play(LaggedStart(*[FadeIn(t) for trios in all_trios for t in trios], lag_ratio=0.12), run_time=2.0)
        shown = footnote(self, "시행 3번 · 결과 8가지")
        self.wait(1.4)
        self.play(FadeIn(count_tex, lag_ratio=0.2), run_time=1.0)
        shown = footnote(self, "성공 수 x 로 묶은 개수", DONE, shown)
        panel = panel_of([
            Tex(R"P(X=x)={}_{n}C_{x}\,p^{x}q^{\,n-x}").set_color(INK),
            Tex(R"P(X=2)={}_{3}C_{2}\,p^{2}q=3p^{2}q").set_color(DONE),
        ], width=4.3, shift=UP * 0.9, buff=0.5)
        self.play(FadeIn(panel[0]), run_time=0.6)
        self.play(FadeIn(panel[1]), run_time=0.6)
        shown = footnote(self, "결과마다 확률 p²q · 3가지", DONE, shown)
        self.wait(3.4)

        # 막대 — B(3, 1/2) → B(10, 1/2) → B(100, 1/2)
        self.play(FadeOut(all_trios), FadeOut(count_tex), FadeOut(panel[1]), run_time=0.6)
        W, H = 7.6, 3.4
        anchor = LEFT * 2.6 + DOWN * 2.3
        charts = []
        for n, lo, hi, step in ((3, 0, 3, 1), (10, 0, 10, 2), (100, 30, 70, 10)):
            axis = number_axis(lo, hi, step, W).move_to(anchor)
            ks = list(range(lo, hi + 1))
            pm = [binom_pmf(n, 0.5, k) for k in ks]
            bars = bars_on(axis, ks, pm, H / max(pm), min(0.8 * W / (hi - lo + 1), 0.9))
            mark = DashedLine(axis.n2p(n / 2), axis.n2p(n / 2) + UP * (H + 0.3)).set_stroke(DONE, 3)
            mlab = Tex(R"np=%g" % (n / 2), font_size=30).set_color(DONE).next_to(mark, UP, buff=0.08)
            name = Tex(R"B(%d,\tfrac12)" % n, font_size=36).set_color(ACCENT)
            name.move_to(axis.n2p(lo) + UP * (H + 0.2) + RIGHT * 0.6)
            charts.append(VGroup(axis, axis.labels, bars, mark, mlab, name))
        self.play(FadeIn(charts[0]), run_time=0.8)
        shown = footnote(self, "B(3, 1/2) · 높이 1 : 3 : 3 : 1", ACCENT, shown)
        self.wait(2.4)
        self.play(FadeOut(charts[0]), FadeIn(charts[1]), run_time=0.8)
        shown = footnote(self, "시행 10번 · 중심 np = 5", ACCENT, shown)
        self.wait(2.4)
        self.play(FadeOut(charts[1]), FadeIn(charts[2]), run_time=0.8)
        n = 100
        mean, var = n * 0.5, n * 0.5 * 0.5
        rows = VGroup(
            Tex(R"E(X)=np=%g" % mean).set_color(DONE),
            Tex(R"V(X)=npq=%g" % var).set_color(CALM),
            Tex(R"\sigma=\sqrt{npq}=%g" % sqrt(var)).set_color(INK),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.scale(0.85).next_to(panel[0], DOWN, buff=0.6).align_to(panel[0], LEFT)
        self.play(FadeIn(rows), run_time=0.7)
        shown = footnote(self, "예제 10-6 · 동전 100번", DONE, shown)
        self.wait(3)


class PoissonLimit(InteractiveScene):
    """정의 10-6 · 정리 10-2. λ = np = 2 로 두고 n 을 키우면 B(n, 2/n) 이 푸아송분포 P(2) 에 겹친다.

    막대는 이항분포, 점은 λ^k e^{−λ}/k!. k = 0 … 8. P(X = 2) 는 n = 10 에서 0.3020, 100 에서 0.2734, 1000 에서 0.2709, 푸아송 0.2707.
    """
    lam = 2.0
    ks = list(range(9))

    def construct(self):
        head_of(self, "이항분포와 푸아송분포", "정의 10-6 · 정리 10-2 · λ = np = 2")
        W, H = 7.0, 3.9
        axis = number_axis(0, 8, 1, W).move_to(LEFT * 2.9 + DOWN * 2.3)
        klab = Tex("k", font_size=28).set_color(GREY_B).next_to(axis, RIGHT, buff=0.2)
        pois = [self.lam ** k * exp(-self.lam) / factorial(k) for k in self.ks]
        unit_h = H / 0.31

        def bars(n):
            pm = [binom_pmf(n, self.lam / n, k) for k in self.ks]
            return bars_on(axis, self.ks, pm, unit_h, 0.62 * W / 8), pm

        b, pm10 = bars(10)
        name = Tex(R"B(10,\ \tfrac{2}{10})", font_size=36).set_color(ACCENT).move_to(axis.n2p(6.3) + UP * 3.3)
        self.play(FadeIn(axis), FadeIn(axis.labels), FadeIn(klab), FadeIn(b), FadeIn(name), run_time=0.9)
        shown = footnote(self, "막대 · 이항분포 n = 10, p = 0.2")
        self.wait(1.4)

        dots = VGroup(*[Dot(axis.n2p(k) + UP * p * unit_h, radius=0.08, color=DONE) for k, p in zip(self.ks, pois)])
        links = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center()).set_stroke(DONE, 2) for i in range(8)])
        charts = {10: (b, pm10)}
        for n in (100, 1000):
            charts[n] = bars(n)
        panel = panel_of([
            Tex(R"P(X=k)=\frac{\lambda^{k}e^{-\lambda}}{k!},\quad\lambda=2").set_color(DONE),
            Tex(R"n=10:\quad P(X=2)=%.4f" % charts[10][1][2]).set_color(ACCENT),
            Tex(R"n=100:\quad P(X=2)=%.4f" % charts[100][1][2]).set_color(ACCENT),
            Tex(R"n=1000:\quad P(X=2)=%.4f" % charts[1000][1][2]).set_color(ACCENT),
            Tex(R"P(2):\quad P(X=2)=%.4f" % pois[2]).set_color(DONE),
        ], width=4.7, shift=UP * 0.4, buff=0.42)
        self.play(FadeIn(links), FadeIn(dots), FadeIn(panel[0]), run_time=0.8)
        shown = footnote(self, "점 · 푸아송분포 P(2)", DONE, shown)
        self.play(FadeIn(panel[1]), run_time=0.5)
        self.wait(1.9)

        for i, n in enumerate((100, 1000)):
            nb = charts[n][0]
            nname = Tex(R"B(%d,\ \tfrac{2}{%d})" % (n, n), font_size=36).set_color(ACCENT).move_to(name)
            self.play(Transform(b, nb), FadeOut(name), FadeIn(nname), FadeIn(panel[2 + i]), run_time=1.2)
            self.add(links, dots)
            name = nname
            shown = footnote(self, "n = %d · p = %g" % (n, self.lam / n), ACCENT, shown)
            self.wait(2.4)
        self.play(FadeIn(panel[4]), run_time=0.6)
        shown = footnote(self, "n 증가 · p 감소 · np = 2", INK, shown)
        self.wait(4.5)


# ─────────────────────────────────────────────────────────────
# 10.3 연속확률분포
# ─────────────────────────────────────────────────────────────
class NormalStandardize(InteractiveScene):
    """정의 10-7 · 10-8 · 정리 10-4 · 예제 10-9. X ~ N(10, 2²).

    μ 를 바꾸면 곡선이 평행이동하고 σ 를 키우면 낮고 넓어진다(넓이는 1). Z = (X − 10)/2 는 축의 눈금을 바꾼 것이고
    Φ(10) = P(X ≤ 10) = P(Z ≤ 0) = 1/2 다.
    """

    def construct(self):
        head_of(self, "정규분포와 표준화", "정의 10-7 · 10-8 · 정리 10-4 · 예제 10-9")
        W = 7.8
        axis = number_axis(2, 18, 2, W).move_to(LEFT * 2.5 + DOWN * 1.9)
        xlab = Tex("x", font_size=28).set_color(GREY_B).next_to(axis, RIGHT, buff=0.2)
        unit_h = 3.6 / normal_pdf(10, 10, 1.2)
        mu, sig = ValueTracker(10.0), ValueTracker(2.0)
        curve = always_redraw(lambda: curve_on(axis, lambda t: normal_pdf(t, mu.get_value(), sig.get_value()), 2, 18, unit_h, ACCENT, 4))
        center = always_redraw(lambda: DashedLine(axis.n2p(mu.get_value()),
                                                  axis.n2p(mu.get_value()) + UP * normal_pdf(0, 0, sig.get_value()) * unit_h
                                                  ).set_stroke(GREY_B, 2))
        self.play(FadeIn(axis), FadeIn(axis.labels), FadeIn(xlab), run_time=0.6)
        self.play(ShowCreation(curve), FadeIn(center), run_time=1.0)
        panel = panel_of([
            Tex(R"f(x)=\frac{1}{\sqrt{2\pi}\,\sigma}\,e^{-\frac12\left(\frac{x-\mu}{\sigma}\right)^{2}}").set_color(INK),
            Tex(R"X\sim N(10,\ 2^{2})").set_color(ACCENT),
            Tex(R"Z=\frac{X-10}{2}\sim N(0,\ 1)").set_color(DONE),
            Tex(R"\Phi(10)=P(Z\le 0)=\tfrac12").set_color(CALM),
        ], width=4.4, shift=UP * 0.5, buff=0.5)
        self.play(FadeIn(panel[0]), FadeIn(panel[1]), run_time=0.6)
        shown = footnote(self, "μ = 10 · σ = 2")
        self.wait(1.4)

        shown = footnote(self, "μ 변경 · 곡선의 평행이동", ACCENT, shown)
        self.play(mu.animate.set_value(13), run_time=1.2)
        self.play(mu.animate.set_value(10), run_time=1.0)
        shown = footnote(self, "σ 변경 · 폭과 높이", ACCENT, shown)
        self.play(sig.animate.set_value(3.5), run_time=1.2)
        self.play(sig.animate.set_value(1.2), run_time=1.4)
        self.play(sig.animate.set_value(2.0), run_time=1.0)
        shown = footnote(self, "곡선 아래 넓이 = 1", INK, shown)
        self.wait(1.4)
        curve.clear_updaters()
        center.clear_updaters()

        # 표준화 — 같은 축에 z 눈금을 한 줄 더 단다
        zrow = VGroup()
        for x in range(4, 17, 2):
            z = (x - 10) / 2
            lab = Tex("%d" % z, font_size=24).set_color(DONE).move_to(axis.n2p(x) + DOWN * 0.85)
            zrow.add(lab)
        zname = Tex("z", font_size=28).set_color(DONE).move_to(xlab.get_center() + DOWN * 0.6)
        self.play(FadeIn(zrow, lag_ratio=0.1), FadeIn(zname), FadeIn(panel[2]), run_time=1.0)
        shown = footnote(self, "표준화 · 눈금 z = (x − 10)/2", DONE, shown)
        self.wait(2.4)
        left = area_on(axis, lambda t: normal_pdf(t, 10, 2), 2, 10, unit_h)
        self.play(FadeIn(left), FadeIn(panel[3]), run_time=0.8)
        self.add(curve)
        shown = footnote(self, "x ≤ 10 · z ≤ 0 · 넓이 절반", CALM, shown)
        self.wait(3)


class BinomialNormalApprox(InteractiveScene):
    """정리 10-5 · 10-6 · 예제 10-10. X ~ B(100, 1/2) 의 막대와 N(50, 5²) 곡선.

    μ ± σ = 45 ~ 55, μ ± 2σ = 40 ~ 60, μ ± 3σ = 35 ~ 65. 표준정규분포에서 P(|Z| ≤ 1) = 0.683, P(|Z| ≤ 2) = 0.954,
    P(|Z| ≤ 3) = 0.997 (math.erf 로 계산). 교재 정리 10-5 는 68% · 95% · 99% 로 적는다.
    """
    n, p = 100, 0.5

    def construct(self):
        head_of(self, "이항분포의 정규분포 근사", "정리 10-5 · 10-6 · 예제 10-10")
        mean = self.n * self.p
        sd = sqrt(self.n * self.p * (1 - self.p))
        assert (mean, sd) == (50, 5)
        W, H = 7.8, 3.9
        lo, hi = 30, 70
        axis = number_axis(lo, hi, 5, W).move_to(LEFT * 2.5 + DOWN * 2.3)
        ks = list(range(lo, hi + 1))
        pm = [binom_pmf(self.n, self.p, k) for k in ks]
        unit_h = H / max(pm)
        bars = bars_on(axis, ks, pm, unit_h, 0.75 * W / (hi - lo), ACCENT, 0.55)
        self.play(FadeIn(axis), FadeIn(axis.labels), run_time=0.5)
        self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.02), run_time=1.4)
        shown = footnote(self, "막대 · B(100, 1/2)")
        self.wait(1.2)
        pdf = lambda t: normal_pdf(t, mean, sd)
        curve = curve_on(axis, pdf, lo, hi, unit_h, DONE, 4)
        panel = panel_of([
            Tex(R"\mu=np=50,\quad \sigma=\sqrt{np(1-p)}=5").set_color(INK),
            Tex(R"X\ \approx\ N(50,\ 5^{2})").set_color(DONE),
        ], width=4.5, shift=UP * 1.5, buff=0.45)
        self.play(ShowCreation(curve), FadeIn(panel), run_time=1.2)
        shown = footnote(self, "곡선 · N(50, 5²)", DONE, shown)
        self.wait(1.9)

        last = panel
        prev = None
        colors = (CALM, BLUE_D, GREY_D)
        for m, color in zip((1, 2, 3), colors):
            a, b = mean - m * sd, mean + m * sd
            prob = erf(m / sqrt(2))
            area = area_on(axis, pdf, a, b, unit_h, CALM, 0.5 if m == 1 else 0.3)
            edges = VGroup(*[DashedLine(axis.n2p(v), axis.n2p(v) + UP * (pdf(v) * unit_h + 0.25)).set_stroke(WHITE, 2) for v in (a, b)])
            row = Tex(R"P(%d\le X\le %d)\approx %.1f\%%" % (a, b, 100 * prob)).set_color(CALM if m == 1 else INK)
            row.scale(panel[1].get_height() / Tex(R"X\ \approx\ N(50,\ 5^{2})").get_height() * 0.95)
            row.next_to(last, DOWN, buff=0.4).align_to(panel, LEFT)
            anims = [FadeIn(area), FadeIn(edges), FadeIn(row)]
            if prev is not None:
                anims += [FadeOut(prev[0]), FadeOut(prev[1])]
            self.play(*anims, run_time=0.9)
            self.add(curve)
            shown = footnote(self, "μ ± %dσ · %d ~ %d" % (m, a, b) if m > 1 else "μ ± σ · %d ~ %d" % (a, b), CALM, shown)
            self.wait(2.9)
            prev, last = (area, edges), row
        self.wait(3.6)


class CentralLimitDice(InteractiveScene):
    """정리 10-7. 주사위 n 개의 눈의 표본평균의 분포. n = 1 → 2 → 5 → 30.

    분포는 균등분포를 n 번 합성곱해 정확히 구한다. 평균 3.5, 분산 (35/12)/n. n = 1 은 균등, n = 2 는 삼각, n 이 커지면
    N(3.5, (35/12)/n) 곡선과 겹친다. 높이는 n 마다 최댓값에 맞춘다(폭의 변화를 본다).
    """
    ns = [1, 2, 5, 30]

    def construct(self):
        head_of(self, "중심극한정리 · 주사위의 표본평균", "정리 10-7")
        W, H = 6.8, 3.9
        anchor = LEFT * 2.5 + DOWN * 2.3
        var1 = sum((k - 3.5) ** 2 for k in range(1, 7)) / 6
        assert abs(var1 - 35 / 12) < 1e-12

        def chart(n):
            pmf = np.ones(6) / 6
            for _ in range(n - 1):
                pmf = np.convolve(pmf, np.ones(6) / 6)
            means = np.arange(n, 6 * n + 1) / n
            axis = number_axis(1, 6, 1, W).move_to(anchor)
            unit_h = H / pmf.max()
            bars = bars_on(axis, means, pmf, unit_h, max(0.8 * W / 5 / n, 0.03), ACCENT, 0.75)
            sd = sqrt(var1 / n)
            group = VGroup(axis, axis.labels, bars)
            if n >= 2:
                # 막대 넓이(확률)와 곡선 넓이를 맞춘다: 막대 간격 1/n 에 밀도를 곱한 값이 확률이다.
                curve = curve_on(axis, lambda t: normal_pdf(t, 3.5, sd) / n, 1, 6, unit_h, DONE, 3)
                group.add(curve)
            return group, sd

        panel_head = panel_of([
            Tex(R"\bar X=\frac{X_1+\cdots+X_n}{n}").set_color(INK),
            Tex(R"\mu=3.5,\quad \sigma^{2}=\tfrac{35}{12}").set_color(INK),
        ], width=4.2, shift=UP * 1.5, buff=0.45)
        self.play(FadeIn(panel_head), run_time=0.6)
        notes = {1: "주사위 1개 · 균등분포", 2: "주사위 2개의 평균 · 삼각형", 5: "주사위 5개의 평균", 30: "주사위 30개의 평균 · 종 모양"}
        shown, cur, row = None, None, None
        for n in self.ns:
            group, sd = chart(n)
            new_row = Tex(R"n=%d:\quad \tfrac{\sigma}{\sqrt n}=%.2f" % (n, sd)).set_color(DONE)
            new_row.scale(0.9).next_to(panel_head, DOWN, buff=0.55).align_to(panel_head, LEFT)
            if cur is None:
                self.play(FadeIn(group), FadeIn(new_row), run_time=0.9)
            else:
                self.play(FadeOut(cur), FadeOut(row), run_time=0.4)
                self.play(FadeIn(group), FadeIn(new_row), run_time=0.8)
            shown = footnote(self, notes[n], ACCENT if n < 30 else DONE, shown)
            cur, row = group, new_row
            self.wait(3.1)
        final = Tex(R"\bar X\ \approx\ N(\mu,\ \sigma^{2}/n)").set_color(CALM)
        final.scale(0.95).next_to(row, DOWN, buff=0.5).align_to(panel_head, LEFT)
        self.play(FadeIn(final), run_time=0.6)
        shown = footnote(self, "곡선 · N(3.5, σ²/n)", DONE, shown)
        self.wait(3)
