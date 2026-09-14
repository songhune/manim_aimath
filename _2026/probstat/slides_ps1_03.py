# -*- coding: utf-8 -*-
"""PS1_03 (Walpole Chapter 3) 영상 19편의 클릭 진행형 판 (manim-slides + manimgl).

slides_ps1_02.py 와 같은 장치다. week04.py 의 씬을 그대로 상속하고, `wait()` 가 임계값(기본 0.5초)
이상이면 그 자리를 슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    python tools/build_slides_site.py --chapter ps1_03 --module _2026/probstat/slides_ps1_03.py

PAGES 의 순서는 덱(insert_videos.py 의 PS1_03_INSERT)과 같다. 제목은 각 씬의 slide_title 문구다.
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat import week04

# (씬 이름, 화면 제목). 덱 순서.
PAGES = [
    ("RandomVariableAsFunction", "Random Variable"),
    ("DiscreteVsContinuous", "Discrete, Continuous"),
    ("PmfAsBars", "Probability Mass Function"),
    ("Example38Laptops", "Example 3.8"),
    ("Example32Helmets", "Example 3.2"),
    ("Example310Cdf", "Example 3.10"),
    ("PdfAsArea", "Probability Density Function"),
    ("Example311Temperature", "Example 3.11"),
    ("Example312Cdf", "Example 3.12"),
    ("Example313Bid", "Example 3.13"),
    ("JointDistributionGrid", "Joint Probability Distribution"),
    ("Example314Pens", "Example 3.14"),
    ("Example315DriveIn", "Example 3.15"),
    ("MarginalAsRowSums", "Marginal Distributions"),
    ("ConditionalDistributionSlice", "Conditional Distribution"),
    ("Example319Spectrum", "Example 3.19"),
    ("Example320Rectangle", "Example 3.20"),
    ("IndependenceProductCheck", "Statistical Independence"),
    ("Example322ShelfLife", "Example 3.22"),
]

STEP_DEFAULT = 0.3      # week04 의 씬은 호흡 0.3–0.4, 단락 끝 0.5–2.0 이라 0.5 로 끊으면 한두 단계뿐이다 (2026-09-14)
STEP_AT = {}

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다. slides_ps1_02.py 와 같다."""
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
        _name + "Slides", (_StepSlide, getattr(week04, _name)),
        {"__module__": __name__, "step_at": STEP_AT.get(_name, STEP_DEFAULT), "page_title": _title},
    )

if __name__ == "__main__":
    import json
    print(json.dumps([{"scene": n, "title": t} for n, t in PAGES], ensure_ascii=False, indent=1))
