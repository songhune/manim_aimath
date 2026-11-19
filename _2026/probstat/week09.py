# -*- coding: utf-8 -*-
"""확률과통계 「단일표본 및 이표본 추정 문제」 장 (Walpole Chapter 9) — 불편추정량 · 신뢰구간 · 예측구간 · 허용한계 ·
대응 관측 · 분산의 구간 · 최대우도추정.

개념 영상 일곱 편이고 예제 영상은 없다(8장과 같은 기준 — 영상은 정지 그림으로 안 보이는 곳에만, 자리는 그 개념
슬라이드 앞). 9장의 예제는 공식에 값을 넣고 표를 읽는 계산이라 풀이 설명문이 맡는다. 일곱 편이 보이는 것:
표본을 되풀이 뽑을 때 n 으로 나눈 분산의 평균이 σ² 아래에 머무는 것, 구간이 표본마다 달라지며 μ 를 덮는 비율,
새 관측값의 변동이 평균 추정의 변동에 더해지는 것, 같은 자료의 세 구간이 서로 다른 폭을 갖는 것,
쌍의 차로 바꾸면 퍼짐이 줄어드는 것, χ² 의 두 꼬리를 뒤집어 얻은 구간이 s² 둘레에서 비대칭인 것,
μ 를 움직일 때 우도가 x̄ 에서 최대가 되는 것.
소재는 교재의 예제 그대로다(9.1 · 9.2 · 9.7 · 사례 연구 9.1 · 9.13 · 9.18 · 9.20). 화면 문구는 영어, 여섯 낱말까지.

덱 삽입 자리 (정본은 insert_videos.py 의 PS1_09_INSERT. 모두 그 개념 슬라이드 바로 앞):
    UnbiasedEstimator              9.3 정의 9.1 (불편추정량) 앞
    ConfidenceIntervalCoverage     9.4 σ 를 알 때 μ 의 신뢰구간 (그림 9.3) 앞
    PredictionInterval             9.6 예측구간 도입 앞
    ThreeIntervals                 9.7 사례 연구 9.1 앞 (세 구간의 구별)
    PairedObservations             9.9 대응 관측 도입 앞
    VarianceIntervalChiSquare      9.12 분산의 추정 앞
    LikelihoodFunction             9.14 최대우도추정 앞

참고: legacy/_2023/clt/main.py (표본이 점으로 떨어져 쌓이는 전개). 코드는 옮기지 않았다.

렌더 (저장소 루트에서, 한 번에 한 프로세스만):
    ./render.sh check _2026/probstat/week09.py
    ./render.sh ppt   _2026/probstat/week09.py UnbiasedEstimator
"""
import math
from math import exp, sqrt

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN,
    crowd, label, note, slide_title,
)
from _2026.probstat.week04 import density_axes, area_under, x_marks
from _2026.probstat.week05 import dashed
from _2026.probstat.week07 import npdf, normal_graph
from _2026.probstat.week08 import Pile, chi2_pdf, drop


# ─────────────────────────────────────────────────────────────
# 도구
# ─────────────────────────────────────────────────────────────
def marked_line(lo, hi, step, width, pos, marks, fmt="%g", scale=0.5):
    """눈금 숫자를 Tex 로 직접 다는 수직선(소수 눈금용)."""
    line = NumberLine(x_range=(lo, hi, step), width=width, include_tip=False)
    line.set_stroke(GREY_B, 2).move_to(pos)
    nums = VGroup(*[Tex(fmt % m).scale(scale).set_color(GREY_B).next_to(line.n2p(m), DOWN, buff=0.15) for m in marks])
    line.ps_nums = nums
    return line


def span(line, a, b, up, color, width=7):
    """수직선 위 up 만큼 띄운 구간 막대(양 끝에 짧은 세로 마개)."""
    p, q = line.n2p(a) + UP * up, line.n2p(b) + UP * up
    bar = Line(p, q).set_stroke(color, width)
    caps = VGroup(*[Line(r + DOWN * 0.1, r + UP * 0.1).set_stroke(color, 3) for r in (p, q)])
    return VGroup(bar, caps)


def poisson(x, mu):
    return exp(-mu) * mu ** x / math.factorial(x)


