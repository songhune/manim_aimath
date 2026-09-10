"""AI기초수학 — 교재 Chapter 1 행렬의 연산.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 01_연립선형방정식과 행렬.pptx` 의
1.3 행렬의 연산 · 1.4 행렬과 연립선형방정식의 관계에 붙는 보조 영상.
화면에 나오는 수는 모두 교재 예제 1-3 ~ 1-9 와 정리 1-5 의 실제 값이다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week02.py
    ./render.sh check _2026/aimath/week02.py
    ./render.sh ppt   _2026/aimath/week02.py MatrixProduct
    ./render.sh all   _2026/aimath/week02.py
"""
import re

from manim_imports_ext import *


# ─────────────────────────────────────────────────────────────
# 강의자료(아주대 템플릿)와 같은 서체·색. 하네스 3.5절.
# ─────────────────────────────────────────────────────────────
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
    """왼쪽 위 제목 + 밑줄. 강의 슬라이드 제목 자리와 맞춘다."""
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def mat(values, color=WHITE, h_buff=0.9, v_buff=0.6):
    """정수 성분 행렬. 성분은 Tex 라 색을 따로 줄 수 있다."""
    m = Matrix(values, h_buff=h_buff, v_buff=v_buff, bracket_h_buff=0.15)
    m.set_color(color)
    return m


def entry_at(m, row, col, n_cols):
    return m.get_entries()[row * n_cols + col]


def box(mobject, color=WARN, buff=0.12):
    return SurroundingRectangle(mobject, buff=buff).set_stroke(color, 3)


def formula(tex, color=GREY_A, size=1.0):
    """화면 아래쪽에 두는 성분 표기 공식. 교재의 표기를 그대로 쓴다."""
    f = Tex(tex).set_color(color).scale(size)
    return f


def symbol_matrix(rows, cols, letter="a", color=WHITE, h_buff=0.75, v_buff=0.55):
    """a_{ij} 로 채운 일반형 행렬."""
    values = []
    for i in range(rows):
        line = []
        for j in range(cols):
            line.append("%s_{%d%d}" % (letter, i + 1, j + 1))
        values.append(line)
    return mat(values, color, h_buff, v_buff)


def diagonal_axis(m, n, color=DONE, stretch=1.3):
    """정방행렬의 주대각선. 성분 (1,1) 과 (n,n) 을 잇고 조금 연장한다.

    성분마다 배경을 깔고 선을 맨 뒤로 보내야 숫자를 가로지르지 않는다.
    부르는 쪽에서 `scene.bring_to_back(axis)` 를 함께 쓴다.
    """
    m.add_background_to_entries()
    first = entry_at(m, 0, 0, n)
    last = entry_at(m, n - 1, n - 1, n)
    axis = Line(first.get_center(), last.get_center())
    axis.scale(stretch)
    axis.set_stroke(color, 3)
    return axis


def shape_tag(m, text, color=GREY_B):
    tag = caption(text, 24, color)
    tag.next_to(m, DOWN, buff=0.25)
    return tag


def op_label(lines, color=CALM):
    """행 연산 표기. 한 단계에 두 줄까지 붙는다."""
    group = VGroup(*[caption(line, 26, color) for line in lines])
    group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    return group


def leading_positions(values):
    """행마다 처음 나오는 0 이 아닌 성분의 열 번호. 영행은 건너뛴다."""
    out = []
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            if value != 0:
                out.append((i, j))
                break
    return out


