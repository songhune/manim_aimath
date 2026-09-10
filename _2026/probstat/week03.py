"""확률과통계 「확률」 장 (Walpole Chapter 2) 2.6–2.8 — 조건부확률 · 독립 · 곱셈법칙 · 전확률 · 베이즈.

강의 교안 `확률과통계/교육메모/03주차.md` 의 시각화 보조자료. 도구와 규칙은 week02.py 와 같다.
개념 영상은 개념 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음·풀이 슬라이드 앞이다(하네스 3.6).
소재는 교재가 정의 옆에 둔 보기(Table 2.1 의 900 명, 정의 2.11 의 주사위와 카드)와 수업에서 다루는
예제(2.34, 2.36, 2.38, 2.41, 2.42)로 한정한다.

덱 삽입 자리 (원본 PS1_02_restyled.pptx 기준):
    ConditionalProbability   42 앞   Definition 2.10 (Table 2.1 의 900 명을 단위 정사각형에. 넓이 = 확률, 조건 = 조각을 남기고 늘리기)
    Example234Flights        44 뒤   Ex 2.34 (넓이 모형, 두 방향으로 늘린다)
    SuneungConditional       52 뒤   2026학년도 수능 확통 28번 슬라이드(insert_videos 가 끼운다) 다음. 곱셈법칙 끝, 전확률 앞
    Independence             46 앞   Definition 2.11 (Table 2.1 → 종속, 복원 카드 → 독립. 가르는 선이 수평이면 독립)
    ProductRule              48 앞   Theorem 2.10–2.12 (Table 2.1 의 나무)
    Example236Fuses          49 뒤   Ex 2.36
    Example238Emergency      51 뒤   Ex 2.38
    TotalProbability         53 앞   Theorem 2.13 (분할과 넓이)
    Example241Machines       54 뒤   Ex 2.41
    BayesRule                56 앞   Theorem 2.14
    Example242Bayes          57 뒤   Ex 2.42

참고: legacy/_2018/eop/chapter1/area_model_bayes.py (분할을 세로 띠로, 조건부확률을 띠 안의 높이로
그리는 넓이 모형), legacy/_2019/bayes/part1.py (BayesDiagram). 전개 순서만 따르고 코드는 옮기지 않았다.
"""
from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MED_COLOR, MUTED, WARN, BODY_FONT,
    chito, crowd, label, note, panel, ring, slide_title, swap, counter, freeze, bar,
)
from _2026.probstat.week02 import die_face, letter_chip, branch


# ─────────────────────────────────────────────────────────────
# 공용 그림
# ─────────────────────────────────────────────────────────────
T21 = {("M", "E"): 460, ("M", "U"): 40, ("W", "E"): 140, ("W", "U"): 260}     # Table 2.1


def table21(cell_w=1.9, cell_h=0.85):
    """Table 2.1. 셀 (행, 열) → Tex 숫자. 행 M·W, 열 E·U, 합계 행·열까지."""
    rows = ["M", "W", "Total"]
    cols = ["E", "U", "Total"]
    vals = {}
    for r in rows:
        for c in cols:
            if r == "Total" and c == "Total":
                v = 900
            elif r == "Total":
                v = sum(T21[(rr, c)] for rr in "MW")
            elif c == "Total":
                v = sum(T21[(r, cc)] for cc in "EU")
            else:
                v = T21[(r, c)]
            vals[(r, c)] = v
    grid = VGroup()
    cells = {}
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            box = Rectangle(width=cell_w, height=cell_h).set_stroke(GREY_C, 1.5)
            box.move_to([(j - 1) * cell_w, -(i - 1) * cell_h, 0])
            num = Tex(f"{vals[(r, c)]:,}".replace(",", "{,}")).scale(0.85).set_color(INK).move_to(box)
            if r == "Total" or c == "Total":
                num.set_color(GREY_B)
            cells[(r, c)] = VGroup(box, num)
            grid.add(cells[(r, c)])
    head_c = VGroup(*[note(t, 24, GREY_A).move_to([(j - 1) * cell_w, cell_h * 1.55, 0])
                      for j, t in enumerate(["employed", "unemployed", "total"])])
    head_r = VGroup(*[note(t, 24, GREY_A).move_to([-cell_w * 2.05, -(i - 1) * cell_h, 0])
                      for i, t in enumerate(["men", "women", "total"])])
    return VGroup(grid, head_c, head_r), cells


def tree3(priors, likes, names, colors, x0=-4.6, x1=-1.4, x2=1.6, ys=(2.0, 0.2, -1.6), scale=0.8):
    """세 갈래 나무. 뿌리 → Bᵢ (사전확률) → A (조건부확률). (뿌리, 가지 점, 잎 점, 가지 글자, 잎 글자)."""
    root = Dot(radius=0.09).set_color(GREY_A).move_to([x0, 0.2, 0])
    mids, leaves, mid_tex, leaf_tex, lines = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
    for p, q, nm, col, y in zip(priors, likes, names, colors, ys):
        m = Dot(radius=0.08).set_color(col).move_to([x1, y, 0])
        lf = Dot(radius=0.08).set_color(col).move_to([x2, y, 0])
        l1 = Line(root.get_center(), m.get_center()).set_stroke(col, 2.5)
        l2 = Line(m.get_center(), lf.get_center()).set_stroke(col, 2.5)
        t1 = Tex(p).scale(scale).set_color(col).next_to(l1.get_center(), UP, buff=0.12)
        t2 = Tex(q).scale(scale).set_color(col).next_to(l2, UP, buff=0.1)
        nlab = Tex(nm).scale(scale).set_color(col).next_to(m, DOWN, buff=0.12)
        mids.add(m); leaves.add(lf); lines.add(l1, l2); mid_tex.add(t1, nlab); leaf_tex.add(t2)
    return root, mids, leaves, lines, mid_tex, leaf_tex


# ─────────────────────────────────────────────────────────────
# 넓이 모형 — 확률공간을 단위 정사각형으로 그린다. 넓이가 확률이다.
# 조건은 "정사각형의 한 조각만 남기고 그 조각을 다시 정사각형으로 늘리는 일"(재정규화)이다.
# 참고: legacy/_2019/bayes/part1.py 의 BayesDiagram (같은 넓이 모형).
# ─────────────────────────────────────────────────────────────
def region(x0, y0, w, h, color, opacity=0.18, stroke=2):
    """왼쪽 아래 (x0, y0) 에서 폭 w, 높이 h 인 조각."""
    r = Rectangle(width=w, height=h).set_stroke(color, stroke).set_fill(color, opacity)
    r.move_to([x0 + w / 2, y0 + h / 2, 0])
    return r