# ─────────────────────────────────────────────────────────────
# 1. 불편추정량 — 9.3 정의 9.1 앞 (예제 9.1)
# ─────────────────────────────────────────────────────────────
class UnbiasedEstimator(InteractiveScene):
    """정규 모집단(μ = 50, σ² = 100)에서 n = 5 를 되풀이 뽑아 편차 제곱합을 n 으로 나눈 값과 n − 1 로 나눈 S² 를
    두 수직선에 떨어뜨린다. 2000번의 평균은 앞쪽이 σ²(n − 1)/n = 80 근처, S² 가 σ² = 100 근처다."""

    def construct(self):
        head = slide_title("Unbiased Estimator")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        rng = np.random.default_rng(91)
        n, sig2 = 5, 100.0

        ax = density_axes((20, 80, 10), (0, 0.045, 0.01), width=4.4, height=1.5).move_to([-4.3, 1.4, 0])
        g = normal_graph(ax, 50, 10, 20, 80, MUTED, 2.5)
        pop = Tex(R"\text{population}\ \ \mu = 50,\ \sigma^2 = 100").scale(0.6).set_color(GREY_B).next_to(ax, UP, buff=0.08)
        n_tag = label("n = 5", 26, CALM).next_to(ax, DOWN, buff=0.25)
        self.play(ShowCreation(ax), ShowCreation(g), FadeIn(pop), FadeIn(n_tag))
        self.wait(0.8)

        f_n = Tex(R"\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar x)^2").scale(0.62).set_color(WARN).move_to([-4.3, -1.0, 0])
        f_s = Tex(R"S^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)^2").scale(0.62).set_color(CALM).move_to([-4.3, -2.5, 0])
        top = marked_line(0, 300, 50, 6.4, [2.9, -0.2, 0], [0, 100, 200, 300])
        bot = marked_line(0, 300, 50, 6.4, [2.9, -2.9, 0], [0, 100, 200, 300])
        self.play(Write(f_n), ShowCreation(top), FadeIn(top.ps_nums))
        self.play(Write(f_s), ShowCreation(bot), FadeIn(bot.ps_nums))
        self.wait(0.8)

        target = dashed(bot.n2p(sig2), top.n2p(sig2) + UP * 1.9, MEAN_COLOR)
        t_lab = Tex(R"\sigma^2 = 100").scale(0.65).set_color(MEAN_COLOR).next_to(target, UP, buff=0.1)
        self.play(ShowCreation(target), FadeIn(t_lab))
        self.wait(0.8)

        p_top = Pile(top, bin_width=10, step=0.115, radius=0.05, color=WARN)
        p_bot = Pile(bot, bin_width=10, step=0.115, radius=0.05, color=CALM)
        shown_n, shown_s = [], []
        for k in range(60):
            x = rng.normal(50, 10, n)
            ss = float(((x - x.mean()) ** 2).sum())
            vn, vs = ss / n, ss / (n - 1)
            shown_n.append(vn); shown_s.append(vs)
            start = ax.c2p(50, 0) + RIGHT * 2.6
            d1 = p_top.dot(min(vn, 295), start)
            d2 = p_bot.dot(min(vs, 295), start)
            if k < 5:
                pts = VGroup(*[Dot(radius=0.06).set_fill(INK, 1).move_to(ax.c2p(v, 0)) for v in np.clip(x, 21, 79)])
                val = Tex(R"\textstyle\sum (x_i - \bar x)^2 = %.0f" % ss).scale(0.58).set_color(INK).move_to([-0.6, 1.5, 0])
                self.play(FadeIn(pts), FadeIn(val), run_time=0.4)
                self.add(d1, d2)
                drop(self, [d1, d2], run_time=0.5, lag=0.0)
                self.play(FadeOut(pts), FadeOut(val), run_time=0.25)
            else:
                self.add(d1, d2)
                drop(self, [d1, d2], run_time=0.12, lag=0.0)
        self.wait(1.0)

        # 2000번의 평균 (화면의 60개 포함)
        more = rng.normal(50, 10, (1940, n))
        ss_more = ((more - more.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
        mean_n = float((sum(shown_n) + (ss_more / n).sum()) / 2000)
        mean_s = float((sum(shown_s) + (ss_more / (n - 1)).sum()) / 2000)
        reps = label("average over 2000 samples", 24, GREY_B).move_to([3.4, 2.35, 0])
        m1 = Line(top.n2p(mean_n), top.n2p(mean_n) + UP * 1.3).set_stroke(WARN, 5)
        m2 = Line(bot.n2p(mean_s), bot.n2p(mean_s) + UP * 1.3).set_stroke(CALM, 5)
        v1 = Tex(R"\text{average} = %.1f" % mean_n).scale(0.65).set_color(WARN).move_to([4.6, 1.0, 0])
        v2 = Tex(R"\text{average} = %.1f" % mean_s).scale(0.65).set_color(CALM).move_to([4.6, -1.7, 0])
        self.play(FadeIn(reps))
        self.play(ShowCreation(m1), Write(v1))
        self.wait(0.8)
        self.play(ShowCreation(m2), Write(v2))
        self.wait(1.2)
        b1 = label("biased", 24, WARN).next_to(v1, DOWN, buff=0.15)
        b2 = Tex(R"E(S^2) = \sigma^2").scale(0.7).set_color(CALM).next_to(v2, DOWN, buff=0.18)
        self.play(FadeIn(b1))
        self.play(Write(b2), FlashAround(f_s, color=CALM, buff=0.12))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 2. 신뢰구간의 포함 비율 — 9.4 (그림 9.3) 앞, 예제 9.2 의 σ = 0.3, n = 36
# ─────────────────────────────────────────────────────────────
class ConfidenceIntervalCoverage(InteractiveScene):
    """μ = 2.6, σ = 0.3 인 모집단에서 n = 36 을 50번 뽑아 x̄ ± 1.96σ/√n 을 쌓는다. μ 를 놓친 구간은 붉게.
    같은 절차를 1000번 하면 덮는 비율이 95 % 근처다(난수 고정, 씬 안에서 센다)."""

    def construct(self):
        head = slide_title("Confidence Interval for μ")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        rng = np.random.default_rng(92)
        mu, sig, n = 2.6, 0.3, 36
        half = 1.96 * sig / sqrt(n)

        pop = Tex(R"\mu = 2.6,\ \ \sigma = 0.3,\ \ n = 36").scale(0.7).set_color(GREY_B).move_to([-4.5, 1.9, 0])
        form = Tex(R"\bar x \pm z_{0.025}\frac{\sigma}{\sqrt{n}}").scale(0.85).set_color(ACCENT).move_to([-4.5, 0.8, 0])
        num = Tex(R"\bar x \pm (1.96)\frac{0.3}{\sqrt{36}} = \bar x \pm %.3f" % half).scale(0.62).set_color(INK).move_to([-4.5, -0.3, 0])
        self.play(Write(pop))
        self.play(Write(form))
        self.play(Write(num))
        self.wait(1.0)

        axis = marked_line(2.4, 2.8, 0.1, 7.2, [2.4, -3.0, 0], [2.4, 2.5, 2.6, 2.7, 2.8], fmt="%.1f")
        mu_line = dashed(axis.n2p(mu), axis.n2p(mu) + UP * 5.0, MEAN_COLOR)
        mu_lab = Tex(R"\mu").scale(0.8).set_color(MEAN_COLOR).next_to(mu_line, UP, buff=0.08)
        self.play(ShowCreation(axis), FadeIn(axis.ps_nums))
        self.play(ShowCreation(mu_line), FadeIn(mu_lab))
        self.wait(0.6)

        bars, hits = [], 0
        for k in range(50):
            xb = float(rng.normal(mu, sig, n).mean())
            ok = abs(xb - mu) < half
            hits += ok
            col = ACCENT if ok else WARN
            up = 0.3 + k * 0.09
            seg = Line(axis.n2p(xb - half) + UP * up, axis.n2p(xb + half) + UP * up).set_stroke(col, 3)
            dot = Dot(radius=0.04).set_fill(col, 1).move_to(axis.n2p(xb) + UP * up)
            bars.append(VGroup(seg, dot))
        for b in bars[:6]:
            self.play(FadeIn(b[1]), ShowCreation(b[0]), run_time=0.45)
        self.wait(0.6)
        self.play(LaggedStart(*[FadeIn(b) for b in bars[6:]], lag_ratio=0.12), run_time=5.0)
        self.wait(0.8)

        c50 = label("50 intervals: %d cover μ" % hits, 26, ACCENT).move_to([-4.5, -1.5, 0])
        miss = label("%d miss μ" % (50 - hits), 26, WARN).next_to(c50, DOWN, buff=0.2).align_to(c50, LEFT)
        self.play(FadeIn(c50))
        self.play(FadeIn(miss))
        self.wait(1.5)

        xs = rng.normal(mu, sig, (1000, n)).mean(axis=1)
        cover = int((np.abs(xs - mu) < half).sum())
        c1000 = label("1000 intervals: %d cover μ" % cover, 26, MEAN_COLOR).next_to(miss, DOWN, buff=0.35).align_to(c50, LEFT)
        self.play(FadeIn(c1000))
        self.play(FlashAround(c1000, color=MEAN_COLOR, buff=0.1))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 3. 예측구간 — 9.6 도입 앞, 예제 9.7
# ─────────────────────────────────────────────────────────────
class PredictionInterval(InteractiveScene):
    """예제 9.7 (n = 50, x̄ = 257,300, σ = 25,000). 새 관측값 x₀ 의 변동은 σ²/n(평균 추정) + σ²(관측 하나)다.
    같은 자료의 95 % 신뢰구간과 예측구간을 한 수직선에 놓고, 새 관측값 40개가 어디에 떨어지는지 센다."""

    def construct(self):
        head = slide_title("Prediction Interval")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        rng = np.random.default_rng(97)
        n, xb, sig = 50, 257.3, 25.0
        ci = 1.96 * sig / sqrt(n)
        pi = 1.96 * sig * sqrt(1 + 1 / n)

        data = Tex(R"n = 50,\ \ \bar x = 257{,}300,\ \ \sigma = 25{,}000").scale(0.65).set_color(GREY_B).move_to([-3.4, 2.1, 0])
        self.play(Write(data))
        v_l = Tex(R"\sigma^2_{x_0 - \bar x} =").scale(0.85).set_color(INK)
        v_a = Tex(R"\frac{\sigma^2}{n}").scale(0.85).set_color(ACCENT)
        v_p = Tex("+").scale(0.85).set_color(INK)
        v_b = Tex(R"\sigma^2").scale(0.85).set_color(WARN)
        VGroup(v_l, v_a, v_p, v_b).arrange(RIGHT, buff=0.22).move_to([-3.6, 1.1, 0])
        t1 = label("estimating the mean", 22, ACCENT).next_to(v_a, DOWN, buff=0.3).shift(LEFT * 1.3)
        t2 = label("one new observation", 22, WARN).next_to(v_b, DOWN, buff=0.3).shift(RIGHT * 1.2)
        self.play(Write(v_l), Write(v_a), FadeIn(t1))
        self.wait(0.8)
        self.play(Write(v_p), Write(v_b), FadeIn(t2))
        self.wait(1.2)

        # 분산의 크기를 막대 길이로: σ²/n 은 σ² 의 1/50
        unit = 4.2
        big = Rectangle(width=unit, height=0.3).set_fill(WARN, 0.8).set_stroke(WARN, 1)
        small = Rectangle(width=unit / n, height=0.3).set_fill(ACCENT, 1).set_stroke(ACCENT, 1)
        small.move_to([1.6, 1.0, 0], aligned_edge=LEFT)
        big.next_to(small, RIGHT, buff=0)
        ratio = Tex(R"\frac{\sigma^2}{n} : \sigma^2 = 1 : 50").scale(0.6).set_color(INK).next_to(VGroup(small, big), UP, buff=0.2)
        self.play(GrowFromEdge(small, LEFT), GrowFromEdge(big, LEFT), FadeIn(ratio))
        self.wait(1.5)

        line = marked_line(200, 320, 20, 11.0, [0, -2.9, 0], [200, 220, 240, 260, 280, 300, 320])
        unit_lab = note("loan amount ($1000)", 20, GREY_B).next_to(line, RIGHT, buff=0.1).shift(UP * 0.35 + LEFT * 1.6)
        mean_mark = dashed(line.n2p(xb), line.n2p(xb) + UP * 1.1, MEAN_COLOR)
        mean_lab = Tex(R"\bar x").scale(0.7).set_color(MEAN_COLOR).move_to(line.n2p(xb) + UP * 2.5)
        self.play(ShowCreation(line), FadeIn(line.ps_nums), FadeIn(unit_lab))
        self.play(ShowCreation(mean_mark), FadeIn(mean_lab))

        ci_bar = span(line, xb - ci, xb + ci, 2.1, ACCENT)
        ci_txt = Tex(R"\bar x \pm z_{0.025}\frac{\sigma}{\sqrt n}:\ \ %s < \mu < %s" % (self.money(xb - ci), self.money(xb + ci))).scale(0.5).set_color(ACCENT)
        ci_txt.next_to(ci_bar, RIGHT, buff=0.3)
        self.play(ShowCreation(ci_bar[0]), FadeIn(ci_bar[1]), Write(ci_txt))
        self.wait(1.2)
        pi_bar = span(line, xb - pi, xb + pi, 1.1, WARN)
        pi_txt = Tex(R"\bar x \pm z_{0.025}\,\sigma\sqrt{1 + 1/n}:\ \ %s < x_0 < %s" % (self.money(xb - pi), self.money(xb + pi))).scale(0.5).set_color(WARN)
        pi_txt.next_to(pi_bar, UP, buff=0.12).align_to(pi_bar, LEFT)
        self.play(ShowCreation(pi_bar[0]), FadeIn(pi_bar[1]))
        self.play(Write(pi_txt))
        self.wait(1.5)

        # 새 관측값 40개
        pile = Pile(line, bin_width=4, step=0.11, radius=0.05, color=INK, lift=0.1)
        xs = np.clip(rng.normal(xb, sig, 40), 201, 319)
        dots = [pile.dot(float(x), line.n2p(float(x)) + UP * 1.0) for x in xs]
        self.add(*dots)
        drop(self, dots, run_time=3.5, lag=0.08)
        in_pi = int(((xs > xb - pi) & (xs < xb + pi)).sum())
        in_ci = int(((xs > xb - ci) & (xs < xb + ci)).sum())
        r1 = label("40 new observations", 22, INK).move_to([-4.6, 0.05, 0])
        r2 = label("%d inside prediction interval" % in_pi, 22, WARN).next_to(r1, DOWN, buff=0.15).align_to(r1, LEFT)
        r3 = label("%d inside confidence interval" % in_ci, 22, ACCENT).next_to(r2, DOWN, buff=0.15).align_to(r1, LEFT)
        self.play(FadeOut(t1), FadeOut(t2), FadeIn(r1))
        self.play(FadeIn(r2))
        self.play(FadeIn(r3))
        self.wait(3.5)

    @staticmethod
    def money(v):
        return "{:,.2f}".format(v * 1000).replace(",", "{,}")


# ─────────────────────────────────────────────────────────────
# 4. 세 구간 — 9.7 사례 연구 9.1 앞
# ─────────────────────────────────────────────────────────────
class ThreeIntervals(InteractiveScene):
    """사례 연구 9.1 의 지름 9개(x̄ = 1.0056, s = 0.0246)로 99 % 신뢰구간 · 예측구간 · 허용한계를 같은 수직선에 놓는다.
    계수는 t₀.₀₀₅(8) = 3.355, 표 A.7 의 k = 4.550 이다."""
    DATA = [1.01, 0.97, 1.03, 1.04, 0.99, 0.98, 0.99, 1.01, 1.03]

    def construct(self):
        head = slide_title("Confidence, Prediction, Tolerance")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        x = np.array(self.DATA)
        n, xb, s = len(x), round(float(x.mean()), 4), round(float(x.std(ddof=1)), 4)     # 교재처럼 넷째 자리로 맺은 값으로 잇는다
        t, k = 3.355, 4.550
        ci, pi, tl = round(t * s / sqrt(n), 4), round(t * s * sqrt(1 + 1 / n), 4), round(k * s, 4)

        line = marked_line(0.85, 1.15, 0.05, 11.0, [-0.6, -2.9, 0], [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15], fmt="%.2f")
        unit_lab = note("diameter (cm)", 20, GREY_B).next_to(line, RIGHT, buff=0.15)
        self.play(ShowCreation(line), FadeIn(line.ps_nums), FadeIn(unit_lab))
        pile = Pile(line, bin_width=0.01, step=0.13, radius=0.06, color=INK, lift=0.1)
        dots = [pile.dot(float(v), line.n2p(float(v)) + UP * 1.2) for v in x]
        self.add(*dots)
        drop(self, dots, run_time=1.5, lag=0.1)
        stat = Tex(R"n = 9,\ \ \bar x = %.4f,\ \ s = %.4f" % (xb, s)).scale(0.65).set_color(GREY_B).move_to([-3.6, 2.2, 0])
        self.play(Write(stat))
        mean_mark = dashed(line.n2p(xb) + UP * 0.45, line.n2p(xb) + UP * 0.8, MEAN_COLOR)
        self.play(ShowCreation(mean_mark))
        self.wait(1.0)

        rows = [
            (ci, ACCENT, "99% confidence interval: mean μ", R"\bar x \pm t_{0.005}\frac{s}{\sqrt n}", 0.85),
            (pi, CALM, "99% prediction interval: one new piece", R"\bar x \pm t_{0.005}\,s\sqrt{1 + 1/n}", 2.05),
            (tl, WARN, "99% tolerance limits: 95% of pieces", R"\bar x \pm ks,\ \ k = 4.550", 3.25),
        ]
        for h, col, name, form, up in rows:
            bar = span(line, xb - h, xb + h, up, col)
            nm = label(name, 22, col).next_to(bar, UP, buff=0.12).align_to(bar, LEFT)
            if nm.get_left()[0] > -2.0:                      # 좁은 막대는 이름을 왼쪽으로 뺀다
                nm.next_to(bar, UP, buff=0.12).set_x(-3.9)
            fm = Tex(form).scale(0.52).set_color(col).next_to(nm, RIGHT, buff=0.4)
            rg = Tex(R"(%.4f,\ %.4f)" % (xb - h, xb + h)).scale(0.6).set_color(col).next_to(fm, RIGHT, buff=0.4)
            self.play(ShowCreation(bar[0]), FadeIn(bar[1]), FadeIn(nm))
            self.play(Write(fm))
            self.play(Write(rg))
            self.wait(1.5)
        self.wait(3.0)


# ─────────────────────────────────────────────────────────────
# 5. 대응 관측 — 9.9 도입 앞, 예제 9.13 (표 9.1)
# ─────────────────────────────────────────────────────────────
class PairedObservations(InteractiveScene):
    """표 9.1 의 TCDD 20쌍. 혈장과 지방 조직을 두 표본으로 보면 표준편차가 8 안팎이고, 사람마다 차 dᵢ 를 내면
    s_d = 2.9773 으로 줄어든다. μ_D 의 95 % 신뢰구간은 d̄ ± t₀.₀₂₅(19) s_d/√n 이다."""
    PLASMA = [2.5, 3.1, 2.1, 3.5, 3.1, 1.8, 6.0, 3.0, 36.0, 4.7, 6.9, 3.3, 4.6, 1.6, 7.2, 1.8, 20.0, 2.0, 2.5, 4.1]
    FAT = [4.9, 5.9, 4.4, 6.9, 7.0, 4.2, 10.0, 5.5, 41.0, 4.4, 7.0, 2.9, 4.6, 1.4, 7.7, 1.1, 11.0, 2.5, 2.3, 2.5]

    def construct(self):
        head = slide_title("Paired Observations")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        p, f = np.array(self.PLASMA), np.array(self.FAT)
        d = p - f
        n = len(d)
        s1, s2, sd, dbar = float(p.std(ddof=1)), float(f.std(ddof=1)), float(d.std(ddof=1)), float(d.mean())
        half = 2.093 * sd / sqrt(n)

        people = crowd(20, 1, 20, height=0.32, buff=0.1, seed=5).move_to([-1.2, 2.2, 0])
        who = label("20 veterans", 22, GREY_B).next_to(people, RIGHT, buff=0.3)
        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.03), FadeIn(who), run_time=1.0)

        marks = [0, 10, 20, 30, 40]
        l1 = marked_line(0, 45, 5, 9.0, [-0.4, 1.2, 0], marks)
        l2 = marked_line(0, 45, 5, 9.0, [-0.4, -0.3, 0], marks)
        n1 = label("plasma", 22, CALM).next_to(l1, LEFT, buff=0.25)
        n2 = label("fat tissue", 22, ACCENT).next_to(l2, LEFT, buff=0.25)
        self.play(ShowCreation(l1), ShowCreation(l2), FadeIn(l2.ps_nums), FadeIn(n1), FadeIn(n2))
        d1 = VGroup(*[Dot(radius=0.055).set_fill(CALM, 1).move_to(l1.n2p(v)) for v in p])
        d2 = VGroup(*[Dot(radius=0.055).set_fill(ACCENT, 1).move_to(l2.n2p(v)) for v in f])
        self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in d1], lag_ratio=0.05),
                  LaggedStart(*[FadeIn(m, shift=DOWN * 0.3) for m in d2], lag_ratio=0.05), run_time=1.8)
        self.wait(0.8)
        t1 = Tex(R"s_1 = %.2f" % s1).scale(0.65).set_color(CALM).move_to([5.6, 1.2, 0])
        t2 = Tex(R"s_2 = %.2f" % s2).scale(0.65).set_color(ACCENT).move_to([5.6, -0.3, 0])
        self.play(Write(t1), Write(t2))
        self.wait(1.5)

        links = VGroup(*[Line(a.get_center(), b.get_center()).set_stroke(GREY_B, 1.5, 0.8) for a, b in zip(d1, d2)])
        same = label("same veteran, two measurements", 22, GREY_B).move_to([3.4, 0.45, 0])
        self.play(LaggedStartMap(ShowCreation, links, lag_ratio=0.05), FadeIn(same), run_time=1.5)
        self.wait(1.5)

        l3 = marked_line(-6, 10, 2, 9.0, [-1.6, -2.9, 0], [-6, -4, -2, 0, 2, 4, 6, 8, 10])
        n3 = Tex(R"d_i = x_{1i} - x_{2i}").scale(0.6).set_color(MEAN_COLOR).next_to(l3, RIGHT, buff=0.3)
        self.play(ShowCreation(l3), FadeIn(l3.ps_nums), Write(n3))
        pile = Pile(l3, bin_width=0.5, step=0.12, radius=0.055, color=MEAN_COLOR, lift=0.1)
        dd = [pile.dot(float(v), ln.get_center()) for v, ln in zip(d, links)]
        self.add(*dd)
        drop(self, dd, run_time=2.5, lag=0.08)
        self.wait(0.8)
        t3 = Tex(R"s_d = %.4f" % sd).scale(0.7).set_color(MEAN_COLOR).move_to([5.3, -2.0, 0])
        self.play(Write(t3))
        self.play(FlashAround(t3, color=MEAN_COLOR, buff=0.1))
        self.wait(1.5)

        bar = span(l3, dbar - half, dbar + half, 0.95, WARN)
        form = Tex(R"\bar d \pm t_{0.025}\frac{s_d}{\sqrt n}").scale(0.6).set_color(WARN).move_to([1.2, -1.45, 0])
        rg = Tex(R"%.4f < \mu_D < %.4f" % (dbar - half, dbar + half)).scale(0.6).set_color(WARN).next_to(form, RIGHT, buff=0.3)
        self.play(FadeOut(same), ShowCreation(bar[0]), FadeIn(bar[1]), Write(form))
        self.play(Write(rg))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 6. 분산의 신뢰구간 — 9.12 앞, 예제 9.18 (그림 9.7)
