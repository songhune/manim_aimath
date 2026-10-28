"""AI기초수학 — 교재 Chapter 6 행렬 분해.

강의자료 `AI기초수학/강의자료_restyled/CHAPTER 06_행렬 분해_강의용.pptx` 의
6.1 LU 분해 · 6.2 특잇값 분해에 붙는 보조 영상 9편.
파일 이름은 앞 장과 같은 규칙이다(week06 = CH05, week07 = CH06).

수식보다 격자가 움직이는 그림으로 세운다(2026-10-13 요청과 같은 기준).
- LU 분해는 변환 두 개의 합성이다. U(상삼각) 를 먼저, L(단위 하삼각) 을 다음에 적용하면 A 를 한 번에 적용한 것과 같다.
- 기본행렬 세 유형은 평면의 반사 · 축 방향 늘림 · 층밀림이다. 역행렬도 같은 유형의 기본행렬이다.
- 행 연산의 배수가 그대로 L 의 성분이 된다(예제 6-1). 피벗 자리에 0 이 나오면 행 교환 P 가 앞에 붙는다(예제 6-3).
- 특잇값은 단위원이 가는 타원의 반축 길이다. AᵀA 의 고유벡터 v1, v2 가 가는 Av1, Av2 가 서로 수직이고 길이가 σ1, σ2 다(정리 6-3).
- A = UΣVᵀ 는 회전(Vᵀ) → 축 방향 늘림(Σ) → 회전(U) 세 단계다(정의 6-4).
- 특잇값을 큰 것부터 k 개만 더한 A_k 가 저랭크 근사다. 이미지 행렬로 보인다(응용).
수는 예제 6-1 · 6-3 · 6-6 의 값을 쓰고, 2차원 그림에는 특잇값이 정수(3, 2)로 떨어지는 [[2,2],[-1,2]] 를 쓴다.
예제 6-2(유일하지 않음) · 6-4 · 6-5 는 계산이라 풀이 슬라이드로 둔다.

격자·기저벡터·단위정사각형은 `GridScene`(week05.py) 에서 물려받는다.
참고: legacy/_2016/eola/chapter3.py (변환의 합성 · 열 읽기), chapter10.py (고유벡터). 특잇값 분해는 원본 시리즈에 없어 새로 만들었다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/aimath/week07.py
    ./render.sh check _2026/aimath/week07.py
    ./render.sh ppt   _2026/aimath/week07.py LUAsComposition
"""
from manim_imports_ext import *

from _2026.aimath.week04 import (
    INK, ACCENT, CALM, WARN, DONE, title, caption, code, slide_title, tag_under, box,
)
from _2026.aimath.week03 import overlay, code_block, mat, augmented
from _2026.aimath.week05 import GridScene, head_on_grid, corner_panel, X_COLOR, Y_COLOR
from _2026.aimath.week06 import side_panel


# 2차원 그림에 쓰는 행렬들. 값은 week06_자료/_build_ch06_강의용_deck.py 의 verify() 가 검산한다.
L_2D = [[1, 0], [1, 1]]            # 단위 하삼각 — 2행에 1행을 더함
U_2D = [[1, 1], [0, 1]]            # 상삼각
A_2D = [[1, 1], [1, 2]]            # = L_2D @ U_2D
A_SVD = [[2, 2], [-1, 2]]          # 특잇값 3, 2
S5 = np.sqrt(5)
V_SVD = [[1 / S5, -2 / S5], [2 / S5, 1 / S5]]     # AᵀA 의 단위 고유벡터를 열로 (회전 63.4°)
U_SVD = [[2 / S5, -1 / S5], [1 / S5, 2 / S5]]     # Av_i / σ_i (회전 26.6°)
SIGMA_SVD = [[3, 0], [0, 2]]
VT_SVD = np.array(V_SVD).T.tolist()


def unit_circle(scene, color=GREY_B):
    """변환을 따라 움직이는 단위원."""
    c = Circle(radius=1.0).set_stroke(color, 3).move_to(scene.plane.c2p(0, 0))
    scene.add_transformable_mobject(c)
    scene.play(ShowCreation(c), run_time=0.6)
    return c


def bottom_panel(scene, rows, width=6.0, buff=0.5, shift=UP * 0.9):
    """왼쪽 아래 수식 패널. 자막(note) 바로 위에 놓는다."""
    panel = VGroup(*rows).arrange(DOWN, buff=0.2, aligned_edge=LEFT).set_width(width)
    panel.to_corner(DL, buff=buff).shift(shift)
    panel.add_background_rectangle(opacity=0.85, buff=0.12)
    scene.add_foreground_mobject(panel)
    scene.play(FadeIn(panel, UP), run_time=0.6)
    return panel


