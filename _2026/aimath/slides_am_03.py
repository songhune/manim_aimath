# -*- coding: utf-8 -*-
"""AM_03 (교재 Chapter 3 벡터공간과 내적) 영상 19편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_03 --module _2026/aimath/slides_am_03.py

씬 정의는 `_2026/aimath/week04.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week04

PAGES = build(globals(), [
    ("VectorOperations", "벡터의 합 · 차 · 스칼라곱"),
    ("ClosedUnderOperations", "벡터공간의 조건"),
    ("SubspaceLine", "부분공간 판정법"),
    ("LinearCombination", "선형결합"),
    ("IndependenceCollinear", "선형독립과 선형종속"),
    ("SpanLineToPlane", "생성집합"),
    ("BasisDimension", "기저와 차원"),
    ("VectorNorm", "노름"),
    ("TriangleInequality", "삼각부등식"),
    ("InnerProduct", "내적"),
    ("InnerProductCosine", "사잇각을 이용한 내적"),
    ("CauchySchwarz", "코시-슈바르츠 부등식"),
    ("OrthogonalPythagoras", "직교와 피타고라스 정리"),
    ("ProjectionOntoVector", "정사영"),
    ("InnerProductFamily", "내적공간"),
    ("HammingManhattan", "해밍 거리와 맨하튼 거리"),
    ("Gradient", "그래디언트"),
    ("Jacobian", "자코비안 행렬"),
    ("HessianLaplacian", "헤시안 행렬과 라플라시안"),
], (week04,))