# ─────────────────────────────────────────────────────────────
class VarianceIntervalChiSquare(InteractiveScene):
    """예제 9.18 의 잔디 씨 10봉지(s² = 0.286). χ²(9) 의 두 꼬리 0.025 를 자르는 2.700 과 19.023 사이에
    (n − 1)S²/σ² 가 들어갈 확률이 0.95 다. σ² 에 대해 뒤집으면 구간은 s² 의 왼쪽이 짧고 오른쪽이 길다."""
    DATA = [46.4, 46.1, 45.8, 47.0, 46.1, 45.9, 45.8, 46.9, 45.2, 46.0]

    def construct(self):
        head = slide_title("Confidence Interval for σ²")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        x = np.array(self.DATA)
        n, s2 = len(x), round(float(x.var(ddof=1)), 3)       # 교재의 0.286
        lo_c, hi_c = 2.700, 19.023
        lo, hi = (n - 1) * s2 / hi_c, (n - 1) * s2 / lo_c

        stat = Tex(R"\chi^2 = \frac{(n-1)S^2}{\sigma^2},\quad v = n - 1 = 9").scale(0.7).set_color(MEAN_COLOR).move_to([-3.4, 2.1, 0])
        self.play(Write(stat))
        axes = density_axes((0, 26, 2), (0, 0.11, 0.02), width=7.4, height=2.5).move_to([-3.0, 0.2, 0])
        g = axes.get_graph(lambda v: chi2_pdf(v, 9), x_range=(0.01, 26, 0.05)).set_stroke(MEAN_COLOR, 3)
        self.play(ShowCreation(axes), ShowCreation(g))
        self.wait(0.6)
        left = area_under(axes, g, 0.01, lo_c, WARN, 0.7)
        right = area_under(axes, g, hi_c, 26, WARN, 0.7)
        mid = area_under(axes, g, lo_c, hi_c, MEAN_COLOR, 0.3)
        marks = x_marks(axes, [lo_c, hi_c], ["2.700", "19.023"], WARN)
        self.play(FadeIn(left), FadeIn(right), FadeIn(marks))
        tail1 = Tex(R"0.025").scale(0.5).set_color(WARN).move_to(axes.c2p(1.3, 0.07))
        ptr = Line(tail1.get_bottom() + DOWN * 0.05, axes.c2p(1.9, 0.006)).set_stroke(WARN, 1.5)
        tail1 = VGroup(tail1, ptr)
        tail2 = Tex(R"0.025").scale(0.5).set_color(WARN).next_to(axes.c2p(22.5, 0.012), UP, buff=0.1)
        self.play(FadeIn(tail1), FadeIn(tail2))
        self.play(FadeIn(mid))
        m95 = Tex(R"0.95").scale(0.6).set_color(MEAN_COLOR).move_to(axes.c2p(8.5, 0.035))
        self.play(FadeIn(m95))
        src = note("Table A.5", 20, GREY_B).next_to(axes, DOWN, buff=0.45).align_to(axes, RIGHT)
        self.play(FadeIn(src))
        self.wait(1.5)

        e1 = Tex(R"2.700 < \frac{(n-1)s^2}{\sigma^2} < 19.023").scale(0.62).set_color(INK).move_to([4.0, 1.9, 0])
        e2 = Tex(R"\frac{(n-1)s^2}{19.023} < \sigma^2 < \frac{(n-1)s^2}{2.700}").scale(0.62).set_color(INK).next_to(e1, DOWN, buff=0.35)
        e3 = Tex(R"\frac{(9)(%.3f)}{19.023} < \sigma^2 < \frac{(9)(%.3f)}{2.700}" % (s2, s2)).scale(0.62).set_color(INK).next_to(e2, DOWN, buff=0.35)
        e4 = Tex(R"%.3f < \sigma^2 < %.3f" % (lo, hi)).scale(0.75).set_color(CALM).next_to(e3, DOWN, buff=0.35)
        self.play(Write(e1))
        self.wait(0.8)
        self.play(Write(e2))
        self.wait(1.0)
        self.play(Write(e3))
        self.play(Write(e4))
        self.wait(1.5)

        line = marked_line(0, 1.0, 0.1, 9.0, [-1.4, -3.0, 0], [0, 0.2, 0.4, 0.6, 0.8, 1.0], fmt="%.1f")
        sig_lab = Tex(R"\sigma^2").scale(0.7).set_color(CALM).next_to(line, RIGHT, buff=0.25)
        self.play(ShowCreation(line), FadeIn(line.ps_nums), FadeIn(sig_lab))
        s_dot = Dot(radius=0.09).set_fill(MEAN_COLOR, 1).move_to(line.n2p(s2) + UP * 0.45)
        s_lab = Tex(R"s^2 = %.3f" % s2).scale(0.6).set_color(MEAN_COLOR).next_to(s_dot, UP, buff=0.15)
        bar = span(line, lo, hi, 0.45, CALM)
        self.play(ShowCreation(bar[0]), FadeIn(bar[1]))
        self.play(FadeIn(s_dot), Write(s_lab))
        self.wait(0.8)
        a = Tex(R"%.3f" % (s2 - lo)).scale(0.55).set_color(WARN).next_to(line.n2p((lo + s2) / 2) + UP * 0.45, DOWN, buff=0.1)
        b = Tex(R"%.3f" % (hi - s2)).scale(0.55).set_color(WARN).next_to(line.n2p((hi + s2) / 2) + UP * 0.45, UP, buff=0.12)
        asym = label("not symmetric about s²", 22, WARN).move_to([4.6, -1.9, 0])
        self.play(Write(a), Write(b))
        self.play(FadeIn(asym))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 7. 우도함수 — 9.14 앞, 예제 9.20 (포아송)
