"""확률과통계 「확률」 장 (Walpole Chapter 2) — 표본공간 · 사건 · 셈의 규칙 · 사건의 확률 · 덧셈법칙.

강의 교안 `확률과통계/교육메모/02주차.md` 의 시각화 보조자료.

영상은 개념 슬라이드 **바로 앞** 에 놓는 개요다(하네스 3.6). 소재는 교재가 정의 옆에 둔
보기 — Example 2.1 의 동전·주사위, 2.3절 본문의 글자 a, b, c, d — 로 한정하고, 번호가 붙은
예제(2.13, 2.15, 2.22, 2.33 …)는 슬라이드가 푼다. 영상이 예제의 답을 먼저 보이지 않는다.
(2026-09-08 개편. 그전 판은 예제 슬라이드 뒤에 붙는 풀이 영상이었고 동전 5회·치토 4명처럼
교재에 없는 소재를 썼다. `week02.py.bak` 에 남겨 두었다.)

덱 삽입 자리 (원본 PS1_02_restyled.pptx 기준, 영상은 그 슬라이드 앞. insert_videos.py 의 anchors):
    SampleSpace           4   Definition 2.1 · Example 2.1
    EventsAndSetOps       8   Definition 2.2–2.6
    MultiplicationRule   12   Rule 2.1 · 2.2
    Permutations         17   Definition 2.7 · Theorem 2.1 · 2.2
    Combinations         18   Theorem 2.6
    ProbabilityOfEvent   27   Definition 2.9 · Rule 2.3
    AdditionRule         35   Theorem 2.7 · 2.9

예제 영상은 문제 슬라이드 다음, 풀이 슬라이드 앞에 놓는다 (2026-09-08 추가. 사용자 요청):
    Example213Dice          13 뒤   Example215Club · Example217EvenNumbers   15 뒤
    Example218Awards        19 뒤   Example222Cartridges                     25 뒤
    Example225LoadedDie     28 뒤   Example228Poker                          32 뒤
    Example229Jobs          36 뒤   Example233Cable                          40 뒤

참고: legacy/_2018/eop/combinations.py 의 HowToComputeNChooseK — 빈 자리에 이름을 얹어
5·4·3 을 세고, 뽑힌 셋의 순열 3! 로 나눈다. Permutations 와 Combinations 가 그 순서를 따른다.
legacy/_2018/eop/chapter2/permutation_grid.py 는 격자 배치만 참고했다.

화면 문구는 이름과 식뿐이다. 설명은 교안 대본에 있다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/probstat/week02.py
    ./render.sh check _2026/probstat/week02.py            # 전 씬 빠른 점검
    ./render.sh ppt   _2026/probstat/week02.py SampleSpace   # PPT 삽입용 재인코딩
    ./render.sh gif   _2026/probstat/week02.py SampleSpace   # Notability 용
"""
from manim_imports_ext import *

import itertools as _it

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MED_COLOR, MUTED, WARN, BODY_FONT,
    chito, crowd, label, note, panel, ring, slide_title, swap, counter, freeze, bar,
)


# ─────────────────────────────────────────────────────────────
# 실험 도구 — 동전과 주사위. 결과를 글자로 적는 대신 물건으로 보인다.
# ─────────────────────────────────────────────────────────────
PIPS = {
    1: [(0, 0)],
    2: [(-.42, .42), (.42, -.42)],
    3: [(-.42, .42), (0, 0), (.42, -.42)],
    4: [(-.42, .42), (.42, .42), (-.42, -.42), (.42, -.42)],
    5: [(-.42, .42), (.42, .42), (0, 0), (-.42, -.42), (.42, -.42)],
    6: [(-.42, .45), (-.42, 0), (-.42, -.45), (.42, .45), (.42, 0), (.42, -.45)],
}


def die_face(n, size=0.62, color=CALM):
    """주사위 한 면. 눈을 점으로 찍는다."""
    body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18)
    body.set_stroke(color, 2).set_fill(BLACK, 1)
    pips = VGroup(*[
        Dot(radius=size * 0.085).set_fill(color, 1).move_to(
            body.get_center() + np.array([x, y, 0]) * size * 0.5
        )
        for x, y in PIPS[n]
    ])
    return VGroup(body, pips)


def die_blank(size=0.62, color=MUTED):
    """아직 던지지 않은 주사위. 눈 대신 물음표."""
    body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18)
    body.set_stroke(color, 2).set_fill(BLACK, 1)
    q = Text("?", font=BODY_FONT, font_size=int(size * 46)).set_color(color).move_to(body)
    return VGroup(body, q)


def coin(letter, size=0.56, color=ACCENT):
    """동전 한 닢. 앞면 H, 뒷면 T."""
    disc = Circle(radius=size / 2).set_stroke(color, 2.5).set_fill(BLACK, 1)
    txt = Text(letter, font=BODY_FONT, font_size=int(size * 46)).set_color(color)
    txt.move_to(disc)
    return VGroup(disc, txt)


def letter_chip(ch, size=0.72, color=INK):
    """글자 카드 한 장. 글자가 아니라 물건으로 다루려고 테두리를 두른다."""
    body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18)
    body.set_stroke(color, 2).set_fill(BLACK, 1)
    txt = Text(str(ch), font=BODY_FONT, font_size=int(size * 50)).set_color(color)
    txt.move_to(body)
    return VGroup(body, txt)


def branch(a, b, color, trim=0.55):
    """두 물건 사이를 잇는 가지. 물건에 닿지 않게 양끝을 자른다."""
    v = b.get_center() - a.get_center()
    ln = Line(a.get_center(), b.get_center(), stroke_color=color, stroke_width=3)
    return ln.set_length(get_norm(v) - trim)


def slot(size=0.95, color=MUTED):
    return RoundedRectangle(width=size, height=size, corner_radius=0.12).set_stroke(color, 2.5)


# ─────────────────────────────────────────────────────────────
# 1. 표본공간 (2.1) — 슬라이드 4 (Definition 2.1, Example 2.1) 앞
# ─────────────────────────────────────────────────────────────
class SampleSpace(InteractiveScene):
    """Example 2.1 의 보기 그대로다. 동전 한 번 → {H, T}. 주사위 한 번 → {1,…,6}.
    같은 주사위인데 짝·홀만 보면 {even, odd}. 실험이 같아도 무엇을 보느냐에 따라
    표본공간이 달라진다는 것을 여섯 면이 두 무리로 갈라지는 것으로 보인다.
    끝에 동전 두 번의 나무그림을 그려 가지 끝이 표본점이 되는 것을 보인다
    (판서 계획의 세 보기: 동전 1회, 주사위 1회, 동전 2회).
    """

    def construct(self):
        head = slide_title("Sample Space")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        LX, RX = -3.4, 2.9
        Y = [1.75, 0.15, -1.55]

        # ── 동전 한 번
        c0 = coin("?", 0.8, MUTED).move_to([LX, Y[0], 0])
        self.play(FadeIn(c0, scale=0.6))
        coins = VGroup(coin("H", 0.7), coin("T", 0.7)).arrange(RIGHT, buff=0.45)
        coins.move_to([LX, Y[0], 0])
        self.play(FadeOut(c0, scale=0.6), FadeIn(coins, lag_ratio=0.3), run_time=0.8)
        s0 = Tex(R"S = \{H,\ T\}").set_color(WHITE).move_to([RX, Y[0], 0])
        self.play(TransformFromCopy(coins, s0), run_time=1.0)
        self.wait(0.5)

        # ── 주사위 한 번
        d0 = die_blank(0.8).move_to([LX, Y[1], 0])
        self.play(FadeIn(d0, scale=0.6))
        dice = VGroup(*[die_face(i + 1, 0.56, CALM) for i in range(6)])
        dice.arrange(RIGHT, buff=0.22).move_to([LX, Y[1], 0])
        self.play(FadeOut(d0, scale=0.6), FadeIn(dice, lag_ratio=0.12), run_time=0.9)
        s1 = Tex(R"S_1 = \{1, 2, 3, 4, 5, 6\}").set_color(WHITE).move_to([RX, Y[1], 0])
        self.play(TransformFromCopy(dice, s1), run_time=1.0)
        self.wait(0.5)

        # ── 같은 주사위, 짝·홀만 본다: 여섯 면이 두 무리로 갈라진다
        again = dice.copy()
        self.play(again.animate.shift(DOWN * (Y[1] - Y[2])), run_time=0.8)
        even = VGroup(*[again[i] for i in (1, 3, 5)])
        odd = VGroup(*[again[i] for i in (0, 2, 4)])
        even.generate_target()
        even.target.arrange(RIGHT, buff=0.12).move_to([LX - 1.25, Y[2], 0])
        odd.generate_target()
        odd.target.arrange(RIGHT, buff=0.12).move_to([LX + 1.25, Y[2], 0])
        self.play(MoveToTarget(even), MoveToTarget(odd), run_time=1.0)
        box_e = panel(even, ACCENT, buff=0.12)
        box_o = panel(odd, WARN, buff=0.12)
        tag_e = note("even", 24, ACCENT).next_to(box_e, DOWN, buff=0.12)
        tag_o = note("odd", 24, WARN).next_to(box_o, DOWN, buff=0.12)
        self.play(ShowCreation(box_e), ShowCreation(box_o), FadeIn(tag_e), FadeIn(tag_o))
        s2 = Tex(R"S_2 = \{\text{even},\ \text{odd}\}").set_color(WHITE).move_to([RX, Y[2], 0])
        self.play(TransformFromCopy(VGroup(box_e, box_o), s2), run_time=1.0)
        same = note("same die, two sample spaces", 26, MEAN_COLOR)
        same.next_to(VGroup(s1, s2), DOWN, buff=0.9).set_x(RX)
        self.play(FadeIn(same))
        self.wait(1.8)

        # ── 두 단계 실험은 나무로 적는다: 동전 두 번
        self.play(*[FadeOut(m) for m in [coins, s0, dice, s1, even, odd, box_e, box_o,
                                          tag_e, tag_o, s2, same]], run_time=0.6)
        tree_tag = note("tree diagram", 26, MUTED).next_to(head[1], DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(tree_tag))

        root = coin("?", 0.85, MUTED).move_to(LEFT * 5.0 + DOWN * 0.2)
        lv1 = VGroup(coin("H", 0.75, ACCENT).move_to(LEFT * 2.4 + UP * 1.25),
                     coin("T", 0.75, CALM).move_to(LEFT * 2.4 + DOWN * 1.65))
        b1 = VGroup(branch(root, lv1[0], ACCENT, 0.9), branch(root, lv1[1], CALM, 0.9))
        self.play(FadeIn(root, scale=0.6))
        self.play(ShowCreation(b1, lag_ratio=0.3), FadeIn(lv1), run_time=1.0)

        leaves = VGroup(coin("H", 0.6, ACCENT), coin("T", 0.6, ACCENT),
                        coin("H", 0.6, CALM), coin("T", 0.6, CALM))
        ys = [1.9, 0.6, -1.0, -2.3]
        for m, y in zip(leaves, ys):
            m.move_to([0.4, y, 0])
        b2 = VGroup(branch(lv1[0], leaves[0], ACCENT, 0.8), branch(lv1[0], leaves[1], ACCENT, 0.8),
                    branch(lv1[1], leaves[2], CALM, 0.8), branch(lv1[1], leaves[3], CALM, 0.8))
        names = ["HH", "HT", "TH", "TT"]
        tags = VGroup(*[
            Text(s, font=BODY_FONT, font_size=32).set_color(ACCENT if s[0] == "H" else CALM)
            .next_to(m, RIGHT, buff=0.35)
            for s, m in zip(names, leaves)
        ])
        self.play(LaggedStartMap(ShowCreation, b2, lag_ratio=0.15),
                  LaggedStartMap(FadeIn, leaves, lag_ratio=0.15), run_time=1.3)
        self.play(LaggedStartMap(FadeIn, tags, lag_ratio=0.1), run_time=0.7)

        brace = Brace(VGroup(leaves, tags), RIGHT)
        n = ValueTracker(0)
        num = counter(n, size=54).next_to(brace, RIGHT, buff=0.3)
        self.add(num)
        self.play(GrowFromCenter(brace), n.animate.set_value(4), run_time=1.0)
        s3 = Tex(R"S = \{HH,\ HT,\ TH,\ TT\}").set_color(WHITE).scale(0.95)
        s3.move_to([0.9, -3.4, 0])
        self.play(TransformFromCopy(tags, s3), run_time=1.3)
        self.play(FlashAround(s3, color=MEAN_COLOR, run_time=1.0))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 사건과 집합 연산 (2.2) — 슬라이드 8 (Definition 2.2–2.6) 앞
