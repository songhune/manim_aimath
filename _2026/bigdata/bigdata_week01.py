"""빅데이터개론 및 분석 1주차 — 오리엔테이션 보조 영상.

강의자료 `빅데이터개론및분석/week01_자료/[1주차]*.md` 의 시각화 보조자료.

1주차는 오리엔테이션이므로 학기에 배울 기법의 예고로 만든다(하네스 3.8).
화면에 나가는 수치는 씬 안에서 numpy 로 실제 계산한 값이고, 자료는 합성 예시임을
화면에 밝힌다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/bigdata/bigdata_week01.py
    ./render.sh check _2026/bigdata/bigdata_week01.py
    ./render.sh ppt   _2026/bigdata/bigdata_week01.py RuleVsStatistical
    ./render.sh all   _2026/bigdata/bigdata_week01.py
"""
from manim_imports_ext import *


# ─────────────────────────────────────────────────────────────
# 강의자료(아주대 템플릿)와 같은 서체·색을 쓴다.
# ─────────────────────────────────────────────────────────────
TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"

INK = GREY_A
ACCENT = BLUE_B        # 자료·통계적 분석
WARN = RED_C           # 오분류·결측
CALM = TEAL_B          # 보조 강조
GOLD_ = YELLOW         # 사람이 정한 규칙


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def body(text, size=30, color=INK):
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def slide_title(text):
    """왼쪽 위 제목 + 밑줄. 강의 슬라이드 제목 위치와 맞춘다."""
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def note(text, size=22, corner=DR):
    """구석에 두는 예시 자료 표시. 오른쪽 항목과 겹치면 왼쪽 아래로 옮긴다."""
    t = body(text, size, GREY_C)
    t.to_corner(corner, buff=0.35)
    return t


def fmt(x, n=2):
    return ("%%.%df" % n) % x


def axis_numbers(axes, xs=(), ys=(), xfmt="%g", yfmt="%g", size=22):
    """축 눈금 숫자를 직접 놓는다.

    manimgl 의 Axes 는 y축을 만든 뒤 90도 회전시키므로 include_numbers 로 붙인
    숫자가 같이 누워서 나온다. 0 은 두 축이 겹치므로 넣지 않는다.
    """
    g = VGroup()
    for v in xs:
        t = body(xfmt % v, size, GREY_B)
        t.next_to(axes.c2p(v, 0), DOWN, buff=0.18)
        g.add(t)
    for v in ys:
        t = body(yfmt % v, size, GREY_B)
        t.next_to(axes.c2p(0, v), LEFT, buff=0.18)
        g.add(t)
    return g


