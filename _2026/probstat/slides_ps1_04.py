# -*- coding: utf-8 -*-
"""PS1_04 (Walpole Chapter 4) 영상 28편의 클릭 진행형 판 (manim-slides + manimgl).

slides_ps1_03.py 와 같은 장치다. week05.py 의 씬을 그대로 상속하고, `wait()` 가 임계값(기본 0.3초)
이상이면 그 자리를 슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    python tools/build_slides_site.py --chapter ps1_04 --module _2026/probstat/slides_ps1_04.py

PAGES 의 순서는 덱(insert_videos.py 의 PS1_04_INSERT)과 같다. 제목은 각 씬의 slide_title 문구다.
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat import week05

# (씬 이름, 화면 제목). 덱 순서. 7차 9/22 는 Example412LinearContinuous 까지, 8차 9/29 는 CovarianceSign 부터.
PAGES = [
    ("ExpectedValueAsBalance", "Expected Value"),
    ("Example41Components", "Example 4.1"),
    ("Example42Salesperson", "Example 4.2"),
    ("Example43DeviceLife", "Example 4.3"),
    ("ExpectationOfFunction", "Expected Value of g(X)"),
    ("Example44CarWash", "Example 4.4"),
    ("Example45FourXPlus3", "Example 4.5"),
    ("Example46TableXY", "Example 4.6"),
    ("Example47RatioYX", "Example 4.7"),
    ("VarianceAsSpread", "Variance"),
    ("Example48TwoCompanies", "Example 4.8"),
    ("Example49Defectives", "Example 4.9"),
    ("Example410WaterDemand", "Example 4.10"),
    ("Example411LinearDiscrete", "Example 4.11"),
    ("Example412LinearContinuous", "Example 4.12"),
    ("CovarianceSign", "Covariance"),
    ("CorrelationScale", "Correlation Coefficient"),
    ("Example413Covariance", "Example 4.13"),
    ("Example415Correlation", "Example 4.15"),
    ("LinearShiftScale", "Linear Combinations"),
    ("VarianceOfSum", "Variance of aX + bY"),
    ("Example417418Rework", "Examples 4.17, 4.18"),
    ("Example419ShiftSquare", "Example 4.19"),
    ("Example420Drink", "Example 4.20"),
    ("Example421Independent", "Example 4.21"),
    ("Example422423Variance", "Examples 4.22, 4.23"),
    ("ChebyshevBand", "Chebyshev's Theorem"),
    ("Example427Chebyshev", "Example 4.27"),
]

STEP_DEFAULT = 0.3      # week05 의 씬도 호흡 0.3–0.4, 단락 끝 0.5–2.0 (week04 와 같다)
STEP_AT = {}

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다. slides_ps1_03.py 와 같다."""
    step_at = STEP_DEFAULT
    skip_reversing = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, output_folder=SLIDES_DIR, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        super().wait(duration, *args, **kwargs)
        self._current_animation += 1
        if duration >= self.step_at:
            self.next_slide()


for _name, _title in PAGES:
    globals()[_name + "Slides"] = type(
        _name + "Slides", (_StepSlide, getattr(week05, _name)),
        {"__module__": __name__, "step_at": STEP_AT.get(_name, STEP_DEFAULT), "page_title": _title},
    )

if __name__ == "__main__":
    import json
    print(json.dumps([{"scene": n, "title": t} for n, t in PAGES], ensure_ascii=False, indent=1))
