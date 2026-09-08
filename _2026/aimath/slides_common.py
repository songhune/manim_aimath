# -*- coding: utf-8 -*-
"""AI기초수학 씬을 클릭 진행형 페이지로 바꾸는 공통 장치 (manim-slides + manimgl).

확률통계(`_2026/probstat/slides_ps1_02.py`)는 긴 `wait()` 마다 끊는다. 그 씬들은
단락마다 `wait()` 를 두고 쓰여 있어서 그렇게 해도 단계가 잘 나뉜다. AI기초수학 씬은
`wait()` 가 씬당 두세 번뿐이고 단계를 `play()` 로 나눈다. 같은 규칙을 쓰면 한 영상이
슬라이드 두 장이 되어 클릭할 것이 없다.

그래서 여기서는 `play()` 의 재생 시간을 쌓아 `min_step` 을 넘을 때 끊는다. 0.3~0.45초짜리
강조 동작(상자 치기 → 계산 → 성분 켜기)이 한 클릭씩 차지하지 않고 한 덩이로 묶인다.
긴 `wait()` 는 그것대로 경계로 삼는다. 씬 본문은 고치지 않는다.

    python tools/build_slides_site.py --chapter am_01 --module _2026/aimath/slides_am_01.py
"""
import os
from pathlib import Path

os.environ.setdefault("MANIM_API", "manimgl")

from manim_slides import Slide

SLIDES_DIR = Path(os.environ.get("SLIDES_DIR", "slides"))

MIN_STEP = 0.8      # play 재생 시간이 이만큼 쌓이면 다음 클릭으로 넘긴다
WAIT_STEP = 0.4     # 이 이상 멈추면 그 자리를 경계로 삼는다


def run_time_of(args, kwargs):
    """play 한 번의 재생 시간. 적지 않았으면 애니메이션이 들고 있는 값을 본다.

    묶음 판단에만 쓰므로 정확할 필요는 없다.

    Parameters
        args (tuple): play 에 넘긴 애니메이션들.
        kwargs (dict): play 에 넘긴 이름 붙은 인자들.

    Returns
        float: 초 단위 재생 시간.
    """
    given = kwargs.get("run_time")
    if given is not None:
        return float(given)
    times = []
    for animation in args:
        value = getattr(animation, "run_time", None)
        if value:
            times.append(float(value))
    if times:
        return max(times)
    return 1.0


class StepSlide(Slide):
    """동작 한 덩이마다 끊는다. 씬은 그대로 두고 play·wait 만 가로챈다.

    두 가지를 지킨다.

    1. **wait 도 한 동작으로 센다.** manimgl 은 `wait()` 에도 부분 영상 파일을 하나
       만드는데(`num_plays` 로 번호를 매긴다), manim-slides 의 `_current_animation` 은
       `play()` 에서만 올라간다. 그대로 두면 첫 `wait()` 뒤부터 슬라이드마다 한 칸씩
       밀린 영상이 붙는다. 그래서 여기서 직접 맞춰 준다.
    2. **끊는 자리는 다음 play 직전이다.** 재생이 끝난 자리에서 끊으면 뒤따르는
       `wait()` 가 다음 슬라이드의 앞머리로 가서, 클릭하자마자 앞 장면의 정지 화면을
       몇 초 보게 된다. 한 박자 미뤄 끊으면 멈춤이 제 슬라이드에 남는다.
    """
    min_step = MIN_STEP
    wait_step = WAIT_STEP
    skip_reversing = True            # RevealJS 는 역재생 파일을 쓰지 않는다

    def __init__(self, *args, **kwargs):
        super().__init__(*args, output_folder=SLIDES_DIR, **kwargs)
        self._step_acc = 0.0

    def play(self, *args, **kwargs):
        if self._step_acc >= self.min_step:
            self.next_slide()
            self._step_acc = 0.0
        super().play(*args, **kwargs)
        self._step_acc += run_time_of(args, kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        super().wait(duration, *args, **kwargs)
        self._current_animation += 1
        if duration >= self.wait_step:
            self._step_acc = self.min_step      # 다음 play 앞에서 끊는다


def build(namespace, pages, modules, step_at=None):
    """PAGES 의 씬마다 `<이름>Slides` 클래스를 만들어 모듈에 넣는다.

    Parameters
        namespace (dict): 부르는 모듈의 globals().
        pages (list): (씬 이름, 화면 제목) 의 목록.
        modules (tuple): 씬을 찾을 모듈들.
        step_at (dict): 씬별 min_step 덮어쓰기. 단계가 잘게 나뉘면 올린다.

    Returns
        list: 넘겨받은 pages 그대로.
    """
    step_at = step_at or {}
    for name, title in pages:
        base = None
        for module in modules:
            if hasattr(module, name):
                base = getattr(module, name)
                break
        if base is None:
            raise KeyError("씬을 찾지 못함: %s" % name)
        namespace[name + "Slides"] = type(
            name + "Slides", (StepSlide, base),
            {"__module__": namespace["__name__"],
             "min_step": step_at.get(name, MIN_STEP),
             "page_title": title},
        )
    return pages