def strings(values):
    return [[str(v) for v in row] for row in values]


def footnote(scene, text, color=GREY_B, shown=None):
    """InteractiveScene 용 아래 자막. 앞 자막을 지우고 새 자막을 놓는다."""
    new = caption(text, 24, color).to_edge(DOWN, buff=0.5)
    if shown is None:
        scene.play(FadeIn(new, UP), run_time=0.4)
    else:
        scene.play(FadeOut(shown), FadeIn(new, UP), run_time=0.4)
    return new


# ─────────────────────────────────────────────────────────────
# 6.1 LU 분해
# ─────────────────────────────────────────────────────────────
class LUAsComposition(GridScene):
    """정의 6-1. A = LU 는 변환 두 개의 합성이다.

    A = [[1,1],[1,2]] 를 U = [[1,1],[0,1]] 다음 L = [[1,0],[1,1]] 로 나누어 적용하면 격자가
    A 를 한 번에 적용한 자리로 간다. 분해는 행렬을 '먼저 하는 일'과 '다음에 하는 일'로 가르는 것이다.
    참고: legacy/_2016/eola/chapter3.py (변환의 합성)
    """

    def construct(self):
        head_on_grid(self, "LU 분해", "정의 6-1")
        eq = Tex(R"A=\begin{bmatrix}1&1\\1&2\end{bmatrix}"
                 R"=\begin{bmatrix}1&0\\1&1\end{bmatrix}\begin{bmatrix}1&1\\0&1\end{bmatrix}=LU")
        eq.set_color(INK)
        panel = side_panel(self, [eq], width=5.6)
        self.add_unit_square()
        self.play(FadeIn(self.square), run_time=0.5)
        self.note("단위정사각형에 두 행렬을 차례로", GREY_B)
        self.wait(0.6)

        self.note("U 먼저 · 상삼각행렬", ACCENT)
        self.apply_matrix(U_2D, path_arc=0, run_time=2.0)
        self.wait(0.5)
        self.note("L 다음 · 단위 하삼각행렬", CALM)
        self.apply_matrix(L_2D, path_arc=0, run_time=2.0)
        self.wait(0.5)
        self.note("e1 → (1,1) · e2 → (1,2)", DONE)
        self.wait(1.0)

        # 되돌린 뒤 A 를 한 번에 적용해도 같은 자리다.
        self.note("되돌린 뒤 A 를 한 번에", GREY_B)
        self.apply_inverse(A_2D, path_arc=0, run_time=1.2)
        self.wait(0.3)
        self.apply_matrix(A_2D, path_arc=0, run_time=2.0)
        self.note("두 단계 = A 한 번", DONE)
        self.wait(2)


class ElementaryMatrixGrid(GridScene):
    """정의 6-2. 기본행렬 세 유형은 평면의 반사 · 축 방향 늘림 · 층밀림이다.

    유형 I E12 는 y = x 에 대한 반사, 유형 II E2^3 은 y 축 방향 3배, 유형 III E12^2 는
    1행의 2배를 2행에 더하는 층밀림이다. 셋 다 되돌릴 수 있고 되돌리는 행렬도 같은 유형이다.
    참고: legacy/_2016/eola/chapter3.py (반사 · 층밀림)
    """
    steps = [
        ([[0, 1], [1, 0]], R"E_{12}=\begin{bmatrix}0&1\\1&0\end{bmatrix}", "유형 I · 행 교환", "y = x 에 대한 반사"),
        ([[1, 0], [0, 3]], R"E_{2}^{3}=\begin{bmatrix}1&0\\0&3\end{bmatrix}", "유형 II · 2행에 3 곱하기", "y 축 방향 3배"),
        ([[1, 0], [2, 1]], R"E_{12}^{2}=\begin{bmatrix}1&0\\2&1\end{bmatrix}", "유형 III · 1행의 2배를 2행에", "층밀림 · 단위 하삼각행렬"),
    ]

    def construct(self):
        head_on_grid(self, "기본행렬", "정의 6-2")
        self.add_unit_square()
        self.play(FadeIn(self.square), run_time=0.5)
        panel = None
        for matrix, tex, first, second in self.steps:
            new = Tex(tex).set_color(INK).set_width(3.6)
            if panel is None:
                panel = side_panel(self, [new], width=3.6)
            else:
                new.move_to(panel).align_to(panel, RIGHT)
                new.add_background_rectangle(opacity=0.85, buff=0.12)
                self.add_foreground_mobject(new)
                self.play(FadeOut(panel), FadeIn(new), run_time=0.5)
                self.foreground_mobjects.remove(panel)
                panel = new
            self.note(first, ACCENT)
            self.apply_matrix(matrix, path_arc=0, run_time=1.8)
            self.wait(0.3)
            self.note(second, DONE)
            self.wait(1.0)
            self.note("역행렬도 기본행렬", GREY_B)
            self.apply_inverse(matrix, path_arc=0, run_time=1.2)
            self.wait(0.4)
        self.note("유형 III 만으로 되면 A = LU", DONE)
        self.wait(2)