# ─────────────────────────────────────────────────────────────
class LikelihoodFunction(InteractiveScene):
    """예제 9.20 의 포아송 모형에 표본 2, 4, 3, 5, 1 (x̄ = 3)을 고정한다. μ 를 1 에서 6 까지 움직이면 표본 값 자리의
    막대 높이 f(xᵢ | μ) 가 바뀌고 그 곱 L(μ) 가 곡선을 그린다. 곡선의 꼭대기는 μ = x̄ 다."""
    SAMPLE = [2, 4, 3, 5, 1]

    def L(self, mu):
        out = 1.0
        for x in self.SAMPLE:
            out *= poisson(x, mu)
        return out

    def construct(self):
        head = slide_title("Maximum Likelihood Estimation")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        xbar = sum(self.SAMPLE) / len(self.SAMPLE)
        lmax = self.L(xbar)

        pmf = Tex(R"f(x \mid \mu) = \frac{e^{-\mu}\mu^x}{x!}").scale(0.7).set_color(INK).move_to([-4.2, 2.1, 0])
        smp = Tex(R"\text{sample}:\ 2,\ 4,\ 3,\ 5,\ 1").scale(0.7).set_color(ACCENT).next_to(pmf, RIGHT, buff=0.9)
        self.play(Write(pmf))
        self.play(Write(smp))
        self.wait(0.8)

        ax = density_axes((-0.5, 10.5, 1), (0, 0.4, 0.1), width=5.6, height=3.0).move_to([-3.8, -0.9, 0])
        nums = x_marks(ax, list(range(0, 11, 2)))
        mu = ValueTracker(1.0)

        def bars():
            g = VGroup()
            m = mu.get_value()
            for x in range(11):
                p = max(poisson(x, m), 1e-4)
                hit = x in self.SAMPLE
                r = Polygon(ax.c2p(x - 0.35, 0), ax.c2p(x - 0.35, p), ax.c2p(x + 0.35, p), ax.c2p(x + 0.35, 0))
                g.add(r.set_fill(ACCENT if hit else MUTED, 0.85 if hit else 0.35).set_stroke(ACCENT if hit else MUTED, 1.5))
            return g

        live_bars = always_redraw(bars)
        mu_tag = Tex(R"\mu =").scale(0.75).set_color(MEAN_COLOR).move_to([-2.6, 0.7, 0])
        mu_num = DecimalNumber(1.0, num_decimal_places=2).scale(0.75).set_color(MEAN_COLOR).next_to(mu_tag, RIGHT, buff=0.15)
        mu_num.f_always.set_value(mu.get_value)
        self.play(ShowCreation(ax), FadeIn(nums))
        first = bars()
        self.play(FadeIn(first), FadeIn(mu_tag), run_time=0.6)
        self.remove(first)
        self.add(live_bars, mu_num)
        self.wait(1.0)

        like = Tex(R"L(\mu) = f(2 \mid \mu)\,f(4 \mid \mu)\,f(3 \mid \mu)\,f(5 \mid \mu)\,f(1 \mid \mu)").scale(0.52).set_color(ACCENT)
        like.move_to([3.4, 1.2, 0])
        self.play(Write(like))
        self.wait(1.2)

        lax = density_axes((0, 7, 1), (0, lmax * 1.2, lmax / 4), width=5.6, height=2.9).move_to([3.4, -1.25, 0])
        lnums = x_marks(lax, [1, 2, 3, 4, 5, 6])
        l_name = Tex(R"L(\mu)").scale(0.6).set_color(ACCENT).next_to(lax.c2p(0, lmax * 1.2), LEFT, buff=0.1)
        m_name = Tex(R"\mu").scale(0.65).set_color(MEAN_COLOR).next_to(lax.c2p(7, 0), DOWN, buff=0.15)
        self.play(ShowCreation(lax), FadeIn(lnums), FadeIn(l_name), FadeIn(m_name))

        def trace():
            m = mu.get_value()
            if m <= 1.02:
                return VMobject()
            return lax.get_graph(self.L, x_range=(1.0, m, 0.02)).set_stroke(ACCENT, 3)

        live_curve = always_redraw(trace)
        live_dot = always_redraw(lambda: Dot(radius=0.08).set_fill(MEAN_COLOR, 1).move_to(lax.c2p(mu.get_value(), self.L(mu.get_value()))))
        self.add(live_curve, live_dot)
        self.wait(0.6)
        self.play(mu.animate.set_value(3.0), run_time=3.5, rate_func=linear)
        self.wait(1.0)
        self.play(mu.animate.set_value(6.0), run_time=4.0, rate_func=linear)
        self.wait(1.0)

        full = lax.get_graph(self.L, x_range=(1.0, 6.0, 0.02)).set_stroke(ACCENT, 3)
        self.remove(live_curve)
        self.add(full)
        self.play(mu.animate.set_value(xbar), run_time=2.5)
        peak = dashed(lax.c2p(xbar, 0), lax.c2p(xbar, lmax), MEAN_COLOR)
        self.play(ShowCreation(peak))
        est = Tex(R"\hat\mu = \bar x = %g" % xbar).scale(0.8).set_color(MEAN_COLOR).move_to([5.3, -0.2, 0])
        top = label("maximum of L(μ)", 22, MEAN_COLOR).next_to(est, UP, buff=0.2)
        self.play(FadeIn(top), Write(est))
        self.play(FlashAround(est, color=MEAN_COLOR, buff=0.1))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 예제 영상 (2026-11-20, 사용자 요청) — 문제 장 뒤, 책 풀이 장 앞
