"""AI기초수학 — 교재 Chapter 4 선형변환과 랭크 정리.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 04_선형변환과 랭크 정리.pptx` 의
4.1 선형변환 · 4.2 랭크 정리에 붙는 보조 영상 12편.
수는 교재 정의 4-1~4-11 과 예제 4-1~4-15 의 값을 그대로 쓴다.
파일 이름은 앞 장과 같은 규칙이다(week04 = CH03, week05 = CH04).

예제 열다섯을 다 그리지 않는다. 격자가 움직이는 그림이 있어야 이해가 달라지는 것만 골랐다.
정리 4-1 · 4-2 의 증명, 예제 4-3(3I) · 4-9(I) 는 슬라이드 판서로 충분하다.

격자·기저벡터·단위정사각형은 `LinearTransformationScene` 에서 물려받는다
(once_useful_constructs/vector_space_scene.py, 3b1b eola 3~7장의 틀).

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week05.py
    ./render.sh check _2026/aimath/week05.py
    ./render.sh ppt   _2026/aimath/week05.py ReflectionTransform
"""
from manim_imports_ext import *

from _2026.aimath.week04 import (
    INK, ACCENT, CALM, WARN, DONE, TITLE_FONT, BODY_FONT,
    title, caption, code, slide_title, tag_under, col, box, plane, arrow, vlabel,
    check_mark, cross_mark,
)
from _2026.aimath.week03 import BACK_PLANE, FRONT_PLANE, overlay, code_block, mat


X_COLOR = GREEN_C
Y_COLOR = RED_C


def head_on_grid(scene, text, tag=None):
    """격자 위에 놓는 제목. 격자가 비쳐 읽히지 않으므로 뒷판을 깐다."""
    head = title(text, 34).to_corner(UL, buff=0.5)
    head.add_background_rectangle(opacity=0.85, buff=0.12)
    scene.add_foreground_mobject(head)
    scene.play(FadeIn(head), run_time=0.6)
    if tag:
        t = caption(tag, 22, GREY_B).next_to(head, DOWN, buff=0.2).align_to(head, LEFT)
        t.add_background_rectangle(opacity=0.85, buff=0.1)
        scene.add_foreground_mobject(t)
        scene.play(FadeIn(t), run_time=0.4)
    return head


def corner_panel(scene, mob, buff=0.6, shift=ORIGIN):
    """오른쪽 위에 얹는 행렬·수식 패널."""
    mob.to_corner(UR, buff=buff).shift(shift)
    mob.add_background_rectangle(opacity=0.85, buff=0.12)
    scene.add_foreground_mobject(mob)
    return mob


class GridScene(LinearTransformationScene):
    """이 장의 공통 설정. 뒤에 남는 격자는 옅게, 움직이는 격자는 파랗게."""
    include_background_plane = True
    include_foreground_plane = True
    background_plane_kwargs = BACK_PLANE
    foreground_plane_kwargs = FRONT_PLANE
    show_coordinates = True
    show_basis_vectors = True
    i_hat_color = X_COLOR
    j_hat_color = Y_COLOR

    def note(self, text, color=DONE, buff=0.4, size=28):
        new = caption(text, size, color)
        overlay(new, self, DOWN, buff)
        if getattr(self, "_note", None) is not None:
            self.play(FadeOut(self._note), FadeIn(new, UP), run_time=0.5)
            self.foreground_mobjects.remove(self._note)
        else:
            self.play(FadeIn(new, UP), run_time=0.5)
        self._note = new
        return new

    def vec(self, coords, color, label=None, new_label=None, direction="right"):
        v = self.add_vector([coords[0], coords[1], 0], color=color, animate=True)
        if label:
            self.add_transformable_label(v, label, new_label=new_label,
                                         direction=direction, color=color)
        return v


# ─────────────────────────────────────────────────────────────
# 4.1 선형변환
# ─────────────────────────────────────────────────────────────
class LinearTransformationIntro(GridScene):
    """정의 4-1. 선형변환은 평면 전체를 움직이는 함수다.

    격자선이 평행하고 등간격인 채로, 원점이 제자리인 채로 움직이는 것이 선형변환이다.
    정의 4-1 의 두 조건은 그 그림의 성질을 적은 것이다 — 평행사변형이 평행사변형으로 가면
    (1) 이고, 같은 직선 위의 배수가 배수로 가면 (2) 다.
    참고: legacy/_2016/eola/chapter3.py IntroduceLinearTransformations · AdditivityProperty
    """
    matrix = [[1, 1], [0, 2]]      # 열 (1,0) · (1,2)

    def construct(self):
        head_on_grid(self, "선형변환이란", "정의 4-1 · 그림 4-1")

        x = self.vec((1.5, 0.5), ACCENT, R"\mathbf{x}", R"L(\mathbf{x})")
        y = self.vec((-1, 1), CALM, R"\mathbf{y}", R"L(\mathbf{y})", direction="left")
        s = self.vec((0.5, 1.5), DONE, R"\mathbf{x}+\mathbf{y}", R"L(\mathbf{x}+\mathbf{y})")
        side1 = DashedLine(x.get_end(), s.get_end()).set_stroke(GREY_B, 2)
        side2 = DashedLine(y.get_end(), s.get_end()).set_stroke(GREY_B, 2)
        self.add_transformable_mobject(side1, side2)
        self.play(ShowCreation(side1), ShowCreation(side2), run_time=0.6)
        self.note("벡터의 합은 평행사변형", GREY_B)
        self.wait(0.6)

        # add_background_rectangle 은 사각형을 [0] 에 끼운다. 조건 둘은 따로 붙들어 둔다.
        cond1 = Tex(R"(1)\ L(\mathbf{x}+\mathbf{y})=L(\mathbf{x})+L(\mathbf{y})")
        cond2 = Tex(R"(2)\ L(\alpha\mathbf{x})=\alpha L(\mathbf{x})")
        panel = VGroup(cond1, cond2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).set_color(INK)
        panel.set_width(4.6)
        corner_panel(self, panel)
        self.play(FadeIn(panel, DOWN))
        self.wait(0.5)

        self.note("평면 전체가 함께 움직임", ACCENT)
        self.apply_matrix(self.matrix, run_time=2.4)
        self.wait(0.5)
        self.note("평행사변형은 평행사변형으로 · (1)", DONE)
        self.play(cond1.animate.set_color(DONE), run_time=0.5)
        self.wait(1.0)

        # (2) 같은 직선 위의 배수. 2x 를 보이고 L(2x) = 2L(x) 를 읽는다.
        twice = self.add_vector([4, 2, 0], color=ACCENT, animate=False)
        twice.set_opacity(0.55)
        lab = Tex(R"2L(\mathbf{x})").set_color(ACCENT).scale(0.8)
        lab.next_to(twice.get_end(), RIGHT, buff=0.1)
        lab.add_background_rectangle(opacity=0.7, buff=0.05)
        self.play(GrowArrow(twice), FadeIn(lab), run_time=0.8)
        self.note("배수는 같은 직선 위 배수로 · (2)", DONE)
        self.play(cond2.animate.set_color(DONE), run_time=0.5)
        self.wait(1.0)

        rules = VGroup(caption("격자선은 평행 · 등간격", 24, GREY_B),
                       caption("원점은 제자리", 24, GREY_B))
        rules.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rules.to_corner(DL, buff=0.5)
        rules.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(rules)
        self.play(FadeIn(rules, UP))
        self.wait(2)