# ─────────────────────────────────────────────────────────────
class EventsAndSetOps(InteractiveScene):
    """Example 2.1 의 주사위를 그대로 쓴다. A = 짝수, B = 3의 배수.
    사건(부분집합) → 여집합 → 교집합 → 합집합을 같은 그림에서 칠하고, 배반은
    Example 2.1 의 S₂ = {even, odd} 로 돌아가 짝수와 홀수를 떼어 놓는다.
    Walpole Example 2.26 이 같은 A, B 를 쓰므로 4차 덧셈법칙 계산과 이어진다.
    """

    def construct(self):
        head = slide_title("Events and Set Operations")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        setup = Tex(R"A = \text{even}, \qquad B = \text{divisible by }3")
        setup.scale(0.85).set_color(INK).next_to(head[1], DOWN, buff=0.28)
        self.play(FadeIn(setup, UP))

        # ── 상자가 S, 원 두 개가 A 와 B
        box = Rectangle(width=9.4, height=4.0)
        box.set_stroke(GREY_C, 2).round_corners(0.12)
        box.next_to(setup, DOWN, buff=0.4)
        s_tag = Tex("S").set_color(GREY_A).scale(0.9)
        s_tag.next_to(box.get_corner(UL), DR, buff=0.22)

        circ_a = Circle(radius=1.45).set_stroke(ACCENT, 3)
        circ_b = Circle(radius=1.45).set_stroke(CALM, 3)
        circ_a.move_to(box.get_center() + LEFT * 0.95)
        circ_b.move_to(box.get_center() + RIGHT * 0.95)
        a_tag = Tex("A").set_color(ACCENT).next_to(circ_a, UP, buff=0.12).shift(LEFT * 0.7)
        b_tag = Tex("B").set_color(CALM).next_to(circ_b, UP, buff=0.12).shift(RIGHT * 0.7)

        # A만: 2, 4 / 겹침: 6 / B만: 3 / 밖: 1, 5
        spots = {
            2: circ_a.get_center() + LEFT * 0.62 + UP * 0.45,
            4: circ_a.get_center() + LEFT * 0.62 + DOWN * 0.45,
            6: box.get_center(),
            3: circ_b.get_center() + RIGHT * 0.62,
            1: box.get_corner(DL) + UR * 0.55,
            5: box.get_corner(DR) + UL * 0.55,
        }
        face = {v: die_face(v, 0.6, GREY_A).move_to(p) for v, p in spots.items()}
        faces = VGroup(*face.values())

        self.play(FadeIn(box), Write(s_tag))
        self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.12))
        self.play(ShowCreation(circ_a), Write(a_tag))
        self.play(ShowCreation(circ_b), Write(b_tag))
        self.wait(0.5)

        # ── 연산을 한 자리에서 갈아 끼운다. 글자는 이름과 원소뿐이다.
        anchor = box.get_bottom() + DOWN * 0.75

        def cap(tex, word, color):
            t = Tex(tex).set_color(color).scale(0.95)
            w = note(word, 26, color)
            return VGroup(t, w).arrange(RIGHT, buff=0.5).move_to(anchor)

        def shaded(region, color):
            region.set_stroke(width=0).set_fill(color, 0.30)
            return region

        steps = [
            (shaded(circ_a.copy(), ACCENT),
             cap(R"A = \{2, 4, 6\}", "event", ACCENT)),
            (shaded(Difference(box, circ_a), WARN),
             cap(R"A' = \{1, 3, 5\}", "complement", WARN)),
            (shaded(Intersection(circ_a, circ_b), MEAN_COLOR),
             cap(R"A \cap B = \{6\}", "intersection", MEAN_COLOR)),
            (shaded(Union(circ_a, circ_b), MED_COLOR),
             cap(R"A \cup B = \{2, 3, 4, 6\}", "union", MED_COLOR)),
        ]

        shade = text = None
        for region, txt in steps:
            if shade is None:
                self.play(FadeIn(region), FadeIn(txt))
            else:
                self.play(FadeOut(shade), FadeOut(text), run_time=0.35)
                self.play(FadeIn(region), FadeIn(txt), run_time=0.55)
            self.bring_to_front(faces)
            shade, text = region, txt
            self.wait(1.2)

        # ── 배반: 짝수와 홀수. 겹치는 눈이 하나도 없다.
        self.play(FadeOut(shade), FadeOut(text), FadeOut(circ_b), FadeOut(b_tag), run_time=0.4)
        setup2 = Tex(R"A = \text{even}, \qquad C = \text{odd}")
        setup2.scale(0.85).set_color(INK).move_to(setup)
        swap(self, setup, setup2)

        ca = box.get_center() + LEFT * 2.3
        cc = box.get_center() + RIGHT * 2.3
        circ_c = Circle(radius=1.45).set_stroke(WARN, 3).move_to(cc)
        c_tag = Tex("C").set_color(WARN).next_to(circ_c, UP, buff=0.12).shift(RIGHT * 0.7)
        dest = {
            2: ca + LEFT * 0.55 + UP * 0.45, 4: ca + LEFT * 0.55 + DOWN * 0.45, 6: ca + RIGHT * 0.55,
            1: cc + LEFT * 0.55 + UP * 0.45, 5: cc + LEFT * 0.55 + DOWN * 0.45, 3: cc + RIGHT * 0.55,
        }
        self.play(
            circ_a.animate.move_to(ca), a_tag.animate.shift(LEFT * 1.35),
            *[face[v].animate.move_to(p) for v, p in dest.items()],
            run_time=1.2,
        )
        self.play(ShowCreation(circ_c), Write(c_tag))
        self.play(FadeIn(shaded(circ_a.copy(), ACCENT)), FadeIn(shaded(circ_c.copy(), WARN)))
        self.bring_to_front(faces)
        disjoint = cap(R"A \cap C = \varnothing", "mutually exclusive", MEAN_COLOR)
        self.play(FadeIn(disjoint))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 곱셈규칙 (2.3) — 슬라이드 12 (Rule 2.1 · 2.2) 앞
# ─────────────────────────────────────────────────────────────
class MultiplicationRule(InteractiveScene):
    """동전을 던지고 주사위를 던진다. 나무의 잎 12 개가 2 × 6 격자로 다시 놓이면
    '각각에 대해' 라는 말이 격자의 줄이 된다. 셋째 단계(동전 한 번 더)를 얹으면
    격자가 두 벌이 되어 24 — 단계가 몇 개든 곱한다는 Rule 2.2 가 그림에서 나온다.
    주사위 두 개(Example 2.13)는 슬라이드가 풀도록 여기서 쓰지 않는다.
    """

    def construct(self):
        head = slide_title("The Multiplication Rule")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 나무: 동전 → 주사위
        root = coin("?", 0.8, MUTED).move_to(LEFT * 6.0 + DOWN * 0.45)
        h = coin("H", 0.7, ACCENT).move_to(LEFT * 4.1 + UP * 1.35)
        t = coin("T", 0.7, CALM).move_to(LEFT * 4.1 + DOWN * 2.25)
        b1 = VGroup(branch(root, h, ACCENT, 0.85), branch(root, t, CALM, 0.85))
        self.play(FadeIn(root, scale=0.6))
        self.play(ShowCreation(b1, lag_ratio=0.3), FadeIn(h), FadeIn(t), run_time=1.0)

        leaves = VGroup(*[die_face(i + 1, 0.48, ACCENT) for i in range(6)],
                        *[die_face(i + 1, 0.48, CALM) for i in range(6)])
        for k, m in enumerate(leaves):
            m.move_to([-2.0, 2.55 - k * 0.545, 0])
        b2 = VGroup(*[branch(h, m, ACCENT, 0.7) for m in leaves[:6]],
                    *[branch(t, m, CALM, 0.7) for m in leaves[6:]])
        self.play(LaggedStartMap(ShowCreation, b2, lag_ratio=0.06),
                  LaggedStartMap(FadeIn, leaves, lag_ratio=0.06), run_time=1.6)

        n = ValueTracker(0)
        num = counter(n, size=72).move_to([3.6, 0.3, 0])
        tag = note("outcomes", 28, MEAN_COLOR).next_to(num, DOWN, buff=0.25)
        brace = Brace(leaves, RIGHT)
        self.add(num)
        self.play(GrowFromCenter(brace), FadeIn(tag), n.animate.set_value(12), run_time=1.2)
        self.wait(0.6)

        # ── 잎을 격자로 다시 놓는다: 줄 = 동전, 칸 = 주사위
        self.play(FadeOut(brace), FadeOut(b2), FadeOut(b1), FadeOut(root),
                  num.animate.move_to([5.4, -2.55, 0]), tag.animate.move_to([5.4, -3.3, 0]),
                  run_time=0.6)
        grid_c = np.array([1.3, 0.9, 0])
        DX, DY = 0.72, 0.85
        targets = []
        for k, m in enumerate(leaves):
            r, c = divmod(k, 6)
            targets.append(grid_c + np.array([(c - 2.5) * DX, (0.5 - r) * DY, 0]))
        self.play(
            *[m.animate.move_to(p) for m, p in zip(leaves, targets)],
            h.animate.move_to(grid_c + np.array([-3.2 * DX, 0.5 * DY, 0])),
            t.animate.move_to(grid_c + np.array([-3.2 * DX, -0.5 * DY, 0])),
            run_time=1.4,
        )
        rows = VGroup(h, t)
        cols = VGroup(*leaves[:6])
        br1 = Brace(rows, LEFT)
        n1 = Tex("n_1 = 2").set_color(ACCENT).scale(0.8).next_to(br1, LEFT, buff=0.15)
        br2 = Brace(cols, UP)
        n2 = Tex("n_2 = 6").set_color(CALM).scale(0.8).next_to(br2, UP, buff=0.15)
        self.play(GrowFromCenter(br1), FadeIn(n1), GrowFromCenter(br2), FadeIn(n2))
        eq1 = Tex(R"n_1 \times n_2 = 2 \times 6 = 12").set_color(MEAN_COLOR)
        eq1.scale(0.9).next_to(leaves, DOWN, buff=0.7).set_x(grid_c[0])
        self.play(Write(eq1))
        self.wait(1.4)

        # ── 셋째 단계: 동전 한 번 더. 격자가 두 벌이 된다.
        block = VGroup(rows, leaves)
        self.play(FadeOut(br1), FadeOut(n1), FadeOut(br2), FadeOut(n2), FadeOut(eq1),
                  block.animate.scale(0.8).move_to([0.6, 1.55, 0]), run_time=0.9)
        block2 = block.copy().move_to([0.6, -1.3, 0])
        c3 = VGroup(coin("H", 0.6, MEAN_COLOR).next_to(block, LEFT, buff=0.7),
                    coin("T", 0.6, MEAN_COLOR).next_to(block2, LEFT, buff=0.7))
        self.play(TransformFromCopy(block, block2), FadeIn(c3), n.animate.set_value(24), run_time=1.3)
        br3 = Brace(c3, LEFT)
        n3 = Tex("n_3 = 2").set_color(MEAN_COLOR).scale(0.8).next_to(br3, LEFT, buff=0.15)
        self.play(GrowFromCenter(br3), FadeIn(n3))
        eq2 = Tex(R"2 \times 6 \times 2 = 24").set_color(MEAN_COLOR).scale(0.9)
        eq2.move_to([5.0, 1.6, 0])
        self.play(Write(eq2))
        self.wait(1.0)

        rule = Tex(R"n_1 \times n_2 \times \cdots \times n_k").set_color(WHITE).scale(1.05)
        rule.next_to(eq2, DOWN, buff=0.9).set_x(eq2.get_x())
        steps = note("k steps", 26).next_to(rule, DOWN, buff=0.3)
        self.play(Write(rule), FadeIn(steps))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 순열 (2.3) — 슬라이드 17 (Definition 2.7 · Theorem 2.1 · 2.2) 앞