# ─────────────────────────────────────────────────────────────
from _2026.probstat.week05 import steps_panel

EX_COL_X = 1.2          # 오른쪽 식 열의 왼쪽 끝


def _eq(tex, ref, color=INK, scale=0.58, gap=0.3):
    """식 한 줄을 ref 아래, 오른쪽 식 열에 왼쪽 맞춤으로 놓는다."""
    t = Tex(tex).scale(scale).set_color(color).next_to(ref, DOWN, buff=gap)
    t.align_to([EX_COL_X, 0, 0], LEFT)
    return t


# ─────────────────────────────────────────────────────────────
# 8. 예제 9.2 — 아연 농도의 95% · 99% 신뢰구간 (문제 장 뒤)
# ─────────────────────────────────────────────────────────────
class Example92ZincInterval(InteractiveScene):
    """n = 36, x̄ = 2.6, σ = 0.3. 표준오차 0.3/√36 = 0.05 를 먼저 구하고, 표준정규곡선의 가운데 넓이 0.95 를 남기는
    z = 1.96 을 표준오차에 곱해 2.6 둘레에 구간을 놓는다. 가운데 넓이를 0.99 로 넓히면 z 가 2.575 로 늘고
    같은 수직선 위의 구간도 2.47–2.73 으로 넓어진다."""

    def construct(self):
        head = slide_title("Example 9.2")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. standard error", "2. z from Table A.3",
                                         "3. 95% interval", "4. 99% interval"], pos=(4.9, 2.0, 0), size=20)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        n, xbar, sig = 36, 2.6, 0.3
        se = sig / sqrt(n)

        given = Tex(R"n = 36,\quad \bar x = 2.6,\quad \sigma = 0.3").scale(0.62).set_color(GREY_B).move_to([-3.6, 2.2, 0])
        self.play(Write(given))
        self.wait(0.8)

        # 1. 표준오차
        self.play(focus(0))
        e1 = _eq(R"\frac{\sigma}{\sqrt n} = \frac{0.3}{\sqrt{36}} = \frac{0.3}{6} = 0.05", box, CALM, gap=0.35)
        self.play(Write(e1))
        self.wait(1.4)

        # 2. 표준정규곡선에서 가운데 0.95
        self.play(focus(1))
        ax = density_axes((-3.6, 3.6, 1), (0, 0.45, 0.1), width=5.6, height=1.9).move_to([-3.7, 0.55, 0])
        g = normal_graph(ax, 0, 1, -3.6, 3.6, MUTED, 2.5)
        zname = Tex("Z").scale(0.6).set_color(GREY_B).next_to(ax.c2p(3.6, 0), RIGHT, buff=0.1)
        self.play(ShowCreation(ax), ShowCreation(g), FadeIn(zname))
        mid95 = area_under(ax, g, -1.96, 1.96, CALM, 0.45)
        a95 = Tex("0.95").scale(0.6).set_color(INK).move_to(ax.c2p(0, 0.14))
        z95 = x_marks(ax, [-1.96, 1.96], ["-1.96", "1.96"], CALM)
        tail = Tex("0.025").scale(0.45).set_color(GREY_B).next_to(ax.c2p(2.5, 0.03), UP, buff=0.12)
        self.play(FadeIn(mid95), FadeIn(a95))
        self.play(FadeIn(z95), FadeIn(tail))
        e2 = _eq(R"z_{0.025} = 1.96", e1, CALM)
        self.play(Write(e2))
        self.wait(1.4)

        # 3. 95% 구간
        self.play(focus(2))
        line = marked_line(2.4, 2.8, 0.05, 6.0, [-3.7, -2.6, 0], [2.4, 2.5, 2.6, 2.7, 2.8], fmt="%.1f", scale=0.5)
        mu_name = Tex(R"\mu").scale(0.6).set_color(GREY_B).next_to(line, RIGHT, buff=0.15)
        dot = Dot(radius=0.08).set_fill(MEAN_COLOR, 1).move_to(line.n2p(xbar))
        xb = Tex(R"\bar x = 2.6").scale(0.55).set_color(MEAN_COLOR).next_to(dot, DOWN, buff=0.5)
        self.play(ShowCreation(line), FadeIn(line.ps_nums), FadeIn(mu_name))
        self.play(FadeIn(dot), FadeIn(xb))
        e3 = _eq(R"2.6 \pm (1.96)(0.05) = 2.6 \pm 0.098", e2, CALM)
        self.play(Write(e3))
        s95 = span(line, xbar - 1.96 * se, xbar + 1.96 * se, 0.35, CALM)
        self.play(GrowFromCenter(s95))
        r3 = _eq(R"2.50 < \mu < 2.70", e3, CALM, scale=0.66, gap=0.2)
        self.play(Write(r3))
        self.wait(1.6)

        # 4. 99% 구간 — 가운데 넓이를 넓히면 z 가 커진다
        self.play(focus(3))
        mid99 = area_under(ax, g, -2.575, 2.575, WARN, 0.3)
        z99 = x_marks(ax, [-2.575, 2.575], ["-2.575", "2.575"], WARN)
        z99.shift(DOWN * 0.3)
        a99 = Tex("0.99").scale(0.6).set_color(WARN).move_to(ax.c2p(0, 0.3))
        self.play(FadeIn(mid99), FadeIn(z99), FadeIn(a99), FadeOut(tail))
        e4 = _eq(R"z_{0.005} = 2.575", r3, WARN, gap=0.35)
        self.play(Write(e4))
        e5 = _eq(R"2.6 \pm (2.575)(0.05) = 2.6 \pm 0.129", e4, WARN, gap=0.2)
        self.play(Write(e5))
        s99 = span(line, xbar - 2.575 * se, xbar + 2.575 * se, 0.75, WARN)
        self.play(GrowFromCenter(s99))
        r5 = _eq(R"2.47 < \mu < 2.73", e5, WARN, scale=0.66, gap=0.2)
        self.play(Write(r5))
        self.wait(1.2)
        self.play(FlashAround(VGroup(r3, r5), color=MEAN_COLOR, buff=0.12))
        self.wait(3.0)


