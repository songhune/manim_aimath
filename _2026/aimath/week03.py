"""AI기초수학 — 교재 Chapter 2 가우스-조르당 소거법.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 02_가우스-조르당 소거법과 여러 가지 행렬.pptx`
의 2.1 가우스-조르당 소거법 · 2.2 역행렬에 붙는 보조 영상.
행 연산 순서와 각 단계의 수는 교재 예제 2-1 · 2-3 · 2-4 를 그대로 따른다.
행 연산 세 가지와 행 사다리꼴 판별은 Chapter 1 내용이므로 week02.py 에 둔다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week03.py
    ./render.sh check _2026/aimath/week03.py
    ./render.sh ppt   _2026/aimath/week03.py GaussJordan
    ./render.sh all   _2026/aimath/week03.py
"""
import re

from manim_imports_ext import *


TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"

INK = GREY_A
ACCENT = BLUE_B
CALM = TEAL_B
WARN = RED_C
DONE = YELLOW


MAX_WORDS = 6          # 하네스 3.6 — 화면에 남는 문구는 여섯 낱말까지
_PUNCT_ONLY = re.compile(r"^[·・,.:;=+\-—~/()\[\]{}<>|]+$")


def screen_words(text):
    """세는 낱말. 숫자가 든 낱말과 기호만 있는 토막은 빼고 센다."""
    out = []
    for word in text.replace("—", " ").split():
        if not word or _PUNCT_ONLY.match(word):
            continue
        if any(c.isdigit() for c in word):
            continue
        out.append(word)
    return out


def check_words(text):
    """화면 문구 길이만 빠르게 막는다(하네스 3.6의 뒷받침 규칙).

    **이것이 3.6 전부가 아니다.** 평가하는 수식어(`아주` `쉬운`)와 표어투
    (`…만 하면 끝`)는 짧아서 길이로는 걸리지 않으므로 여기서 보지 않는다.
    그 판정은 `_harness/harness_rules.py` 가 하고, `./render.sh` 가 렌더 전에
    불러 막는다. 여기는 손으로 씬을 돌릴 때 긴 문장을 바로 알아채라고 두는 것이다.
    """
    words = screen_words(text)
    if len(words) > MAX_WORDS:
        raise ValueError(
            "화면 문구가 %d낱말이다 (최대 %d): %r\n"
            "설명은 수업운영 메모로 옮기고 화면에는 이름만 남길 것."
            % (len(words), MAX_WORDS, text))
    return text


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def body(text, size=28, color=INK):
    check_words(text)
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def caption(text, size=26, color=GREY_B):
    """화면 문구. 명사구나 짧은 구절만 받는다(하네스 3.6).

    길이를 넘기면 렌더가 여기서 멈춘다. 설명이 길어졌다는 것은 그 설명이 화면이
    아니라 수업운영 메모로 갈 것이라는 뜻이다. 확률과통계의 `ps_common.label()`
    과 같은 장치이며, 판정의 원본은 `_harness/harness_rules.py` 다.
    """
    words = screen_words(text)
    if len(words) > MAX_WORDS:
        raise ValueError(
            "화면 문구가 %d낱말이다 (최대 %d): %r\n"
            "설명은 수업운영 메모로 옮기고 화면에는 이름만 남길 것."
            % (len(words), MAX_WORDS, text))
    check_words(text)
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def code(text, size=24, color=CALM):
    """화면에 놓는 코드 한 줄.

    코드는 자막이 아니다. 하네스 3.6 은 `caption()`·`body()` 만 문구로 보는데,
    여기는 학생이 그대로 받아 칠 줄이므로 낱말 수로 재면 안 된다. 대신 강의자료
    파이썬 코드와 **글자 하나까지 같아야** 한다.
    """
    # 앞 공백은 글자가 아니라서 arrange 가 무시한다. 들여쓰기 깊이만 기억해 두고
    # `code_block()` 이 자리를 잡을 때 그만큼 오른쪽으로 민다.
    stripped = text.lstrip(" ")
    mob = Text(stripped, font="D2Coding", font_size=size).set_color(color)
    mob.indent = len(text) - len(stripped)
    return mob


def code_block(lines, size=20, buff=0.22, step=0.36):
    """코드 여러 줄. 파이썬에서 들여쓰기는 구조 그 자체이므로 반드시 살린다.

    `arrange(aligned_edge=LEFT)` 는 각 줄의 첫 글자에 맞춰 정렬해 공백을 지운다.
    정렬한 뒤 줄마다 들여쓰기 깊이(공백 4개 = 한 단계)만큼 오른쪽으로 민다.
    """
    group = VGroup(*[code(t, size) for t in lines])
    group.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    for line in group:
        line.shift(RIGHT * step * (line.indent / 4))
    return group


def slide_title(text):
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def mat(values, color=WHITE, h_buff=0.85, v_buff=0.6):
    m = Matrix(values, h_buff=h_buff, v_buff=v_buff, bracket_h_buff=0.15)
    m.set_color(color)
    return m


def augmented(values, split, color=WHITE, h_buff=0.85, v_buff=0.6):
    """계수 부분과 상수 부분을 세로선으로 가른 첨가행렬."""
    m = mat(values, color, h_buff, v_buff)
    left = m.get_columns()[split - 1]
    right = m.get_columns()[split]
    x = 0.5 * (left.get_right()[0] + right.get_left()[0])
    bar = Line(UP, DOWN).set_stroke(GREY_C, 2)
    bar.set_height(m.get_height() * 0.82)
    bar.move_to(np.array([x, m.get_center()[1], 0]))
    group = VGroup(m, bar)
    group.matrix = m
    return group


def box(mobject, color=WARN, buff=0.12):
    return SurroundingRectangle(mobject, buff=buff).set_stroke(color, 3)


def op_label(lines, color=CALM):
    """행 연산 표기. 한 단계에 두 줄까지 붙는다."""
    group = VGroup(*[caption(line, 26, color) for line in lines])
    group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    return group


