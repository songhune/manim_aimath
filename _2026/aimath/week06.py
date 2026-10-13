"""AI기초수학 — 교재 Chapter 5 고윳값과 케일리-해밀턴 정리.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 05_고윳값과 케일리-해밀턴 정리_강의용.pptx` 의
5.1 고윳값과 고유벡터 · 5.2 케일리-해밀턴 정리에 붙는 보조 영상 8편.
파일 이름은 앞 장과 같은 규칙이다(week05 = CH04, week06 = CH05).

수식보다 격자가 움직이는 그림으로 세운다(2026-10-13 요청).
- 고유벡터는 변환 뒤에도 자기 직선 위에 남는 벡터, 고윳값은 그 직선 위에서 늘어난 배수다.
- 특성방정식 det(λI − A) = 0 은 λI − A 가 평면을 직선으로 누르는 λ 를 찾는 식이다.
- 고유공간은 그 고윳값의 고유벡터 전부(와 영벡터)가 이루는 직선 · 평면이다.
- Aᵏ 는 고유벡터를 λᵏ 배, A⁻¹ 은 1/λ 배로 보낸다. det 은 고유벡터로 만든 사각형의 넓이 배율이다.
- 케일리-해밀턴 정리 p(A) = O 는 p(A) 가 두 고유벡터를 모두 영벡터로 보내므로 평면 전체를 원점으로 누른다는 뜻이다.
수는 예제 5-1 · 5-2 · 5-9 의 값을 쓰고, 두 고유벡터가 정수로 떨어지는 [[2,1],[1,2]] (고윳값 3, 1) 을 보조로 쓴다.
유니타리 행렬(정의 5-4) · 슈어 분해(정리 5-4)는 평가 범위가 아니라 그리지 않았다.
직교행렬(정의 5-3)은 CH04 의 `OrthogonalOperator` 가 같은 조건 AᵀA = I 를 보인다.

격자·기저벡터·단위정사각형은 `GridScene`(week05.py) 에서 물려받는다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week06.py
    ./render.sh check _2026/aimath/week06.py
    ./render.sh ppt   _2026/aimath/week06.py EigenvectorIntro
"""
from manim_imports_ext import *

from _2026.aimath.week04 import (
    INK, ACCENT, CALM, WARN, DONE, title, caption, code, slide_title, tag_under, box,
)
from _2026.aimath.week03 import overlay, code_block, mat
from _2026.aimath.week05 import GridScene, head_on_grid, corner_panel


# 예제 5-2 의 행렬. 고유벡터 (1,1) 은 5배, (1,−1) 은 −1배.
A_EX52 = [[2, 3], [3, 2]]
# 보조 행렬. 고윳값 3 · 1, 고유벡터 (1,1) · (1,−1). 두 번 적용해도 화면 안에 남는다.
A_31 = [[2, 1], [1, 2]]


def eigen_lines(scene, color1=DONE, color2=CALM, reach=4.2):
    """고유벡터가 놓인 두 직선 y = x, y = −x. 변환해도 같은 자리로 간다."""
    p = scene.plane
    l1 = Line(p.c2p(-reach, -reach), p.c2p(reach, reach)).set_stroke(color1, 2, opacity=0.55)
    l2 = Line(p.c2p(-reach, reach), p.c2p(reach, -reach)).set_stroke(color2, 2, opacity=0.55)
    scene.add_transformable_mobject(l1, l2)
    scene.play(ShowCreation(l1), ShowCreation(l2), run_time=0.6)
    return l1, l2


def side_panel(scene, rows, width=4.6, buff=0.6, corner=UR, shift=ORIGIN):
    """구석에 세로로 쌓는 수식 패널. 기본은 오른쪽 위, 벡터가 그쪽으로 가는 씬은 오른쪽 아래에 둔다."""
    panel = VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT).set_width(width)
    panel.to_corner(corner, buff=buff).shift(shift)
    panel.add_background_rectangle(opacity=0.85, buff=0.12)
    scene.add_foreground_mobject(panel)
    scene.play(FadeIn(panel, DOWN), run_time=0.6)
    return panel


