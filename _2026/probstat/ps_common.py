# -*- coding: utf-8 -*-
"""확률과통계 씬이 함께 쓰는 서체·색·마스코트·도우미.

week00 ~ week02 가 각자 들고 있던 상수와 함수를 한 곳으로 모은 것이다.

화면 문구 규칙 (하네스 3.6):
    화면에 뜨는 글자는 짧은 명사구나 수식이다. 문장으로 설명하는 몫은 교안의
    대본이 맡는다. `label()` 은 6단어를 넘으면 예외를 낸다. 넘겨야 할 만큼
    설명이 길다면 그 설명은 화면이 아니라 대본으로 가야 한다는 뜻이다.
"""
from manim_imports_ext import *

import os.path as _osp


# ─────────────────────────────────────────────────────────────
# 서체와 색 — 강의자료(아주대 템플릿)와 맞춘다.
# ─────────────────────────────────────────────────────────────
TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"

INK = GREY_A          # 본문
ACCENT = BLUE_B       # 강조
WARN = RED_C          # 주의·극단값
CALM = TEAL_B         # 보조 강조
MUTED = GREY_C        # 배경으로 물러난 것
MEAN_COLOR = YELLOW
MED_COLOR = TEAL_B

# 치토 색이름 → 문구·도형에 쓸 색. 같은 무리는 같은 색으로 묶는다.
TINT_COLOR = {
    None: ACCENT,
    "teal": CALM,
    "red": WARN,
    "gold": MEAN_COLOR,
    "grey": MUTED,
}


# ─────────────────────────────────────────────────────────────
# 마스코트 '치토'
#
# 낱장과 생성 스크립트는 강의 폴더 쪽에 있다:
#   2026-2/확률과통계/이미지/치토/   (README.md · extract_chito.py · tint_chito.py)
# 검은 배경에서는 남색 외곽선이 묻히므로 밝은 테두리를 덧댄 `_outline` 판을 쓴다.
# 이 파일: 2026-2/manim_songhune/_2026/probstat/ps_common.py
# ─────────────────────────────────────────────────────────────
ASSET_DIR = _osp.join(
    _osp.abspath(_osp.join(_osp.dirname(__file__), "..", "..", "..")),
    "확률과통계", "이미지", "치토",
)


def chito(pose="front", tint=None, height=0.42):
    """치토 한 마리. pose 는 front/back, tint 는 None/teal/red/gold/grey.

    앞뒤로 무리를 나누면 색맹 여부와 무관하게 구분되고, 색으로 나누면 멀리서도
    구분된다. 둘을 겹쳐 쓰면 강의실 뒷자리에서도 읽힌다.
    """
    name = "chito_%s%s_outline.png" % (pose, "_" + tint if tint else "")
    path = _osp.join(ASSET_DIR, name)
    if not _osp.exists(path):
        raise FileNotFoundError(
            "마스코트 이미지가 없다: %s\n"
            "확률과통계/이미지/치토/ 에서 extract_chito.py 와 tint_chito.py 를 "
            "차례로 실행할 것." % path
        )
    return ImageMobject(path, height=height)


def crowd(n, rows, cols, pose="front", tint=None, height=0.42, buff=0.16,
          jitter=0.035, seed=0):
    """치토 n 마리를 격자로 세운다. 줄이 너무 반듯하면 무리로 보이지 않으므로
    아주 조금 흔들어 둔다."""
    rng = np.random.default_rng(seed)
    g = Group(*[chito(pose, tint, height) for _ in range(n)])
    g.arrange_in_grid(rows, cols, buff=buff)
    if jitter:
        for m in g:
            m.shift(rng.uniform(-jitter, jitter, 3) * np.array([1, 1, 0]))
    return g


def restyle(mob, pose=None, tint=None):
    """이미 놓인 치토를 같은 자리·같은 크기로 다른 판으로 갈아 끼운다.

    ImageMobject 는 색을 못 바꾸므로 뒷모습으로 돌리거나 색을 바꾸려면 새 이미지가
    필요하다. 자리와 높이를 그대로 물려주어 제자리에서 바뀐 것처럼 보이게 한다.
    """
    pose = pose or getattr(mob, "ps_pose", "front")
    new = chito(pose, tint, mob.get_height())
    new.move_to(mob)
    new.ps_pose, new.ps_tint = pose, tint
    return new


def swap_pose(scene, mobs, pose=None, tint=None, run_time=1.0, scale=1.1):
    """무리의 일부를 제자리에서 다른 판으로 바꾼다. 바뀐 것들을 Group 으로 돌려준다.

    ImageMobject 는 Transform 으로 그림이 바뀌지 않는다(점만 보간되고 텍스처는
    원본 그대로다). 옛 판을 지우고 새 판을 같은 자리에 띄운다.
    """
    fresh = Group(*[chito(pose or getattr(m, "ps_pose", "front"), tint,
                          m.get_height()).move_to(m) for m in mobs])
    scene.play(
        *[FadeOut(m, scale=1 / scale) for m in mobs],
        *[FadeIn(f, scale=scale) for f in fresh],
        run_time=run_time,
    )
    for f in fresh:
        f.ps_pose, f.ps_tint = pose, tint
    return fresh