# ─────────────────────────────────────────────────────────────
# 1. 가우스-조르당 소거법 — 교재 예제 2-1
# ─────────────────────────────────────────────────────────────
class GaussJordan(InteractiveScene):
    """첨가행렬을 기약 행 사다리꼴까지 밀고, 마지막 열에서 해를 읽는다.

    단계와 수는 교재 예제 2-1 과 같다. 정지 화면으로는 여섯 개의 행렬이
    나란히 놓일 뿐이지만, 한 자리에서 값이 바뀌면 어느 성분이 0 이 되는지 보인다.
    """
    start = [[1, 3, 2, 2], [2, 2, 0, 0], [-3, 1, 1, -2]]
    steps = [
        (["2행 → 2행 - 2 × 1행", "3행 → 3행 + 3 × 1행"],
         [[1, 3, 2, 2], [0, -4, -4, -4], [0, 10, 7, 4]], [1, 2], 0, None),
        (["2행 → 2행 × (-1/4)"],
         [[1, 3, 2, 2], [0, 1, 1, 1], [0, 10, 7, 4]], [1], 1, None),
        (["3행 → 3행 - 10 × 2행"],
         [[1, 3, 2, 2], [0, 1, 1, 1], [0, 0, -3, -6]], [2], 1, None),
        (["3행 → 3행 × (-1/3)"],
         [[1, 3, 2, 2], [0, 1, 1, 1], [0, 0, 1, 2]], [2], 2, "행 사다리꼴"),
        (["1행 → 1행 - 2 × 3행", "2행 → 2행 - 3행"],
         [[1, 3, 0, -2], [0, 1, 0, -1], [0, 0, 1, 2]], [0, 1], 2, None),
        (["1행 → 1행 - 3 × 2행"],
         [[1, 0, 0, 1], [0, 1, 0, -1], [0, 0, 1, 2]], [0], 1,
         "기약 행 사다리꼴"),
    ]

    def construct(self):
        head = slide_title("가우스-조르당 소거법")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        group = augmented(self.start, 3, WHITE)
        group.move_to(2.9 * LEFT + 0.4 * DOWN)
        m = group.matrix
        self.play(FadeIn(group))

        stamp = VGroup()
        self.add(stamp)

        for lines, values, rows, pivot_col, tag in self.steps:
            label = op_label(lines)
            label.next_to(group, RIGHT, buff=1.3)

            column = box(m.get_columns()[pivot_col], ACCENT, 0.14)
            marks = VGroup(*[box(m.get_rows()[i], WARN, 0.13) for i in rows])

            self.play(ShowCreation(column), run_time=0.4)
            self.play(FadeIn(label, RIGHT), ShowCreation(marks), run_time=0.6)

            target = augmented(values, 3, WHITE).move_to(group)
            self.play(Transform(group, target), run_time=1.1)
            m = group[0]
            self.wait(0.4)

            if tag:
                new_stamp = caption(tag, 30, DONE)
                new_stamp.next_to(group, DOWN, buff=0.55)
                self.play(FadeOut(stamp), FadeIn(new_stamp, UP), run_time=0.6)
                stamp = new_stamp
                self.wait(0.8)

            self.play(FadeOut(label), FadeOut(marks), FadeOut(column),
                      run_time=0.4)

        answer = Tex("x_1 = 1,\; x_2 = -1,\; x_3 = 2").set_color(DONE)
        answer.next_to(group, RIGHT, buff=1.1)
        last_col = box(m.get_columns()[3], DONE, 0.14)
        self.play(ShowCreation(last_col))
        self.play(Write(answer))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 행 연산으로 구하는 역행렬 — 교재 예제 2-3
# ─────────────────────────────────────────────────────────────
class InverseByRowOps(InteractiveScene):
    """[A | I] 를 밀어 왼쪽이 I 가 되면 오른쪽에 남는 것이 역행렬이다."""
    start = [["2", "3", "1", "0"], ["5", "7", "0", "1"]]
    steps = [
        ([R"1행 → 1행 × 1/2"],
         [["1", R"\frac{3}{2}", R"\frac{1}{2}", "0"], ["5", "7", "0", "1"]],
         [0]),
        (["2행 → 2행 - 5 × 1행"],
         [["1", R"\frac{3}{2}", R"\frac{1}{2}", "0"],
          ["0", R"-\frac{1}{2}", R"-\frac{5}{2}", "1"]], [1]),
        (["2행 → 2행 × (-2)"],
         [["1", R"\frac{3}{2}", R"\frac{1}{2}", "0"], ["0", "1", "5", "-2"]],
         [1]),
        (["1행 → 1행 - 3/2 × 2행"],
         [["1", "0", "-7", "3"], ["0", "1", "5", "-2"]], [0]),
    ]

    def construct(self):
        head = slide_title("행 연산으로 구하는 역행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        group = augmented(self.start, 2, WHITE, h_buff=0.95, v_buff=0.75)
        group.move_to(3.1 * LEFT + 0.6 * DOWN)
        m = group.matrix
        bar_x = group[1].get_center()[0]

        # 상태마다 분수가 들어가 높이가 달라지므로, 표시는 고정된 높이에 둔다.
        tag_y = 1.95
        left_tag = caption("A", 30, ACCENT)
        right_tag = caption("I", 30, CALM)
        left_tag.move_to(np.array([0.5 * (m.get_left()[0] + bar_x), tag_y, 0]))
        right_tag.move_to(np.array([0.5 * (bar_x + m.get_right()[0]), tag_y, 0]))

        self.play(FadeIn(group), FadeIn(left_tag), FadeIn(right_tag))
        self.wait(0.5)

        for lines, values, rows in self.steps:
            label = op_label(lines)
            label.next_to(group, RIGHT, buff=1.4)
            marks = VGroup(*[box(m.get_rows()[i], WARN, 0.13) for i in rows])

            self.play(FadeIn(label, RIGHT), ShowCreation(marks), run_time=0.6)
            target = augmented(values, 2, WHITE, h_buff=0.95,
                               v_buff=0.75).move_to(group)
            self.play(FadeTransform(group, target), run_time=1.1)
            group = target
            m = group.matrix
            self.wait(0.4)
            self.play(FadeOut(label), FadeOut(marks), run_time=0.4)

        new_left = caption("I", 30, CALM).move_to(left_tag)
        new_right = caption("A 의 역행렬", 26, DONE)
        new_right.move_to(np.array([right_tag.get_center()[0], tag_y, 0]))
        self.play(Transform(left_tag, new_left),
                  Transform(right_tag, new_right))

        check = VGroup(
            Tex("A A^{-1} ="),
            Matrix([["1", "0"], ["0", "1"]], h_buff=0.8, v_buff=0.6),
        ).arrange(RIGHT, buff=0.3).set_color(DONE)
        check.next_to(group, RIGHT, buff=1.2)
        self.play(Write(check))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 첨가행렬 — 교재 2.1 절 정의
# ─────────────────────────────────────────────────────────────
class AugmentedMatrix(InteractiveScene):
    """연립방정식의 계수와 상수가 첨가행렬의 어느 자리로 가는지 본다."""

    def construct(self):
        head = slide_title("첨가행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        system = VGroup(*[Tex(line) for line in (
            R"x_1 + 3x_2 + 2x_3 = 2",
            R"2x_1 + 2x_2 + 0x_3 = 0",
            R"-3x_1 + x_2 + x_3 = -2",
        )])
        system.arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        system.to_edge(LEFT, buff=1.1).shift(0.3 * DOWN)
        self.play(LaggedStartMap(FadeIn, system, lag_ratio=0.3))
        self.wait(0.6)

        coeff = mat([[1, 3, 2], [2, 2, 0], [-3, 1, 1]], ACCENT)
        const = mat([[2], [0], [-2]], DONE)
        pair = VGroup(coeff, const).arrange(RIGHT, buff=0.7)
        pair.to_edge(RIGHT, buff=1.4).shift(0.3 * DOWN)

        names = VGroup(caption("계수행렬", 24, ACCENT),
                       caption("상수벡터", 24, DONE))
        names[0].next_to(coeff, UP, buff=0.35)
        names[1].next_to(const, UP, buff=0.35)

        self.play(TransformFromCopy(system, coeff), run_time=1.2)
        self.play(FadeIn(names[0]))
        self.wait(0.4)
        self.play(TransformFromCopy(system, const), run_time=1.0)
        self.play(FadeIn(names[1]))
        self.wait(0.8)

        joined = augmented([[1, 3, 2, 2], [2, 2, 0, 0], [-3, 1, 1, -2]], 3)
        joined.move_to(pair)
        self.play(FadeOut(names), FadeTransform(pair, joined), run_time=1.2)

        note = caption("계수는 왼쪽, 상수는 오른쪽", 26, GREY_B)
        note.next_to(joined, DOWN, buff=0.7)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 양말-신발 성질 — 교재 정리 2-4 (2)