class NonlinearExamples(GridScene):
    """예제 4-1 · 4-2. 3x 는 선형, ax + b 는 선형이 아니다.

    b 가 원점을 옮긴다. 원점이 움직이면 L(0) = 0 이 깨지고, 그 순간 (2) 에 α = 0 을 넣은
    식이 성립하지 않는다. 격자는 그대로 평행·등간격이라 눈으로는 속기 쉬운 반례다.
    참고: legacy/_2016/eola/chapter3.py 의 비선형 반례 세 편 (458~490행)
    """

    def construct(self):
        head_on_grid(self, "선형인 것과 아닌 것", "예제 4-1 · 4-2")
        x = self.vec((2, 1), ACCENT, R"\mathbf{x}", R"3\mathbf{x}")

        f1 = Tex(R"L(\mathbf{x})=3\mathbf{x}").set_color(DONE).scale(1.1)
        corner_panel(self, f1)
        self.play(FadeIn(f1, DOWN))
        self.note("예제 4-1 · 세 배로 늘리기", GREY_B)
        self.apply_matrix([[3, 0], [0, 3]], run_time=2.0)
        self.wait(0.4)
        marks = VGroup(Tex(R"3(\mathbf{x}+\mathbf{y})=3\mathbf{x}+3\mathbf{y}"),
                       Tex(R"3(\alpha\mathbf{x})=\alpha(3\mathbf{x})")).set_color(DONE)
        marks.arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(4.2)
        marks.next_to(f1, DOWN, buff=0.3).align_to(f1, RIGHT)
        marks.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(marks)
        self.play(FadeIn(marks, UP))
        self.note("원점 제자리 · 격자 등간격 · 선형", DONE)
        self.wait(1.2)

        self.apply_inverse([[3, 0], [0, 3]], run_time=1.2)
        self.play(FadeOut(marks), run_time=0.3)
        self.foreground_mobjects.remove(marks)
        f2 = Tex(R"L(\mathbf{x})=a\mathbf{x}+\mathbf{b},\ \mathbf{b}\ne\mathbf{0}").set_color(WARN)
        f2.set_width(4.4).move_to(f1).align_to(f1, RIGHT)
        f2.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(f2)
        self.play(FadeOut(f1), FadeIn(f2), run_time=0.5)
        self.foreground_mobjects.remove(f1)
        self.note("예제 4-2 · b 만큼 밀기", GREY_B)

        shift = np.array([1.5, 1.0, 0])
        self.apply_nonlinear_transformation(lambda p: p + shift, run_time=2.0)
        self.wait(0.4)
        origin_dot = Dot(shift, radius=0.1).set_color(WARN)
        zero = Tex(R"L(\mathbf{0})=\mathbf{b}\ne\mathbf{0}").set_color(WARN).scale(0.9)
        zero.next_to(origin_dot, DOWN, buff=0.5)
        zero.add_background_rectangle(opacity=0.8, buff=0.06)
        self.play(FadeIn(origin_dot, scale=0.5), FadeIn(zero), run_time=0.6)
        self.note("원점이 움직임 · 선형 아님", WARN)
        why = Tex(R"L(\alpha\mathbf{x})=\alpha a\mathbf{x}+\mathbf{b}\ \ne\ \alpha L(\mathbf{x})").set_color(WARN)
        why.set_width(5.0).next_to(f2, DOWN, buff=0.3).align_to(f2, RIGHT)
        why.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(why)
        self.play(FadeIn(why, UP))
        self.wait(2)


