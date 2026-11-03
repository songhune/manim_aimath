# -*- coding: utf-8 -*-
"""확률과통계 「기본 표본분포와 자료 기술」 장 (Walpole Chapter 8) — 표본평균의 분포 · 중심극한정리 · S² 의 분포 · t 분포.

7장(확률변수의 함수, `PS1_07_restyled`)은 영상이 없다. 이 파일은 8장이다.
강의 교안 `확률과통계/교육메모/11주차.md` 의 「영상 태그」 를 옮긴 것이다. 도구와 규칙은 week07.py 와 같다.
이 장은 **개념 영상 네 편뿐**이고 예제 영상은 없다(2026-11-03, 사용자 결정 — 영상은 꼭 필요한 곳에만, 자리는 그 개념
슬라이드 **앞**). 예제(8.4–8.11)는 표 읽기와 표준화라 6장의 영상과 풀이 판이 맡는다. 네 편은 정지 그림으로는 안 보이는
것만 고른 것이다: x̄ 가 뽑을 때마다 달라져 쌓이는 모양, 치우친 모집단이 평균을 내면 종 모양이 되는 과정, s² 가 쌓여
오른쪽으로 긴 χ² 가 되는 과정, σ 를 S 로 바꾸면 꼬리가 두꺼워지는 이유.
사람은 치토 무리, 표본은 둥근 테두리(`ring`), 통계량 하나는 점 하나다. 점이 쌓여 막대가 되고 그 위에 곡선을 얹는다.
화면 문구는 영어, 여섯 낱말까지(`ps_common.label`).

덱 삽입 자리 (원본 PS1_08_restyled.pptx 41장 기준. 레이아웃 정리 뒤의 번호는 insert_videos.py 의 PS1_08_INSERT 가 정본이다.
네 편 모두 "N 앞" = 그 개념 슬라이드 바로 앞):
    SampleMeanAsRandomVariable       9 앞    8.4 도입 — x̄ 는 확률변수, μ_x̄ = μ, σ_x̄ = σ/√n
    CentralLimitTheorem             10 앞    정리 8.2 중심극한정리 — 치우친 모집단, n = 1 · 2 · 5 · 30
    ChiSquareFromVariance           22 앞    8.5 S² 의 표본분포 — (n − 1)S²/σ² 가 χ²(n − 1), 표 A.5 의 95 % 띠
    TDistributionTails              26 앞    8.6 t 분포 — σ 대신 S, 꼬리가 두껍다, z₀.₀₂₅ = 1.960 과 t₀.₀₂₅ = 2.145

참고: legacy/_2023/clt/main.py (DiceSumDistributions — 표본이 막대로 떨어져 쌓이고, BuildUpGaussian — 막대 위에 곡선을
      세운다). 전개 순서만 가져오고 코드는 옮기지 않았다.

렌더 (저장소 루트에서, 한 번에 한 프로세스만):
    ./render.sh check _2026/probstat/week08.py
    ./render.sh ppt   _2026/probstat/week08.py SampleMeanAsRandomVariable
"""
import math
from math import exp, sqrt

from manim_imports_ext import *

from _2026.probstat.ps_common import (
    ACCENT, CALM, INK, MEAN_COLOR, MUTED, WARN,
    crowd, label, note, ring, slide_title,
)
from _2026.probstat.week04 import density_axes, area_under, x_marks
from _2026.probstat.week05 import dashed
from _2026.probstat.week07 import npdf, normal_graph, gamma_pdf, frozen


# ─────────────────────────────────────────────────────────────
# 도구 — 수직선, 점 쌓기, 곡선
# ─────────────────────────────────────────────────────────────
def number_line(lo, hi, step, width, pos, font_size=22):
    line = NumberLine(x_range=(lo, hi, step), width=width, include_tip=False)
    line.set_stroke(GREY_B, 2).move_to(pos)
    line.add_numbers(font_size=font_size)
    line.numbers.set_color(GREY_B)
    return line


