# -*- coding: utf-8 -*-
"""AM_04 (교재 Chapter 4 선형변환과 랭크 정리) 영상 16편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_04 --module _2026/aimath/slides_am_04.py

씬 정의는 `_2026/aimath/week05.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week05

PAGES = build(globals(), [
    ("LinearTransformationIntro", "선형변환이란"),
    ("NonlinearExamples", "선형인 것과 아닌 것"),
    ("BrokenArrowProblem", "보충 · 부러진 화살 문제"),
    ("ColumnsAreImages", "표준행렬의 열"),
    ("StandardMatrixFromPair", "표준행렬 구하기"),
    ("ReflectionTransform", "반사변환"),
    ("RotationTransform", "회전변환"),
    ("CompositeTransform", "합성변환의 표준행렬"),
    ("InverseTransform", "역변환"),
    ("OrthogonalOperator", "직교연산자"),
    ("ColumnSpaceNullSpace", "열공간 · 행공간 · 영공간"),
    ("RankAndKernel", "랭크와 영공간"),
    ("RankNullityTheorem", "랭크 정리"),
    # 2026-10-13 추가 — 7주차 복습용 세 편
    ("ReflectRotateOrder", "반사와 회전의 순서"),
    ("TransformationGallery", "표준행렬 읽기"),
    ("RowSpaceNullSpace", "행공간과 영공간의 직교"),
], (week05,), step_at={"BrokenArrowProblem": 1.6})   # 문구 교체가 0.5초씩이라 기본값으로는 클릭이 너무 잦다
