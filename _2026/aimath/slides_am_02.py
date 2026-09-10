# -*- coding: utf-8 -*-
"""AM_02 (교재 Chapter 2 가우스-조르당 소거법과 여러 가지 행렬) 영상 12편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_02 --module _2026/aimath/slides_am_02.py

씬 정의는 `_2026/aimath/week03.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다. manimlib 은 들여올 때 sys.argv 를 읽는데,
# manim_slides 쪽 어댑터가 그 사이 argv 를 잠시 비워 준다. week 모듈을 먼저
# 들여오면 빌드 스크립트의 인자를 manimlib 이 제 것으로 읽어 오류가 난다.
from _2026.aimath.slides_common import build
from _2026.aimath import week03

PAGES = build(globals(), [
    ("AugmentedMatrix", "첨가행렬"),
    ("GaussJordan", "가우스-조르당 소거법"),
    ("ReadRREF", "기약 행 사다리꼴에서 해 읽기"),
    ("Determinant2x2", "행렬식"),
    ("InverseByRowOps", "행 연산으로 구하는 역행렬"),
    ("DeterminantZero", "행렬식이 0 인 행렬"),
    ("Determinant3x3", "3차 정방행렬의 행렬식"),
    ("DeterminantRules", "행렬식의 성질"),
    ("SocksShoes", "양말-신발 성질"),
    ("InverseSolve", "역행렬로 푸는 행렬방정식"),
    ("TransposeRules", "전치행렬의 성질"),
    ("MatrixZoo", "여러 가지 행렬"),
], (week03,))