class Pile:
    """수직선 위에 점을 쌓는다. 같은 칸(bin)의 점은 위로 포갠다."""

    def __init__(self, line, bin_width=1.0, step=0.13, radius=0.055, color=ACCENT, lift=0.08):
        self.line, self.bw, self.step, self.r, self.color, self.lift = line, bin_width, step, radius, color, lift
        self.counts = {}
        self.dots = VGroup()

    def target(self, x):
        k = round(x / self.bw)
        n = self.counts.get(k, 0)
        self.counts[k] = n + 1
        return self.line.n2p(k * self.bw) + UP * (self.lift + n * self.step)

    def dot(self, x, start):
        d = Dot(radius=self.r).set_fill(self.color, 1).move_to(start)
        d.ps_target = self.target(x)
        self.dots.add(d)
        return d

    def height(self):
        return self.lift + max(self.counts.values(), default=0) * self.step


def bell(line, mu, sd, amp, lo, hi, color=MEAN_COLOR, width=3):
    """수직선 위에 세운 종 모양. amp 는 꼭대기 높이(화면 단위)."""
    xs = np.linspace(lo, hi, 90)
    pts = [line.n2p(x) + UP * (amp * exp(-0.5 * ((x - mu) / sd) ** 2)) for x in xs]
    return VMobject().set_points_smoothly(pts).set_stroke(color, width)


def curve_on_line(line, fn, amp, lo, hi, color=MEAN_COLOR, width=3, n=120):
    """수직선 위에 fn(x) × amp 높이로 그린 곡선."""
    xs = np.linspace(lo, hi, n)
    pts = [line.n2p(x) + UP * (amp * fn(x)) for x in xs]
    return VMobject().set_points_smoothly(pts).set_stroke(color, width)


def band_on_line(line, fn, amp, a, b, color=MEAN_COLOR, opacity=0.5, n=60):
    """수직선 위 곡선 fn 아래, a 부터 b 까지의 띠."""
    xs = np.linspace(a, b, n)
    top = [line.n2p(x) + UP * (amp * fn(x)) for x in xs]
    base = [line.n2p(b), line.n2p(a)]
    return Polygon(*top, *base).set_fill(color, opacity).set_stroke(width=0)


def chi2_pdf(x, v):
    return gamma_pdf(x, v / 2, 2.0)


def t_pdf(x, v):
    return (math.gamma((v + 1) / 2) / (sqrt(v * math.pi) * math.gamma(v / 2))
            * (1 + x * x / v) ** (-(v + 1) / 2))


def drop(scene, dots, run_time=0.5, lag=0.08):
    """점들을 제자리로 떨어뜨린다."""
    if len(dots) == 1:
        scene.play(dots[0].animate.move_to(dots[0].ps_target), run_time=run_time)
    else:
        scene.play(LaggedStart(*[d.animate.move_to(d.ps_target) for d in dots], lag_ratio=lag), run_time=run_time)