class ColumnsAreImages(GridScene):
    """정리 4-2 · 예제 4-4. 표준행렬의 열은 기저벡터가 가는 자리다.

    L(1,0) = (2,3) 은 첫째 열 그대로다. L(1,1) = (4,5) 에서 L(0,1) 을 빼내는 것이 이 예제의 요점 —
    (1,1) = e1 + e2 이므로 L(e2) = L(1,1) − L(e1) = (2,2).
    참고: legacy/_2016/eola/chapter3.py ColumnsToBasisVectors
    """
    matrix = [[2, 2], [3, 2]]      # 열 (2,3) · (2,2)

    def construct(self):
        head_on_grid(self, "표준행렬의 열", "정리 4-2 · 예제 4-4")
        u = self.vec((1, 1), DONE, "(1,1)", "(4,5)")

        given = VGroup(Tex(R"L(1,0)=(2,3)").set_color(X_COLOR),
                       Tex(R"L(1,1)=(4,5)").set_color(DONE))
        given.arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(3.4)
        corner_panel(self, given)
        self.play(FadeIn(given, DOWN))

        unknown = Matrix([["2", "?"], ["3", "?"]], h_buff=0.8).set_color(INK)
        unknown.get_entries()[0].set_color(X_COLOR)
        unknown.get_entries()[2].set_color(X_COLOR)
        unknown.set_height(1.4).next_to(given, DOWN, buff=0.35).align_to(given, RIGHT)
        unknown.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(unknown)
        self.play(FadeIn(unknown, UP))
        self.note("첫째 열 = L(e1) · 둘째 열은 아직", GREY_B)
        self.wait(0.6)

        self.apply_matrix(self.matrix, run_time=2.2)
        self.wait(0.4)
        self.note("e1 은 (2,3) 으로 · (1,1) 은 (4,5) 로", DONE)
        self.wait(0.8)

        e2 = Tex(R"L(0,1)=L(1,1)-L(1,0)=(2,2)").set_color(Y_COLOR)
        e2.set_width(5.2)
        overlay(e2, self, DOWN, 1.1)
        self.play(FadeIn(e2, UP))
        self.note("(1,1) = e1 + e2 · 빼서 얻음", Y_COLOR)
        self.wait(0.8)

        full = Matrix([["2", "2"], ["3", "2"]], h_buff=0.8).set_color(INK)
        for k in (0, 2):
            full.get_entries()[k].set_color(X_COLOR)
        for k in (1, 3):
            full.get_entries()[k].set_color(Y_COLOR)
        full.set_height(1.4).move_to(unknown).align_to(unknown, RIGHT)
        full.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(full)
        self.play(FadeOut(unknown), FadeIn(full), run_time=0.6)
        self.foreground_mobjects.remove(unknown)
        a = Tex(R"A=[\,L(\mathbf{e}_1)\ \ L(\mathbf{e}_2)\,]").set_color(DONE)
        a.set_width(3.6).next_to(full, DOWN, buff=0.3).align_to(full, RIGHT)
        a.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(a)
        self.play(FadeIn(a, UP))
        self.note("열 = 기저벡터의 상", DONE)
        self.wait(2)


class StandardMatrixFromPair(InteractiveScene):
    """예제 4-5. 기저가 아닌 두 벡터의 상이 주어지면 역행렬로 푼다.

    A(1,2) = (2,3), A(3,4) = (4,5) 를 한 식 AP = B 로 묶으면 A = BP⁻¹ 이다.
    답 [[0,1],[-1,2]] 는 예제 4-8 의 A1 과 같은 행렬이다.
    """

    def construct(self):
        head = slide_title("표준행렬 구하기")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "예제 4-5")
        self.play(FadeIn(tag))

        p = plane((-1, 6, 1), (-1, 6, 1), 4.0).to_edge(LEFT, buff=0.5).shift(0.3 * DOWN)
        self.play(FadeIn(p))
        p1 = arrow(p, (1, 2), GREY_B); p2 = arrow(p, (3, 4), GREY_B)
        q1 = arrow(p, (2, 3), ACCENT); q2 = arrow(p, (4, 5), CALM)
        l1 = vlabel(p1, "(1,2)", GREY_B, LEFT); l2 = vlabel(p2, "(3,4)", GREY_B, LEFT)
        m1 = vlabel(q1, "(2,3)", ACCENT, RIGHT); m2 = vlabel(q2, "(4,5)", CALM, RIGHT)
        self.play(GrowArrow(p1), GrowArrow(p2), FadeIn(l1), FadeIn(l2))
        self.play(TransformFromCopy(p1, q1), TransformFromCopy(p2, q2), FadeIn(m1), FadeIn(m2),
                  run_time=1.2)

        cap = caption("기저가 아닌 두 벡터의 상", 24, GREY_B).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap))

        steps = VGroup(
            Tex(R"A\begin{bmatrix}1\\2\end{bmatrix}=\begin{bmatrix}2\\3\end{bmatrix},\ "
                R"A\begin{bmatrix}3\\4\end{bmatrix}=\begin{bmatrix}4\\5\end{bmatrix}"),
            Tex(R"A\begin{bmatrix}1&3\\2&4\end{bmatrix}=\begin{bmatrix}2&4\\3&5\end{bmatrix}"),
            Tex(R"A=\begin{bmatrix}2&4\\3&5\end{bmatrix}\begin{bmatrix}1&3\\2&4\end{bmatrix}^{-1}"),
            Tex(R"=\begin{bmatrix}2&4\\3&5\end{bmatrix}\cdot\frac{1}{-2}"
                R"\begin{bmatrix}4&-3\\-2&1\end{bmatrix}"),
            Tex(R"A=\begin{bmatrix}0&1\\-1&2\end{bmatrix}"),
        ).set_color(INK)
        steps[4].set_color(DONE)
        steps.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.set_width(6.0)
        if steps.get_height() > 5.3:
            steps.set_height(5.3)
        steps.to_edge(RIGHT, buff=0.5).align_to(tag, UP)

        self.play(Write(steps[0]), run_time=1.0)
        self.wait(0.4)
        cap2 = caption("두 식을 한 행렬식으로", 24, ACCENT).move_to(cap)
        self.play(FadeTransform(cap, cap2), FadeIn(steps[1], UP)); cap = cap2
        self.wait(0.6)
        cap2 = caption("오른쪽에서 역행렬을 곱하기", 24, CALM).move_to(cap)
        self.play(FadeTransform(cap, cap2), FadeIn(steps[2], UP)); cap = cap2
        self.wait(0.6)
        self.play(FadeIn(steps[3], UP)); self.wait(0.6)
        self.play(FadeIn(steps[4], UP))
        chk = Tex(R"\begin{bmatrix}0&1\\-1&2\end{bmatrix}\begin{bmatrix}1\\2\end{bmatrix}"
                  R"=\begin{bmatrix}2\\3\end{bmatrix}\ \checkmark").set_color(DONE)
        chk.set_width(3.4).next_to(p, DOWN, buff=0.15)
        cap2 = caption("확인 · 예제 4-8 의 A1 과 같은 행렬", 24, DONE).move_to(cap)
        self.play(FadeTransform(cap, cap2), FadeIn(chk, UP))
        self.wait(2)


