# -*- coding: utf-8 -*-
"""ML_03 (회귀 알고리즘과 모델 규제 · k-최근접 이웃 회귀의 확률적 해석) 영상 3편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter ml_03 --module _2026/ml/slides_ml_03.py

씬 정의는 `_2026/ml/ml_week04.py` 에 있다. 끊는 규칙은 `_2026/aimath/slides_common.py` 참고.
장 번호는 주차가 아니라 교재(혼자 공부하는 머신러닝+딥러닝) 장 번호다(하네스 3.6).
"""
from _2026.aimath.slides_common import build
from _2026.ml import ml_week04

PAGES = build(globals(), [
    ("PerchAsRandomVariable", "농어 표본과 확률변수"),
    ("ConditionalExpectation", "조건부 기댓값과 k-최근접 이웃"),
    ("LeastSquaresPrediction", "최소제곱과 조건부 기댓값"),
    ("ResidualAndConditionalSpread", "잔차와 조건부 분산"),
    ("NeighborCountAndVariance", "이웃 수 k 와 조건부 분산"),
    ("DistributionView", "분포 관점: 평균·중앙값·분위수"),
], (ml_week04,))