# ─────────────────────────────────────────────────────────────
# 1. 표본평균의 분포 — 슬라이드 9 (8.4 도입) 앞
# ─────────────────────────────────────────────────────────────
class SampleMeanAsRandomVariable(InteractiveScene):
    """모집단(치토 48, μ = 50, σ = 10)에서 n = 4 를 뽑아 x̄ 를 구하고 수직선에 점으로 떨어뜨린다. 서른 번 쌓이면
    μ 둘레의 좁은 더미가 되고 그 위에 종 모양이 선다: μ_x̄ = μ, σ_x̄ = σ/√n. n = 16 이면 더미가 절반 폭이다."""

    def construct(self):
        head = slide_title("Sampling Distribution of the Mean")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        rng = np.random.default_rng(8)
        vals = np.clip(rng.normal(50, 10, 48), 22, 78)
        people = crowd(48, 6, 8, tint="grey", height=0.34, buff=0.12, seed=3).move_to([-4.0, -1.1, 0])
        ax = density_axes((20, 80, 10), (0, 0.045, 0.01), width=4.6, height=1.3).move_to([-4.0, 1.45, 0])
        g = normal_graph(ax, 50, 10, 20, 80, MUTED, 2.5)
        pop = note("population  μ = 50, σ = 10", 22, GREY_B).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
        self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.02), run_time=1.2)
        self.play(ShowCreation(ax), ShowCreation(g), FadeIn(pop))
        self.wait(0.8)

        line = number_line(35, 65, 5, 6.0, [3.1, -2.3, 0])
        xbar = Tex(R"\bar{x}").scale(0.8).set_color(ACCENT).next_to(line, RIGHT, buff=0.25)
        self.play(ShowCreation(line), FadeIn(xbar))
        pile = Pile(line, bin_width=1.0)

        def sample(n, slow):
            idx = rng.choice(48, n, replace=False)
            m = float(vals[idx].mean())
            rings = VGroup(*[ring(people[i], CALM) for i in idx])
            if slow:
                self.play(LaggedStartMap(ShowCreation, rings, lag_ratio=0.15), run_time=0.6)
                value = Tex(R"\bar{x} = %.1f" % m).scale(0.75).set_color(ACCENT).move_to([0.9, -0.3, 0])
                self.play(FadeIn(value), run_time=0.3)
                d = pile.dot(m, value.get_center())
                self.add(d)
                drop(self, [d], run_time=0.5)
                self.play(FadeOut(rings), FadeOut(value), run_time=0.3)
                return []
            return [pile.dot(m, [0.9, -0.3, 0])]

        n_tag = label("n = 4", 26, CALM).move_to([3.4, 1.7, 0])
        self.play(FadeIn(n_tag))
        self.wait(0.5)
        for _ in range(5):
            sample(4, True)
        fast = []
        for _ in range(25):
            fast += sample(4, False)
        self.add(*fast)
        drop(self, fast, run_time=3.0, lag=0.06)
        self.wait(0.3)
        b4 = bell(line, 50, 5.0, pile.height() + 0.15, 36, 64)
        self.play(ShowCreation(b4))
        self.wait(0.8)
        f1 = Tex(R"\mu_{\bar X} = \mu").scale(0.8).set_color(MEAN_COLOR).move_to([3.0, 0.9, 0])
        f2 = Tex(R"\sigma_{\bar X} = \frac{\sigma}{\sqrt{n}}").scale(0.8).set_color(MEAN_COLOR).next_to(f1, DOWN, buff=0.3).align_to(f1, LEFT)
        self.play(Write(f1))
        self.play(Write(f2))
        self.wait(1.5)

        # n = 16
        self.play(FadeOut(pile.dots), FadeOut(b4), FadeOut(n_tag))
        pile = Pile(line, bin_width=1.0, color=CALM)
        n_tag = label("n = 16", 26, CALM).move_to([3.4, 1.7, 0])
        self.play(FadeIn(n_tag))
        idx = rng.choice(48, 16, replace=False)
        rings = VGroup(*[ring(people[i], CALM) for i in idx])
        self.play(LaggedStartMap(ShowCreation, rings, lag_ratio=0.05), run_time=0.8)
        self.wait(0.3)
        self.wait(0.4)
        self.play(FadeOut(rings), run_time=0.3)
        fast = []
        for _ in range(30):
            fast += sample(16, False)
        self.add(*fast)
        drop(self, fast, run_time=3.0, lag=0.06)
        b16 = bell(line, 50, 2.5, pile.height() + 0.15, 40, 60, CALM)
        self.play(ShowCreation(b16))
        self.wait(0.6)
        narrow = label("half the spread", 24, CALM).next_to(n_tag, RIGHT, buff=0.5)
        self.play(FadeIn(narrow))
        self.wait(1.2)
        self.play(FlashAround(VGroup(f1, f2), color=MEAN_COLOR, buff=0.15))
        self.wait(3.0)