class ReflectionTransform(GridScene):
    """정의 4-3 · 예제 4-6. x 축 반사는 y 의 부호를, y 축 반사는 x 의 부호를 바꾼다.

    표준행렬의 열을 읽으면 된다 — e1 은 제자리, e2 는 -e2 로 가므로 [[1,0],[0,-1]] 이다.
    (2,1) → (2,-1), (3,5) → (-3,5). (3,5) 가 격자 밖으로 나가므로 화면을 조금 넓혀 둔다.
    """
    background_plane_kwargs = dict(BACK_PLANE, x_range=(-10, 10, 1), y_range=(-6, 6, 1))
    foreground_plane_kwargs = dict(FRONT_PLANE, x_range=(-10, 10, 1), y_range=(-6, 6, 1))

    def construct(self):
        self.frame.set_height(11.5)
        for mob in self.foreground_mobjects:
            mob.fix_in_frame()
        head = head_on_grid(self, "반사변환", "정의 4-3 · 예제 4-6")
        self.fix_foreground()

        x = self.vec((2, 1), ACCENT, "(2,1)", "(2,-1)")
        mx = Matrix([["1", "0"], ["0", "-1"]], h_buff=0.8).set_color(INK).set_height(1.4)
        corner_panel(self, mx)
        mx.fix_in_frame()
        self.play(FadeIn(mx, DOWN))
        self.note("x 축 기준 반사 · e2 가 −e2 로", GREY_B)
        self.apply_matrix([[1, 0], [0, -1]], path_arc=0, run_time=1.8)
        self.wait(0.5)
        self.note("(2,1) → (2,−1) · y 의 부호만", DONE)
        self.wait(1.0)

        self.apply_matrix([[1, 0], [0, -1]], path_arc=0, run_time=1.0)
        self.play(FadeOut(x), run_time=0.3)
        self.moving_vectors.remove(x)
        for lab in list(self.transformable_labels):
            self.remove(lab)
            self.transformable_labels.remove(lab)
        y = self.vec((3, 5), CALM, "(3,5)", "(-3,5)")
        my = Matrix([["-1", "0"], ["0", "1"]], h_buff=0.8).set_color(INK).set_height(1.4)
        my.move_to(mx)
        my.add_background_rectangle(opacity=0.85, buff=0.12)
        my.fix_in_frame()
        self.add_foreground_mobject(my)
        self.play(FadeOut(mx), FadeIn(my), run_time=0.5)
        self.foreground_mobjects.remove(mx)
        self.note("y 축 기준 반사 · e1 이 −e1 로", GREY_B)
        self.apply_matrix([[-1, 0], [0, 1]], path_arc=0, run_time=1.8)
        self.wait(0.5)
        self.note("(3,5) → (−3,5) · x 의 부호만", DONE)
        self.wait(2)

    def fix_foreground(self):
        for mob in self.foreground_mobjects:
            mob.fix_in_frame()

    def note(self, text, color=DONE, buff=0.4, size=28):
        new = super().note(text, color, buff, size)
        new.fix_in_frame()
        return new


class RotationTransform(GridScene):
    """정의 4-4 · 예제 4-7. 회전변환의 열은 회전한 e1, e2 다.

    e1 = (1,0) 을 θ 만큼 돌리면 (cos θ, sin θ), e2 = (0,1) 을 돌리면 (−sin θ, cos θ).
    이 두 열이 표준행렬이다. 30°, 45°, 60°, 90° 를 차례로 쌓아 돌린다.
    참고: legacy/_2016/eola/chapter3.py Rotation · Describe90DegreeRotation
    """
    steps = [
        (30, R"\begin{bmatrix}\frac{\sqrt3}{2}&-\frac12\\[2pt]\frac12&\frac{\sqrt3}{2}\end{bmatrix}"),
        (45, R"\begin{bmatrix}\frac{\sqrt2}{2}&-\frac{\sqrt2}{2}\\[2pt]\frac{\sqrt2}{2}&\frac{\sqrt2}{2}\end{bmatrix}"),
        (60, R"\begin{bmatrix}\frac12&-\frac{\sqrt3}{2}\\[2pt]\frac{\sqrt3}{2}&\frac12\end{bmatrix}"),
        (90, R"\begin{bmatrix}0&-1\\1&0\end{bmatrix}"),
    ]

    def construct(self):
        head_on_grid(self, "회전변환", "정의 4-4 · 예제 4-7")
        general = Tex(R"\begin{bmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{bmatrix}")
        general.set_color(INK).set_height(1.4)
        corner_panel(self, general)
        self.play(FadeIn(general, DOWN))
        self.note("열 = 회전한 e1, e2", GREY_B)
        self.wait(0.6)

        x = self.vec((3, 1), ACCENT, R"\mathbf{x}", R"L(\mathbf{x})")
        current = 0
        label = None
        for deg, tex in self.steps:
            delta = deg - current
            rad = delta * DEGREES
            m = [[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]]
            self.note("반시계로 %d°" % deg, DONE)
            self.apply_matrix(m, run_time=1.2)
            current = deg
            new = Tex(tex).set_color(DONE).set_height(1.5)
            new.next_to(general, DOWN, buff=0.3).align_to(general, RIGHT)
            new.add_background_rectangle(opacity=0.85, buff=0.1)
            self.add_foreground_mobject(new)
            if label is None:
                self.play(FadeIn(new, UP), run_time=0.5)
            else:
                self.play(FadeOut(label), FadeIn(new), run_time=0.5)
                self.foreground_mobjects.remove(label)
            label = new
            self.wait(0.7)
        self.note("90° · e1 이 e2 자리로", DONE)
        self.wait(2)