# ─────────────────────────────────────────────────────────────
# 9. 예제 9.3 — 오차가 0.05 미만이 되는 표본 크기 (문제 장 뒤)
# ─────────────────────────────────────────────────────────────
class Example93SampleSize(InteractiveScene):
    """예제 9.2 의 σ = 0.3, 95% 에서 오차의 한계 1.96·0.3/√n 을 n 의 곡선으로 그린다. n = 36 에서 0.098 이고,
    곡선이 e = 0.05 선 아래로 내려가는 자리가 n = 138.3 이라 139 로 올린다. 138 과 139 의 한계값을 나란히 적는다."""

    def construct(self):
        head = slide_title("Example 9.3")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        steps, box, focus = steps_panel(["1. error bound", "2. set bound to e = 0.05",
                                         "3. solve for n", "4. round up"], pos=(4.7, 2.0, 0), size=20)
        self.play(FadeIn(box), LaggedStartMap(FadeIn, steps, lag_ratio=0.2))
        z, sig, e = 1.96, 0.3, 0.05

        def bound(n):
            return z * sig / sqrt(n)

        given = Tex(R"\sigma = 0.3,\quad z_{0.025} = 1.96,\quad e = 0.05").scale(0.6).set_color(GREY_B).move_to([-3.4, 2.2, 0])
        self.play(Write(given))
        self.wait(0.8)

        # 1. 오차의 한계는 n 의 함수다
        self.play(focus(0))
        ax = Axes(x_range=(0, 200, 20), y_range=(0, 0.2, 0.05), width=6.2, height=3.4,
                  axis_config=dict(include_ticks=True, stroke_width=2, stroke_color=GREY_B)).move_to([-3.5, -0.75, 0])
        xn = VGroup(*[Tex(str(v)).scale(0.45).set_color(GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (40, 80, 120, 160, 200)])
        yn = VGroup(*[Tex("%.2f" % v).scale(0.45).set_color(GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0.05, 0.10, 0.15, 0.20)])
        n_name = Tex("n").scale(0.6).set_color(GREY_B).next_to(ax.c2p(200, 0), RIGHT, buff=0.12)
        curve = ax.get_graph(bound, x_range=(10, 200, 0.5)).set_stroke(ACCENT, 3)
        e1 = _eq(R"\text{error} \le z_{\alpha/2}\frac{\sigma}{\sqrt n} = \frac{(1.96)(0.3)}{\sqrt n}", box, ACCENT, gap=0.35)
        self.play(ShowCreation(ax), FadeIn(xn), FadeIn(yn), FadeIn(n_name))
        self.play(Write(e1))
        self.play(ShowCreation(curve), run_time=2.0)
        p36 = Dot(radius=0.08).set_fill(MUTED, 1).move_to(ax.c2p(36, bound(36)))
        t36 = Tex(R"n = 36:\ 0.098").scale(0.5).set_color(GREY_B).next_to(p36, UR, buff=0.08)
        self.play(FadeIn(p36), FadeIn(t36))
        self.wait(1.4)

        # 2. 한계를 e 에 맞춘다
        self.play(focus(1))
        eline = dashed(ax.c2p(0, e), ax.c2p(200, e), WARN)
        ename = Tex("e = 0.05").scale(0.5).set_color(WARN).next_to(ax.c2p(200, e), UP, buff=0.08).shift(LEFT * 0.5)
        self.play(ShowCreation(eline), FadeIn(ename))
        e2 = _eq(R"\frac{(1.96)(0.3)}{\sqrt n} = 0.05", e1, WARN)
        self.play(Write(e2))
        self.wait(1.2)

        # 3. n 에 대해 푼다
        self.play(focus(2))
        e3 = _eq(R"\sqrt n = \frac{(1.96)(0.3)}{0.05} = 11.76", e2, INK)
        self.play(Write(e3))
        e4 = _eq(R"n = (11.76)^2 = 138.3", e3, INK, gap=0.2)
        self.play(Write(e4))
        cross = Dot(radius=0.08).set_fill(MEAN_COLOR, 1).move_to(ax.c2p(138.3, e))
        down = dashed(ax.c2p(138.3, e), ax.c2p(138.3, 0), MEAN_COLOR)
        t138 = Tex("138.3").scale(0.5).set_color(MEAN_COLOR).next_to(ax.c2p(138.3, 0), DOWN, buff=0.4)
        self.play(FadeIn(cross), ShowCreation(down), FadeIn(t138))
        self.wait(1.4)

        # 4. 올림 — 138 은 한계가 0.05 를 넘는다
        self.play(focus(3))
        e5 = _eq(R"n = 138:\ \frac{(1.96)(0.3)}{\sqrt{138}} = 0.05005", e4, WARN, scale=0.52)
        e6 = _eq(R"n = 139:\ \frac{(1.96)(0.3)}{\sqrt{139}} = 0.04987", e5, CALM, scale=0.52, gap=0.15)
        self.play(Write(e5))
        self.play(Write(e6))
        ans = Tex(R"n = 139").scale(0.95).set_color(MEAN_COLOR).move_to(ax.c2p(120, 0.15))     # 식 열이 화면 아래까지 차서 답은 곡선 위 빈 자리에
        self.play(Write(ans))
        self.play(FlashAround(ans, color=MEAN_COLOR, buff=0.1))
        self.wait(3.0)
