# -*- coding: utf-8 -*-
"""클릭 진행형 영상 시험 (manim-slides + manimgl).

한 영상 안의 동작 단위마다 멈췄다가 클릭(→ / 스페이스)으로 다음 단위로 넘어가는 형식이
가능한지 확인하는 시험 파일이다. 기존 씬을 그대로 상속하고, `self.wait()` 가 1초 이상이면
그 자리를 슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    MANIM_API=manimgl PYTHONPATH=.:legacy manim-slides render --GL _2026/probstat/slides_poc.py AdditionRuleSlides -w
    manim-slides convert AdditionRuleSlides videos/_scratch/slides/index.html --one-file

결과 index.html 은 RevealJS 페이지라 GitHub Pages 에 그대로 올릴 수 있다.
"""
import os
os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat.week02 import AdditionRule, Combinations


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다."""
    step_at = 1.0

    def wait(self, duration=1.0, *args, **kwargs):
        super().wait(duration, *args, **kwargs)
        if duration >= self.step_at:
            self.next_slide()


class AdditionRuleSlides(_StepSlide, AdditionRule):
    pass


class CombinationsSlides(_StepSlide, Combinations):
    pass
