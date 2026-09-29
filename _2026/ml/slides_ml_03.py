# -*- coding: utf-8 -*-
"""ML_03 (회귀 알고리즘과 모델 규제 · k-최근접 이웃 회귀의 확률적 해석) 영상 2편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter ml_03 --module _2026/ml/slides_ml_03.py

씬 정의는 `_2026/ml/ml_week04.py` 에 있다. 끊는 규칙은 `_2026/aimath/slides_common.py` 참고.
장 번호는 주차가 아니라 교재(혼자 공부하는 머신러닝+딥러닝) 장 번호다(하네스 3.6).
두 씬 모두 단(段)마다 긴 wait 를 두어 페이지가 그 자리에서 끊긴다.
"""
from _2026.aimath.slides_common import build
from _2026.ml import ml_week04

PAGES = build(globals(), [
    ("RandomVariableToVariance", "확률변수·분포·기댓값·분산"),
    ("ConditionalToKNN", "조건부 기댓값과 k-최근접 이웃 회귀"),
], (ml_week04,))
