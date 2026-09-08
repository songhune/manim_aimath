"""확률과통계 「확률」 장 (Walpole Chapter 2) 2.6–2.8 — 조건부확률 · 독립 · 곱셈법칙 · 전확률 · 베이즈.

강의 교안 `확률과통계/교육메모/03주차.md` 의 시각화 보조자료. 도구와 규칙은 week02.py 와 같다.
개념 영상은 개념 슬라이드 바로 앞, 예제 영상은 문제 슬라이드 다음·풀이 슬라이드 앞이다(하네스 3.6).
소재는 교재가 정의 옆에 둔 보기(Table 2.1 의 900 명, 정의 2.11 의 주사위와 카드)와 수업에서 다루는
예제(2.34, 2.36, 2.38, 2.41, 2.42)로 한정한다.

덱 삽입 자리 (원본 PS1_02_restyled.pptx 기준):
    ConditionalProbability   42 앞   Definition 2.10 (Table 2.1 로 보인다)
    Example234Flights        44 뒤   Ex 2.34
    Independence             46 앞   Definition 2.11 (찌그러진 주사위 → 종속, 복원 카드 → 독립)
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
    label, note, panel, ring, slide_title, swap, counter, freeze, bar,
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
# 1. 조건부확률 (2.6) — 슬라이드 42 (Definition 2.10) 앞
# ─────────────────────────────────────────────────────────────
class ConditionalProbability(InteractiveScene):
    """Table 2.1 의 900 명. '고용된 사람이 뽑혔다' 는 조건이 붙으면 표본공간이 900 에서 600 으로
    갈아 끼워진다. 그 안에서 남자 460 을 세면 P(M | E) = 460/600. 분모가 P(E) 인 이유가
    표에서 바로 보인다."""

    def construct(self):
        head = slide_title("Conditional Probability")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        table, cells = table21()
        table.move_to([-2.2, 0.2, 0])
        self.play(FadeIn(table, lag_ratio=0.02), run_time=1.4)
        s_tag = Tex("n(S) = 900").set_color(GREY_A).scale(0.9).move_to([4.2, 2.3, 0])
        self.play(FadeIn(s_tag))
        self.wait(0.6)

        # ── 조건 E: 고용 열만 남는다
        given = Tex(R"\text{given } E").set_color(CALM).scale(0.95).move_to([4.2, 1.4, 0])
        col_e = VGroup(cells[("M", "E")], cells[("W", "E")], cells[("Total", "E")])
        others = VGroup(*[v for k, v in cells.items() if k[1] != "E"])
        box_e = SurroundingRectangle(col_e, buff=0.05).set_stroke(CALM, 3)
        self.play(FadeIn(given), others.animate.set_opacity(0.2), ShowCreation(box_e))
        new_s = Tex("n(E) = 600").set_color(CALM).scale(0.9).next_to(given, DOWN, buff=0.35)
        self.play(FadeIn(new_s))
        self.wait(0.6)

        # ── 그 안에서 남자 460
        me = ring(cells[("M", "E")], ACCENT, buff=0.04)
        n_me = Tex(R"n(E \cap M) = 460").set_color(ACCENT).scale(0.9).next_to(new_s, DOWN, buff=0.35)
        self.play(ShowCreation(me), FadeIn(n_me))
        self.wait(0.5)
        ratio = Tex(R"P(M \mid E) = \frac{460}{600}").set_color(WHITE).scale(1.0)
        ratio.next_to(n_me, DOWN, buff=0.6).set_x(4.2)
        self.play(TransformFromCopy(VGroup(n_me, new_s), ratio), run_time=1.2)
        self.wait(1.0)

        # ── 900 으로 나눠도 같다: 정의
        self.play(FadeOut(table), FadeOut(box_e), FadeOut(me), FadeOut(s_tag), run_time=0.5)
        defn = Tex(R"P(M \mid E) = \frac{460/900}{600/900} = \frac{P(E \cap M)}{P(E)}",
                   t2c={"P(E)": CALM, R"P(E \cap M)": ACCENT}).scale(1.0)
        defn.move_to([-2.2, 0.8, 0])
        self.play(Write(defn))
        self.wait(0.8)
        general = Tex(R"P(B \mid A) = \frac{P(A \cap B)}{P(A)}, \quad P(A) > 0").set_color(WHITE).scale(1.15)
        general.move_to([-2.2, -1.4, 0])
        self.play(FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.34 — 정시 출발·정시 도착. 원본 44 뒤 (풀이 45 앞)
# ─────────────────────────────────────────────────────────────
class Example234Flights(InteractiveScene):
    """벤 다이어그램에 0.05 · 0.78 · 0.04 를 적는다. 조건이 D 면 D 안(0.83)만 세계가 되고,
    조건이 A 면 A 안(0.82)만 세계가 된다. 같은 0.78 을 다른 것으로 나눈다."""

    def construct(self):
        head = slide_title("Example 2.34")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        given = Tex(R"P(D) = 0.83, \quad P(A) = 0.82, \quad P(D \cap A) = 0.78",
                    t2c={"P(D)": ACCENT, "P(A)": CALM, R"P(D \cap A)": MEAN_COLOR}).scale(0.85)
        given.next_to(head[1], DOWN, buff=0.3)
        self.play(FadeIn(given, UP))

        cD = Circle(radius=1.6).move_to(LEFT * 3.0 + DOWN * 0.3).set_stroke(ACCENT, 3)
        cA = Circle(radius=1.6).move_to(LEFT * 1.0 + DOWN * 0.3).set_stroke(CALM, 3)
        only_d = Difference(cD, cA).set_stroke(width=0).set_fill(ACCENT, 0.3)
        lens = Intersection(cD, cA).set_stroke(width=0).set_fill(MEAN_COLOR, 0.45)
        only_a = Difference(cA, cD).set_stroke(width=0).set_fill(CALM, 0.3)
        tD = Tex("D").set_color(ACCENT).next_to(cD, UP, buff=0.1).shift(LEFT * 0.8)
        tA = Tex("A").set_color(CALM).next_to(cA, UP, buff=0.1).shift(RIGHT * 0.8)
        nums = VGroup(Tex("0.05").move_to(cD.get_center() + LEFT * 0.85),
                      Tex("0.78").move_to((cD.get_center() + cA.get_center()) / 2),
                      Tex("0.04").move_to(cA.get_center() + RIGHT * 0.85)).set_color(WHITE)
        for n in nums:
            n.scale(0.9)
        self.play(ShowCreation(cD), FadeIn(tD), ShowCreation(cA), FadeIn(tA))
        self.play(FadeIn(only_d), FadeIn(lens), FadeIn(only_a), FadeIn(nums))
        self.wait(0.8)

        # (a) D 가 세계
        qa = Tex(R"\text{(a)}\ P(A \mid D) = \frac{0.78}{0.83} \approx 0.94",
                 t2c={"0.83": ACCENT, "0.78": MEAN_COLOR}).scale(0.95).move_to([3.6, 0.8, 0])
        self.play(only_a.animate.set_fill(CALM, 0.06), cA.animate.set_stroke(CALM, 1),
                  nums[2].animate.set_opacity(0.25), run_time=0.8)
        self.play(FlashAround(cD, color=ACCENT, buff=0.05), Write(qa), run_time=1.4)
        self.wait(1.2)

        # (b) A 가 세계
        self.play(only_a.animate.set_fill(CALM, 0.3), cA.animate.set_stroke(CALM, 3), nums[2].animate.set_opacity(1),
                  only_d.animate.set_fill(ACCENT, 0.06), cD.animate.set_stroke(ACCENT, 1),
                  nums[0].animate.set_opacity(0.25), run_time=0.8)
        qb = Tex(R"\text{(b)}\ P(D \mid A) = \frac{0.78}{0.82} \approx 0.95",
                 t2c={"0.82": CALM, "0.78": MEAN_COLOR}).scale(0.95).next_to(qa, DOWN, buff=0.7).align_to(qa, LEFT)
        self.play(FlashAround(cA, color=CALM, buff=0.05), Write(qb), run_time=1.4)
        self.wait(0.6)
        same = note("same numerator, different world", 24, GREY_B).next_to(qb, DOWN, buff=0.4).align_to(qb, LEFT)
        self.play(FadeIn(same))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 독립 (2.6) — 슬라이드 46 (Definition 2.11) 앞
# ─────────────────────────────────────────────────────────────
class Independence(InteractiveScene):
    """정의 2.11 옆의 두 보기. 찌그러진 주사위(Example 2.25 의 w, 2w)에서 A = {4,5,6}, B = {1,4}:
    P(B | A) = 2/5 인데 P(B) = 1/3 이라 종속. 카드를 뽑아 되돌려 놓고 다시 뽑으면 둘째 뽑기가
    보는 카드는 언제나 52 장이라 P(B | A) = P(B) = 1/4, 독립."""

    def construct(self):
        head = slide_title("Independent Events")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 주사위: 종속
        faces = VGroup(*[die_face(i + 1, 0.55, GREY_A) for i in range(6)]).arrange(RIGHT, buff=0.4)
        faces.move_to([-3.4, 1.75, 0])
        wts = VGroup(*[Tex("2w" if (i + 1) % 2 == 0 else "w").scale(0.7).set_color(GREY_B).next_to(f, DOWN, buff=0.12)
                       for i, f in enumerate(faces)])
        self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.08), FadeIn(wts))
        setup = Tex(R"A = \{4, 5, 6\}, \quad B = \{1, 4\}", t2c={"A": ACCENT, "B": CALM}).scale(0.8)
        setup.next_to(faces, UP, buff=0.3)
        self.play(FadeIn(setup))
        pb = Tex(R"P(B) = \frac{w + 2w}{9w} = \frac{1}{3}").scale(0.85).set_color(CALM).move_to([2.2, 2.3, 0]).align_to([-0.2, 0, 0], LEFT)
        ringB = VGroup(ring(faces[0], CALM, buff=0.06), ring(faces[3], CALM, buff=0.06))
        self.play(ShowCreation(ringB), Write(pb))
        self.wait(0.5)
        boxA = SurroundingRectangle(VGroup(faces[3], faces[4], faces[5], wts[3], wts[5]), buff=0.12).set_stroke(ACCENT, 3)
        pba = Tex(R"P(B \mid A) = \frac{2w}{2w + w + 2w} = \frac{2}{5}").scale(0.85).set_color(ACCENT)
        pba.next_to(pb, DOWN, buff=0.35).align_to(pb, LEFT)
        self.play(ShowCreation(boxA), *[f.animate.set_opacity(0.25) for f in faces[:3]],
                  *[w.animate.set_opacity(0.25) for w in wts[:3]], Write(pba))
        dep = Tex(R"\frac{2}{5} \ne \frac{1}{3}").scale(0.9).set_color(WARN).next_to(pba, DOWN, buff=0.3).align_to(pb, LEFT)
        dep_tag = note("dependent", 26, WARN).next_to(dep, RIGHT, buff=0.5)
        self.play(FadeIn(dep), FadeIn(dep_tag))
        self.wait(1.4)

        # ── 카드: 복원하면 독립
        self.play(*[FadeOut(m) for m in [faces, wts, setup, pb, pba, ringB, boxA, dep, dep_tag]], run_time=0.5)
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suits = [("s", CALM), ("h", MUTED), ("d", MUTED), ("c", MUTED)]          # 스페이드만 색을 준다
        deck = VGroup()
        for si, (sn, col) in enumerate(suits):
            for rk in ranks:
                c = letter_chip(rk, 0.4, col if rk != "A" else ACCENT)
                if sn == "s" and rk == "A":
                    c = letter_chip(rk, 0.4, ACCENT)
                deck.add(c)
        deck.arrange_in_grid(4, 13, buff=0.07).move_to([-1.6, 0.9, 0])
        box = panel(deck, MUTED, buff=0.18)
        spade_tag = note("spades", 22, CALM).next_to(deck[:13], LEFT, buff=0.3)
        self.play(LaggedStartMap(FadeIn, deck, lag_ratio=0.01), FadeIn(box), FadeIn(spade_tag), run_time=1.4)
        setup2 = Tex(R"A = \text{first card ace}, \quad B = \text{second card spade}",
                     t2c={"A": ACCENT, "B": CALM}).scale(0.75)
        setup2.next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(setup2))

        # 첫 장: 에이스 하나를 뽑았다가 되돌린다
        ace = deck[13]                                   # 하트 에이스
        pick = ring(ace, ACCENT, buff=0.04)
        out = ace.copy()
        self.play(ShowCreation(pick))
        self.play(out.animate.shift(DOWN * 1.9 + RIGHT * 2.0), run_time=0.8)
        back = note("replaced", 22, ACCENT).next_to(out, RIGHT, buff=0.25)
        self.play(FadeIn(back))
        self.play(out.animate.move_to(ace), run_time=0.8)
        self.remove(out)
        self.play(FadeOut(pick), FadeOut(back), run_time=0.3)

        # 둘째 장이 보는 것은 여전히 52 장, 스페이드 13 장
        sp = SurroundingRectangle(deck[:13], buff=0.05).set_stroke(CALM, 3)
        pb2 = Tex(R"P(B \mid A) = \frac{13}{52} = P(B)").scale(0.95).set_color(WHITE).move_to([4.3, 0.9, 0])
        self.play(ShowCreation(sp), Write(pb2))
        ind = note("independent", 26, CALM).next_to(pb2, DOWN, buff=0.3)
        self.play(FadeIn(ind))
        self.wait(0.8)
        defn = Tex(R"P(B \mid A) = P(B) \iff P(A \cap B) = P(A)\,P(B)").set_color(WHITE).scale(1.0)
        defn.to_edge(DOWN, buff=0.55)
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