# ─────────────────────────────────────────────────────────────
class SocksShoes(InteractiveScene):
    """정리 2-4 (2)  (AB)^{-1} = B^{-1}A^{-1}.

    강의자료의 정리 순서를 따른다. A 와 B 를 먼저 세우고, 각각의 역행렬을 보이고,
    그다음 곱의 역행렬이 순서를 뒤집은 곱과 같은지 수로 확인한다. A 는 예제 2-3 의 행렬이다.
    """
    A = [[2, 3], [5, 7]]; Ai = [[-7, 3], [5, -2]]
    B = [[1, 1], [2, 3]]; Bi = [[3, -1], [-2, 1]]
    AB = [[8, 11], [19, 26]]
    right = [[-26, 11], [19, -8]]      # (AB)^{-1} = B^{-1}A^{-1}
    wrong = [[-27, 10], [19, -7]]      # A^{-1}B^{-1}

    def construct(self):
        head = slide_title("양말-신발 성질")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = caption("정리 2-4 (2)", 24, GREY_B).next_to(head, DOWN, buff=0.25).align_to(head, LEFT)
        self.play(FadeIn(tag))

        def named(sym, values, color):
            g = VGroup(Tex(sym).set_color(color), mat(values, color, h_buff=0.9))
            return g.arrange(DOWN, buff=0.3)

        # A 와 B
        a_blk = named("A", self.A, ACCENT); b_blk = named("B", self.B, CALM)
        top = VGroup(a_blk, b_blk).arrange(RIGHT, buff=2.0).move_to(1.3 * UP)
        self.play(FadeIn(a_blk, UP), FadeIn(b_blk, UP), run_time=0.9)
        self.wait(0.6)

        # 각각의 역행렬
        ai_blk = named("A^{-1}", self.Ai, ACCENT); bi_blk = named("B^{-1}", self.Bi, CALM)
        bottom = VGroup(ai_blk, bi_blk).arrange(RIGHT, buff=2.0).move_to(1.5 * DOWN)
        self.play(FadeIn(ai_blk, UP), FadeIn(bi_blk, UP), run_time=0.9)
        note = caption("예제 2-3 의 행렬과 그 역행렬", 22, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note)); self.wait(1.0)
        self.play(FadeOut(VGroup(top, bottom, note)))

        # 정리의 식
        chain = Tex(R"(AB)^{-1} = B^{-1}A^{-1}").set_width(6.0).move_to(2.3 * UP)
        self.play(Write(chain), run_time=1.0); self.wait(0.5)

        good = VGroup(caption("순서를 지킨 곱", 22, DONE), Tex(R"B^{-1}A^{-1}").set_color(DONE),
                      mat(self.right, DONE, h_buff=1.1)).arrange(DOWN, buff=0.3)
        bad = VGroup(caption("지키지 않은 곱", 22, WARN), Tex(R"A^{-1}B^{-1}").set_color(WARN),
                     mat(self.wrong, WARN, h_buff=1.1)).arrange(DOWN, buff=0.3)
        ab = VGroup(Tex(R"(AB)^{-1}").set_color(GREY_A), mat(self.right, GREY_A, h_buff=1.1)).arrange(DOWN, buff=0.3)
        row = VGroup(ab, good, bad).arrange(RIGHT, buff=1.3).move_to(0.9 * DOWN)
        self.play(FadeIn(ab, UP), run_time=0.8); self.wait(0.5)
        self.play(FadeIn(good, UP), run_time=0.8); self.wait(0.6)
        same = box(VGroup(ab, good), DONE, 0.2)
        self.play(ShowCreation(same)); self.wait(0.8)
        self.play(FadeIn(bad, UP), run_time=0.8)
        marks = VGroup(*[box(bad[2].get_entries()[k], WARN, 0.1) for k in (0, 1, 3)])
        self.play(ShowCreation(marks))
        last = caption("세 자리가 다름", 24, WARN).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(last, UP)); self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 역행렬로 푸는 행렬방정식 — 교재 예제 2-6
# ─────────────────────────────────────────────────────────────
class InverseSolve(InteractiveScene):
    """x = A^{-1}b. 예제 2-1 을 소거법 대신 역행렬로 푼다.

    분모 12 를 앞으로 빼면 정수 행렬만 남아 암산으로 검산된다.
    그 12 는 A 의 행렬식이다(`Determinant3x3`).
    """
    adj = [[2, -1, -4], [-2, 7, 4], [8, -10, -4]]

    def construct(self):
        head = slide_title("역행렬로 푸는 행렬방정식")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        eq = Tex(R"A\mathbf{x} = \mathbf{b} \quad\Longrightarrow\quad "
                 R"\mathbf{x} = A^{-1}\mathbf{b}")
        eq.set_width(7.6).move_to(2.2 * UP)
        self.play(Write(eq), run_time=1.2)
        self.wait(0.8)

        frac = Tex(R"\frac{1}{12}").set_color(DONE)
        inv = mat(self.adj, WHITE, h_buff=1.0)
        b = mat([[2], [0], [-2]], ACCENT)
        row = VGroup(frac, inv, b).arrange(RIGHT, buff=0.35)
        row.move_to(0.6 * DOWN)
        self.play(FadeIn(row, UP), run_time=0.9)
        self.wait(0.8)

        product = mat([[12], [-12], [24]], WHITE)
        answer = mat([[1], [-1], [2]], DONE)
        eq2 = Tex("=")
        eq3 = Tex("=")

        stage = VGroup(row.copy(), eq2, VGroup(Tex(R"\frac{1}{12}").set_color(DONE),
                                               product).arrange(RIGHT, buff=0.3),
                       eq3, answer)
        stage.arrange(RIGHT, buff=0.45).set_width(11.6).move_to(0.6 * DOWN)

        self.play(Transform(row, stage[0]), run_time=0.8)
        self.play(FadeIn(stage[1]), FadeIn(stage[2], RIGHT), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(stage[3]), FadeIn(stage[4], RIGHT), run_time=1.0)

        note = caption("예제 2-1 과 같은 해", 28, DONE)
        note.next_to(stage, DOWN, buff=0.8)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 행렬식 (2x2) — 교재 정리 2-3 의 ad-bc 에 이름을 붙인다
# ─────────────────────────────────────────────────────────────
class Determinant2x2(InteractiveScene):
    """정리 2-3 의 분모 ad-bc 가 행렬식이다.

    교재는 이 수에 이름을 붙이지 않고 공식 안에만 둔다. 이름이 없으면
    2.2 절의 '역행렬이 존재하지 않는 경우'와 이어지지 않는다.
    수는 예제 2-3 의 행렬을 그대로 쓴다.

    **여기서는 이름과 계산까지만 한다.** 이 수가 무엇을 재는 수인지는
    `DeterminantGeometry` 가 맡는다. 공식을 외우는 것으로 끝나면 CH04 선형변환에서
    다시 만났을 때 같은 것인 줄 모른다.
    """
    values = [[2, 3], [5, 7]]

    def construct(self):
        head = slide_title("행렬식")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        symbol = mat([["a", "b"], ["c", "d"]], WHITE, h_buff=1.0)
        symbol.move_to(3.9 * LEFT + 0.7 * UP)
        self.play(FadeIn(symbol))
        self.wait(0.4)

        e = symbol.get_entries()
        down = Line(e[0].get_center(), e[3].get_center()).set_stroke(DONE, 4)
        up = Line(e[2].get_center(), e[1].get_center()).set_stroke(WARN, 4)
        self.play(ShowCreation(down))
        self.play(ShowCreation(up))

        formula = Tex(R"\det A = ad - bc")
        formula["ad"].set_color(DONE)
        formula["bc"].set_color(WARN)
        formula.set_width(5.2).next_to(symbol, RIGHT, buff=1.5)
        self.play(Write(formula), run_time=1.2)

        note = caption("두 대각선 곱의 차", 26, GREY_B)
        note.next_to(symbol, DOWN, buff=0.9).align_to(symbol, LEFT)
        self.play(FadeIn(note, UP))
        self.wait(1.2)
        self.play(FadeOut(note))

        # 예제 2-3 의 수로 확인한다.
        number = mat(self.values, WHITE, h_buff=1.0).move_to(symbol)
        self.play(FadeTransform(symbol, number),
                  FadeOut(down), FadeOut(up), run_time=0.9)
        ne = number.get_entries()
        down2 = Line(ne[0].get_center(), ne[3].get_center()).set_stroke(DONE, 4)
        up2 = Line(ne[2].get_center(), ne[1].get_center()).set_stroke(WARN, 4)
        self.play(ShowCreation(down2), ShowCreation(up2), run_time=0.6)

        value = Tex(R"2 \cdot 7 - 3 \cdot 5 = -1")
        value.set_width(5.2).move_to(formula).set_color(DONE)
        self.play(FadeTransform(formula, value), run_time=0.9)
        self.wait(0.8)

        inverse = Tex(R"A^{-1} = \frac{1}{\det A}"
                      R"\begin{bmatrix} d & -b \\ -c & a \end{bmatrix}")
        inverse.set_width(6.4).move_to(2.2 * DOWN)
        self.play(Write(inverse), run_time=1.4)
        mark = box(inverse[R"\det A"], DONE, 0.1)
        self.play(ShowCreation(mark))

        last = caption("정리 2-3 의 분모", 26, DONE)
        last.next_to(inverse, RIGHT, buff=0.9)
        self.play(FadeIn(last, LEFT))
        self.wait(1.4)

        bridge = caption("이 수가 무엇을 재는지는 다음 편", 24, GREY_B)
        bridge.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bridge, UP))
        self.wait(1.6)