# ─────────────────────────────────────────────────────────────
class Permutations(InteractiveScene):
    """교재 2.3절 본문의 보기 그대로다. 글자 a, b, c 를 늘어놓으면 3 · 2 · 1 = 6.
    a, b, c, d 에서 두 개를 늘어놓으면 4 · 3 = 12. 자리마다 남은 카드에 테두리를 둘러
    후보 수를 세고, 그 수가 곱의 법칙으로 곱해진다. 12 개의 순서쌍은 다음 영상
    (Combinations) 이 그대로 이어받는다.
    """

    def construct(self):
        head = slide_title("Permutations")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        LX, RX = -3.6, 3.4

        # ── a, b, c 세 장을 모두 늘어놓는다
        letters = "abc"
        pool = {ch: letter_chip(ch) for ch in letters}
        row = VGroup(*pool.values()).arrange(RIGHT, buff=0.3).move_to([LX, 2.0, 0])
        frame = panel(row, MUTED, buff=0.22)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1), FadeIn(frame))

        slots = VGroup(*[slot() for _ in range(3)]).arrange(RIGHT, buff=0.4)
        slots.move_to([LX, 0.1, 0])
        self.play(ShowCreation(slots))

        placed = []

        def left_over():
            return [ch for ch in letters if ch not in placed]

        counts = VGroup()
        for s, ch in zip(slots, "abc"):
            avail = left_over()
            rings = VGroup(*[ring(pool[x], ACCENT, buff=0.06) for x in avail])
            cnt = Integer(len(avail)).set_color(ACCENT).scale(1.05).next_to(s, DOWN, buff=0.25)
            self.play(ShowCreation(rings), FadeIn(cnt), run_time=0.6)
            self.wait(0.2)
            self.play(FadeOut(rings), pool[ch].animate.move_to(s), run_time=0.6)
            placed.append(ch)
            counts.add(cnt)

        eq1 = Tex(R"3 \times 2 \times 1 = 3! = 6").set_color(ACCENT)
        eq1.scale(0.95).move_to([LX, -1.7, 0])
        self.play(TransformFromCopy(counts, eq1), run_time=1.0)

        # 오른쪽: 여섯 배열을 모두 적는다
        arr = VGroup(*[
            Text(s, font=BODY_FONT, font_size=34).set_color(INK)
            for s in ("abc", "acb", "bac", "bca", "cab", "cba")
        ])
        arr.arrange_in_grid(3, 2, buff=0.5).move_to([RX, 1.0, 0])
        n6 = ValueTracker(0)
        num6 = counter(n6, color=ACCENT, size=56).next_to(arr, DOWN, buff=0.5)
        tag6 = note("arrangements", 26, ACCENT).next_to(num6, DOWN, buff=0.2)
        self.add(num6)
        self.play(LaggedStartMap(FadeIn, arr, lag_ratio=0.12), n6.animate.set_value(6),
                  FadeIn(tag6), run_time=1.5)
        self.wait(1.5)

        # ── a, b, c, d 에서 두 개만 늘어놓는다
        freeze(num6)
        self.play(*[FadeOut(m) for m in [row, frame, slots, counts, eq1, arr, num6, tag6]],
                  run_time=0.6)

        letters = "abcd"
        pool = {ch: letter_chip(ch) for ch in letters}
        row = VGroup(*pool.values()).arrange(RIGHT, buff=0.3).move_to([LX, 2.0, 0])
        frame = panel(row, MUTED, buff=0.22)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1), FadeIn(frame))
        slots = VGroup(*[slot() for _ in range(2)]).arrange(RIGHT, buff=0.4)
        slots.move_to([LX, 0.1, 0])
        self.play(ShowCreation(slots))

        placed = []
        counts = VGroup()
        for s, ch in zip(slots, "ab"):
            avail = [x for x in letters if x not in placed]
            rings = VGroup(*[ring(pool[x], CALM, buff=0.06) for x in avail])
            cnt = Integer(len(avail)).set_color(CALM).scale(1.05).next_to(s, DOWN, buff=0.25)
            self.play(ShowCreation(rings), FadeIn(cnt), run_time=0.6)
            self.wait(0.2)
            self.play(FadeOut(rings), pool[ch].animate.move_to(s), run_time=0.6)
            placed.append(ch)
            counts.add(cnt)

        eq2 = Tex(R"4 \times 3 = 12").set_color(CALM).scale(0.95).move_to([LX, -1.7, 0])
        self.play(TransformFromCopy(counts, eq2), run_time=1.0)

        pairs = VGroup(*[
            Text(a + b, font=BODY_FONT, font_size=32).set_color(INK)
            for a, b in _it.permutations(letters, 2)
        ])
        pairs.arrange_in_grid(3, 4, buff=0.45).move_to([RX, 1.3, 0])
        n12 = ValueTracker(0)
        num12 = counter(n12, color=CALM, size=56).next_to(pairs, DOWN, buff=0.45)
        tag12 = note("ordered pairs", 26, CALM).next_to(num12, DOWN, buff=0.2)
        self.add(num12)
        self.play(LaggedStartMap(FadeIn, pairs, lag_ratio=0.06), n12.animate.set_value(12),
                  FadeIn(tag12), run_time=1.6)
        self.wait(0.8)

        # ── 식으로 정리한다
        freeze(num12)
        self.play(FadeOut(num12), FadeOut(tag12), run_time=0.4)
        p42 = Tex(R"{}_4P_2 = 4 \times 3 = \frac{4!}{2!} = 12").set_color(CALM)
        p42.scale(0.95).next_to(pairs, DOWN, buff=0.5)
        self.play(Write(p42))
        self.wait(0.8)
        general = Tex(R"{}_nP_r = \frac{n!}{(n-r)!}").set_color(WHITE).scale(1.1)
        general.move_to([LX, -2.9, 0])
        self.play(FadeOut(eq2), FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 조합 (2.3) — 슬라이드 18 (Theorem 2.6) 앞
# ─────────────────────────────────────────────────────────────
class Combinations(InteractiveScene):
    """Permutations 가 남긴 12 개의 순서쌍에서 시작한다. ab 와 ba 는 같은 두 글자다.
    순서를 가리키던 화살표를 지우고 둘을 포개면 6 장이 남는다. 포개는 동작이
    2! 로 나누는 일이고, 그 식이 ₙCᵣ = ₙPᵣ / r! 이다.
    참고: legacy/_2018/eop/combinations.py HowToComputeNChooseK.
    """
    letters = "abcd"

    def card(self, pair, color):
        """순서쌍 카드. 위의 화살표가 '앞자리 → 뒷자리' 다. 순서를 버릴 때 이 화살표만 지운다.
        (테두리, 두 글자, 화살표) 순서라 arrow 를 out[2] 로 집을 수 있다."""
        chips = VGroup(*[letter_chip(ch, 0.5) for ch in pair]).arrange(RIGHT, buff=0.16)
        box = SurroundingRectangle(chips, buff=0.14).round_corners(0.1)
        box.set_stroke(color, 2).set_fill(color, 0.07)
        arrow = Arrow(chips[0].get_top() + UP * 0.05, chips[1].get_top() + UP * 0.05, buff=0.02)
        arrow.set_color(color).set_stroke(width=2)
        return VGroup(box, chips, arrow)

    def construct(self):
        head = slide_title("Combinations")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        pool = VGroup(*[letter_chip(ch) for ch in self.letters]).arrange(RIGHT, buff=0.3)
        pool.next_to(head[1], DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        frame = panel(pool, MUTED, buff=0.22)
        self.play(LaggedStartMap(FadeIn, pool, lag_ratio=0.1), FadeIn(frame))

        # ── 순서를 따진 12 장 (Permutations 의 마지막 화면)
        RIGHT_X = 4.5
        ordered = list(_it.permutations(self.letters, 2))
        cards = VGroup(*[self.card(p, ACCENT) for p in ordered])
        cards.arrange_in_grid(3, 4, buff=0.3)
        cards.set_width(6.6).next_to(frame, DOWN, buff=0.5).set_x(-2.6)

        n_perm = ValueTracker(0)
        perm_num = counter(n_perm, color=ACCENT, size=64)
        perm_tag = note("ordered", 26, ACCENT).move_to([RIGHT_X, 1.4, 0])
        perm_num.next_to(perm_tag, DOWN, buff=0.2)
        self.add(perm_num)
        self.play(LaggedStartMap(FadeIn, cards, lag_ratio=0.06), n_perm.animate.set_value(12),
                  FadeIn(perm_tag), run_time=1.8)
        perm_tex = Tex(R"{}_4P_2 = 12").set_color(ACCENT).scale(0.95)
        perm_tex.next_to(perm_num, DOWN, buff=0.5)
        self.play(Write(perm_tex))
        self.wait(1.0)

        # ── ab 와 ba: 같은 두 글자, 순서만 다르다. 이런 짝이 2! = 2 장씩이다.
        i_ab = ordered.index(("a", "b"))
        i_ba = ordered.index(("b", "a"))
        marks = VGroup(ring(cards[i_ab], MEAN_COLOR, buff=0.06), ring(cards[i_ba], MEAN_COLOR, buff=0.06))
        two = Tex(R"2! = 2").set_color(MEAN_COLOR).scale(0.95).move_to([RIGHT_X, -0.9, 0])
        each = note("orders per pair", 24, MEAN_COLOR).next_to(two, DOWN, buff=0.2)
        self.play(ShowCreation(marks), FadeIn(two), FadeIn(each))
        self.wait(1.2)
        self.play(FadeOut(marks), run_time=0.3)

        # ── 순서를 버린다: 화살표를 지우고 둘씩 포갠다
        groups = {}
        for i, p in enumerate(ordered):
            groups.setdefault(frozenset(p), []).append(i)
        keep = [idx[0] for idx in groups.values()]
        drop = [idx[1] for idx in groups.values()]

        n_comb = ValueTracker(12)
        comb_num = counter(n_comb, color=CALM, size=64)
        comb_tag = note("unordered", 26, CALM).move_to(perm_tag)
        comb_num.next_to(comb_tag, DOWN, buff=0.2)
        freeze(perm_num)
        self.play(FadeOut(perm_tag), FadeOut(perm_num), FadeOut(perm_tex), run_time=0.35)
        self.add(comb_num)
        self.play(FadeIn(comb_tag), run_time=0.35)

        self.play(*[cards[i][2].animate.set_opacity(0) for i in range(12)], run_time=0.5)
        self.play(
            *[cards[d].animate.move_to(cards[k]).set_opacity(0) for k, d in zip(keep, drop)],
            *[cards[k][0].animate.set_stroke(CALM, 2).set_fill(CALM, 0.07) for k in keep],
            n_comb.animate.set_value(6),
            run_time=1.8,
        )
        self.remove(*[cards[d] for d in drop])
        for k in keep:
            cards[k].remove(cards[k][2])

        survivors = VGroup(*[cards[k] for k in keep])
        survivors.generate_target()
        survivors.target.arrange_in_grid(2, 3, buff=0.35)
        survivors.target.set_width(5.2).move_to(survivors)
        self.play(MoveToTarget(survivors), run_time=1.2)
        self.wait(0.5)

        # ── 식: 포갠 것이 2! 로 나눈 것이다
        self.play(FadeOut(two), FadeOut(each), run_time=0.3)
        comb_tex = Tex(R"{}_4C_2 = \frac{{}_4P_2}{2!} = \frac{12}{2} = 6").set_color(CALM)
        comb_tex.scale(0.95).next_to(comb_num, DOWN, buff=0.5)
        self.play(Write(comb_tex))
        self.wait(1.0)
        general = Tex(R"\binom{n}{r} = \frac{{}_nP_r}{r!} = \frac{n!}{r!\,(n-r)!}").set_color(WHITE)
        general.scale(1.0).next_to(survivors, DOWN, buff=0.6).set_x(survivors.get_x())
        self.play(FadeIn(general, UP))
        self.play(FlashAround(general, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 사건의 확률 (2.4) — 슬라이드 27 (Definition 2.9 · Rule 2.3) 앞
# ─────────────────────────────────────────────────────────────
class ProbabilityOfEvent(InteractiveScene):
    """Example 2.1 의 주사위. 눈마다 무게 1/6 을 막대로 달아 두고, 여섯을 쌓으면 높이가
    1 이다(P(S) = 1). 사건 A = 짝수의 확률은 A 에 든 눈의 무게를 쌓은 것 — 3/6.
    등가능이면 그 값이 n/N 이라는 Rule 2.3 이 막대의 개수 비로 보인다.
    찌그러진 주사위(Example 2.25)는 슬라이드가 푼다.
    """

    def construct(self):
        head = slide_title("Probability of an Event")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        faces = VGroup(*[die_face(i + 1, 0.6, GREY_A) for i in range(6)])
        faces.arrange(RIGHT, buff=0.55).move_to([-2.6, 1.55, 0])
        self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.1))

        # ── 무게: 같은 높이 막대 여섯, 각 1/6
        H = 3.3                                  # 높이 1 을 이 길이로 그린다
        base_y = -2.55
        bars = VGroup(*[bar(1, 6, width=0.6, height=H, color=ACCENT) for _ in range(6)])
        for b, f in zip(bars, faces):
            b.move_to([f.get_x(), base_y + b.get_height() / 2, 0])
        wts = VGroup(*[Tex(R"\frac{1}{6}").scale(0.7).set_color(ACCENT).next_to(b, UP, buff=0.12)
                       for b in bars])
        base = Line(LEFT * 5.2, RIGHT * 0.1).set_stroke(GREY_C, 2).move_to([-2.6, base_y, 0])
        self.play(ShowCreation(base))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                  LaggedStartMap(FadeIn, wts, lag_ratio=0.1), run_time=1.2)
        wtag = note("weights", 26, ACCENT).next_to(base, DOWN, buff=0.25).align_to(base, LEFT)
        self.play(FadeIn(wtag))
        self.wait(0.6)

        # ── 여섯을 쌓으면 1
        col_x = 2.4
        stack = bars.copy()
        for i, b in enumerate(stack):
            b.generate_target()
            b.target.move_to([col_x, base_y + (i + 0.5) * H / 6, 0])
        axis = Line(DOWN * H / 2, UP * H / 2).set_stroke(GREY_C, 2).move_to([col_x - 0.6, base_y + H / 2, 0])
        one = Tex("1").set_color(GREY_A).next_to(axis.get_top(), LEFT, buff=0.15)
        zero = Tex("0").set_color(GREY_A).next_to(axis.get_bottom(), LEFT, buff=0.15)
        self.play(ShowCreation(axis), FadeIn(one), FadeIn(zero))
        self.play(LaggedStartMap(MoveToTarget, stack, lag_ratio=0.12), run_time=1.5)
        ps = Tex(R"P(S) = 1").set_color(WHITE).next_to(stack, RIGHT, buff=0.5).set_y(base_y + H * 0.85)
        self.play(Write(ps))
        self.wait(1.0)

        # ── 사건 A = 짝수: A 에 든 눈의 무게만 쌓는다
        self.play(FadeOut(stack), run_time=0.5)
        setup = Tex(R"A = \text{even} = \{2, 4, 6\}").scale(0.85).set_color(CALM)
        setup.next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.7)
        self.play(FadeIn(setup, UP))
        idx = [1, 3, 5]
        marks = VGroup(*[ring(faces[i], CALM, buff=0.07) for i in idx])
        self.play(ShowCreation(marks),
                  *[bars[i].animate.set_fill(CALM, 0.85).set_stroke(CALM, 2) for i in idx],
                  *[wts[i].animate.set_color(CALM) for i in idx])
        sub = VGroup(*[bars[i].copy() for i in idx])
        for j, b in enumerate(sub):
            b.generate_target()
            b.target.move_to([col_x, base_y + (j + 0.5) * H / 6, 0])
        self.play(LaggedStartMap(MoveToTarget, sub, lag_ratio=0.15), run_time=1.3)
        pa = Tex(R"P(A) = \frac{3}{6}").set_color(CALM).next_to(sub, RIGHT, buff=0.5)
        self.play(Write(pa))
        self.wait(1.0)

        # ── 등가능이면 개수 비: n / N
        brN = Brace(faces, UP)
        tN = Tex("N = 6").set_color(GREY_A).scale(0.8).next_to(brN, UP, buff=0.12)
        self.play(GrowFromCenter(brN), FadeIn(tN))
        brn = Brace(VGroup(*[bars[i] for i in idx]), DOWN, buff=0.05).shift(DOWN * 0.05)
        tn = Tex("n = 3").set_color(CALM).scale(0.8).next_to(brn, DOWN, buff=0.1)
        self.play(FadeOut(wtag), GrowFromCenter(brn), FadeIn(tn))
        rule = Tex(R"P(A) = \frac{n}{N}").set_color(WHITE).scale(1.1)
        rule.move_to([4.9, -3.0, 0])
        equal = note("equally likely outcomes", 24, GREY_B).next_to(rule, DOWN, buff=0.25)
        self.play(TransformFromCopy(pa, rule), FadeIn(equal), run_time=1.2)
        self.play(FlashAround(rule, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 덧셈법칙 (2.5) — 슬라이드 35 (Theorem 2.7 · 2.9) 앞
# ─────────────────────────────────────────────────────────────
class AdditionRule(InteractiveScene):
    """벤 다이어그램의 세 조각마다 '몇 번 세었나' 를 숫자로 달아 둔다.
    P(A) 를 더하면 왼쪽과 가운데가 1, P(B) 를 더하면 가운데가 2 가 된다.
    가운데만 2 라는 것이 눈에 남으면 왜 한 번 빼는지 말이 필요 없다.
    배반이면 겹치는 자리가 없고, A 와 A' 이 S 를 채우면 둘의 합이 1 이다(Theorem 2.9).
    Example 2.29 의 숫자는 슬라이드가 푼다.
    """

    def construct(self):
        head = slide_title("Additive Rules")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 벤 다이어그램. 가운데 위에 두고 아래를 식이 쓸 자리로 비워 둔다.
        cA = Circle(radius=1.7).move_to(LEFT * 1.05 + UP * 0.6)
        cB = Circle(radius=1.7).move_to(RIGHT * 1.05 + UP * 0.6)
        cA.set_stroke(ACCENT, 3)
        cB.set_stroke(CALM, 3)

        only_a = Difference(cA, cB).set_stroke(width=0).set_fill(ACCENT, 0.0)
        lens = Intersection(cA, cB).set_stroke(width=0).set_fill(MEAN_COLOR, 0.0)
        only_b = Difference(cB, cA).set_stroke(width=0).set_fill(CALM, 0.0)
        regions = VGroup(only_a, lens, only_b)

        tA = Tex("A").set_color(ACCENT).next_to(cA, UP, buff=0.1).shift(LEFT * 0.9)
        tB = Tex("B").set_color(CALM).next_to(cB, UP, buff=0.1).shift(RIGHT * 0.9)

        self.play(ShowCreation(cA), FadeIn(tA))
        self.play(ShowCreation(cB), FadeIn(tB))
        self.add(regions)
        self.wait(0.3)

        # ── 조각마다 '몇 번 세었나' 를 달아 둔다
        spots = [cA.get_center() + LEFT * 0.86,
                 (cA.get_center() + cB.get_center()) / 2,
                 cB.get_center() + RIGHT * 0.86]
        trackers = [ValueTracker(0) for _ in range(3)]
        tallies = VGroup(*[
            counter(t, color=WHITE, size=46).move_to(p)
            for t, p in zip(trackers, spots)
        ])

        # ── 항을 하나씩 적으면서 그 항이 칠하는 자리를 함께 센다.
        terms = VGroup(*[
            Tex(t) for t in
            [R"P(A \cup B)", "=", "P(A)", "+", "P(B)", "-", R"P(A \cap B)"]
        ])
        terms.arrange(RIGHT, buff=0.18)
        scale = min(0.95, 9.0 / terms.get_width())
        terms.scale(scale).to_edge(DOWN, buff=1.35).set_x(0)
        terms[2].set_color(ACCENT)
        terms[4].set_color(CALM)
        terms[6].set_color(MEAN_COLOR)

        self.play(Write(terms[0]), Write(terms[1]))

        # + P(A) : 왼쪽과 가운데가 1 이 된다
        self.add(tallies[0], tallies[1])
        self.play(
            Write(terms[2]),
            only_a.animate.set_fill(ACCENT, 0.35),
            lens.animate.set_fill(ACCENT, 0.35),
            trackers[0].animate.set_value(1),
            trackers[1].animate.set_value(1),
            run_time=1.1,
        )
        self.bring_to_front(tallies)
        self.wait(0.6)

        # + P(B) : 가운데만 2 가 된다
        self.add(tallies[2])
        self.play(
            Write(terms[3]), Write(terms[4]),
            only_b.animate.set_fill(CALM, 0.35),
            lens.animate.set_fill(MEAN_COLOR, 0.62),
            trackers[2].animate.set_value(1),
            trackers[1].animate.set_value(2),
            run_time=1.1,
        )
        self.bring_to_front(tallies)
        self.play(FlashAround(tallies[1], color=MEAN_COLOR, buff=0.2), run_time=1.0)
        self.wait(0.6)

        # − P(A ∩ B) : 다시 1 로 내린다
        self.play(
            Write(terms[5]), Write(terms[6]),
            lens.animate.set_fill(MEAN_COLOR, 0.35),
            trackers[1].animate.set_value(1),
            run_time=1.1,
        )
        self.bring_to_front(tallies)

        once = note("counted once", 28, MEAN_COLOR)
        once.next_to(cB, RIGHT, buff=0.55).set_y(cB.get_y())
        self.play(
            *[FlashAround(t, color=MEAN_COLOR, buff=0.2) for t in tallies],
            FadeIn(once), run_time=1.2,
        )
        self.wait(1.6)

        # ── 배반이면 겹치는 자리가 아예 없다. 조각 대신 온전한 원을 칠한다.
        freeze(*tallies)
        self.play(
            FadeOut(terms[5]), FadeOut(terms[6]),
            FadeOut(tallies[1]), FadeOut(regions), FadeOut(once),
            cA.animate.set_fill(ACCENT, 0.32).shift(LEFT * 1.15),
            tA.animate.shift(LEFT * 1.15), tallies[0].animate.shift(LEFT * 1.15),
            cB.animate.set_fill(CALM, 0.32).shift(RIGHT * 1.15),
            tB.animate.shift(RIGHT * 1.15), tallies[2].animate.shift(RIGHT * 1.15),
            run_time=1.3,
        )
        self.bring_to_front(tallies[0], tallies[2])
        empty = Tex(R"A \cap B = \varnothing").set_color(WARN).scale(1.05)
        empty.next_to(cB, RIGHT, buff=0.45).set_y(cB.get_y())
        self.play(FadeIn(empty))
        self.wait(1.8)

        # ── 여사건: A 와 A' 이 S 를 채운다. 둘의 합이 1 이다.
        self.play(
            FadeOut(cB), FadeOut(tB), FadeOut(tallies[2]), FadeOut(empty),
            FadeOut(tallies[0]), *[FadeOut(t) for t in terms[:5]],
            cA.animate.move_to(UP * 0.6 + LEFT * 0.8), tA.animate.move_to(UP * 2.2 + LEFT * 2.6),
            run_time=0.9,
        )
        box = Rectangle(width=8.4, height=4.3).set_stroke(GREY_C, 2).round_corners(0.12)
        box.move_to(UP * 0.6)
        s_tag = Tex("S").set_color(GREY_A).scale(0.9).next_to(box.get_corner(UL), DR, buff=0.22)
        outside = Difference(box, cA).set_stroke(width=0).set_fill(WARN, 0.3)
        tA2 = Tex("A'").set_color(WARN).move_to(box.get_center() + RIGHT * 2.9)
        self.play(ShowCreation(box), Write(s_tag))
        self.play(FadeIn(outside), FadeIn(tA2))
        comp = Tex(R"P(A) + P(A') = 1", t2c={"P(A)": ACCENT, "P(A')": WARN})
        comp.scale(1.05).to_edge(DOWN, buff=1.35)
        self.play(Write(comp))
        self.play(FlashAround(comp, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 네 자리 짝수 — 제약이 센 자리부터 채운다 (Walpole Example 2.17)
# ─────────────────────────────────────────────────────────────
def digit_chip(d, size=0.72, color=INK):
    """숫자 카드 한 장. 글자가 아니라 물건으로 다루려고 테두리를 두른다."""
    body = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18)
    body.set_stroke(color, 2).set_fill(BLACK, 1)
    txt = Text(str(d), font=BODY_FONT, font_size=int(size * 50)).set_color(color)
    txt.move_to(body)
    return VGroup(body, txt)


def cross(mob, color=WARN, width=4):
    """'이건 못 온다' 표시. 대각선 두 줄."""
    a = Line(mob.get_corner(UL), mob.get_corner(DR))
    b = Line(mob.get_corner(UR), mob.get_corner(DL))
    return VGroup(a, b).set_stroke(color, width)


class Example217EvenNumbers(InteractiveScene):
    """Example 2.17 — 네 자리 짝수. 원본 15 뒤 (풀이 16 앞), Example215Club 다음에 이어진다.

    0, 1, 2, 5, 6, 9 로 만드는 네 자리 짝수. 천의 자리부터 채우면 일의 자리 후보가
    3 개였다 2 개였다 하며 갈라지는 것을 먼저 보이고, 일의 자리부터 채우면 경우가
    둘(0 / 2·6)로 깨끗이 나뉘어 60 + 96 = 156 이 되는 것을 보인다.
    '제약이 센 자리부터' 라는 말을 카드가 움직이는 순서가 대신한다.
    """
    digits = [0, 1, 2, 5, 6, 9]
    even = [0, 2, 6]

    # ── 도우미 ─────────────────────────────────────────────
    def tint(self, chip, color):
        """카드 색을 바꾸는 애니메이션 둘. 받는 쪽에서 `*` 로 푼다."""
        return [chip[0].animate.set_stroke(color, 2),
                chip[1].animate.set_color(color)]

    def rings(self, chips, color):
        return VGroup(*[ring(c, color, buff=0.06) for c in chips])

    def count_under(self, slot, n, color):
        t = Integer(n).set_color(color).scale(1.1)
        t.next_to(slot, DOWN, buff=0.28)
        return t

    def construct(self):
        head = slide_title("Example 2.17")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 숫자 카드 여섯 장. 자리를 비워도 줄은 그대로 둔다.
        pool = VGroup(*[digit_chip(d) for d in self.digits])
        pool.arrange(RIGHT, buff=0.32)
        pool.next_to(head[1], DOWN, buff=0.5).set_x(-2.6)
        home = [c.get_center().copy() for c in pool]
        chip = {d: pool[i] for i, d in enumerate(self.digits)}
        frame = panel(pool, MUTED, buff=0.22)
        self.play(LaggedStartMap(FadeIn, pool, lag_ratio=0.1), FadeIn(frame))

        # ── 자리 네 칸
        slots = VGroup(*[
            RoundedRectangle(width=1.25, height=1.25, corner_radius=0.12)
            .set_stroke(MUTED, 2.5) for _ in range(4)
        ])
        slots.arrange(RIGHT, buff=0.45).next_to(frame, DOWN, buff=1.0).set_x(-2.6)
        slot_tags = VGroup(*[
            note(s, 22, MUTED).next_to(slots[i], UP, buff=0.12)
            for i, s in enumerate(["1000s", "100s", "10s", "1s"])
        ])
        self.play(ShowCreation(slots), FadeIn(slot_tags))

        # 오른쪽 기둥: 식이 쌓이는 자리
        RIGHT_X = 4.35
        phase = note("thousands first", 28, WARN).move_to([RIGHT_X, 2.35, 0])
        self.play(FadeIn(phase))
        self.wait(0.3)

        # ── 1) 천의 자리부터: 일의 자리 후보가 3 개였다 2 개였다 한다
        self.play(chip[1].animate.move_to(slots[0]))
        r = self.rings([chip[0], chip[2], chip[6]], CALM)
        c_units = self.count_under(slots[3], 3, CALM)
        self.play(ShowCreation(r), FadeIn(c_units))
        self.wait(0.8)

        self.play(FadeOut(r), FadeOut(c_units), run_time=0.3)
        self.play(chip[1].animate.move_to(home[1]),
                  chip[2].animate.move_to(slots[0]), run_time=0.8)
        r = self.rings([chip[0], chip[6]], WARN)
        c_units = self.count_under(slots[3], 2, WARN)
        self.play(ShowCreation(r), FadeIn(c_units))
        why = note("3 or 2 — depends", 26, WARN).next_to(c_units, DOWN, buff=0.3)
        self.play(FadeIn(why))
        self.wait(1.2)

        # 접는다
        self.play(FadeOut(r), FadeOut(c_units), FadeOut(why),
                  chip[2].animate.move_to(home[2]), FadeOut(phase), run_time=0.6)
        phase = note("units first", 28, CALM).move_to([RIGHT_X, 2.35, 0])
        self.play(FadeIn(phase))
        self.wait(0.3)

        # ── 2) 일의 자리 = 0
        case1 = note("units 0", 26, CALM).move_to([RIGHT_X, 1.35, 0])
        self.play(FadeIn(case1))
        self.play(chip[0].animate.move_to(slots[3]), *self.tint(chip[0], CALM))
        c1 = self.count_under(slots[3], 1, CALM)
        self.play(FadeIn(c1))

        counts1 = VGroup(c1)
        picks = [(0, 1), (1, 5), (2, 9)]       # (칸, 뽑을 카드) — 실제 예 1590
        for k, (s, d) in enumerate(picks):
            avail = [x for x in self.digits if chip[x].get_center()[1] > slots.get_y() + 0.5]
            r = self.rings([chip[x] for x in avail], CALM)
            n = self.count_under(slots[s], len(avail), CALM)
            self.play(ShowCreation(r), FadeIn(n), run_time=0.7)
            self.wait(0.25)
            self.play(FadeOut(r), chip[d].animate.move_to(slots[s]), run_time=0.6)
            counts1.add(n)

        eq1 = Tex(R"1 \times 5 \times 4 \times 3 = 60").set_color(CALM)
        eq1.set_width(4.4).next_to(case1, DOWN, buff=0.3)
        self.play(TransformFromCopy(VGroup(*[counts1[i] for i in (0, 1, 2, 3)]), eq1),
                  run_time=1.2)
        self.wait(1.0)

        # 카드를 되돌린다
        self.play(*[chip[d].animate.move_to(home[self.digits.index(d)]) for d in (0, 1, 5, 9)],
                  *self.tint(chip[0], INK), FadeOut(counts1), run_time=0.8)

        # ── 3) 일의 자리 = 2 (또는 6): 천의 자리에서 0 이 빠진다
        case2 = note("units 2 or 6", 26, ACCENT).move_to([RIGHT_X, -0.55, 0])
        self.play(FadeIn(case2))
        self.play(chip[2].animate.move_to(slots[3]), *self.tint(chip[2], ACCENT))
        r6 = ring(chip[6], ACCENT, buff=0.06)
        c2 = self.count_under(slots[3], 2, ACCENT)
        self.play(ShowCreation(r6), FadeIn(c2))
        self.wait(0.4)
        self.play(FadeOut(r6), run_time=0.3)

        counts2 = VGroup(c2)
        # 천의 자리: 0 은 못 온다
        avail = [1, 5, 6, 9]
        x0 = cross(chip[0])
        r = self.rings([chip[x] for x in avail], ACCENT)
        n = self.count_under(slots[0], 4, ACCENT)
        self.play(ShowCreation(x0), ShowCreation(r), FadeIn(n), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(r), chip[1].animate.move_to(slots[0]), run_time=0.6)
        counts2.add(n)
        # 백의 자리: 이제 0 도 온다
        self.play(FadeOut(x0), run_time=0.3)
        avail = [0, 5, 6, 9]
        r = self.rings([chip[x] for x in avail], ACCENT)
        n = self.count_under(slots[1], 4, ACCENT)
        self.play(ShowCreation(r), FadeIn(n), run_time=0.7)
        self.wait(0.25)
        self.play(FadeOut(r), chip[0].animate.move_to(slots[1]), run_time=0.6)
        counts2.add(n)
        # 십의 자리
        avail = [5, 6, 9]
        r = self.rings([chip[x] for x in avail], ACCENT)
        n = self.count_under(slots[2], 3, ACCENT)
        self.play(ShowCreation(r), FadeIn(n), run_time=0.7)
        self.wait(0.25)
        self.play(FadeOut(r), chip[5].animate.move_to(slots[2]), run_time=0.6)
        counts2.add(n)

        eq2 = Tex(R"2 \times 4 \times 4 \times 3 = 96").set_color(ACCENT)
        eq2.set_width(4.4).next_to(case2, DOWN, buff=0.3)
        self.play(TransformFromCopy(counts2, eq2), run_time=1.2)
        self.wait(1.0)

        # ── 4) 두 경우는 겹치지 않는다: 더한다
        total = Tex(R"60 + 96 = 156").set_color(MEAN_COLOR).scale(1.2)
        total.next_to(eq2, DOWN, buff=0.6).set_x(RIGHT_X)
        self.play(TransformFromCopy(VGroup(eq1, eq2), total), run_time=1.4)
        self.play(FlashAround(total, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 원순열 — 돌려서 같은 것은 하나로 센다 (Walpole Theorem 2.3, 슬라이드 32)
# ─────────────────────────────────────────────────────────────
class CircularPermutation(InteractiveScene):
    """슬라이드 32 (정리 2.3, 원순열 (n−1)!). 판서에서는 결과만 쓰므로 유도를 그림이 맡는다.

    네 명이 원탁에 앉는다. 줄로 세우면 4! = 24 인데, 원탁을 90° 씩 돌린 네 자리는
    이웃이 그대로라 같은 앉음이다 — 그래서 4 로 나눠 6. 같은 6 을 'A 를 고정하고
    나머지 셋만 세운다' 로 다시 얻는다. 두 길이 (n−1)! 에서 만난다.
    """
    names = ["A", "B", "C", "D"]
    R = 1.25                                 # 원탁 반지름
    SEAT = 0.55                              # 원탁 테두리 밖으로 사람이 앉는 거리
    ANG = [PI / 2, 0, -PI / 2, PI]           # 시계 방향: 위, 오른쪽, 아래, 왼쪽

    # ── 도우미 ─────────────────────────────────────────────
    def person(self, name, height=0.62, tint=None):
        m = chito("front", tint, height)
        tag = note(name, 22).next_to(m, DOWN, buff=0.06)
        return Group(m, tag)

    def seat_point(self, center, angle):
        return center + (self.R + self.SEAT) * np.array([np.cos(angle), np.sin(angle), 0])

    def mini(self, order, color=MUTED, r=0.42, size=24, fixed=None):
        """글자만 앉힌 작은 원탁. order 는 위·오른쪽·아래·왼쪽 순서."""
        disc = Circle(radius=r).set_stroke(color, 2)
        letters = VGroup(*[
            note(nm, size, MEAN_COLOR if nm == fixed else INK)
            .move_to(disc.get_center() + r * 0.62 * np.array([np.cos(a), np.sin(a), 0]))
            for nm, a in zip(order, self.ANG)
        ])
        return VGroup(disc, letters)

    def rotate_once(self, people, center, run_time=1.2):
        """모두가 시계 방향으로 한 자리씩 옮긴다. 이웃 관계는 그대로다."""
        anims = []
        for p in people:
            a = p.ps_angle
            arc = Arc(start_angle=a, angle=-PI / 2, radius=self.R + self.SEAT,
                      arc_center=center)
            anims.append(MoveAlongPath(p, arc))
            p.ps_angle = a - PI / 2
        self.play(*anims, run_time=run_time)

    def construct(self):
        head = slide_title("Around a Round Table")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 원탁과 네 사람
        center = np.array([-3.3, 0.3, 0])
        table = Circle(radius=self.R).set_stroke(MUTED, 2.5).set_fill(GREY_E, 0.35)
        table.move_to(center)
        people = Group(*[self.person(n) for n in self.names])
        for p, a in zip(people, self.ANG):
            p.move_to(self.seat_point(center, a))
            p.ps_angle = a
        self.play(FadeIn(table), LaggedStartMap(FadeIn, people, lag_ratio=0.15))

        # 오른쪽 기둥
        RIGHT_X = 4.4
        line_tag = note("in a line", 26, ACCENT).move_to([RIGHT_X, 2.2, 0])
        line_tex = Tex(R"4! = 24").set_color(ACCENT).scale(1.1)
        line_tex.next_to(line_tag, DOWN, buff=0.25)
        self.play(FadeIn(line_tag), Write(line_tex))
        self.wait(0.8)

        # ── 돌려도 같은 앉음: 네 번 돌리면 제자리
        rot_tag = note("rotate", 26, CALM).move_to([RIGHT_X, 0.55, 0])
        self.play(FadeIn(rot_tag))

        snaps = VGroup()
        order = list(self.names)
        for i in range(4):
            snap = self.mini(order, CALM if i == 0 else MUTED)
            snap.move_to([-5.4 + 1.5 * i, -3.0, 0])
            snaps.add(snap)
            self.play(FadeIn(snap), run_time=0.4)
            if i < 3:
                self.rotate_once(people, center)
                order = [order[-1]] + order[:-1]     # 시계 방향으로 한 칸
        self.wait(0.3)

        box = panel(snaps, CALM, buff=0.18)
        same = note("same neighbors", 24, CALM).next_to(box, RIGHT, buff=0.3)
        self.play(ShowCreation(box), FadeIn(same))
        self.rotate_once(people, center, run_time=1.0)   # 네 번째 회전으로 제자리
        self.wait(0.4)

        rot_tex = Tex(R"\frac{4!}{4} = 6").set_color(CALM).scale(1.1)
        rot_tex.next_to(rot_tag, DOWN, buff=0.25)
        self.play(TransformFromCopy(line_tex, rot_tex), run_time=1.2)
        self.wait(1.0)

        # ── 같은 6 을 다른 길로: A 를 고정하고 나머지 셋만 세운다
        self.play(FadeOut(box), FadeOut(same), FadeOut(snaps), run_time=0.5)
        fix_tag = note("fix A", 26, MEAN_COLOR).move_to([RIGHT_X, -1.1, 0])
        pin = ring(people[0], MEAN_COLOR, buff=0.08)
        self.play(FadeIn(fix_tag), ShowCreation(pin))
        self.wait(0.3)

        # 나머지 셋이 자리를 바꾼다 (B→C 자리, C→D 자리, D→B 자리)
        b, c, d = people[1], people[2], people[3]
        pb, pc, pd = b.get_center(), c.get_center(), d.get_center()
        self.play(b.animate.move_to(pc), c.animate.move_to(pd), d.animate.move_to(pb),
                  run_time=1.0)
        self.wait(0.3)

        grid = VGroup(*[
            self.mini(["A"] + list(perm), MUTED, fixed="A")
            for perm in _it.permutations(["B", "C", "D"])
        ])
        for i, g in enumerate(grid):
            g.move_to([-5.9 + 1.45 * i, -3.0, 0])
        n_fix = ValueTracker(0)
        fix_num = counter(n_fix, color=MEAN_COLOR, size=56)
        fix_num.next_to(fix_tag, DOWN, buff=0.2)
        self.add(fix_num)
        self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.2),
                  n_fix.animate.set_value(6), run_time=1.8)
        freeze(fix_num)
        self.wait(0.4)

        fix_tex = Tex(R"3! = 6").set_color(MEAN_COLOR).scale(1.1)
        fix_tex.move_to(fix_num)
        self.play(FadeOut(fix_num), run_time=0.3)
        self.play(FadeIn(fix_tex), run_time=0.3)
        self.wait(0.6)

        # ── 두 길이 만난다
        final = Tex(R"(n-1)!").set_color(MEAN_COLOR).scale(1.3)
        final.next_to(fix_tex, DOWN, buff=0.55).set_x(RIGHT_X)
        self.play(TransformFromCopy(VGroup(rot_tex, fix_tex), final), run_time=1.3)
        self.play(FlashAround(final, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ═════════════════════════════════════════════════════════════
# 예제 영상 — 문제 슬라이드 다음, 풀이 슬라이드 앞에 놓인다 (하네스 3.6).
# 개념 영상이 개요를 주고 나면 슬라이드가 문제를 읽히고, 그 다음에 이 영상이 푼다.
# 소재는 교재 예제 그대로이고 씬 이름에 예제 번호를 넣는다.
# ═════════════════════════════════════════════════════════════

def small_chip(text, size=0.5, color=INK):
    """작은 카드. 게임팩·카드 같은 물건 하나."""
    return letter_chip(text, size, color)


# ─────────────────────────────────────────────────────────────
# Example 2.13 — 주사위 두 개, 6 × 6 = 36. 원본 13 뒤 (풀이 14 앞)
# ─────────────────────────────────────────────────────────────
class Example213Dice(InteractiveScene):
    """주사위 두 개의 표본공간을 6 × 6 격자로 채워 36 을 세게 한다.
    축의 눈금을 숫자 대신 주사위 면으로 그려서 격자 한 칸이 결과 하나임을 보인다.
    """

    def construct(self):
        head = slide_title("Example 2.13")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        d1 = die_face(3, 0.9, ACCENT)
        d2 = die_face(5, 0.9, CALM)
        pair = Group(d1, d2).arrange(RIGHT, buff=0.45).move_to(np.array([3.5, 2.3, 0]))
        qmark = Tex("?").scale(1.9).set_color(MEAN_COLOR).next_to(pair, RIGHT, buff=0.55)
        self.play(FadeIn(pair, scale=0.7), FadeIn(qmark))
        self.wait(0.4)

        cells = VGroup(*[Square(side_length=0.62).set_stroke(GREY_C, 1.5).set_fill(ACCENT, 0.0)
                         for _ in range(36)])
        cells.arrange_in_grid(6, 6, buff=0.07).move_to(DOWN * 0.55 + LEFT * 2.2)
        first = VGroup(*[die_face(i + 1, 0.46, ACCENT) for i in range(6)])
        second = VGroup(*[die_face(j + 1, 0.46, CALM) for j in range(6)])
        for i, t in enumerate(first):
            t.next_to(cells[i * 6], LEFT, buff=0.24)
        for j, t in enumerate(second):
            t.next_to(cells[j], UP, buff=0.24)
        self.play(ShowCreation(cells, lag_ratio=0.01, run_time=1.3))
        self.play(LaggedStartMap(FadeIn, first, lag_ratio=0.08),
                  LaggedStartMap(FadeIn, second, lag_ratio=0.08), run_time=1.2)
        self.wait(0.3)

        filled = ValueTracker(0)
        num = counter(filled, size=80).move_to(np.array([3.9, 0.3, 0]))
        tag = note("outcomes", 28, MEAN_COLOR).next_to(num, DOWN, buff=0.25)
        self.add(num)
        self.play(FadeIn(tag))
        rows = [VGroup(*cells[i * 6:(i + 1) * 6]) for i in range(6)]
        for k, row in enumerate(rows):
            self.play(row.animate.set_fill(ACCENT, 0.35),
                      filled.animate.set_value(6 * (k + 1)), run_time=0.45)
        self.wait(0.5)

        n1 = Brace(first, LEFT)
        n1_tex = Tex("n_1 = 6").set_color(ACCENT).scale(0.75).next_to(n1, LEFT, buff=0.15)
        n2 = Brace(second, UP)
        n2_tex = Tex("n_2 = 6").set_color(CALM).scale(0.75).next_to(n2, UP, buff=0.15)
        self.play(GrowFromCenter(n1), FadeIn(n1_tex), GrowFromCenter(n2), FadeIn(n2_tex))
        answer = Tex(R"n_1 \times n_2 = 6 \times 6 = 36").set_color(MEAN_COLOR)
        answer.scale(0.9).next_to(cells, DOWN, buff=0.55)
        self.play(FadeOut(qmark), Write(answer))
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.0)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.15 — 22 명 중 회장과 총무, 22 × 21 = 462. 원본 15 뒤 (풀이 16 앞)
# ─────────────────────────────────────────────────────────────
class Example215Club(InteractiveScene):
    """회장이 뽑혀 자리를 뜨면 남은 줄이 21 명으로 줄어드는 것을 보인다."""
    n_member = 22
    pick_chair = 7
    pick_treas = 15

    def construct(self):
        head = slide_title("Example 2.15")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        club = crowd(self.n_member, 2, 11, height=0.75, buff=0.2, seed=5)
        club.next_to(head[1], DOWN, buff=0.55)
        home = club.get_center()
        frame = panel(club, MUTED)
        n_pool = ValueTracker(0)
        pool_num = counter(n_pool, color=WHITE, size=60).next_to(frame, RIGHT, buff=0.45)
        self.add(pool_num)
        self.play(LaggedStartMap(FadeIn, club, lag_ratio=0.04),
                  n_pool.animate.set_value(self.n_member), FadeIn(frame), run_time=2.0)
        self.wait(0.5)

        seats = VGroup(*[RoundedRectangle(width=2.1, height=1.5, corner_radius=0.12).set_stroke(c, 2.5)
                         for c in (ACCENT, CALM)])
        seats.arrange(RIGHT, buff=2.0).next_to(frame, DOWN, buff=1.1).set_x(-1.0)
        seat_tags = VGroup(note("chair", 26, ACCENT).next_to(seats[0], UP, buff=0.15),
                           note("treasurer", 26, CALM).next_to(seats[1], UP, buff=0.15))
        self.play(ShowCreation(seats), FadeIn(seat_tags))

        chair = club[self.pick_chair]
        mark = ring(chair, ACCENT)
        self.play(ShowCreation(mark))
        new_chair = chito("front", "gold", 1.15).move_to(seats[0])
        self.play(FadeOut(mark), FadeOut(chair, scale=0.5), FadeIn(new_chair, scale=1.4),
                  n_pool.animate.set_value(self.n_member - 1), run_time=1.2)
        n1 = Tex("n_1 = 22").set_color(ACCENT).scale(0.9).next_to(seats[0], DOWN, buff=0.3)
        self.play(FadeIn(n1))
        self.wait(0.6)

        rest = Group(*[m for i, m in enumerate(club) if i != self.pick_chair])
        rest.generate_target()
        rest.target.arrange_in_grid(2, 11, buff=0.2).move_to(home)
        new_frame = panel(rest.target, MUTED)
        self.play(MoveToTarget(rest), Transform(frame, new_frame), run_time=1.2)
        self.play(FlashAround(pool_num, color=CALM), run_time=1.0)
        self.wait(0.4)

        treas = rest[self.pick_treas]
        mark2 = ring(treas, CALM)
        self.play(ShowCreation(mark2))
        new_treas = chito("front", "teal", 1.15).move_to(seats[1])
        self.play(FadeOut(mark2), FadeOut(treas, scale=0.5), FadeIn(new_treas, scale=1.4), run_time=1.2)
        n2 = Tex("n_2 = 21").set_color(CALM).scale(0.9).next_to(seats[1], DOWN, buff=0.3)
        self.play(FadeIn(n2))
        self.wait(0.6)

        answer = Tex(R"22 \times 21 = 462").set_color(MEAN_COLOR).scale(1.15)
        answer.next_to(seats, RIGHT, buff=1.0).set_y(seats.get_y())
        self.play(TransformFromCopy(VGroup(n1, n2), answer), run_time=1.4)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.25), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.18 — 대학원생 25 명에게 서로 다른 상 셋, 25 × 24 × 23. 원본 19 뒤 (풀이 20 앞)
# ─────────────────────────────────────────────────────────────
class Example218Awards(InteractiveScene):
    """상이 서로 다르므로 누가 어느 상을 받느냐가 결과를 바꾼다. 한 사람이 뽑혀 나갈 때마다
    줄이 하나씩 줄고 자리 아래 숫자가 25, 24, 23 으로 내려간다. 곱하면 ₂₅P₃ 이다."""
    n_student = 25
    picks = [4, 11, 20]                      # 원래 줄의 색인

    def construct(self):
        head = slide_title("Example 2.18")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        cls = crowd(self.n_student, 3, 9, height=0.6, buff=0.15, seed=3)
        cls.next_to(head[1], DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        frame = panel(cls, MUTED)
        n_pool = ValueTracker(0)
        pool_num = counter(n_pool, color=WHITE, size=60).next_to(frame, RIGHT, buff=0.5)
        self.add(pool_num)
        self.play(LaggedStartMap(FadeIn, cls, lag_ratio=0.03),
                  n_pool.animate.set_value(self.n_student), FadeIn(frame), run_time=1.8)

        names = ["research", "teaching", "service"]
        colors = [ACCENT, CALM, MEAN_COLOR]
        tints = ["teal", "gold", "red"]
        seats = VGroup(*[RoundedRectangle(width=1.7, height=1.35, corner_radius=0.12).set_stroke(c, 2.5)
                         for c in colors])
        seats.arrange(RIGHT, buff=1.1).next_to(frame, DOWN, buff=1.0).set_x(-1.6)
        seat_tags = VGroup(*[note(n, 24, c).next_to(s, UP, buff=0.12)
                             for n, c, s in zip(names, colors, seats)])
        self.play(ShowCreation(seats), FadeIn(seat_tags))

        counts = VGroup()
        for k, (idx, seat, color, tint) in enumerate(zip(self.picks, seats, colors, tints)):
            person = cls[idx]
            mark = ring(person, color)
            self.play(ShowCreation(mark), run_time=0.5)
            winner = chito("front", tint, 1.0).move_to(seat)
            cnt = Integer(self.n_student - k).set_color(color).scale(1.05).next_to(seat, DOWN, buff=0.25)
            self.play(FadeOut(mark), FadeOut(person, scale=0.5), FadeIn(winner, scale=1.4), FadeIn(cnt),
                      n_pool.animate.set_value(self.n_student - k - 1), run_time=1.0)
            counts.add(cnt)
            self.wait(0.4)

        answer = Tex(R"{}_{25}P_{3} = 25 \times 24 \times 23 = 13{,}800").set_color(MEAN_COLOR)
        answer.scale(1.0).move_to([-1.6, -3.25, 0])
        self.play(TransformFromCopy(counts, answer), run_time=1.4)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.22 — 아케이드 10 개 중 3, 스포츠 5 개 중 2. 원본 25 뒤 (풀이 26 앞)
# ─────────────────────────────────────────────────────────────
class Example222Cartridges(InteractiveScene):
    """고르는 순서는 무의미하므로 조합이다. 두 무리에서 따로 고르고 곱의 법칙으로 묶는다."""

    def construct(self):
        head = slide_title("Example 2.22")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        arcade = VGroup(*[small_chip("A", 0.55, ACCENT) for _ in range(10)])
        arcade.arrange_in_grid(2, 5, buff=0.14).move_to([-3.4, 1.7, 0])
        sports = VGroup(*[small_chip("S", 0.55, CALM) for _ in range(5)])
        sports.arrange(RIGHT, buff=0.14).move_to([2.8, 2.0, 0])
        a_box = panel(arcade, ACCENT, buff=0.2)
        s_box = panel(sports, CALM, buff=0.2)
        a_tag = note("10 arcade", 24, ACCENT).next_to(a_box, UP, buff=0.12)
        s_tag = note("5 sports", 24, CALM).next_to(s_box, UP, buff=0.12)
        self.play(LaggedStartMap(FadeIn, arcade, lag_ratio=0.05), FadeIn(a_box), FadeIn(a_tag),
                  LaggedStartMap(FadeIn, sports, lag_ratio=0.08), FadeIn(s_box), FadeIn(s_tag), run_time=1.4)

        bag = RoundedRectangle(width=4.2, height=1.3, corner_radius=0.15).set_stroke(MEAN_COLOR, 2.5)
        bag.move_to([-0.3, -1.0, 0])
        bag_tag = note("5 cartridges, unordered", 24, MEAN_COLOR).next_to(bag, UP, buff=0.12)
        self.play(ShowCreation(bag), FadeIn(bag_tag))

        # 아케이드 3 개
        pick_a = [1, 4, 7]
        marks = VGroup(*[ring(arcade[i], ACCENT, buff=0.05) for i in pick_a])
        self.play(ShowCreation(marks))
        moved_a = VGroup(*[arcade[i].copy() for i in pick_a])
        self.play(FadeOut(marks),
                  *[m.animate.move_to(bag.get_center() + LEFT * (1.3 - 0.65 * k)) for k, m in enumerate(moved_a)],
                  run_time=1.0)
        c_a = Tex(R"\binom{10}{3} = 120").set_color(ACCENT).scale(0.95)
        c_a.next_to(a_box, DOWN, buff=0.35)
        self.play(Write(c_a))
        self.wait(0.6)

        # 스포츠 2 개
        pick_s = [0, 3]
        marks = VGroup(*[ring(sports[i], CALM, buff=0.05) for i in pick_s])
        self.play(ShowCreation(marks))
        moved_s = VGroup(*[sports[i].copy() for i in pick_s])
        self.play(FadeOut(marks),
                  *[m.animate.move_to(bag.get_center() + RIGHT * (0.95 + 0.65 * k)) for k, m in enumerate(moved_s)],
                  run_time=1.0)
        c_s = Tex(R"\binom{5}{2} = 10").set_color(CALM).scale(0.95)
        c_s.next_to(s_box, DOWN, buff=0.35)
        self.play(Write(c_s))
        self.wait(0.6)

        answer = Tex(R"\binom{10}{3} \binom{5}{2} = 120 \times 10 = 1{,}200").set_color(MEAN_COLOR)
        answer.scale(1.0).next_to(bag, DOWN, buff=0.7)
        self.play(TransformFromCopy(VGroup(c_a, c_s), answer), run_time=1.3)
        self.play(FlashAround(answer, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.25 — 짝수가 두 배 잘 나오는 주사위. 원본 28 뒤 (풀이 29 앞)
# ─────────────────────────────────────────────────────────────
class Example225LoadedDie(InteractiveScene):
    """홀수에 w, 짝수에 2w 를 매기고 여섯 막대를 쌓으면 9w 가 1 이다. E = {1, 2, 3} 은
    w + 2w + w = 4w = 4/9. 등가능이 아니면 n/N 을 못 쓰고 무게를 직접 더한다."""

    def construct(self):
        head = slide_title("Example 2.25")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        faces = VGroup(*[die_face(i + 1, 0.6, GREY_A) for i in range(6)])
        faces.arrange(RIGHT, buff=0.55).move_to([-2.6, 1.55, 0])
        self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.1))

        H = 3.3
        base_y = -2.55
        units = [1, 2, 1, 2, 1, 2]
        bars = VGroup(*[bar(u, 9, width=0.6, height=H, color=(ACCENT if u == 2 else MUTED)) for u in units])
        for b, f in zip(bars, faces):
            b.move_to([f.get_x(), base_y + b.get_height() / 2, 0])
        wts = VGroup(*[Tex("2w" if u == 2 else "w").scale(0.8).set_color(ACCENT if u == 2 else GREY_B)
                       .next_to(b, UP, buff=0.12) for b, u in zip(bars, units)])
        base = Line(LEFT * 5.2, RIGHT * 0.1).set_stroke(GREY_C, 2).move_to([-2.6, base_y, 0])
        self.play(ShowCreation(base))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                  LaggedStartMap(FadeIn, wts, lag_ratio=0.1), run_time=1.2)
        self.wait(0.6)

        col_x = 2.4
        axis = Line(DOWN * H / 2, UP * H / 2).set_stroke(GREY_C, 2).move_to([col_x - 0.6, base_y + H / 2, 0])
        one = Tex("1").set_color(GREY_A).next_to(axis.get_top(), LEFT, buff=0.15)
        zero = Tex("0").set_color(GREY_A).next_to(axis.get_bottom(), LEFT, buff=0.15)
        self.play(ShowCreation(axis), FadeIn(one), FadeIn(zero))
        stack = bars.copy()
        y = base_y
        for b in stack:
            b.generate_target()
            b.target.move_to([col_x, y + b.get_height() / 2, 0])
            y += b.get_height()
        self.play(LaggedStartMap(MoveToTarget, stack, lag_ratio=0.12), run_time=1.5)
        eq1 = Tex(R"9w = 1").set_color(WHITE).next_to(stack, RIGHT, buff=0.5).set_y(base_y + H * 0.85)
        eq2 = Tex(R"w = \frac{1}{9}").set_color(WHITE).next_to(eq1, DOWN, buff=0.35).align_to(eq1, LEFT)
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.wait(1.0)

        # E = {1, 2, 3}
        self.play(FadeOut(stack), run_time=0.5)
        setup = Tex(R"E = \{1, 2, 3\}").scale(0.85).set_color(CALM)
        setup.next_to(head[1], DOWN, buff=0.25).to_edge(RIGHT, buff=0.7)
        self.play(FadeIn(setup, UP))
        idx = [0, 1, 2]
        marks = VGroup(*[ring(faces[i], CALM, buff=0.07) for i in idx])
        self.play(ShowCreation(marks),
                  *[bars[i].animate.set_fill(CALM, 0.85).set_stroke(CALM, 2) for i in idx],
                  *[wts[i].animate.set_color(CALM) for i in idx])
        sub = VGroup(*[bars[i].copy() for i in idx])
        y = base_y
        for b in sub:
            b.generate_target()
            b.target.move_to([col_x, y + b.get_height() / 2, 0])
            y += b.get_height()
        self.play(LaggedStartMap(MoveToTarget, sub, lag_ratio=0.15), run_time=1.3)
        pe = Tex(R"P(E) = w + 2w + w = \frac{4}{9}").set_color(CALM).scale(0.95)
        pe.move_to([1.4, -3.35, 0])
        self.play(Write(pe))
        self.play(FlashAround(pe, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.28 — 포커 5 장에 에이스 2 장, 잭 3 장. 원본 32 뒤 (풀이 33 앞)
# ─────────────────────────────────────────────────────────────
class Example228Poker(InteractiveScene):
    """분모를 조합으로 셌으면 분자도 조합으로 센다. 52 장을 4 × 13 격자로 깔고 에이스 열과
    잭 열만 살린 뒤, 거기서 2 장·3 장을 고른다."""
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def construct(self):
        head = slide_title("Example 2.28")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        cards = VGroup()
        for r in range(4):
            for c, rk in enumerate(self.ranks):
                col = ACCENT if rk == "A" else (CALM if rk == "J" else MUTED)
                cards.add(small_chip(rk, 0.42, col))
        cards.arrange_in_grid(4, 13, buff=0.08).move_to([-1.6, 1.4, 0])
        deck_box = panel(cards, MUTED, buff=0.2)
        self.play(LaggedStartMap(FadeIn, cards, lag_ratio=0.01), FadeIn(deck_box), run_time=1.6)

        N = Tex(R"N = \binom{52}{5} = 2{,}598{,}960").set_color(WHITE).scale(0.9)
        N.next_to(deck_box, DOWN, buff=0.4).align_to(deck_box, LEFT)
        unord = note("5 cards, unordered", 24, GREY_B).next_to(N, RIGHT, buff=0.6)
        self.play(Write(N), FadeIn(unord))
        self.wait(0.8)

        aces = VGroup(*[cards[r * 13 + 0] for r in range(4)])
        jacks = VGroup(*[cards[r * 13 + 10] for r in range(4)])
        others = VGroup(*[m for m in cards if m not in aces and m not in jacks])
        self.play(others.animate.set_opacity(0.15), run_time=0.8)

        ma = VGroup(ring(aces[0], ACCENT, buff=0.04), ring(aces[2], ACCENT, buff=0.04))
        mj = VGroup(*[ring(jacks[i], CALM, buff=0.04) for i in (0, 1, 3)])
        ca = Tex(R"\binom{4}{2} = 6").set_color(ACCENT).scale(0.9)
        cj = Tex(R"\binom{4}{3} = 4").set_color(CALM).scale(0.9)
        ca.next_to(aces, LEFT, buff=0.5)
        cj.next_to(jacks, RIGHT, buff=0.5)
        if ca.get_left()[0] < -6.9:
            ca.next_to(aces, DOWN, buff=1.4)
        self.play(ShowCreation(ma), Write(ca))
        self.wait(0.4)
        self.play(ShowCreation(mj), Write(cj))
        self.wait(0.6)

        n = Tex(R"n = 6 \times 4 = 24").set_color(MEAN_COLOR).scale(0.9)
        n.next_to(N, DOWN, buff=0.35).align_to(N, LEFT)
        self.play(TransformFromCopy(VGroup(ca, cj), n), run_time=1.2)
        self.wait(0.5)

        P = Tex(R"P = \frac{24}{2{,}598{,}960} = \frac{1}{108{,}290} \approx 9.23 \times 10^{-6}")
        P.set_color(WHITE).scale(0.9).next_to(n, DOWN, buff=0.4).align_to(N, LEFT)
        self.play(Write(P))
        self.play(FlashAround(P, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.29 — 두 회사 합격, 0.8 + 0.6 − 0.5 = 0.9. 원본 36 뒤 (풀이 37 앞)
# ─────────────────────────────────────────────────────────────
class Example229Jobs(InteractiveScene):
    """벤 다이어그램에 세 조각의 확률을 직접 적는다. 겹친 0.5 를 두 번 더했으므로 한 번 뺀다."""

    def construct(self):
        head = slide_title("Example 2.29")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        given = Tex(R"P(A) = 0.8, \quad P(B) = 0.6, \quad P(A \cap B) = 0.5",
                    t2c={"P(A)": ACCENT, "P(B)": CALM, R"P(A \cap B)": MEAN_COLOR})
        given.scale(0.85).next_to(head[1], DOWN, buff=0.3)
        self.play(FadeIn(given, UP))

        cA = Circle(radius=1.7).move_to(LEFT * 1.05 + DOWN * 0.1).set_stroke(ACCENT, 3)
        cB = Circle(radius=1.7).move_to(RIGHT * 1.05 + DOWN * 0.1).set_stroke(CALM, 3)
        only_a = Difference(cA, cB).set_stroke(width=0).set_fill(ACCENT, 0.3)
        lens = Intersection(cA, cB).set_stroke(width=0).set_fill(MEAN_COLOR, 0.45)
        only_b = Difference(cB, cA).set_stroke(width=0).set_fill(CALM, 0.3)
        tA = Tex("A").set_color(ACCENT).next_to(cA, UP, buff=0.1).shift(LEFT * 0.9)
        tB = Tex("B").set_color(CALM).next_to(cB, UP, buff=0.1).shift(RIGHT * 0.9)
        self.play(ShowCreation(cA), FadeIn(tA), ShowCreation(cB), FadeIn(tB))

        # 겹침 0.5 → A 만 0.3 → B 만 0.1
        mid = Tex("0.5").set_color(WHITE).move_to((cA.get_center() + cB.get_center()) / 2)
        left = Tex("0.3").set_color(WHITE).move_to(cA.get_center() + LEFT * 0.86)
        right = Tex("0.1").set_color(WHITE).move_to(cB.get_center() + RIGHT * 0.86)
        self.play(FadeIn(lens), FadeIn(mid))
        self.wait(0.5)
        sa = Tex(R"0.8 - 0.5 = 0.3").set_color(ACCENT).scale(0.8).next_to(cA, LEFT, buff=0.4)
        self.play(FadeIn(only_a), FadeIn(sa))
        self.play(TransformFromCopy(sa, left), run_time=0.8)
        self.wait(0.4)
        sb = Tex(R"0.6 - 0.5 = 0.1").set_color(CALM).scale(0.8).next_to(cB, RIGHT, buff=0.4)
        self.play(FadeIn(only_b), FadeIn(sb))
        self.play(TransformFromCopy(sb, right), run_time=0.8)
        self.wait(0.6)

        total = Tex(R"P(A \cup B) = 0.3 + 0.5 + 0.1 = 0.9").set_color(WHITE).scale(0.95)
        total.next_to(cA, DOWN, buff=0.55).set_x(0)
        self.play(TransformFromCopy(VGroup(left, mid, right), total), run_time=1.2)
        self.wait(0.6)
        formula = Tex(R"P(A) + P(B) - P(A \cap B) = 0.8 + 0.6 - 0.5 = 0.9",
                      t2c={"P(A)": ACCENT, "P(B)": CALM, R"P(A \cap B)": MEAN_COLOR})
        formula.scale(0.9).next_to(total, DOWN, buff=0.35)
        self.play(Write(formula))
        self.play(FlashAround(formula, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# Example 2.33 — 케이블 길이 2000 ± 10, 규격 안 0.99. 원본 40 뒤 (풀이 41 앞)
# ─────────────────────────────────────────────────────────────
class Example233Cable(InteractiveScene):
    """수직선에 규격 구간을 놓고 양쪽 꼬리를 대칭으로 나눈다. (a) 너무 긴 쪽 0.005,
    (b) 1990 보다 긴 것은 규격 안과 긴 쪽을 합쳐 0.995."""

    def construct(self):
        head = slide_title("Example 2.33")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        L, R_ = -5.5, 5.5
        line = Line([L, 0.3, 0], [R_, 0.3, 0]).set_stroke(GREY_B, 3)
        xs = {1990: -2.4, 2000: 0.0, 2010: 2.4}
        ticks = VGroup(*[Line(UP * 0.15, DOWN * 0.15).set_stroke(GREY_B, 3).move_to([x, 0.3, 0]) for x in xs.values()])
        nums = VGroup(*[Tex(str(v)).scale(0.75).set_color(GREY_A).next_to(t, DOWN, buff=0.2)
                        for v, t in zip(xs, ticks)])
        unit = note("mm", 22, GREY_B).next_to(line, RIGHT, buff=0.15)
        self.play(ShowCreation(line), ShowCreation(ticks), FadeIn(nums), FadeIn(unit))

        def band(x0, x1, color, op=0.35):
            r = Rectangle(width=x1 - x0, height=0.9).set_stroke(width=0).set_fill(color, op)
            return r.move_to([(x0 + x1) / 2, 0.3, 0])

        M = band(xs[1990], xs[2010], CALM)
        S = band(L, xs[1990], WARN)
        Lg = band(xs[2010], R_, WARN)
        mt = Tex(R"P(M) = 0.99").set_color(CALM).scale(0.85).next_to(M, UP, buff=0.35)
        self.play(FadeIn(M), Write(mt))
        self.wait(0.5)
        st = Tex(R"P(S) = 0.005").set_color(WARN).scale(0.8).next_to(S, UP, buff=0.35)
        lt = Tex(R"P(L) = 0.005").set_color(WARN).scale(0.8).next_to(Lg, UP, buff=0.35)
        rest = Tex(R"1 - 0.99 = 0.01", t2c={"0.01": WARN}).scale(0.85).move_to([0, -1.4, 0])
        half = Tex(R"0.01 / 2 = 0.005", t2c={"0.005": WARN}).scale(0.85).next_to(rest, DOWN, buff=0.25)
        self.play(FadeIn(S), FadeIn(Lg), Write(rest))
        self.play(Write(half))
        self.play(FadeIn(st), FadeIn(lt))
        self.wait(0.8)

        # (a) 너무 긴 쪽
        a = Tex(R"\text{(a)}\ P(L) = 0.005").set_color(WARN).scale(0.95).move_to([-3.6, -1.7, 0])
        self.play(FadeOut(rest), FadeOut(half), Lg.animate.set_fill(WARN, 0.7), Write(a))
        self.wait(0.8)
        self.play(Lg.animate.set_fill(WARN, 0.35))

        # (b) 1990 보다 긴 것 = M ∪ L
        cover = band(xs[1990], R_, MEAN_COLOR, 0.0).set_stroke(MEAN_COLOR, 3)
        b = Tex(R"\text{(b)}\ P(X > 1990) = P(M) + P(L) = 0.995",
                t2c={"P(M)": CALM, "P(L)": WARN}).scale(0.95).move_to([0.4, -2.9, 0])
        self.play(ShowCreation(cover), Write(b))
        self.play(FlashAround(b, color=MEAN_COLOR, buff=0.2), run_time=1.2)
        self.wait(2)
