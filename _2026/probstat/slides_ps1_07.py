# -*- coding: utf-8 -*-
"""PS1_07 (Walpole Chapter 7) 영상 4편의 클릭 진행형 판 (manim-slides + manimgl).

slides_ps1_06.py 와 같은 장치다. week07b.py 의 씬을 그대로 상속하고, `wait()` 가 임계값(기본 0.3초)
이상이면 그 자리를 슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    python tools/build_slides_site.py --chapter ps1_07 --module _2026/probstat/slides_ps1_07.py

PAGES 의 순서는 덱(insert_videos.py 의 PS1_07_INSERT)과 같다. 제목은 각 씬의 slide_title 문구다.
개념 영상 네 편 + 적분이 있는 예제 영상 네 편(7.3 · 7.4 · 7.5 · 7.7, 2026-11-05 저녁)이다. 7장 씬 파일은 week07b.py 다(week07.py 는 6장).
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat import week07b

# (씬 이름, 화면 제목). 덱 순서.
PAGES = [
    ("DiscreteTransformation", "Transformation of a Discrete Variable"),
    ("JacobianStretch", "Jacobian of a Transformation"),
    ("Example73Linear", "Example 7.3"),
    ("Example74Jacobian2D", "Example 7.4"),
    ("NotOneToOne", "Transformation That Is Not One-to-One"),
    ("Example75ChiSquare", "Example 7.5"),
    ("MomentGeneratingFunction", "Moment-Generating Function"),
    ("Example77NormalMGF", "Example 7.7"),
]

STEP_DEFAULT = 0.3      # week07b 의 씬도 호흡 0.3–0.5, 단락 끝 0.8–3.0 (week07 과 같다)
STEP_AT = {}

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다. slides_ps1_06.py 와 같다."""
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
        _name + "Slides", (_StepSlide, getattr(week07b, _name)),
        {"__module__": __name__, "step_at": STEP_AT.get(_name, STEP_DEFAULT), "page_title": _title},
    )

if __name__ == "__main__":
    import json
    print(json.dumps([{"scene": n, "title": t} for n, t in PAGES], ensure_ascii=False, indent=1))
