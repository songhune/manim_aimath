# -*- coding: utf-8 -*-
"""PS1_02 (Walpole Chapter 2) 영상 26편의 클릭 진행형 판 (manim-slides + manimgl).

한 영상 안에서 동작 단위마다 멈췄다가 클릭(→ / 스페이스)으로 다음 단위로 넘어간다.
week02.py·week03.py 의 씬을 그대로 상속하고, `wait()` 가 임계값(기본 0.5초) 이상이면 그 자리를
슬라이드 경계(`next_slide`)로 삼는다. 씬 본문은 고치지 않는다.

    # 빌드(렌더 → 변환 → 목차)는 tools/build_slides_site.py 가 한다.
    python tools/build_slides_site.py --chapter ps1_02 --module _2026/probstat/slides_ps1_02.py

    # 한 씬만 손으로
    MANIM_API=manimgl PYTHONPATH=.:legacy SLIDES_DIR=$TMPDIR/manim_songhune_slides/slides \
      manim-slides render --GL _2026/probstat/slides_ps1_02.py AdditionRuleSlides --hd
    manim-slides convert --folder $SLIDES_DIR --one-file --offline AdditionRuleSlides docs/ps1_02/AdditionRule.html

PAGES 의 순서는 덱(insert_videos.py 의 PS1_02 job)과 같다. 제목은 각 씬의 slide_title 문구다.
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

from _2026.probstat import week02, week03

# (씬 이름, 화면 제목). 덱 순서.
PAGES = [
    ("SampleSpace", "Sample Space"),
    ("EventsAndSetOps", "Events and Set Operations"),
    ("MultiplicationRule", "The Multiplication Rule"),
    ("Example213Dice", "Example 2.13"),
    ("Example215Club", "Example 2.15"),
    ("Example217EvenNumbers", "Example 2.17"),
    ("Permutations", "Permutations"),
    ("Combinations", "Combinations"),
    ("Example218Awards", "Example 2.18"),
    ("Example222Cartridges", "Example 2.22"),
    ("ProbabilityOfEvent", "Probability of an Event"),
    ("Example225LoadedDie", "Example 2.25"),
    ("Example228Poker", "Example 2.28"),
    ("AdditionRule", "Additive Rules"),
    ("Example229Jobs", "Example 2.29"),
    ("Example233Cable", "Example 2.33"),
    ("ConditionalProbability", "Conditional Probability"),
    ("Example234Flights", "Example 2.34"),
    ("Independence", "Independent Events"),
    ("ProductRule", "The Product Rule"),
    ("Example236Fuses", "Example 2.36"),
    ("Example238Emergency", "Example 2.38"),
    ("TotalProbability", "Total Probability"),
    ("Example241Machines", "Example 2.41"),
    ("BayesRule", "Bayes' Rule"),
    ("Example242Bayes", "Example 2.42"),
]

# 씬별 경계 임계값(초). 적지 않으면 STEP_DEFAULT. 단계가 너무 잘게 나뉘면 올리고, 한 덩어리면 내린다.
# 씬의 wait 는 호흡 0.3–0.4, 단락 끝 0.5–2.0 으로 쓰여 있어 0.5 가 단락 경계와 맞는다(정적 집계로 확인).
STEP_DEFAULT = 0.5
STEP_AT = {"Example218Awards": 0.4}     # 상 하나 줄 때마다 wait(0.4) 뿐이라 거기서 끊는다

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))


class _StepSlide(Slide):
    """긴 wait 마다 슬라이드를 끊는다. 짧은 wait(호흡)는 그대로 둔다."""
    step_at = STEP_DEFAULT
    skip_reversing = True                    # RevealJS 는 역재생 파일을 쓰지 않는다

    def __init__(self, *args, **kwargs):
        super().__init__(*args, output_folder=SLIDES_DIR, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        super().wait(duration, *args, **kwargs)
        if duration >= self.step_at:
            self.next_slide()


def _scene(name):
    for mod in (week02, week03):
        if hasattr(mod, name):
            return getattr(mod, name)
    raise KeyError(name)


for _name, _title in PAGES:
    globals()[_name + "Slides"] = type(
        _name + "Slides", (_StepSlide, _scene(_name)),
        {"__module__": __name__, "step_at": STEP_AT.get(_name, STEP_DEFAULT), "page_title": _title},
    )

if __name__ == "__main__":
    import json
    print(json.dumps([{"scene": n, "title": t} for n, t in PAGES], ensure_ascii=False, indent=1))
