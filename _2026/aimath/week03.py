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
# 4. 기약 행 사다리꼴에서 해 읽기 — 교재 2.1 절 도입
# ─────────────────────────────────────────────────────────────
class ReadRREF(InteractiveScene):
    """왼쪽이 단위행렬이 되면 마지막 열이 그대로 해다."""

    def construct(self):
        head = slide_title("기약 행 사다리꼴에서 해 읽기")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        group = augmented([[1, 0, 0, 1], [0, 1, 0, -1], [0, 0, 1, 2]], 3)
        group.move_to(2.6 * LEFT + 0.3 * DOWN)
        m = group.matrix
        self.play(FadeIn(group))
        self.wait(0.5)

        left = box(VGroup(*m.get_columns()[:3]), ACCENT, 0.16)
        left_tag = caption("단위행렬", 26, ACCENT)
        left_tag.next_to(left, UP, buff=0.3)
        self.play(ShowCreation(left), FadeIn(left_tag))
        self.wait(0.6)

        rows = [Tex(t) for t in (R"x_1 = 1", R"x_2 = -1", R"x_3 = 2")]
        lines = VGroup(*rows).arrange(DOWN, buff=0.55)
        lines.next_to(group, RIGHT, buff=1.9).set_color(DONE)

        arrows = VGroup()
        for i, line in enumerate(rows):
            entry = m.get_rows()[i][3]
            arrow = Arrow(entry.get_right(), line.get_left(), buff=0.25)
            arrow.set_stroke(GREY_C, 3)
            arrows.add(arrow)

        for arrow, line in zip(arrows, rows):
            self.play(ShowCreation(arrow), FadeIn(line, RIGHT), run_time=0.7)

        note = caption("마지막 열이 그대로 해", 26, GREY_B)
        note.next_to(group, DOWN, buff=0.8)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 양말-신발 성질 — 교재 정리 2-4 (2)