# ─────────────────────────────────────────────────────────────
# 1. 합과 차 — 교재 예제 1-3
# ─────────────────────────────────────────────────────────────
class MatrixAddition(InteractiveScene):
    """같은 자리 성분끼리 더하고 뺀다. 크기가 같아야 짝이 생긴다."""
    A = [[1, 0], [2, 1], [4, 3]]
    B = [[4, 3], [1, 1], [0, 2]]

    def construct(self):
        head = slide_title("행렬의 합과 차")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        sums = [[a + b for a, b in zip(ra, rb)]
                for ra, rb in zip(self.A, self.B)]
        diffs = [[a - b for a, b in zip(ra, rb)]
                 for ra, rb in zip(self.A, self.B)]

        a = mat(self.A, ACCENT)
        b = mat(self.B, CALM)
        sign = Tex("+").set_color(GREY_B)
        eq = Tex("=").set_color(GREY_B)
        out = mat(sums, WHITE)

        row = VGroup(a, sign, b, eq, out).arrange(RIGHT, buff=0.45)
        row.set_width(min(row.get_width(), FRAME_WIDTH - 3.0))
        row.move_to(0.25 * DOWN)

        out.get_entries().set_opacity(0)
        self.play(FadeIn(a), FadeIn(b), Write(sign), Write(eq),
                  ShowCreation(out.get_brackets()))

        rule = formula(R"(A + B)_{ij} = a_{ij} + b_{ij}")
        rule.to_edge(DOWN, buff=1.05)
        note = caption("같은 자리 성분끼리 계산")
        note.to_edge(DOWN, buff=0.55)
        self.play(Write(rule), FadeIn(note, UP))

        for k in range(6):
            ea, eb = a.get_entries()[k], b.get_entries()[k]
            eo = out.get_entries()[k]
            boxes = VGroup(box(ea, ACCENT), box(eb, CALM))
            self.play(ShowCreation(boxes), run_time=0.35)
            self.play(eo.animate.set_opacity(1), FadeOut(boxes), run_time=0.4)
        self.wait()

        minus = Tex("-").set_color(GREY_B).move_to(sign)
        diff = mat(diffs, WHITE).match_height(out).move_to(out)
        rule_minus = formula(R"(A - B)_{ij} = a_{ij} - b_{ij}").move_to(rule)
        self.play(Transform(sign, minus), Transform(out, diff),
                  Transform(rule, rule_minus))
        self.wait()

        warn = caption("크기가 다르면 짝이 없어 정의되지 않음", 26, WARN)
        warn.move_to(note)
        self.play(FadeOut(note, DOWN), FadeIn(warn, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 스칼라곱 — 교재 예제 1-3 의 5B
# ─────────────────────────────────────────────────────────────
class ScalarMultiple(InteractiveScene):
    """스칼라 하나가 모든 성분에 같은 배로 걸린다.

    c 를 1 에서 5 까지 한 칸씩 올리면 여섯 성분이 함께 움직인다. 화면에 나오는
    값은 모두 cB 를 실제로 계산한 정수다. 스칼라를 c 로 쓰는 것은 교재 정의 1-6 을 따른다.
    """
    B = [[4, 3], [1, 1], [0, 2]]

    def construct(self):
        head = slide_title("스칼라곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        base = mat(self.B, CALM)
        out = mat(self.B, WHITE)
        arrow = Tex(R"\longrightarrow").set_color(GREY_C)

        row = VGroup(base, arrow, out).arrange(RIGHT, buff=0.8)
        row.move_to(0.4 * DOWN)

        readout = VGroup(
            Tex("c = ").set_color(GREY_B),
            Integer(1).set_color(DONE),
        ).arrange(RIGHT, buff=0.12)
        readout.next_to(row, UP, buff=0.75)

        rule = formula(R"(cA)_{ij} = c\,a_{ij}")
        rule.to_edge(DOWN, buff=1.05)

        self.play(FadeIn(base), Write(arrow), FadeIn(out), FadeIn(readout))
        self.play(Write(rule))
        self.wait(0.4)

        for k in range(2, 6):
            scaled = [[k * v for v in line] for line in self.B]
            target = mat(scaled, WHITE).match_height(out).move_to(out)
            counter = Integer(k).set_color(DONE).move_to(readout[1], LEFT)
            self.play(Transform(out, target),
                      Transform(readout[1], counter),
                      run_time=0.9)
            self.wait(0.35)

        note = caption("성분마다 다른 수를 곱하는 연산이 아님")
        note.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(note, UP))
        self.play(LaggedStartMap(FlashAround, out.get_entries(),
                                 lag_ratio=0.12, run_time=1.6))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 행렬의 곱 — 교재 예제 1-4
# ─────────────────────────────────────────────────────────────
class MatrixProduct(InteractiveScene):
    """(i 행) 과 (j 열) 이 만나 결과의 (i, j) 성분 하나를 만든다.

    계산에 들어가기 전에 크기 조건을 먼저 세운다. 행 하나와 열 하나의 길이가
    같아야 짝을 지어 곱할 수 있다는 것이 곱의 정의 자체다.
    """
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    def construct(self):
        head = slide_title("행렬의 곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        prod = [[sum(self.A[i][t] * self.B[t][j] for t in range(2))
                 for j in range(2)] for i in range(2)]

        a = mat(self.A, ACCENT)
        b = mat(self.B, CALM)
        eq = Tex("=").set_color(GREY_B)
        out = mat(prod, WHITE)

        row = VGroup(a, b, eq, out).arrange(RIGHT, buff=0.5)
        row.move_to(0.55 * UP)
        out.get_entries().set_opacity(0)

        self.play(FadeIn(a), FadeIn(b))

        rule = Tex(R"(m \times n)(n \times p) = m \times p")
        rule.set_color(GREY_A).scale(0.95)
        rule.next_to(row, DOWN, buff=0.9)
        self.play(Write(rule))

        cond = caption("A의 열과 B의 행이 같아야 함", 26, DONE)
        cond.next_to(rule, DOWN, buff=0.4)
        inner = VGroup(box(rule[3], WARN, 0.06), box(rule[6], WARN, 0.06))
        self.play(ShowCreation(inner), FadeIn(cond, UP))
        self.wait(1.2)
        self.play(FadeOut(inner), FadeOut(rule), FadeOut(cond))

        self.play(Write(eq), ShowCreation(out.get_brackets()))

        entry_rule = formula(R"c_{ij} = \sum_{k=1}^{n} a_{ik} b_{kj}", DONE)
        entry_rule.to_edge(DOWN, buff=0.5)
        self.play(Write(entry_rule))

        work = VGroup()
        self.add(work)
        for i in range(2):
            for j in range(2):
                row_box = box(a.get_rows()[i], ACCENT, 0.14)
                col_box = box(b.get_columns()[j], CALM, 0.14)
                terms = " + ".join(
                    R"%d \cdot %d" % (self.A[i][t], self.B[t][j])
                    for t in range(2))
                line = Tex(terms + " = %d" % prod[i][j])
                line.set_color(WHITE).set_width(min(line.get_width(), 8.0))
                line.to_edge(DOWN, buff=2.15)

                self.play(ShowCreation(row_box), ShowCreation(col_box),
                          run_time=0.45)
                self.play(FadeTransform(work, line), run_time=0.6)
                work = line
                self.play(out.get_entries()[i * 2 + j].animate.set_opacity(1),
                          FadeOut(row_box), FadeOut(col_box), run_time=0.5)
        self.wait()

        note = caption("i행과 j열의 길이가 같음")
        note.next_to(entry_rule, UP, buff=0.45)
        self.play(FadeOut(work), FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 곱의 순서 — 교재 예제 1-4
# ─────────────────────────────────────────────────────────────
class ProductOrder(InteractiveScene):
    """AB 와 BA 가 다른 이유는 짝짓는 행과 열이 서로 바뀌기 때문이다.

    두 결과만 늘어놓으면 다르다는 사실만 남는다. A 와 B 를 위에 두고, 같은
    (1, 1) 성분이 어느 행과 어느 열에서 나왔는지 짚는다.
    """
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    def construct(self):
        head = slide_title("곱의 순서")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        ab = [[sum(self.A[i][t] * self.B[t][j] for t in range(2))
               for j in range(2)] for i in range(2)]
        ba = [[sum(self.B[i][t] * self.A[t][j] for t in range(2))
               for j in range(2)] for i in range(2)]

        a = mat(self.A, ACCENT, h_buff=0.7, v_buff=0.45)
        b = mat(self.B, CALM, h_buff=0.7, v_buff=0.45)
        given = VGroup(
            VGroup(Tex("A =").set_color(ACCENT), a).arrange(RIGHT, buff=0.25),
            VGroup(Tex("B =").set_color(CALM), b).arrange(RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=1.6)
        given.move_to(1.75 * UP)
        self.play(FadeIn(given, UP))
        self.wait(0.4)

        left = VGroup(
            Tex("AB =").set_color(GREY_B),
            mat(ab, WHITE, h_buff=0.7, v_buff=0.45),
        ).arrange(RIGHT, buff=0.25)
        right = VGroup(
            Tex("BA =").set_color(GREY_B),
            mat(ba, WHITE, h_buff=0.7, v_buff=0.45),
        ).arrange(RIGHT, buff=0.25)
        pair = VGroup(left, right).arrange(RIGHT, buff=1.6)
        pair.move_to(0.45 * DOWN)

        self.play(FadeIn(left, DOWN))
        self.play(FadeIn(right, DOWN))
        self.wait(0.4)

        # 같은 (1, 1) 자리가 어디에서 나오는지 짚는다.
        for source, target, terms, value in (
                (a, b, R"1 \cdot 5 + 2 \cdot 7", ab[0][0]),
                (b, a, R"5 \cdot 1 + 6 \cdot 3", ba[0][0])):
            src_box = box(source.get_rows()[0], ACCENT if source is a else CALM, 0.1)
            dst_box = box(target.get_columns()[0], CALM if target is b else ACCENT, 0.1)
            line = Tex(terms + " = %d" % value).set_color(WHITE)
            line.next_to(pair, DOWN, buff=0.65)
            self.play(ShowCreation(src_box), ShowCreation(dst_box), run_time=0.5)
            self.play(FadeIn(line, UP), run_time=0.5)
            self.wait(0.9)
            self.play(FadeOut(src_box), FadeOut(dst_box), FadeOut(line),
                      run_time=0.4)

        marks = VGroup(*[
            box(entry, WARN, 0.08)
            for entry in [*left[1].get_entries(), *right[1].get_entries()]
        ])
        self.play(LaggedStartMap(ShowCreation, marks, lag_ratio=0.1,
                                 run_time=1.4))

        verdict = Tex(R"AB \ne BA").set_color(WARN).scale(1.1)
        verdict.next_to(pair, DOWN, buff=0.75)
        self.play(Write(verdict))

        note = caption("짝짓는 행과 열이 서로 바뀜")
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 곱이 정의되는 크기 — 교재 예제 1-5 (b)
# ─────────────────────────────────────────────────────────────
class ProductShapeRule(InteractiveScene):
    """안쪽 두 수가 같을 때만 곱이 정의된다. 되는 경우와 안 되는 경우를 함께 본다.

    교재 예제 1-5 의 네 행렬 중 A 와 B 는 둘 다 3×2 라 AB 가 정의되지 않고,
    C 는 2×3 이라 AC 가 3×3 으로 정의된다. 같은 자료에서 두 경우가 모두 나온다.
    """
    A = [[3, 0], [-1, 2], [1, 1]]
    B = [[-3, -1], [2, 1], [4, 3]]
    C = [[1, 2, 3], [2, 0, 1]]

    def construct(self):
        head = slide_title("곱이 정의되는 크기")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        rule = Tex(R"(m \times n)(n \times p) = m \times p").scale(1.15)
        rule.set_color(GREY_A).move_to(1.9 * UP)
        self.play(Write(rule))
        inner = VGroup(box(rule[3], DONE, 0.07), box(rule[6], DONE, 0.07))
        self.play(ShowCreation(inner))
        self.play(FadeIn(caption("안쪽 두 수가 같아야 함", 26, DONE)
                         .next_to(rule, DOWN, buff=0.4), UP))
        self.wait(1.2)
        self.play(FadeOut(VGroup(*self.mobjects[2:])))

        # 안 되는 경우 — A(3×2) 와 B(3×2)
        a = mat(self.A, ACCENT, h_buff=0.7, v_buff=0.45)
        b = mat(self.B, CALM, h_buff=0.7, v_buff=0.45)
        bad = VGroup(a, b).arrange(RIGHT, buff=0.5).move_to(0.9 * UP)
        tag_a = shape_tag(a, "3 × 2", ACCENT)
        tag_b = shape_tag(b, "3 × 2", CALM)
        self.play(FadeIn(bad), FadeIn(tag_a), FadeIn(tag_b))

        clash = VGroup(box(tag_a[-1], WARN, 0.08), box(tag_b[0], WARN, 0.08))
        self.play(ShowCreation(clash))
        verdict = caption("2 와 3 이 달라 곱이 정의되지 않음", 28, WARN)
        verdict.next_to(VGroup(tag_a, tag_b), DOWN, buff=0.7)
        self.play(FadeIn(verdict, UP))
        self.wait(1.6)
        self.play(FadeOut(VGroup(bad, tag_a, tag_b, clash, verdict)))

        # 되는 경우 — A(3×2) 와 C(2×3)
        ac = [[sum(self.A[i][t] * self.C[t][j] for t in range(2))
               for j in range(3)] for i in range(3)]
        a = mat(self.A, ACCENT, h_buff=0.7, v_buff=0.45)
        c = mat(self.C, CALM, h_buff=0.7, v_buff=0.45)
        eq = Tex("=").set_color(GREY_B)
        out = mat(ac, WHITE, h_buff=0.7, v_buff=0.45)
        good = VGroup(a, c, eq, out).arrange(RIGHT, buff=0.5)
        good.set_width(min(good.get_width(), FRAME_WIDTH - 2.6))
        good.move_to(0.75 * UP)

        tag_a = shape_tag(a, "3 × 2", ACCENT)
        tag_c = shape_tag(c, "2 × 3", CALM)
        tag_o = shape_tag(out, "3 × 3", DONE)

        out.get_entries().set_opacity(0)
        self.play(FadeIn(a), FadeIn(c), Write(eq),
                  ShowCreation(out.get_brackets()),
                  FadeIn(tag_a), FadeIn(tag_c))

        match = VGroup(box(tag_a[-1], DONE, 0.08), box(tag_c[0], DONE, 0.08))
        self.play(ShowCreation(match))
        self.wait(0.8)
        self.play(FadeOut(match))

        reveal = []
        for entry in out.get_entries():
            reveal.append(entry.animate.set_opacity(1))
        self.play(LaggedStart(*reveal, lag_ratio=0.08, run_time=1.6))
        outer = VGroup(box(tag_a[0], DONE, 0.08), box(tag_c[-1], DONE, 0.08))
        self.play(FadeIn(tag_o), ShowCreation(outer))

        note = caption("바깥 두 수가 결과의 크기")
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6. 거듭제곱 — 교재 예제 1-6
# ─────────────────────────────────────────────────────────────
class MatrixPower(InteractiveScene):
    """A 를 거듭 곱하면 오른쪽 위 성분만 -1 씩 쌓인다."""
    A = [[1, -1], [0, 1]]

    def construct(self):
        head = slide_title("행렬의 거듭제곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        powers = []
        current = [row[:] for row in self.A]
        for _ in range(4):
            powers.append([row[:] for row in current])
            current = [[sum(current[i][t] * self.A[t][j] for t in range(2))
                        for j in range(2)] for i in range(2)]

        blocks = VGroup()
        for n, values in enumerate(powers, start=1):
            label = Tex("A^{%d}" % n).set_color(GREY_B)
            block = VGroup(label, mat(values, ACCENT, h_buff=0.7, v_buff=0.5))
            block.arrange(DOWN, buff=0.35)
            blocks.add(block)
        blocks.arrange(RIGHT, buff=0.85)
        blocks.set_width(min(blocks.get_width(), FRAME_WIDTH - 2.0))
        blocks.move_to(0.4 * UP)

        rule = formula(R"A^{k} = A \times A \times \cdots \times A")
        rule.to_edge(DOWN, buff=1.05)
        self.play(Write(rule))

        self.play(FadeIn(blocks[0], UP))
        for block in blocks[1:]:
            self.play(FadeIn(block, UP), run_time=0.7)
        self.wait(0.4)

        corners = VGroup(*[
            box(entry_at(block[1], 0, 1, 2), DONE, 0.1) for block in blocks
        ])
        self.play(LaggedStartMap(ShowCreation, corners, lag_ratio=0.18,
                                 run_time=1.4))

        general = VGroup(
            Tex("A^{n} =").set_color(GREY_B),
            Matrix([["1", "-n"], ["0", "1"]], h_buff=0.9, v_buff=0.5),
        ).arrange(RIGHT, buff=0.3)
        general.set_color(DONE)
        general.next_to(blocks, DOWN, buff=0.85)
        self.play(FadeOut(rule), Write(general))

        note = caption("나머지 세 성분은 그대로")
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 7. 전치행렬 — 교재 정의 1-5
# ─────────────────────────────────────────────────────────────
class Transpose(InteractiveScene):
    """(A^T)_{ij} = a_{ji}. 첨자 두 개가 자리를 바꾼다.

    수만 옮기면 규칙이 보이지 않는다. 일반형 a_{ij} 로 첨자가 뒤집히는 것을 먼저
    보이고, 교재 정의 1-5 의 수 예를 이어 붙인다.
    """
    A = [[9, 7, 3], [4, 8, 9]]

    def move_entries(self, src_mat, dst_mat, rows, cols, run_time):
        """src 의 (i, j) 성분을 dst 의 (j, i) 자리로 옮긴다.

        사본을 직접 들고 있다가 지운다. 애니메이션이 남긴 사본이 원래 성분 위에
        겹쳐 남는 것을 막는다.
        """
        copies = VGroup()
        moves = []
        for i in range(rows):
            for j in range(cols):
                src = entry_at(src_mat, i, j, cols)
                dst = entry_at(dst_mat, j, i, rows)
                clone = src.copy()
                copies.add(clone)
                moves.append(clone.animate.move_to(dst).set_color(WHITE))
        self.add(copies)
        self.play(LaggedStart(*moves, lag_ratio=0.16, run_time=run_time))
        self.remove(copies)
        dst_mat.get_entries().set_opacity(1)

    def construct(self):
        head = slide_title("전치행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # 1단계 — 일반형에서 첨자가 뒤집히는 것
        a = symbol_matrix(2, 3, "a", ACCENT, h_buff=0.7, v_buff=0.5)
        t_values = [["a_{%d%d}" % (i + 1, j + 1) for i in range(2)]
                    for j in range(3)]
        t = mat(t_values, WHITE, h_buff=0.7, v_buff=0.5)

        left = VGroup(Tex("A =").set_color(ACCENT), a).arrange(RIGHT, buff=0.25)
        right = VGroup(Tex("A^{T} =").set_color(WHITE), t).arrange(RIGHT, buff=0.25)
        board = VGroup(left, right).arrange(RIGHT, buff=1.5)
        board.set_width(min(board.get_width(), FRAME_WIDTH - 2.4))
        board.move_to(0.55 * UP)

        t.get_entries().set_opacity(0)
        self.add(board)
        self.play(FadeIn(left), FadeIn(right[0]),
                  ShowCreation(t.get_brackets()))
        self.move_entries(a, t, 2, 3, 2.6)

        rule = formula(R"(A^{T})_{ij} = a_{ji}", DONE, 1.15)
        rule.next_to(board, DOWN, buff=0.75)
        self.play(Write(rule))
        note = caption("첨자 두 개가 자리를 바꿈", 26)
        note.next_to(rule, DOWN, buff=0.4)
        self.play(FadeIn(note, UP))
        self.wait(1.6)

        # 2단계 — 교재 정의 1-5 의 수 예
        self.play(FadeOut(board), FadeOut(note))
        self.remove(board)

        at = [[self.A[i][j] for i in range(2)] for j in range(3)]
        na = mat(self.A, ACCENT, h_buff=0.8, v_buff=0.55)
        nt = mat(at, WHITE, h_buff=0.8, v_buff=0.55)
        left = VGroup(Tex("A =").set_color(ACCENT), na).arrange(RIGHT, buff=0.25)
        right = VGroup(Tex("A^{T} =").set_color(WHITE), nt).arrange(RIGHT, buff=0.25)
        board = VGroup(left, right).arrange(RIGHT, buff=1.5)
        board.move_to(0.55 * UP)
        rule_target = rule.copy()
        rule_target.next_to(board, DOWN, buff=0.75)

        tag_a = shape_tag(na, "2 × 3", ACCENT)
        tag_t = shape_tag(nt, "3 × 2", DONE)

        nt.get_entries().set_opacity(0)
        self.add(board)
        self.play(FadeIn(left), FadeIn(right[0]),
                  ShowCreation(nt.get_brackets()),
                  Transform(rule, rule_target), FadeIn(tag_a))
        self.move_entries(na, nt, 2, 3, 2.2)
        self.play(FadeIn(tag_t))

        back = formula(R"(A^{T})^{T} = A", GREY_A)
        back.next_to(rule, DOWN, buff=0.45)
        self.play(Write(back))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 8. 기본 행 연산 — 교재 정리 1-5
# ─────────────────────────────────────────────────────────────
class RowOperations(InteractiveScene):
    """기본 행 연산(elementary row operation)은 셋뿐이다.

    교재 정리 1-5 의 차례를 그대로 따른다. 스칼라곱 · 교환 · 다른 행에 더하기.
    셋 모두 연립선형방정식의 해집합을 바꾸지 않는다.
    """
    M = [[1, 3, 2], [2, 2, 0], [-3, 1, 1]]

    def construct(self):
        head = slide_title("기본 행 연산")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        naming = Tex(R"\text{elementary row operation}").set_color(GREY_B)
        naming.scale(0.7).next_to(head[1], DOWN, buff=0.25).align_to(head[0], LEFT)
        self.play(FadeIn(naming))

        m = mat(self.M, WHITE, h_buff=0.9)
        m.move_to(4.2 * LEFT + 0.6 * DOWN)
        self.play(FadeIn(m))

        # 교재 정리 1-5 의 차례. 1) 스칼라곱 2) 교환 3) 다른 행에 더하기
        cases = [
            (["1. 한 행에 0이 아닌 스칼라곱", "2행 → (1/2) × 2행"],
             [[1, 3, 2], [1, 1, 0], [-3, 1, 1]], [1]),
            (["2. 행 교환", "1행 ↔ 3행"],
             [[-3, 1, 1], [2, 2, 0], [1, 3, 2]], [0, 2]),
            (["3. 한 행의 상수배를 다른 행에 더하기", "2행 → 2행 + (-2) × 1행"],
             [[1, 3, 2], [0, -4, -4], [-3, 1, 1]], [1]),
        ]

        shown = VGroup()
        self.add(shown)
        for lines, values, rows in cases:
            label = op_label(lines, WARN)
            # 연산 이름이 길어 왼쪽 절반을 넘지 않도록 폭을 맞춘다.
            if label.get_width() > 5.4:
                label.set_width(5.4)
            label.next_to(m, UP, buff=0.55)

            target = mat(values, WHITE, h_buff=0.9).move_to(m)
            marks = VGroup(*[box(m.get_rows()[i], WARN, 0.13) for i in rows])

            self.play(FadeIn(label, UP), ShowCreation(marks), run_time=0.7)
            self.play(Transform(m, target), run_time=1.0)
            self.wait(0.7)

            frozen = mat(values, CALM, h_buff=0.5, v_buff=0.32)
            frozen.set_height(1.25)
            record = VGroup(caption(lines[1], 22, GREY_B), frozen)
            record.arrange(RIGHT, buff=0.5)
            shown.add(record)
            shown.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            shown.move_to(2.7 * RIGHT + 0.4 * DOWN)

            back = mat(self.M, WHITE, h_buff=0.9).move_to(m)
            self.play(FadeOut(marks), FadeOut(label),
                      FadeIn(record), Transform(m, back), run_time=0.9)

        note = caption("세 연산 모두 해집합을 바꾸지 않음")
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 9. 행 사다리꼴 판별 — 교재 예제 1-9
# ─────────────────────────────────────────────────────────────
class EchelonForms(InteractiveScene):
    """선행 성분의 자리가 오른쪽 아래로 내려가는지, 그 위아래가 0 인지 본다."""
    cases = [
        ("(a)", [[1, 1, 0], [0, 4, 1], [0, 0, 1]], "행 사다리꼴",
         "2행의 선행 성분이 1이 아님"),
        ("(b)", [[1, 0, 0, 0], [0, 1, 0, 7], [0, 0, 1, 2]],
         "기약 행 사다리꼴", "선행 1의 위아래가 모두 0"),
        ("(c)", [[1, 0, 0, 4], [0, 1, 1, 0], [0, 0, 0, 0]],
         "기약 행 사다리꼴", "영행이 맨 아래"),
        ("(d)", [[1, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], "행 사다리꼴",
         "4열 선행 1 위에 1이 남음"),
    ]

    def construct(self):
        head = slide_title("행 사다리꼴과 기약 행 사다리꼴")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        shown = VGroup()
        self.add(shown)

        for tag, values, verdict, reason in self.cases:
            m = mat(values, WHITE, h_buff=0.8)
            name = caption(tag, 30, GREY_B)
            name.next_to(m, LEFT, buff=0.6)
            board = VGroup(name, m).move_to(0.6 * UP)

            self.play(FadeIn(board))

            pivots = leading_positions(values)
            n_cols = len(values[0])
            circles = VGroup(*[
                Circle(radius=0.28).set_stroke(DONE, 3).move_to(
                    m.get_entries()[i * n_cols + j])
                for i, j in pivots
            ])
            self.play(LaggedStartMap(ShowCreation, circles, lag_ratio=0.25,
                                     run_time=1.2))

            stair = VMobject().set_stroke(ACCENT, 3)
            points = []
            for i, j in pivots:
                entry = m.get_entries()[i * n_cols + j]
                points.append(entry.get_center() + 0.42 * LEFT + 0.42 * UP)
                points.append(entry.get_center() + 0.42 * RIGHT + 0.42 * UP)
            stair.set_points_as_corners(points)
            self.play(ShowCreation(stair), run_time=1.0)

            color = DONE if verdict.startswith("기약") else CALM
            answer = caption(verdict, 30, color)
            why = caption(reason, 24, GREY_B)
            block = VGroup(answer, why).arrange(DOWN, buff=0.25)
            block.next_to(board, DOWN, buff=0.8)
            self.play(FadeIn(block, UP))
            self.wait(1.4)

            self.play(FadeOut(VGroup(board, circles, stair, block)),
                      run_time=0.5)

        note = caption("선행 성분이 오른쪽 아래로 내려감")
        note.move_to(0.2 * DOWN)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 10. 3차원 이상의 배열 — 교재 1.2 의 텐서 그림 보충
# ─────────────────────────────────────────────────────────────
class ArrayDimensions(InteractiveScene):
    """스칼라 · 벡터 · 행렬 · 3차원 배열. 축이 하나씩 늘어난다.

    교재는 '행렬을 일반화 = 3차원 텐서' 한 줄로 넘어가고, 그 뒤로 다시 다루지
    않는다. Chapter 13 에서 합성곱 필터를 3차원 텐서라고 부르는 것이 전부다.
    축이 하나 늘어나는 자리를 여기서 한 번 보여 둔다.

    화면의 수는 4×4 예시 이미지의 채널값이며 씬 안에서 계산한다.
    """
    size = 4

    def channels(self):
        n = self.size
        red = [[30 * i + 50 * j for j in range(n)] for i in range(n)]
        green = [[200 - 40 * i for _ in range(n)] for i in range(n)]
        blue = [[60 + 20 * j for j in range(n)] for i in range(n)]
        return red, green, blue

    def construct(self):
        head = slide_title("3차원 이상의 배열")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        red, green, blue = self.channels()
        center = 2.1 * RIGHT + 0.35 * DOWN

        rows = VGroup()
        for name, shape in (("스칼라", "( )"), ("벡터", "(4,)"),
                            ("행렬", "(4, 4)"), ("3차원 배열", "(4, 4, 3)")):
            line = VGroup(
                caption(name, 27, GREY_A),
                Tex(shape).set_color(DONE).scale(0.8),
            ).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            rows.add(line)
        rows.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        rows.move_to(4.3 * LEFT + 0.35 * DOWN)
        for line in rows:
            line.set_opacity(0.18)

        self.play(FadeIn(rows))

        # 1. 스칼라 — 한 픽셀의 밝기
        scalar = Tex(str(red[1][1])).set_color(ACCENT).scale(2.0)
        scalar.move_to(center)
        self.play(rows[0].animate.set_opacity(1), FadeIn(scalar))
        note = caption("한 픽셀의 밝기", 25)
        note.next_to(scalar, DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 2. 벡터 — 한 줄
        vector = mat([red[1]], ACCENT, h_buff=0.55, v_buff=0.4)
        vector.set_width(4.0).move_to(center)
        self.play(rows[1].animate.set_opacity(1),
                  ReplacementTransform(scalar, vector),
                  FadeOut(note))
        note = caption("한 줄에 놓인 픽셀 4개", 25)
        note.next_to(vector, DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 3. 행렬 — 흑백 이미지 한 장
        grid = mat(red, ACCENT, h_buff=0.5, v_buff=0.35)
        grid.set_width(4.2).move_to(center)
        self.play(rows[2].animate.set_opacity(1),
                  ReplacementTransform(vector, grid),
                  FadeOut(note))
        note = caption("4 × 4 흑백 이미지 한 장", 25)
        note.next_to(grid, DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 4. 3차원 배열 — 같은 크기가 세 장
        # 세 장에 모두 숫자를 적으면 겹쳐서 읽히지 않는다. 앞 장만 값을 남기고
        # 뒤 두 장은 테두리만 남겨 장이 쌓인 것을 보인다.
        front = mat(red, RED_C, h_buff=0.5, v_buff=0.35)
        front.set_width(4.2).move_to(center)

        sheets = VGroup()
        for values, color, step in ((blue, BLUE_D, 2), (green, GREEN_D, 1)):
            sheet = mat(values, color, h_buff=0.5, v_buff=0.35)
            sheet.set_width(4.2).move_to(center)
            sheet.get_entries().set_opacity(0)
            sheet.get_brackets().set_stroke(color, 2).set_fill(color, 1)
            sheet.shift(step * (0.42 * RIGHT + 0.42 * UP))
            sheets.add(sheet)

        tags = VGroup()
        for target, name, color in ((sheets[0], "B", BLUE_D),
                                    (sheets[1], "G", GREEN_D),
                                    (front, "R", RED_C)):
            tag = Tex(name).set_color(color).scale(0.9)
            tag.next_to(target, UP, buff=0.12).align_to(target, RIGHT)
            tags.add(tag)

        self.play(rows[3].animate.set_opacity(1),
                  ReplacementTransform(grid, front),
                  FadeOut(note))
        self.play(FadeIn(sheets[1], 0.42 * (RIGHT + UP)), FadeIn(tags[1]),
                  run_time=0.7)
        self.play(FadeIn(sheets[0], 0.42 * (RIGHT + UP)), FadeIn(tags[0]),
                  run_time=0.7)
        self.play(FadeIn(tags[2]))

        note = caption("컬러 이미지 = 행렬 3장", 25)
        note.next_to(VGroup(front, sheets), DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        closing = caption("축이 늘면 차원도 늚")
        closing.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(closing, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 11. 성분 표기 — 교재 정의 1-2
# ─────────────────────────────────────────────────────────────
class EntryNotation(InteractiveScene):
    """a_{ij} 의 첨자 두 개가 각각 행 번호와 열 번호를 가리킨다.

    이후의 모든 연산 정의가 이 표기 위에 서 있다. 첨자를 바꾸면 어느 칸이
    켜지는지를 눈으로 확인해 둔다.
    """
    rows = 3
    cols = 4

    def construct(self):
        head = slide_title("행렬의 성분 표기")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        m = symbol_matrix(self.rows, self.cols, "a", WHITE,
                          h_buff=0.75, v_buff=0.6)
        m.move_to(1.1 * LEFT + 0.35 * DOWN)
        self.play(FadeIn(m))

        row_brace = Brace(m, LEFT, buff=0.2).set_color(ACCENT)
        col_brace = Brace(m, DOWN, buff=0.2).set_color(CALM)
        row_label = caption("행 %d개" % self.rows, 26, ACCENT)
        col_label = caption("열 %d개" % self.cols, 26, CALM)
        row_label.next_to(row_brace, LEFT, buff=0.2)
        col_label.next_to(col_brace, DOWN, buff=0.2)

        self.play(GrowFromCenter(row_brace), FadeIn(row_label))
        self.play(GrowFromCenter(col_brace), FadeIn(col_label))

        size = formula(R"%d \times %d" % (self.rows, self.cols), DONE, 1.1)
        size.next_to(m, RIGHT, buff=1.5).shift(1.1 * UP)
        self.play(Write(size))
        self.wait(0.6)

        readout = VGroup()
        self.add(readout)
        marker = VGroup()
        self.add(marker)

        for i, j in ((1, 2), (2, 0), (0, 3)):
            entry = entry_at(m, i, j, self.cols)
            new_marker = box(entry, WARN, 0.14)
            line = VGroup(
                Tex("a_{%d%d}" % (i + 1, j + 1)).set_color(WARN).scale(1.2),
                caption("%d행 %d열" % (i + 1, j + 1), 26, GREY_A),
            ).arrange(DOWN, buff=0.3)
            line.next_to(m, RIGHT, buff=1.5).shift(0.9 * DOWN)

            self.play(FadeTransform(marker, new_marker),
                      FadeTransform(readout, line), run_time=0.7)
            marker, readout = new_marker, line
            self.wait(0.9)

        note = caption("앞 첨자는 행, 뒤 첨자는 열")
        note.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 12. 정방행렬의 주대각선 — 교재 정의 1-3 · 1-4 · 1-5
# ─────────────────────────────────────────────────────────────
class SquareMatrixDiagonal(InteractiveScene):
    """행과 열의 수가 같으면 첨자가 같은 자리, 곧 주대각선이 생긴다.

    대각행렬과 단위행렬은 이 축을 기준으로 정의된다. 수 예는 교재 1.2 절의
    대각행렬 예와 3차 단위행렬을 쓴다.
    """
    n = 3
    diagonal = [[1, 0, 0], [0, 5, 0], [0, 0, 9]]

    def construct(self):
        head = slide_title("정방행렬과 주대각선")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        m = symbol_matrix(self.n, self.n, "a", WHITE, h_buff=0.8, v_buff=0.6)
        m.move_to(3.1 * LEFT + 0.35 * DOWN)
        self.play(FadeIn(m))

        size = caption("행 %d개, 열 %d개 — %d차 정방행렬" % (self.n, self.n, self.n),
                       26, GREY_A)
        size.next_to(m, UP, buff=0.55)
        self.play(FadeIn(size, DOWN))
        self.wait(0.5)

        axis = diagonal_axis(m, self.n)
        marks = VGroup(*[
            box(entry_at(m, i, i, self.n), DONE, 0.12) for i in range(self.n)
        ])
        self.play(ShowCreation(axis))
        self.bring_to_back(axis)
        self.play(LaggedStartMap(ShowCreation, marks, lag_ratio=0.25,
                                 run_time=1.1))

        name = VGroup(
            caption("주대각 성분", 28, DONE),
            Tex("a_{11},\; a_{22},\; a_{33}").set_color(DONE),
        ).arrange(DOWN, buff=0.35)
        name.next_to(m, RIGHT, buff=1.5)
        self.play(FadeIn(name, RIGHT))
        self.wait(1.2)

        # 대각행렬 — 주대각 밖이 모두 0
        self.play(FadeOut(VGroup(marks, name, size)))
        target = mat(self.diagonal, WHITE, h_buff=0.8, v_buff=0.6).move_to(m)
        target.add_background_to_entries()
        new_axis = diagonal_axis(target, self.n)
        self.play(Transform(m, target), Transform(axis, new_axis))
        self.bring_to_back(axis)

        off = VGroup(*[
            box(entry_at(m, i, j, self.n), WARN, 0.1)
            for i in range(self.n) for j in range(self.n) if i != j
        ])
        self.play(LaggedStartMap(ShowCreation, off, lag_ratio=0.06,
                                 run_time=1.2))
        block = VGroup(
            caption("대각행렬", 28, CALM),
            formula(R"a_{ij} = 0 \quad (i \ne j)", WARN),
        ).arrange(DOWN, buff=0.35)
        block.next_to(m, RIGHT, buff=1.5)
        self.play(FadeIn(block, RIGHT))
        self.wait(1.4)

        # 단위행렬 — 주대각이 모두 1
        identity = [[1 if i == j else 0 for j in range(self.n)]
                    for i in range(self.n)]
        target = mat(identity, WHITE, h_buff=0.8, v_buff=0.6).move_to(m)
        target.add_background_to_entries()
        new_block = VGroup(
            caption("단위행렬", 28, DONE),
            formula(R"a_{ii} = 1,\quad a_{ij} = 0 \; (i \ne j)", DONE, 0.85),
        ).arrange(DOWN, buff=0.35)
        new_block.next_to(m, RIGHT, buff=1.5)
        self.play(FadeOut(off), Transform(m, target),
                  FadeTransform(block, new_block))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 13. 대칭행렬 — 교재 정의 1-5 보충
# ─────────────────────────────────────────────────────────────
class SymmetricMatrix(InteractiveScene):
    """주대각선을 축으로 접었을 때 겹치는 행렬이 대칭행렬이다.

    전치는 주대각선을 축으로 한 반사다. 반사해도 그대로면 A = A^T 이고,
    달라지면 대칭행렬이 아니다. 두 경우를 같은 자리에서 비교한다.
    """
    n = 3
    symmetric = [[1, 2, 3], [2, 5, 4], [3, 4, 9]]
    plain = [[1, 2, 3], [0, 5, 4], [7, 8, 9]]
    pairs = [(0, 1), (0, 2), (1, 2)]

    def construct(self):
        head = slide_title("대칭행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        rule = formula(R"a_{ij} = a_{ji} \;\Longleftrightarrow\; A = A^{T}",
                       DONE, 1.0)
        rule.to_edge(DOWN, buff=0.9)

        # 대칭인 경우
        m = mat(self.symmetric, WHITE, h_buff=0.85, v_buff=0.6)
        m.move_to(3.0 * LEFT + 0.35 * DOWN)
        axis = diagonal_axis(m, self.n)
        self.play(FadeIn(m), ShowCreation(axis))
        self.bring_to_back(axis)

        note = caption("주대각선을 축으로 짝을 맞바꿈", 26)
        note.next_to(m, UP, buff=0.55)
        self.play(FadeIn(note, DOWN))

        for i, j in self.pairs:
            upper = entry_at(m, i, j, self.n)
            lower = entry_at(m, j, i, self.n)
            marks = VGroup(box(upper, CALM, 0.1), box(lower, CALM, 0.1))
            self.play(ShowCreation(marks), run_time=0.3)
            self.play(Swap(upper, lower), run_time=0.7)
            self.play(FadeOut(marks), run_time=0.2)

        verdict = VGroup(
            caption("바꿔도 그대로", 28, DONE),
            formula(R"A = A^{T}", DONE, 1.1),
        ).arrange(DOWN, buff=0.35)
        verdict.next_to(m, RIGHT, buff=1.6)
        self.play(FadeIn(verdict, RIGHT), Write(rule))
        self.wait(1.6)

        # 대칭이 아닌 경우
        self.play(FadeOut(VGroup(verdict, note)))
        target = mat(self.plain, WHITE, h_buff=0.85, v_buff=0.6).move_to(m)
        target.add_background_to_entries()
        self.play(Transform(m, target))
        self.bring_to_back(axis)

        for i, j in self.pairs:
            upper = entry_at(m, i, j, self.n)
            lower = entry_at(m, j, i, self.n)
            marks = VGroup(box(upper, WARN, 0.1), box(lower, WARN, 0.1))
            self.play(ShowCreation(marks), run_time=0.3)
            self.play(Swap(upper, lower), run_time=0.7)
            self.play(FadeOut(marks), run_time=0.2)

        verdict = VGroup(
            caption("바꾸면 달라짐", 28, WARN),
            formula(R"A \ne A^{T}", WARN, 1.1),
        ).arrange(DOWN, buff=0.35)
        verdict.next_to(m, RIGHT, buff=1.6)
        self.play(FadeIn(verdict, RIGHT))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 14. 내적 · 외적 · 텐서곱 — 교재 정의 1-9 · 정리 1-3
# ─────────────────────────────────────────────────────────────
class InnerOuterTensor(InteractiveScene):
    """내적과 외적은 새 연산이 아니라 이미 배운 행렬 곱의 두 극단이다.

    (m×n)(n×p) = m×p 한 규칙에서, 행 하나와 열 하나를 곱하면 안쪽 크기가 만나
    수 하나(1×1)로 줄고, 열 하나와 행 하나를 곱하면 바깥 크기가 남아 행렬(m×n)로
    펼쳐진다. 외적의 (i, j) 성분이 u_i v_j 라는 데서 '텐서곱'이라는 이름이 나온다.
    벡터를 하나 더 곱하면 첨자가 셋(u_i v_j x_k)이 되어 3차원 배열이 된다.

    화면의 수는 모두 교재 값이다. 내적은 정리 1-3 뒤의 예 [1 2; 3 4][5; -1] 의
    첫 성분, 외적은 정의 1-9 뒤의 예 u = [2; 5], v = [2; 1; 4], 3차원 배열은
    그 외적에 같은 쪽의 x = [5; -1] 을 세 번째 축으로 곱한 것이다.
    """
    row = [[1, 2]]
    col = [[5], [-1]]
    u = [[2], [5]]
    v = [[2, 1, 4]]
    x = [5, -1]

    def construct(self):
        head = slide_title("내적 · 외적 · 텐서곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        rule = Tex(R"(m \times n)(n \times p) = m \times p")
        rule.set_color(GREY_A).scale(0.9)
        rule.next_to(head, DOWN, buff=0.35).align_to(head[0], LEFT)
        self.play(Write(rule))

        self.inner_product()
        self.outer_product()
        self.tensor()

    # 1. 내적 — 행 하나 × 열 하나 = 수 하나
    def inner_product(self):
        value = sum(a * b for a, b in zip(self.row[0], [c[0] for c in self.col]))

        a = mat(self.row, ACCENT, h_buff=0.7, v_buff=0.45)
        b = mat(self.col, CALM, h_buff=0.7, v_buff=0.45)
        eq = Tex("=").set_color(GREY_B)
        out = mat([[value]], WHITE, h_buff=0.7, v_buff=0.45)
        line = VGroup(a, b, eq, out).arrange(RIGHT, buff=0.45)
        line.move_to(0.35 * UP)
        out.get_entries().set_opacity(0)

        name = caption("내적", 30, DONE).next_to(line, LEFT, buff=1.2)
        shapes = VGroup(shape_tag(a, "1 × 2"), shape_tag(b, "2 × 1"),
                        shape_tag(out, "1 × 1", DONE))

        self.play(FadeIn(name), FadeIn(a), FadeIn(b), Write(eq),
                  ShowCreation(out.get_brackets()))
        self.play(FadeIn(shapes, UP))

        terms = Tex(R"1 \cdot 5 + 2 \cdot (-1) = %d" % value).set_color(WHITE)
        terms.next_to(line, DOWN, buff=1.3)
        marks = VGroup(box(a.get_rows()[0], ACCENT, 0.12),
                       box(b.get_columns()[0], CALM, 0.12))
        self.play(ShowCreation(marks), run_time=0.45)
        self.play(FadeIn(terms, UP), run_time=0.5)
        self.play(out.get_entries().animate.set_opacity(1), FadeOut(marks),
                  run_time=0.5)

        note = caption("안쪽 크기가 만나 수 하나로 줄어듦", 26)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(1.6)
        self.play(FadeOut(VGroup(name, line, shapes, terms, note)))

    # 2. 외적 — 열 하나 × 행 하나 = 행렬
    def outer_product(self):
        u = [r[0] for r in self.u]
        v = self.v[0]
        prod = [[ui * vj for vj in v] for ui in u]

        a = mat(self.u, ACCENT, h_buff=0.7, v_buff=0.45)
        b = mat(self.v, CALM, h_buff=0.7, v_buff=0.45)
        eq = Tex("=").set_color(GREY_B)
        out = mat(prod, WHITE, h_buff=0.75, v_buff=0.45)
        line = VGroup(a, b, eq, out).arrange(RIGHT, buff=0.45)
        line.move_to(0.35 * UP)
        out.get_entries().set_opacity(0)

        name = VGroup(caption("외적", 30, DONE),
                      Tex(R"\mathbf{u}\mathbf{v}^{T}").set_color(DONE).scale(0.9))
        name.arrange(DOWN, buff=0.2).next_to(line, LEFT, buff=1.0)
        shapes = VGroup(shape_tag(a, "2 × 1"), shape_tag(b, "1 × 3"),
                        shape_tag(out, "2 × 3", DONE))

        self.play(FadeIn(name), FadeIn(a), FadeIn(b), Write(eq),
                  ShowCreation(out.get_brackets()))
        self.play(FadeIn(shapes, UP))

        entry_rule = formula(R"(\mathbf{u}\mathbf{v}^{T})_{ij} = u_i v_j", DONE)
        entry_rule.to_edge(DOWN, buff=0.5)
        self.play(Write(entry_rule))

        work = VGroup()
        self.add(work)
        for i in range(2):
            for j in range(3):
                marks = VGroup(box(a.get_rows()[i], ACCENT, 0.1),
                               box(b.get_columns()[j], CALM, 0.1))
                term = Tex(R"%d \cdot %d = %d" % (u[i], v[j], prod[i][j]))
                term.set_color(WHITE).next_to(line, DOWN, buff=1.3)
                self.play(ShowCreation(marks), run_time=0.3)
                self.play(FadeTransform(work, term), run_time=0.35)
                work = term
                self.play(out.get_entries()[i * 3 + j].animate.set_opacity(1),
                          FadeOut(marks), run_time=0.35)

        note = caption("바깥 크기가 남아 행렬로 펼쳐짐", 26)
        note.next_to(entry_rule, UP, buff=0.45)
        self.play(FadeOut(work), FadeIn(note, UP))
        self.wait(1.6)
        self.play(FadeOut(VGroup(name, line, shapes, note, entry_rule)))

    # 3. 텐서곱 — 첨자가 하나 늘면 축이 하나 는다
    def tensor(self):
        u = [r[0] for r in self.u]
        v = self.v[0]
        outer = [[ui * vj for vj in v] for ui in u]
        sheets_values = [[[c * xk for c in row] for row in outer] for xk in self.x]

        center = 1.6 * RIGHT + 0.3 * DOWN
        rows = VGroup()
        for name, shape, tex in (("외적", "(2, 3)", R"u_i v_j"),
                                 ("텐서곱", "(2, 3, 2)", R"u_i v_j x_k")):
            line = VGroup(
                caption(name, 27, GREY_A),
                Tex(shape).set_color(DONE).scale(0.8),
                Tex(tex).set_color(GREY_A).scale(0.8),
            ).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            rows.add(line)
        rows.arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        rows.move_to(4.6 * LEFT + 0.3 * DOWN)
        for line in rows:
            line.set_opacity(0.18)
        self.play(FadeIn(rows))

        grid = mat(outer, WHITE, h_buff=0.75, v_buff=0.45)
        grid.set_width(4.2).move_to(center)
        self.play(rows[0].animate.set_opacity(1), FadeIn(grid))
        self.wait(0.6)

        # 세 번째 벡터 x 를 곱한다. 앞 장은 x_1 배, 뒷장은 x_2 배.
        x_tex = VGroup(Tex(R"\mathbf{x} =").set_color(CALM),
                       mat([[xk] for xk in self.x], CALM, h_buff=0.6, v_buff=0.4))
        x_tex.arrange(RIGHT, buff=0.2).next_to(grid, UP, buff=0.5)
        self.play(FadeIn(x_tex, DOWN))

        front = mat(sheets_values[0], WHITE, h_buff=0.75, v_buff=0.45)
        front.set_width(4.2).move_to(center)
        back = mat(sheets_values[1], GREY_B, h_buff=0.75, v_buff=0.45)
        back.set_width(4.2).move_to(center)
        back.shift(0.42 * (RIGHT + UP))
        back.get_brackets().set_stroke(GREY_B, 2)

        tags = VGroup(
            Tex(R"x_1 = %d" % self.x[0]).set_color(CALM).scale(0.75),
            Tex(R"x_2 = %d" % self.x[1]).set_color(CALM).scale(0.75),
        )
        tags[0].next_to(front, DOWN, buff=0.25)
        tags[1].next_to(back, RIGHT, buff=0.25)

        self.play(rows[1].animate.set_opacity(1),
                  ReplacementTransform(grid, front), FadeIn(tags[0]))
        self.play(FadeIn(back, 0.42 * (RIGHT + UP)), FadeIn(tags[1]),
                  run_time=0.7)
        self.wait(0.6)

        closing = caption("첨자가 하나 늘면 축이 하나 증가", 26)
        closing.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(closing, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 보충. 곱이라 부르는 연산들 — 내적 · 외적 · 크로네커 곱
#
# 교재는 행렬의 곱만 정의하고 넘어간다. 같은 자리에 "내적"과 "외적"이라는
# 이름이 여러 뜻으로 쓰이므로, 크기 규칙으로 갈라 두는 편이 뒤에서 덜 헷갈린다.
# 화면의 값은 모두 numpy 로 확인한 값이다.
# ─────────────────────────────────────────────────────────────
def vec_col(values, color=WHITE, v_buff=0.6):
    """열벡터. n × 1 행렬로 그린다."""
    return mat([[v] for v in values], color, h_buff=0.7, v_buff=v_buff)


def vec_row(values, color=WHITE, h_buff=0.9):
    """행벡터. 1 × n 행렬로 그린다."""
    return mat([values], color, h_buff=h_buff, v_buff=0.6)


def signed(value):
    """식에 넣을 수. 음수면 괄호를 씌워 곱셈 기호와 붙지 않게 한다."""
    if value < 0:
        return "(%d)" % value
    return "%d" % value


def tag_row(items, y, size=24):
    """행렬 여러 개의 크기표를 같은 높이에 나란히 붙인다.

    Parameters
        items (list): (mobject, 표시할 글, 색) 의 목록.
        y (float): 크기표를 놓을 세로 위치.
        size (int): 글자 크기.

    Returns
        VGroup: 붙인 크기표.
    """
    out = VGroup()
    for mobject, text, color in items:
        tag = caption(text, size, color)
        tag.move_to([mobject.get_center()[0], y, 0])
        out.add(tag)
    return out


# 보-1. 벡터의 내적
class VectorInnerProduct(InteractiveScene):
    """내적은 두 벡터를 수 하나로 줄인다. 두 벡터의 차원이 같아야 정의된다.

    값은 교재 예제 2-1 의 계수행렬 1행 (1, 3, 2) 와 그 해 (1, -1, 2) 다.
    같은 짝이 뒤의 `MatrixVectorProduct` 에서 Ax 의 첫 성분으로 다시 나온다.
    """
    u = [1, 3, 2]
    v = [1, -1, 2]

    def construct(self):
        head = slide_title("벡터의 내적")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        total = 0
        for a, b in zip(self.u, self.v):
            total += a * b

        ut = vec_row(self.u, ACCENT)
        vc = vec_col(self.v, CALM)
        eq = Tex("=").set_color(GREY_B)
        answer = Tex(str(total)).set_color(DONE).scale(1.4)

        line = VGroup(ut, vc, eq, answer).arrange(RIGHT, buff=0.5)
        line.move_to(0.85 * UP)
        answer.set_opacity(0)
        self.play(FadeIn(ut), FadeIn(vc))

        tags = tag_row([(ut, "1 × 3", ACCENT), (vc, "3 × 1", CALM)],
                       line.get_bottom()[1] - 0.45)
        self.play(FadeIn(tags))

        cond = caption("안쪽 두 수가 같아야 함", 26, DONE)
        cond.move_to([0, tags.get_bottom()[1] - 0.5, 0])
        self.play(FadeIn(cond, UP))
        self.wait(1.0)
        self.play(FadeOut(cond))

        self.play(Write(eq), answer.animate.set_opacity(1))

        terms = " + ".join(R"%s \cdot %s" % (signed(a), signed(b))
                           for a, b in zip(self.u, self.v))
        work = Tex(terms + " = %d" % total).set_color(WHITE)
        work.move_to([0, tags.get_bottom()[1] - 0.75, 0])
        self.play(Write(work))

        marks = VGroup()
        for k in range(3):
            marks.add(box(ut.get_entries()[k], ACCENT, 0.09))
            marks.add(box(vc.get_entries()[k], CALM, 0.09))
        self.play(LaggedStartMap(ShowCreation, marks, lag_ratio=0.12,
                                 run_time=1.4))
        self.wait(0.6)
        self.play(FadeOut(marks))

        rule = formula(R"\mathbf{u} \cdot \mathbf{v} = \mathbf{u}^{T}\mathbf{v}"
                       R" = \sum_{i=1}^{n} u_i v_i", DONE)
        rule.to_edge(DOWN, buff=0.7)
        self.play(FadeOut(work), Write(rule))

        note = caption("결과는 1 × 1 크기, 곧 스칼라")
        note.next_to(rule, UP, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-2. 벡터의 외적
class VectorOuterProduct(InteractiveScene):
    """외적은 두 벡터를 행렬로 키운다. 차원이 달라도 언제나 정의된다.

    내적이 (1 × n)(n × 1) 이라면 외적은 (n × 1)(1 × m) 이다. 안쪽 두 수가
    둘 다 1 이므로 크기 조건이 걸릴 자리가 없다.
    """
    u = [2, 5]
    v = [2, 1, 4]

    def construct(self):
        head = slide_title("벡터의 외적")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        naming = Tex(R"\text{outer product}").set_color(GREY_B)
        naming.scale(0.7).next_to(head[1], DOWN, buff=0.25)
        naming.align_to(head[0], LEFT)
        self.play(FadeIn(naming))

        product = []
        for a in self.u:
            row = []
            for b in self.v:
                row.append(a * b)
            product.append(row)

        uc = vec_col(self.u, ACCENT)
        vt = vec_row(self.v, CALM)
        eq = Tex("=").set_color(GREY_B)
        out = mat(product, WHITE, h_buff=0.9, v_buff=0.55)

        line = VGroup(uc, vt, eq, out).arrange(RIGHT, buff=0.5)
        line.move_to(0.55 * UP)
        out.get_entries().set_opacity(0)
        self.play(FadeIn(uc), FadeIn(vt))

        tags = tag_row([(uc, "2 × 1", ACCENT), (vt, "1 × 3", CALM),
                        (out, "2 × 3", GREY_B)],
                       line.get_bottom()[1] - 0.45)
        self.play(FadeIn(tags[0]), FadeIn(tags[1]))

        cond = caption("차원이 달라도 정의됨", 26, DONE)
        cond.move_to([0, tags.get_bottom()[1] - 0.5, 0])
        self.play(FadeIn(cond, UP))
        self.wait(1.2)
        self.play(FadeOut(cond))

        self.play(Write(eq), ShowCreation(out.get_brackets()), FadeIn(tags[2]))

        reveal = []
        for i in range(2):
            for j in range(3):
                reveal.append(entry_at(out, i, j, 3).animate.set_opacity(1))
        self.play(LaggedStart(*reveal, lag_ratio=0.15, run_time=1.8))
        self.wait(0.5)

        # 화면에 놓인 이 두 벡터로는 내적을 잡을 수 없다. u 가 2차원, v 가 3차원이라
        # 짝지어 곱할 성분이 모자란다. 외적은 되는데 내적은 안 되는 대조가 요점이다.
        gap = caption("u는 2차원, v는 3차원 — 둘의 내적은 정의되지 않음",
                      26, WARN)
        gap.move_to([0, tags.get_bottom()[1] - 0.55, 0])
        self.play(FadeIn(gap, UP))
        self.wait(1.3)
        self.play(FadeOut(gap))

        rule = formula(R"(\mathbf{u}\mathbf{v}^{T})_{ij} = u_i v_j", DONE)
        rule.to_edge(DOWN, buff=0.55)
        self.play(Write(rule))

        note = caption("모든 행이 v의 상수배 — 랭크가 1인 행렬")
        note.next_to(rule, UP, buff=0.4)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-2b. 한 예로 보는 세 가지 곱 (내적 · 외적 · 행렬곱)
class OneExampleThreeProducts(InteractiveScene):
    """내적 · 외적 · 행렬곱을 한 예에서 잇달아 본다.

    셋을 따로 떼어 각기 다른 수로 보여 주면, 학생이 영상마다 재료를 새로 읽어야 해서
    정작 셋이 어떻게 다른지가 남지 않는다. 그래서 재료를 하나로 고정한다.
    교재 예제 2-1 의 계수행렬 A 와 그 해 x, 그리고 A 의 1행 u 뿐이다.

        내적   u^T x = (1×3)(3×1) = 1×1  →  2
        외적   u x^T = (3×1)(1×3) = 3×3  →  랭크 1 인 행렬
        행렬곱 A x   = (3×3)(3×1) = 3×1  →  (2, 0, -2) = b

    셋 다 같은 규칙 (m×n)(n×p) = m×p 의 서로 다른 경우다. 안쪽 두 수가 만나 사라지고
    바깥 두 수가 결과의 크기로 남는다. 내적과 외적은 같은 두 벡터를 순서만 바꾼 것이라
    수 하나와 3×3 행렬로 갈린다. 행렬곱의 첫 성분은 앞서 구한 내적 그 값이다.
    """
    A = [[1, 3, 2], [2, 2, 0], [-3, 1, 1]]
    x = [1, -1, 2]

    def construct(self):
        self.head = slide_title("한 예로 보는 내적 · 외적 · 행렬곱")
        self.play(FadeIn(self.head[0]), ShowCreation(self.head[1]))

        self.rule = Tex(R"(m \times n)(n \times p) = m \times p")
        self.rule.set_color(GREY_B).scale(0.8)
        self.rule.next_to(self.head[1], DOWN, buff=0.22).align_to(self.head[0], LEFT)
        self.play(FadeIn(self.rule))

        self.u = self.A[0]
        self.materials()
        self.inner()
        self.outer()
        self.matrix_vector()
        self.closing()

    # 1. 재료 — A 와 x, 그리고 A 의 1행
    def materials(self):
        a = mat(self.A, ACCENT, h_buff=0.8, v_buff=0.5)
        xc = vec_col(self.x, CALM, v_buff=0.5)
        group = VGroup(VGroup(Tex("A =").set_color(ACCENT), a).arrange(RIGHT, buff=0.25),
                       VGroup(Tex(R"\mathbf{x} =").set_color(CALM), xc)
                       .arrange(RIGHT, buff=0.25))
        group.arrange(RIGHT, buff=1.5).move_to(0.55 * UP)
        self.play(FadeIn(group, UP))

        note = caption("예제 2-1 의 계수행렬과 해", 27)
        note.next_to(group, DOWN, buff=0.6)
        self.play(FadeIn(note, UP))
        self.wait(1.4)

        row = box(a.get_rows()[0], DONE, 0.12)
        pick = caption("A의 1행을 u로 두고 시작", 26, DONE)
        pick.move_to(note)
        self.play(ShowCreation(row), FadeTransform(note, pick))
        self.wait(1.2)
        self.play(FadeOut(VGroup(group, row, pick)))

    def size_line(self, text, target):
        line = Tex(text).set_color(GREY_A).scale(0.9)
        line.next_to(target, DOWN, buff=0.5)
        return line

    # 2. 내적 — 행 하나 곱하기 열 하나
    def inner(self):
        head = caption("내적", 30, DONE).to_edge(LEFT, buff=1.0).shift(1.15 * UP)
        ut = vec_row(self.u, DONE)
        xc = vec_col(self.x, CALM, v_buff=0.5)
        eq = Tex("=").set_color(GREY_B)
        total = 0
        for a, b in zip(self.u, self.x):
            total += a * b
        out = Tex(str(total)).set_color(WHITE).scale(1.3)

        line = VGroup(ut, xc, eq, out).arrange(RIGHT, buff=0.45).move_to(1.15 * UP)
        self.play(FadeIn(head), FadeIn(ut), FadeIn(xc), Write(eq), FadeIn(out))

        size = self.size_line(R"(1 \times 3)(3 \times 1) = 1 \times 1", line)
        self.play(Write(size))
        terms = Tex(" + ".join(R"%s \cdot %s" % (signed(a), signed(b))
                               for a, b in zip(self.u, self.x)) + " = %d" % total)
        terms.set_color(WHITE).next_to(size, DOWN, buff=0.45)
        self.play(Write(terms))
        self.wait(0.6)

        why = caption("결과는 스칼라", 26, DONE)
        why.next_to(terms, DOWN, buff=0.5)
        self.play(FadeIn(why, UP))
        self.wait(1.6)
        self.play(FadeOut(VGroup(head, line, size, terms, why)))
        self.inner_value = total

    # 3. 외적 — 순서만 바꾼다
    def outer(self):
        head = caption("외적", 30, DONE).to_edge(LEFT, buff=1.0).shift(1.15 * UP)
        product = []
        for a in self.u:
            product.append([a * b for b in self.x])

        uc = vec_col(self.u, DONE, v_buff=0.5)
        xt = vec_row(self.x, CALM)
        eq = Tex("=").set_color(GREY_B)
        out = mat(product, WHITE, h_buff=0.85, v_buff=0.5)

        line = VGroup(uc, xt, eq, out).arrange(RIGHT, buff=0.45).move_to(1.15 * UP)
        out.get_entries().set_opacity(0)
        self.play(FadeIn(head), FadeIn(uc), FadeIn(xt), Write(eq),
                  ShowCreation(out.get_brackets()))

        swap = caption("같은 두 벡터, 순서만 바꿈", 26, WARN)
        swap.next_to(line, DOWN, buff=0.45)
        self.play(FadeIn(swap, UP))
        self.wait(1.0)

        size = self.size_line(R"(3 \times 1)(1 \times 3) = 3 \times 3", line)
        self.play(FadeTransform(swap, size))
        reveal = []
        for i in range(3):
            for j in range(3):
                reveal.append(entry_at(out, i, j, 3).animate.set_opacity(1))
        self.play(LaggedStart(*reveal, lag_ratio=0.09, run_time=1.6))
        self.wait(0.5)

        why = caption("차원이 달라도 정의됨", 26, DONE)
        why.next_to(size, DOWN, buff=0.55)
        self.play(FadeIn(why, UP))
        self.wait(1.5)
        rank = caption("모든 행이 x의 상수배 — 랭크가 1인 행렬", 26)
        rank.move_to(why)
        self.play(FadeTransform(why, rank))
        self.wait(1.4)
        self.play(FadeOut(VGroup(head, line, size, rank)))

    # 4. 행렬곱 — 내적을 행마다 되풀이한다
    def matrix_vector(self):
        head = caption("행렬곱", 30, DONE).to_edge(LEFT, buff=1.0).shift(1.15 * UP)
        result = []
        for i in range(3):
            value = 0
            for k in range(3):
                value += self.A[i][k] * self.x[k]
            result.append(value)

        a = mat(self.A, ACCENT, h_buff=0.8, v_buff=0.5)
        xc = vec_col(self.x, CALM, v_buff=0.5)
        eq = Tex("=").set_color(GREY_B)
        out = vec_col(result, WHITE, v_buff=0.5)

        line = VGroup(a, xc, eq, out).arrange(RIGHT, buff=0.45).move_to(1.15 * UP)
        out.get_entries().set_opacity(0)
        self.play(FadeIn(head), FadeIn(a), FadeIn(xc), Write(eq),
                  ShowCreation(out.get_brackets()))
        size = self.size_line(R"(3 \times 3)(3 \times 1) = 3 \times 1", line)
        self.play(Write(size))

        work = VGroup()
        self.add(work)
        for i in range(3):
            mark = box(a.get_rows()[i], DONE, 0.12)
            terms = Tex(" + ".join(R"%s \cdot %s" % (signed(self.A[i][k]),
                                                     signed(self.x[k]))
                                   for k in range(3)) + " = %d" % result[i])
            terms.set_color(WHITE).scale(0.95)
            terms.next_to(size, DOWN, buff=0.45)
            self.play(ShowCreation(mark), run_time=0.35)
            self.play(FadeTransform(work, terms), run_time=0.5)
            work = terms
            self.play(out.get_entries()[i].animate.set_opacity(1),
                      FadeOut(mark), run_time=0.45)
            if i == 0:
                tie = caption("첫 성분은 앞의 내적", 26, WARN)
                tie.next_to(terms, DOWN, buff=0.45)
                self.play(FadeIn(tie, UP))
                self.wait(1.3)
                self.play(FadeOut(tie))
        self.play(FadeOut(work))

        why = caption("행마다 내적 한 번", 26, DONE)
        why.next_to(size, DOWN, buff=0.6)
        self.play(FadeIn(why, UP))
        self.wait(1.6)
        self.play(FadeOut(VGroup(head, line, size, why)))

    # 5. 정리
    def closing(self):
        rows = [
            ("내적", R"\mathbf{u}^{T}\mathbf{x}", R"(1 \times 3)(3 \times 1)", "1 × 1"),
            ("외적", R"\mathbf{u}\mathbf{x}^{T}", R"(3 \times 1)(1 \times 3)", "3 × 3"),
            ("행렬곱", R"A\mathbf{x}", R"(3 \times 3)(3 \times 1)", "3 × 1"),
        ]
        cells = VGroup()
        for name, mark, size, out in rows:
            cells.add(caption(name, 27, WHITE))
            cells.add(Tex(mark).set_color(DONE).scale(0.85))
            cells.add(Tex(size).set_color(GREY_A).scale(0.8))
            cells.add(caption(out, 26, CALM))
        cells.arrange_in_grid(3, 4, h_buff=1.1, v_buff=0.5, aligned_edge=LEFT)
        cells.move_to(0.75 * UP)
        self.play(LaggedStart(*[FadeIn(cells[4 * k:4 * k + 4], RIGHT)
                                for k in range(3)], lag_ratio=0.3, run_time=1.5))
        self.wait(0.8)

        note = caption("안쪽은 사라지고 바깥이 남음",
                       27, DONE)
        note.next_to(cells, DOWN, buff=0.75)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-3. 벡터곱
class CrossProduct(InteractiveScene):
    """한국어 '외적'은 벡터곱을 가리키기도 한다. 이쪽은 3차원에서만 정의된다.

    성분 공식 u_2v_3 - u_3v_2, u_3v_1 - u_1v_3, u_1v_2 - u_2v_1 을 그대로 적으면
    첨자가 왜 저렇게 도는지 알 수 없다. 그래서 계산을 눈에 보이는 규칙으로 바꾼다.
    u 와 v 를 두 열로 세우고, 구하려는 자리의 **행 하나를 지우면** 네 수가 남는다.
    그 넷을 어긋나게 곱해 빼면 그 성분이다. 가운데 성분만 곱하는 방향이 뒤집힌다.

    값은 교재 예제 2-1 계수행렬의 1행 (1, 3, 2) 와 3행 (-3, 1, 1) 이다. 내적 편의
    첫 벡터와 같은 것을 써서, 같은 자리에서 내적은 수 2 가, 벡터곱은 두 벡터와
    수직인 벡터 (1, -7, 10) 이 나오는 것을 견준다. 세 성분이 모두 0 이 아니라
    가운데의 부호 뒤집힘이 값으로도 드러난다.
    """
    u = [1, 3, 2]
    v = [-3, 1, 1]

    # 성분 k = u[a]v[b] - u[b]v[a]. 지우는 행이 k 이고, 남는 두 행이 (a, b) 다.
    PAIRS = {0: (1, 2), 1: (2, 0), 2: (0, 1)}

    def construct(self):
        head = slide_title("벡터곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        naming = Tex(R"\text{cross product}").set_color(GREY_B)
        naming.scale(0.7).next_to(head[1], DOWN, buff=0.25)
        naming.align_to(head[0], LEFT)
        self.play(FadeIn(naming))

        cross = []
        for k in range(3):
            a, b = self.PAIRS[k]
            cross.append(self.u[a] * self.v[b] - self.u[b] * self.v[a])

        uc = vec_col(self.u, ACCENT, v_buff=0.62)
        times = Tex(R"\times").set_color(GREY_B)
        vc = vec_col(self.v, CALM, v_buff=0.62)
        eq = Tex("=").set_color(GREY_B)
        out = vec_col(cross, WHITE, v_buff=0.62)

        line = VGroup(uc, times, vc, eq, out).arrange(RIGHT, buff=0.5)
        line.move_to(1.15 * UP)
        out.get_entries().set_opacity(0)
        self.play(FadeIn(uc), FadeIn(vc), Write(times))
        self.play(Write(eq), ShowCreation(out.get_brackets()))

        rule = caption("그 행을 지우고 대각선 곱의 차",
                       26, DONE)
        rule.move_to([0, line.get_bottom()[1] - 0.55, 0])
        self.play(FadeIn(rule, UP))
        self.wait(1.0)

        work = VGroup()
        self.add(work)
        for k in range(3):
            a, b = self.PAIRS[k]
            gone = VGroup(uc.get_entries()[k], vc.get_entries()[k])
            plus = Line(uc.get_entries()[a].get_center(),
                        vc.get_entries()[b].get_center())
            plus.set_stroke(DONE, 3)
            minus = Line(uc.get_entries()[b].get_center(),
                         vc.get_entries()[a].get_center())
            minus.set_stroke(WARN, 3)

            terms = Tex(R"%s \cdot %s - %s \cdot %s = %d"
                        % (signed(self.u[a]), signed(self.v[b]),
                           signed(self.u[b]), signed(self.v[a]), cross[k]))
            terms.set_color(WHITE).scale(0.95)
            terms.move_to([0, line.get_bottom()[1] - 1.35, 0])

            self.play(gone.animate.set_opacity(0.18), run_time=0.35)
            self.play(ShowCreation(plus), ShowCreation(minus), run_time=0.5)
            self.play(FadeTransform(work, terms), run_time=0.5)
            work = terms
            self.play(out.get_entries()[k].animate.set_opacity(1), run_time=0.4)
            self.wait(0.45)
            self.play(FadeOut(plus), FadeOut(minus),
                      gone.animate.set_opacity(1), run_time=0.35)
        self.play(FadeOut(work), FadeOut(rule))

        flip = caption("가운데 성분만 곱하는 방향이 뒤집힘", 26, WARN)
        flip.move_to([0, line.get_bottom()[1] - 0.55, 0])
        self.play(FadeIn(flip, UP))
        self.wait(1.1)
        self.play(FadeOut(flip))

        check = Tex(R"\mathbf{u} \cdot (\mathbf{u} \times \mathbf{v}) = 0,"
                    R"\quad \mathbf{v} \cdot (\mathbf{u} \times \mathbf{v}) = 0")
        check.set_color(CALM).scale(0.95)
        check.move_to([0, line.get_bottom()[1] - 0.75, 0])
        self.play(Write(check))
        self.play(FadeIn(caption("결과는 두 벡터 모두와 수직", 26, CALM)
                         .next_to(check, DOWN, buff=0.35), UP))
        self.wait(1.2)

        warn = VGroup(
            caption("3차원에서만 정의됨", 27, WARN),
            caption("한국어 '외적'은 텐서곱과 벡터곱을 함께 가리킴", 27, WARN),
        ).arrange(DOWN, buff=0.22)
        warn.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(warn, UP))
        self.wait(2)


# 보-4. 행렬의 내적
class FrobeniusInner(InteractiveScene):
    """행렬끼리도 내적을 잡는다. 같은 자리 성분을 곱해 모두 더한 수 하나다.

    값은 교재 예제 1-3 의 A, B 를 그대로 쓴다.
    """
    A = [[1, 0], [2, 1], [4, 3]]
    B = [[4, 3], [1, 1], [0, 2]]

    def construct(self):
        head = slide_title("행렬의 내적")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        naming = Tex(R"\text{Frobenius inner product}").set_color(GREY_B)
        naming.scale(0.7).next_to(head[1], DOWN, buff=0.25)
        naming.align_to(head[0], LEFT)
        self.play(FadeIn(naming))

        a = mat(self.A, ACCENT, h_buff=0.8, v_buff=0.5)
        b = mat(self.B, CALM, h_buff=0.8, v_buff=0.5)
        pair = VGroup(a, b).arrange(RIGHT, buff=1.5).move_to(0.9 * UP)
        self.play(FadeIn(a), FadeIn(b))

        tags = tag_row([(a, "3 × 2", ACCENT), (b, "3 × 2", CALM)],
                       pair.get_bottom()[1] - 0.4)
        self.play(FadeIn(tags))
        cond = caption("같은 크기일 때만 정의됨", 26, DONE)
        cond.move_to([0, tags.get_bottom()[1] - 0.45, 0])
        self.play(FadeIn(cond, UP))
        self.wait(0.9)
        self.play(FadeOut(cond))

        total = 0
        parts = []
        for i in range(3):
            for j in range(2):
                total += self.A[i][j] * self.B[i][j]
                parts.append(R"%d \cdot %d" % (self.A[i][j], self.B[i][j]))

        running = VGroup()
        self.add(running)
        marks = VGroup()
        self.add(marks)
        for k in range(6):
            i, j = k // 2, k % 2
            pick = VGroup(box(entry_at(a, i, j, 2), ACCENT, 0.08),
                          box(entry_at(b, i, j, 2), CALM, 0.08))
            step = Tex(" + ".join(parts[:k + 1])).set_color(WHITE)
            step.set_width(min(step.get_width(), 9.5))
            step.move_to([0, tags.get_bottom()[1] - 0.8, 0])
            self.play(FadeTransform(marks, pick),
                      FadeTransform(running, step), run_time=0.45)
            marks, running = pick, step
        self.play(FadeOut(marks))

        answer = Tex(" + ".join(parts) + " = %d" % total).set_color(DONE)
        answer.set_width(min(answer.get_width(), 10.5))
        answer.move_to(running)
        self.play(FadeTransform(running, answer))
        running = answer
        self.wait(0.8)

        rule = formula(R"\langle A, B \rangle = \sum_{i,j} a_{ij} b_{ij}"
                       R" = \mathrm{tr}(A^{T}B) = %d" % total, DONE)
        rule.to_edge(DOWN, buff=0.7)
        self.play(FadeOut(running), Write(rule))

        note = caption("성분별 곱을 모두 더해 얻은 스칼라")
        note.next_to(rule, UP, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-5. 크로네커 곱
class KroneckerProduct(InteractiveScene):
    """행렬의 외적. 성분마다 상대 행렬 전체를 붙여 크기를 곱한 만큼 키운다.

    값은 교재 예제 1-4 의 A, B 를 그대로 쓴다. 같은 두 행렬로 AB 는 2 × 2,
    크로네커 곱은 4 × 4 가 된다.
    """
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]

    def construct(self):
        head = slide_title("크로네커 곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        naming = Tex(R"\text{Kronecker product}").set_color(GREY_B)
        naming.scale(0.7).next_to(head[1], DOWN, buff=0.25)
        naming.align_to(head[0], LEFT)
        self.play(FadeIn(naming))

        big = []
        for i in range(2):
            for p in range(2):
                row = []
                for j in range(2):
                    for q in range(2):
                        row.append(self.A[i][j] * self.B[p][q])
                big.append(row)

        a = mat(self.A, ACCENT, h_buff=0.7, v_buff=0.45)
        sign = Tex(R"\otimes").set_color(GREY_B)
        b = mat(self.B, CALM, h_buff=0.7, v_buff=0.45)
        eq = Tex("=").set_color(GREY_B)
        out = mat(big, WHITE, h_buff=0.75, v_buff=0.45)
        out.set_height(2.9)

        line = VGroup(a, sign, b, eq, out).arrange(RIGHT, buff=0.42)
        line.set_width(min(line.get_width(), 11.8))
        line.move_to(0.55 * UP)
        out.get_entries().set_opacity(0)

        self.play(FadeIn(a), Write(sign), FadeIn(b))
        self.play(Write(eq), ShowCreation(out.get_brackets()))

        for i in range(2):
            for j in range(2):
                cell = box(entry_at(a, i, j, 2), WARN, 0.07)
                block = VGroup()
                for p in range(2):
                    for q in range(2):
                        block.add(entry_at(out, 2 * i + p, 2 * j + q, 4))
                frame = SurroundingRectangle(block, buff=0.12)
                frame.set_stroke(WARN, 3)
                label = Tex(R"%d B" % self.A[i][j]).set_color(WARN).scale(0.8)
                label.next_to(frame, UP, buff=0.12)

                self.play(ShowCreation(cell), run_time=0.35)
                self.play(block.animate.set_opacity(1),
                          ShowCreation(frame), FadeIn(label), run_time=0.6)
                self.wait(0.35)
                self.play(FadeOut(cell), FadeOut(frame), FadeOut(label),
                          run_time=0.3)

        rule = Tex(R"(m \times n) \otimes (p \times q) = mp \times nq")
        rule.set_color(GREY_A).scale(0.95)
        rule.next_to(line, DOWN, buff=0.7)
        self.play(Write(rule))

        note = caption("크기 조건 없음", 27, DONE)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-6. 행렬과 벡터의 곱
class MatrixVectorProduct(InteractiveScene):
    """Ax 의 각 성분은 A의 한 행과 x의 내적이다.

    값은 교재 예제 2-1 의 계수행렬과 그 해를 쓴다. 곱한 결과가 상수벡터 b 다.
    """
    A = [[1, 3, 2], [2, 2, 0], [-3, 1, 1]]
    x = [1, -1, 2]

    def construct(self):
        head = slide_title("행렬과 벡터의 곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        result = []
        for i in range(3):
            value = 0
            for k in range(3):
                value += self.A[i][k] * self.x[k]
            result.append(value)

        a = mat(self.A, ACCENT, h_buff=0.8, v_buff=0.5)
        xc = vec_col(self.x, CALM, v_buff=0.5)
        eq = Tex("=").set_color(GREY_B)
        out = vec_col(result, WHITE, v_buff=0.5)

        line = VGroup(a, xc, eq, out).arrange(RIGHT, buff=0.45)
        line.move_to(0.75 * UP)
        out.get_entries().set_opacity(0)
        self.play(FadeIn(a), FadeIn(xc))

        tags = tag_row([(a, "3 × 3", ACCENT), (xc, "3 × 1", CALM),
                        (out, "3 × 1", GREY_B)],
                       line.get_bottom()[1] - 0.45)
        self.play(FadeIn(tags[0]), FadeIn(tags[1]))
        self.play(Write(eq), ShowCreation(out.get_brackets()), FadeIn(tags[2]))

        work = VGroup()
        self.add(work)
        for i in range(3):
            row_box = box(a.get_rows()[i], ACCENT, 0.12)
            col_box = box(xc.get_entries(), CALM, 0.12)
            terms = " + ".join(
                R"%d \cdot (%d)" % (self.A[i][k], self.x[k])
                if self.x[k] < 0 else R"%d \cdot %d" % (self.A[i][k], self.x[k])
                for k in range(3))
            step = Tex(terms + " = %d" % result[i]).set_color(WHITE)
            step.set_width(min(step.get_width(), 9.0))
            step.move_to([0, tags.get_bottom()[1] - 0.8, 0])

            self.play(ShowCreation(row_box), ShowCreation(col_box),
                      run_time=0.4)
            self.play(FadeTransform(work, step), run_time=0.55)
            work = step
            self.play(out.get_entries()[i].animate.set_opacity(1),
                      FadeOut(row_box), FadeOut(col_box), run_time=0.45)
        self.play(FadeOut(work))

        rule = formula(R"(A\mathbf{x})_i = \sum_{k=1}^{n} a_{ik} x_k", DONE)
        rule.to_edge(DOWN, buff=0.55)
        self.play(Write(rule))

        note = caption("행렬방정식 Ax = b 의 좌변")
        note.next_to(rule, UP, buff=0.4)
        self.play(FadeIn(note, UP))
        self.wait(2)


# 보-7. 곱의 크기 규칙
class ProductSizeMap(InteractiveScene):
    """이름이 '곱'인 연산들을 크기 규칙으로 갈라 둔다.

    조건이 붙는 쪽(내적 · 행렬의 곱)과 붙지 않는 쪽(외적 · 크로네커 곱)이
    나뉜다. 벡터곱만 차원 자체가 3으로 묶인다.
    """
    rows = [
        ("벡터의 내적", R"\mathbf{u}^{T}\mathbf{v}", R"(1 \times n)(n \times 1)",
         "스칼라", True),
        ("벡터의 외적", R"\mathbf{u}\mathbf{v}^{T}", R"(n \times 1)(1 \times m)",
         "n × m 행렬", False),
        ("벡터곱", R"\mathbf{u} \times \mathbf{v}", R"n = 3",
         "3차원 벡터", True),
        ("행렬의 내적", R"\mathrm{tr}(A^{T}B)", R"(m \times n),\ (m \times n)",
         "스칼라", True),
        ("행렬의 곱", R"AB", R"(m \times n)(n \times p)", "m × p 행렬", True),
        ("크로네커 곱", R"A \otimes B", None, "mp × nq 행렬", False),
    ]

    def construct(self):
        head = slide_title("곱의 크기 규칙")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        header = ["연산", "표기", "크기 조건", "결과"]
        cells = VGroup()
        for text in header:
            cells.add(caption(text, 26, DONE))
        for name, mark, cond, result, _ in self.rows:
            cells.add(caption(name, 25, WHITE))
            cells.add(Tex(mark).set_color(ACCENT).scale(0.75))
            if cond is None:
                cells.add(caption("조건 없음", 24, GREY_A))
            else:
                cells.add(Tex(cond).set_color(GREY_A).scale(0.7))
            cells.add(caption(result, 24, CALM))

        cells.arrange_in_grid(len(self.rows) + 1, 4, h_buff=1.0, v_buff=0.45,
                              aligned_edge=LEFT)
        cells.set_width(min(cells.get_width(), 11.0))
        cells.move_to(0.45 * DOWN)

        rule = Line(LEFT, RIGHT).set_stroke(GREY_C, 2)
        rule.set_width(cells.get_width() + 0.4)
        rule.next_to(cells[:4], DOWN, buff=0.22)
        rule.match_x(cells)

        self.play(FadeIn(cells[:4]), ShowCreation(rule))
        for k in range(len(self.rows)):
            band = cells[4 * (k + 1):4 * (k + 2)]
            self.play(FadeIn(band, RIGHT), run_time=0.45)
        self.wait(0.8)

        # 크기 조건이 붙는 연산과 붙지 않는 연산을 갈라 표시한다.
        strict = VGroup()
        free = VGroup()
        for k, item in enumerate(self.rows):
            band = cells[4 * (k + 1):4 * (k + 2)]
            frame = SurroundingRectangle(band, buff=0.1)
            frame.set_stroke(WARN if item[4] else CALM, 2.5)
            (strict if item[4] else free).add(frame)

        self.play(ShowCreation(strict), run_time=1.0)
        left_note = caption("크기가 맞아야 정의됨", 26, WARN)
        left_note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(left_note, UP))
        self.wait(1.2)

        self.play(FadeOut(strict), ShowCreation(free), run_time=1.0)
        right_note = caption("크기 조건 없이 언제나 정의됨", 26, CALM)
        right_note.move_to(left_note)
        self.play(FadeTransform(left_note, right_note))
        self.wait(2)