# ─────────────────────────────────────────────────────────────
# 1. 규칙 기반 분석과 통계적 분석 — 10주차 분류분석 예고
# ─────────────────────────────────────────────────────────────
class RuleVsStatistical(InteractiveScene):
    """강의자료 18-1절.

    같은 산점도 위에 사람이 정한 임계값과 자료에서 추정한 경계를 차례로 얹는다.
    정확도는 씬 안에서 세어 붙이므로 그림과 수치가 어긋나지 않는다.
    학기 10주차 분류분석에서 쓰는 산점도·결정경계·정확도를 미리 보여 주는 것이 목적이다.
    """
    n = 40

    def make_data(self):
        """리뷰 길이(어절)와 긍정 단어 비율. 경계가 기울어져 있어 축 평행 규칙으로는 덜 맞는다."""
        rng = np.random.default_rng(11)
        x = rng.uniform(4, 38, self.n)
        y = rng.uniform(0.05, 0.95, self.n)
        score = 0.021 * x + y - 1.06
        label = (score > 0).astype(int)
        flip = rng.random(self.n) < 0.05          # 겹치는 영역을 만들기 위한 잡음
        label = np.where(flip, 1 - label, label)
        return x, y, label

    def fit_logistic(self, x, y, label):
        """경사하강법으로 로지스틱 회귀 계수를 구한다. 화면의 경계선은 이 값에서 나온다."""
        X = np.stack([np.ones_like(x), x / 40.0, y], axis=1)
        w = np.zeros(3)
        for _ in range(4000):
            p = 1.0 / (1.0 + np.exp(-X @ w))
            w -= 0.5 * (X.T @ (p - label)) / len(label)
        return w

    def construct(self):
        head = slide_title("규칙 기반 분석과 통계적 분석")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        x, y, label = self.make_data()

        axes = Axes(
            x_range=(0, 40, 10),
            y_range=(0, 1, 0.25),
            width=8.0,
            height=4.5,
            axis_config=dict(include_tip=False),
        )
        axes.move_to(LEFT * 2.4 + DOWN * 0.35)
        nums = axis_numbers(axes, xs=(10, 20, 30, 40),
                            ys=(0.25, 0.5, 0.75, 1.0), yfmt="%.2f")
        x_lab = body("리뷰 길이 (어절)", 24, GREY_B)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.55)
        y_lab = body("긍정 단어 비율", 24, GREY_B)
        y_lab.next_to(axes.y_axis, UP, buff=0.2).align_to(axes.y_axis, LEFT)

        self.play(ShowCreation(axes), FadeIn(nums), FadeIn(x_lab), FadeIn(y_lab))
        self.add(note("예시 자료 · n = %d" % self.n, corner=DL))

        dots = VGroup()
        for xi, yi, li in zip(x, y, label):
            d = Dot(axes.c2p(xi, yi), radius=0.075)
            d.set_fill(ACCENT if li else WARN, 1)
            dots.add(d)
        legend = VGroup(
            VGroup(Dot(radius=0.075).set_fill(ACCENT, 1), body("긍정", 24, ACCENT)),
            VGroup(Dot(radius=0.075).set_fill(WARN, 1), body("부정", 24, WARN)),
        )
        for row in legend:
            row.arrange(RIGHT, buff=0.18)
        legend.arrange(RIGHT, buff=0.6)
        legend.next_to(axes, UP, buff=0.25).align_to(axes, RIGHT)

        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.03, run_time=1.6),
                  FadeIn(legend))
        self.wait()

        panel_x = RIGHT * 4.35

        # ── ① 사람이 정한 규칙: 긍정 단어 비율 0.5 를 임계값으로
        thr = 0.5
        rule_pred = (y > thr).astype(int)
        rule_acc = float((rule_pred == label).mean())

        rule_line = Line(axes.c2p(0, thr), axes.c2p(40, thr))
        rule_line.set_stroke(GOLD_, 4)

        head1 = body("① 규칙 기반", 30, GOLD_).move_to(panel_x + UP * 2.25)
        line1 = VGroup(
            body("사람이 임계값 지정", 24, INK),
            body("긍정 단어 비율 0.5 기준", 24, INK),
            body("축에 평행한 경계", 24, INK),
        )
        line1.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        line1.next_to(head1, DOWN, buff=0.26).align_to(head1, LEFT)

        self.play(ShowCreation(rule_line))
        self.play(FadeIn(head1), FadeIn(line1))

        wrong1 = VGroup(*[
            Circle(radius=0.16).set_stroke(WARN, 3).move_to(dots[i])
            for i in range(self.n) if rule_pred[i] != label[i]
        ])
        acc1 = body("정확도 %s" % fmt(rule_acc), 28, GOLD_)
        acc1.next_to(line1, DOWN, buff=0.28).align_to(head1, LEFT)
        miss1 = body("오분류 %d개" % len(wrong1), 24, WARN)
        miss1.next_to(acc1, DOWN, buff=0.16).align_to(head1, LEFT)

        self.play(LaggedStartMap(ShowCreation, wrong1, lag_ratio=0.08))
        self.play(FadeIn(acc1), FadeIn(miss1))
        self.wait(2)

        # ── ② 자료에서 추정한 경계
        w = self.fit_logistic(x, y, label)
        stat_pred = (w[0] + w[1] * x / 40.0 + w[2] * y > 0).astype(int)
        stat_acc = float((stat_pred == label).mean())

        def boundary_y(xv):
            return -(w[0] + w[1] * xv / 40.0) / w[2]

        p0 = axes.c2p(0, np.clip(boundary_y(0), 0, 1))
        p1 = axes.c2p(40, np.clip(boundary_y(40), 0, 1))
        stat_line = Line(p0, p1).set_stroke(ACCENT, 4)

        head2 = body("② 통계적 분석", 30, ACCENT).move_to(panel_x + DOWN * 0.7)
        line2 = VGroup(
            body("자료에서 계수 추정", 24, INK),
            body("로지스틱 회귀 경계", 24, INK),
            body("기울어진 경계 허용", 24, INK),
        )
        line2.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        line2.next_to(head2, DOWN, buff=0.26).align_to(head2, LEFT)

        wrong2 = VGroup(*[
            Circle(radius=0.16).set_stroke(WARN, 3).move_to(dots[i])
            for i in range(self.n) if stat_pred[i] != label[i]
        ])
        acc2 = body("정확도 %s" % fmt(stat_acc), 28, ACCENT)
        acc2.next_to(line2, DOWN, buff=0.28).align_to(head2, LEFT)
        miss2 = body("오분류 %d개" % len(wrong2), 24, WARN)
        miss2.next_to(acc2, DOWN, buff=0.16).align_to(head2, LEFT)

        self.play(
            FadeOut(wrong1),
            rule_line.animate.set_stroke(GOLD_, 2, opacity=0.3),
        )
        self.play(ShowCreation(stat_line))
        self.play(FadeIn(head2), FadeIn(line2))
        self.play(LaggedStartMap(ShowCreation, wrong2, lag_ratio=0.1))
        self.play(FadeIn(acc2), FadeIn(miss2))
        self.wait(3)


