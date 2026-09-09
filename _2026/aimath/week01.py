"""AI기초수학 1주차 — 강좌소개 및 오리엔테이션.

강의자료 `AI기초수학/1.강의소개.pptx` 와 교안 `week01_강좌소개_오리엔테이션.md` 의
시각화 보조자료.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week01.py
    ./render.sh check _2026/aimath/week01.py              # 전 씬 빠른 점검
    ./render.sh ppt   _2026/aimath/week01.py CourseRoadmap  # PPT 삽입용 재인코딩
    ./render.sh all   _2026/aimath/week01.py              # 전부 1080p
"""
import re

from manim_imports_ext import *


# ─────────────────────────────────────────────────────────────
# 강의자료(아주대 템플릿)와 같은 서체·색을 쓴다.
# 폰트 표준은 2026-2 콘텐츠제작_하네스_PRD.md 3.5절.
# ─────────────────────────────────────────────────────────────
TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"

INK = GREY_A
ACCENT = BLUE_B
WARN = RED_C
CALM = TEAL_B
GOLD_ = YELLOW

STAGE_COLORS = [BLUE_B, GREEN_B, TEAL_B, YELLOW]


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
    """화면 문구 길이를 막는다(하네스 3.6).

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
    return text


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def body(text, size=30, color=INK):
    check_words(text)
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def slide_title(text):
    """왼쪽 위 제목 + 밑줄. 강의 슬라이드 제목 위치와 맞춘다."""
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def card(head, chapters, note, color, width=2.9, height=2.5):
    """수강계획의 꼭지 하나. 제목 / 교재 장 / 한 줄 설명을 담은 카드."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.18)
    box.set_stroke(color, 3).set_fill(color, 0.10)

    head_t = body(head, 32, color)
    chap_t = body(chapters, 22, GREY_B)
    note_t = body(note, 24, INK)

    stack = VGroup(head_t, chap_t, note_t).arrange(DOWN, buff=0.28)
    stack.move_to(box)
    return VGroup(box, stack)