# ─────────────────────────────────────────────────────────────
class SocksShoes(InteractiveScene):
    """(AB)^{-1} = B^{-1}A^{-1}. 순서를 지키지 않은 곱은 다른 행렬이 된다.

    A 는 예제 2-3 의 행렬이다. 그 역행렬을 이미 손으로 구해 봤으므로
    여기서는 결과만 쓴다.
    """
    A = [[2, 3], [5, 7]]
    B = [[1, 1], [2, 3]]
    AB = [[8, 11], [19, 26]]
    right = [[-26, 11], [19, -8]]      # (AB)^{-1} = B^{-1}A^{-1}
    wrong = [[-27, 10], [19, -7]]      # A^{-1}B^{-1}

    def construct(self):
        head = slide_title("양말-신발 성질")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        chain = Tex(R"(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = AA^{-1} = I")
        chain.set_width(11.0).move_to(1.9 * UP)
        self.play(Write(chain), run_time=1.6)
        self.wait(0.6)

        inner = caption("안쪽부터 만나 사라짐", 26, DONE)
        inner.next_to(chain, DOWN, buff=0.45)
        self.play(FadeIn(inner, UP))
        self.wait(1.2)
        self.play(FadeOut(inner))

        good = VGroup(caption("순서를 지킨 곱", 24, DONE),
                      Tex(R"B^{-1}A^{-1}").set_color(DONE),
                      mat(self.right, DONE, h_buff=1.15))
        bad = VGroup(caption("지키지 않은 곱", 24, WARN),
                     Tex(R"A^{-1}B^{-1}").set_color(WARN),
                     mat(self.wrong, WARN, h_buff=1.15))
        for col in (good, bad):
            col.arrange(DOWN, buff=0.4)
        pair = VGroup(good, bad).arrange(RIGHT, buff=2.4)
        pair.move_to(1.3 * DOWN)

        self.play(FadeIn(good, LEFT), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(bad, RIGHT), run_time=0.9)
        self.wait(1.0)

        marks = VGroup(box(bad[2].get_entries()[0], WARN, 0.1),
                       box(bad[2].get_entries()[1], WARN, 0.1),
                       box(bad[2].get_entries()[3], WARN, 0.1))
        self.play(ShowCreation(marks))
        note = caption("세 자리가 다름", 26, WARN)
        note.next_to(bad, DOWN, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


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

        note = caption("어긋나게 곱해 뺀 수", 26, GREY_B)
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
        self.wait(2)


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
    """(AB)^T = B^T A^T. 양말-신발과 같은 자리에서 순서가 뒤집힌다."""
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 3]]
    AB = [[4, 6], [10, 12]]
    ABt = [[4, 10], [6, 12]]

    def construct(self):
        head = slide_title("전치행렬의 성질")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        left = VGroup(Tex("(AB)^{T}").set_color(DONE),
                      mat(self.ABt, DONE, h_buff=1.05))
        left.arrange(DOWN, buff=0.45)
        right = VGroup(Tex("B^{T}A^{T}").set_color(DONE),
                       mat(self.ABt, DONE, h_buff=1.05))
        right.arrange(DOWN, buff=0.45)
        equal = Tex("=")
        pair = VGroup(left, equal, right).arrange(RIGHT, buff=1.5)
        pair.move_to(0.9 * UP)

        source = VGroup(Tex("AB").set_color(GREY_B),
                        mat(self.AB, GREY_B, h_buff=1.05))
        source.arrange(DOWN, buff=0.45).move_to(0.9 * UP)

        self.play(FadeIn(source))
        self.wait(0.8)
        self.play(FadeTransform(source, left), run_time=1.0)
        self.play(FadeIn(equal), FadeIn(right, RIGHT), run_time=0.9)
        self.wait(1.0)

        flip = caption("전치도 순서가 뒤집힌다", 28, WARN)
        flip.next_to(pair, DOWN, buff=0.9)
        self.play(FadeIn(flip, UP))
        self.wait(1.2)

        also = Tex(R"(A^{T})^{-1} = (A^{-1})^{T}")
        also.set_width(6.0).next_to(flip, DOWN, buff=0.8)
        self.play(Write(also), run_time=1.2)
        note = caption("전치와 역행렬은 자리를 바꿔도 같음", 24, GREY_B)
        note.next_to(also, DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 여러 가지 행렬 — 교재 2.3 절
# ─────────────────────────────────────────────────────────────
class MatrixZoo(InteractiveScene):
    """이름이 붙는 자리를 색으로 보인다. 성분이 어디에 있느냐가 이름이다."""
    items = [
        ("대각행렬", [[2, 0, 0], [0, 3, 0], [0, 0, 5]],
         [(0, 0), (1, 1), (2, 2)]),
        ("상삼각행렬", [[1, 4, 2], [0, 2, 5], [0, 0, 3]],
         [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]),
        ("대칭행렬", [[1, 3, 2], [3, 2, 5], [2, 5, 4]],
         [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]),
        ("직교행렬", [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
         [(0, 1), (1, 2), (2, 0)]),
    ]

    def construct(self):
        head = slide_title("여러 가지 행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        blocks = VGroup()
        for name, values, spots in self.items:
            m = mat(values, GREY_B, h_buff=0.62, v_buff=0.48)
            m.set_height(1.72)
            for r, c in spots:
                m.get_rows()[r][c].set_color(DONE)
            block = VGroup(caption(name, 24, WHITE), m)
            block.arrange(DOWN, buff=0.3)
            blocks.add(block)

        blocks.arrange_in_grid(2, 2, buff=1.25)
        blocks.set_height(4.9).move_to(0.55 * DOWN)

        for block in blocks:
            self.play(FadeIn(block, UP), run_time=0.7)
            self.wait(0.5)

        note = caption("성분이 놓인 자리로 부르는 이름", 26, GREY_B)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        ortho = Tex(R"Q^{T}Q = I").set_color(DONE)
        ortho.next_to(blocks[3], RIGHT, buff=0.5).shift(0.2 * UP)
        self.play(FadeIn(ortho, LEFT))
        self.wait(2)