# ─────────────────────────────────────────────────────────────
# 5.1 고윳값과 고유벡터
# ─────────────────────────────────────────────────────────────
class EigenvectorIntro(GridScene):
    """정의 5-1 · 예제 5-2. A = [[2,3],[3,2]] 를 평면에 적용하면 대부분의 벡터는 방향이 바뀐다.

    (1,1) 은 5배로 늘어나며 자기 직선에 남고, (1,−1) 은 뒤집혀 자기 직선에 남는다.
    그 둘이 고유벡터, 5 와 −1 이 고윳값이다. 정의 5-1 의 Ax = λx 는 이 그림을 식으로 적은 것이다.
    참고: legacy/_2016/eola/chapter10.py (3b1b, eigenvectors and eigenvalues)
    """
    A = A_EX52

    def construct(self):
        head_on_grid(self, "고유벡터란", "정의 5-1 · 예제 5-2")
        panel = Tex(R"A=\begin{bmatrix}2&3\\3&2\end{bmatrix}").set_color(ACCENT).set_height(1.2)
        corner_panel(self, panel)
        self.play(FadeIn(panel, DOWN))

        eigen_lines(self)
        w = self.vec((1, 0.2), ACCENT, R"\mathbf{w}", R"A\mathbf{w}")
        x = self.vec((0.5, 0.5), DONE, R"\mathbf{x}", R"A\mathbf{x}")
        y = self.vec((1, -1), CALM, R"\mathbf{y}", R"A\mathbf{y}", direction="left")
        self.note("벡터 셋에 A 를 적용", GREY_B)
        self.wait(0.5)

        self.apply_matrix(self.A, run_time=2.4)
        self.wait(0.4)
        self.note("w 는 방향이 바뀜", ACCENT)
        self.wait(0.8)
        self.note("x 는 같은 직선 · 5배", DONE)
        self.wait(0.8)
        self.note("y 는 같은 직선 · −1배", CALM)
        self.wait(0.8)

        eq1 = Tex(R"A\mathbf{x}=5\mathbf{x}").set_color(DONE)
        eq2 = Tex(R"A\mathbf{y}=-\mathbf{y}").set_color(CALM)
        eqs = VGroup(eq1, eq2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(2.6)
        eqs.next_to(panel, DOWN, buff=0.3).align_to(panel, RIGHT)
        eqs.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(eqs)
        self.play(FadeIn(eqs, UP))
        self.note("고유벡터 x, y · 고윳값 5, −1", DONE)
        self.wait(2)


class CharacteristicEquation(GridScene):
    """정의 5-2 · 예제 5-2. (λI − A)x = 0 에 영벡터가 아닌 해가 있으려면 λI − A 가 평면을 눌러야 한다.

    λ = 1 이면 λI − A 는 평면을 평면으로 보내 원점으로 가는 벡터가 없다(det = −8).
    λ = 5 이면 평면이 직선으로 눌리고 (1,1) 방향이 원점으로 간다(det = 0). 그 λ 가 고윳값이다.
    참고: legacy/_2016/eola/chapter10.py (det(A − λI) = 0 을 격자 누르기로 보이는 장면)
    """
    A = A_EX52

    def construct(self):
        head_on_grid(self, "특성방정식", "정의 5-2 · 예제 5-2")
        eq = Tex(R"(\lambda I-A)\mathbf{x}=\mathbf{0},\quad \mathbf{x}\neq\mathbf{0}").set_color(INK)
        panel = side_panel(self, [eq], width=4.4)
        self.note("영벡터 아닌 해가 있는 λ", GREY_B)
        self.wait(0.6)

        # 원점으로 눌리는 벡터는 Vector 로 두면 촉을 만들 수 없다. 몸통은 선, 머리는 점으로 둔다.
        k_end = self.plane.c2p(1, 1)
        k_line = Line(self.plane.c2p(0, 0), k_end).set_stroke(DONE, 6)
        k_dot = Dot(k_end, radius=0.1).set_color(DONE)
        k_lab = Tex(R"\mathbf{x}=(1,1)").set_color(DONE).scale(0.85)
        k_lab.next_to(k_end, UR, buff=0.1)
        k_lab.add_background_rectangle(opacity=0.8, buff=0.05)
        self.add_transformable_mobject(k_line)
        self.add_moving_mobject(k_dot)
        self.add_foreground_mobject(k_lab)
        self.play(ShowCreation(k_line), FadeIn(k_dot), FadeIn(k_lab), run_time=0.6)

        # λ = 1: 평면은 평면. 원점으로 가는 벡터가 없다.
        m1 = Tex(R"\lambda=1:\ I-A=\begin{bmatrix}-1&-3\\-3&-1\end{bmatrix}").set_color(INK).set_width(4.4)
        m1.next_to(panel, DOWN, buff=0.3).align_to(panel, RIGHT)
        m1.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(m1)
        self.play(FadeIn(m1, UP))
        self.note("λ = 1 · 평면은 평면 · det = −8", INK)
        self.apply_matrix([[-1, -3], [-3, -1]], path_arc=0, run_time=2.0)
        self.wait(0.6)
        self.note("원점으로 가는 벡터 없음 · 고윳값 아님", WARN)
        self.wait(0.8)
        self.apply_inverse([[-1, -3], [-3, -1]], path_arc=0, run_time=1.2)

        # λ = 5: 평면이 직선으로. (1,1) 이 원점으로 간다.
        m5 = Tex(R"\lambda=5:\ 5I-A=\begin{bmatrix}3&-3\\-3&3\end{bmatrix}").set_color(DONE).set_width(4.4)
        m5.move_to(m1).align_to(m1, RIGHT)
        m5.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(m5)
        self.play(FadeOut(m1), FadeIn(m5), run_time=0.5)
        self.foreground_mobjects.remove(m1)
        self.note("λ = 5 · 평면이 직선으로 · det = 0", DONE)
        self.apply_matrix([[3, -3], [-3, 3]], path_arc=0, run_time=2.2)
        gone = Tex(R"(5I-A)\mathbf{x}=\mathbf{0}").set_color(DONE).scale(0.85)
        gone.next_to(self.plane.c2p(0, 0), UR, buff=0.15)
        gone.add_background_rectangle(opacity=0.8, buff=0.05)
        self.add_foreground_mobject(gone)
        self.play(FadeOut(k_lab), FadeIn(gone), run_time=0.4)
        self.foreground_mobjects.remove(k_lab)
        self.note("(1,1) 이 원점으로 · 고윳값 5", DONE)
        self.wait(1.0)

        det = Tex(R"\det(\lambda I-A)=\lambda^{2}-4\lambda-5=(\lambda-5)(\lambda+1)").set_color(DONE)
        det.set_width(6.2).to_corner(DL, buff=0.5).shift(UP * 0.9)
        det.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(det)
        self.play(FadeIn(det, UP))
        self.note("det(λI − A) = 0 · 특성방정식", DONE)
        self.wait(2)


class TriangularEigen(InteractiveScene):
    """예제 5-1 · 정리 5-1. 삼각행렬의 고윳값은 대각 성분이다.

    λI − A 도 삼각행렬이라 행렬식이 대각 성분의 곱 (λ−1)(λ−4)(λ−6) 이다. 근이 셋이므로 고윳값도
    최대 셋(정리 5-1). 코드 두 줄은 `파이썬실습/py/05_고윳값과 케일리-해밀턴 정리.py` 와 글자 단위로 같다.
    """

    def construct(self):
        head = slide_title("삼각행렬의 고윳값")
        self.add(head)
        tag = tag_under(head, "예제 5-1 · 정리 5-1")
        self.play(FadeIn(tag))

        A = mat([["1", "2", "3"], ["0", "4", "5"], ["0", "0", "6"]], INK).set_height(2.0)
        A_lab = Tex("A=").set_color(INK).next_to(A, LEFT, buff=0.2)
        left = VGroup(A_lab, A).move_to(LEFT * 3.6 + UP * 0.7)
        self.play(FadeIn(left))
        self.wait(0.4)

        diag = VGroup(*[A.get_entries()[i] for i in (0, 4, 8)])
        marks = VGroup(*[box(e, DONE, 0.08) for e in diag])
        self.play(ShowCreation(marks), run_time=0.8)
        self.play(diag.animate.set_color(DONE), run_time=0.4)
        note1 = caption("대각 성분 1, 4, 6", 26, DONE).next_to(left, DOWN, buff=0.45)
        self.play(FadeIn(note1, UP))
        self.wait(0.6)

        lam = Tex(R"\lambda I-A=\begin{bmatrix}\lambda-1&-2&-3\\0&\lambda-4&-5\\0&0&\lambda-6\end{bmatrix}")
        lam.set_color(INK).set_width(5.6).move_to(RIGHT * 3.2 + UP * 1.0)
        self.play(FadeIn(lam, LEFT))
        self.wait(0.4)
        det = Tex(R"\det(\lambda I-A)=(\lambda-1)(\lambda-4)(\lambda-6)").set_color(DONE)
        det.set_width(5.6).next_to(lam, DOWN, buff=0.35)
        self.play(Write(det), run_time=1.2)
        note2 = caption("삼각행렬 · 행렬식은 대각 성분의 곱", 24, GREY_B).next_to(det, DOWN, buff=0.25)
        self.play(FadeIn(note2, UP))
        self.wait(0.8)
        note3 = caption("고윳값 1, 4, 6 · 최대 3개", 26, DONE).next_to(note2, DOWN, buff=0.3)
        self.play(FadeIn(note3, UP))
        self.wait(0.8)

        lines = code_block([
            "A = np.array([[1,2,3],[0,4,5],[0,0,6]])",
            'print("A의 고윳값 : ", np.linalg.eig(A)[0])',
        ], size=22)
        out = code("A의 고윳값 :  [1. 4. 6.]", 22, DONE)
        block = VGroup(lines, out).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        block.to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
        self.play(FadeIn(lines, UP))
        self.wait(0.5)
        self.play(FadeIn(out, UP))
        self.wait(2)


class Eigenspace(GridScene):
    """정의 5-1 보충 · 예제 5-3. 고유공간은 그 고윳값의 고유벡터 전부(와 영벡터)다.

    2I 는 모든 벡터를 2배로 보내 모든 벡터가 고유벡터다 — 고유공간이 평면 전체.
    층밀림 [[1,1],[0,1]] 은 x 축 위의 벡터만 제자리에 두고 나머지는 기울인다 — 고유공간이 직선 하나.
    예제 5-3 의 3차원 행렬은 같은 것을 공간에서 한다(평면 하나, 직선 하나).
    """

    def construct(self):
        head_on_grid(self, "고유공간", "정의 5-1 · 예제 5-3")
        a = self.vec((0.8, 1.2), ACCENT, R"\mathbf{a}", R"\mathbf{a}'")
        b = self.vec((-1, 1), CALM, R"\mathbf{b}", R"\mathbf{b}'", direction="left")
        c = self.vec((1.5, 0), DONE, R"\mathbf{c}", R"\mathbf{c}'")

        m2 = Tex(R"2I=\begin{bmatrix}2&0\\0&2\end{bmatrix}").set_color(ACCENT).set_height(1.2)
        corner_panel(self, m2)
        self.play(FadeIn(m2, DOWN))
        self.note("2I · 모든 벡터가 2배", ACCENT)
        self.apply_matrix([[2, 0], [0, 2]], path_arc=0, run_time=2.0)
        self.wait(0.4)
        self.note("모든 벡터가 고유벡터 · λ = 2", DONE)
        e2 = Tex(R"E_2=\mathbb{R}^{2}").set_color(DONE).set_height(0.7)
        e2.next_to(m2, DOWN, buff=0.3).align_to(m2, RIGHT)
        e2.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(e2)
        self.play(FadeIn(e2, UP))
        self.note("고유공간은 평면 전체", DONE)
        self.wait(1.2)
        self.apply_inverse([[2, 0], [0, 2]], path_arc=0, run_time=1.0)

        ms = Tex(R"S=\begin{bmatrix}1&1\\0&1\end{bmatrix}").set_color(ACCENT).set_height(1.2)
        ms.move_to(m2).align_to(m2, RIGHT)
        ms.add_background_rectangle(opacity=0.85, buff=0.12)
        self.add_foreground_mobject(ms)
        self.play(FadeOut(m2), FadeOut(e2), FadeIn(ms), run_time=0.5)
        self.foreground_mobjects.remove(m2)
        self.foreground_mobjects.remove(e2)
        self.note("층밀림 · x 축 위 벡터만 제자리", ACCENT)
        self.apply_matrix([[1, 1], [0, 1]], path_arc=0, run_time=2.0)
        self.wait(0.4)
        self.note("c 만 고유벡터 · λ = 1", DONE)
        e1 = Tex(R"E_1=\operatorname{span}\{(1,0)\}").set_color(DONE).set_width(3.2)
        e1.next_to(ms, DOWN, buff=0.3).align_to(ms, RIGHT)
        e1.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(e1)
        self.play(FadeIn(e1, UP))
        self.note("고유공간은 x 축 하나", DONE)
        self.wait(1.2)
        self.note("고유공간 = 고유벡터 전부 + 영벡터", GREY_B)
        self.wait(2)


class EigenPowers(GridScene):
    """정리 5-2 · 예제 5-4. Aᵏ 는 고유벡터를 λᵏ 배, A⁻¹ 은 1/λ 배, kA 는 kλ 배로 보낸다.

    A = [[2,1],[1,2]] 의 고유벡터 (1,1) 은 3배. 두 번 적용하면 9배, 되돌리면 1/3 배씩.
    2A 를 적용하면 6배. 고유벡터 (1,−1) 은 고윳값 1 이라 줄곧 제자리다.
    """
    A = A_31

    def construct(self):
        head_on_grid(self, "고윳값의 성질", "정리 5-2 · 예제 5-4")
        rows = [
            Tex(R"A=\begin{bmatrix}2&1\\1&2\end{bmatrix},\ \lambda=3,\,1").set_color(ACCENT),
            Tex(R"A^{k}:\ \lambda^{k}").set_color(GREY_C),
            Tex(R"A^{-1}:\ 1/\lambda").set_color(GREY_C),
            Tex(R"kA:\ k\lambda").set_color(GREY_C),
        ]
        # 벡터가 오른쪽 위로 자라므로 패널은 오른쪽 아래에 둔다.
        panel = side_panel(self, rows, width=3.6, corner=DR, shift=UP * 1.1)
        eigen_lines(self)
        x = self.vec((0.4, 0.4), DONE, R"\mathbf{x}", R"\mathbf{x}")
        y = self.vec((1, -1), CALM, R"\mathbf{y}", R"\mathbf{y}", direction="left")
        self.wait(0.4)

        self.note("A · x 는 3배, y 는 1배", DONE)
        self.apply_matrix(self.A, path_arc=0, run_time=1.8)
        self.wait(0.6)
        self.play(rows[1].animate.set_color(DONE), run_time=0.4)
        self.note("A 한 번 더 · 3 × 3 = 9배", DONE)
        self.apply_matrix(self.A, path_arc=0, run_time=1.8)
        self.wait(0.8)

        self.play(rows[1].animate.set_color(GREY_C), rows[2].animate.set_color(DONE), run_time=0.4)
        self.note("A⁻¹ 두 번 · 1/3 배씩 되돌아감", CALM)
        self.apply_inverse(self.A, path_arc=0, run_time=1.2)
        self.apply_inverse(self.A, path_arc=0, run_time=1.2)
        self.wait(0.6)

        self.play(rows[2].animate.set_color(GREY_C), rows[3].animate.set_color(DONE), run_time=0.4)
        self.note("2A · 2 × 3 = 6배", DONE)
        self.apply_matrix([[4, 2], [2, 4]], path_arc=0, run_time=1.8)
        self.wait(0.6)
        self.note("고유벡터는 그대로 · 배수만 바뀜", GREY_B)
        self.wait(2)


class DetTraceFromEigen(GridScene):
    """정리 5-3. det A 는 고윳값의 곱, tr A 는 고윳값의 합.

    고유벡터 (1,1) · (1,−1) 을 변으로 하는 정사각형은 A 를 거치며 한 변은 3배, 다른 변은 1배가 된다.
    넓이는 3 × 1 = 3 배 — 행렬식(CH02 보충 '행렬식이 재는 것')과 같은 수다. 단위정사각형도 3배.
    대각합 2 + 2 = 4 는 3 + 1 이다.
    """
    A = A_31

    def construct(self):
        head_on_grid(self, "행렬식과 대각합", "정리 5-3")
        # 사각형이 오른쪽 위로 커지므로 행렬은 오른쪽 아래, 결과는 왼쪽 아래에 둔다.
        panel = side_panel(self, [Tex(R"A=\begin{bmatrix}2&1\\1&2\end{bmatrix},\ \lambda=3,\,1").set_color(ACCENT)],
                           width=3.6, corner=DR, shift=UP * 1.1)

        p = self.plane
        self.add_unit_square()
        self.play(FadeIn(self.square))
        quad = Polygon(p.c2p(0, 0), p.c2p(1, 1), p.c2p(2, 0), p.c2p(1, -1))
        quad.set_fill(CALM, opacity=0.35).set_stroke(CALM, 3)
        self.add_transformable_mobject(quad)
        self.play(FadeIn(quad), run_time=0.6)
        self.note("고유벡터를 변으로 한 정사각형 · 넓이 2", CALM)
        self.wait(0.8)

        self.apply_matrix(self.A, path_arc=0, run_time=2.2)
        self.wait(0.4)
        self.note("한 변은 3배 · 다른 변은 1배", DONE)
        self.wait(0.8)
        self.note("넓이 2 → 6 · 3 × 1 = 3배", DONE)
        self.wait(0.8)
        self.note("단위정사각형 넓이 1 → 3 · det A", DONE)
        self.wait(0.8)

        rows = VGroup(
            Tex(R"\det A=2\cdot2-1\cdot1=3=\lambda_1\lambda_2").set_color(DONE),
            Tex(R"\operatorname{tr}A=2+2=4=\lambda_1+\lambda_2").set_color(DONE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(5.2)
        rows.to_corner(DL, buff=0.5).shift(UP * 1.1)
        rows.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(rows)
        self.play(FadeIn(rows, UP))
        self.note("행렬식은 곱 · 대각합은 합", DONE)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5.2 케일리-해밀턴 정리
# ─────────────────────────────────────────────────────────────
class CayleyHamiltonCollapse(GridScene):
    """정리 5-5. 특성다항식에 A 를 넣으면 영행렬이 되는 이유.

    A = [[2,1],[1,2]], p(λ) = λ² − 4λ + 3. 고유벡터 x (λ = 3) 에 p(A) 를 적용하면
    A²x − 4Ax + 3x = 9x − 12x + 3x = 0 — 세 화살표를 이어 붙이면 원점으로 돌아온다.
    y (λ = 1) 도 y − 4y + 3y = 0. 평면의 모든 벡터가 두 고유벡터의 합이므로 p(A) 는 전부 원점으로 보낸다.
    마지막에 영행렬을 적용해 격자가 점으로 눌리는 것을 보인다.
    """
    A = A_31

    def chain(self, start, steps, color, labels):
        """start 에서 steps 의 벡터를 머리에 꼬리를 이어 그린다. 끝점을 돌려준다."""
        p = self.plane
        here = np.array(start, dtype=float)
        arrows = VGroup()
        for (dx, dy), lab in zip(steps, labels):
            nxt = here + np.array([dx, dy])
            a = Arrow(p.c2p(*here), p.c2p(*nxt), buff=0, thickness=4).set_color(color)
            t = Tex(lab).set_color(color).scale(0.75)
            t.next_to(a.get_center(), UR if dx >= 0 else DL, buff=0.08)
            t.add_background_rectangle(opacity=0.8, buff=0.04)
            self.add_foreground_mobject(a, t)
            self.play(GrowArrow(a), FadeIn(t), run_time=0.7)
            arrows.add(a, t)
            here = nxt
        return arrows, here

    def construct(self):
        head_on_grid(self, "케일리-해밀턴 정리", "정리 5-5")
        rows = [
            Tex(R"A=\begin{bmatrix}2&1\\1&2\end{bmatrix}").set_color(ACCENT),
            Tex(R"p(\lambda)=\lambda^{2}-4\lambda+3=(\lambda-3)(\lambda-1)").set_color(INK),
            Tex(R"p(3)=0,\quad p(1)=0").set_color(DONE),
        ]
        side_panel(self, rows, width=5.0)
        eigen_lines(self)
        self.wait(0.4)

        # x = (0.3, 0.3), λ = 3. 9x, −12x, 3x 를 이어 붙인다.
        x = self.vec((0.3, 0.3), DONE, R"\mathbf{x}")
        self.note("x 에 p(A) 를 적용", DONE)
        arrows_x, end = self.chain((0, 0), [(2.7, 2.7), (-3.6, -3.6), (0.9, 0.9)], DONE,
                                   [R"A^{2}\mathbf{x}=9\mathbf{x}", R"-4A\mathbf{x}=-12\mathbf{x}", R"3\mathbf{x}"])
        self.note("9 − 12 + 3 = 0 · 원점으로", DONE)
        self.wait(1.0)
        self.play(FadeOut(arrows_x), run_time=0.4)
        for m in arrows_x:
            if m in self.foreground_mobjects:
                self.foreground_mobjects.remove(m)

        # y = (1, −1), λ = 1. y, −4y, 3y.
        y = self.vec((1, -1), CALM, R"\mathbf{y}", direction="left")
        self.note("y 에 p(A) 를 적용", CALM)
        arrows_y, end = self.chain((0, 0), [(1, -1), (-4, 4), (3, -3)], CALM,
                                   [R"A^{2}\mathbf{y}=\mathbf{y}", R"-4A\mathbf{y}=-4\mathbf{y}", R"3\mathbf{y}"])
        self.note("1 − 4 + 3 = 0 · 원점으로", CALM)
        self.wait(1.0)
        self.play(FadeOut(arrows_y), run_time=0.4)
        for m in arrows_y:
            if m in self.foreground_mobjects:
                self.foreground_mobjects.remove(m)

        self.note("모든 벡터 = 고유벡터의 합", GREY_B)
        self.wait(0.8)
        self.note("p(A) 는 평면 전체를 원점으로", WARN)
        walk = VGroup(*self.moving_vectors, *self.transformable_labels)
        self.play(FadeOut(walk), run_time=0.4)
        self.moving_vectors.clear()
        self.transformable_labels.clear()
        self.apply_matrix([[0, 0], [0, 0]], path_arc=0, run_time=1.8)
        dot = Dot(self.plane.c2p(0, 0), radius=0.12).set_color(WARN)
        self.play(FadeIn(dot, scale=0.3), run_time=0.4)
        result = Tex(R"p(A)=A^{2}-4A+3I=O").set_color(DONE).set_width(4.6)
        result.to_corner(DL, buff=0.5).shift(UP * 0.9)
        result.add_background_rectangle(opacity=0.85, buff=0.1)
        self.add_foreground_mobject(result)
        self.play(FadeIn(result, UP))
        self.wait(2)


class CayleyHamiltonUse(InteractiveScene):
    """예제 5-9. 케일리-해밀턴 정리로 높은 거듭제곱과 역행렬을 낮은 차수로 줄인다.

    A = [[1,3],[2,1]], p(λ) = λ² − 2λ − 5. A² = 2A + 5I 로 A² 를 볼 때마다 바꿔 쓰면
    A⁴ = 28A + 45I 이고 A⁴ − 14A² + 26I = I. 역행렬은 A(A − 2I) = 5I 에서 (A − 2I)/5.
    """

    def construct(self):
        head = slide_title("케일리-해밀턴 정리의 쓰임")
        self.add(head)
        tag = tag_under(head, "예제 5-9")
        self.play(FadeIn(tag))

        A = Tex(R"A=\begin{bmatrix}1&3\\2&1\end{bmatrix}").set_color(ACCENT).set_height(1.1)
        A.to_corner(UR, buff=0.6).shift(DOWN * 1.0)
        self.play(FadeIn(A, DOWN))

        steps = [
            (R"p(\lambda)=\lambda^{2}-2\lambda-5\ \Rightarrow\ A^{2}-2A-5I=O", INK),
            (R"A^{2}=2A+5I", DONE),
            (R"A^{4}=(A^{2})^{2}=(2A+5I)^{2}=4A^{2}+20A+25I", INK),
            (R"\phantom{A^{4}}=4(2A+5I)+20A+25I=28A+45I", INK),
            (R"A^{4}-14A^{2}+26I=(28A+45I)-14(2A+5I)+26I=I", DONE),
        ]
        rows = VGroup(*[Tex(t).set_color(c) for t, c in steps])
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).set_width(8.6)
        rows.next_to(tag, DOWN, buff=0.5).align_to(tag, LEFT)
        notes = [
            "특성방정식에 A 를 넣음",
            "A² 를 A 와 I 의 식으로",
            "거듭제곱을 A 와 I 의 식으로",
            "A² 가 보이면 다시 바꿔 씀",
            "답은 단위행렬",
        ]
        shown = None
        for row, text in zip(rows, notes):
            color = DONE if row.get_color() == Color(DONE) else GREY_B
            new = caption(text, 24, color).to_edge(DOWN, buff=0.5)
            self.play(Write(row), run_time=1.0)
            if shown is None:
                self.play(FadeIn(new, UP), run_time=0.4)
            else:
                self.play(FadeOut(shown), FadeIn(new, UP), run_time=0.4)
            shown = new
            self.wait(0.8)

        inv = VGroup(
            Tex(R"A(A-2I)=5I").set_color(INK),
            Tex(R"A^{-1}=\tfrac15(A-2I)=\tfrac15\begin{bmatrix}-1&3\\2&-1\end{bmatrix}").set_color(DONE),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).set_width(5.2)
        inv.next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        new = caption("역행렬도 같은 식에서", 24, DONE).to_edge(DOWN, buff=0.5)
        self.play(Write(inv), run_time=1.2)
        self.play(FadeOut(shown), FadeIn(new, UP), run_time=0.4)
        self.wait(2)