# ─────────────────────────────────────────────────────────────
# 8. 행렬식이 0 인 경우 — 역행렬이 없다는 신호
# ─────────────────────────────────────────────────────────────
class DeterminantZero(InteractiveScene):
    """det = 0 과 '행 연산으로 밀면 영행이 생긴다'가 같은 신호임을 본다."""
    values = [[1, 2], [2, 4]]

    def construct(self):
        head = slide_title("행렬식이 0 인 행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        m = mat(self.values, WHITE, h_buff=1.0)
        m.move_to(3.7 * LEFT + 1.0 * UP)
        self.play(FadeIn(m))

        e = m.get_entries()
        down = Line(e[0].get_center(), e[3].get_center()).set_stroke(DONE, 4)
        up = Line(e[2].get_center(), e[1].get_center()).set_stroke(WARN, 4)
        self.play(ShowCreation(down), ShowCreation(up), run_time=0.6)

        value = Tex(R"1 \cdot 4 - 2 \cdot 2 = 0").set_color(WARN)
        value.set_width(4.6).next_to(m, RIGHT, buff=1.6)
        self.play(Write(value), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(down), FadeOut(up))

        # 같은 행렬을 행 연산으로 밀면 영행이 남는다.
        group = augmented([[1, 2, 1, 0], [2, 4, 0, 1]], 2, WHITE, h_buff=0.95)
        group.move_to(2.4 * LEFT + 1.3 * DOWN)
        self.play(FadeIn(group))

        label = op_label(["2행 → 2행 - 2 × 1행"])
        label.next_to(group, RIGHT, buff=1.3)
        self.play(FadeIn(label, RIGHT), run_time=0.6)

        target = augmented([[1, 2, 1, 0], [0, 0, -2, 1]], 2, WHITE,
                           h_buff=0.95).move_to(group)
        self.play(FadeTransform(group, target), run_time=1.1)
        group = target

        zero = box(group.matrix.get_rows()[1][:2], WARN, 0.14)
        self.play(ShowCreation(zero))
        tag = caption("영행", 26, WARN)
        tag.next_to(zero, DOWN, buff=0.35)
        self.play(FadeIn(tag, UP))
        self.wait(0.8)
        self.play(FadeOut(label))

        note = caption("행렬식이 0 이면 역행렬 없음", 28, WARN)
        note.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 행렬식 (3x3) — 사루스 법칙, 예제 2-4 의 행렬
# ─────────────────────────────────────────────────────────────
class Determinant3x3(InteractiveScene):
    """앞의 두 열을 오른쪽에 베껴 두고 대각선 여섯 줄을 읽는다.

    행렬은 예제 2-4(=예제 2-1 의 계수행렬)이고 det = 12 다. 그 12 가
    예제 2-4 에서 구한 역행렬의 분모와 같다. 이 장의 매듭이 여기다.
    """
    wide = [[1, 3, 2, 1, 3], [2, 2, 0, 2, 2], [-3, 1, 1, -3, 1]]
    downs = [(0, 2, 4, "1 \\cdot 2 \\cdot 1 = 2"),
             (1, 3, 5, "3 \\cdot 0 \\cdot (-3) = 0"),
             (2, 4, 6, "2 \\cdot 2 \\cdot 1 = 4")]

    def construct(self):
        head = slide_title("3차 정방행렬의 행렬식")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        m = mat(self.wide, WHITE, h_buff=0.85, v_buff=0.62)
        m.set_width(8.6).move_to(1.1 * UP)
        cols = m.get_columns()
        for col in cols[3:]:
            col.set_color(GREY_D)
        self.play(FadeIn(m))

        copied = caption("앞의 두 열을 베낌", 24, GREY_C)
        copied.next_to(VGroup(*cols[3:]), UP, buff=0.35)
        self.play(FadeIn(copied))
        self.wait(0.8)

        def diagonal(start_col, direction, color):
            pts = []
            for k in range(3):
                r = k if direction > 0 else 2 - k
                pts.append(m.get_rows()[r][start_col + k].get_center())
            line = Line(pts[0], pts[2]).set_stroke(color, 4)
            return line

        down_lines = VGroup(*[diagonal(c, +1, DONE) for c in range(3)])
        up_lines = VGroup(*[diagonal(c, -1, WARN) for c in range(3)])

        self.play(LaggedStartMap(ShowCreation, down_lines, lag_ratio=0.35),
                  run_time=1.4)
        down_sum = Tex(R"2 + 0 + 4 = 6").set_color(DONE)
        down_sum.move_to(1.55 * DOWN).shift(3.3 * LEFT)
        self.play(Write(down_sum), run_time=0.9)
        self.wait(0.8)

        self.play(LaggedStartMap(ShowCreation, up_lines, lag_ratio=0.35),
                  run_time=1.4)
        up_sum = Tex(R"-12 + 0 + 6 = -6").set_color(WARN)
        up_sum.move_to(1.55 * DOWN).shift(3.3 * RIGHT)
        self.play(Write(up_sum), run_time=0.9)
        self.wait(0.8)

        note = caption("아래 합에서 위 합을 뺀다", 26, GREY_B)
        note.move_to(2.55 * DOWN)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        result = Tex(R"\det A = 6 - (-6) = 12").set_color(DONE)
        result.set_width(6.2).move_to(2.55 * DOWN)
        self.play(FadeTransform(note, result), run_time=0.9)
        self.wait(1.2)

        self.play(FadeOut(down_lines), FadeOut(up_lines), FadeOut(copied),
                  FadeOut(down_sum), FadeOut(up_sum),
                  FadeOut(m), FadeOut(result.copy()), run_time=0.8)

        bridge = VGroup(
            Tex(R"\det A = 12").set_color(DONE),
            Tex(R"A^{-1} = \frac{1}{12}"
                R"\begin{bmatrix} 2 & -1 & -4 \\ -2 & 7 & 4 \\ 8 & -10 & -4"
                R"\end{bmatrix}"),
        ).arrange(RIGHT, buff=1.3)
        bridge.set_width(10.4).move_to(0.4 * UP)
        self.play(Transform(result, bridge[0]), FadeIn(bridge[1], RIGHT),
                  run_time=1.2)
        same = caption("예제 2-4 의 분모와 같은 수", 28, DONE)
        same.next_to(bridge, DOWN, buff=0.9)
        self.play(FadeIn(same, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 행렬식의 성질
# ─────────────────────────────────────────────────────────────
class DeterminantRules(InteractiveScene):
    """곱·역·전치에서 행렬식이 어떻게 되는지 수로 확인한다."""
    A = [[1, 2], [3, 4]]        # det = -2
    B = [[2, 0], [1, 3]]        # det = 6
    AB = [[4, 6], [10, 12]]     # det = -12

    def construct(self):
        head = slide_title("행렬식의 성질")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        row = VGroup(
            VGroup(mat(self.A, ACCENT, h_buff=0.9),
                   Tex(R"\det = -2").set_color(ACCENT)).arrange(DOWN, buff=0.35),
            VGroup(mat(self.B, CALM, h_buff=0.9),
                   Tex(R"\det = 6").set_color(CALM)).arrange(DOWN, buff=0.35),
            VGroup(mat(self.AB, DONE, h_buff=0.9),
                   Tex(R"\det = -12").set_color(DONE)).arrange(DOWN, buff=0.35),
        )
        row.arrange(RIGHT, buff=1.5).set_width(10.4).move_to(1.35 * UP)
        names = VGroup(caption("A", 24, ACCENT), caption("B", 24, CALM),
                       caption("AB", 24, DONE))
        for name, block in zip(names, row):
            name.next_to(block, UP, buff=0.3)

        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.4), FadeIn(names),
                  run_time=1.6)
        self.wait(1.0)

        rules = VGroup(
            Tex(R"\det(AB) = \det A \cdot \det B"),
            Tex(R"\det(A^{-1}) = \frac{1}{\det A}"),
            Tex(R"\det(A^{T}) = \det A"),
        )
        rules.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        rules.set_width(6.0).move_to(1.7 * DOWN).shift(2.6 * LEFT)

        checks = VGroup(
            Tex(R"-12 = (-2)(6)").set_color(DONE),
            Tex(R"-\tfrac{1}{2}").set_color(DONE),
            Tex(R"-2").set_color(DONE),
        )
        for rule, check in zip(rules, checks):
            check.next_to(rule, RIGHT, buff=1.1)

        for rule, check in zip(rules, checks):
            self.play(FadeIn(rule, RIGHT), run_time=0.7)
            self.play(FadeIn(check, LEFT), run_time=0.5)
            self.wait(0.4)

        note = caption("곱의 행렬식은 행렬식의 곱", 26, GREY_B)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 전치행렬의 성질 — 교재 정리 2-5 (3) (5)
# ─────────────────────────────────────────────────────────────
class TransposeRules(InteractiveScene):
    """정의 2-4 전치행렬 → 정리 2-5 (3) (AB)^T = B^T A^T → (5) (A^T)^{-1} = (A^{-1})^T.

    강의자료의 정의·정리 순서를 그대로 따른다. A 와 B 를 먼저 세우고 전치를 보인 뒤
    정리로 간다. (3) 은 수로 확인하고, 순서를 지키지 않은 곱과 견준다.
    """
    A = [[1, 2], [3, 4]]; At = [[1, 3], [2, 4]]
    B = [[2, 0], [1, 3]]; Bt = [[2, 1], [0, 3]]
    AB = [[4, 6], [10, 12]]; ABt = [[4, 10], [6, 12]]
    wrong = [[2, 10], [4, 14]]         # A^T B^T

    def construct(self):
        head = slide_title("전치행렬의 성질")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        def named(sym, values, color, h=0.9):
            g = VGroup(Tex(sym).set_color(color), mat(values, color, h_buff=h))
            return g.arrange(DOWN, buff=0.3)

        # 정의 2-4 — 행과 열을 바꾼 행렬
        tag = caption("정의 2-4 전치행렬", 24, GREY_B).next_to(head, DOWN, buff=0.25).align_to(head, LEFT)
        self.play(FadeIn(tag))
        a_blk = named("A", self.A, ACCENT); at_blk = named("A^{T}", self.At, ACCENT)
        b_blk = named("B", self.B, CALM); bt_blk = named("B^{T}", self.Bt, CALM)
        grid = VGroup(a_blk, at_blk, b_blk, bt_blk).arrange_in_grid(2, 2, buff=1.2)
        grid.set_height(4.6).move_to(0.4 * DOWN)
        self.play(FadeIn(a_blk), FadeIn(b_blk), run_time=0.8); self.wait(0.5)
        self.play(TransformFromCopy(a_blk, at_blk), run_time=1.0)
        self.play(TransformFromCopy(b_blk, bt_blk), run_time=1.0)
        rule = Tex(R"(A^{T})_{ij} = a_{ji}").set_color(GREY_B).set_width(3.6).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rule)); self.wait(1.2)
        self.play(FadeOut(grid), FadeOut(rule), FadeOut(tag))

        # 정리 2-5 (3) — 곱의 전치는 순서가 뒤집힌다
        tag = caption("정리 2-5 (3)", 24, GREY_B).next_to(head, DOWN, buff=0.25).align_to(head, LEFT)
        self.play(FadeIn(tag))
        law = Tex(R"(AB)^{T} = B^{T}A^{T}").set_width(5.4).move_to(2.2 * UP)
        self.play(Write(law), run_time=1.0)
        left = named("(AB)^{T}", self.ABt, DONE, 1.05)
        right = named("B^{T}A^{T}", self.ABt, DONE, 1.05)
        bad = named("A^{T}B^{T}", self.wrong, WARN, 1.05)
        row = VGroup(left, right, bad).arrange(RIGHT, buff=1.4).move_to(0.9 * DOWN)
        ab_blk = named("AB", self.AB, GREY_A, 1.05).move_to(left)
        self.play(FadeIn(ab_blk)); self.wait(0.5)
        self.play(FadeTransform(ab_blk, left), run_time=0.9)
        self.play(FadeIn(right, UP), run_time=0.8)
        same = box(VGroup(left, right), DONE, 0.2)
        self.play(ShowCreation(same)); self.wait(0.7)
        self.play(FadeIn(bad, UP), run_time=0.8)
        flip = caption("순서를 지키지 않으면 다른 행렬", 24, WARN).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(flip, UP)); self.wait(1.4)
        self.play(FadeOut(VGroup(row, same, flip, law, tag)))

        # 정리 2-5 (5) — 전치와 역행렬은 순서를 바꿔도 같다
        tag = caption("정리 2-5 (5)", 24, GREY_B).next_to(head, DOWN, buff=0.25).align_to(head, LEFT)
        self.play(FadeIn(tag))
        also = Tex(R"(A^{T})^{-1} = (A^{-1})^{T}").set_width(6.0).move_to(0.6 * UP)
        self.play(Write(also), run_time=1.2)
        note = caption("전치와 역행렬은 순서를 바꿔도 같음", 24, GREY_B).next_to(also, DOWN, buff=0.7)
        self.play(FadeIn(note, UP)); self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 여러 가지 행렬 — 교재 2.3 절