class CompositeTransform(GridScene):
    """정의 4-5 · 정리 4-3 · 예제 4-8. 합성변환의 표준행렬은 곱 A2A1 이다.

    먼저 하는 변환이 오른쪽이다. A1 → A2 순서로 격자를 움직이면 A2A1 = [[0,1],[-1,4]] 이고,
    순서를 바꾸면 A1A2 = [[2,1],[3,2]] 로 다른 결과다.
    참고: legacy/_2016/eola/chapter4.py (곱의 순서)
    """
    A1 = [[0, 1], [-1, 2]]
    A2 = [[1, 0], [2, 1]]

    def construct(self):
        head_on_grid(self, "합성변환의 표준행렬", "정리 4-3 · 예제 4-8")
        self.add_unit_square()
        self.play(FadeIn(self.square))

        m1 = Matrix([["0", "1"], ["-1", "2"]], h_buff=0.75).set_color(ACCENT)
        m2 = Matrix([["1", "0"], ["2", "1"]], h_buff=0.75).set_color(CALM)
        t1 = Tex("A_1").set_color(ACCENT); t2 = Tex("A_2").set_color(CALM)
        row = VGroup(VGroup(t1, m1).arrange(DOWN, buff=0.15),
                     VGroup(t2, m2).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.5)
        row.set_height(1.9)
        corner_panel(self, row)
        self.play(FadeIn(row, DOWN))

        self.note("먼저 A1", ACCENT)
        self.apply_matrix(self.A1, run_time=1.6)
        self.wait(0.3)
        self.note("이어서 A2", CALM)
        self.apply_matrix(self.A2, run_time=1.6)
        self.wait(0.3)
        prod = Tex(R"A_2A_1=\begin{bmatrix}0&1\\-1&4\end{bmatrix}").set_color(DONE)
        prod.set_width(3.6).next_to(row, DOWN, buff=0.3).align_to(row, RIGHT)
        prod.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(prod)
        self.play(FadeIn(prod, UP))
        self.note("먼저 한 것이 오른쪽 · A2A1", DONE)
        self.wait(1.0)

        total = np.array(self.A2) @ np.array(self.A1)
        self.apply_inverse(total, run_time=1.0)
        self.note("순서를 바꾸면", WARN)
        self.apply_matrix(self.A2, run_time=1.2)
        self.apply_matrix(self.A1, run_time=1.2)
        other = Tex(R"A_1A_2=\begin{bmatrix}2&1\\3&2\end{bmatrix}").set_color(WARN)
        other.set_width(3.6).next_to(prod, DOWN, buff=0.25).align_to(prod, RIGHT)
        other.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(other)
        self.play(FadeIn(other, UP))
        self.note("다른 격자 · 곱은 순서를 지킴", WARN)
        line = code("cal_Comp_Transformation = Matrix2@Matrix1", 20)
        overlay(line, self, DOWN, 1.05)
        self.play(FadeIn(line, UP))
        self.wait(2)


class InverseTransform(GridScene):
    """정의 4-7 · 예제 4-10. 역변환은 변환을 되돌린다.

    A = [[1,2],[1,3]] 이 (−1,1) 을 (1,2) 로 보내므로, A⁻¹ = [[3,−2],[−1,1]] 은 (1,2) 를 (−1,1) 로
    돌려보낸다. L⁻¹((1,2)) 는 "무엇이 (1,2) 로 갔나" 를 묻는 것이다.
    CH02 의 `InverseAsUndo` 와 같은 그림에 예제 값을 붙였다.
    """
    A = [[1, 2], [1, 3]]

    def construct(self):
        head_on_grid(self, "역변환", "정의 4-7 · 예제 4-10")
        ma = Tex(R"A=\begin{bmatrix}1&2\\1&3\end{bmatrix}").set_color(ACCENT).set_height(1.3)
        corner_panel(self, ma)
        self.play(FadeIn(ma, DOWN))

        v = self.vec((-1, 1), DONE, "(-1,1)", "(1,2)", direction="left")
        self.note("A 가 (−1,1) 을 보내는 곳", GREY_B)
        self.apply_matrix(self.A, run_time=2.0)
        self.wait(0.6)
        self.note("(1,2) 에 닿음", ACCENT)
        self.wait(0.6)

        inv = Tex(R"A^{-1}=\begin{bmatrix}3&-2\\-1&1\end{bmatrix}").set_color(DONE)
        inv.set_height(1.3).next_to(ma, DOWN, buff=0.3).align_to(ma, RIGHT)
        inv.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(inv)
        self.play(FadeIn(inv, UP))
        self.note("A⁻¹ 이 되돌림", DONE)
        self.apply_inverse(self.A, run_time=2.0)
        self.wait(0.5)
        ans = Tex(R"L^{-1}((1,2))=\begin{bmatrix}3&-2\\-1&1\end{bmatrix}"
                  R"\begin{bmatrix}1\\2\end{bmatrix}=\begin{bmatrix}-1\\1\end{bmatrix}").set_color(DONE)
        ans.set_width(5.6)
        overlay(ans, self, DOWN, 1.05)
        self.play(FadeIn(ans, UP))
        self.note("(1,2) 로 간 것은 (−1,1)", DONE)
        self.wait(2)


