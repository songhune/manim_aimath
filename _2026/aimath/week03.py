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
from manim_imports_ext import *


TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"

INK = GREY_A
ACCENT = BLUE_B
CALM = TEAL_B
WARN = RED_C
DONE = YELLOW


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def body(text, size=28, color=INK):
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def caption(text, size=26, color=GREY_B):
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