# ─────────────────────────────────────────────────────────────
class MatrixZoo(InteractiveScene):
    """이름이 붙는 자리를 색으로 보이고, 정의 조건을 이름 아래 같은 형식으로 단다.

    네 행렬 모두 같은 꼴(이름 · 행렬 · 조건)로 놓는다. 어느 하나에만 식이 붙으면
    그것만 다른 종류로 보인다. 기호는 다른 편과 같이 A 로 통일한다.
    """
    items = [
        ("대각행렬", [[2, 0, 0], [0, 3, 0], [0, 0, 5]],
         [(0, 0), (1, 1), (2, 2)], R"a_{ij} = 0 \quad (i \neq j)"),
        ("상삼각행렬", [[1, 4, 2], [0, 2, 5], [0, 0, 3]],
         [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)], R"a_{ij} = 0 \quad (i > j)"),
        ("대칭행렬", [[1, 3, 2], [3, 2, 5], [2, 5, 4]],
         [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)], R"A^{T} = A"),
        ("직교행렬", [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
         [(0, 1), (1, 2), (2, 0)], R"A^{T} A = I"),
    ]

    def construct(self):
        head = slide_title("여러 가지 행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        blocks = VGroup()
        for name, values, spots, cond in self.items:
            m = mat(values, GREY_B, h_buff=0.62, v_buff=0.48)
            m.set_height(1.6)
            for r, c in spots:
                m.get_rows()[r][c].set_color(DONE)
            rule = Tex(cond).set_color(GREY_B).set_height(0.34)
            block = VGroup(caption(name, 24, WHITE), m, rule)
            block.arrange(DOWN, buff=0.26)
            blocks.add(block)

        blocks.arrange_in_grid(2, 2, buff=1.1)
        blocks.set_height(5.3).move_to(0.45 * DOWN)

        for block in blocks:
            self.play(FadeIn(block, UP), run_time=0.7)
            self.wait(0.5)

        note = caption("성분이 놓인 자리로 부르는 이름", 26, GREY_B)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13~14. 행렬식과 역행렬이 하는 일 — 선형변환으로 보기
#
# 참고: legacy/_2016/eola/chapter6.py (3blue1brown, Essence of Linear Algebra)
#   DescribeInverse · MultiplyToIdentity · InvertNonInvertable · SquishExmapleDet
#
# 원본의 Pi creature 와 말풍선 장면(TeacherStudentsScene)은 가져오지 않는다.
# 사람 아이콘은 치토를 쓰기로 되어 있고(하네스 3.6), 여기는 사람이 나올 자리가 아니다.
# 격자·기저벡터·단위정사각형만 `LinearTransformationScene` 에서 물려받는다.
#
# **이 두 편은 맛보기다.** 기저와 선형변환의 정의는 CH04 에서 한다. 여기서는
# 행렬식이라는 수가 무엇을 재는 수인지, 역행렬이 무엇을 되돌리는지까지만 본다.
# ─────────────────────────────────────────────────────────────
# 배경 격자. 공용 클래스 기본값은 NumberPlane 의 보조선(faded line)까지 그려 격자가
# 두 겹으로 겹친다. 뒤에 남는 격자는 "원래 자리" 만 보이면 되므로 큰 눈금만 옅게 둔다.
# 움직이는 파란 격자는 그대로 둔다 — 그것이 변환이다.
BACK_PLANE = dict(
    x_range=(-7, 7, 1), y_range=(-4, 4, 1),
    faded_line_ratio=0,
    axis_config=dict(stroke_color=GREY_B, stroke_width=2),
    background_line_style=dict(stroke_color=GREY_D, stroke_width=1,
                               stroke_opacity=0.5),
)
FRONT_PLANE = dict(
    x_range=(-7, 7, 1), y_range=(-4, 4, 1),
    faded_line_ratio=0,
    background_line_style=dict(stroke_color=BLUE_D, stroke_width=2),
)


def overlay(mob, scene, edge=DOWN, buff=0.4):
    """격자 위에 얹는 문구. 격자가 비쳐 읽히지 않으므로 뒷판을 깐다."""
    mob.to_edge(edge, buff=buff)
    mob.add_background_rectangle(opacity=0.85, buff=0.12)
    scene.add_foreground_mobject(mob)
    return mob


class DeterminantGeometry(LinearTransformationScene):
    """행렬식은 그 행렬이 넓이를 몇 배로 바꾸는지를 재는 수다.

    공식만 외우면 CH04 선형변환에서 같은 것을 다시 만났을 때 알아보지 못한다.
    """
    include_background_plane = True
    include_foreground_plane = True
    background_plane_kwargs = BACK_PLANE
    foreground_plane_kwargs = FRONT_PLANE
    show_coordinates = True
    show_basis_vectors = True
    matrix = [[2, 1], [1, 3]]      # det = 5

    def construct(self):
        head = title("행렬식이 재는 것", 34)
        head.to_corner(UL, buff=0.5)
        head.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(head)

        # add_unit_square(animate=True) 은 DrawBorderThenFill 을 쓰는데
        # 지금 manimlib 에는 그 애니메이션이 없다. 직접 띄운다.
        self.add_unit_square()
        self.play(FadeIn(self.square))
        before = caption("넓이 1", 30, DONE)
        overlay(before, self, DOWN, 0.4)
        self.play(FadeIn(before))
        self.wait(0.8)

        label = Matrix([["2", "1"], ["1", "3"]], h_buff=0.8)
        label.set_color(ACCENT).set_height(1.15).to_corner(UR, buff=0.6)
        label.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(label)
        self.play(FadeIn(label, DOWN))
        self.wait(0.5)

        self.apply_matrix(self.matrix, run_time=2.2)
        self.wait(0.5)

        after = caption("넓이 5", 30, DONE)
        overlay(after, self, DOWN, 0.4)
        self.play(FadeOut(before), FadeIn(after))
        self.wait(0.8)

        rule = Tex(R"\det \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix} = 5")
        rule.set_color(DONE).set_width(4.0)
        rule.next_to(label, DOWN, buff=0.4).align_to(label, RIGHT)
        rule.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(rule)
        self.play(Write(rule), run_time=1.2)
        self.wait(0.8)

        note = caption("행렬식은 넓이의 배율", 30, DONE)
        overlay(note, self, DOWN, 0.4)
        self.play(FadeOut(after), FadeIn(note, UP))
        self.wait(2)


class DeterminantCollapse(LinearTransformationScene):
    """행렬식이 0 이면 평면 전체가 직선 하나로 눌린다.

    행렬은 `DeterminantZero` 와 같다. 그 편은 행 연산에서 영행이 나오는 것을
    보였고, 이 편은 같은 사실을 그림으로 본다.
    """
    include_background_plane = True
    background_plane_kwargs = BACK_PLANE
    foreground_plane_kwargs = FRONT_PLANE
    show_coordinates = True
    show_basis_vectors = True
    matrix = [[1, 2], [2, 4]]      # det = 0

    def construct(self):
        head = title("행렬식이 0 인 경우", 34)
        head.to_corner(UL, buff=0.5)
        head.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(head)

        # add_unit_square(animate=True) 은 DrawBorderThenFill 을 쓰는데
        # 지금 manimlib 에는 그 애니메이션이 없다. 직접 띄운다.
        self.add_unit_square()
        self.play(FadeIn(self.square))
        label = Tex(R"\det \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix} = 0")
        label.set_color(WARN).set_width(4.4).to_corner(UR, buff=0.6)
        label.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(label)
        self.play(Write(label), run_time=1.2)
        self.wait(0.5)

        self.apply_matrix(self.matrix, run_time=2.4)
        self.wait(0.8)

        note = caption("평면 전체가 직선 하나로", 28, WARN)
        overlay(note, self, DOWN, 1.0)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        last = caption("눌린 평면은 되돌릴 수 없음", 30, WARN)
        overlay(last, self, DOWN, 0.35)
        self.play(FadeIn(last, UP))
        self.wait(2)


class InverseAsUndo(LinearTransformationScene):
    """A 로 움직인 평면을 A^{-1} 이 제자리로 돌려놓는다.

    분모가 det A 라는 것을 그림 뒤에 한 번 더 만난다. 예제 2-4 의 분모 12 와 같은 자리다.
    """
    include_background_plane = True
    background_plane_kwargs = BACK_PLANE
    foreground_plane_kwargs = FRONT_PLANE
    show_coordinates = True
    show_basis_vectors = True
    matrix = [[2, 1], [1, 3]]      # DeterminantGeometry 와 같은 행렬

    def construct(self):
        head = title("역행렬이 하는 일", 34)
        head.to_corner(UL, buff=0.5)
        head.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(head)

        # add_unit_square(animate=True) 은 DrawBorderThenFill 을 쓰는데
        # 지금 manimlib 에는 그 애니메이션이 없다. 직접 띄운다.
        self.add_unit_square()
        self.play(FadeIn(self.square))

        label = Tex("A").set_color(ACCENT).scale(1.6).to_corner(UR, buff=0.8)
        label.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(label)
        self.play(FadeIn(label, DOWN))

        self.apply_matrix(self.matrix, run_time=2.0)
        self.wait(0.8)

        # label 은 이미 foreground 라 FadeTransform 으로 지워도 다시 그려진다.
        # 새 것을 따로 올리지 말고 있던 것의 모양만 바꾼다.
        back = Tex("A^{-1}").set_color(DONE).scale(1.6).move_to(label)
        back.add_background_rectangle(opacity=0.85, buff=0.12)
        self.play(Transform(label, back), run_time=0.7)

        self.apply_inverse(self.matrix, run_time=2.0)
        self.wait(0.5)

        note = caption("역행렬은 되돌리는 사상", 30, DONE)
        overlay(note, self, DOWN, 0.4)
        self.play(FadeIn(note, UP))
        self.wait(2)


class InverseDenominator(InteractiveScene):
    """역행렬의 분모가 행렬식이다. 앞 편의 그림에 수를 붙인다."""

    def construct(self):
        head = slide_title("역행렬의 분모")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        formula = VGroup(
            Tex(R"\det A = 5").set_color(ACCENT),
            Tex(R"A^{-1} = \frac{1}{5}"
                R"\begin{bmatrix} 3 & -1 \\ -1 & 2 \end{bmatrix}"),
        ).arrange(RIGHT, buff=1.4)
        formula.set_width(9.6).move_to(0.6 * UP)
        self.play(Write(formula), run_time=1.6)

        mark = box(formula[1][R"\frac{1}{5}"], DONE, 0.1)
        self.play(ShowCreation(mark))
        note = caption("분모가 행렬식", 30, DONE)
        note.next_to(formula, DOWN, buff=1.0)
        self.play(FadeIn(note, UP))
        self.wait(1.2)

        tail = caption("행렬식이 0 이면 나눌 수 없음", 28, WARN)
        tail.next_to(note, DOWN, buff=0.55)
        self.play(FadeIn(tail, UP))
        self.wait(1.2)

        same = caption("예제 2-4 의 분모 12 와 같은 자리", 26, GREY_B)
        same.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(same, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 15. rref 함수 리뷰 — 강의자료 p.12
#
# 앞서 `PartialPivot` 과 `EliminateColumn` 두 편으로 잘라 두었는데, 변수 설명 없이
# p 와 r 부터 꺼내는 바람에 코딩이 처음인 학생이 따라올 수 없었다. 한 편으로 합치고
# **변수가 무엇인지부터** 시작한다 (2026-09-11).
# ─────────────────────────────────────────────────────────────
class RrefCodeReview(InteractiveScene):
    """강의자료 p.12 의 rref 함수를 처음부터 읽는다.

    수는 예제 2-1 의 첨가행렬이다. 손으로 풀 때는 1행을 그대로 썼는데 코드는
    3행을 먼저 올린다. 그 차이가 어디서 오는지도 이 편에서 답한다.
    """
    start = [["1", "3", "2", "2"], ["2", "2", "0", "0"], ["-3", "1", "1", "-2"]]
    swapped = [["-3", "1", "1", "-2"], ["2", "2", "0", "0"], ["1", "3", "2", "2"]]
    scaled = [["1", "-\\frac{1}{3}", "-\\frac{1}{3}", "\\frac{2}{3}"],
              ["2", "2", "0", "0"], ["1", "3", "2", "2"]]
    cleared = [["1", "-\\frac{1}{3}", "-\\frac{1}{3}", "\\frac{2}{3}"],
               ["0", "\\frac{8}{3}", "\\frac{2}{3}", "-\\frac{4}{3}"],
               ["0", "\\frac{10}{3}", "\\frac{7}{3}", "\\frac{4}{3}"]]
    final = [["1", "0", "0", "1"], ["0", "1", "0", "-1"], ["0", "0", "1", "2"]]

    def board(self, values, h_buff=0.95):
        m = augmented(values, 3, WHITE, h_buff=h_buff, v_buff=0.62)
        m.set_width(5.4).move_to(3.4 * RIGHT + 0.5 * DOWN)
        return m

    def construct(self):
        head = slide_title("rref 함수 리뷰")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 1. 변수가 무엇인지부터 ────────────────────────────
        lines = code_block((
            "def rref(M, tol=1e-12):",
            "    R = np.array(M, dtype=float)",
            "    rows, cols = R.shape",
            "    r = 0",
        ), 21, buff=0.24)
        lines.to_edge(LEFT, buff=0.7).shift(1.6 * UP)
        self.play(LaggedStartMap(FadeIn, lines, lag_ratio=0.3), run_time=1.6)

        group = self.board(self.start)
        m = group.matrix
        self.play(FadeIn(group))
        self.wait(0.6)

        frame = box(m, ACCENT, 0.16)
        tag_R = caption("행렬 R", 24, ACCENT)
        tag_R.next_to(frame, UP, buff=0.25)
        self.play(ShowCreation(frame), FadeIn(tag_R))
        self.wait(0.9)
        self.play(FadeOut(frame), FadeOut(tag_R))

        size = caption("rows 3, cols 4", 24, CALM)
        size.next_to(group, DOWN, buff=0.45)
        self.play(FadeIn(size, UP))
        self.wait(0.9)
        self.play(FadeOut(size))

        row_mark = box(m.get_rows()[0], DONE, 0.13)
        row_tag = VGroup(code("r", 26, DONE), caption("지금 채우는 행", 22, DONE))
        row_tag.arrange(RIGHT, buff=0.35)
        row_tag.next_to(group, DOWN, buff=0.45)
        self.play(ShowCreation(row_mark), FadeIn(row_tag, UP))
        self.wait(1.1)

        col_mark = box(m.get_columns()[0], WARN, 0.13)
        col_tag = VGroup(code("c", 26, WARN), caption("지금 보는 열", 22, WARN))
        col_tag.arrange(RIGHT, buff=0.35)
        col_tag.next_to(row_tag, DOWN, buff=0.35)
        self.play(ShowCreation(col_mark), FadeIn(col_tag, UP))
        self.wait(1.1)
        self.play(FadeOut(row_mark), FadeOut(col_mark),
                  FadeOut(row_tag), FadeOut(col_tag), FadeOut(lines))

        # ── 2. 한 열을 처리하는 여덟 줄 — 변수를 디버거처럼 찍으며 간다 ──
        body = code_block((
            "for c in range(cols):",
            "    p = r + int(np.argmax(np.abs(R[r:, c])))",
            "    R[[r, p]] = R[[p, r]]",
            "    R[r] = R[r] / R[r, c]",
            "    for i in range(rows):",
            "        if i != r:",
            "            R[i] = R[i] - R[i, c] * R[r]",
            "    r += 1",
        ), 20)
        body.set_width(6.6).to_edge(LEFT, buff=0.5).shift(0.45 * UP)
        self.play(LaggedStartMap(FadeIn, body, lag_ratio=0.18), run_time=1.8)

        # 행렬을 위로 올려 아래에 변수 창과 계산 줄이 들어갈 자리를 만든다.
        # Transform 은 옛 객체를 화면에 남긴다. 뒤에서 group 을 갈아 끼우므로 FadeTransform 으로 바꾼다.
        top = self.board(self.start); top.set_width(4.8).move_to(3.6 * RIGHT + 1.45 * UP)
        self.play(FadeTransform(group, top), run_time=0.8)
        group = top; m = group.matrix

        def spotlight(index):
            return box(body[index], CALM, 0.09)

        # 변수 창 — 디버거의 watch 처럼 지금 값을 보여 준다.
        watch = code("c = 0    r = 0", 18, WARN)
        watch.move_to(3.6 * RIGHT + 1.15 * DOWN)
        self.play(FadeIn(watch, UP))

        def set_watch(text):
            nonlocal watch
            new = code(text, 18, WARN)
            if new.get_width() > 6.2:
                new.set_width(6.2)
            new.move_to(watch)
            self.play(Transform(watch, new), run_time=0.4)

        light = spotlight(0)
        self.play(ShowCreation(light)); self.wait(0.5)

        # p — 절댓값이 가장 큰 행
        self.play(Transform(light, spotlight(1)))
        picks = VGroup(*[caption(t, 22, WARN) for t in ("1", "2", "3")])
        for tag, row in zip(picks, m.get_rows()):
            tag.next_to(row[0], LEFT, buff=0.3)
        self.play(LaggedStartMap(FadeIn, picks, lag_ratio=0.3), run_time=0.9)
        chosen = box(m.get_rows()[2], WARN, 0.13)
        self.play(ShowCreation(chosen))
        set_watch("c = 0    r = 0    p = 2")
        note = caption("절댓값이 가장 큰 행", 22, WARN)
        note.next_to(watch, DOWN, buff=0.35)
        self.play(FadeIn(note, UP)); self.wait(1.2)
        self.play(FadeOut(picks), FadeOut(chosen), FadeOut(note))

        # 행 교환
        self.play(Transform(light, spotlight(2)))
        target = self.board(self.swapped); target.set_width(4.8).move_to(group)
        self.play(FadeTransform(group, target), run_time=1.0)
        group, m = target, target.matrix; self.wait(0.6)

        # 선행 성분을 1 로
        self.play(Transform(light, spotlight(3)))
        target = self.board(self.scaled, h_buff=1.15); target.set_width(4.8).move_to(group)
        self.play(FadeTransform(group, target), run_time=1.0)
        group, m = target, target.matrix
        lead = box(m.get_rows()[0][0], DONE, 0.1)
        self.play(ShowCreation(lead)); self.wait(0.7); self.play(FadeOut(lead))

        # 안쪽 반복문 — i 마다 조건과 계산을 그대로 찍는다.
        self.play(Transform(light, spotlight(4)))
        calc_pos = 3.6 * RIGHT + 2.55 * DOWN

        def show_calc(lines):
            g = VGroup(*[Tex(t) for t in lines]).set_color(GREY_A)
            g.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            g.set_width(6.0).move_to(calc_pos)
            return g

        # i = 0 : 피벗 행 자신은 건너뛴다
        set_watch("i = 0    r = 0    i != r  False")
        self.play(Transform(light, spotlight(5)))
        skip = caption("피벗 행은 건너뜀", 22, GREY_B).move_to(calc_pos)
        self.play(FadeIn(skip)); self.wait(0.9); self.play(FadeOut(skip))

        # i = 1
        set_watch("i = 1    r = 0    i != r  True    R[i, c] = 2")
        self.play(Transform(light, spotlight(6)))
        mark = box(m.get_rows()[1], WARN, 0.12); self.play(ShowCreation(mark))
        calc = show_calc((
            R"R[1] = R[1] - 2 \cdot R[0]",
            R"= [\,2,\ 2,\ 0,\ 0\,] - 2\,[\,1,\ -\tfrac{1}{3},\ -\tfrac{1}{3},\ \tfrac{2}{3}\,]",
            R"= [\,0,\ \tfrac{8}{3},\ \tfrac{2}{3},\ -\tfrac{4}{3}\,]",
        ))
        for line in calc:
            self.play(FadeIn(line, RIGHT), run_time=0.7); self.wait(0.5)
        mid = [self.scaled[0], ["0", "\\frac{8}{3}", "\\frac{2}{3}", "-\\frac{4}{3}"], self.scaled[2]]
        target = self.board(mid, h_buff=1.15); target.set_width(4.8).move_to(group)
        self.play(FadeTransform(group, target), FadeOut(mark), run_time=1.0)
        group, m = target, target.matrix; self.wait(0.6)
        self.play(FadeOut(calc))

        # i = 2
        set_watch("i = 2    r = 0    i != r  True    R[i, c] = 1")
        mark = box(m.get_rows()[2], WARN, 0.12); self.play(ShowCreation(mark))
        calc = show_calc((
            R"R[2] = R[2] - 1 \cdot R[0]",
            R"= [\,1,\ 3,\ 2,\ 2\,] - [\,1,\ -\tfrac{1}{3},\ -\tfrac{1}{3},\ \tfrac{2}{3}\,]",
            R"= [\,0,\ \tfrac{10}{3},\ \tfrac{7}{3},\ \tfrac{4}{3}\,]",
        ))
        for line in calc:
            self.play(FadeIn(line, RIGHT), run_time=0.7); self.wait(0.5)
        target = self.board(self.cleared, h_buff=1.15); target.set_width(4.8).move_to(group)
        self.play(FadeTransform(group, target), FadeOut(mark), run_time=1.0)
        group, m = target, target.matrix
        column = box(m.get_columns()[0], DONE, 0.13)
        self.play(ShowCreation(column)); self.wait(0.8)
        self.play(FadeOut(column), FadeOut(calc))

        # 다음 행으로
        self.play(Transform(light, spotlight(7)))
        set_watch("c = 0    r = 1"); self.wait(0.8)
        self.play(FadeOut(light), FadeOut(watch))

        # ── 3. 열마다 되풀이 ──────────────────────────────────
        again = caption("열마다 되풀이", 26, GREY_B).move_to(calc_pos)
        self.play(FadeIn(again, UP)); self.wait(0.8)
        target = self.board(self.final); target.set_width(4.8).move_to(group)
        self.play(FadeTransform(group, target), FadeOut(again), run_time=1.2)
        group, m = target, target.matrix
        answer = Tex("x_1 = 1,\\; x_2 = -1,\\; x_3 = 2").set_color(DONE)
        answer.set_width(4.6).next_to(group, DOWN, buff=0.5)
        self.play(Write(answer), run_time=1.0); self.wait(0.8)

        # 교재 풀이는 1행을 그대로 피벗으로 썼고, 코드는 3행을 올렸다. 중간 행렬은
        # 다르지만 기약 행 사다리꼴은 하나라 답이 같다. 학생이 반드시 묻는 자리다.
        why1 = caption("교재는 1행, 코드는 3행부터", 24, GREY_B)
        why2 = caption("결과는 같은 기약 행 사다리꼴", 24, DONE)
        VGroup(why1, why2).arrange(DOWN, buff=0.25).next_to(answer, DOWN, buff=0.5)
        self.play(FadeIn(why1, UP)); self.wait(0.9)
        self.play(FadeIn(why2, UP)); self.wait(2)
