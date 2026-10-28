# -*- coding: utf-8 -*-
"""AM_05 (교재 Chapter 5 고윳값과 케일리-해밀턴 정리) 영상 8편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_05 --module _2026/aimath/slides_am_05.py

씬 정의는 `_2026/aimath/week06.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week06

PAGES = build(globals(), [
    ("EigenvectorIntro", "고유벡터란"),
    ("CharacteristicEquation", "특성방정식"),
    ("TriangularEigen", "삼각행렬의 고윳값"),
    ("Eigenspace", "고유공간"),
    ("EigenPowers", "고윳값의 성질"),
    ("DetTraceFromEigen", "행렬식과 대각합"),
    ("CayleyHamiltonCollapse", "케일리-해밀턴 정리"),
    ("CayleyHamiltonUse", "케일리-해밀턴 정리의 쓰임"),
], (week06,))
