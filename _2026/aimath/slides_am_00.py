# -*- coding: utf-8 -*-
"""AM_00 (강좌소개·오리엔테이션) 영상 4편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter am_00 --module _2026/aimath/slides_am_00.py

씬 정의는 `_2026/aimath/week01.py` 에 있다. 규칙은 `slides_common.py` 참고.
"""
# manim_slides 를 먼저 들여온다. manimlib 은 들여올 때 sys.argv 를 읽는데,
# manim_slides 쪽 어댑터가 그 사이 argv 를 잠시 비워 준다. week 모듈을 먼저
# 들여오면 빌드 스크립트의 인자를 manimlib 이 제 것으로 읽어 오류가 난다.
from _2026.aimath.slides_common import build
from _2026.aimath import week01

PAGES = build(globals(), [
    ("CourseRoadmap", "학기 수강계획"),
    ("PixelsAreDiscrete", "연속 화면과 이산 픽셀"),
    ("ImageAsMatrix", "이미지의 행렬 표현"),
    ("GradientDescentGlimpse", "경사 하강법 개요"),
], (week01,))