# ─────────────────────────────────────────────────────────────
# 2. 중심극한정리 — 슬라이드 10 (정리 8.2) 앞
# ─────────────────────────────────────────────────────────────
class CentralLimitTheorem(InteractiveScene):
    """치우친 모집단(값 1–6, 확률 0.40 … 0.04)에서 n 개를 뽑아 평균 낸 x̄ 의 분포를 n = 1, 2, 5, 30 으로 보인다.
    분포는 정확한 합성곱으로 구한다. 막대마다 평균 μ, 표준편차 σ/√n 인 정규곡선을 얹으면 n = 30 에서 막대 끝을 지난다."""
    P = [0.40, 0.25, 0.15, 0.10, 0.06, 0.04]

    def mean_pmf(self, n):
        pmf = np.array([1.0])
        base = np.array(self.P)
        for _ in range(n):
            pmf = np.convolve(pmf, base)
        xs = [(n + k) / n for k in range(len(pmf))]       # 합 n … 6n 을 n 으로 나눈 x̄
        return xs, pmf

    def construct(self):
        head = slide_title("Central Limit Theorem")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        mu = sum((i + 1) * p for i, p in enumerate(self.P))
        var = sum((i + 1) ** 2 * p for i, p in enumerate(self.P)) - mu ** 2
        sig = sqrt(var)

        # 모집단 — 왼쪽 위 작은 막대
        pax = density_axes((0.5, 6.5, 1), (0, 0.5, 0.1), width=4.2, height=1.5).move_to([-4.3, 1.45, 0])
        pbars = VGroup()
        for i, p in enumerate(self.P):
            x = i + 1
            r = Polygon(pax.c2p(x - 0.4, 0), pax.c2p(x - 0.4, p), pax.c2p(x + 0.4, p), pax.c2p(x + 0.4, 0))
            pbars.add(r.set_fill(MUTED, 0.7).set_stroke(MUTED, 1.5))
        pnums = x_marks(pax, [1, 2, 3, 4, 5, 6])
        ptag = label("population: skewed", 22, GREY_B).next_to(pax, UP, buff=0.08).align_to(pax, LEFT)
        pval = Tex(R"\mu = %.2f,\ \sigma = %.2f" % (mu, sig)).scale(0.6).set_color(GREY_B).next_to(ptag, RIGHT, buff=0.4)
        self.play(ShowCreation(pax), LaggedStartMap(GrowFromEdge, pbars, edge=DOWN, lag_ratio=0.1), FadeIn(pnums), FadeIn(ptag))
        self.play(Write(pval))
        self.wait(1.5)

        shown = None
        for n in (1, 2, 3, 5, 10, 30):
            xs, pmf = self.mean_pmf(n)
            sd = sig / sqrt(n)
            curve_fn = lambda x, sd=sd, n=n: npdf(x, mu, sd) / n
            ymax = max(max(pmf), max(curve_fn(x) for x in np.linspace(1, 6, 200))) * 1.15
            axes = density_axes((0.5, 6.5, 1), (0, ymax, ymax / 4), width=8.6, height=3.1).move_to([-1.0, -1.35, 0])
            bars = VGroup()
            w = 0.5 / n
            for x, p in zip(xs, pmf):
                if p < 1e-6:
                    continue
                r = Polygon(axes.c2p(x - w, 0), axes.c2p(x - w, p), axes.c2p(x + w, p), axes.c2p(x + w, 0))
                bars.add(r.set_fill(ACCENT, 0.55).set_stroke(ACCENT, 1.0 if n > 5 else 1.5))
            nums = x_marks(axes, [1, 2, 3, 4, 5, 6])
            tag = label("n = %d" % n, 30, ACCENT).move_to([4.6, 1.6, 0])
            sub = Tex(R"\bar{X}:\ \mu_{\bar X} = %.2f,\ \sigma_{\bar X} = %.2f" % (mu, sd)).scale(0.6).set_color(INK).next_to(tag, DOWN, buff=0.3)
            curve = axes.get_graph(curve_fn, x_range=(1, 6, 0.02)).set_stroke(MEAN_COLOR, 3)
            if shown is None:
                self.play(ShowCreation(axes), FadeIn(nums), FadeIn(tag), FadeIn(sub))
                self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.1), run_time=1.0)
            else:
                self.play(FadeOut(shown), FadeIn(VGroup(axes, nums, tag, sub)), run_time=0.6)
                self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.5 / len(bars)), run_time=1.2)
            self.play(ShowCreation(curve), run_time=1.0)
            shown = VGroup(axes, nums, tag, sub, bars, curve)
            self.wait(1.8 if n < 30 else 0.8)

        fits = label("n ≥ 30: approximately normal", 24, MEAN_COLOR).move_to([4.6, 0.1, 0])
        self.play(FadeIn(fits))
        self.wait(0.6)
        z = Tex(R"Z = \frac{\bar X - \mu}{\sigma/\sqrt{n}}").scale(0.85).set_color(MEAN_COLOR).move_to([4.6, -1.0, 0])
        self.play(Write(z))
        self.play(FlashAround(z, color=MEAN_COLOR, buff=0.12))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 3. S² 의 표본분포 — 슬라이드 22 (8.5) 앞