class OrthogonalOperator(GridScene):
    """정의 4-8 · 정리 4-4 · 예제 4-11 · 4-12. 직교연산자는 길이와 각을 지킨다.

    예제 4-11 의 A 는 22.5° 직선에 대한 반사다. 원은 원으로, 직교하는 두 벡터는 직교하는
    두 벡터로 간다. AᵀA = I 가 그 성질의 행렬 표현이다. 예제 4-12 는 성분의 자리만 바꾸는
    행렬이라 노름이 그대로다.
    """
    A = [[np.sqrt(2) / 2, np.sqrt(2) / 2], [np.sqrt(2) / 2, -np.sqrt(2) / 2]]

    def construct(self):
        head_on_grid(self, "직교연산자", "정의 4-8 · 정리 4-4 · 예제 4-11")
        ma = Tex(R"A=\begin{bmatrix}\frac{\sqrt2}{2}&\frac{\sqrt2}{2}\\[2pt]"
                 R"\frac{\sqrt2}{2}&-\frac{\sqrt2}{2}\end{bmatrix}").set_color(ACCENT)
        ma.set_height(1.5)
        corner_panel(self, ma)
        self.play(FadeIn(ma, DOWN))

        circle = Circle(radius=np.sqrt(5)).set_stroke(DONE, 2)
        circle.move_to(self.plane.c2p(0, 0))
        self.add_transformable_mobject(circle)
        self.play(ShowCreation(circle))
        x = self.vec((2, 1), ACCENT, R"\mathbf{x}", R"L(\mathbf{x})")
        y = self.vec((-1, 2), CALM, R"\mathbf{y}", R"L(\mathbf{y})", direction="left")
        self.note("x ⊥ y · 길이 √5", GREY_B)
        self.wait(0.5)

        self.apply_matrix(self.A, path_arc=0, run_time=2.2)
        self.wait(0.4)
        self.note("원은 원으로 · 직각은 직각으로", DONE)
        facts = VGroup(
            Tex(R"\Vert L(\mathbf{x})\Vert=\Vert\mathbf{x}\Vert"),
            Tex(R"L(\mathbf{x})\cdot L(\mathbf{y})=\mathbf{x}\cdot\mathbf{y}=0"),
            Tex(R"A^{T}A=I"),
        ).set_color(DONE).arrange(DOWN, buff=0.22, aligned_edge=LEFT).set_width(4.2)
        facts.next_to(ma, DOWN, buff=0.3).align_to(ma, RIGHT)
        facts.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(facts)
        self.play(FadeIn(facts, UP))
        self.wait(1.2)

        # 예제 4-12 — 성분의 자리만 바꾸는 4×4 행렬
        perm = Tex(R"A\begin{bmatrix}x_1\\x_2\\x_3\\x_4\end{bmatrix}"
                   R"=\begin{bmatrix}x_2\\x_3\\x_1\\x_4\end{bmatrix}").set_color(CALM)
        perm.set_height(2.2).to_edge(LEFT, buff=0.6).shift(1.0 * DOWN)
        perm.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(perm)
        self.play(FadeIn(perm, UP))
        self.note("예제 4-12 · 자리만 바뀜 · 노름 그대로", CALM)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4.2 랭크 정리
# ─────────────────────────────────────────────────────────────
class ColumnSpaceNullSpace(InteractiveScene):
    """정의 4-9 · 4-10 · 예제 4-13. 열공간 · 행공간 · 영공간을 한 행렬에서.

    A = [[1,0,1],[0,1,2]] 는 R³ → R² 다. 열공간은 R² 전체(랭크 2), 행공간은 R³ 안의 평면,
    영공간은 그 평면에 수직인 직선 t(−1,−2,1) 이다. 3차원 축에 행공간 평면과 영공간 직선을
    그려 둘이 수직임을 본다. 카메라는 축 중심으로 천천히 돈다.
    참고: legacy/_2016/eola/chapter6.py NameNullSpace
    """
    r1 = (1, 0, 1)
    r2 = (0, 1, 2)
    nul = (-1, -2, 1)

    def construct(self):
        head = slide_title("열공간 · 행공간 · 영공간")
        head.fix_in_frame()
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "정의 4-9 · 4-10 · 예제 4-13")
        tag.fix_in_frame()
        self.play(FadeIn(tag))

        panel = VGroup(
            Tex(R"A=\begin{bmatrix}1&0&1\\0&1&2\end{bmatrix}").set_color(INK),
            Tex(R"\mathrm{Col}(A)=\mathrm{span}\{(1,0),(0,1)\}=\mathbb{R}^2").set_color(ACCENT),
            Tex(R"\mathrm{rank}(A)=2").set_color(ACCENT),
            Tex(R"\mathrm{Row}(A)=\mathrm{span}\{(1,0,1),(0,1,2)\}").set_color(CALM),
            Tex(R"A\mathbf{x}=\mathbf{0}:\ x_1+x_3=0,\ x_2+2x_3=0").set_color(WARN),
            Tex(R"\mathrm{Nul}(A)=\{t(-1,-2,1)\}").set_color(WARN),
        ).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        panel.set_width(5.4).to_edge(RIGHT, buff=0.4).shift(0.1 * DOWN)
        panel.fix_in_frame()

        ax = ThreeDAxes(x_range=(-2, 2, 1), y_range=(-3, 2, 1), z_range=(-1, 3, 1),
                        width=4.2, height=5.0, depth=4.2,
                        axis_config=dict(stroke_color=GREY_B, stroke_width=2, include_tip=True))
        ax.move_to(ORIGIN)
        labels = VGroup(Tex("x_1"), Tex("x_2"), Tex("x_3")).set_color(GREY_B)
        labels[0].next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        labels[1].next_to(ax.y_axis.get_end(), UP, buff=0.1)
        labels[2].next_to(ax.z_axis.get_end(), OUT, buff=0.1)
        for lab in labels:
            lab.rotate(PI / 2, RIGHT)
        self.frame.reorient(-40, 64, 0, center=(2.0, 0.3, -0.2), height=9.8)
        self.play(FadeIn(ax), FadeIn(labels), FadeIn(panel[0]))
        self.frame.add_updater(lambda f, dt: f.increment_theta(0.04 * dt))

        cap = caption("정의역 R³ 안에서", 24, GREY_B).to_edge(DOWN, buff=0.45)
        cap.fix_in_frame()
        self.play(FadeIn(cap))

        def say(text, color=DONE):
            nonlocal cap
            new = caption(text, 24, color).to_edge(DOWN, buff=0.45)
            new.fix_in_frame()
            self.play(FadeTransform(cap, new), run_time=0.4)
            cap = new

        def arr3(end, color, start=(0, 0, 0)):
            m = Arrow(ax.c2p(*start), ax.c2p(*end), buff=0, thickness=5).set_color(color)
            m.set_stroke(color, 2)
            return m

        self.play(FadeIn(panel[1], UP)); self.wait(0.3)
        self.play(FadeIn(panel[2], UP))
        say("열 둘이 R² 를 채움 · 랭크 2", ACCENT)
        self.wait(0.8)

        a1 = arr3(self.r1, CALM); a2 = arr3(self.r2, CALM)
        pts = []
        for a_, b_ in ((-1.2, -1.2), (1.4, -1.2), (1.4, 1.1), (-1.2, 1.1)):
            pts.append(ax.c2p(*[a_ * self.r1[k] + b_ * self.r2[k] for k in range(3)]))
        row_plane = Polygon(*pts).set_fill(CALM, 0.22).set_stroke(CALM, 1, opacity=0.5)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(panel[3], UP))
        self.play(FadeIn(row_plane))
        say("행벡터 둘이 만드는 평면 · 행공간", CALM)
        self.wait(0.8)

        self.play(FadeIn(panel[4], UP))
        say("Ax = 0 의 해", WARN)
        self.wait(0.5)
        nline = Line(ax.c2p(*[-1.1 * c for c in self.nul]), ax.c2p(*[1.3 * c for c in self.nul]))
        nline.set_stroke(WARN, 3)
        nvec = arr3(self.nul, WARN)
        self.play(ShowCreation(nline), GrowArrow(nvec), FadeIn(panel[5], UP))
        say("영공간은 직선 · 행공간에 수직", WARN)
        self.wait(1.0)
        dims = Tex(R"\mathrm{rank}(A)+\mathrm{nullity}(A)=2+1=3").set_color(DONE)
        dims.set_width(4.8).next_to(panel, DOWN, buff=0.35).align_to(panel, LEFT)
        dims.fix_in_frame()
        self.play(FadeIn(dims, UP))
        say("평면 2 + 직선 1 = 열 개수 3", DONE)
        self.wait(2)