class LUByRowOps(InteractiveScene):
    """예제 6-1 · 정리 6-1. 행 연산의 배수가 그대로 L 의 성분이 된다.

    A = [[1,2,0],[0,1,2],[2,0,1]]. R3 ← R3 − 2R1, R3 ← R3 + 4R2 로 U = [[1,2,0],[0,1,2],[0,0,9]].
    뺀 배수 2 와 −4 의 부호를 바꾸지 않고 '뺀 만큼'을 L 의 (3,1), (3,2) 에 적으면 L = [[1,0,0],[0,1,0],[2,−4,1]].
    E2 E1 A = U 에서 A = E1⁻¹ E2⁻¹ U 이고 E1⁻¹ E2⁻¹ 이 L 이다(정리 6-1 의 증명).
    """
    A0 = [[1, 2, 0], [0, 1, 2], [2, 0, 1]]
    A1 = [[1, 2, 0], [0, 1, 2], [0, -4, 1]]
    U = [[1, 2, 0], [0, 1, 2], [0, 0, 9]]

    def board(self, values):
        m = mat(strings(values), INK, h_buff=0.9, v_buff=0.62)
        m.set_height(2.1).move_to(LEFT * 3.4 + UP * 1.1)
        return m

    def construct(self):
        head = slide_title("행 연산과 LU 분해")
        self.add(head)
        tag = tag_under(head, "예제 6-1 · 정리 6-1")
        self.play(FadeIn(tag))

        a_lab = Tex("A=").set_color(INK)
        m = self.board(self.A0)
        a_lab.next_to(m, LEFT, buff=0.15)
        self.play(FadeIn(a_lab), FadeIn(m))

        l_lab = Tex("L=").set_color(CALM)
        L = mat([["1", "0", "0"], ["0", "1", "0"], [R"\square", R"\square", "1"]], CALM, h_buff=0.9, v_buff=0.62)
        L.set_height(2.1).move_to(RIGHT * 3.6 + UP * 1.1)
        l_lab.next_to(L, LEFT, buff=0.15)
        self.play(FadeIn(l_lab), FadeIn(L))
        shown = footnote(self, "행 연산으로 상삼각행렬을 만듦", GREY_B)
        self.wait(0.8)

        # 1단계 — R3 ← R3 − 2R1
        target = box(m.get_entries()[6], WARN, 0.1)
        op1 = Tex(R"R_3\leftarrow R_3-2R_1").set_color(WARN).scale(0.9)
        op1.next_to(m, DOWN, buff=0.45)
        self.play(ShowCreation(target), Write(op1), run_time=0.8)
        self.wait(0.5)
        m1 = self.board(self.A1)
        self.play(FadeOut(target), ReplacementTransform(m, m1), run_time=1.0)
        m = m1
        new_entry = Tex("2").set_color(DONE).move_to(L.get_entries()[6])
        self.play(Transform(L.get_entries()[6], new_entry), run_time=0.6)
        shown = footnote(self, "배수 2 가 L 의 (3,1) 로", DONE, shown)
        self.wait(1.0)

        # 2단계 — R3 ← R3 + 4R2
        target = box(m.get_entries()[7], WARN, 0.1)
        op2 = Tex(R"R_3\leftarrow R_3+4R_2").set_color(WARN).scale(0.9)
        op2.move_to(op1)
        self.play(ShowCreation(target), FadeOut(op1), Write(op2), run_time=0.8)
        self.wait(0.5)
        m2 = self.board(self.U)
        self.play(FadeOut(target), ReplacementTransform(m, m2), run_time=1.0)
        m = m2
        u_lab = Tex("U=").set_color(ACCENT).move_to(a_lab)
        self.play(FadeOut(a_lab), FadeIn(u_lab), m.animate.set_color(ACCENT), run_time=0.5)
        new_entry2 = Tex("-4").set_color(DONE).move_to(L.get_entries()[7])
        self.play(Transform(L.get_entries()[7], new_entry2), run_time=0.6)
        shown = footnote(self, "배수 −4 가 L 의 (3,2) 로", DONE, shown)
        self.wait(1.0)

        # 정리 6-1 의 증명을 한 줄로
        proof = VGroup(
            Tex(R"E_2E_1A=U\ \Rightarrow\ A=E_1^{-1}E_2^{-1}U=LU").set_color(INK),
            Tex(R"L=E_1^{-1}E_2^{-1}=E_{13}^{2}E_{23}^{-4}=\begin{bmatrix}1&0&0\\0&1&0\\2&-4&1\end{bmatrix}").set_color(CALM),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).set_width(6.8)
        proof.next_to(op2, DOWN, buff=0.3).align_to(m, LEFT).shift(LEFT * 0.9)
        self.play(FadeOut(op2), Write(proof), run_time=1.6)
        shown = footnote(self, "검산 · LU 의 3행 = (2, 0, 1)", DONE, shown)
        self.wait(2)


