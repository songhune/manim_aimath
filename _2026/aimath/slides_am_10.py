# -*- coding: utf-8 -*-
"""AM_10 (교재 Chapter 10 확률과 확률분포) 영상 9편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_10 --module _2026/aimath/slides_am_10.py

씬 정의는 `_2026/aimath/week11.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다(이유는 slides_am_02.py 와 같다).
from _2026.aimath.slides_common import build
from _2026.aimath import week11

PAGES = build(globals(), [
    ("ConditionalProbabilityCrowd", "조건부 확률 · 표본공간의 축소"),
    ("IndependenceDiceGrid", "독립사건 · 주사위 두 개"),
    ("BayesAreaSpam", "베이즈 정리 · 스팸 필터"),
    ("ExpectationBalance", "기댓값과 분산 · 막대의 균형점"),
    ("BinomialCounting", "이항분포 · 성공 수가 같은 결과"),
    ("PoissonLimit", "이항분포와 푸아송분포"),
    ("NormalStandardize", "정규분포와 표준화"),
    ("BinomialNormalApprox", "이항분포의 정규분포 근사"),
    ("CentralLimitDice", "중심극한정리 · 주사위의 표본평균"),
], (week11,))