def people_in(rect, n, cols, pose="front", tint=None, height=0.34, seed=0):
    """조각 안에 치토 n 마리를 격자로 채운다. 조각보다 크면 줄인다."""
    g = crowd(n, -(-n // cols), cols, pose=pose, tint=tint, height=height, buff=0.05, jitter=0.0, seed=seed)
    if g.get_width() > rect.get_width() * 0.94:
        g.set_width(rect.get_width() * 0.94)
    if g.get_height() > rect.get_height() * 0.94:
        g.set_height(rect.get_height() * 0.94)
    g.move_to(rect)
    return g


def city_pin(color=WARN, size=0.32):
    """지도 핀. 동네 하나를 가리키는 표시."""
    head = Circle(radius=size / 2).set_stroke(color, 2).set_fill(color, 0.9)
    tip = Triangle().set_stroke(width=0).set_fill(color, 0.9)
    tip.set_width(size * 0.8).set_height(size * 0.55, stretch=True).rotate(PI)
    tip.next_to(head, DOWN, buff=-size * 0.12)
    hole = Circle(radius=size / 6).set_stroke(width=0).set_fill(BLACK, 1).move_to(head)
    return VGroup(head, tip, hole)


# ─────────────────────────────────────────────────────────────
# 1. 조건부확률 (2.6) — 슬라이드 42 (Definition 2.10) 앞
# ─────────────────────────────────────────────────────────────
class ConditionalProbability(InteractiveScene):
    """Table 2.1 의 900 명을 단위 정사각형에 넣는다(치토 한 마리 = 10 명). 넓이가 확률이다.
    세로로 E·U, 그 안을 M·W 로 가르면 아홉 숫자가 네 조각의 넓이가 된다.
    'E 가 일어났다' 는 U 조각을 지우고 남은 E 조각을 다시 정사각형으로 늘리는 일이다.
    늘어난 정사각형에서 M 조각의 넓이 460/600 이 P(M | E). 분모 P(E) 는 늘리는 배율이다."""
    SIDE = 4.6

    def construct(self):
        head = slide_title("Conditional Probability")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        W = self.SIDE
        x0, y0 = -5.6, -2.6
        S = region(x0, y0, W, W, GREY_B, 0.0, 2.5)
        pin = city_pin().next_to(S, UP, buff=0.18).align_to(S, LEFT)
        town = note("Suwon · 900 adults", 26, GREY_A).next_to(pin, RIGHT, buff=0.15)
        self.play(ShowCreation(S), FadeIn(pin), FadeIn(town))
        everyone = people_in(S, 90, 9)
        self.play(LaggedStartMap(FadeIn, everyone, lag_ratio=0.01), run_time=1.4)
        area1 = Tex(R"\text{area} = P(S) = 1").set_color(GREY_A).scale(0.85).move_to([3.4, 2.5, 0])
        self.play(FadeIn(area1))
        self.wait(0.6)

        # ── 세로로 가른다: E 600 / U 300
        wE = W * 600 / 900
        rE = region(x0, y0, wE, W, CALM, 0.14)
        rU = region(x0 + wE, y0, W - wE, W, MUTED, 0.14)
        tE = note("E · employed 600", 22, CALM).next_to(rE, DOWN, buff=0.15)
        tU = note("U · 300", 22, MUTED).next_to(rU, DOWN, buff=0.15)
        self.play(FadeOut(everyone), FadeIn(rE), FadeIn(rU), FadeIn(tE), FadeIn(tU), run_time=0.8)
        # 남 46 / 여 14 (E), 남 4 / 여 26 (U). 여자는 gold, 일하지 않는 사람은 등을 돌린다.
        hEM, hUM = W * 460 / 600, W * 40 / 300
        rEM = region(x0, y0, wE, hEM, ACCENT, 0.22)
        rEW = region(x0, y0 + hEM, wE, W - hEM, MEAN_COLOR, 0.16)
        rUM = region(x0 + wE, y0, W - wE, hUM, ACCENT, 0.22)
        rUW = region(x0 + wE, y0 + hUM, W - wE, W - hUM, MEAN_COLOR, 0.16)
        pEM = people_in(rEM, 46, 6, "front", None)
        pEW = people_in(rEW, 14, 6, "front", "gold")
        pUM = people_in(rUM, 4, 3, "back", None)
        pUW = people_in(rUW, 26, 3, "back", "gold")
        pe = Tex(R"P(E) = \frac{600}{900}").set_color(CALM).scale(0.8).move_to([3.4, 1.75, 0])
        self.play(LaggedStartMap(FadeIn, Group(pEM, pEW, pUM, pUW), lag_ratio=0.01), Write(pe), run_time=1.4)
        self.play(FadeIn(rEM), FadeIn(rEW), FadeIn(rUM), FadeIn(rUW), run_time=0.6)
        nEM = Tex("460").scale(0.8).set_color(WHITE).move_to(rEM.get_corner(UR) + DL * 0.35)
        nEW = Tex("140").scale(0.8).set_color(WHITE).move_to(rEW.get_corner(UR) + DL * 0.35)
        nUM = Tex("40").scale(0.7).set_color(WHITE).move_to(rUM.get_corner(UR) + DL * 0.3)
        nUW = Tex("260").scale(0.8).set_color(WHITE).move_to(rUW.get_corner(UR) + DL * 0.35)
        pem = Tex(R"P(E \cap M) = \frac{460}{900}").set_color(ACCENT).scale(0.8).move_to([3.4, 1.0, 0]).align_to(pe, LEFT)
        legend = Group(chito("front", None, 0.34), note("men", 22, ACCENT), chito("front", "gold", 0.34), note("women", 22, MEAN_COLOR))
        legend.arrange(RIGHT, buff=0.18).move_to([3.4, 0.2, 0]).align_to(pe, LEFT)
        self.play(FadeIn(nEM), FadeIn(nEW), FadeIn(nUM), FadeIn(nUW), Write(pem), FadeIn(legend))
        self.wait(1.0)

        # ── E 가 일어났다: U 조각을 지우고 E 조각을 정사각형으로 늘린다
        given = Tex(R"\text{given } E").set_color(CALM).scale(1.0).move_to([3.4, -0.7, 0]).align_to(pe, LEFT)
        self.play(FadeIn(given),
                  *[FadeOut(m) for m in (rU, rUM, rUW, pUM, pUW, nUM, nUW, tU)], run_time=0.8)
        k = W / wE                                        # 늘리는 배율 = 1 / P(E)
        new_rE = region(x0, y0, W, W, CALM, 0.14)
        new_rEM = region(x0, y0, W, hEM, ACCENT, 0.22)
        new_rEW = region(x0, y0 + hEM, W, W - hEM, MEAN_COLOR, 0.16)
        pEM.generate_target(); pEM.target = people_in(new_rEM, 46, 9, "front", None)
        pEW.generate_target(); pEW.target = people_in(new_rEW, 14, 9, "front", "gold")
        factor = Tex(R"\times \frac{900}{600}").set_color(CALM).scale(0.8).next_to(S, RIGHT, buff=0.15).set_y(y0 + W * 0.5)
        self.play(Transform(rE, new_rE), Transform(rEM, new_rEM), Transform(rEW, new_rEW),
                  MoveToTarget(pEM), MoveToTarget(pEW),
                  nEM.animate.move_to(new_rEM.get_corner(UR) + DL * 0.35),
                  nEW.animate.move_to(new_rEW.get_corner(UR) + DL * 0.35),
                  tE.animate.next_to(new_rE, DOWN, buff=0.15), FadeIn(factor), run_time=1.6)
        self.wait(0.5)
        area_now = Tex(R"\text{area} = \frac{460}{600}").set_color(ACCENT).scale(0.9).move_to([3.4, -1.65, 0]).align_to(pe, LEFT)
        self.play(FlashAround(rEM, color=ACCENT, buff=0.05), Write(area_now), run_time=1.2)
        self.wait(0.8)

        # ── 식: 늘린 넓이는 원래 넓이를 P(E) 로 나눈 것
        self.play(*[FadeOut(m) for m in (area1, pe, pem, legend, given, area_now, factor)], run_time=0.5)
        defn = Tex(R"P(M \mid E) = \frac{460/900}{600/900} = \frac{P(E \cap M)}{P(E)}",
                   t2c={"P(E)": CALM, R"P(E \cap M)": ACCENT}).scale(0.9).move_to([3.3, 1.7, 0])
        if defn.get_right()[0] > 6.9:
            defn.scale(0.85).move_to([3.1, 1.7, 0])
        self.play(Write(defn))
        self.wait(0.6)
        general = Tex(R"P(B \mid A) = \frac{P(A \cap B)}{P(A)}").set_color(WHITE).scale(1.1).move_to([3.3, -0.4, 0])
        self.play(FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        renorm = note("divide by P(A): rescale", 24, GREY_B).next_to(general, DOWN, buff=0.35)
        self.play(FadeIn(renorm))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.34 — 정시 출발·정시 도착. 원본 44 뒤 (풀이 45 앞)
# ─────────────────────────────────────────────────────────────
class Example234Flights(InteractiveScene):
    """같은 넓이 모형. 세로로 D(0.83)·D′, 그 안을 A 로 가르면 0.78 · 0.05 · 0.04 · 0.13.
    (a) D 를 남기고 늘리면 A 조각이 0.78/0.83. (b) 가로로 A(0.82) 를 남기고 늘리면 D 조각이 0.78/0.82.
    같은 0.78 을 다른 방향으로 늘린다."""
    SIDE = 4.4

    def construct(self):
        head = slide_title("Example 2.34")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        given = Tex(R"P(D) = 0.83, \quad P(A) = 0.82, \quad P(D \cap A) = 0.78",
                    t2c={"P(D)": ACCENT, "P(A)": CALM, R"P(D \cap A)": MEAN_COLOR}).scale(0.85)
        given.next_to(head[1], DOWN, buff=0.25)
        self.play(FadeIn(given, UP))

        W = self.SIDE
        x0, y0 = -5.9, -3.0
        S = region(x0, y0, W, W, GREY_B, 0.0, 2.5)
        wD = W * 0.83
        rD = region(x0, y0, wD, W, ACCENT, 0.10)
        rN = region(x0 + wD, y0, W - wD, W, MUTED, 0.10)
        hDA, hNA = W * 0.78 / 0.83, W * 0.04 / 0.17
        rDA = region(x0, y0, wD, hDA, MEAN_COLOR, 0.35)
        rNA = region(x0 + wD, y0, W - wD, hNA, CALM, 0.35)
        labels = VGroup(
            Tex("0.78").scale(0.9).move_to(rDA),
            Tex("0.05").scale(0.8).move_to([x0 + wD / 2, y0 + hDA + (W - hDA) / 2, 0]),
            Tex("0.04").scale(0.6).move_to(rNA),
            Tex("0.13").scale(0.7).move_to([x0 + wD + (W - wD) / 2, y0 + hNA + (W - hNA) / 2, 0]),
        ).set_color(WHITE)
        tD = Tex("D").set_color(ACCENT).next_to(rD, DOWN, buff=0.12)
        tN = Tex("D'").set_color(MUTED).next_to(rN, DOWN, buff=0.12)
        tA = Tex("A").set_color(MEAN_COLOR).next_to(S, LEFT, buff=0.15).set_y(y0 + hDA / 2)
        self.play(ShowCreation(S), FadeIn(rD), FadeIn(rN), FadeIn(tD), FadeIn(tN))
        self.play(FadeIn(rDA), FadeIn(rNA), FadeIn(tA), FadeIn(labels))
        self.wait(0.8)

        # (a) D 를 남기고 옆으로 늘린다
        qa = Tex(R"\text{(a)}\ \text{given } D").set_color(ACCENT).scale(0.9).move_to([3.3, 2.0, 0])
        self.play(FadeIn(qa), FadeOut(rN), FadeOut(rNA), FadeOut(tN), FadeOut(labels[2]), FadeOut(labels[3]), run_time=0.6)
        self.play(Transform(rD, region(x0, y0, W, W, ACCENT, 0.10)),
                  Transform(rDA, region(x0, y0, W, hDA, MEAN_COLOR, 0.35)),
                  labels[0].animate.move_to([x0 + W / 2, y0 + hDA / 2, 0]),
                  labels[1].animate.move_to([x0 + W / 2, y0 + hDA + (W - hDA) / 2, 0]),
                  tD.animate.next_to(S, DOWN, buff=0.12), run_time=1.2)
        ra = Tex(R"P(A \mid D) = \frac{0.78}{0.83} \approx 0.94", t2c={"0.83": ACCENT, "0.78": MEAN_COLOR}).scale(0.9)
        ra.next_to(qa, DOWN, buff=0.3).align_to(qa, LEFT)
        self.play(Write(ra))
        self.wait(1.2)

        # (b) 되돌린 뒤 가로로 A 를 남기고 위로 늘린다
        self.play(Transform(rD, region(x0, y0, wD, W, ACCENT, 0.10)),
                  Transform(rDA, region(x0, y0, wD, hDA, MEAN_COLOR, 0.35)),
                  labels[0].animate.move_to([x0 + wD / 2, y0 + hDA / 2, 0]),
                  labels[1].animate.move_to([x0 + wD / 2, y0 + hDA + (W - hDA) / 2, 0]),
                  tD.animate.next_to(region(x0, y0, wD, W, ACCENT), DOWN, buff=0.12),
                  FadeIn(rN), FadeIn(rNA), FadeIn(tN), FadeIn(labels[2]), FadeIn(labels[3]), run_time=1.0)
        # 가로 자르기: A 띠(높이 0.82) 안에서 D 의 폭이 0.78/0.82
        hA = W * 0.82
        wAD = W * 0.78 / 0.82
        rA = region(x0, y0, W, hA, MEAN_COLOR, 0.10)
        rAD = region(x0, y0, wAD, hA, ACCENT, 0.35)
        qb = Tex(R"\text{(b)}\ \text{given } A").set_color(MEAN_COLOR).scale(0.9).next_to(ra, DOWN, buff=0.7).align_to(qa, LEFT)
        self.play(FadeOut(rD), FadeOut(rDA), FadeOut(rN), FadeOut(rNA), FadeOut(labels), FadeOut(tD), FadeOut(tN), FadeOut(tA), run_time=0.5)
        l78 = Tex("0.78").scale(0.9).set_color(WHITE).move_to(rAD)
        l04 = Tex("0.04").scale(0.6).set_color(WHITE).move_to([x0 + wAD + (W - wAD) / 2, y0 + hA / 2, 0])
        l18 = Tex("0.18").scale(0.7).set_color(WHITE).move_to([x0 + W / 2, y0 + hA + (W - hA) / 2, 0])
        self.play(FadeIn(rA), FadeIn(rAD), FadeIn(l78), FadeIn(l04), FadeIn(l18), FadeIn(qb), run_time=0.8)
        self.play(FadeOut(l18), Transform(rA, region(x0, y0, W, W, MEAN_COLOR, 0.10)),
                  Transform(rAD, region(x0, y0, wAD, W, ACCENT, 0.35)),
                  l78.animate.move_to([x0 + wAD / 2, y0 + W / 2, 0]),
                  l04.animate.move_to([x0 + wAD + (W - wAD) / 2, y0 + W / 2, 0]), run_time=1.2)
        rb = Tex(R"P(D \mid A) = \frac{0.78}{0.82} \approx 0.95", t2c={"0.82": MEAN_COLOR, "0.78": ACCENT}).scale(0.9)
        rb.next_to(qb, DOWN, buff=0.3).align_to(qa, LEFT)
        self.play(Write(rb))
        same = note("same piece, different stretch", 24, GREY_B).next_to(rb, DOWN, buff=0.35).align_to(qa, LEFT)
        self.play(FadeIn(same))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2026학년도 수능 확률과 통계 28번 — 조건부확률 + 곱셈법칙. 덱에 끼운 문제 슬라이드 뒤 (원본 52 뒤, 곱셈법칙 끝)
# ─────────────────────────────────────────────────────────────
def trial_info(k):
    """눈 k 한 번의 결과: (공의 개수, 3번 상자 − 2번 상자)."""
    if k % 2 == 1:
        return 3, 1
    if k == 2:
        return 2, -1
    if k == 4:
        return 3, -1
    return 4, 0


ODD = "1,3,4,5"          # 공이 홀수 개인 눈
EVEN = "2,6"             # 공이 짝수 개인 눈


class SuneungConditional(InteractiveScene):
    """등가능 표본공간이라 칸 수로 센다는 것이 이 문제의 특수성이다. 주사위를 4번 던지므로 표본공간은
    6⁴ = 1296 으로 고정되어 있고, 조건부확률은 n(A ∩ B)/n(A) 다.
    네 번의 결과를 괄호 네 칸으로 적고 칸마다 올 수 있는 눈을 넣는다. (1,3,4,5 | 2,6 | 2,6 | 2,6) 은
    첫 시행만 공이 홀수 개인 경우이고 4·2·2·2 = 32 가지. 홀수 시행의 자리가 넷이니 4 × 32 = 128.
    홀수 시행 3번은 (1,3,4,5 | 1,3,4,5 | 1,3,4,5 | 2,6) 꼴 네 자리, 4 × 4·4·4·2 = 512 → n(A) = 640.
    A 안에서 3번 − 2번 = 1 인 무늬는 (1,3,5 | 6 | 6 | 6) 네 자리 × 3 = 12 와
    (1,3,5 | 1,3,5 | 4 | 6) 12 가지 순서 × 3·3 = 108 → n(A ∩ B) = 120. P(B | A) = 120/640 = 3/16. 답 ②."""

    def tuple_row(self, labels, colors, w=1.05, h=0.46, size=0.5):
        """괄호 네 칸. labels 는 칸마다 올 수 있는 눈."""
        cells = VGroup()
        for lab, col in zip(labels, colors):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.08).set_stroke(col, 1.8).set_fill(col, 0.10)
            t = Tex(lab).scale(size).set_color(col).move_to(r)
            cells.add(VGroup(r, t))
        cells.arrange(RIGHT, buff=0.1)
        lp = Tex("(").scale(1.1).set_color(GREY_B).next_to(cells, LEFT, buff=0.05)
        rp = Tex(")").scale(1.1).set_color(GREY_B).next_to(cells, RIGHT, buff=0.05)
        return VGroup(lp, cells, rp)

    def pattern_block(self, rows_spec, center, count_tex, color):
        """자리 무늬 여러 줄. 첫 줄 오른쪽에 한 줄의 가짓수. rows_spec = [(labels, colors), ...]"""
        rows = VGroup(*[self.tuple_row(l, c) for l, c in rows_spec]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        rows.move_to(center)
        each = Tex(count_tex).scale(0.65).set_color(color).next_to(rows[0], RIGHT, buff=0.35)
        return rows, each

    def total_line(self, rows, total_tex, color, note_tex=None):
        """마지막 줄 오른쪽에 무늬 수 × 한 줄 가짓수. 옆에 조합 기호가 그 무늬 고르기라는 메모."""
        eq = Tex(total_tex).scale(0.75).set_color(color).next_to(rows[-1], RIGHT, buff=0.35)
        if note_tex is None:
            return eq, None
        nt = Tex(note_tex).scale(0.55).set_color(GREY_B).next_to(eq, RIGHT, buff=0.3)
        return eq, nt

    def construct(self):
        head = slide_title("CSAT 2026 · Problem 28")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 1) 눈 여섯 → 두 부류. 공이 홀수 개인 눈 넷, 짝수 개인 눈 둘.
        faces = VGroup(*[die_face(k, 0.5, GREY_A) for k in range(1, 7)]).arrange(RIGHT, buff=0.3).move_to([-3.2, 2.2, 0])
        balls = VGroup(*[Tex(str(trial_info(k)[0])).scale(0.65).set_color(CALM if trial_info(k)[0] % 2 else MUTED).next_to(f, DOWN, buff=0.1)
                         for k, f in zip(range(1, 7), faces)])
        bl = note("balls", 22, GREY_B).next_to(balls, LEFT, buff=0.3)
        self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.1), FadeIn(balls), FadeIn(bl))
        rings = VGroup(*[ring(faces[k - 1], CALM, buff=0.05) for k in (1, 3, 4, 5)])
        odd_tag = Tex(R"\text{odd balls: } 1, 3, 4, 5").scale(0.7).set_color(CALM).move_to([3.6, 2.4, 0])
        even_tag = Tex(R"\text{even balls: } 2, 6").scale(0.7).set_color(MUTED).next_to(odd_tag, DOWN, buff=0.2).align_to(odd_tag, LEFT)
        self.play(ShowCreation(rings), FadeIn(odd_tag), FadeIn(even_tag))
        self.wait(0.8)

        # ── 2) 표본공간: 괄호 네 칸에 눈 6가지씩. 6⁴ 으로 크기가 고정된 등가능 공간이라 칸 수로 센다.
        S_row = self.tuple_row(["1..6", "1..6", "1..6", "1..6"], [GREY_A] * 4).move_to([-3.2, 0.9, 0])
        s_tag = note("4 throws", 22, GREY_B).next_to(S_row, UP, buff=0.15).align_to(S_row, LEFT)
        self.play(FadeIn(S_row), FadeIn(s_tag))
        ns = Tex(R"n(S) = 6 \cdot 6 \cdot 6 \cdot 6 = 1296").scale(0.85).set_color(GREY_A).move_to([3.6, 0.9, 0])
        fixed = note("fixed, equally likely", 22, GREY_B).next_to(ns, DOWN, buff=0.15)
        count_rule = Tex(R"P(B \mid A) = \frac{n(A \cap B)}{n(A)}").scale(0.85).set_color(WHITE).next_to(fixed, DOWN, buff=0.3)
        self.play(Write(ns), FadeIn(fixed))
        self.play(Write(count_rule))
        self.wait(1.0)

        # ── 3) n(A): 홀수 시행이 1번 — 괄호에 올 수 있는 눈을 적고 곱한다. 자리가 넷.
        self.play(FadeOut(S_row), FadeOut(s_tag), FadeOut(count_rule), FadeOut(fixed),
                  ns.animate.scale(0.8).move_to([3.6, 1.45, 0]), run_time=0.5)
        a_head = Tex(R"A:\ \text{odd total} \Leftrightarrow 1 \text{ or } 3 \text{ odd trials}").scale(0.7).set_color(CALM)
        a_head.move_to([-2.4, 1.3, 0])
        self.play(FadeIn(a_head))

        C1 = [CALM, MUTED, MUTED, MUTED]
        k1_rows, k1_each = self.pattern_block(
            [([ODD, EVEN, EVEN, EVEN], C1), ([EVEN, ODD, EVEN, EVEN], [MUTED, CALM, MUTED, MUTED]),
             ([EVEN, EVEN, ODD, EVEN], [MUTED, MUTED, CALM, MUTED]), ([EVEN, EVEN, EVEN, ODD], [MUTED, MUTED, MUTED, CALM])],
            [-3.6, -0.1, 0], R"4 \cdot 2 \cdot 2 \cdot 2 = 32", CALM)
        self.play(FadeIn(k1_rows[0]), Write(k1_each))
        self.wait(0.4)
        self.play(LaggedStartMap(FadeIn, VGroup(*k1_rows[1:]), lag_ratio=0.25), run_time=0.9)
        k1_eq, k1_nt = self.total_line(k1_rows, R"4 \times 32 = 128", CALM, R"4 \text{ patterns} = \binom{4}{1}")
        self.play(Write(k1_eq))
        self.play(FadeIn(k1_nt))
        self.wait(0.6)

        # k = 3
        k3_rows, k3_each = self.pattern_block(
            [([ODD, ODD, ODD, EVEN], [CALM, CALM, CALM, MUTED]), ([ODD, ODD, EVEN, ODD], [CALM, CALM, MUTED, CALM]),
             ([ODD, EVEN, ODD, ODD], [CALM, MUTED, CALM, CALM]), ([EVEN, ODD, ODD, ODD], [MUTED, CALM, CALM, CALM])],
            [-3.6, -2.45, 0], R"4 \cdot 4 \cdot 4 \cdot 2 = 128", CALM)
        self.play(FadeIn(k3_rows[0]), Write(k3_each))
        self.play(LaggedStartMap(FadeIn, VGroup(*k3_rows[1:]), lag_ratio=0.25), run_time=0.9)
        k3_eq, k3_nt = self.total_line(k3_rows, R"4 \times 128 = 512", CALM, R"4 \text{ patterns} = \binom{4}{3}")
        self.play(Write(k3_eq), FadeIn(k3_nt))
        na = Tex(R"n(A) = 128 + 512 = 640").scale(0.85).set_color(CALM).move_to([3.6, 0.7, 0])
        self.play(TransformFromCopy(VGroup(k1_eq, k3_eq), na), run_time=1.0)
        self.wait(1.0)

        # ── 4) n(A ∩ B): Δ 의 합이 +1 이 되는 눈의 무늬는 둘뿐
        self.play(*[FadeOut(m) for m in (k1_rows, k1_each, k1_eq, k1_nt, k3_rows, k3_each, k3_eq, k3_nt, a_head)], run_time=0.5)
        b_head = Tex(R"B:\ \text{box 3} - \text{box 2} = 1 \text{ inside } A").scale(0.7).set_color(MEAN_COLOR).move_to([-2.4, 1.3, 0])
        self.play(FadeIn(b_head))
        Y, M = MEAN_COLOR, MUTED
        p1_rows, p1_each = self.pattern_block(
            [(["1,3,5", "6", "6", "6"], [Y, M, M, M]), (["6", "1,3,5", "6", "6"], [M, Y, M, M]),
             (["6", "6", "1,3,5", "6"], [M, M, Y, M]), (["6", "6", "6", "1,3,5"], [M, M, M, Y])],
            [-3.6, -0.1, 0], R"3 \cdot 1 \cdot 1 \cdot 1 = 3", Y)
        self.play(FadeIn(p1_rows[0]), Write(p1_each))
        self.play(LaggedStartMap(FadeIn, VGroup(*p1_rows[1:]), lag_ratio=0.25), run_time=0.9)
        p1_eq, p1_nt = self.total_line(p1_rows, R"4 \times 3 = 12", Y, R"4 \text{ patterns}")
        self.play(Write(p1_eq), FadeIn(p1_nt))
        self.wait(0.5)
        p2_rows, p2_each = self.pattern_block(
            [(["1,3,5", "1,3,5", "4", "6"], [Y, Y, M, M]), (["1,3,5", "4", "1,3,5", "6"], [Y, M, Y, M]),
             (["4", "6", "1,3,5", "1,3,5"], [M, M, Y, Y])],
            [-3.6, -2.3, 0], R"3 \cdot 3 \cdot 1 \cdot 1 = 9", Y)
        dots = Tex(R"\cdots").scale(0.8).set_color(GREY_B).next_to(p2_rows, DOWN, buff=0.1).align_to(p2_rows[0][1], LEFT)
        self.play(FadeIn(p2_rows[0]), Write(p2_each))
        self.play(LaggedStartMap(FadeIn, VGroup(*p2_rows[1:]), lag_ratio=0.25), FadeIn(dots), run_time=0.9)
        p2_eq, p2_nt = self.total_line(p2_rows, R"12 \times 9 = 108", Y, R"12 \text{ patterns} = \tfrac{4!}{2!}")
        self.play(Write(p2_eq), FadeIn(p2_nt))
        nab = Tex(R"n(A \cap B) = 12 + 108 = 120").scale(0.85).set_color(Y).next_to(na, DOWN, buff=0.35).align_to(na, LEFT)
        self.play(TransformFromCopy(VGroup(p1_eq, p2_eq), nab), run_time=1.0)
        self.wait(1.0)

        # ── 5) A 가 일어났다: 640 가지가 세계. 그 안의 120 가지.
        self.play(*[FadeOut(m) for m in (p1_rows, p1_each, p1_eq, p1_nt, p2_rows, p2_each, p2_eq, p2_nt, dots, b_head, faces, balls, bl, rings)], run_time=0.5)
        Wb = 8.0
        bar = Rectangle(width=Wb, height=0.9).set_stroke(CALM, 2.5).set_fill(CALM, 0.18).move_to([-2.4, -0.5, 0])
        part = Rectangle(width=Wb * 120 / 640, height=0.9).set_stroke(width=0).set_fill(Y, 0.8).align_to(bar, LEFT).set_y(bar.get_y())
        t640 = Tex("640").scale(0.7).set_color(CALM).next_to(bar, DOWN, buff=0.15).align_to(bar, RIGHT)
        t120 = Tex("120").scale(0.7).set_color(Y).next_to(part, DOWN, buff=0.15)
        given = Tex(R"\text{given } A").set_color(CALM).scale(0.9).next_to(bar, UP, buff=0.15).align_to(bar, LEFT)
        self.play(FadeIn(bar), FadeIn(given), FadeIn(t640))
        self.play(GrowFromEdge(part, LEFT), FadeIn(t120), run_time=1.0)
        ans = Tex(R"P(B \mid A) = \frac{n(A \cap B)}{n(A)} = \frac{120}{640} = \frac{3}{16}").scale(0.95).set_color(WHITE).move_to([-1.6, -2.3, 0])
        self.play(Write(ans))
        self.play(FlashAround(ans, color=Y, buff=0.2), run_time=1.2)
        pick = note("answer ②", 28, WHITE).next_to(ans, RIGHT, buff=0.6)
        self.play(FadeIn(pick))
        self.wait(2)

