# -*- coding: utf-8 -*-
"""AM_01 (교재 Chapter 1 연립선형방정식과 행렬) 영상 20편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_01 --module _2026/aimath/slides_am_01.py

차례는 강의 덱(`AI기초수학/week02_자료/_build_ch01_deck.py` 의 VIDEOS)과 같다.
`InnerOuterTensor` 는 덱에 넣지 않은 씬이라 여기서도 뺐다. 보충 일곱 편이 같은 내용을
크기 규칙으로 나누어 다룬다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다. manimlib 은 들여올 때 sys.argv 를 읽는데,
# manim_slides 쪽 어댑터가 그 사이 argv 를 잠시 비워 준다. week 모듈을 먼저
# 들여오면 빌드 스크립트의 인자를 manimlib 이 제 것으로 읽어 오류가 난다.
from _2026.aimath.slides_common import build
from _2026.aimath import week02

PAGES = build(globals(), [
    # 1.2 행렬의 정의
    ("EntryNotation", "행렬의 성분 표기"),
    ("ArrayDimensions", "3차원 이상의 배열"),
    ("SquareMatrixDiagonal", "정방행렬과 주대각선"),
    ("Transpose", "전치행렬"),
    ("SymmetricMatrix", "대칭행렬"),
    # 1.3 행렬의 연산
    ("MatrixAddition", "행렬의 합과 차"),
    ("ScalarMultiple", "스칼라곱"),
    ("MatrixProduct", "행렬의 곱"),
    ("ProductOrder", "곱의 순서"),
    ("ProductShapeRule", "곱이 정의되는 크기"),
    ("MatrixPower", "행렬의 거듭제곱"),
    # 1.4 행렬과 연립선형방정식의 관계
    ("RowOperations", "기본 행 연산"),
    ("EchelonForms", "행 사다리꼴과 기약 행 사다리꼴"),
    # 보충 — 곱이라 부르는 연산들
    ("VectorInnerProduct", "벡터의 내적"),
    ("MatrixVectorProduct", "행렬과 벡터의 곱"),
    ("VectorOuterProduct", "벡터의 외적"),
    ("CrossProduct", "벡터곱"),
    ("FrobeniusInner", "행렬의 내적"),
    ("KroneckerProduct", "크로네커 곱"),
    ("ProductSizeMap", "곱의 크기 규칙"),
], (week02,), step_at={
    # 성분마다 상자 → 블록 → 지우기 세 동작이 한 덩이다. 기본값이면 지나치게 잘게 나뉜다.
    "KroneckerProduct": 1.2,
    "SymmetricMatrix": 1.0,
    "ProductSizeMap": 0.5,      # 표는 줄마다 0.45초씩 붙는다
})
