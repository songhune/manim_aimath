"""AI기초수학 — 교재 Chapter 3 벡터공간과 내적.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 03_벡터공간과 내적.pptx` 의
3.1 벡터와 벡터공간 · 3.2 벡터의 내적 · 3.3 벡터의 미분에 붙는 보조 영상 19편.
수는 교재 정의 3-1~3-22 와 예제 3-1~3-27 의 값을 그대로 쓴다.
파일 이름은 앞 장과 같은 규칙이다(week02 = CH01, week03 = CH02, week04 = CH03).

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week04.py
    ./render.sh check _2026/aimath/week04.py
    ./render.sh ppt   _2026/aimath/week04.py VectorNorm
    ./render.sh all   _2026/aimath/week04.py
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

    판정의 원본은 `_harness/harness_rules.py` 이고 `./render.sh` 가 렌더 전에 부른다.
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


def caption(text, size=26, color=GREY_B):
    """화면 문구. 명사구나 짧은 구절만 받는다(하네스 3.6)."""
    check_words(text)
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def code(text, size=24, color=CALM):
    """화면에 놓는 코드 한 줄. 강의자료 파이썬 코드와 글자 하나까지 같아야 한다."""
    stripped = text.lstrip(" ")
    mob = Text(stripped, font="D2Coding", font_size=size).set_color(color)
    mob.indent = len(text) - len(stripped)
    return mob


def slide_title(text):
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def tag_under(head, text, color=GREY_B):
    """제목 아래 작은 꼬리표. 정의·예제 번호를 적는다."""
    t = caption(text, 22, color)
    t.next_to(head, DOWN, buff=0.25).align_to(head, LEFT)
    return t


def col(values, color=WHITE, v_buff=0.5):
    """열벡터."""
    m = Matrix([[str(v)] for v in values], v_buff=v_buff, bracket_h_buff=0.15)
    m.set_color(color)
    return m


def box(mobject, color=WARN, buff=0.12):
    return SurroundingRectangle(mobject, buff=buff).set_stroke(color, 3)


def plane(x_range=(-1, 5, 1), y_range=(-1, 4, 1), height=5.0):
    """옅은 격자. 벡터가 놓이는 자리다."""
    p = NumberPlane(
        x_range=x_range, y_range=y_range, faded_line_ratio=0,
        background_line_style=dict(stroke_color=GREY_D, stroke_width=1,
                                   stroke_opacity=0.6),
        axis_config=dict(stroke_color=GREY_B, stroke_width=2),
    )
    p.set_height(height)
    return p


def arrow(p, coords, color, start=(0, 0)):
    """격자 좌표로 놓는 화살표."""
    a = Arrow(p.c2p(*start), p.c2p(*coords), buff=0, thickness=4)
    a.set_color(color)
    return a


def vlabel(a, tex, color, direction=UR, buff=0.1):
    return Tex(tex).set_color(color).scale(0.9).next_to(a.get_end(), direction, buff=buff)


def check_mark(color=DONE):
    return Tex(R"\checkmark").set_color(color)


def cross_mark(color=WARN):
    return Tex(R"\times").set_color(color)


# ─────────────────────────────────────────────────────────────
# 3.1 벡터와 벡터공간
# ─────────────────────────────────────────────────────────────
# 도입 두 편. 정의 3-1 부터 성분 계산으로 들어가기 전에, 좌표평면에서 벡터가 무엇이고
# 벡터공간이 무엇인지 그림으로 세운다.
# 참고: legacy/_2016/eola/chapter1.py (3blue1brown, Essence of Linear Algebra)
#   HowIWantYouToThinkAboutVectors · CoordinateSystemWalkthrough · ListsOfNumbersAddOn
# 원본의 Pi creature 장면은 가져오지 않고, 좌표축·화살표·성분 상자만 물려받는다.
X_COLOR = GREEN_C
Y_COLOR = RED_C
Z_COLOR = BLUE_C


class VectorsOnCoordinatePlane(InteractiveScene):
    """벡터 = 원점에서 시작하는 화살표 = 수의 목록. 좌표평면이 그 둘을 잇는다."""

    def construct(self):
        head = slide_title("좌표평면 위의 벡터")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "3.1 도입 · 정의 3-1 앞")))

        p = plane((-5, 5, 1), (-3, 4, 1), 5.2)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        axes = VGroup(p.get_x_axis().copy(), p.get_y_axis().copy()).set_stroke(GREY_A, 3)

        # 1. 화살표 하나 — 꼬리는 원점
        v = arrow(p, (-2, 3), DONE)
        self.play(GrowArrow(v))
        tail = Dot(p.c2p(0, 0), color=WARN)
        tl = caption("꼬리는 원점", 22, WARN).next_to(tail, DR, buff=0.12)
        self.play(FadeIn(tail, scale=2), FadeIn(tl))
        self.wait(0.6)
        self.play(FadeOut(tl))

        # 2. 좌표축과 격자
        xl = Tex("x").set_color(GREY_A).next_to(p.c2p(5, 0), RIGHT, buff=0.1)
        yl = Tex("y").set_color(GREY_A).next_to(p.c2p(0, 4), UP, buff=0.1)
        self.play(ShowCreation(axes[0]), FadeIn(xl))
        self.play(ShowCreation(axes[1]), FadeIn(yl))
        unit = Brace(Line(p.c2p(0, 0), p.c2p(1, 0)), DOWN, buff=0.08).set_color(GREY_B)
        one = Tex("1").set_color(GREY_B).scale(0.8).next_to(unit, DOWN, buff=0.08)
        self.play(GrowFromCenter(unit), FadeIn(one))
        self.wait(0.4)
        self.play(FadeOut(unit), FadeOut(one), FadeIn(p), Animation(axes), Animation(v))
        self.wait(0.3)

        # 3. 성분 두 개
        xline = Line(p.c2p(0, 0), p.c2p(-2, 0)).set_stroke(X_COLOR, 6)
        yline = Line(p.c2p(-2, 0), p.c2p(-2, 3)).set_stroke(Y_COLOR, 6)
        column = Matrix([["-2"], ["3"]], v_buff=0.55, bracket_h_buff=0.15)
        column.get_entries()[0].set_color(X_COLOR)
        column.get_entries()[1].set_color(Y_COLOR)
        column.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(FadeIn(column))
        xn = caption("왼쪽으로 2", 22, X_COLOR).next_to(xline, DOWN, buff=0.1)
        yn = caption("위로 3", 22, Y_COLOR).next_to(yline, LEFT, buff=0.1)
        self.play(ShowCreation(xline), FadeIn(xn))
        self.play(ShowCreation(yline), FadeIn(yn))
        note = caption("화살표 하나 = 수 두 개", 24, DONE).next_to(column, DOWN, buff=0.5).align_to(column, LEFT)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        # 4. 벡터 여럿과 그 목록
        self.play(FadeOut(VGroup(xline, yline, xn, yn)))
        others = [((1, 2), TEAL_B), ((2, -1), PURPLE_B), ((4, 0), PINK)]
        arrows = VGroup(*[arrow(p, c, col) for c, col in others])
        cols = VGroup(*[Matrix([[str(c[0])], [str(c[1])]], v_buff=0.55, bracket_h_buff=0.15).set_color(col)
                        for c, col in others])
        row = VGroup(column, *cols).arrange(RIGHT, buff=0.45)
        row.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(column.animate.move_to(row[0]))
        for a, c in zip(arrows, cols):
            self.play(GrowArrow(a), FadeIn(c), run_time=0.6)
        note2 = caption("첫 수는 가로 · 둘째 수는 세로", 24, DONE).move_to(note).align_to(row, LEFT)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        # 5. 점으로 읽어도 같은 두 수
        pt = Dot(p.c2p(-4, 2), color=WHITE)
        ptl = Tex("(-4,\,2)").set_color(WHITE).scale(0.8).next_to(pt, DOWN, buff=0.1)
        pa = arrow(p, (-4, 2), WHITE)
        self.play(FadeIn(pt, scale=2), FadeIn(ptl))
        self.play(GrowArrow(pa))
        note3 = caption("점으로 읽어도 같은 두 수", 24, GREY_B).move_to(note2).align_to(row, LEFT)
        self.play(FadeTransform(note2, note3))
        self.wait(0.8)

        # 6. 세 수, n 개의 수
        three = Matrix([["2"], ["1"], ["3"]], v_buff=0.5, bracket_h_buff=0.15)
        for k, col in enumerate((X_COLOR, Y_COLOR, Z_COLOR)):
            three.get_entries()[k].set_color(col)
        n_vec = Tex(R"(x_1,\,x_2,\,\ldots,\,x_n)").set_color(INK)
        tail_g = VGroup(three, n_vec).arrange(RIGHT, buff=0.8)
        tail_g.next_to(note3, DOWN, buff=0.6).align_to(row, LEFT)
        self.play(FadeIn(three, UP))
        last = caption("n 개의 수는 n 차원", 24, DONE)
        last.next_to(tail_g, DOWN, buff=0.4).align_to(row, LEFT)
        self.play(FadeIn(n_vec, UP))
        self.play(FadeIn(last, UP))
        self.wait(2)


class VectorSpaceAsPlane(InteractiveScene):
    """좌표평면 전체가 벡터공간이다. 정의 3-3 의 목록은 이 그림의 성질을 적은 것이다."""

    def construct(self):
        head = slide_title("좌표평면이 곧 벡터공간")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "3.1 도입 · 정의 3-3 앞")))

        p = plane((-4, 4, 1), (-3, 3, 1), 5.0)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        # 1. 모든 화살표의 모임
        rng = np.random.default_rng(3)
        faint = VGroup(*[arrow(p, (float(x), float(y)), GREY_C)
                         for x, y in zip(rng.uniform(-3.5, 3.5, 14), rng.uniform(-2.7, 2.7, 14))]).set_opacity(0.35)
        self.play(FadeIn(faint, lag_ratio=0.05), run_time=1.2)
        r2 = Tex(R"\mathbb{R}^2 = \{(x,\,y)\mid x,\,y\in\mathbb{R}\}").set_color(INK)
        r2.set_width(5.2).next_to(p, RIGHT, buff=0.8).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(r2))
        note = caption("평면의 화살표 전부가 한 집합", 24, GREY_B).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 2. 더해도 늘려도 그 안
        self.play(faint.animate.set_opacity(0.12))
        x = arrow(p, (2, 1), ACCENT)
        y = arrow(p, (-1, 2), CALM)
        s = arrow(p, (1, 3), DONE)
        ghost = DashedLine(p.c2p(2, 1), p.c2p(1, 3)).set_stroke(CALM, 2)
        self.play(GrowArrow(x), GrowArrow(y))
        self.play(ShowCreation(ghost), GrowArrow(s))
        two = arrow(p, (-1.5, 3), DONE)
        self.play(FadeOut(ghost), FadeOut(s), GrowArrow(two))
        note2 = caption("더해도 늘려도 평면 안", 24, DONE).move_to(note)
        self.play(FadeTransform(note, note2))
        rules = VGroup(
            Tex(R"\mathbf{x}+\mathbf{y}\in\mathbb{R}^2").set_color(DONE),
            Tex(R"\alpha\mathbf{x}\in\mathbb{R}^2").set_color(DONE),
        ).arrange(RIGHT, buff=0.8)
        rules.next_to(r2, DOWN, buff=0.5).align_to(r2, LEFT)
        self.play(FadeIn(rules, UP))
        self.wait(1.0)

        # 3. 같은 성질을 가진 다른 집합들
        family = VGroup(
            Tex(R"\mathbb{R}^3,\ \mathbb{R}^n").set_color(INK),
            Tex(R"M_{m\times n}(\mathbb{R})").set_color(INK),
            Tex(R"\{a_0+a_1x+\cdots+a_nx^n\}").set_color(INK),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        family.set_width(4.4).next_to(rules, DOWN, buff=0.55).align_to(r2, LEFT)
        for line in family:
            self.play(FadeIn(line, UP), run_time=0.5)
        note3 = caption("행렬 · 다항식도 같은 성질", 24, GREY_B).next_to(family, DOWN, buff=0.35).align_to(r2, LEFT)
        self.play(FadeIn(note3, UP))
        self.wait(0.6)
        last = caption("정의 3-3 은 이 성질의 목록", 24, DONE).move_to(note2)
        self.play(FadeTransform(note2, last))
        self.wait(2)


class VectorOperations(InteractiveScene):
    """정의 3-1 · 3-2 와 예제 3-1. 그림은 2차원, 수는 예제의 3차원 값이다."""

    def construct(self):
        head = slide_title("벡터의 합 · 차 · 스칼라곱")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-1 · 3-2 · 예제 3-1")))

        p = plane((-3, 5, 1), (-3, 4, 1), 5.0)
        p.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        x = arrow(p, (2, 1), ACCENT)
        y = arrow(p, (1, 2), CALM)
        xl = vlabel(x, R"\mathbf{x}", ACCENT, DR)
        yl = vlabel(y, R"\mathbf{y}", CALM, UL)
        self.play(GrowArrow(x), FadeIn(xl), GrowArrow(y), FadeIn(yl))

        ghost = DashedLine(p.c2p(2, 1), p.c2p(3, 3)).set_stroke(CALM, 2)
        s = arrow(p, (3, 3), DONE)
        sl = vlabel(s, R"\mathbf{x}+\mathbf{y}", DONE, UR)
        self.play(ShowCreation(ghost))
        self.play(GrowArrow(s), FadeIn(sl))
        note = caption("머리에 꼬리를 잇기", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 차 — 반대 방향 벡터를 더한다
        ny = arrow(p, (-1, -2), WARN)
        nyl = vlabel(ny, R"-\mathbf{y}", WARN, DL)
        d = arrow(p, (1, -1), DONE)
        dl = vlabel(d, R"\mathbf{x}-\mathbf{y}", DONE, DR)
        self.play(FadeOut(ghost), FadeOut(s), FadeOut(sl))
        self.play(GrowArrow(ny), FadeIn(nyl))
        self.play(GrowArrow(d), FadeIn(dl))
        note2 = caption("반대 벡터를 더하기", 24, DONE).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(0.8)

        # 스칼라곱 — 같은 직선 위
        self.play(FadeOut(VGroup(ny, nyl, d, dl, y, yl)))
        two = arrow(p, (4, 2), DONE)
        twol = vlabel(two, R"2\mathbf{x}", DONE, UR)
        neg = arrow(p, (-2, -1), WARN)
        negl = vlabel(neg, R"-\mathbf{x}", WARN, DOWN)
        self.play(GrowArrow(two), FadeIn(twol))
        self.play(GrowArrow(neg), FadeIn(negl))
        note3 = caption("같은 직선 위에서 늘리고 뒤집기", 24, DONE).move_to(note)
        self.play(FadeTransform(note2, note3))
        self.wait(0.6)

        # 예제 3-1 — 성분끼리
        lines = VGroup(
            Tex(R"\mathbf{x}=(1,\,3,\,-6),\quad \mathbf{y}=(2,\,-1,\,3)").set_color(INK),
            Tex(R"\mathbf{x}+\mathbf{y}=(3,\,2,\,-3)").set_color(DONE),
            Tex(R"\mathbf{x}-\mathbf{y}=(-1,\,4,\,-9)").set_color(DONE),
            Tex(R"3\mathbf{x}=(3,\,9,\,-18)").set_color(DONE),
            Tex(R"5\mathbf{y}=(10,\,-5,\,15)").set_color(DONE),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        lines.set_width(5.6).next_to(p, RIGHT, buff=0.9).align_to(p, UP)
        for line in lines:
            self.play(FadeIn(line, UP), run_time=0.5)
            self.wait(0.3)
        last = caption("성분끼리 계산", 24, GREY_B).next_to(lines, DOWN, buff=0.5)
        self.play(FadeIn(last, UP))
        self.wait(2)


class ClosedUnderOperations(InteractiveScene):
    """정의 3-3 의 열 조건을 그림으로 하나씩 확인한다.

    (1)·(6) 이 '닫힘' 이고 나머지는 합과 스칼라곱의 계산 규칙이다. 규칙마다 평면에서
    한 번씩 보이고 표에 ✓ 를 단다. 끝에 닫히지 않는 집합 둘(1사분면 · 단위원)을 본다.
    """
    x = (2, 1)
    y = (-1, 2)
    z = (2, -1)

    def construct(self):
        head = slide_title("벡터공간의 조건")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-3 · 열 조건")))

        p = plane((-4, 4, 1), (-3, 3, 1), 4.7)
        p.to_edge(LEFT, buff=0.4).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        items = [
            R"(1)\ \mathbf{x}+\mathbf{y}\in V",
            R"(2)\ \mathbf{x}+(\mathbf{y}+\mathbf{z})=(\mathbf{x}+\mathbf{y})+\mathbf{z}",
            R"(3)\ \mathbf{x}+\mathbf{y}=\mathbf{y}+\mathbf{x}",
            R"(4)\ \mathbf{x}+\mathbf{0}=\mathbf{x}",
            R"(5)\ \mathbf{x}+(-\mathbf{x})=\mathbf{0}",
            R"(6)\ \alpha\mathbf{x}\in V",
            R"(7)\ \alpha(\mathbf{x}+\mathbf{y})=\alpha\mathbf{x}+\alpha\mathbf{y}",
            R"(8)\ (\alpha+\beta)\mathbf{x}=\alpha\mathbf{x}+\beta\mathbf{x}",
            R"(9)\ \alpha(\beta\mathbf{x})=(\alpha\beta)\mathbf{x}",
            R"(10)\ 1\mathbf{x}=\mathbf{x}",
        ]
        rows = VGroup(*[Tex(t).set_color(GREY_B) for t in items])
        rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        rows.set_height(4.9).to_edge(RIGHT, buff=0.5).shift(0.5 * DOWN)
        if rows.get_width() > 6.4:
            rows.set_width(6.4).to_edge(RIGHT, buff=0.5)
        self.play(FadeIn(rows, lag_ratio=0.05))
        note = caption("합 규칙 다섯 · 스칼라곱 규칙 다섯", 22, GREY_B).next_to(p, DOWN, buff=0.2)
        self.play(FadeIn(note, UP))
        self.wait(0.5)

        x = arrow(p, self.x, ACCENT)
        y = arrow(p, self.y, CALM)
        xl = vlabel(x, R"\mathbf{x}", ACCENT, DR)
        yl = vlabel(y, R"\mathbf{y}", CALM, UL)
        self.play(GrowArrow(x), FadeIn(xl), GrowArrow(y), FadeIn(yl))

        def show(k, text, *mobs, keep=()):
            mark = check_mark().scale(0.8).next_to(rows[k], RIGHT, buff=0.2)
            cap = caption(text, 22, DONE).move_to(note)
            anims = [rows[k].animate.set_color(DONE), FadeIn(mark)]
            for m in mobs:
                anims.append(GrowArrow(m) if isinstance(m, Arrow) else FadeIn(m))
            self.play(*anims, run_time=0.7)
            self.play(FadeIn(cap), run_time=0.3)
            self.wait(0.7)
            gone = [m for m in mobs if m not in keep]
            self.play(FadeOut(VGroup(*gone)), FadeOut(cap), run_time=0.35)

        sx, sy = self.x, self.y
        s_ = (sx[0] + sy[0], sx[1] + sy[1])
        self.remove(note)
        # (1) 합에 닫힘
        show(0, "더한 것도 평면 안", DashedLine(p.c2p(*sx), p.c2p(*s_)).set_stroke(CALM, 2),
             arrow(p, s_, DONE))
        # (3) 교환 — 두 길이 같은 머리에 닿음
        show(2, "어느 순서로 가도 같은 머리",
             DashedLine(p.c2p(*sx), p.c2p(*s_)).set_stroke(CALM, 2),
             DashedLine(p.c2p(*sy), p.c2p(*s_)).set_stroke(ACCENT, 2),
             arrow(p, s_, DONE))
        # (2) 결합 — 셋을 어떻게 묶어도 같은 머리
        z = arrow(p, self.z, PURPLE_B, start=s_)
        end = (s_[0] + self.z[0], s_[1] + self.z[1])
        show(1, "셋을 어떻게 묶어도 같은 머리",
             DashedLine(p.c2p(*sx), p.c2p(*s_)).set_stroke(CALM, 2), z, arrow(p, end, DONE))
        # (4) 영벡터
        show(3, "영벡터를 더하면 그대로", Dot(p.c2p(0, 0), color=DONE))
        # (5) 역원
        nx = (-sx[0], -sx[1])
        show(4, "반대 벡터를 더하면 원점", arrow(p, nx, WARN), Dot(p.c2p(0, 0), color=DONE))
        # (6) 스칼라곱에 닫힘
        show(5, "늘려도 같은 직선 위", arrow(p, (1.5 * sx[0], 1.5 * sx[1]), DONE))
        # (7) 분배 — 평행사변형이 통째로 줄어듦
        hx, hy, hs = (sx[0] / 2, sx[1] / 2), (sy[0] / 2, sy[1] / 2), (s_[0] / 2, s_[1] / 2)
        show(6, "평행사변형이 통째로 줄어듦",
             DashedLine(p.c2p(*hx), p.c2p(*hs)).set_stroke(CALM, 2),
             DashedLine(p.c2p(*hy), p.c2p(*hs)).set_stroke(ACCENT, 2), arrow(p, hs, DONE))
        # (8) 분배 — 같은 직선 위에서 이어 붙임
        show(7, "같은 직선 위에서 이어 붙임", arrow(p, hx, DONE),
             arrow(p, (1.5 * sx[0], 1.5 * sx[1]), PURPLE_B, start=hx))
        # (9) 결합 — 두 번 늘린 것과 한 번에 늘린 것
        show(8, "두 번 늘려도 한 번에 늘려도", arrow(p, (1.5 * sx[0], 1.5 * sx[1]), DONE))
        # (10) 1 배
        show(9, "1 배는 그대로", Dot(p.c2p(*sx), color=DONE))

        done = caption("열 조건 모두 통과 · 벡터공간", 24, DONE).move_to(note)
        self.play(FadeIn(done, UP))
        self.wait(1.0)

        # 반례 — 1사분면, 단위원
        self.play(FadeOut(VGroup(x, xl, y, yl, done)), rows.animate.set_color(GREY_B))
        quad = Polygon(p.c2p(0, 0), p.c2p(4, 0), p.c2p(4, 3), p.c2p(0, 3))
        quad.set_fill(CALM, 0.18).set_stroke(width=0)
        self.play(FadeIn(quad))
        v = arrow(p, (2, 1), ACCENT)
        w = arrow(p, (-2, -1), WARN)
        wl = vlabel(w, R"(-1)\mathbf{x}", WARN, DOWN)
        self.play(GrowArrow(v))
        self.play(GrowArrow(w), FadeIn(wl))
        bad6 = cross_mark().scale(0.8).next_to(rows[5], RIGHT, buff=0.2)
        self.play(rows[5].animate.set_color(WARN), FadeIn(bad6))
        c1 = caption("1사분면은 (6) 에서 탈락", 24, WARN).move_to(note)
        self.play(FadeIn(c1, UP))
        self.wait(1.0)

        self.play(FadeOut(VGroup(quad, v, w, wl, c1, bad6)), rows[5].animate.set_color(GREY_B))
        unit = np.linalg.norm(p.c2p(1, 0) - p.c2p(0, 0))
        circle = Circle(radius=unit).move_to(p.c2p(0, 0)).set_stroke(CALM, 3)
        self.play(ShowCreation(circle))
        e1 = arrow(p, (1, 0), ACCENT)
        e2 = arrow(p, (0, 1), ACCENT)
        e12 = arrow(p, (1, 1), WARN)
        self.play(GrowArrow(e1), GrowArrow(e2))
        self.play(GrowArrow(e2.copy().shift(p.c2p(1, 0) - p.c2p(0, 0))), GrowArrow(e12))
        bad1 = cross_mark().scale(0.8).next_to(rows[0], RIGHT, buff=0.2)
        self.play(rows[0].animate.set_color(WARN), FadeIn(bad1))
        c2 = caption("단위원은 (1) 에서 탈락", 24, WARN).move_to(note)
        self.play(FadeIn(c2, UP))
        self.wait(1.0)

        last = caption("하나라도 깨지면 벡터공간 아님", 24, WARN).move_to(note)
        self.play(FadeTransform(c2, last))
        self.wait(2)


class SubspaceLine(InteractiveScene):
    """정리 3-1 세 조건으로 후보 집합 넷을 판정하고, 예제 3-3 의 초평면까지 간다.

    후보마다 어느 조건에서 걸리는지가 다르다. 원점 안 지나는 직선은 (1), 1사분면은 (3),
    두 축의 합집합은 (2) 에서 탈락한다. 세 조건이 서로 다른 것을 보는 것이 요점이다.
    """
    cands = ["y = x", "y = x + 1.5", "1사분면", "x축 ∪ y축"]

    def construct(self):
        head = slide_title("부분공간 판정법")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정리 3-1 · 예제 3-3")))

        p = plane((-3, 4, 1), (-3, 4, 1), 4.7)
        p.to_edge(LEFT, buff=0.4).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        # 점검표 — 행은 후보, 열은 세 조건과 판정
        heads = VGroup(
            Tex(R"S").set_color(GREY_B),
            Tex(R"(1)\ \mathbf{0}\in S").set_color(GREY_B),
            Tex(R"(2)\ \mathbf{x}+\mathbf{y}").set_color(GREY_B),
            Tex(R"(3)\ \alpha\mathbf{x}").set_color(GREY_B),
            caption("판정", 22, GREY_B),
        )
        for h in heads:
            h.set_height(min(h.get_height(), 0.34))
        table = VGroup(heads)
        for name in self.cands:
            row = VGroup(caption(name, 22, INK), *[VGroup() for _ in range(4)])
            table.add(row)
        # 칸 배치
        col_w = [1.9, 1.5, 1.5, 1.3, 1.3]
        right = FRAME_WIDTH / 2 - 0.4
        left = right - sum(col_w)
        top = p.get_top()[1] - 0.05
        row_h = 0.62
        cells = {}
        for r, row in enumerate(table):
            for c in range(5):
                x0 = left + sum(col_w[:c]) + col_w[c] / 2
                cells[(r, c)] = np.array([x0, top - r * row_h, 0])
            for c, m in enumerate(row):
                if len(m) or isinstance(m, (Tex, Text)):
                    m.move_to(cells[(r, c)])
        rule = Line([left, top - row_h / 2, 0], [right, top - row_h / 2, 0]).set_stroke(GREY_C, 2)
        self.play(FadeIn(heads), ShowCreation(rule))
        self.wait(0.3)

        def mark(r, c, ok):
            m = (check_mark() if ok else cross_mark()).scale(0.8).move_to(cells[(r, c)])
            self.play(FadeIn(m, scale=1.5), run_time=0.35)
            return m

        def verdict(r, ok):
            t = caption("부분공간" if ok else "아님", 22, DONE if ok else WARN).move_to(cells[(r, 4)])
            self.play(FadeIn(t, UP), run_time=0.4)
            return t

        note = caption("", 22).next_to(p, DOWN, buff=0.2)

        def say(text, color=DONE):
            nonlocal note
            new = caption(text, 22, color).next_to(p, DOWN, buff=0.2)
            self.play(FadeTransform(note, new), run_time=0.35)
            note = new

        # 1. y = x
        line = Line(p.c2p(-3, -3), p.c2p(4, 4)).set_stroke(DONE, 3)
        self.play(FadeIn(table[1][0]), ShowCreation(line))
        o = Dot(p.c2p(0, 0), color=DONE)
        self.play(FadeIn(o, scale=2)); mark(1, 1, True)
        a = arrow(p, (1, 1), ACCENT); b = arrow(p, (3, 3), CALM, start=(1, 1)); s_ = arrow(p, (3, 3), DONE)
        self.play(GrowArrow(a), GrowArrow(b)); self.play(GrowArrow(s_)); mark(1, 2, True)
        self.play(FadeOut(VGroup(b, s_)))
        t = arrow(p, (-2, -2), DONE)
        self.play(GrowArrow(t)); mark(1, 3, True); verdict(1, True)
        say("원점을 지나는 직선은 세 조건 통과")
        self.wait(0.6)
        self.play(FadeOut(VGroup(line, o, a, t)))

        # 2. y = x + 1.5
        line2 = Line(p.c2p(-3, -1.5), p.c2p(2.5, 4)).set_stroke(WARN, 3)
        self.play(FadeIn(table[2][0]), ShowCreation(line2))
        o2 = Dot(p.c2p(0, 0), color=WARN)
        self.play(Flash(o2, color=WARN)); mark(2, 1, False); verdict(2, False)
        say("영벡터가 없으면 (1) 에서 끝", WARN)
        self.wait(0.6)
        self.play(FadeOut(line2))

        # 3. 1사분면
        quad = Polygon(p.c2p(0, 0), p.c2p(4, 0), p.c2p(4, 4), p.c2p(0, 4)).set_fill(CALM, 0.18).set_stroke(width=0)
        self.play(FadeIn(table[3][0]), FadeIn(quad))
        self.play(FadeIn(Dot(p.c2p(0, 0), color=DONE), scale=2)); mark(3, 1, True)
        a3 = arrow(p, (2, 1), ACCENT); b3 = arrow(p, (3, 3), CALM, start=(2, 1)); s3 = arrow(p, (3, 3), DONE)
        self.play(GrowArrow(a3), GrowArrow(b3)); self.play(GrowArrow(s3)); mark(3, 2, True)
        self.play(FadeOut(VGroup(b3, s3)))
        n3 = arrow(p, (-2, -1), WARN)
        self.play(GrowArrow(n3)); mark(3, 3, False); verdict(3, False)
        say("스칼라곱이 밖으로 나가면 (3) 탈락", WARN)
        self.wait(0.6)
        self.play(FadeOut(VGroup(quad, a3, n3)))

        # 4. x축 ∪ y축
        ax = Line(p.c2p(-3, 0), p.c2p(4, 0)).set_stroke(CALM, 5)
        ay = Line(p.c2p(0, -3), p.c2p(0, 4)).set_stroke(CALM, 5)
        self.play(FadeIn(table[4][0]), ShowCreation(ax), ShowCreation(ay))
        mark(4, 1, True)
        e1 = arrow(p, (2, 0), ACCENT)
        self.play(GrowArrow(e1))
        self.play(Transform(e1, arrow(p, (-2, 0), ACCENT))); mark(4, 3, True)
        e2 = arrow(p, (0, 2), ACCENT); e12 = arrow(p, (2, 2), WARN)
        self.play(Transform(e1, arrow(p, (2, 0), ACCENT)), GrowArrow(e2))
        self.play(GrowArrow(e12)); mark(4, 2, False); verdict(4, False)
        say("두 축의 합집합은 합에서 탈락", WARN)
        self.wait(0.8)
        self.play(FadeOut(VGroup(ax, ay, e1, e2, e12)))

        # 예제 3-3 — 초평면
        hyper = VGroup(
            Tex(R"S=\{\mathbf{x}\in\mathbb{R}^n \mid x_1+\cdots+x_n=0\}").set_color(INK),
            Tex(R"(1)\ 0+\cdots+0=0").set_color(DONE),
            Tex(R"(2)\ \textstyle\sum(x_i+y_i)=\sum x_i+\sum y_i=0").set_color(DONE),
            Tex(R"(3)\ \textstyle\sum \alpha x_i=\alpha\sum x_i=0").set_color(DONE),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        hyper.set_width(5.4).move_to(p).align_to(p, UP).shift(0.1 * DOWN)
        hyper.add_background_rectangle(opacity=0.85, buff=0.15)
        for line in hyper[1:]:
            self.play(FadeIn(line, UP), run_time=0.45)
        say("예제 3-3 도 세 조건 통과 · 부분공간")
        self.wait(0.8)
        say("(3) 에 α = -1 을 넣으면 역원", GREY_B)
        self.wait(2)


class LinearCombination(InteractiveScene):
    """정의 3-5 와 예제 3-4. 스칼라 둘을 돌리면 합의 머리가 어디까지 가는지를 먼저 본다.

    참고: legacy/_2016/eola/chapter2.py ShowVaryingLinearCombinations (3blue1brown).
    두 벡터를 각각 늘린 뒤 이어 붙인 머리가 스칼라에 따라 움직이고, 지나간 자리에 점을
    남긴다. 그다음 예제 3-4 의 값으로 성분 계산을 한 번 하고 코드 한 줄과 잇는다.
    """
    v = np.array([2.0, 1.0])
    w = np.array([-1.0, 2.0])
    pairs = [(1.5, 0.6), (0.7, 1.0), (-1.0, -0.8), (1.2, -0.5), (-0.8, 1.0), (0.5, 1.2)]

    def construct(self):
        head = slide_title("선형결합")
        head.fix_in_frame()
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "정의 3-5 · 예제 3-4")
        tag.fix_in_frame()
        self.play(FadeIn(tag))

        p = plane((-4, 4, 1), (-3, 4, 1), 5.0)
        p.to_edge(LEFT, buff=0.4).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        v0 = arrow(p, tuple(self.v), ACCENT)
        w0 = arrow(p, tuple(self.w), CALM)
        vl = vlabel(v0, R"\mathbf{v}", ACCENT, DR)
        wl = vlabel(w0, R"\mathbf{w}", CALM, UL)
        self.play(GrowArrow(v0), FadeIn(vl), GrowArrow(w0), FadeIn(wl))
        self.wait(0.4)

        ta, tb = ValueTracker(1.0), ValueTracker(1.0)

        def sv():
            return arrow(p, tuple(ta.get_value() * self.v), ACCENT)

        def sw():
            tip = ta.get_value() * self.v
            return arrow(p, tuple(tip + tb.get_value() * self.w), CALM, start=tuple(tip))

        def ssum():
            return arrow(p, tuple(ta.get_value() * self.v + tb.get_value() * self.w), DONE)

        av = always_redraw(sv)
        bw = always_redraw(sw)
        total = always_redraw(ssum)
        self.play(FadeOut(VGroup(v0, vl, w0, wl)))
        self.add(av, bw, total)

        na = DecimalNumber(1.0, num_decimal_places=1, color=ACCENT)
        nb = DecimalNumber(1.0, num_decimal_places=1, color=CALM)
        na.f_always.set_value(ta.get_value)
        nb.f_always.set_value(tb.get_value)
        formula = VGroup(na, Tex(R"\mathbf{v}").set_color(ACCENT), Tex("+").set_color(INK),
                         nb, Tex(R"\mathbf{w}").set_color(CALM)).arrange(RIGHT, buff=0.18)
        formula.scale(1.2).next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        anchor = formula.get_left().copy()
        formula.add_updater(lambda m: m.arrange(RIGHT, buff=0.18).next_to(anchor, RIGHT, buff=0))
        self.play(FadeIn(formula))
        note = caption("스칼라 둘을 돌리면 머리가 움직임", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))

        trail = VGroup()
        self.add(trail)
        for a_, b_ in self.pairs:
            self.play(ta.animate.set_value(a_), tb.animate.set_value(b_), run_time=1.1)
            trail.add(Dot(p.c2p(*(a_ * self.v + b_ * self.w)), radius=0.06, color=DONE))
            self.wait(0.25)
        rule = Tex(R"a\mathbf{v}+b\mathbf{w}").set_color(DONE).scale(1.1)
        rule.next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        self.play(Write(rule))
        note2 = caption("닿는 점 전부가 생성집합", 24, GREY_B).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        # 예제 3-4 — 같은 일을 3차원 공간에서. a = (1,0,3), b = (2,1,2), 2a + 3b = (8,3,12)
        formula.clear_updaters()
        self.play(FadeOut(VGroup(formula, rule, note2, trail, av, bw, total, p)))
        self.remove(av, bw, total)

        ax = ThreeDAxes(x_range=(0, 9, 1), y_range=(0, 4, 1), z_range=(0, 13, 1),
                        width=6.0, height=2.6, depth=5.4,
                        axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=True))
        ax.move_to(ORIGIN)
        labels = VGroup(Tex("x"), Tex("y"), Tex("z")).set_color(GREY_B)
        labels[0].next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        labels[1].next_to(ax.y_axis.get_end(), UP, buff=0.1)
        labels[2].next_to(ax.z_axis.get_end(), OUT, buff=0.1).rotate(PI / 2, RIGHT)
        labels[1].rotate(PI / 2, RIGHT)
        labels[0].rotate(PI / 2, RIGHT)
        # 카메라는 제 중심을 축으로 돈다. 축을 중심 가까이 두어야 회전해도 그림이 흐르지 않는다.
        self.frame.reorient(-35, 66, 0, center=(1.7, 0.3, -0.5), height=9.6)
        self.play(FadeIn(ax), FadeIn(labels))

        def arr3(start, end, color):
            m = Arrow(ax.c2p(*start), ax.c2p(*end), buff=0, thickness=5).set_color(color)
            m.set_stroke(color, 2)
            return m

        panel = VGroup(
            Tex(R"\mathbf{a}=(1,0,3)").set_color(ACCENT),
            Tex(R"\mathbf{b}=(2,1,2)").set_color(CALM),
            Tex(R"2\mathbf{a}=(2,0,6)").set_color(ACCENT),
            Tex(R"3\mathbf{b}=(6,3,6)").set_color(CALM),
            Tex(R"2\mathbf{a}+3\mathbf{b}=(8,3,12)").set_color(DONE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        panel.set_width(3.9).to_edge(RIGHT, buff=0.5).shift(0.5 * UP)
        panel.fix_in_frame()
        cap = caption("예제 3-4 · 3차원의 두 벡터", 24, GREY_B).to_edge(DOWN, buff=0.45)
        cap.fix_in_frame()
        self.play(FadeIn(cap))

        a3 = arr3((0, 0, 0), (1, 0, 3), ACCENT)
        b3 = arr3((0, 0, 0), (2, 1, 2), CALM)
        self.play(GrowArrow(a3), FadeIn(panel[0]))
        self.play(GrowArrow(b3), FadeIn(panel[1]))
        self.frame.add_updater(lambda f, dt: f.increment_theta(0.04 * dt))
        self.wait(0.8)

        # 늘리고 이어 붙인다
        a2 = arr3((0, 0, 0), (2, 0, 6), ACCENT)
        self.play(Transform(a3, a2), FadeIn(panel[2]), run_time=0.9)
        cap2 = caption("늘리기 · 같은 직선 위", 24, ACCENT).move_to(cap); cap2.fix_in_frame()
        self.play(FadeTransform(cap, cap2)); cap = cap2
        self.wait(0.5)
        b3s = arr3((2, 0, 6), (8, 3, 12), CALM)
        self.play(Transform(b3, b3s), FadeIn(panel[3]), run_time=0.9)
        cap3 = caption("3b 를 2a 의 머리에 잇기", 24, CALM).move_to(cap); cap3.fix_in_frame()
        self.play(FadeTransform(cap, cap3)); cap = cap3
        self.wait(0.5)
        total3 = arr3((0, 0, 0), (8, 3, 12), DONE)
        tip = Dot(ax.c2p(8, 3, 12), color=DONE, radius=0.07)
        drop = DashedLine(ax.c2p(8, 3, 12), ax.c2p(8, 3, 0)).set_stroke(GREY_B, 2)
        foot = DashedLine(ax.c2p(8, 3, 0), ax.c2p(8, 0, 0)).set_stroke(GREY_B, 2)
        self.play(GrowArrow(total3), FadeIn(tip), FadeIn(panel[4]))
        self.play(ShowCreation(drop), ShowCreation(foot))
        cap4 = caption("머리가 닿는 점이 선형결합", 24, DONE).move_to(cap); cap4.fix_in_frame()
        self.play(FadeTransform(cap, cap4)); cap = cap4
        self.wait(1.2)

        line = code("print(\"2*a + 3*b = \", 2*a + 3*b)", 19)
        shown = code("2*a + 3*b =  [ 8  3 12]", 18, GREY_B)
        codes = VGroup(line, shown).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        codes.next_to(panel, DOWN, buff=0.5).align_to(panel, LEFT)
        codes.fix_in_frame()
        self.play(FadeIn(codes, UP))
        self.wait(2)
        self.frame.clear_updaters()


class IndependenceCollinear(InteractiveScene):
    """정의 3-6 과 예제 3-5 · 3-6.

    같은 직선 위의 두 벡터는 종속이고, 한쪽이 다른 쪽의 배수다. 예제 3-6 은
    세 벡터의 선형결합을 0 으로 놓은 연립방정식이 자명한 해뿐임을 본다.
    """

    def construct(self):
        head = slide_title("선형독립과 선형종속")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-6 · 예제 3-5 · 3-6")))

        p = plane((-1, 4, 1), (-1, 5, 1), 4.8)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        v2 = arrow(p, (2, 4), WARN)
        v1 = arrow(p, (1, 2), ACCENT)
        l1 = vlabel(v1, R"\mathbf{v}_1", ACCENT, RIGHT)
        l2 = vlabel(v2, R"\mathbf{v}_2", WARN, RIGHT)
        self.play(GrowArrow(v2), FadeIn(l2), GrowArrow(v1), FadeIn(l1))
        dep = Tex(R"2\mathbf{v}_1 - \mathbf{v}_2 = \mathbf{0}").set_color(WARN)
        dep.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(dep))
        note = caption("같은 직선 위 · 선형종속", 24, WARN).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        self.play(FadeOut(VGroup(v2, l2)))
        w = arrow(p, (3, 1), CALM)
        wl = vlabel(w, R"\mathbf{v}_2", CALM, RIGHT)
        self.play(GrowArrow(w), FadeIn(wl))
        ind = Tex(R"a\mathbf{v}_1 + b\mathbf{v}_2 = \mathbf{0}\ \Rightarrow\ a=b=0").set_color(DONE)
        ind.set_width(5.4).move_to(dep).align_to(dep, LEFT)
        self.play(FadeTransform(dep, ind))
        note2 = caption("다른 직선 · 선형독립", 24, DONE).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        # 예제 3-6
        sys_ = VGroup(
            Tex(R"a(1,1,0)+b(0,-1,1)+c(1,0,1)=\mathbf{0}").set_color(INK),
            Tex(R"a+c=0,\quad a-b=0,\quad b+c=0").set_color(INK),
            Tex(R"a=b=c=0").set_color(DONE),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        sys_.set_width(5.6).next_to(ind, DOWN, buff=0.7).align_to(ind, LEFT)
        for line in sys_:
            self.play(FadeIn(line, UP), run_time=0.6)
            self.wait(0.3)
        last = caption("자명한 해뿐 · 선형독립", 24, DONE).next_to(sys_, DOWN, buff=0.4).align_to(sys_, LEFT)
        self.play(FadeIn(last, UP))
        self.wait(2)


class SpanLineToPlane(InteractiveScene):
    """정의 3-7 과 예제 3-7. 한 벡터의 생성은 직선, 독립인 두 벡터의 생성은 평면."""

    def construct(self):
        head = slide_title("생성집합")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-7 · 예제 3-7")))

        p = plane((-4, 4, 1), (-3, 3, 1), 4.9)
        p.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        v = arrow(p, (2, 1), ACCENT)
        vl = vlabel(v, R"\mathbf{v}", ACCENT, DR)
        self.play(GrowArrow(v), FadeIn(vl))
        line = DashedLine(p.c2p(-4, -2), p.c2p(4, 2)).set_stroke(ACCENT, 2)
        multiples = VGroup(*[arrow(p, (2 * a, a), ACCENT) for a in (-1.5, -0.5, 0.5, 1.5)])
        multiples.set_opacity(0.45)
        self.play(ShowCreation(line), FadeIn(multiples))
        span1 = Tex(R"\mathrm{span}\{\mathbf{v}\} = \{a\mathbf{v}\}").set_color(ACCENT)
        span1.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(span1))
        note = caption("한 벡터의 생성은 직선", 24, ACCENT).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        w = arrow(p, (-1, 2), CALM)
        wl = vlabel(w, R"\mathbf{w}", CALM, UL)
        self.play(GrowArrow(w), FadeIn(wl))
        dots = VGroup(*[Dot(p.c2p(2 * a - b, a + 2 * b), radius=0.04, color=DONE)
                        for a in np.arange(-3, 3.1, 0.5) for b in np.arange(-3, 3.1, 0.5)
                        if -4 <= 2 * a - b <= 4 and -3 <= a + 2 * b <= 3])
        self.play(FadeOut(multiples), FadeOut(line), FadeIn(dots, lag_ratio=0.02), run_time=1.6)
        span2 = Tex(R"\mathrm{span}\{\mathbf{v},\mathbf{w}\} = \{a\mathbf{v}+b\mathbf{w}\}").set_color(DONE)
        span2.set_width(5.4).next_to(span1, DOWN, buff=0.5).align_to(span1, LEFT)
        self.play(Write(span2))
        note2 = caption("독립인 두 벡터의 생성은 평면", 24, DONE).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        ex = Tex(R"S=\{(2,3,4),\,(-1,2,1)\}").set_color(INK)
        ex2 = Tex(R"\mathrm{span}(S)=\{a(2,3,4)+b(-1,2,1)\}").set_color(DONE)
        exg = VGroup(ex, ex2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        exg.set_width(5.4).next_to(span2, DOWN, buff=0.7).align_to(span2, LEFT)
        self.play(FadeIn(exg, UP))
        last = caption("R³ 안의 원점을 지나는 평면", 24, GREY_B).next_to(exg, DOWN, buff=0.35).align_to(exg, LEFT)
        self.play(FadeIn(last, UP))
        self.wait(2)


class BasisDimension(InteractiveScene):
    """정의 3-8 · 3-9 와 예제 3-8 · 3-9 를 3차원 공간에서.

    앞 두 벡터가 만드는 평면을 깔아 두고 셋째 벡터가 그 평면 밖으로 나가는지(3-8, 기저)
    평면 안에 눕는지(3-9, 셋째 = 앞 둘의 합, 차원 2)를 본다. 카메라는 축 중심으로 천천히 돈다.
    """
    v1 = (1, 1, 0)
    v2 = (0, 1, 1)
    v3 = (1, 0, 1)
    v3_dep = (1, 2, 1)

    def construct(self):
        head = slide_title("기저와 차원")
        head.fix_in_frame()
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "정의 3-8 · 3-9 · 예제 3-8 · 3-9")
        tag.fix_in_frame()
        self.play(FadeIn(tag))

        rule = VGroup(caption("생성", 24, ACCENT), Tex("+").set_color(INK),
                      caption("선형독립", 24, CALM), Tex(R"\Rightarrow").set_color(INK),
                      caption("기저", 24, DONE)).arrange(RIGHT, buff=0.3)
        rule.to_edge(RIGHT, buff=0.6).shift(2.3 * UP)
        rule.fix_in_frame()
        self.play(FadeIn(rule, UP))

        ax = ThreeDAxes(x_range=(-1, 3, 1), y_range=(-1, 4, 1), z_range=(-1, 3, 1),
                        width=4.6, height=4.6, depth=4.4,
                        axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=True))
        ax.move_to(ORIGIN)
        labels = VGroup(Tex("x"), Tex("y"), Tex("z")).set_color(GREY_B)
        labels[0].next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        labels[1].next_to(ax.y_axis.get_end(), UP, buff=0.1)
        labels[2].next_to(ax.z_axis.get_end(), OUT, buff=0.1)
        for lab in labels:
            lab.rotate(PI / 2, RIGHT)
        self.frame.reorient(-40, 64, 0, center=(1.9, 0.4, -0.3), height=9.8)
        self.play(FadeIn(ax), FadeIn(labels))
        self.frame.add_updater(lambda f, dt: f.increment_theta(0.04 * dt))

        def arr3(end, color, start=(0, 0, 0)):
            m = Arrow(ax.c2p(*start), ax.c2p(*end), buff=0, thickness=5).set_color(color)
            m.set_stroke(color, 2)
            return m

        def span_plane(u, w, color):
            pts = []
            for a_, b_ in ((-0.5, -0.5), (1.8, -0.5), (1.8, 1.8), (-0.5, 1.8)):
                pts.append(ax.c2p(*[a_ * u[k] + b_ * w[k] for k in range(3)]))
            poly = Polygon(*pts).set_fill(color, 0.22).set_stroke(color, 1, opacity=0.5)
            return poly

        panel = VGroup(
            Tex(R"\mathbf{v}_1=(1,1,0)").set_color(ACCENT),
            Tex(R"\mathbf{v}_2=(0,1,1)").set_color(CALM),
            Tex(R"\mathbf{v}_3=(1,0,1)").set_color(PURPLE_B),
            Tex(R"a\mathbf{v}_1+b\mathbf{v}_2+c\mathbf{v}_3=\mathbf{0}\ \Rightarrow\ a=b=c=0").set_color(INK),
            Tex(R"\dim(\mathbb{R}^3)=3").set_color(DONE),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        panel.set_width(4.6).to_edge(RIGHT, buff=0.5).shift(0.2 * UP)
        panel.fix_in_frame()

        cap = caption("예제 3-8 · 세 벡터", 24, GREY_B).to_edge(DOWN, buff=0.45)
        cap.fix_in_frame()
        self.play(FadeIn(cap))

        def say(text, color=DONE):
            nonlocal cap
            new = caption(text, 24, color).to_edge(DOWN, buff=0.45)
            new.fix_in_frame()
            self.play(FadeTransform(cap, new), run_time=0.4)
            cap = new

        a1 = arr3(self.v1, ACCENT); a2 = arr3(self.v2, CALM); a3 = arr3(self.v3, PURPLE_B)
        self.play(GrowArrow(a1), FadeIn(panel[0]))
        self.play(GrowArrow(a2), FadeIn(panel[1]))
        plane = span_plane(self.v1, self.v2, CALM)
        self.play(FadeIn(plane))
        say("앞의 둘이 만드는 평면", CALM)
        self.wait(0.6)
        self.play(GrowArrow(a3), FadeIn(panel[2]))
        say("셋째는 평면 밖 · 선형독립", PURPLE_B)
        self.wait(0.6)
        self.play(FadeIn(panel[3], UP))
        self.wait(0.5)
        self.play(FadeIn(panel[4], UP))
        say("독립인 셋이 공간을 채움 · 기저", DONE)
        self.wait(1.2)

        # 예제 3-9 — 셋째가 앞 둘의 합
        self.play(FadeOut(VGroup(panel[3], panel[4])))
        p3 = Tex(R"\mathbf{v}_3=(1,2,1)").set_color(WARN)
        p3.set_height(panel[2].get_height()).move_to(panel[2]).align_to(panel, LEFT)
        p3.fix_in_frame()
        dep = arr3(self.v3_dep, WARN)
        self.play(FadeTransform(a3, dep), FadeTransform(panel[2], p3))
        say("예제 3-9 · 셋째를 (1, 2, 1) 로", WARN)
        self.wait(0.5)
        ghost = arr3(self.v3_dep, CALM, start=self.v1)
        ghost.set_opacity(0.6)
        self.play(GrowArrow(ghost))
        eq = Tex(R"(1,2,1)=(1,1,0)+(0,1,1)").set_color(WARN)
        eq.set_width(4.2).next_to(p3, DOWN, buff=0.4).align_to(panel, LEFT)
        eq.fix_in_frame()
        self.play(Write(eq))
        say("셋째가 평면 안 · 선형종속", WARN)
        self.wait(0.8)
        dim2 = Tex(R"\dim(\mathrm{span}(S))=2").set_color(DONE)
        dim2.set_width(3.2).next_to(eq, DOWN, buff=0.4).align_to(panel, LEFT)
        dim2.fix_in_frame()
        self.play(FadeIn(dim2, UP))
        say("셋이 평면 하나만 채움 · 차원 2", DONE)
        self.wait(2)
        self.frame.clear_updaters()


class VectorNorm(InteractiveScene):
    """정의 3-10 과 예제 3-10. 노름은 원점에서 그 점까지의 거리다."""

    def construct(self):
        head = slide_title("노름")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-10 · 예제 3-10")))

        p = plane((-1, 5, 1), (-1, 5, 1), 4.9)
        p.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        x = arrow(p, (3, 4), ACCENT)
        xl = vlabel(x, R"\mathbf{x}=(3,4)", ACCENT, UR)
        self.play(GrowArrow(x), FadeIn(xl))
        drop = DashedLine(p.c2p(3, 4), p.c2p(3, 0)).set_stroke(GREY_B, 2)
        base = Line(p.c2p(0, 0), p.c2p(3, 0)).set_stroke(DONE, 3)
        b3 = Tex("3").set_color(DONE).scale(0.8).next_to(base, DOWN, buff=0.12)
        b4 = Tex("4").set_color(DONE).scale(0.8).next_to(drop, RIGHT, buff=0.12)
        self.play(ShowCreation(drop), ShowCreation(base), FadeIn(b3), FadeIn(b4))
        formula = Tex(R"\Vert \mathbf{x}\Vert  = \sqrt{3^2+4^2} = 5").set_color(DONE)
        formula.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(formula))
        note = caption("원점에서 점까지의 거리", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        general = Tex(R"\Vert \mathbf{x}\Vert  = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}").set_color(INK)
        general.set_width(5.4).next_to(formula, DOWN, buff=0.6).align_to(formula, LEFT)
        self.play(Write(general))
        ex = Tex(R"\Vert (1,2,0,2)\Vert  = \sqrt{1+4+0+4} = 3").set_color(DONE)
        ex.set_width(5.4).next_to(general, DOWN, buff=0.5).align_to(general, LEFT)
        self.play(FadeIn(ex, UP))
        self.wait(0.6)
        line = code("norm_vec = np.sqrt(np.sum(vec1*vec1))", 21)
        line.next_to(ex, DOWN, buff=0.6).align_to(ex, LEFT)
        self.play(FadeIn(line, UP))
        self.wait(2)


class TriangleInequality(InteractiveScene):
    """예제 3-11 을 3차원 공간에서. x, 머리에 이은 y, 원점에서 x+y 가 삼각형을 이룬다.

    두 변을 돌아가는 길(√6 + √2)이 지름길(√10)보다 길다. 카메라는 축 중심으로 천천히 돈다.
    """
    x = (1, -1, 2)
    y = (0, 1, 1)
    s = (1, 0, 3)

    def construct(self):
        head = slide_title("삼각부등식")
        head.fix_in_frame()
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "정리 3-3 (3) · 예제 3-11")
        tag.fix_in_frame()
        self.play(FadeIn(tag))

        rule = Tex(R"\Vert \mathbf{x}+\mathbf{y}\Vert \le \Vert \mathbf{x}\Vert + \Vert \mathbf{y}\Vert").set_color(DONE)
        rule.set_width(4.4).to_edge(RIGHT, buff=0.6).shift(2.2 * UP)
        rule.fix_in_frame()
        self.play(Write(rule))

        ax = ThreeDAxes(x_range=(-1, 2, 1), y_range=(-1, 2, 1), z_range=(0, 4, 1),
                        width=3.6, height=3.6, depth=4.6,
                        axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=True))
        ax.move_to(ORIGIN)
        labels = VGroup(Tex("x"), Tex("y"), Tex("z")).set_color(GREY_B)
        labels[0].next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        labels[1].next_to(ax.y_axis.get_end(), UP, buff=0.1)
        labels[2].next_to(ax.z_axis.get_end(), OUT, buff=0.1)
        for lab in labels:
            lab.rotate(PI / 2, RIGHT)
        self.frame.reorient(-40, 66, 0, center=(1.9, 0.4, -0.2), height=9.8)
        self.play(FadeIn(ax), FadeIn(labels))
        self.frame.add_updater(lambda f, dt: f.increment_theta(0.04 * dt))

        def arr3(end, color, start=(0, 0, 0)):
            m = Arrow(ax.c2p(*start), ax.c2p(*end), buff=0, thickness=5).set_color(color)
            m.set_stroke(color, 2)
            return m

        panel = VGroup(
            Tex(R"\mathbf{x}=(1,-1,2),\ \Vert\mathbf{x}\Vert=\sqrt{6}").set_color(ACCENT),
            Tex(R"\mathbf{y}=(0,1,1),\ \Vert\mathbf{y}\Vert=\sqrt{2}").set_color(CALM),
            Tex(R"\mathbf{x}+\mathbf{y}=(1,0,3),\ \Vert\mathbf{x}+\mathbf{y}\Vert=\sqrt{10}").set_color(DONE),
            Tex(R"\sqrt{10}\approx 3.16\ \le\ \sqrt{6}+\sqrt{2}\approx 3.86").set_color(DONE),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        panel.set_width(5.0).to_edge(RIGHT, buff=0.5).shift(0.2 * DOWN)
        panel.fix_in_frame()

        cap = caption("예제 3-11 · 두 벡터", 24, GREY_B).to_edge(DOWN, buff=0.45)
        cap.fix_in_frame()
        self.play(FadeIn(cap))

        def say(text, color=DONE):
            nonlocal cap
            new = caption(text, 24, color).to_edge(DOWN, buff=0.45)
            new.fix_in_frame()
            self.play(FadeTransform(cap, new), run_time=0.4)
            cap = new

        xa = arr3(self.x, ACCENT)
        ya = arr3(self.s, CALM, start=self.x)
        sa = arr3(self.s, DONE)
        self.play(GrowArrow(xa), FadeIn(panel[0]))
        self.play(GrowArrow(ya), FadeIn(panel[1]))
        say("y 를 x 의 머리에 잇기", CALM)
        self.wait(0.5)
        self.play(GrowArrow(sa), FadeIn(panel[2]))
        face = Polygon(ax.c2p(0, 0, 0), ax.c2p(*self.x), ax.c2p(*self.s))
        face.set_fill(DONE, 0.18).set_stroke(width=0)
        self.play(FadeIn(face))
        say("세 화살표가 공간의 삼각형", DONE)
        self.wait(0.8)
        self.play(FadeIn(panel[3], UP))
        mark = box(panel[3], DONE, 0.12)
        mark.fix_in_frame()
        self.play(ShowCreation(mark))
        say("지름길이 돌아가는 길보다 짧음", DONE)
        self.wait(1.0)
        say("3차원에서도 같은 부등식", GREY_B)
        self.wait(2)
        self.frame.clear_updaters()


# ─────────────────────────────────────────────────────────────
# 3.2 벡터의 내적
# ─────────────────────────────────────────────────────────────
class InnerProduct(InteractiveScene):
    """정의 3-11 과 예제 3-12. 같은 자리끼리 곱해 더한다. y·z = 0 은 직교의 예고다."""
    x = [1, 2, 3, -1]
    y = [0, 1, 2, 1]
    z = [2023, 1, -1, 1]

    def construct(self):
        head = slide_title("내적")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-11 · 예제 3-12")))

        rule = Tex(R"\mathbf{x}\cdot\mathbf{y} = x_1y_1 + x_2y_2 + \cdots + x_ny_n").set_color(INK)
        rule.set_width(6.0).move_to(2.1 * UP)
        self.play(Write(rule), run_time=1.0)

        xc = col(self.x, ACCENT, 0.45)
        yc = col(self.y, CALM, 0.45)
        pair = VGroup(xc, Tex(R"\cdot").set_color(INK), yc).arrange(RIGHT, buff=0.35)
        pair.move_to(0.6 * DOWN + 4.2 * LEFT)
        self.play(FadeIn(pair))

        terms = ["1\\cdot 0", "2\\cdot 1", "3\\cdot 2", "(-1)\\cdot 1"]
        expr = Tex(" + ".join(terms) + " = 7").set_color(INK)
        expr.set_width(6.2).next_to(pair, RIGHT, buff=0.8)
        self.play(FadeIn(expr))
        marks = VGroup()
        for k in range(4):
            m = VGroup(box(xc.get_entries()[k], DONE, 0.08), box(yc.get_entries()[k], DONE, 0.08))
            self.play(ShowCreation(m), run_time=0.35)
            self.play(FadeOut(m), run_time=0.2)
        self.play(ShowCreation(box(expr[-1:], DONE, 0.12)))
        note = caption("같은 자리끼리 곱해서 더하기", 24, DONE).next_to(expr, DOWN, buff=0.5)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        zc = col(self.z, WARN, 0.45)
        pair2 = VGroup(col(self.y, CALM, 0.45), Tex(R"\cdot").set_color(INK), zc).arrange(RIGHT, buff=0.35)
        pair2.move_to(pair)
        expr2 = Tex(R"0\cdot 2023 + 1\cdot 1 + 2\cdot(-1) + 1\cdot 1 = 0").set_color(INK)
        expr2.set_width(6.2).move_to(expr).align_to(expr, LEFT)
        self.play(FadeTransform(pair, pair2), FadeTransform(expr, expr2), FadeOut(note))
        note2 = caption("내적이 0 인 두 벡터", 24, WARN).next_to(expr2, DOWN, buff=0.5)
        self.play(FadeIn(note2, UP))
        self.wait(0.8)

        line = code("innerprod_vecs = np.sum(vec1*vec2)", 22).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(line, UP))
        self.wait(2)


class InnerProductCosine(InteractiveScene):
    """정의 3-12 와 예제 3-13. 사잇각으로 내적을 쓴다."""

    def construct(self):
        head = slide_title("사잇각을 이용한 내적")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-12 · 예제 3-13")))

        p = plane((-1, 4, 1), (-1, 3, 1), 4.6)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        th = 30 * DEGREES
        xe = (2 * np.cos(th), 2 * np.sin(th))
        x = arrow(p, xe, ACCENT)
        y = arrow(p, (3, 0), CALM)
        xl = vlabel(x, R"\mathbf{x},\ \Vert \mathbf{x}\Vert =2", ACCENT, UP)
        yl = vlabel(y, R"\mathbf{y},\ \Vert \mathbf{y}\Vert =3", CALM, DOWN)
        self.play(GrowArrow(y), FadeIn(yl), GrowArrow(x), FadeIn(xl))
        unit = np.linalg.norm(p.c2p(1, 0) - p.c2p(0, 0))
        arc = Arc(0, th, radius=0.7 * unit, arc_center=p.c2p(0, 0)).set_stroke(DONE, 3)
        tl = Tex(R"30^\circ").set_color(DONE).scale(0.8).next_to(arc, RIGHT, buff=0.08).shift(0.1 * UP)
        self.play(ShowCreation(arc), FadeIn(tl))

        rule = Tex(R"\mathbf{x}\cdot\mathbf{y} = \Vert \mathbf{x}\Vert \,\Vert \mathbf{y}\Vert \cos\theta").set_color(INK)
        rule.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(rule))
        self.wait(0.5)

        drop = DashedLine(p.c2p(*xe), p.c2p(xe[0], 0)).set_stroke(GREY_B, 2)
        shadow = Line(p.c2p(0, 0), p.c2p(xe[0], 0)).set_stroke(DONE, 5)
        sl = Tex(R"\Vert \mathbf{x}\Vert \cos\theta").set_color(DONE).scale(0.8).next_to(shadow, DOWN, buff=0.15)
        self.play(ShowCreation(drop), ShowCreation(shadow), FadeIn(sl))
        note = caption("그림자 길이 곱하기 y 의 길이", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        ex = Tex(R"\mathbf{x}\cdot\mathbf{y} = 2\cdot 3\cdot\cos 30^\circ = 3\sqrt{3}").set_color(DONE)
        ex.set_width(5.4).next_to(rule, DOWN, buff=0.7).align_to(rule, LEFT)
        self.play(Write(ex))
        self.wait(2)


class CauchySchwarz(InteractiveScene):
    """정리 3-5 와 예제 3-14. 코사인의 절댓값이 1 을 넘지 못하는 것과 같은 말이다."""

    def construct(self):
        head = slide_title("코시-슈바르츠 부등식")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정리 3-5 · 예제 3-14")))

        rule = Tex(R"|\mathbf{x}\cdot\mathbf{y}| \le \Vert \mathbf{x}\Vert \,\Vert \mathbf{y}\Vert ").set_color(DONE)
        rule.set_width(5.0).move_to(1.9 * UP)
        self.play(Write(rule), run_time=1.0)
        why = Tex(R"|\cos\theta| \le 1").set_color(GREY_B).next_to(rule, DOWN, buff=0.35)
        self.play(FadeIn(why, UP))
        self.wait(0.6)

        lines = VGroup(
            Tex(R"\mathbf{x}=(1,-1,3),\quad \mathbf{y}=(1,1,3)").set_color(INK),
            Tex(R"\mathbf{x}\cdot\mathbf{y} = 1 - 1 + 9 = 9").set_color(INK),
            Tex(R"\Vert \mathbf{x}\Vert  = \sqrt{11},\quad \Vert \mathbf{y}\Vert  = \sqrt{11}").set_color(INK),
            Tex(R"|9| \le \sqrt{11}\cdot\sqrt{11} = 11").set_color(DONE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lines.set_width(6.0).move_to(1.2 * DOWN)
        for line in lines:
            self.play(FadeIn(line, UP), run_time=0.6)
            self.wait(0.3)
        self.play(ShowCreation(box(lines[3], DONE, 0.12)))
        note = caption("등호는 두 벡터가 평행할 때", 24, GREY_B).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, UP))
        self.wait(2)


class OrthogonalPythagoras(InteractiveScene):
    """정의 3-13 · 정리 3-6 과 예제 3-15 · 3-16.

    내적이 0 이면 직교이고, 직교하면 피타고라스 정리가 벡터에서도 성립한다.
    """
    pairs = [
        (R"\mathbf{x}\cdot\mathbf{y}", "4 - 5 + 1 = 0", True),
        (R"\mathbf{x}\cdot\mathbf{z}", "8 - 5 - 3 = 0", True),
        (R"\mathbf{y}\cdot\mathbf{z}", "8 + 1 - 3 = 6", False),
    ]

    def construct(self):
        head = slide_title("직교와 피타고라스 정리")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-13 · 정리 3-6 · 예제 3-15 · 3-16")))

        given = Tex(R"\mathbf{x}=(2,-5,1),\ \mathbf{y}=(2,1,1),\ \mathbf{z}=(4,1,-3)").set_color(INK)
        given.set_width(7.0).move_to(2.1 * UP)
        self.play(FadeIn(given))

        rows = VGroup()
        for lhs, rhs, ok in self.pairs:
            row = VGroup(Tex(lhs + " = " + rhs).set_color(INK),
                         check_mark() if ok else cross_mark()).arrange(RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(0.4 * UP + 3.2 * LEFT)
        for row in rows:
            self.play(FadeIn(row[0], UP), run_time=0.5)
            self.play(FadeIn(row[1]), run_time=0.3)
        note = caption("내적이 0 이면 직교", 24, DONE).next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 예제 3-16 — 직교하는 두 벡터의 합의 길이
        p = plane((-1, 5, 1), (-1, 5, 1), 3.9)
        p.to_edge(RIGHT, buff=0.6).shift(0.9 * DOWN)
        self.play(FadeIn(p))
        x = arrow(p, (3, 0), ACCENT)
        y = arrow(p, (3, 4), CALM, start=(3, 0))
        s = arrow(p, (3, 4), DONE)
        self.play(GrowArrow(x), GrowArrow(y))
        self.play(GrowArrow(s))
        elbow = Elbow(width=0.22, angle=PI / 2).shift(p.c2p(3, 0)).set_stroke(GREY_B, 2)
        elbow.rotate(PI / 2, about_point=p.c2p(3, 0))
        self.play(ShowCreation(elbow))
        rule = Tex(R"\Vert \mathbf{x}+\mathbf{y}\Vert ^2 = \Vert \mathbf{x}\Vert ^2 + \Vert \mathbf{y}\Vert ^2").set_color(INK)
        ex = Tex(R"\Vert \mathbf{x}+\mathbf{y}\Vert  = \sqrt{3^2+4^2} = 5").set_color(DONE)
        eg = VGroup(rule, ex).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        eg.set_width(5.6).next_to(note, DOWN, buff=0.6).align_to(rows, LEFT)
        self.play(Write(rule))
        self.play(FadeIn(ex, UP))
        last = caption("직교하면 피타고라스 정리", 24, DONE).next_to(p, DOWN, buff=0.2)
        self.play(FadeIn(last, UP))
        self.wait(2)


class ProjectionOntoVector(InteractiveScene):
    """정의 3-14 · 정리 3-7 과 예제 3-17 · 3-18. y 위로 내린 그림자가 정사영이다."""

    def construct(self):
        head = slide_title("정사영")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-14 · 정리 3-7 · 예제 3-17 · 3-18")))

        p = plane((-1, 4, 1), (-1, 3, 1), 4.6)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        x = arrow(p, (1, 1), ACCENT)
        y = arrow(p, (2, 0), CALM)
        xl = vlabel(x, R"\mathbf{x}=(1,1)", ACCENT, UP)
        yl = vlabel(y, R"\mathbf{y}=(2,0)", CALM, DOWN)
        self.play(GrowArrow(y), FadeIn(yl), GrowArrow(x), FadeIn(xl))
        drop = DashedLine(p.c2p(1, 1), p.c2p(1, 0)).set_stroke(GREY_B, 2)
        elbow = Elbow(width=0.2).shift(p.c2p(1, 0)).set_stroke(GREY_B, 2)
        elbow.rotate(PI / 2, about_point=p.c2p(1, 0))
        pr = arrow(p, (1, 0), DONE)
        prl = Tex(R"\mathrm{proj}_{\mathbf{y}}\mathbf{x}").set_color(DONE).scale(0.8).next_to(pr, DOWN, buff=0.35)
        self.play(ShowCreation(drop), ShowCreation(elbow))
        self.play(GrowArrow(pr), FadeIn(prl))
        note = caption("y 방향으로 내린 그림자", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        rule = Tex(R"\mathrm{proj}_{\mathbf{y}}\mathbf{x} = \frac{\mathbf{x}\cdot\mathbf{y}}{\mathbf{y}\cdot\mathbf{y}}\,\mathbf{y}").set_color(INK)
        ex1 = Tex(R"\frac{2}{4}(2,0) = (1,0)").set_color(DONE)
        ex2 = VGroup(
            Tex(R"\mathbf{x}=(4,5),\ \mathbf{y}=(6,1)").set_color(INK),
            Tex(R"\frac{\mathbf{x}\cdot\mathbf{y}}{\mathbf{y}\cdot\mathbf{y}} = \frac{29}{37}").set_color(INK),
            Tex(R"\mathrm{proj}_{\mathbf{y}}\mathbf{x} = \frac{29}{37}(6,1)").set_color(DONE),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        column = VGroup(rule, ex1, ex2).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        column.set_width(4.4)
        if column.get_height() > 5.4:
            column.set_height(5.4)
        column.to_edge(RIGHT, buff=0.8).shift(0.45 * DOWN)
        self.play(Write(rule))
        self.play(FadeIn(ex1, UP))
        self.wait(0.8)
        for line in ex2:
            self.play(FadeIn(line, UP), run_time=0.5)
            self.wait(0.25)
        self.wait(2)


class InnerProductFamily(InteractiveScene):
    """정의 3-15 와 예제 3-19 · 3-20.

    네 규칙을 지키는 함수는 무엇이든 내적이다. 수 벡터, 행렬, 함수에서 하나씩 본다.
    행렬의 내적은 CH01 보충의 `FrobeniusInner` 와 같은 것이다.
    """

    def construct(self):
        head = slide_title("내적공간")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-15 · 예제 3-19 · 3-20")))

        rules = VGroup(
            Tex(R"(1)\ \langle\mathbf{x},\mathbf{x}\rangle \ge 0"),
            Tex(R"(2)\ \langle\mathbf{x},\mathbf{x}\rangle = 0 \Leftrightarrow \mathbf{x}=\mathbf{0}"),
            Tex(R"(3)\ \langle\mathbf{x},\mathbf{y}\rangle = \langle\mathbf{y},\mathbf{x}\rangle"),
            Tex(R"(4)\ \langle\alpha\mathbf{x}+\beta\mathbf{y},\mathbf{z}\rangle = \alpha\langle\mathbf{x},\mathbf{z}\rangle+\beta\langle\mathbf{y},\mathbf{z}\rangle"),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).set_color(INK)
        rules.set_width(6.4).to_edge(LEFT, buff=0.7).shift(0.9 * UP)
        frame = box(rules, GREY_B, 0.25)
        self.play(FadeIn(rules), ShowCreation(frame))
        note = caption("네 규칙을 지키면 내적", 24, DONE).next_to(frame, DOWN, buff=0.3)
        self.play(FadeIn(note, UP))
        self.wait(0.6)

        items = [
            (R"\mathbb{R}^n", R"\mathbf{x}\cdot\mathbf{y} = \sum_i x_i y_i", ACCENT),
            (R"M_{m\times n}(\mathbb{R})", R"\langle A,B\rangle = \sum_i\sum_j a_{ij}b_{ij}", CALM),
            (R"C[c,d]", R"\langle f,g\rangle = \int_c^d f(x)g(x)\,dx", DONE),
        ]
        blocks = VGroup()
        for space, form, color in items:
            b = VGroup(Tex(space).set_color(color).scale(0.9), Tex(form).set_color(color))
            b.arrange(DOWN, buff=0.22)
            blocks.add(b)
        blocks.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        blocks.set_width(4.6)
        if blocks.get_height() > 5.0:
            blocks.set_height(5.0)
        blocks.to_edge(RIGHT, buff=0.7).shift(0.45 * DOWN)
        for b in blocks:
            self.play(FadeIn(b, UP), run_time=0.6)
            self.wait(0.3)

        ex = Tex(R"\left\langle \begin{bmatrix}1&2\\3&4\end{bmatrix}, \begin{bmatrix}0&1\\1&0\end{bmatrix}\right\rangle = 0+2+3+0 = 5").set_color(CALM)
        ex.set_width(6.4).to_edge(DOWN, buff=1.0).to_edge(LEFT, buff=0.7)
        self.play(Write(ex))
        last = caption("같은 규칙, 다른 벡터", 24, GREY_B).next_to(ex, DOWN, buff=0.25).align_to(ex, LEFT)
        self.play(FadeIn(last, UP))
        self.wait(2)


class HammingManhattan(InteractiveScene):
    """정의 3-17 · 3-18 과 예제 3-22 · 3-23. 유클리드 거리 말고 다른 두 거리."""
    v = [0, 1, 1, 0, 1]
    w = [1, 1, 0, 1, 0]

    def construct(self):
        head = slide_title("해밍 거리와 맨하튼 거리")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-17 · 3-18 · 예제 3-22 · 3-23")))

        # 해밍 거리
        vr = VGroup(*[Tex(str(d)).set_color(ACCENT) for d in self.v]).arrange(RIGHT, buff=0.45)
        wr = VGroup(*[Tex(str(d)).set_color(CALM) for d in self.w]).arrange(RIGHT, buff=0.45)
        vl = Tex(R"\mathbf{v}").set_color(ACCENT)
        wl = Tex(R"\mathbf{w}").set_color(CALM)
        rows = VGroup(VGroup(vl, vr).arrange(RIGHT, buff=0.5),
                      VGroup(wl, wr).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows.scale(1.2).to_edge(LEFT, buff=1.0).shift(1.2 * UP)
        self.play(FadeIn(rows))
        diff = [k for k in range(5) if self.v[k] != self.w[k]]
        marks = VGroup(*[box(VGroup(vr[k], wr[k]), WARN, 0.1) for k in diff])
        self.play(LaggedStart(*[ShowCreation(m) for m in marks], lag_ratio=0.3))
        dh = Tex(R"d_H(\mathbf{v},\mathbf{w}) = 4").set_color(WARN).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        self.play(Write(dh))
        note = caption("서로 다른 자리의 개수", 24, WARN).next_to(dh, DOWN, buff=0.3).align_to(dh, LEFT)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        # 맨하튼 거리
        p = plane((0, 4, 1), (0, 3, 1), 3.0)
        p.to_edge(RIGHT, buff=0.9).shift(0.6 * UP)
        self.play(FadeIn(p))
        A = Dot(p.c2p(0, 0), color=WHITE)
        B = Dot(p.c2p(3, 2), color=WHITE)
        al = Tex("A").scale(0.8).next_to(A, DL, buff=0.1)
        bl = Tex("B").scale(0.8).next_to(B, UR, buff=0.1)
        self.play(FadeIn(VGroup(A, B, al, bl)))
        straight = Line(p.c2p(0, 0), p.c2p(3, 2)).set_stroke(ACCENT, 4)
        self.play(ShowCreation(straight))
        eu = Tex(R"\sqrt{3^2+2^2} = \sqrt{13}").set_color(ACCENT).scale(0.85)
        eu.next_to(p, DOWN, buff=0.3).align_to(p, LEFT)
        self.play(Write(eu))
        stairs = VMobject().set_stroke(DONE, 4)
        stairs.set_points_as_corners([p.c2p(0, 0), p.c2p(3, 0), p.c2p(3, 2)])
        self.play(ShowCreation(stairs))
        mh = Tex(R"|3| + |2| = 5").set_color(DONE).scale(0.85).next_to(eu, DOWN, buff=0.25).align_to(eu, LEFT)
        self.play(Write(mh))
        last = caption("도로를 따라 재는 거리", 24, DONE).next_to(mh, DOWN, buff=0.3).align_to(mh, LEFT)
        self.play(FadeIn(last, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3.3 벡터의 미분
# ─────────────────────────────────────────────────────────────
class Gradient(InteractiveScene):
    """정의 3-19 와 예제 3-24. 변수 하나만 보고 나머지는 상수로 두는 편미분을 세로로 쌓는다."""

    def construct(self):
        head = slide_title("그래디언트")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-19 · 예제 3-24")))

        rule = Tex(R"\nabla f = \begin{bmatrix} \partial f/\partial x \\ \partial f/\partial y \\ \partial f/\partial z \end{bmatrix}").set_color(INK)
        rule.set_height(2.0).to_edge(LEFT, buff=1.0).shift(0.7 * UP)
        self.play(Write(rule), run_time=1.0)
        note = caption("변수 하나씩 · 나머지는 상수", 24, GREY_B).next_to(rule, DOWN, buff=0.4)
        self.play(FadeIn(note, UP))

        f = Tex(R"f(x,y,z) = xyz").set_color(ACCENT)
        f.next_to(rule, RIGHT, buff=1.4).align_to(rule, UP)
        self.play(FadeIn(f))
        parts = VGroup(
            Tex(R"\partial f/\partial x = yz").set_color(INK),
            Tex(R"\partial f/\partial y = xz").set_color(INK),
            Tex(R"\partial f/\partial z = xy").set_color(INK),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        parts.next_to(f, DOWN, buff=0.4).align_to(f, LEFT)
        for line in parts:
            self.play(FadeIn(line, UP), run_time=0.5)
            self.wait(0.2)
        ga = Tex(R"\nabla f = (yz,\ xz,\ xy)").set_color(DONE).next_to(parts, DOWN, buff=0.4).align_to(parts, LEFT)
        self.play(Write(ga))
        self.wait(1.0)

        self.play(FadeOut(VGroup(f, parts, ga)))
        fb = Tex(R"f(x,y,z) = x^2y^3 + z^2 + e^{xy}").set_color(ACCENT)
        fb.next_to(rule, RIGHT, buff=1.4).align_to(rule, UP)
        self.play(FadeIn(fb))
        partsb = VGroup(
            Tex(R"\partial f/\partial x = 2xy^3 + y\,e^{xy}").set_color(INK),
            Tex(R"\partial f/\partial y = 3x^2y^2 + x\,e^{xy}").set_color(INK),
            Tex(R"\partial f/\partial z = 2z").set_color(INK),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        partsb.next_to(fb, DOWN, buff=0.4).align_to(fb, LEFT)
        for line in partsb:
            self.play(FadeIn(line, UP), run_time=0.5)
            self.wait(0.2)
        gb = Tex(R"\nabla f = (2xy^3+ye^{xy},\ 3x^2y^2+xe^{xy},\ 2z)").set_color(DONE)
        gb.set_width(6.2).next_to(partsb, DOWN, buff=0.4).align_to(partsb, LEFT)
        self.play(Write(gb))
        self.wait(2)


class Jacobian(InteractiveScene):
    """정의 3-20 과 예제 3-25. 성분 함수마다 한 행, 변수마다 한 열."""

    def construct(self):
        head = slide_title("자코비안 행렬")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-20 · 예제 3-25")))

        F = Tex(R"F(x,y,z) = \begin{bmatrix} x - y + z^2 \\ x\cos y \\ y^2 e^{3z} \end{bmatrix}").set_color(ACCENT)
        F.set_height(1.8).to_edge(LEFT, buff=0.7).shift(0.8 * UP)
        self.play(Write(F), run_time=1.0)
        note = caption("행은 성분 함수 · 열은 변수", 24, GREY_B).next_to(F, DOWN, buff=0.45)
        self.play(FadeIn(note, UP))
        self.wait(0.4)

        J = Tex(R"J_F = \begin{bmatrix} 1 & -1 & 2z \\ \cos y & -x\sin y & 0 \\ 0 & 2ye^{3z} & 3y^2e^{3z} \end{bmatrix}").set_color(DONE)
        J.set_width(6.0).to_edge(RIGHT, buff=0.6).align_to(F, UP)
        self.play(Write(J), run_time=1.6)
        self.wait(0.5)

        heads = Tex(R"\partial/\partial x \qquad\quad \partial/\partial y \qquad\quad \partial/\partial z").set_color(GREY_B)
        heads.set_width(J.get_width() * 0.72).next_to(J, UP, buff=0.2).shift(0.45 * RIGHT)
        self.play(FadeIn(heads, UP))
        self.wait(1.0)
        last = caption("3 × 3 · 한 행이 한 그래디언트", 24, DONE).next_to(J, DOWN, buff=0.5)
        self.play(FadeIn(last, UP))
        self.wait(2)


class HessianLaplacian(InteractiveScene):
    """정의 3-21 · 3-22 와 예제 3-26 · 3-27. 헤시안의 대각합이 라플라시안이다."""

    def construct(self):
        head = slide_title("헤시안 행렬과 라플라시안")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-21 · 3-22 · 예제 3-26 · 3-27")))

        f = Tex(R"f(x,y,z) = x^2 - y^2 + z^3").set_color(ACCENT)
        f.to_edge(LEFT, buff=1.0).shift(1.9 * UP)
        self.play(FadeIn(f))
        grad = Tex(R"\nabla f = (2x,\ -2y,\ 3z^2)").set_color(INK).next_to(f, DOWN, buff=0.35).align_to(f, LEFT)
        self.play(FadeIn(grad, UP))
        H = Tex(R"H(f) = \begin{bmatrix} 2 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & 6z \end{bmatrix}").set_color(DONE)
        H.set_height(2.0).next_to(grad, DOWN, buff=0.45).align_to(f, LEFT)
        self.play(Write(H), run_time=1.2)
        note = caption("그래디언트를 한 번 더 미분", 24, GREY_B).next_to(H, DOWN, buff=0.35).align_to(f, LEFT)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        diag = VGroup(*[box(H.get_entries()[k], DONE, 0.06) for k in (0, 4, 8)]) if hasattr(H, "get_entries") else VGroup()
        lap = Tex(R"\nabla^2 f = 2 + (-2) + 6z = 6z").set_color(DONE)
        lap.next_to(H, RIGHT, buff=1.2).align_to(H, UP).shift(0.2 * DOWN)
        self.play(Write(lap))
        note2 = caption("대각 성분의 합이 라플라시안", 24, DONE).next_to(lap, DOWN, buff=0.35).align_to(lap, LEFT)
        self.play(FadeIn(note2, UP))
        self.wait(0.8)

        ex = VGroup(
            Tex(R"f(x,y) = x^3 + 2x + y^2").set_color(INK),
            Tex(R"\nabla^2 f = 6x + 2").set_color(DONE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ex.next_to(note2, DOWN, buff=0.6).align_to(lap, LEFT)
        self.play(FadeIn(ex[0], UP))
        self.play(FadeIn(ex[1], UP))
        self.wait(2)
