# -*- coding: utf-8 -*-
"""AM_09 (교재 Chapter 9 편미분과 경사 하강법) 영상 8편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_09 --module _2026/aimath/slides_am_09.py

씬 정의는 `_2026/aimath/week10.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week10

PAGES = build(globals(), [
    ("SurfaceAndLevelSets", "그래프와 레벨집합"),
    ("PartialDerivativeSlice", "편도함수 · 단면의 기울기"),
    ("GradientDirection", "방향도함수와 그래디언트"),
    ("ChainRuleCurve", "연쇄법칙 · 경로 위의 변화율"),
    ("LagrangeTangency", "라그랑주 승수법 · 접점 조건"),
    ("QuadraticFormBowl", "정부호 행렬 · 곡면의 모양"),
    ("HessianCritical", "헤시안 판별 · 안장점과 극소점"),
    ("GradientDescentSteps", "경사 하강법 · step"),
], (week10,))