# ─────────────────────────────────────────────────────────────
class ChiSquareFromVariance(InteractiveScene):
    """정규 모집단(μ = 50, σ = 10)에서 n = 5 를 뽑아 s² 를 구하고 (n − 1)s²/σ² 를 수직선 0–20 에 점으로 떨어뜨린다.
    쌓인 더미는 오른쪽으로 긴 χ²(4) 다. v = 10 이면 오른쪽으로 옮겨 가며 평평해진다(평균 v).
    v = 4 의 가운데 95 % 띠는 표 A.5 의 0.484 와 11.143 사이다."""

    def construct(self):
        head = slide_title("Sampling Distribution of S²")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        rng = np.random.default_rng(21)
        sigma = 10.0

        ax = density_axes((20, 80, 10), (0, 0.045, 0.01), width=5.4, height=1.9).move_to([-3.9, 1.2, 0])
        g = normal_graph(ax, 50, sigma, 20, 80, MUTED, 2.5)
        pop = Tex(R"\text{population}\ n(x;\,\mu = 50,\ \sigma = 10)").scale(0.6).set_color(GREY_B).next_to(ax, UP, buff=0.08)
        self.play(ShowCreation(ax), ShowCreation(g), FadeIn(pop))

        s_def = Tex(R"s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)^2").scale(0.6).set_color(INK).move_to([3.7, 1.9, 0])
        stat = Tex(R"\chi^2 = \frac{(n-1)s^2}{\sigma^2}").scale(0.75).set_color(MEAN_COLOR).next_to(s_def, DOWN, buff=0.35).align_to(s_def, LEFT)
        n_tag = label("n = 5", 26, CALM).next_to(stat, DOWN, buff=0.3).align_to(s_def, LEFT)
        self.play(Write(s_def), Write(stat), FadeIn(n_tag))
        self.wait(1.5)

        line = number_line(0, 20, 2, 9.0, [-0.6, -2.5, 0])
        chi = Tex(R"\chi^2").scale(0.8).set_color(MEAN_COLOR).next_to(line, RIGHT, buff=0.25)
        self.play(ShowCreation(line), FadeIn(chi))
        pile = Pile(line, bin_width=0.5, step=0.12, radius=0.05, color=ACCENT)

        def one(slow):
            x = rng.normal(50, sigma, 5)
            s2 = float(x.var(ddof=1))
            c = 4 * s2 / sigma ** 2
            c = min(c, 19.5)
            if slow:
                dots = VGroup(*[Dot(radius=0.06).set_fill(CALM, 1).move_to(ax.c2p(v, 0)) for v in x])
                self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.15), run_time=0.5)
                val = Tex(R"s^2 = %.1f" % s2).scale(0.65).set_color(CALM).move_to([2.4, -0.3, 0])
                cv = Tex(R"\chi^2 = \frac{4 \times %.1f}{100} = %.2f" % (s2, c)).scale(0.6).set_color(MEAN_COLOR).next_to(val, DOWN, buff=0.25).align_to(val, LEFT)
                self.play(FadeIn(val), run_time=0.3)
                self.play(Write(cv), run_time=0.6)
                d = pile.dot(c, cv.get_left() + RIGHT * 0.3)
                self.add(d)
                drop(self, [d], run_time=0.5)
                self.play(FadeOut(dots), FadeOut(val), FadeOut(cv), run_time=0.3)
                return []
            return [pile.dot(c, [3.7, -0.4, 0])]

        for _ in range(5):
            one(True)
        fast = []
        for _ in range(67):
            fast += one(False)
        self.add(*fast)
        drop(self, fast, run_time=4.5, lag=0.03)
        self.wait(0.5)

        amp = 72 * 0.5 * 0.12          # 점 48 개 × 칸 폭 0.5 × 점 간격 → 밀도를 화면 높이로
        c4 = curve_on_line(line, lambda x: chi2_pdf(x, 4), amp, 0.05, 20, MEAN_COLOR)
        v4 = label("v = n − 1 = 4", 24, MEAN_COLOR).move_to([-1.2, 0.1, 0])
        self.play(ShowCreation(c4), FadeIn(v4))
        self.wait(1.5)
        c10 = curve_on_line(line, lambda x: chi2_pdf(x, 10), amp, 0.05, 20, CALM)
        v10 = label("v = 10", 24, CALM).next_to(v4, RIGHT, buff=0.6)
        mean_v = label("mean = v", 24, GREY_B).next_to(v10, RIGHT, buff=0.6)
        self.play(ShowCreation(c10), FadeIn(v10))
        self.play(FadeIn(mean_v))
        self.wait(1.5)

        self.play(FadeOut(c10), FadeOut(v10), FadeOut(mean_v), pile.dots.animate.set_opacity(0.25))
        band = band_on_line(line, lambda x: chi2_pdf(x, 4), amp, 0.484, 11.143, MEAN_COLOR, 0.45)
        lo = Tex(R"\chi^2_{0.975} = 0.484").scale(0.6).set_color(WARN).move_to([-3.6, -0.5, 0])
        hi = Tex(R"\chi^2_{0.025} = 11.143").scale(0.6).set_color(WARN).move_to([3.4, -0.9, 0])
        m_lo = dashed(line.n2p(0.484), line.n2p(0.484) + UP * 1.6, WARN)
        m_hi = dashed(line.n2p(11.143), line.n2p(11.143) + UP * 1.0, WARN)
        mid = label("95 % between", 24, MEAN_COLOR).move_to([-1.2, -0.5, 0])
        self.play(FadeIn(band), ShowCreation(m_lo), ShowCreation(m_hi))
        self.wait(0.8)
        self.play(Write(lo), Write(hi), FadeIn(mid))
        src = note("Table A.5", 22, GREY_B).next_to(hi, DOWN, buff=0.15).align_to(hi, LEFT)
        self.play(FadeIn(src))
        self.wait(3.5)