class RankAndKernel(GridScene):
    """정의 4-10 · 4-11 · 정리 4-6 을 2차원에서. 랭크는 상의 차원, 퇴화차수는 눌린 방향의 수.

    단위행렬은 평면 전체(랭크 2, 퇴화차수 0). [[1,2],[2,4]] 는 평면을 직선으로 누르고(랭크 1),
    (2,−1) 방향의 벡터는 모두 원점으로 간다(퇴화차수 1). 영행렬은 점 하나(랭크 0, 퇴화차수 2).
    어느 경우든 둘의 합이 2 다.
    참고: legacy/_2016/eola/chapter6.py DefineRank · NameNullSpace
    """
    A = [[1, 2], [2, 4]]

    def construct(self):
        head_on_grid(self, "랭크와 영공간", "정의 4-10 · 4-11 · 정리 4-6")
        rows = [
            Tex(R"\mathrm{rank}\ 2\ +\ \mathrm{nullity}\ 0\ =\ 2").set_color(DONE),
            Tex(R"\mathrm{rank}\ 1\ +\ \mathrm{nullity}\ 1\ =\ 2").set_color(GREY_C),
            Tex(R"\mathrm{rank}\ 0\ +\ \mathrm{nullity}\ 2\ =\ 2").set_color(GREY_C),
        ]
        table = VGroup(*rows).arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(4.4)
        corner_panel(self, table)
        self.play(FadeIn(table, DOWN))
        self.note("단위행렬 · 상은 평면 전체", DONE)
        self.wait(0.8)

        # 원점으로 눌리는 벡터는 Vector 로 두면 촉을 만들 수 없어 렌더가 멈춘다.
        # 몸통은 변환되는 선, 머리는 움직이는 점으로 따로 둔다.
        k_end = self.plane.c2p(2, -1)
        k_line = Line(self.plane.c2p(0, 0), k_end).set_stroke(WARN, 6)
        k_dot = Dot(k_end, radius=0.1).set_color(WARN)
        k_lab = Tex(R"\mathbf{k}=(2,-1)").set_color(WARN).scale(0.85)
        k_lab.next_to(k_end, DR, buff=0.1)
        k_lab.add_background_rectangle(opacity=0.8, buff=0.05)
        self.add_transformable_mobject(k_line)
        self.add_moving_mobject(k_dot)
        self.add_foreground_mobject(k_lab)
        self.play(ShowCreation(k_line), FadeIn(k_dot), FadeIn(k_lab), run_time=0.6)
        ma = Tex(R"A=\begin{bmatrix}1&2\\2&4\end{bmatrix}").set_color(ACCENT).set_height(1.2)
        ma.next_to(table, DOWN, buff=0.3).align_to(table, RIGHT)
        ma.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(ma)
        self.play(FadeIn(ma, UP))
        self.note("열 둘이 같은 직선 위", ACCENT)
        self.apply_matrix(self.A, run_time=2.4)
        self.wait(0.4)
        self.play(rows[0].animate.set_color(GREY_C), rows[1].animate.set_color(DONE))
        self.note("상은 직선 · 랭크 1", DONE)
        self.wait(0.8)
        gone = Tex(R"L(\mathbf{k})=\mathbf{0}").set_color(WARN).scale(0.85)
        gone.move_to(k_lab).align_to(k_lab, LEFT)
        gone.add_background_rectangle(opacity=0.8, buff=0.05)
        self.add_foreground_mobject(gone)
        self.play(FadeOut(k_lab), FadeIn(gone), run_time=0.4)
        self.foreground_mobjects.remove(k_lab)
        self.note("(2,−1) 방향은 원점으로 · 퇴화차수 1", WARN)
        self.wait(1.2)

        # 길이 0 인 화살표는 촉을 만들 수 없다. 벡터는 먼저 걷고 격자만 누른다.
        self.note("영행렬 · 모두 원점으로", GREY_B)
        walk = VGroup(*self.moving_vectors, *self.transformable_labels, k_dot, gone)
        self.play(FadeOut(walk), run_time=0.4)
        self.moving_vectors.clear()
        self.transformable_labels.clear()
        self.moving_mobjects.remove(k_dot)
        self.foreground_mobjects.remove(gone)
        self.apply_matrix([[0, 0], [0, 0]], path_arc=0, run_time=1.8)
        dot = Dot(self.plane.c2p(0, 0), radius=0.12).set_color(WARN)
        self.play(FadeIn(dot, scale=0.3), run_time=0.4)
        self.play(rows[1].animate.set_color(GREY_C), rows[2].animate.set_color(DONE))
        self.note("상은 점 · 랭크 0 · 퇴화차수 2", DONE)
        self.wait(2)


