"""확률과통계 오리엔테이션 — 강의개요 보조자료.

수업안 `확통_00_오리엔테이션.pptx` 강의개요(확률과 통계가 주는 통찰)에 삽입한다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/probstat/week00.py
    ./render.sh check _2026/probstat/week00.py
    ./render.sh ppt   _2026/probstat/week00.py MontyHall
"""
from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN, BODY_FONT, TITLE_FONT,
    chito, counter, freeze, label, note, panel, ring, slide_title, swap, title,
)


def body(text, size=30, color=INK):
    """화면 문구. ps_common.label 과 같고, 길면 예외를 낸다."""
    return label(text, size, color)


# ─────────────────────────────────────────────────────────────
# 1. 몬티 홀 문제 — 조건부확률(사후 확률) 도입
# ─────────────────────────────────────────────────────────────
class MontyHall(InteractiveScene):
    """오리엔테이션 강의개요. 문을 바꾸면 당첨 확률이 1/3에서 2/3으로 오른다.

    직관과 어긋나는 결과가 조건부확률로 설명된다는 것을 보여 준다.
    답의 유도는 3주차 베이즈 정리에서 다룬다.
    """

    def construct(self):
        head = slide_title("The Monty Hall Problem")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        # ── 문 세 개
        doors = VGroup()
        for i in range(3):
            panel = RoundedRectangle(width=2.0, height=2.9, corner_radius=0.12)
            panel.set_stroke(GREY_B, 3).set_fill(GREY_E, 1)
            num = Text(str(i + 1), font=TITLE_FONT, font_size=40).set_color(GREY_A)
            num.move_to(panel)
            doors.add(VGroup(panel, num))
        doors.arrange(RIGHT, buff=1.1).move_to(UP * 0.35)

        rule = body("one car, two goats", 28)
        rule.next_to(doors, DOWN, buff=0.6)
        self.play(LaggedStartMap(FadeIn, doors, lag_ratio=0.15), FadeIn(rule))
        self.wait(0.6)

        # ── 1번 문을 고른다
        pick = SurroundingRectangle(doors[0], buff=0.08)
        pick.set_stroke(ACCENT, 4).round_corners(0.15)
        pick_label = body("chosen", 24, ACCENT).next_to(doors[0], UP, buff=0.15)
        self.play(ShowCreation(pick), FadeIn(pick_label))
        self.wait(0.6)

        # ── 사회자가 3번 문을 연다: 염소
        goat = body("goat", 30, WARN).move_to(doors[2])
        self.play(
            doors[2][0].animate.set_fill(BLACK, 1),
            FadeOut(doors[2][1]),
            FadeIn(goat),
        )
        host = body("host opens a goat", 26, GREY_B)
        host.next_to(rule, DOWN, buff=0.25)
        self.play(FadeIn(host))
        self.wait(0.8)

        # ── 질문
        q = body("switch or stay?", 34, MEAN_COLOR)
        q.next_to(host, DOWN, buff=0.35)
        self.play(FadeIn(q, UP))
        self.wait(1.0)

        # ── 확률 비교 막대
        self.play(FadeOut(rule), FadeOut(host), FadeOut(q))

        base = 4.8
        stay_t = body("stay", 26).move_to(LEFT * 4.0 + DOWN * 1.9)
        sw_t = body("switch", 26).move_to(LEFT * 4.0 + DOWN * 2.7)

        bar_stay = Rectangle(width=base / 3, height=0.5)
        bar_stay.set_stroke(width=0).set_fill(GREY_C, 1)
        bar_stay.next_to(stay_t, RIGHT, buff=0.45)

        bar_sw = Rectangle(width=base * 2 / 3, height=0.5)
        bar_sw.set_stroke(width=0).set_fill(ACCENT, 1)
        bar_sw.next_to(sw_t, RIGHT, buff=0.45)

        p_stay = Tex(R"\tfrac{1}{3}").set_color(GREY_A)
        p_stay.next_to(bar_stay, RIGHT, buff=0.3)
        p_sw = Tex(R"\tfrac{2}{3}").set_color(ACCENT)
        p_sw.next_to(bar_sw, RIGHT, buff=0.3)

        self.play(FadeIn(stay_t), GrowFromEdge(bar_stay, LEFT))
        self.play(Write(p_stay))
        self.play(FadeIn(sw_t), GrowFromEdge(bar_sw, LEFT))
        self.play(Write(p_sw))

        # 선택 테두리를 2번 문으로 옮겨 '변경'을 보여 준다
        pick2 = SurroundingRectangle(doors[1], buff=0.08)
        pick2.set_stroke(ACCENT, 4).round_corners(0.15)
        self.play(
            Transform(pick, pick2),
            pick_label.animate.next_to(doors[1], UP, buff=0.15),
        )

        infer = VGroup(
            Tex(R"P(\text{car in }2 \mid \text{host opened }3)").set_color(MEAN_COLOR).scale(0.8),
            note("Chapter 2", 22),
        ).arrange(RIGHT, buff=0.45)   # 세로로 쌓으면 아래 줄이 화면 밖으로 나간다
        # 막대 무리 아래에 붙인다. to_edge 로 내리면 'switch' 막대와 겹치고,
        # 여백을 더 주면 'Chapter 2' 가 화면 밖으로 밀린다.
        infer.next_to(VGroup(bar_stay, bar_sw, sw_t, p_sw), DOWN, buff=0.35).set_x(0)
        self.play(FadeIn(infer, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 확률의 두 얼굴 ① 빈도 — 반복하면 비율이 자리를 잡는다
# ─────────────────────────────────────────────────────────────
class FrequencyView(InteractiveScene):
    """오리엔테이션 강의개요, 보충 대본 `01주차_보충_빈도vs믿음_말하기대본.md` 1절.

    동전을 계속 던지면 앞면 비율이 1/2 에 다가간다. 확률을 '아주 많이 반복했을
    때의 비율'로 읽는 관점이다. 이어서 그 관점의 한계 — 내일은 반복할 수 없다 —
    를 못 박아 2절(믿음 관점)로 넘긴다.
    """
    n_flips = 400
    seed = 7

    def construct(self):
        head = slide_title("Two Readings of Probability: Frequency")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        claim = body("“The probability of heads is 1/2.”", 30, CALM)
        claim.next_to(head[1], DOWN, buff=0.35)
        self.play(FadeIn(claim, UP))
        self.wait(0.5)

        reading = body("proportion over many tosses", 28)
        reading.next_to(claim, DOWN, buff=0.25)
        self.play(FadeIn(reading))
        self.wait(0.5)

        # ── 앞면 비율의 누적 그래프
        axes = Axes(
            x_range=(0, self.n_flips, 100),
            y_range=(0, 1, 0.5),
            width=9.0, height=3.4,
            axis_config=dict(stroke_width=2),
        )
        axes.next_to(reading, DOWN, buff=0.55).shift(RIGHT * 0.4)
        axes.x_axis.add_numbers(range(100, self.n_flips + 1, 100), font_size=20)

        half = DashedLine(axes.c2p(0, 0.5), axes.c2p(self.n_flips, 0.5))
        half.set_stroke(MEAN_COLOR, 3)
        half_tag = Tex(R"\tfrac{1}{2}").set_color(MEAN_COLOR)
        half_tag.next_to(half, LEFT, buff=0.2)

        x_tag = body("number of tosses", 22, GREY_B).next_to(axes.x_axis, DOWN, buff=0.15)
        y_tag = body("proportion of heads", 22, GREY_B).next_to(axes.y_axis, UP, buff=0.15)

        self.play(ShowCreation(axes), FadeIn(x_tag), FadeIn(y_tag))
        self.play(ShowCreation(half), FadeIn(half_tag))

        rng = np.random.default_rng(self.seed)
        heads = rng.integers(0, 2, self.n_flips)
        props = np.cumsum(heads) / np.arange(1, self.n_flips + 1)

        walk = ValueTracker(2.0)   # 지금까지 던진 횟수 (2회부터 그린다)

        def flips_so_far():
            return int(np.clip(walk.get_value(), 2, self.n_flips))

        def make_path():
            k = flips_so_far()
            pts = [axes.c2p(i + 1, props[i]) for i in range(k)]
            return VMobject().set_points_as_corners(pts).set_stroke(ACCENT, 3)

        path = always_redraw(make_path)

        # 숫자는 왼쪽 모서리를 고정한 채 자릿수가 늘어난다. 그래서 이름표를
        # 왼쪽에 두고 숫자를 오른쪽에 두어, 늘어나는 쪽을 여백으로 보낸다.
        counter = VGroup(
            body("tosses", 24, GREY_B),
            Integer(2).set_color(INK),
        )
        counter.arrange(RIGHT, buff=0.25)
        counter[1].f_always.set_value(flips_so_far)

        ratio = VGroup(
            body("proportion", 24, ACCENT),
            DecimalNumber(0.5, num_decimal_places=3).set_color(ACCENT),
        )
        ratio.arrange(RIGHT, buff=0.25)
        ratio[1].f_always.set_value(lambda: float(props[flips_so_far() - 1]))

        readout = VGroup(counter, ratio)
        readout.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        readout.move_to(axes.c2p(self.n_flips, 0.88), RIGHT)   # 그래프 오른쪽 위 빈 자리

        self.add(path, readout)
        self.play(
            walk.animate.set_value(self.n_flips),
            run_time=6, rate_func=linear,
        )
        self.wait(0.8)

        settle = VGroup(
            body("law of large numbers", 28, ACCENT),
            note("Chapter 8", 22),
        ).arrange(DOWN, buff=0.15)
        settle.next_to(axes, DOWN, buff=0.35)
        self.play(FadeIn(settle, UP))
        self.wait(1.2)

        # ── 한계: 반복할 수 없는 사건
        self.play(
            *[FadeOut(m) for m in [claim, reading, axes, half, half_tag,
                                   x_tag, y_tag, path, readout, settle]]
        )

        claim2 = body("“The probability of rain tomorrow is 70%.”", 32, WARN)
        ask = body("repeat tomorrow 10,000 times?", 28)
        limit = VGroup(
            body("tomorrow happens once", 30, MEAN_COLOR),
            body("no repetition, no proportion", 30, MEAN_COLOR),
        ).arrange(DOWN, buff=0.2)

        VGroup(claim2, ask, limit).arrange(DOWN, buff=0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(claim2, UP))
        self.play(FadeIn(ask))
        self.wait(0.8)

        cross = Line(ask.get_left(), ask.get_right()).set_stroke(WARN, 5)
        self.play(ShowCreation(cross))

        self.play(FadeIn(limit, UP))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 확률의 두 얼굴 ② 믿음 — 데이터가 확신을 갱신한다
# ─────────────────────────────────────────────────────────────
class BeliefUpdate(InteractiveScene):
    """오리엔테이션 강의개요, 보충 대본 2–3절.

    스팸 필터 하나로 사전확률 → 데이터 → 사후확률을 보여 준다.
    베이즈 정리의 공식은 3주차에 다룬다. 여기서는 구조만 남긴다.
    """
    prior = 0.20
    posterior = 0.95

    def construct(self):
        head = slide_title("Two Readings of Probability: Belief")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        claim = body("degree of belief", 34, CALM)
        claim.next_to(head[1], DOWN, buff=0.35)
        self.play(FadeIn(claim, UP))
        self.wait(0.5)

        # ── 확신 막대 (0 ~ 1)
        scale_line = NumberLine(
            x_range=(0, 1, 0.5), width=9.0,
            decimal_number_config=dict(num_decimal_places=1),
            include_numbers=True,
        )
        scale_line.move_to(DOWN * 2.2)

        belief = ValueTracker(self.prior)

        track = Rectangle(width=9.0, height=0.55)
        track.set_style(fill_color=GREY_E, fill_opacity=1, stroke_color=GREY_C,
                        stroke_width=2)
        track.next_to(scale_line, UP, buff=0.15)

        fill = Rectangle(height=0.55, width=1.0)
        fill.set_style(fill_color=ACCENT, fill_opacity=0.85, stroke_width=0)

        def resize_fill(m):
            m.set_width(max(9.0 * belief.get_value(), 1e-3), stretch=True)
            m.move_to(track.get_left(), LEFT)

        fill.add_updater(resize_fill)

        pct = VGroup(
            DecimalNumber(self.prior * 100, num_decimal_places=0).set_color(MEAN_COLOR),
            body("%", 28, MEAN_COLOR),
        )
        pct.arrange(RIGHT, buff=0.08)
        pct[0].f_always.set_value(lambda: belief.get_value() * 100)
        pct.add_updater(lambda m: m.next_to(track, UP, buff=0.4))

        self.play(ShowCreation(scale_line), FadeIn(track))
        self.add(fill, pct)
        self.wait(0.3)

        step1 = body("prior", 30, INK)
        step1.next_to(claim, DOWN, buff=0.5)
        self.play(FadeIn(step1))
        self.wait(1.0)

        # ── 데이터가 도착한다
        mail = RoundedRectangle(width=4.2, height=1.4, corner_radius=0.1)
        mail.set_stroke(GREY_B, 3).set_fill(GREY_E, 1)
        flap_tip = mail.get_center() + UP * 0.1
        flap = VGroup(
            Line(mail.get_corner(UL), flap_tip),
            Line(mail.get_corner(UR), flap_tip),
        ).set_stroke(GREY_B, 3)
        words = VGroup(*[body(w, 22, WARN) for w in ["free", "winner", "click now"]])
        words.arrange(RIGHT, buff=0.35)
        words.move_to(mail.get_bottom() + UP * 0.45)
        envelope = VGroup(mail, flap, words)
        envelope.next_to(step1, DOWN, buff=0.25)

        # 영문 문구가 길어 봉투 좌우에 놓으면 화면을 넘는다. 한 자리에서 갈아 끼운다.
        step2 = body("new data", 30, WARN)
        step2.move_to(step1)

        self.play(FadeOut(step1), run_time=0.4)
        self.play(FadeIn(step2), run_time=0.4)
        self.play(FadeIn(mail), ShowCreation(flap))
        self.play(LaggedStartMap(FadeIn, words, lag_ratio=0.25))
        self.wait(0.6)

        step3 = body("posterior", 30, MEAN_COLOR)
        step3.move_to(step2)
        self.play(FadeOut(step2), run_time=0.4)
        self.play(FadeIn(step3), run_time=0.4)
        self.play(
            belief.animate.set_value(self.posterior),
            fill.animate.set_color(MEAN_COLOR),
            run_time=2,
        )
        self.wait(1.0)

        # ── 구조만 남긴다. fill 과 pct 는 track 을 따라오므로 같이 올라간다.
        self.play(
            *[FadeOut(m) for m in [claim, step3, envelope]],
            VGroup(track, scale_line).animate.shift(UP * 2.0),
        )
        self.bring_to_front(fill, pct)   # track 을 다시 play 에 넘기면 fill 위로 올라온다
        # 갱신의 구조는 낱말 세 개와 화살표 두 개면 된다. 문장으로 늘리지 않는다.
        chain = VGroup(
            body("prior", 32, INK),
            Tex(R"\rightarrow").set_color(GREY_B),
            body("data", 32, WARN),
            Tex(R"\rightarrow").set_color(GREY_B),
            body("posterior", 32, MEAN_COLOR),
        ).arrange(RIGHT, buff=0.45)
        chain.next_to(scale_line, DOWN, buff=1.1)
        self.play(LaggedStartMap(FadeIn, chain, lag_ratio=0.2), run_time=1.4)
        self.wait(0.8)

        tail = Tex(R"P(\text{spam} \mid \text{words})").set_color(MEAN_COLOR).scale(0.95)
        tail.next_to(chain, DOWN, buff=0.55)
        self.play(Write(tail))
        self.wait(2)