# ─────────────────────────────────────────────────────────────
# 1. 과목 로드맵 — 한 학기가 지나가는 길
# ─────────────────────────────────────────────────────────────
class CourseRoadmap(InteractiveScene):
    """1차시 [다루는 내용]. 선형대수 → 미적분 → 확률통계 → 머신러닝·딥러닝.

    교재 장 번호로 네 꼭지를 표시하고, 중간·기말 시험 범위를 묶어 준다.
    """
    stages = [
        ("선형대수", "CH01~CH06", "데이터 표현"),
        ("미적분", "CH07~CH09", "최적화"),
        ("확률·통계", "CH10~CH11", "불확실성 정량화"),
        ("머신러닝·딥러닝", "CH12~CH13", "앞의 셋을 결합"),
    ]

    def construct(self):
        head = slide_title("학기 수강계획")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        cards = VGroup(*[
            card(name, chapters, note, color)
            for (name, chapters, note), color in zip(self.stages, STAGE_COLORS)
        ])
        cards.arrange(RIGHT, buff=0.62)
        cards.set_width(FRAME_WIDTH - 1.4)
        cards.move_to(UP * 0.35)

        arrows = VGroup(*[
            Arrow(a.get_right(), b.get_left(), buff=0.12).set_color(GREY_B)
            for a, b in zip(cards, cards[1:])
        ])

        self.play(FadeIn(cards[0], UP))
        for arrow, nxt in zip(arrows, cards[1:]):
            self.play(GrowArrow(arrow), FadeIn(nxt, UP), run_time=0.8)
        self.wait()

        exam = VGroup(
            body("중간고사", 24, GREY_B),
            body("기말고사", 24, GREY_B),
        )
        exam[0].next_to(cards[0:2], DOWN, buff=0.22)
        exam[1].next_to(cards[2:4], DOWN, buff=0.22)
        brace_l = Brace(cards[0:2], DOWN, buff=0.05).set_color(GREY_C)
        brace_r = Brace(cards[2:4], DOWN, buff=0.05).set_color(GREY_C)
        exam[0].next_to(brace_l, DOWN, buff=0.12)
        exam[1].next_to(brace_r, DOWN, buff=0.12)

        self.play(
            GrowFromCenter(brace_l), GrowFromCenter(brace_r),
            FadeIn(exam[0]), FadeIn(exam[1]),
        )
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 연속처럼 보이지만 이산이다 — DLSS 사례
# ─────────────────────────────────────────────────────────────
class PixelsAreDiscrete(InteractiveScene):
    """1차시 [강의 개요 · 사례 1]. 화면은 연속으로 보이지만 픽셀은 이산이다.

    부드러운 곡선 하나를 격자 위에 올리면 계단이 된다. 프레임을 채워 넣는 계산은
    이 격자 위에서 벌어지므로 이산적 위치를 다루는 언어가 필요하다.
    """
    n_cols = 16
    n_rows = 9
    cell = 0.5

    def construct(self):
        head = slide_title("연속 화면과 이산 픽셀")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        grid = VGroup(*[
            Square(self.cell) for _ in range(self.n_rows * self.n_cols)
        ])
        grid.arrange_in_grid(self.n_rows, self.n_cols, buff=0)
        grid.set_stroke(GREY_D, 1).set_fill(BLACK, 1)
        grid.move_to(DOWN * 0.5)

        def curve_y(x):
            return 1.25 * np.sin(1.0 * x) - 0.2 * x

        curve = ParametricCurve(
            lambda t: np.array([t, curve_y(t), 0]),
            t_range=(-3.8, 3.8, 0.02),
        )
        curve.set_stroke(ACCENT, 5)
        curve.move_to(grid)

        self.play(ShowCreation(curve), run_time=2)
        note = body("연속 곡선", 28, ACCENT)
        note.next_to(grid, DOWN, buff=0.28)
        self.play(FadeIn(note))
        self.wait()

        self.play(ShowCreation(grid, lag_ratio=0.004), run_time=2)
        self.wait(0.5)

        # 열마다 곡선이 지나는 칸 하나씩 — 계단이 드러난다
        def cell_at(row, col):
            return grid[row * self.n_cols + col]

        samples = np.array([curve.pfp(a) for a in np.linspace(0, 1, 600)])
        lit = VGroup()
        for col in range(self.n_cols):
            cx = cell_at(0, col).get_center()[0]
            i = int(np.argmin(np.abs(samples[:, 0] - cx)))
            if abs(samples[i][0] - cx) > self.cell:
                continue
            ys = np.array([cell_at(r, col).get_center()[1] for r in range(self.n_rows)])
            lit.add(cell_at(int(np.argmin(np.abs(ys - samples[i][1]))), col))

        self.play(
            lit.animate.set_fill(ACCENT, 0.85).set_stroke(ACCENT, 1),
            FadeOut(curve),
            run_time=1.5,
        )

        new_note = body("실제 점등 픽셀", 28, WARN)
        new_note.move_to(note)
        self.play(FadeTransform(note, new_note))
        self.wait()

        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 그림 한 장이 행렬 하나 — 선형대수로 들어가는 문
# ─────────────────────────────────────────────────────────────
class ImageAsMatrix(InteractiveScene):
    """1차시 [강의 개요 · 왜 행렬부터인가]. 2주차 연립선형방정식과 행렬로 이어진다.

    8×8 흑백 그림 → 밝기 숫자가 채워진 행렬 → 한 줄로 편 벡터.
    """
    n = 8
    cell = 0.44

    # 숫자 7 모양. 1이 밝은 픽셀이다.
    glyph = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]

    def construct(self):
        head = slide_title("이미지의 행렬 표현")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        values = []
        for row in self.glyph:
            for v in row:
                values.append(v)

        squares = VGroup(*[Square(self.cell) for _ in values])
        squares.arrange_in_grid(self.n, self.n, buff=0)
        squares.set_stroke(GREY_D, 1)
        for sq, v in zip(squares, values):
            sq.set_fill(WHITE if v else BLACK, 1)
        squares.move_to(LEFT * 4.0 + UP * 0.1)

        matrix_label = Tex(R"A \in \mathbb{R}^{8 \times 8}").set_color(ACCENT)
        matrix_label.next_to(squares, UP, buff=0.3)

        pic_label = body("8×8 흑백 이미지 (28×28도 동일한 원리)", 24, GREY_B)
        pic_label.next_to(squares, RIGHT, buff=0.9).align_to(squares, UP)

        self.play(ShowCreation(squares, lag_ratio=0.01), run_time=1.8)
        self.play(FadeIn(pic_label))
        self.wait()

        # 칸마다 밝기 숫자를 얹는다
        numbers = VGroup(*[
            Integer(v).set_height(self.cell * 0.42).move_to(sq)
            .set_color(BLACK if v else GREY_B)
            for sq, v in zip(squares, values)
        ])
        self.play(LaggedStartMap(FadeIn, numbers, lag_ratio=0.01), run_time=2)
        self.play(Write(matrix_label))
        self.wait()

        num_note = body("밝기 숫자 64개", 26, INK)
        num_note.next_to(pic_label, DOWN, buff=0.4).align_to(pic_label, LEFT)
        self.play(FadeIn(num_note))
        self.wait()

        # 한 줄로 편다 — 벡터가 된다
        strip = VGroup(*[Square(0.17) for _ in values])
        strip.arrange(RIGHT, buff=0)
        strip.set_stroke(GREY_D, 1)
        for sq, v in zip(strip, values):
            sq.set_fill(WHITE if v else BLACK, 1)
        strip.move_to(DOWN * 2.7)

        vec_label = Tex(R"\vec{x} \in \mathbb{R}^{64}").set_color(CALM)
        vec_label.next_to(strip, UP, buff=0.3)

        flatten = body("한 줄로 펴기", 26, GREY_B)
        flatten.next_to(num_note, DOWN, buff=0.4).align_to(num_note, LEFT)

        self.play(FadeOut(numbers), FadeIn(flatten))
        self.play(TransformFromCopy(squares, strip), run_time=1.6)
        self.play(Write(vec_label))
        self.wait()

        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 학습은 기울기를 따라 내려가는 일 — 미적분으로 들어가는 문