# ─────────────────────────────────────────────────────────────
# 2. 분석 절차와 단계별 산출물 — 5·9주차 예고
# ─────────────────────────────────────────────────────────────
class AnalysisSteps(InteractiveScene):
    """강의자료 17-4절.

    같은 자료가 단계를 지날 때마다 산출물이 바뀌는 것을 보여 준다.
    표 → 결측 제거 → 히스토그램 → 산점도와 회귀직선 순으로, 학기 5주차(통계 분석)와
    9주차(회귀분석)에서 실제로 만드는 그림을 미리 보여 주는 것이 목적이다.
    수치는 모두 씬 안에서 계산한다.
    """
    n = 120

    def make_data(self):
        """방문수와 매출. 결측 몇 개를 섞어 정제 단계가 하는 일이 보이게 한다."""
        rng = np.random.default_rng(5)
        visits = rng.normal(110, 22, self.n)
        sales = 0.021 * visits + rng.normal(0.9, 0.35, self.n)
        miss = rng.choice(self.n, 8, replace=False)
        sales_raw = sales.copy()
        sales_raw[miss] = np.nan
        return visits, sales_raw

    def table(self, rows, header, highlight=None):
        """작은 미리보기 표. Text 를 격자로 놓고 머리글 아래에만 선을 긋는다."""
        grid = VGroup()
        cells = []
        for r, row in enumerate([header] + rows):
            line = VGroup()
            for c, val in enumerate(row):
                t = body(val, 24, WHITE if r == 0 else INK)
                if highlight is not None and (r - 1, c) == highlight:
                    t.set_color(WARN)
                line.add(t)
            cells.append(line)
            grid.add(line)
        widths = [1.9, 1.9, 1.7]
        for line in grid:
            for c, t in enumerate(line):
                t.set_width(min(t.get_width(), widths[c] - 0.2))
        for line in grid:
            for c, t in enumerate(line):
                t.move_to(RIGHT * sum(widths[:c]) + RIGHT * widths[c] / 2)
        grid.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        for line in grid:
            for c, t in enumerate(line):
                t.set_x(sum(widths[:c]) + widths[c] / 2)
        rule = Line(LEFT, RIGHT).set_width(sum(widths))
        rule.set_stroke(GREY_C, 2)
        rule.next_to(grid[0], DOWN, buff=0.1)
        rule.set_x(grid.get_x())
        out = VGroup(grid, rule)
        out.center()
        return out

    def construct(self):
        head = slide_title("분석 절차와 단계별 산출물")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))
        self.add(note("예시 자료 · n = %d" % self.n))

        visits, sales_raw = self.make_data()
        step_tag = body("① 수집 — 원자료", 30, CALM)
        step_tag.next_to(head[1], DOWN, buff=0.35).align_to(head[1], LEFT)
        self.play(FadeIn(step_tag))

        # ── ① 원자료 미리보기. 결측이 눈에 보인다.
        first = list(range(6))
        rows = []
        miss_at = None
        for k, i in enumerate(first):
            s = sales_raw[i]
            rows.append(["%d" % (i + 1), "%d" % round(visits[i]),
                         "NaN" if np.isnan(s) else fmt(s)])
            if np.isnan(s):
                miss_at = (k, 2)
        if miss_at is None:                    # 앞 6행에 결측이 없으면 하나를 가져온다
            j = int(np.where(np.isnan(sales_raw))[0][0])
            rows[-1] = ["%d" % (j + 1), "%d" % round(visits[j]), "NaN"]
            miss_at = (len(rows) - 1, 2)

        tbl = self.table(rows, ["행", "방문수", "매출"], highlight=miss_at)
        tbl.move_to(LEFT * 4.3 + DOWN * 0.5)
        self.play(FadeIn(tbl))
        self.wait()

        n_miss = int(np.isnan(sales_raw).sum())
        miss_note = body("결측 %d행" % n_miss, 26, WARN)
        miss_note.next_to(tbl, DOWN, buff=0.4)
        self.play(FadeIn(miss_note))
        self.wait()

        # ── ② 정제
        ok = ~np.isnan(sales_raw)
        v, s = visits[ok], sales_raw[ok]
        step2 = body("② 정제 — 결측 행 제거", 30, CALM).move_to(step_tag, LEFT)
        kept = body("%d행 → %d행" % (self.n, len(v)), 26, CALM)
        kept.move_to(miss_note, LEFT)

        clean_rows = []
        for i in range(len(v))[:6]:
            clean_rows.append(["%d" % (i + 1), "%d" % round(v[i]), fmt(s[i])])
        tbl2 = self.table(clean_rows, ["행", "방문수", "매출"])
        tbl2.move_to(tbl)

        self.play(FadeOut(step_tag), FadeIn(step2))
        self.play(FadeOut(miss_note), FadeIn(kept),
                  ReplacementTransform(tbl, tbl2))
        self.wait()
        tbl = tbl2

        # ── ③ 요약 — 히스토그램
        step3 = body("③ 요약 — 분포 확인", 30, CALM).move_to(step_tag, LEFT)
        self.play(FadeOut(step2), FadeIn(step3))

        counts, edges = np.histogram(s, bins=9)
        hax = Axes(
            x_range=(0, 6, 1),
            y_range=(0, float(counts.max()) + 4, 10),
            width=6.4,
            height=3.6,
            axis_config=dict(include_tip=False),
        )
        hax.move_to(RIGHT * 3.4 + DOWN * 0.7)
        hnums = axis_numbers(hax, xs=(1, 2, 3, 4, 5), ys=(10, 20, 30))
        hx = body("매출", 24, GREY_B).next_to(hax.x_axis, DOWN, buff=0.55)
        hy = body("빈도", 24, GREY_B).next_to(hax.y_axis, UP, buff=0.18)

        bars = VGroup()
        for i, c in enumerate(counts):
            lo, hi = edges[i], edges[i + 1]
            corner_l = hax.c2p(lo, 0)
            corner_r = hax.c2p(hi, c)
            bar = Rectangle(width=corner_r[0] - corner_l[0],
                            height=max(corner_r[1] - corner_l[1], 0.001))
            bar.set_stroke(ACCENT, 2).set_fill(ACCENT, 0.35)
            bar.move_to((corner_l + corner_r) / 2)
            bars.add(bar)

        self.play(ShowCreation(hax), FadeIn(hnums), FadeIn(hx), FadeIn(hy))
        self.play(LaggedStartMap(FadeIn, bars, lag_ratio=0.08, run_time=1.4))

        stat = body("평균 %s   표준편차 %s" % (fmt(s.mean()), fmt(s.std(ddof=1))),
                    26, ACCENT)
        stat.next_to(hax, UP, buff=0.3)
        self.play(FadeIn(stat))
        self.wait(2)

        # ── ④ 관계 — 산점도와 회귀직선
        step4 = body("④ 관계 — 회귀직선", 30, CALM).move_to(step_tag, LEFT)
        self.play(FadeOut(step3), FadeIn(step4))

        slope, intercept = np.polyfit(v, s, 1)
        r = float(np.corrcoef(v, s)[0, 1])

        sax = Axes(
            x_range=(0, 180, 60),
            y_range=(0, 5, 1),
            width=6.4,
            height=3.6,
            axis_config=dict(include_tip=False),
        )
        sax.move_to(hax)
        snums = axis_numbers(sax, xs=(60, 120, 180), ys=(1, 2, 3, 4, 5))
        sx = body("방문수", 24, GREY_B).next_to(sax.x_axis, DOWN, buff=0.55)
        sy = body("매출", 24, GREY_B).next_to(sax.y_axis, UP, buff=0.18)

        pts = VGroup(*[
            Dot(sax.c2p(vi, si), radius=0.055).set_fill(ACCENT, 0.85)
            for vi, si in zip(v, s)
        ])
        fit = Line(sax.c2p(0, intercept), sax.c2p(180, intercept + slope * 180))
        fit.set_stroke(GOLD_, 4)

        self.play(FadeOut(bars), FadeOut(stat), FadeOut(hax), FadeOut(hnums),
                  FadeOut(hx), FadeOut(hy))
        self.play(ShowCreation(sax), FadeIn(snums), FadeIn(sx), FadeIn(sy))
        self.play(LaggedStartMap(FadeIn, pts, lag_ratio=0.01, run_time=1.4))
        self.play(ShowCreation(fit))

        coef = body("기울기 %s   상관계수 %s" % (fmt(slope, 3), fmt(r)), 26, GOLD_)
        coef.next_to(sax, UP, buff=0.3)
        self.play(FadeIn(coef))
        self.wait()

        # ── ⑤ 해석
        step5 = body("⑤ 해석", 30, CALM).move_to(step_tag, LEFT)
        read = body("방문수 +100  →  매출 +%s" % fmt(slope * 100), 28, INK)
        read.next_to(tbl, DOWN, buff=0.4).align_to(tbl, LEFT)
        self.play(FadeOut(step4), FadeIn(step5))
        self.play(FadeOut(kept), FadeIn(read))
        self.wait(3)