def ring(mob, color=ACCENT, buff=0.045, width=3):
    """개체 하나를 감싸는 둥근 테두리. '이건 뽑혔다' 는 표시."""
    r = SurroundingRectangle(mob, buff=buff)
    return r.set_stroke(color, width).round_corners(0.08)


def panel(mob, color=GREY_C, buff=0.28, width=2):
    """무리 하나를 감싸는 둥근 상자."""
    r = SurroundingRectangle(mob, buff=buff)
    return r.set_stroke(color, width).round_corners(0.15)


# ─────────────────────────────────────────────────────────────
# 글자 — 짧게
# ─────────────────────────────────────────────────────────────
MAX_WORDS = 6


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def label(text, size=30, color=INK, _check=True):
    """화면 문구. 명사구나 짧은 구절만 받는다.

    문장을 넣으려다 걸리면 그 문장은 교안 대본으로 옮기고, 화면에는 그 문장이
    가리키는 대상만 남긴다. 숫자가 든 문구는 단어 수를 세지 않는다.
    """
    if _check:
        # 숫자가 든 낱말은 세지 않는다. `n = 22` 나 `24/40 = 60%` 는 이름이지 문장이 아니다.
        # 문구 전체를 숫자 하나로 봐주면 "…on a scale from 0 to 1" 같은 문장이 빠져나간다.
        words = [w for w in text.replace("—", " ").split()
                 if w and not any(c.isdigit() for c in w)]
        if len(words) > MAX_WORDS:
            raise ValueError(
                "화면 문구가 %d단어다 (최대 %d): %r\n"
                "설명은 교안 대본으로 옮기고 화면에는 이름만 남길 것."
                % (len(words), MAX_WORDS, text)
            )
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def note(text, size=24, color=GREY_B):
    """보조 문구. 축 이름·단위·출처처럼 읽지 않아도 되는 것."""
    return label(text, size, color)


def slide_title(text):
    """왼쪽 위 제목 + 밑줄. 강의 슬라이드 제목 위치와 맞춘다."""
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def under(text, ref, color=INK, size=28):
    """참조 도형 바로 아래에 놓는 문구."""
    return label(text, size, color).next_to(ref, DOWN, buff=0.45)


def swap(scene, old, new, run_time=0.4):
    """같은 자리의 문구를 갈아 끼운다.

    FadeOut 과 FadeIn 을 한 play 에 넣으면 두 글자가 반투명으로 겹쳐 뭉개진다.
    두 번에 나누어 재생한다.
    """
    scene.play(FadeOut(old), run_time=run_time)
    scene.play(FadeIn(new), run_time=run_time)


# ─────────────────────────────────────────────────────────────
# 숫자와 움직임
# ─────────────────────────────────────────────────────────────
def counter(tracker, fmt=int, color=MEAN_COLOR, size=48, places=0):
    """트래커를 따라가는 숫자.

    `.animate.set_value` 는 글리프 자체를 보간해서 획이 뭉개진다. 트래커를 두고
    `f_always.set_value` 로 따라가게 한다. 자리 고정은 왼쪽이라 숫자가 오른쪽으로
    늘어나므로, 이름은 숫자의 왼쪽에 둔다.
    """
    num = (Integer(0) if fmt is int else DecimalNumber(0, num_decimal_places=places))
    num.set_color(color).scale(size / 48)
    if fmt is int:
        num.f_always.set_value(lambda: int(tracker.get_value()))
    else:
        num.f_always.set_value(tracker.get_value)
    return num


def freeze(*mobs):
    """따라가기를 멈춘다.

    `counter()` 가 만든 숫자는 매 프레임 글리프를 다시 만든다. 그 상태로 FadeOut
    이나 .animate 를 걸면 애니메이션이 붙잡아 둔 사본과 점 개수가 어긋나
    broadcast 오류가 난다. 사라뜨리거나 옮기기 전에 이걸 먼저 부른다.
    """
    for m in mobs:
        m.clear_updaters()
    return mobs[0] if len(mobs) == 1 else mobs


def named_counter(name, tracker, **kwargs):
    """이름 + 숫자. 숫자가 늘어나도 이름을 밀지 않는다."""
    tag = note(name, 26)
    num = counter(tracker, **kwargs)
    num.next_to(tag, RIGHT, buff=0.25, aligned_edge=DOWN)
    return Group(tag, num)


def sweep(scene, targets, color=CALM, run_time=2.0, from_edge=None):
    """무리를 훑는 동작. 조사·측정·검사처럼 '전부 한 번씩 봤다' 는 사건을 보인다.

    참고: legacy/_2020/med_test.py 의 scan_lines.
    """
    origin = from_edge if from_edge is not None else FRAME_HEIGHT * DOWN / 2
    lines = VGroup(*[
        Line(origin, m.get_center(), stroke_width=1,
             stroke_color=interpolate_color(color, WHITE, random.random() * 0.6))
        for m in targets
    ])
    scene.play(LaggedStartMap(ShowCreationThenFadeOut, lines,
                              lag_ratio=1 / max(len(lines), 1), run_time=run_time))


def bar(value, vmax, width=0.9, height=4.0, color=ACCENT, opacity=0.85):
    """아래에서 자라는 막대 하나."""
    r = Rectangle(width=width, height=max(height * value / vmax, 1e-3))
    r.set_fill(color, opacity).set_stroke(color, 2)
    return r