class LUSolve(InteractiveScene):
    """LU 로 연립방정식 풀기. 삼각행렬 두 개는 대입만으로 풀린다.

    예제 6-1 의 A = LU 에 b = (3, 3, 3). Ly = b 를 위에서 아래로(앞으로 대입) 풀면 y = (3, 3, 9),
    Ux = y 를 아래에서 위로(뒤로 대입) 풀면 x = (1, 1, 1). b 가 바뀌어도 분해는 다시 하지 않는다.
    """
    L = [["1", "0", "0", "3"], ["0", "1", "0", "3"], ["2", "-4", "1", "3"]]
    U = [["1", "2", "0", "3"], ["0", "1", "2", "3"], ["0", "0", "9", "9"]]

    def system(self, values, color):
        g = augmented(values, 3, color, h_buff=0.85, v_buff=0.6)
        g.set_width(4.0)
        return g

    def construct(self):
        head = slide_title("LU 로 연립방정식 풀기")
        self.add(head)
        tag = tag_under(head, "예제 6-1 의 A · b = (3, 3, 3)")
        self.play(FadeIn(tag))

        chain = Tex(R"A\mathbf{x}=\mathbf{b}\ \Rightarrow\ L(U\mathbf{x})=\mathbf{b}\ \Rightarrow\ "
                    R"L\mathbf{y}=\mathbf{b},\ U\mathbf{x}=\mathbf{y}").set_color(INK)
        chain.set_width(8.0).next_to(tag, DOWN, buff=0.3).align_to(tag, LEFT)
        self.play(Write(chain), run_time=1.4)
        self.wait(0.6)

        left = self.system(self.L, CALM).move_to(LEFT * 3.3 + DOWN * 0.15)
        right = self.system(self.U, ACCENT).move_to(RIGHT * 3.3 + DOWN * 0.15)
        l_head = Tex(R"L\mathbf{y}=\mathbf{b}").set_color(CALM).next_to(left, UP, buff=0.3)
        u_head = Tex(R"U\mathbf{x}=\mathbf{y}").set_color(ACCENT).next_to(right, UP, buff=0.3)
        self.play(FadeIn(left), FadeIn(l_head), run_time=0.8)
        shown = footnote(self, "앞으로 대입 · Ly = b", CALM)

        y_vals = ["y_1=3", "y_2=3", "y_3=3-2\\cdot3+4\\cdot3=9"]
        y_rows = VGroup(*[Tex(t).set_color(DONE).scale(0.8) for t in y_vals])
        y_rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(left, DOWN, buff=0.3)
        rows = left.matrix.get_rows()
        for k, (row, text) in enumerate(zip(rows, y_rows)):
            mark = box(row, DONE, 0.1)
            self.play(ShowCreation(mark), run_time=0.4)
            self.play(Write(text), run_time=0.8)
            self.play(FadeOut(mark), run_time=0.3)
        self.wait(0.8)

        self.play(FadeIn(right), FadeIn(u_head), run_time=0.8)
        shown = footnote(self, "뒤로 대입 · Ux = y", ACCENT, shown)
        x_vals = ["9x_3=9\\ \\Rightarrow\\ x_3=1", "x_2+2\\cdot1=3\\ \\Rightarrow\\ x_2=1", "x_1+2\\cdot1=3\\ \\Rightarrow\\ x_1=1"]
        x_rows = VGroup(*[Tex(t).set_color(DONE).scale(0.8) for t in x_vals])
        x_rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(right, DOWN, buff=0.3)
        rows = right.matrix.get_rows()
        for row, text in zip(reversed(list(rows)), x_rows):
            mark = box(row, DONE, 0.1)
            self.play(ShowCreation(mark), run_time=0.4)
            self.play(Write(text), run_time=0.8)
            self.play(FadeOut(mark), run_time=0.3)
        shown = footnote(self, "해 x = (1, 1, 1)", DONE, shown)
        self.wait(1.0)
        shown = footnote(self, "b 가 바뀌어도 분해는 한 번", GREY_B, shown)
        self.wait(2)