# ─────────────────────────────────────────────────────────────
# 4. t 분포 — 슬라이드 26 (8.6 도입) 앞
# ─────────────────────────────────────────────────────────────
class TDistributionTails(InteractiveScene):
    """Z 는 σ 가 고정이고 T 는 표본마다 S 가 달라진다. 같은 표본(n = 5)으로 z 와 t 를 구해 두 수직선에 떨어뜨리면 t 가
    더 넓게 흩어진다. 곡선은 v = 2, 5 가 표준정규보다 꼬리가 두껍고 v → ∞ 에서 포개진다. 오른쪽 꼬리 0.025 를 자르는
    값은 z = 1.960, t(14) = 2.145 로 t 쪽이 더 오른쪽이다."""

    def construct(self):
        head = slide_title("t-Distribution")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        rng = np.random.default_rng(14)

        z_eq = Tex(R"Z = \frac{\bar X - \mu}{\sigma/\sqrt{n}}").scale(0.8).set_color(CALM).move_to([-4.2, 1.5, 0])
        z_note = label("σ fixed", 24, CALM).next_to(z_eq, RIGHT, buff=0.5)
        self.play(Write(z_eq), FadeIn(z_note))
        t_eq = Tex(R"T = \frac{\bar X - \mu}{S/\sqrt{n}}").scale(0.8).set_color(WARN).move_to([-4.2, -0.3, 0])
        t_note = label("S varies", 24, WARN).next_to(t_eq, RIGHT, buff=0.5)
        self.play(Write(t_eq), FadeIn(t_note))
        self.wait(0.8)

        # S 눈금: 표본마다 다른 값
        gauge = number_line(4, 16, 4, 2.6, [-3.4, -1.7, 0], font_size=18)
        s_lab = Tex("S").scale(0.7).set_color(WARN).next_to(gauge, LEFT, buff=0.2)
        marker = Triangle().set_height(0.22).rotate(PI).set_fill(WARN, 1).set_stroke(width=0)
        marker.next_to(gauge.n2p(10), UP, buff=0.03)
        self.play(ShowCreation(gauge), FadeIn(s_lab), FadeIn(marker))

        zl = number_line(-6, 6, 2, 6.0, [3.4, 1.2, 0])
        tl = number_line(-6, 6, 2, 6.0, [3.4, -1.3, 0])
        zt = Tex("z").scale(0.7).set_color(CALM).next_to(zl, LEFT, buff=0.2)
        tt = Tex("t").scale(0.7).set_color(WARN).next_to(tl, LEFT, buff=0.2)
        self.play(ShowCreation(zl), ShowCreation(tl), FadeIn(zt), FadeIn(tt))
        zp = Pile(zl, bin_width=0.4, step=0.12, radius=0.05, color=CALM)
        tp = Pile(tl, bin_width=0.4, step=0.12, radius=0.05, color=WARN)

        for k in range(28):
            x = rng.normal(50, 10, 5)
            xb, s = float(x.mean()), float(x.std(ddof=1))
            z = (xb - 50) / (10 / sqrt(5))
            t = (xb - 50) / (s / sqrt(5))
            t = max(-5.9, min(5.9, t))
            dz = zp.dot(z, zl.n2p(0) + UP * 1.3)
            dt = tp.dot(t, tl.n2p(0) + UP * 1.3)
            self.add(dz, dt)
            if k < 8:
                self.play(marker.animate.next_to(gauge.n2p(min(16, max(4, s))), UP, buff=0.03), run_time=0.3)
                drop(self, [dz, dt], run_time=0.45, lag=0.0)
            else:
                drop(self, [dz, dt], run_time=0.18, lag=0.0)
        wide = label("heavier tails", 24, WARN).next_to(tl, DOWN, buff=0.45)
        self.play(FadeIn(wide))
        self.wait(2.2)

        # 곡선 — v = 2, 5, ∞
        self.play(FadeOut(VGroup(gauge, s_lab, marker, zl, tl, zt, tt, zp.dots, tp.dots, wide, z_note, t_note)),
                  z_eq.animate.scale(0.75).move_to([-5.2, 1.9, 0]), t_eq.animate.scale(0.75).move_to([-5.2, 0.6, 0]))
        axes = density_axes((-5, 5, 1), (0, 0.45, 0.1), width=8.6, height=3.1).move_to([-0.6, -1.35, 0])
        nums = x_marks(axes, [-4, -2, 0, 2, 4])
        self.play(ShowCreation(axes), FadeIn(nums))
        gz = axes.get_graph(lambda x: npdf(x), x_range=(-5, 5, 0.02)).set_stroke(CALM, 3)
        g2 = axes.get_graph(lambda x: t_pdf(x, 2), x_range=(-5, 5, 0.02)).set_stroke(WARN, 3)
        g5 = axes.get_graph(lambda x: t_pdf(x, 5), x_range=(-5, 5, 0.02)).set_stroke(ACCENT, 3)
        l_inf = label("v → ∞: standard normal", 22, CALM).move_to([4.6, 1.5, 0])
        l2 = label("v = 2", 22, WARN).next_to(l_inf, DOWN, buff=0.25).align_to(l_inf, LEFT)
        l5 = label("v = 5", 22, ACCENT).next_to(l2, DOWN, buff=0.25).align_to(l_inf, LEFT)
        self.play(ShowCreation(gz), FadeIn(l_inf))
        self.play(ShowCreation(g2), FadeIn(l2))
        self.play(ShowCreation(g5), FadeIn(l5))
        self.wait(2.0)

        # 꼬리 0.025 — z 와 t(14)
        self.play(FadeOut(g2), FadeOut(g5), FadeOut(l2), FadeOut(l5))
        g14 = axes.get_graph(lambda x: t_pdf(x, 14), x_range=(-5, 5, 0.02)).set_stroke(WARN, 3)
        l14 = label("v = 14", 22, WARN).next_to(l_inf, DOWN, buff=0.25).align_to(l_inf, LEFT)
        self.play(ShowCreation(g14), FadeIn(l14))
        tail_z = area_under(axes, gz, 1.960, 5, CALM, 0.55)
        tail_t = area_under(axes, g14, 2.145, 5, WARN, 0.45)
        self.play(FadeIn(tail_z), FadeIn(tail_t))
        self.wait(0.8)
        area = label("right tail area 0.025", 22, GREY_B).next_to(l14, DOWN, buff=0.35).align_to(l_inf, LEFT)
        zc = Tex(R"z_{0.025} = 1.960").scale(0.65).set_color(CALM).next_to(area, DOWN, buff=0.25).align_to(l_inf, LEFT)
        tc = Tex(R"t_{0.025} = 2.145\ (v = 14)").scale(0.65).set_color(WARN).next_to(zc, DOWN, buff=0.2).align_to(l_inf, LEFT)
        mz = dashed(axes.c2p(1.960, 0), axes.c2p(1.960, 0.16), CALM)
        mt = dashed(axes.c2p(2.145, 0), axes.c2p(2.145, 0.22), WARN)
        self.play(FadeIn(area), Write(zc), ShowCreation(mz))
        self.play(Write(tc), ShowCreation(mt))
        further = label("t cutoff further right", 22, WARN).next_to(axes.c2p(2.145, 0.22), UR, buff=0.1)
        self.play(FadeIn(further), FlashAround(tc, color=WARN, buff=0.08))
        self.wait(3.5)
