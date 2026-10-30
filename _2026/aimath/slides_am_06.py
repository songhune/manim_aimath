# -*- coding: utf-8 -*-
"""AM_06 (교재 Chapter 6 행렬 분해) 영상 10편(참고 1편 포함)의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_06 --module _2026/aimath/slides_am_06.py

씬 정의는 `_2026/aimath/week07.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week07

PAGES = build(globals(), [
    ("LUAsComposition", "LU 분해"),
    ("ElementaryMatrixGrid", "기본행렬"),
    ("LUByRowOps", "행 연산과 LU 분해"),
    ("LUSolve", "LU 로 연립방정식 풀기"),
    ("PLUPermutation", "PLU 분해"),
    ("SingularValueScaling", "특잇값과 행렬식"),
    ("SVDThreeSteps", "특잇값 분해의 세 단계"),
    ("SvdCodeReview", "특잇값 분해 코드 리뷰"),
    ("SVDLowRank", "저랭크 근사"),
    ("PCAPreview", "주성분분석 미리 보기 (참고)"),
], (week07,))