class PLUPermutation(InteractiveScene):
    """예제 6-3. 피벗 자리에 0 이 나오면 행 교환이 필요하고, 그 교환이 치환행렬 P 가 된다.

    A = [[1,1,1],[1,1,0],[0,1,1]] 은 R2 − R1 뒤에 (2,2) 성분이 0 이라 유형 III 만으로는 상삼각이 되지 않는다.
    2행과 3행을 먼저 바꾼 PA 는 LU 가 되고(L = [[1,0,0],[0,1,0],[1,0,1]], U = [[1,1,1],[0,1,1],[0,0,−1]]),
    P⁻¹ = P 이므로 A = PLU 다.
    """
    A0 = [[1, 1, 1], [1, 1, 0], [0, 1, 1]]
    A1 = [[1, 1, 1], [0, 0, -1], [0, 1, 1]]
    PA = [[1, 1, 1], [0, 1, 1], [1, 1, 0]]
    U = [[1, 1, 1], [0, 1, 1], [0, 0, -1]]

    def board(self, values, color=INK):
        m = mat(strings(values), color, h_buff=0.9, v_buff=0.62)
        m.set_height(2.3).move_to(LEFT * 3.4 + UP * 0.5)
        return m

    def construct(self):
        head = slide_title("PLU 분해")
        self.add(head)
        tag = tag_under(head, "예제 6-3")
        self.play(FadeIn(tag))

        a_lab = Tex("A=").set_color(INK)
        m = self.board(self.A0)
        a_lab.next_to(m, LEFT, buff=0.15)
        self.play(FadeIn(a_lab), FadeIn(m))
        shown = footnote(self, "유형 III 로 상삼각행렬 만들기", GREY_B)

        op1 = Tex(R"R_2\leftarrow R_2-R_1").set_color(WARN).scale(0.9).next_to(m, DOWN, buff=0.45)
        self.play(Write(op1), run_time=0.7)
        m1 = self.board(self.A1)
        self.play(ReplacementTransform(m, m1), run_time=1.0)
        m = m1
        pivot = box(m.get_entries()[4], WARN, 0.1)
        self.play(ShowCreation(pivot), run_time=0.5)
        shown = footnote(self, "피벗 자리에 0 · 행 교환 필요", WARN, shown)
        self.wait(1.2)

        # 처음으로 돌아가 2행과 3행을 먼저 바꾼다.
        self.play(FadeOut(pivot), FadeOut(op1), run_time=0.4)
        m0 = self.board(self.A0)
        self.play(ReplacementTransform(m, m0), run_time=0.6)
        m = m0
        P = Tex(R"P=\begin{bmatrix}1&0&0\\0&0&1\\0&1&0\end{bmatrix}").set_color(DONE).set_height(1.8)
        P.move_to(RIGHT * 3.6 + UP * 0.5)
        self.play(FadeIn(P, LEFT), run_time=0.7)
        shown = footnote(self, "2행과 3행 교환 · 치환행렬 P", DONE, shown)
        pa_lab = Tex("PA=").set_color(INK).move_to(a_lab).shift(LEFT * 0.25)
        mp = self.board(self.PA)
        self.play(FadeOut(a_lab), FadeIn(pa_lab), ReplacementTransform(m, mp), run_time=1.0)
        m = mp
        self.wait(0.8)

        op2 = Tex(R"R_3\leftarrow R_3-R_1").set_color(WARN).scale(0.9).next_to(m, DOWN, buff=0.45)
        self.play(Write(op2), run_time=0.7)
        mu = self.board(self.U, ACCENT)
        u_lab = Tex("U=").set_color(ACCENT).move_to(pa_lab)
        self.play(ReplacementTransform(m, mu), FadeOut(pa_lab), FadeIn(u_lab), run_time=1.0)
        shown = footnote(self, "배수 1 이 L 의 (3,1) 로", CALM, shown)
        L = Tex(R"L=\begin{bmatrix}1&0&0\\0&1&0\\1&0&1\end{bmatrix}").set_color(CALM).set_height(1.8)
        L.next_to(P, DOWN, buff=0.4)
        self.play(FadeIn(L, UP), run_time=0.7)
        self.wait(0.8)

        result = Tex(R"PA=LU\ \Rightarrow\ A=P^{-1}LU=PLU").set_color(DONE)
        result.set_width(6.4).next_to(op2, DOWN, buff=0.4).align_to(mu, LEFT).shift(LEFT * 0.9)
        self.play(FadeOut(op2), Write(result), run_time=1.2)
        shown = footnote(self, "교환은 P · 배수는 L", DONE, shown)
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 6.2 특잇값 분해
# ─────────────────────────────────────────────────────────────
class SingularValueEllipse(GridScene):
    """정의 6-3 · 정리 6-3. 특잇값은 단위원이 가는 타원의 반축 길이다.

    A = [[2,2],[−1,2]] 에서 AᵀA = [[5,2],[2,8]] 의 고윳값은 9, 4 이고 단위 고유벡터는 (1,2)/√5, (−2,1)/√5 다.
    A 를 적용하면 단위원은 타원이 되고, 두 고유벡터는 서로 수직인 반축 Av1, Av2 로 간다.
    길이가 √9 = 3, √4 = 2 — 그것이 특잇값이다. 다른 방향의 벡터는 길이가 그 사이에 있다.
    """

    def construct(self):
        head_on_grid(self, "특잇값과 타원", "정의 6-3 · 정리 6-3")
        rows = [
            Tex(R"A=\begin{bmatrix}2&2\\-1&2\end{bmatrix}").set_color(ACCENT),
            Tex(R"A^{T}A=\begin{bmatrix}5&2\\2&8\end{bmatrix},\ \lambda=9,\,4").set_color(INK),
        ]
        panel = side_panel(self, rows, width=4.2)
        unit_circle(self)
        v1 = self.vec((1 / S5, 2 / S5), DONE, R"\mathbf{v}_1", R"A\mathbf{v}_1")
        v2 = self.vec((-2 / S5, 1 / S5), CALM, R"\mathbf{v}_2", R"A\mathbf{v}_2", direction="left")
        w = self.vec((1, 0), GREY_B, R"\mathbf{w}", R"A\mathbf{w}")
        self.note("단위원과 AᵀA 의 고유벡터 v1, v2", GREY_B)
        self.wait(0.8)

        self.apply_matrix(A_SVD, path_arc=0, run_time=2.4)
        self.note("원이 타원으로", ACCENT)
        self.wait(0.6)

        # 수직 표시와 길이
        origin = self.background_plane.c2p(0, 0)
        elbow = Elbow(width=0.3, angle=angle_of_vector(v1.get_end() - origin)).set_stroke(DONE, 3)
        elbow.shift(origin)
        self.play(ShowCreation(elbow), run_time=0.5)
        self.note("Av1 ⊥ Av2 · 길이 3, 2", DONE)
        self.wait(1.0)

        facts = bottom_panel(self, [
            Tex(R"\lVert A\mathbf{v}_1\rVert=\sqrt{9}=3=\sigma_1").set_color(DONE),
            Tex(R"\lVert A\mathbf{v}_2\rVert=\sqrt{4}=2=\sigma_2").set_color(CALM),
            Tex(R"2\le\lVert A\mathbf{w}\rVert\le 3").set_color(GREY_B),
        ], width=4.4)
        self.note("특잇값 σ = √λ · 타원의 반축", DONE)
        self.wait(2)