# ─────────────────────────────────────────────────────────────
# 2. 독립 (2.6) — 슬라이드 46 (Definition 2.11) 앞
# ─────────────────────────────────────────────────────────────
class Independence(InteractiveScene):
    """같은 넓이 모형 두 개. 왼쪽은 Table 2.1: E 기둥과 U 기둥에서 M 조각의 높이가 다르다
    (460/600 과 40/300). 어느 기둥을 골라 늘리느냐에 따라 M 의 넓이가 바뀌므로 종속.
    오른쪽은 복원 카드(정의 2.11 의 보기): 첫 장이 에이스인 기둥과 아닌 기둥에서 둘째 장이 스페이드인
    조각의 높이가 13/52 로 같다. 가르는 선이 수평이면 조건이 넓이를 바꾸지 않는다. 그것이 독립이다."""
    SIDE = 2.8

    def square(self, x0, y0, wL, hL, hR, cols, colL, colR, top):
        W = self.SIDE
        S = region(x0, y0, W, W, GREY_B, 0.0, 2.5)
        L = region(x0, y0, wL, W, cols[0], 0.10)
        Rr = region(x0 + wL, y0, W - wL, W, cols[1], 0.10)
        aL = region(x0, y0, wL, hL, top, 0.35)
        aR = region(x0 + wL, y0, W - wL, hR, top, 0.35)
        tl = note(colL, 22, cols[0]).next_to(L, DOWN, buff=0.12)
        tr = note(colR, 22, cols[1]).next_to(Rr, DOWN, buff=0.12)
        return S, L, Rr, aL, aR, tl, tr

    def construct(self):
        head = slide_title("Independent Events")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        W = self.SIDE

        # ── 왼쪽: Table 2.1 — 기둥마다 M 의 높이가 다르다
        x0, y0 = -6.0, -0.3
        S1, L1, R1, aL1, aR1, tl1, tr1 = self.square(x0, y0, W * 600 / 900, W * 460 / 600, W * 40 / 300,
                                                     (CALM, MUTED), "E", "U", ACCENT)
        cap1 = note("Table 2.1", 24, GREY_A).next_to(S1, UP, buff=0.15)
        self.play(ShowCreation(S1), FadeIn(L1), FadeIn(R1), FadeIn(tl1), FadeIn(tr1), FadeIn(cap1))
        self.play(FadeIn(aL1), FadeIn(aR1))
        mE = Tex(R"P(M \mid E) = \frac{460}{600}").scale(0.65).set_color(ACCENT).move_to([x0 + W / 2, y0 - 0.9, 0])
        mU = Tex(R"P(M \mid U) = \frac{40}{300}").scale(0.65).set_color(ACCENT).next_to(mE, DOWN, buff=0.12)
        self.play(FadeIn(mE), FadeIn(mU))
        step = Line(aL1.get_corner(UR), aR1.get_corner(UL)).set_stroke(WARN, 4)
        dep = Tex(R"\ne \Rightarrow \text{dependent}").scale(0.7).set_color(WARN).next_to(mU, DOWN, buff=0.14)
        self.play(ShowCreation(step), FadeIn(dep))
        self.wait(1.2)

        # ── 오른쪽: 복원 카드 — 가르는 선이 수평이다
        x1 = 1.2
        wA = W * 4 / 52
        S2, L2, R2, aL2, aR2, tl2, tr2 = self.square(x1, y0, wA, W * 13 / 52, W * 13 / 52,
                                                     (ACCENT, MUTED), "A · ace", "not ace", CALM)
        cap2 = note("card replaced, then drawn again", 22, GREY_A).next_to(S2, UP, buff=0.15)
        self.play(ShowCreation(S2), FadeIn(L2), FadeIn(R2), FadeIn(tl2), FadeIn(tr2), FadeIn(cap2))
        self.play(FadeIn(aL2), FadeIn(aR2))
        bTag = Tex(R"B \text{ · spade}").scale(0.7).set_color(CALM).next_to(S2, RIGHT, buff=0.15).set_y(y0 + W * 13 / 104)
        flat = Line([x1, y0 + W * 13 / 52, 0], [x1 + W, y0 + W * 13 / 52, 0]).set_stroke(CALM, 4)
        self.play(FadeIn(bTag), ShowCreation(flat))
        eq = Tex(R"P(B \mid A) = \frac{13}{52} = P(B)").scale(0.65).set_color(CALM).move_to([x1 + W / 2, y0 - 0.9, 0])
        ind = Tex(R"\Rightarrow \text{independent}").scale(0.7).set_color(CALM).next_to(eq, DOWN, buff=0.12)
        self.play(FadeIn(eq), FadeIn(ind))
        self.wait(1.0)

        flat_note = note("flat cut: condition changes nothing", 20, GREY_B).next_to(ind, DOWN, buff=0.14)
        self.play(FadeIn(flat_note))
        defn = Tex(R"P(B \mid A) = P(B) \iff P(A \cap B) = P(A)\,P(B)").set_color(WHITE).scale(0.9)
        defn.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(defn, UP))
        self.play(FlashAround(defn, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)

# ─────────────────────────────────────────────────────────────
# 3. 곱셈법칙 (2.6) — 슬라이드 48 (Theorem 2.10–2.12) 앞
# ─────────────────────────────────────────────────────────────
class ProductRule(InteractiveScene):
    """정의를 뒤집으면 P(A ∩ B) = P(A) P(B | A). Table 2.1 을 나무로 그리면 가지의 확률을 따라
    곱한 것이 잎이다: (600/900)(460/600) = 460/900. 가운데 600 이 지워지는 것이 보인다.
    단계가 셋이면 가지를 하나 더 잇는다."""

    def construct(self):
        head = slide_title("The Product Rule")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        defn = Tex(R"P(B \mid A) = \frac{P(A \cap B)}{P(A)} \ \Rightarrow\ P(A \cap B) = P(A)\,P(B \mid A)").scale(0.9)
        defn.next_to(head[1], DOWN, buff=0.3)
        self.play(Write(defn))
        self.wait(0.8)

        # ── Table 2.1 의 나무: E / U, 그 안에서 M / W
        root = Dot(radius=0.09).set_color(GREY_A).move_to([-5.6, -0.5, 0])
        e = Dot(radius=0.08).set_color(CALM).move_to([-2.6, 0.6, 0])
        u = Dot(radius=0.08).set_color(MUTED).move_to([-2.6, -1.7, 0])
        em = Dot(radius=0.08).set_color(ACCENT).move_to([0.6, 1.2, 0])
        ew = Dot(radius=0.08).set_color(CALM).move_to([0.6, 0.0, 0])
        l_e = Line(root.get_center(), e.get_center()).set_stroke(CALM, 2.5)
        l_u = Line(root.get_center(), u.get_center()).set_stroke(MUTED, 2.5)
        l_em = Line(e.get_center(), em.get_center()).set_stroke(ACCENT, 2.5)
        l_ew = Line(e.get_center(), ew.get_center()).set_stroke(CALM, 2.5)
        t_e = Tex(R"P(E) = \frac{600}{900}").scale(0.75).set_color(CALM).next_to(l_e.get_center(), UP, buff=0.15)
        t_u = Tex(R"\frac{300}{900}").scale(0.75).set_color(MUTED).next_to(l_u.get_center(), DOWN, buff=0.15)
        t_em = Tex(R"P(M \mid E) = \frac{460}{600}").scale(0.75).set_color(ACCENT).next_to(l_em.get_center(), UP, buff=0.15)
        t_ew = Tex(R"\frac{140}{600}").scale(0.75).set_color(CALM).next_to(l_ew.get_center(), DOWN, buff=0.15)
        lab_e = Tex("E").scale(0.8).set_color(CALM).next_to(e, DOWN, buff=0.12)
        lab_u = Tex("U").scale(0.8).set_color(MUTED).next_to(u, DOWN, buff=0.12)
        lab_em = Tex(R"E \cap M").scale(0.8).set_color(ACCENT).next_to(em, RIGHT, buff=0.15)
        lab_ew = Tex(R"E \cap W").scale(0.8).set_color(CALM).next_to(ew, RIGHT, buff=0.15)
        self.play(FadeIn(root), ShowCreation(l_e), ShowCreation(l_u), FadeIn(e), FadeIn(u),
                  FadeIn(lab_e), FadeIn(lab_u), FadeIn(t_e), FadeIn(t_u), run_time=1.2)
        self.play(ShowCreation(l_em), ShowCreation(l_ew), FadeIn(em), FadeIn(ew),
                  FadeIn(lab_em), FadeIn(lab_ew), FadeIn(t_em), FadeIn(t_ew), run_time=1.2)
        self.wait(0.6)

        # ── 길을 따라 곱한다
        path = VGroup(l_e.copy(), l_em.copy()).set_stroke(MEAN_COLOR, 6)
        self.play(ShowCreation(path), run_time=1.0)
        prod = Tex(R"P(E \cap M) = \frac{600}{900} \times \frac{460}{600} = \frac{460}{900}",
                   t2c={R"\frac{600}{900}": CALM, R"\frac{460}{600}": ACCENT}).scale(0.9)
        prod.move_to([3.3, -1.0, 0])
        if prod.get_right()[0] > 6.9:
            prod.scale(0.85).move_to([3.1, -1.0, 0])
        self.play(TransformFromCopy(VGroup(t_e, t_em), prod), run_time=1.3)
        self.wait(1.2)

        # ── 세 단계면 가지를 하나 더 잇는다
        self.play(FadeOut(path), run_time=0.3)
        three = Tex(R"P(A_1 \cap A_2 \cap A_3) = P(A_1)\,P(A_2 \mid A_1)\,P(A_3 \mid A_1 \cap A_2)").scale(0.85)
        three.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(three, UP))
        self.play(FlashAround(three, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.36 — 퓨즈 20 개 중 불량 5, 비복원 2 개. 원본 49 뒤 (풀이 50 앞)
# ─────────────────────────────────────────────────────────────
class Example236Fuses(InteractiveScene):
    """첫 퓨즈가 불량이면 상자에는 19 개, 불량 4 개가 남는다. 둘째 확률의 분자·분모가 함께 준다."""

    def construct(self):
        head = slide_title("Example 2.36")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        kinds = ["D"] * 5 + ["N"] * 15
        chips = VGroup(*[letter_chip(k, 0.55, WARN if k == "D" else MUTED) for k in kinds])
        chips.arrange_in_grid(2, 10, buff=0.14).move_to([-2.2, 1.6, 0])
        box = panel(chips, MUTED, buff=0.2)
        self.play(LaggedStartMap(FadeIn, chips, lag_ratio=0.04), FadeIn(box), run_time=1.2)

        n_all = ValueTracker(20)
        n_def = ValueTracker(5)
        cnt_all = counter(n_all, color=GREY_A, size=48)
        cnt_def = counter(n_def, color=WARN, size=48)
        tag_all = note("fuses", 22, GREY_A)
        tag_def = note("defective", 22, WARN)
        col = VGroup(tag_all, cnt_all, tag_def, cnt_def).arrange(DOWN, buff=0.15).move_to([4.6, 1.6, 0])
        self.add(cnt_all, cnt_def)
        self.play(FadeIn(tag_all), FadeIn(tag_def))
        self.wait(0.5)

        slots = VGroup(*[RoundedRectangle(width=1.0, height=1.0, corner_radius=0.12).set_stroke(MUTED, 2.5)
                         for _ in range(2)]).arrange(RIGHT, buff=2.6).move_to([-3.2, -1.2, 0])
        slot_tags = VGroup(note("first", 22, MUTED).next_to(slots[0], UP, buff=0.12),
                           note("second", 22, MUTED).next_to(slots[1], UP, buff=0.12))
        self.play(ShowCreation(slots), FadeIn(slot_tags))

        # 첫 번째: 불량 5/20
        first = chips[2]
        mark = ring(first, WARN, buff=0.05)
        self.play(ShowCreation(mark))
        p1 = Tex(R"P(A) = \frac{5}{20}").scale(0.9).set_color(WARN).next_to(slots[0], DOWN, buff=0.3)
        self.play(FadeOut(mark), first.animate.move_to(slots[0]), FadeIn(p1),
                  n_all.animate.set_value(19), n_def.animate.set_value(4), run_time=1.0)
        self.wait(0.6)

        # 두 번째: 남은 19 개 중 불량 4
        second = chips[4]
        mark = ring(second, WARN, buff=0.05)
        self.play(ShowCreation(mark))
        p2 = Tex(R"P(B \mid A) = \frac{4}{19}").scale(0.9).set_color(WARN).next_to(slots[1], DOWN, buff=0.3)
        self.play(FadeOut(mark), second.animate.move_to(slots[1]), FadeIn(p2),
                  n_all.animate.set_value(18), n_def.animate.set_value(3), run_time=1.0)
        self.wait(0.6)

        answer = Tex(R"P(A \cap B) = \frac{5}{20} \times \frac{4}{19} = \frac{1}{19}").set_color(MEAN_COLOR).scale(1.0)
        answer.move_to([3.4, -1.4, 0])
        self.play(TransformFromCopy(VGroup(p1, p2), answer), run_time=1.3)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.38 — 소방차 0.98, 구급차 0.92, 독립. 원본 51 뒤 (풀이 52 앞)
# ─────────────────────────────────────────────────────────────
class Example238Emergency(InteractiveScene):
    """단위 정사각형 안의 0.98 × 0.92 직사각형. 독립이면 곱셈법칙의 조건부확률이 그냥 확률이 된다."""

    def construct(self):
        head = slide_title("Example 2.38")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        S = 4.4
        unit = Square(side_length=S).set_stroke(GREY_B, 2).move_to([-2.4, -0.3, 0])
        one_x = Tex("1").scale(0.8).set_color(GREY_A).next_to(unit.get_corner(DR), DOWN, buff=0.15)
        one_y = Tex("1").scale(0.8).set_color(GREY_A).next_to(unit.get_corner(UL), LEFT, buff=0.15)
        self.play(ShowCreation(unit), FadeIn(one_x), FadeIn(one_y))

        a = Rectangle(width=S * 0.98, height=S).set_stroke(width=0).set_fill(ACCENT, 0.25)
        a.align_to(unit, DL)
        ta = Tex(R"P(A) = 0.98").scale(0.85).set_color(ACCENT).next_to(unit, DOWN, buff=0.45)
        self.play(FadeIn(a), Write(ta))
        self.wait(0.4)
        b = Rectangle(width=S, height=S * 0.92).set_stroke(width=0).set_fill(CALM, 0.25)
        b.align_to(unit, DL)
        tb = Tex(R"P(B) = 0.92").scale(0.85).set_color(CALM).next_to(unit, LEFT, buff=0.45).rotate(PI / 2)
        self.play(FadeIn(b), Write(tb))
        self.wait(0.4)

        both = Rectangle(width=S * 0.98, height=S * 0.92).set_stroke(MEAN_COLOR, 3).set_fill(MEAN_COLOR, 0.15)
        both.align_to(unit, DL)
        tag = Tex(R"A \cap B").scale(0.9).set_color(MEAN_COLOR).move_to(both)
        self.play(ShowCreation(both), FadeIn(tag))
        indep = note("independent", 26, GREY_B).move_to([3.6, 1.6, 0])
        rule = Tex(R"P(A \cap B) = P(A)\,P(B \mid A) = P(A)\,P(B)").scale(0.85).next_to(indep, DOWN, buff=0.35)
        if rule.get_right()[0] > 6.9:
            rule.scale(0.85).next_to(indep, DOWN, buff=0.35)
        self.play(FadeIn(indep), Write(rule))
        self.wait(0.6)
        answer = Tex(R"0.98 \times 0.92 = 0.9016").set_color(MEAN_COLOR).scale(1.1).next_to(rule, DOWN, buff=0.6)
        self.play(TransformFromCopy(VGroup(ta, tb), answer), run_time=1.2)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 전확률 정리 (2.7) — 슬라이드 53 (Theorem 2.13) 앞
# ─────────────────────────────────────────────────────────────
class TotalProbability(InteractiveScene):
    """S 를 세로 띠 B₁, B₂, B₃ 으로 가른다(폭 = P(Bᵢ)). 띠마다 A 인 부분의 높이가 P(A | Bᵢ) 다.
    A 의 넓이는 띠별 넓이의 합 — 그것이 Σ P(Bᵢ) P(A | Bᵢ). 참고: legacy area_model_bayes."""
    widths = [0.5, 0.3, 0.2]                 # P(B_i). 숫자는 화면에 적지 않는다(보기용 비율)
    heights = [0.55, 0.25, 0.8]              # P(A | B_i)

    def construct(self):
        head = slide_title("Total Probability")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        W, H = 7.0, 3.4
        origin = np.array([-5.4, -1.75, 0])
        S = Rectangle(width=W, height=H).set_stroke(GREY_B, 2).move_to(origin + np.array([W / 2, H / 2, 0]))
        s_tag = Tex("S").set_color(GREY_A).next_to(S.get_corner(UL), UR, buff=0.1)
        self.play(ShowCreation(S), FadeIn(s_tag))

        colors = [ACCENT, CALM, MED_COLOR]
        strips, labels, x = VGroup(), VGroup(), 0.0
        for w, col, i in zip(self.widths, colors, range(3)):
            r = Rectangle(width=W * w, height=H).set_stroke(col, 2).set_fill(col, 0.08)
            r.move_to(origin + np.array([x + W * w / 2, H / 2, 0]))
            t = Tex(f"B_{i + 1}").set_color(col).scale(0.9).next_to(r, DOWN, buff=0.15)
            p = Tex(f"P(B_{i + 1})").set_color(col).scale(0.7).next_to(t, DOWN, buff=0.1)
            strips.add(r); labels.add(t, p); x += W * w
        self.play(LaggedStartMap(FadeIn, strips, lag_ratio=0.2), FadeIn(labels))
        part = note("partition of S", 24, GREY_B).move_to([3.9, 2.5, 0])
        self.play(FadeIn(part))
        self.wait(0.6)

        # A: 띠마다 높이가 다르다
        pieces, htex, x = VGroup(), VGroup(), 0.0
        for w, h, col, i in zip(self.widths, self.heights, colors, range(3)):
            r = Rectangle(width=W * w, height=H * h).set_stroke(width=0).set_fill(WARN, 0.45)
            r.move_to(origin + np.array([x + W * w / 2, H * h / 2, 0]))
            t = Tex(f"P(A \\mid B_{i + 1})").set_color(WARN).scale(0.65).move_to(r)
            pieces.add(r); htex.add(t); x += W * w
        a_tag = Tex("A").set_color(WARN).scale(1.0).next_to(S, RIGHT, buff=0.35).set_y(origin[1] + 0.9)
        self.play(LaggedStart(*[GrowFromEdge(pc, DOWN) for pc in pieces], lag_ratio=0.2), FadeIn(a_tag), run_time=1.4)
        self.play(FadeIn(htex))
        self.wait(0.8)

        # 넓이 = 폭 × 높이 를 더한다
        terms = VGroup(*[Tex(f"P(B_{i + 1})\\,P(A \\mid B_{i + 1})").scale(0.8).set_color(c)
                         for i, c in enumerate(colors)])
        plus = VGroup(Tex("P(A) ="), terms[0], Tex("+"), terms[1], Tex("+"), terms[2]).arrange(RIGHT, buff=0.18)
        plus.scale(min(1.0, 12.5 / plus.get_width())).to_edge(DOWN, buff=0.45)
        self.play(Write(plus[0]))
        for k, (piece, term) in enumerate(zip(pieces, terms)):
            anims = [TransformFromCopy(piece, term)]
            if k > 0:
                anims.append(FadeIn(plus[2 * k]))
            self.play(*anims, run_time=0.9)
        self.wait(0.8)
        general = Tex(R"P(A) = \sum_{i=1}^{k} P(B_i)\,P(A \mid B_i)").set_color(WHITE).scale(1.0)
        general.move_to([3.9, 1.2, 0])
        self.play(FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.41 — 기계 셋, 불량률. 원본 54 뒤 (풀이 55 앞)
# ─────────────────────────────────────────────────────────────
class Example241Machines(InteractiveScene):
    """세 갈래 나무. 갈래마다 (기계일 확률) × (그 기계의 불량률) 을 잎에 적고 더한다."""

    def construct(self):
        head = slide_title("Example 2.41")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        root, mids, leaves, lines, mid_tex, leaf_tex = tree3(
            ["0.30", "0.45", "0.25"], [R"P(A \mid B_1) = 0.02", R"P(A \mid B_2) = 0.03", R"P(A \mid B_3) = 0.02"],
            ["B_1", "B_2", "B_3"], [ACCENT, CALM, MED_COLOR])
        self.play(FadeIn(root), LaggedStartMap(ShowCreation, VGroup(lines[0], lines[2], lines[4]), lag_ratio=0.2),
                  FadeIn(mids), FadeIn(mid_tex), run_time=1.2)
        self.play(LaggedStartMap(ShowCreation, VGroup(lines[1], lines[3], lines[5]), lag_ratio=0.2),
                  FadeIn(leaves), FadeIn(leaf_tex), run_time=1.2)
        a_tag = Tex(R"A = \text{defective}").scale(0.8).set_color(WARN).next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.7)
        self.play(FadeIn(a_tag))
        self.wait(0.5)

        prods = ["0.30 \\times 0.02 = 0.006", "0.45 \\times 0.03 = 0.0135", "0.25 \\times 0.02 = 0.005"]
        ptex = VGroup()
        for lf, txt, col in zip(leaves, prods, [ACCENT, CALM, MED_COLOR]):
            t = Tex(txt).scale(0.8).set_color(col).next_to(lf, RIGHT, buff=0.35)
            ptex.add(t)
        for lf, t, l1, l2 in zip(leaves, ptex, lines[0::2], lines[1::2]):
            path = VGroup(l1.copy(), l2.copy()).set_stroke(MEAN_COLOR, 6)
            self.play(ShowCreation(path), run_time=0.6)
            self.play(FadeIn(t), FadeOut(path), run_time=0.6)
        self.wait(0.6)

        total = Tex(R"P(A) = 0.006 + 0.0135 + 0.005 = 0.0245").set_color(MEAN_COLOR).scale(1.0)
        total.to_edge(DOWN, buff=0.6)
        self.play(TransformFromCopy(ptex, total), run_time=1.3)
        self.play(FlashAround(total, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 베이즈 정리 (2.7) — 슬라이드 56 (Theorem 2.14) 앞
# ─────────────────────────────────────────────────────────────
class BayesRule(InteractiveScene):
    """전확률의 세 조각을 한 줄로 이어 붙이면 P(A) 다. 그중 한 조각이 차지하는 비율이
    P(B_r | A). 원인 → 결과(P(A | B_r))를 결과 → 원인(P(B_r | A))으로 뒤집는다."""
    widths = [0.5, 0.3, 0.2]
    heights = [0.55, 0.25, 0.8]

    def construct(self):
        head = slide_title("Bayes' Rule")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        colors = [ACCENT, CALM, MED_COLOR]
        areas = [w * h for w, h in zip(self.widths, self.heights)]
        total = sum(areas)
        W = 10.0
        pieces, ptex, x = VGroup(), VGroup(), -W / 2
        for a, col, i in zip(areas, colors, range(3)):
            r = Rectangle(width=W * a / total, height=1.0).set_stroke(WHITE, 1.5).set_fill(col, 0.5)
            r.move_to([x + W * a / total / 2, 1.2, 0])
            t = Tex(f"P(B_{i + 1})\\,P(A \\mid B_{i + 1})").scale(0.65).set_color(col)
            t.next_to(r, DOWN, buff=0.15 + (0.5 if i == 1 else 0.0))
            pieces.add(r); ptex.add(t); x += W * a / total
        brace = Brace(pieces, UP)
        pa = Tex("P(A)").set_color(WARN).next_to(brace, UP, buff=0.12)
        self.play(LaggedStartMap(FadeIn, pieces, lag_ratio=0.2), FadeIn(ptex))
        self.play(GrowFromCenter(brace), FadeIn(pa))
        self.wait(0.8)

        # 조각 하나의 비율
        r = 2
        self.play(pieces[0].animate.set_fill(ACCENT, 0.15), pieces[1].animate.set_fill(CALM, 0.15),
                  ptex[0].animate.set_opacity(0.3), ptex[1].animate.set_opacity(0.3),
                  pieces[2].animate.set_fill(MED_COLOR, 0.8), run_time=0.8)
        given = Tex(R"\text{given } A").set_color(WARN).scale(0.9).move_to([0, -0.8, 0])
        self.play(FadeIn(given))
        ratio = Tex(R"P(B_3 \mid A) = \frac{P(B_3)\,P(A \mid B_3)}{P(A)}",
                    t2c={"P(A)": WARN}).scale(0.95).move_to([0, -1.85, 0])
        self.play(TransformFromCopy(VGroup(ptex[2], pa), ratio), run_time=1.3)
        self.wait(1.0)
        general = Tex(R"P(B_r \mid A) = \frac{P(B_r)\,P(A \mid B_r)}{\sum_i P(B_i)\,P(A \mid B_i)}").set_color(WHITE).scale(0.9)
        general.move_to([0, -3.15, 0])
        self.play(FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.42 — 불량품이 B₃ 에서 왔을 확률. 원본 57 뒤 (풀이 58 앞)
# ─────────────────────────────────────────────────────────────
class Example242Bayes(InteractiveScene):
    """Example 2.41 의 세 잎 0.006, 0.0135, 0.005 를 이어 붙이면 0.0245. B₃ 조각의 비율이 답이다."""

    def construct(self):
        head = slide_title("Example 2.42")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        vals = [0.006, 0.0135, 0.005]
        names = ["B_1", "B_2", "B_3"]
        colors = [ACCENT, CALM, MED_COLOR]
        total = sum(vals)
        W = 10.0
        pieces, ptex, x = VGroup(), VGroup(), -W / 2
        for v, nm, col in zip(vals, names, colors):
            r = Rectangle(width=W * v / total, height=1.0).set_stroke(WHITE, 1.5).set_fill(col, 0.5)
            r.move_to([x + W * v / total / 2, 1.4, 0])
            t = Tex(f"{v}").scale(0.8).set_color(col).move_to(r)
            n = Tex(nm).scale(0.8).set_color(col).next_to(r, DOWN, buff=0.15)
            pieces.add(r); ptex.add(t, n); x += W * v / total
        brace = Brace(pieces, UP)
        pa = Tex(R"P(A) = 0.0245").set_color(WARN).scale(0.9).next_to(brace, UP, buff=0.12)
        self.play(LaggedStartMap(FadeIn, pieces, lag_ratio=0.2), FadeIn(ptex))
        self.play(GrowFromCenter(brace), FadeIn(pa))
        self.wait(0.8)

        self.play(pieces[0].animate.set_fill(ACCENT, 0.15), pieces[1].animate.set_fill(CALM, 0.15),
                  pieces[2].animate.set_fill(MED_COLOR, 0.85), run_time=0.8)
        given = Tex(R"\text{given } A").set_color(WARN).scale(0.9).move_to([0, -0.4, 0])
        self.play(FadeIn(given))
        answer = Tex(R"P(B_3 \mid A) = \frac{0.005}{0.0245} \approx 0.204",
                     t2c={"0.005": MED_COLOR, "0.0245": WARN}).scale(1.05).move_to([0, -1.6, 0])
        self.play(TransformFromCopy(VGroup(ptex[4], pa), answer), run_time=1.3)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(0.6)
        others = Tex(R"P(B_1 \mid A) \approx 0.245, \quad P(B_2 \mid A) \approx 0.551").scale(0.85).set_color(GREY_B)
        others.next_to(answer, DOWN, buff=0.6)
        self.play(FadeIn(others))
        self.wait(2)
