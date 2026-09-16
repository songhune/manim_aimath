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
    """정의 3-3 · 3-4. 합과 스칼라곱에 닫혀 있어야 벡터공간이다.

    열 가지 조건 가운데 (1) 과 (6) 이 '닫힘' 이고 나머지는 계산 규칙이다.
    닫히지 않는 집합의 예로 1사분면을 든다. 반대 벡터가 밖으로 나간다.
    """

    def construct(self):
        head = slide_title("벡터공간의 조건")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-3 · 3-4")))

        p = plane((-4, 4, 1), (-3, 3, 1), 4.9)
        p.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        rules = VGroup(
            Tex(R"(1)\ \ \mathbf{x},\mathbf{y}\in V \Rightarrow \mathbf{x}+\mathbf{y}\in V").set_color(INK),
            Tex(R"(6)\ \ \alpha\mathbf{x}\in V").set_color(INK),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        rules.set_width(5.2).next_to(p, RIGHT, buff=0.8).align_to(p, UP)
        self.play(FadeIn(rules))

        x = arrow(p, (1, 1), ACCENT)
        y = arrow(p, (2, -1), CALM)
        s = arrow(p, (3, 0), DONE)
        self.play(GrowArrow(x), GrowArrow(y))
        self.play(GrowArrow(s))
        ok1 = check_mark().next_to(rules[0], RIGHT, buff=0.3)
        self.play(FadeIn(ok1))
        self.play(FadeOut(VGroup(y, s)))
        two = arrow(p, (2, 2), DONE)
        self.play(GrowArrow(two))
        ok2 = check_mark().next_to(rules[1], RIGHT, buff=0.3)
        self.play(FadeIn(ok2))
        note = caption("평면 전체는 닫힌 집합", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(0.8)

        # 닫히지 않는 예 — 1사분면
        self.play(FadeOut(VGroup(x, two)))
        quad = Polygon(p.c2p(0, 0), p.c2p(4, 0), p.c2p(4, 3), p.c2p(0, 3))
        quad.set_fill(CALM, 0.18).set_stroke(width=0)
        self.play(FadeIn(quad))
        v = arrow(p, (2, 1), ACCENT)
        self.play(GrowArrow(v))
        w = arrow(p, (-2, -1), WARN)
        wl = vlabel(w, R"(-1)\mathbf{x}", WARN, DL)
        self.play(GrowArrow(w), FadeIn(wl))
        bad = cross_mark().next_to(rules[1], RIGHT, buff=0.3)
        self.play(FadeTransform(ok2, bad))
        note2 = caption("1사분면은 스칼라곱에 열림", 24, WARN).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        last = caption("닫힌 집합이 벡터공간", 26, DONE).next_to(rules, DOWN, buff=0.9)
        self.play(FadeIn(last, UP))
        self.wait(2)


class SubspaceLine(InteractiveScene):
    """정리 3-1 부분공간 판정법. 원점을 지나는 직선은 되고, 안 지나면 안 된다.

    예제 3-3 의 초평면 x_1 + ... + x_n = 0 도 같은 이유로 부분공간이다.
    """

    def construct(self):
        head = slide_title("부분공간 판정법")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정리 3-1 · 예제 3-3")))

        p = plane((-3, 4, 1), (-3, 4, 1), 5.0)
        p.to_edge(LEFT, buff=0.5).shift(0.5 * DOWN)
        self.play(FadeIn(p))

        rules = VGroup(
            Tex(R"(1)\ \ \mathbf{0}\in S").set_color(INK),
            Tex(R"(2)\ \ \mathbf{x},\mathbf{y}\in S \Rightarrow \mathbf{x}+\mathbf{y}\in S").set_color(INK),
            Tex(R"(3)\ \ \mathbf{x}\in S \Rightarrow \alpha\mathbf{x}\in S").set_color(INK),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rules.set_width(5.6).next_to(p, RIGHT, buff=0.8).align_to(p, UP)
        self.play(FadeIn(rules))

        line = Line(p.c2p(-3, -3), p.c2p(4, 4)).set_stroke(DONE, 3)
        ll = Tex(R"S:\ y=x").set_color(DONE).scale(0.8).next_to(p.c2p(2.4, 2.4), DR, buff=0.1)
        self.play(ShowCreation(line), FadeIn(ll))
        origin = Dot(p.c2p(0, 0), color=DONE)
        self.play(FadeIn(origin, scale=2))
        marks = VGroup(*[check_mark().next_to(r, RIGHT, buff=0.3) for r in rules])
        self.play(FadeIn(marks[0]))
        a = arrow(p, (1, 1), ACCENT)
        b = arrow(p, (2, 2), CALM, start=(1, 1))
        s = arrow(p, (3, 3), DONE)
        self.play(GrowArrow(a), GrowArrow(b))
        self.play(GrowArrow(s), FadeIn(marks[1]))
        self.play(FadeOut(VGroup(b, s)))
        two = arrow(p, (-2, -2), DONE)
        self.play(GrowArrow(two), FadeIn(marks[2]))
        note = caption("원점을 지나는 직선은 부분공간", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        # 원점을 지나지 않는 직선
        self.play(FadeOut(VGroup(a, two, line, ll, marks)))
        line2 = Line(p.c2p(-3, -1.5), p.c2p(2.5, 4)).set_stroke(WARN, 3)
        l2 = Tex(R"T:\ y=x+1.5").set_color(WARN).scale(0.8).next_to(p.c2p(-1.5, 0), DR, buff=0.1)
        self.play(ShowCreation(line2), FadeIn(l2))
        bad = cross_mark().next_to(rules[0], RIGHT, buff=0.3)
        self.play(Flash(origin, color=WARN), FadeIn(bad))
        note2 = caption("영벡터가 없으면 부분공간 아님", 24, WARN).move_to(note)
        self.play(FadeTransform(note, note2))
        self.wait(1.0)

        hyper = Tex(R"x_1 + x_2 + \cdots + x_n = 0").set_color(DONE)
        hyper.set_width(4.6).next_to(rules, DOWN, buff=0.8)
        last = caption("예제 3-3 도 원점을 지남", 24, DONE).next_to(hyper, DOWN, buff=0.3)
        self.play(Write(hyper))
        self.play(FadeIn(last, UP))
        self.wait(2)


class LinearCombination(InteractiveScene):
    """정의 3-5 와 예제 3-4. 2a + 3b 를 성분으로 계산하고 코드 한 줄과 잇는다."""

    def construct(self):
        head = slide_title("선형결합")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-5 · 예제 3-4")))

        rule = Tex(R"a_1\mathbf{x}_1 + a_2\mathbf{x}_2 + \cdots + a_k\mathbf{x}_k").set_color(INK)
        rule.set_width(6.0).move_to(2.1 * UP)
        self.play(Write(rule), run_time=1.0)
        self.wait(0.4)

        a = col([1, 0, 3], ACCENT)
        b = col([2, 1, 2], CALM)
        expr = VGroup(Tex("2").set_color(DONE), a, Tex("+").set_color(INK),
                      Tex("3").set_color(DONE), b).arrange(RIGHT, buff=0.3)
        expr.move_to(0.1 * DOWN + 3.2 * LEFT)
        self.play(FadeIn(expr))
        self.wait(0.4)

        ta = col([2, 0, 6], ACCENT)
        tb = col([6, 3, 6], CALM)
        mid = VGroup(Tex("=").set_color(INK), ta, Tex("+").set_color(INK), tb).arrange(RIGHT, buff=0.3)
        mid.next_to(expr, RIGHT, buff=0.3)
        self.play(FadeIn(mid))
        self.wait(0.4)

        out = col([8, 3, 12], DONE)
        res = VGroup(Tex("=").set_color(INK), out).arrange(RIGHT, buff=0.3).next_to(mid, RIGHT, buff=0.3)
        self.play(FadeIn(res))
        self.play(ShowCreation(box(out, DONE, 0.15)))
        self.wait(0.6)

        line = code("print(\"2*a + 3*b = \", 2*a + 3*b)", 24)
        line.to_edge(DOWN, buff=1.15)
        shown = code("2*a + 3*b =  [ 8  3 12]", 22, GREY_B).next_to(line, DOWN, buff=0.3)
        self.play(FadeIn(line, UP))
        self.play(FadeIn(shown, UP))
        self.wait(2)


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
    """정의 3-8 · 3-9 와 예제 3-8 · 3-9.

    생성하면서 독립이면 기저, 기저의 원소 수가 차원이다. 예제 3-9 는 셋째 벡터가
    앞 둘의 합이라 종속이고, 그래서 생성하는 공간의 차원이 2 다.
    """

    def construct(self):
        head = slide_title("기저와 차원")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정의 3-8 · 3-9 · 예제 3-8 · 3-9")))

        rule = VGroup(caption("생성", 26, ACCENT), Tex("+").set_color(INK),
                      caption("선형독립", 26, CALM), Tex(R"\Rightarrow").set_color(INK),
                      caption("기저", 26, DONE)).arrange(RIGHT, buff=0.35)
        rule.move_to(2.2 * UP)
        self.play(FadeIn(rule, UP))
        self.wait(0.5)

        vs = VGroup(col([1, 1, 0], INK), col([0, 1, 1], INK), col([1, 0, 1], INK))
        vs.arrange(RIGHT, buff=0.7).move_to(0.3 * DOWN + 3.3 * LEFT)
        lab = Tex(R"S").set_color(INK).next_to(vs, LEFT, buff=0.4)
        self.play(FadeIn(vs), FadeIn(lab))
        good = VGroup(
            Tex(R"a+c=0,\ a+b=0,\ b+c=0\ \Rightarrow\ a=b=c=0").set_color(CALM),
            Tex(R"\dim(\mathbb{R}^3)=3").set_color(DONE),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        good.set_width(5.6).next_to(vs, RIGHT, buff=0.8)
        self.play(FadeIn(good[0], UP))
        self.play(FadeIn(good[1], UP))
        note = caption("독립인 세 벡터 · R³ 의 기저", 24, DONE).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(note, UP))
        self.wait(1.2)

        # 예제 3-9
        self.play(FadeOut(VGroup(good, note)))
        third = col([1, 2, 1], WARN).move_to(vs[2])
        self.play(FadeTransform(vs[2], third))
        vs.remove(vs[2])
        eq = Tex(R"(1,2,1) = (1,1,0)+(0,1,1)").set_color(WARN)
        eq.set_width(5.0).next_to(third, RIGHT, buff=0.8).shift(0.4 * UP)
        self.play(Write(eq))
        dim = Tex(R"\dim(\mathrm{span}(S)) = 2").set_color(DONE)
        dim.next_to(eq, DOWN, buff=0.45).align_to(eq, LEFT)
        self.play(FadeIn(dim, UP))
        note2 = caption("셋째는 앞 둘의 합 · 종속", 24, WARN).move_to(note)
        self.play(FadeIn(note2, UP))
        self.wait(2)


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
    """예제 3-11. 두 변의 합이 남은 변보다 짧을 수 없다."""

    def construct(self):
        head = slide_title("삼각부등식")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.play(FadeIn(tag_under(head, "정리 3-3 (3) · 예제 3-11")))

        p = plane((-1, 5, 1), (-1, 4, 1), 4.6)
        p.to_edge(LEFT, buff=0.5).shift(0.55 * DOWN)
        self.play(FadeIn(p))

        x = arrow(p, (3, 1), ACCENT)
        y = arrow(p, (4, 3), CALM, start=(3, 1))
        s = arrow(p, (4, 3), DONE)
        xl = vlabel(x, R"\mathbf{x}", ACCENT, DOWN)
        yl = Tex(R"\mathbf{y}").set_color(CALM).scale(0.9).next_to(y, RIGHT, buff=0.1)
        sl = Tex(R"\mathbf{x}+\mathbf{y}").set_color(DONE).scale(0.9).next_to(s.get_center(), UL, buff=0.1)
        self.play(GrowArrow(x), FadeIn(xl))
        self.play(GrowArrow(y), FadeIn(yl))
        self.play(GrowArrow(s), FadeIn(sl))
        rule = Tex(R"\Vert \mathbf{x}+\mathbf{y}\Vert  \le \Vert \mathbf{x}\Vert  + \Vert \mathbf{y}\Vert ").set_color(DONE)
        rule.next_to(p, RIGHT, buff=0.9).align_to(p, UP).shift(0.2 * DOWN)
        self.play(Write(rule))
        note = caption("지름길이 돌아가는 길보다 짧음", 24, DONE).next_to(p, DOWN, buff=0.25)
        self.play(FadeIn(note, UP))
        self.wait(1.0)

        lines = VGroup(
            Tex(R"\mathbf{x}=(1,-1,2),\ \mathbf{y}=(0,1,1),\ \mathbf{x}+\mathbf{y}=(1,0,3)").set_color(INK),
            Tex(R"\Vert \mathbf{x}\Vert =\sqrt{6},\quad \Vert \mathbf{y}\Vert =\sqrt{2},\quad \Vert \mathbf{x}+\mathbf{y}\Vert =\sqrt{10}").set_color(INK),
            Tex(R"\sqrt{10}\approx 3.16 \ \le\ \sqrt{6}+\sqrt{2}\approx 3.86").set_color(DONE),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        lines.set_width(5.8).next_to(rule, DOWN, buff=0.6).align_to(rule, LEFT)
        for line in lines:
            self.play(FadeIn(line, UP), run_time=0.6)
            self.wait(0.3)
        self.play(ShowCreation(box(lines[2], DONE, 0.12)))
        self.wait(2)


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