class SVDThreeSteps(GridScene):
    """정의 6-4 · 정리 6-5. A = UΣVᵀ 는 회전 → 축 방향 늘림 → 회전이다.

    Vᵀ 가 고유벡터 v1, v2 를 e1, e2 자리로 돌리고, Σ 가 e1 방향을 3배 · e2 방향을 2배로 늘리고,
    U 가 그 결과를 u1, u2 방향으로 돌린다. 세 단계를 거친 그림이 A 를 한 번에 적용한 그림과 같다.
    """

    def construct(self):
        head_on_grid(self, "특잇값 분해의 세 단계", "정의 6-4 · 정리 6-5")
        eq = Tex(R"A=U\Sigma V^{T}", isolate=["U", R"\Sigma", "V^{T}"]).set_color(INK).scale(1.2)
        mats = Tex(R"U=\tfrac{1}{\sqrt5}\begin{bmatrix}2&-1\\1&2\end{bmatrix},\ "
                   R"\Sigma=\begin{bmatrix}3&0\\0&2\end{bmatrix},\ "
                   R"V=\tfrac{1}{\sqrt5}\begin{bmatrix}1&-2\\2&1\end{bmatrix}").set_color(INK)
        panel = side_panel(self, [eq, mats], width=5.4)
        self.add_unit_square()
        self.play(FadeIn(self.square), run_time=0.5)
        unit_circle(self)
        self.vec((1 / S5, 2 / S5), DONE)
        self.vec((-2 / S5, 1 / S5), CALM)
        self.wait(0.4)

        self.note("Vᵀ · 회전 · v1, v2 가 축으로", ACCENT)
        self.play(eq.select_part("V^{T}").animate.set_color(ACCENT), run_time=0.4)
        self.apply_matrix(VT_SVD, run_time=2.0)
        self.wait(0.5)

        self.note("Σ · 축 방향 3배, 2배", DONE)
        self.play(eq.select_part("V^{T}").animate.set_color(INK),
                  eq.select_part(R"\Sigma").animate.set_color(DONE), run_time=0.4)
        self.apply_matrix(SIGMA_SVD, path_arc=0, run_time=2.0)
        self.wait(0.5)

        self.note("U · 회전 · 축이 u1, u2 로", CALM)
        self.play(eq.select_part(R"\Sigma").animate.set_color(INK),
                  eq.select_part("U").animate.set_color(CALM), run_time=0.4)
        self.apply_matrix(U_SVD, run_time=2.0)
        self.wait(0.5)
        self.play(eq.select_part("U").animate.set_color(INK), run_time=0.3)
        self.note("세 단계 = A", DONE)
        self.wait(1.0)

        self.note("되돌린 뒤 A 한 번에 적용", GREY_B)
        self.apply_inverse(A_SVD, path_arc=0, run_time=1.2)
        self.wait(0.3)
        self.apply_matrix(A_SVD, path_arc=0, run_time=2.0)
        self.note("같은 그림 · A = UΣVᵀ", DONE)
        self.wait(2)