# ─────────────────────────────────────────────────────────────
class GradientDescentGlimpse(InteractiveScene):
    """1차시 [강의 개요 · 왜 미분인가]. 11주차 편미분과 경사 하강법의 예고편.

    접선의 기울기가 가리키는 반대쪽으로 조금씩 옮기면 바닥에 닿는다.
    """
    x0 = 3.3
    eta = 0.55
    n_steps = 10

    def loss(self, x):
        return 0.25 * x ** 2 + 0.6

    def slope(self, x):
        return 0.5 * x

    def construct(self):
        head = slide_title("경사 하강법 개요")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        axes = Axes(
            x_range=(-4.2, 4.2, 1),
            y_range=(0, 4.4, 1),
            width=8.2,
            height=4.2,
        )
        axes.move_to(LEFT * 2.2 + DOWN * 0.55)
        x_label = body("모형의 값", 24, GREY_B)
        x_label.next_to(axes.x_axis.get_right(), DOWN, buff=0.25)
        y_label = body("틀린 정도", 24, GREY_B)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.15)

        graph = axes.get_graph(self.loss, x_range=(-4.0, 4.0))
        graph.set_stroke(ACCENT, 4)

        self.play(ShowCreation(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(ShowCreation(graph), run_time=1.6)
        self.wait()

        x = self.x0
        ball = Dot(axes.c2p(x, self.loss(x)), radius=0.13).set_fill(WARN, 1)
        self.play(FadeIn(ball, scale=0.5))

        readout = VGroup(
            body("접선의 기울기", 26, GOLD_),
            DecimalNumber(self.slope(x), num_decimal_places=2).set_color(GOLD_),
        )
        readout.arrange(RIGHT, buff=0.25)
        readout.move_to(RIGHT * 4.6 + UP * 1.4)
        self.play(FadeIn(readout))

        def tangent_at(xv):
            m = self.slope(xv)
            dx = 1.1
            p1 = axes.c2p(xv - dx, self.loss(xv) - m * dx)
            p2 = axes.c2p(xv + dx, self.loss(xv) + m * dx)
            return Line(p1, p2).set_stroke(GOLD_, 3)

        tangent = tangent_at(x)
        self.play(ShowCreation(tangent))
        self.wait()

        rule = Tex(R"x \leftarrow x - \eta \, f'(x)").set_color(WHITE)
        rule.set_width(3.6).next_to(readout, DOWN, buff=0.6)
        rule_note = body("기울기의 반대 방향으로 이동", 24, GREY_B)
        rule_note.next_to(rule, DOWN, buff=0.4)
        self.play(Write(rule))
        self.play(FadeIn(rule_note))
        self.wait()

        for _ in range(self.n_steps):
            x_new = x - self.eta * self.slope(x)
            self.play(
                ball.animate.move_to(axes.c2p(x_new, self.loss(x_new))),
                Transform(tangent, tangent_at(x_new)),
                ChangeDecimalToValue(readout[1], self.slope(x_new)),
                run_time=0.55,
            )
            x = x_new
        self.wait()

        self.wait(2)