class RankNullityTheorem(InteractiveScene):
    """정리 4-6 · 예제 4-14 · 4-15. 랭크는 피벗의 개수, 퇴화차수는 열 개수에서 뺀 것.

    예제 4-14 는 행 연산 한 번에 피벗 둘, 예제 4-15 는 교재의 행 연산 다섯 단계를 그대로 밟아
    피벗 셋. 코드 두 줄은 `파이썬실습/py/04_선형변환과 랭크 정리.py` 와 글자 단위로 같다.
    """

    def construct(self):
        head = slide_title("랭크 정리")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        tag = tag_under(head, "정리 4-6 · 예제 4-14 · 4-15")
        self.play(FadeIn(tag))

        law = Tex(R"\mathrm{rank}(A)+\mathrm{nullity}(A)=n").set_color(DONE).scale(1.1)
        law.to_edge(RIGHT, buff=0.6).shift(2.2 * UP)
        self.play(Write(law))
        cap = caption("피벗 수 + 자유변수 수 = 열 수", 24, GREY_B).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap))

        def say(text, color=DONE):
            nonlocal cap
            new = caption(text, 24, color).to_edge(DOWN, buff=0.45)
            self.play(FadeTransform(cap, new), run_time=0.4)
            cap = new

        # 예제 4-14
        ex14 = caption("예제 4-14", 24, ACCENT).to_edge(LEFT, buff=0.6).shift(2.2 * UP)
        m14 = mat([["1", "1", "3", "2"], ["0", "1", "2", "2"]], INK, 0.6, 0.5).set_height(1.3)
        r14 = mat([["1", "0", "1", "0"], ["0", "1", "2", "2"]], INK, 0.6, 0.5).set_height(1.3)
        arrow14 = Tex(R"\sim").set_color(GREY_B)
        row14 = VGroup(m14, arrow14, r14).arrange(RIGHT, buff=0.35)
        row14.next_to(ex14, DOWN, buff=0.3).align_to(ex14, LEFT)
        self.play(FadeIn(ex14), FadeIn(m14))
        say("1행 − 2행", GREY_B)
        self.play(FadeIn(arrow14), TransformFromCopy(m14, r14), run_time=1.0)
        pivots14 = VGroup(box(r14.get_entries()[0], DONE, 0.06), box(r14.get_entries()[5], DONE, 0.06))
        self.play(ShowCreation(pivots14), run_time=0.6)
        ans14 = Tex(R"\mathrm{rank}=2,\ \mathrm{nullity}=4-2=2").set_color(DONE)
        ans14.set_width(4.6).next_to(row14, DOWN, buff=0.25).align_to(row14, LEFT)
        self.play(FadeIn(ans14, UP))
        say("피벗 둘 · 열 넷 · 퇴화차수 2", DONE)
        self.wait(1.2)

        # 예제 4-15 — 교재 풀이의 행 연산 순서 그대로
        self.play(FadeOut(VGroup(ex14, row14, pivots14, ans14)), run_time=0.5)
        ex15 = caption("예제 4-15", 24, ACCENT).move_to(ex14).align_to(ex14, LEFT)
        chain = [
            ([["1", "1", "3", "2"], ["0", "2", "2", "2"], ["1", "1", "2", "5"]], "시작"),
            ([["1", "1", "3", "2"], ["0", "1", "1", "1"], ["1", "1", "2", "5"]], "2행 ÷ 2"),
            ([["1", "1", "3", "2"], ["0", "1", "1", "1"], ["0", "0", "-1", "3"]], "3행 − 1행"),
            ([["1", "1", "3", "2"], ["0", "1", "1", "1"], ["0", "0", "1", "-3"]], "3행 × (−1) · 행 사다리꼴"),
            ([["1", "1", "0", "11"], ["0", "1", "0", "4"], ["0", "0", "1", "-3"]], "3열을 위로 소거"),
            ([["1", "0", "0", "7"], ["0", "1", "0", "4"], ["0", "0", "1", "-3"]], "기약 행 사다리꼴"),
        ]
        current = mat(chain[0][0], INK, 0.6, 0.5).set_height(1.9)
        current.next_to(ex15, DOWN, buff=0.3).align_to(ex15, LEFT)
        self.play(FadeIn(ex15), FadeIn(current))
        for values, what in chain[1:]:
            say(what, GREY_B)
            new = mat(values, INK, 0.6, 0.5).set_height(1.9).move_to(current).align_to(current, LEFT)
            self.play(FadeTransform(current, new), run_time=0.7)
            current = new
            self.wait(0.3)
        entries = current.get_entries()
        pivots = VGroup(*[box(entries[k], DONE, 0.06) for k in (0, 5, 10)])
        self.play(ShowCreation(pivots), run_time=0.6)
        ans15 = Tex(R"\mathrm{rank}=3,\ \mathrm{nullity}=4-3=1").set_color(DONE)
        ans15.set_width(4.6).next_to(current, DOWN, buff=0.3).align_to(current, LEFT)
        self.play(FadeIn(ans15, UP))
        say("피벗 셋 · 열 넷 · 퇴화차수 1", DONE)
        self.wait(0.8)

        lines = code_block([
            "rank_Mat = np.linalg.matrix_rank(Matrix_1)",
            "Nullity_Mat = len(Matrix_1[0,:]) - rank_Mat",
        ], 20)
        lines.set_width(5.6).to_edge(RIGHT, buff=0.5).shift(0.4 * DOWN)
        self.play(LaggedStartMap(FadeIn, lines, lag_ratio=0.3))
        note = VGroup(caption("len(Matrix_1[0,:]) = 열 개수 n", 22, CALM),
                      caption("Rank(A) = 3 · Nullity(A) = 1", 22, DONE))
        note.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(lines, DOWN, buff=0.35).align_to(lines, LEFT)
        self.play(FadeIn(note, UP))
        say("코드는 피벗 세기를 한 줄로", DONE)
        self.wait(2)