def sample_image(n=24):
    """예시 자료. 웃는 얼굴을 n×n 밝기 행렬로 만든다(0 검정 · 1 흰색)."""
    y, x = np.mgrid[0:n, 0:n]
    c = (n - 1) / 2.0
    img = np.full((n, n), 0.15)
    img[(x - c) ** 2 + (y - c) ** 2 <= (n * 0.42) ** 2] = 0.9
    for ex in (c - 4.5, c + 4.5):
        img[(x - ex) ** 2 + (y - (c - 3.5)) ** 2 <= 2.0 ** 2] = 0.1
    r2 = (x - c) ** 2 + (y - (c - 1)) ** 2
    img[(r2 >= 5.5 ** 2) & (r2 <= 7.0 ** 2) & (y > c + 2.5)] = 0.1
    return img


def pixel_grid(values, side=0.14):
    """밝기 행렬을 정사각형 모눈으로 그린다."""
    n, m = values.shape
    squares = VGroup()
    for i in range(n):
        for j in range(m):
            v = float(np.clip(values[i, j], 0, 1))
            sq = Square(side_length=side).set_stroke(width=0)
            sq.set_fill(interpolate_color(BLACK, WHITE, v), opacity=1)
            sq.move_to(np.array([j * side, -i * side, 0]))
            squares.add(sq)
    squares.center()
    return squares


class SVDLowRank(InteractiveScene):
    """응용. 특잇값을 큰 것부터 k 개만 더한 A_k = Σ σᵢ uᵢ vᵢᵀ 가 저랭크 근사다.

    24×24 예시 이미지(웃는 얼굴)를 numpy 로 특잇값 분해하고, k = 1, 2, 3, 4, 6, 10, 24 로 다시 만든다.
    특잇값이 작은 항을 버려도 그림이 남는다. 저장하는 수는 k(m+n+1) 개 — 이미지 압축과 주성분분석(CH12)의 바탕이다.
    값은 씬 안에서 계산한다(하네스 3.8).
    """
    ks = [1, 2, 3, 4, 6, 10, 24]

    def construct(self):
        head = slide_title("저랭크 근사")
        self.add(head)
        tag = tag_under(head, "A = σ1u1v1ᵀ + σ2u2v2ᵀ + … · 응용")
        self.play(FadeIn(tag))

        img = sample_image()
        n = img.shape[0]
        U, s, VT = np.linalg.svd(img)

        orig = pixel_grid(img).move_to(LEFT * 4.2 + DOWN * 0.4)
        o_lab = caption("원본 A · 24×24 예시 자료", 22, GREY_B).next_to(orig, UP, buff=0.25)
        self.play(FadeIn(orig), FadeIn(o_lab), run_time=0.8)

        # 특잇값 막대 — 오른쪽 위. 큰 것부터 k 개를 켠다.
        bars = VGroup()
        bar_w = 0.16
        for i, val in enumerate(s):
            b = Rectangle(width=bar_w * 0.8, height=max(float(val) / float(s[0]) * 1.6, 0.02))
            b.set_stroke(width=0).set_fill(GREY_C, 1)
            b.move_to(np.array([i * bar_w, 0, 0]), DOWN)
            bars.add(b)
        bars.move_to(RIGHT * 4.3 + DOWN * 0.2)
        s_lab = caption("특잇값 σ1 ≥ σ2 ≥ … ≥ σ24", 22, GREY_B).next_to(bars, UP, buff=0.2)
        self.play(FadeIn(bars), FadeIn(s_lab), run_time=0.8)

        recon = None
        k_lab = None
        store = None
        shown = footnote(self, "k 개의 항만 더함", GREY_B)
        for k in self.ks:
            approx = (U[:, :k] * s[:k]) @ VT[:k, :]
            new = pixel_grid(approx).move_to(LEFT * 0.3 + DOWN * 0.4)
            new_k = Tex(R"A_{%d}=\sum_{i=1}^{%d}\sigma_i\mathbf{u}_i\mathbf{v}_i^{T}" % (k, k)).set_color(DONE)
            new_k.scale(0.75).next_to(new, UP, buff=0.2)
            count = k * (2 * n + 1)
            new_store = caption("저장 값 %d / %d" % (count, n * n), 22, CALM).next_to(new, DOWN, buff=0.2)
            lit = [bars[i].animate.set_fill(DONE) for i in range(k)]
            if recon is None:
                recon, k_lab, store = new, new_k, new_store
                self.play(FadeIn(recon), FadeIn(k_lab), FadeIn(store), *lit, run_time=0.8)
            else:
                self.play(Transform(recon, new), Transform(k_lab, new_k), Transform(store, new_store), *lit,
                          run_time=1.0)
            self.wait(0.9)
        shown = footnote(self, "k = 24 · 원본과 같음", DONE, shown)
        self.wait(0.8)
        shown = footnote(self, "작은 특잇값의 항은 생략 가능", DONE, shown)
        self.wait(2)


