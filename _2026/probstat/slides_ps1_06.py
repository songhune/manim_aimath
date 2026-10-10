# -*- coding: utf-8 -*-
"""PS1_06 (Walpole Chapter 6) 영상 14편의 클릭 진행형 판 (manim-slides + manimgl).

slides_ps1_05.py 와 같은 장치다. week07.py 의 씬을 그대로 상속하고, `wait()` 가 임계값(기본 0.3초)
이상이면 그 자리를 슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    python tools/build_slides_site.py --chapter ps1_06 --module _2026/probstat/slides_ps1_06.py

PAGES 의 순서는 덱(insert_videos.py 의 PS1_06_INSERT)과 같다. 제목은 각 씬의 slide_title 문구다.
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat import week07

# (씬 이름, 화면 제목). 덱 순서. 12차 10/16 은 Example615Recovery 까지, 13차 10/27 은 GammaFamily 부터.
PAGES = [
    ("UniformDensity", "Continuous Uniform Distribution"),
    ("NormalCurveShape", "Normal Distribution"),
    ("StandardizeToZ", "Areas under the Normal Curve"),
    ("Example62TableA3", "Example 6.2"),
    ("Example67Battery", "Example 6.7"),
    ("Example69Bearings", "Example 6.9"),
    ("Example613Grades", "Example 6.13"),
    ("NormalApproximatesBinomial", "Normal Approximation to the Binomial"),
    ("Example615Recovery", "Example 6.15"),
    ("GammaFamily", "Gamma Distribution"),
    ("PoissonToExponential", "Poisson Process and Exponential"),
    ("MemorylessExponential", "Memoryless Property"),
    ("Example618Calls", "Example 6.18"),
    ("LognormalFromNormal", "Lognormal Distribution"),
]

STEP_DEFAULT = 0.3      # week07 의 씬도 호흡 0.3–0.4, 단락 끝 0.5–2.0 (week06 과 같다)
STEP_AT = {}

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다. slides_ps1_05.py 와 같다."""
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
        _name + "Slides", (_StepSlide, getattr(week07, _name)),
        {"__module__": __name__, "step_at": STEP_AT.get(_name, STEP_DEFAULT), "page_title": _title},
    )

if __name__ == "__main__":
    import json
    print(json.dumps([{"scene": n, "title": t} for n, t in PAGES], ensure_ascii=False, indent=1))