class SvdCodeReview(InteractiveScene):
    """예제 6-6 의 코드. np.linalg.svd 가 반환하는 세 값의 모양을 읽는다.

    코드 여섯 줄은 `파이썬실습/py/06_행렬 분해.py` 와 글자 단위로 같다. Sig 는 특잇값만 든 1차원 배열이라
    m×n 의 Σ 는 영행렬을 만들어 대각에 채운다. U · VT 의 열 부호는 구현에 따라 바뀔 수 있다.
    """
    lines = (
        "A = np.array([[1, 2, 0], [0, 1, 2]])",
        "U, Sig, VT = np.linalg.svd(A) # 특잇값 분해",
        "m, n = A.shape",
        "Sigma = np.zeros((m, n)) # m×n 행렬 Σ",
        "k = np.size(Sig)",
        "Sigma[:k, :k] = np.diag(Sig) # 특잇값",
    )

    def construct(self):
        head = slide_title("특잇값 분해 코드 리뷰")
        self.add(head)
        tag = tag_under(head, "예제 6-6 · np.linalg.svd")
        self.play(FadeIn(tag))

        block = code_block(self.lines, 20, buff=0.24)
        block.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)
        self.play(LaggedStartMap(FadeIn, block[:2], lag_ratio=0.3), run_time=1.0)
        shown = footnote(self, "반환값 셋 · U, Sig, VT", GREY_B)
        shapes = VGroup(
            code("U.shape    (2, 2)", 20, CALM),
            code("Sig.shape  (2,)", 20, DONE),
            code("VT.shape   (3, 3)", 20, CALM),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        shapes.next_to(block, RIGHT, buff=1.0).align_to(block, UP)
        self.play(FadeIn(shapes, lag_ratio=0.3), run_time=0.9)
        self.wait(0.8)

        sig = VGroup(
            code("Sig = [2.64575131 1.73205081]", 20, DONE),
            Tex(R"=\,[\sqrt7\ \ \sqrt3]").set_color(DONE).scale(0.9),
        ).arrange(RIGHT, buff=0.25)
        sig.next_to(shapes, DOWN, buff=0.5).align_to(shapes, LEFT)
        self.play(Write(sig), run_time=1.0)
        shown = footnote(self, "Sig 는 1차원 · 대각행렬 아님", DONE, shown)
        self.wait(1.2)

        self.play(LaggedStartMap(FadeIn, block[2:], lag_ratio=0.3), run_time=1.2)
        mark = box(block[3], ACCENT, 0.08)
        self.play(ShowCreation(mark), run_time=0.4)
        sigma = VGroup(
            code("Sigma =", 20, ACCENT),
            mat([[R"\sqrt7", "0", "0"], ["0", R"\sqrt3", "0"]], ACCENT, h_buff=0.7, v_buff=0.5).set_height(1.1),
        ).arrange(RIGHT, buff=0.25)
        sigma.next_to(sig, DOWN, buff=0.45).align_to(sig, LEFT)
        self.play(FadeIn(sigma), run_time=0.8)
        shown = footnote(self, "Σ 는 m×n · 영행렬에 대각 채움", ACCENT, shown)
        self.wait(1.0)
        self.play(FadeOut(mark), run_time=0.3)

        outs = code_block((
            "U = [[-0.707 -0.707]",
            "     [-0.707  0.707]]",
            "VT[0] = [-0.267 -0.802 -0.535]",
        ), 18, buff=0.14)
        outs.set_color(CALM)
        outs.next_to(block, DOWN, buff=0.45).align_to(block, LEFT)
        self.play(FadeIn(outs, lag_ratio=0.3), run_time=0.9)
        shown = footnote(self, "부호는 바뀔 수 있음 · UΣVᵀ = A", GREY_B, shown)
        self.wait(2)
