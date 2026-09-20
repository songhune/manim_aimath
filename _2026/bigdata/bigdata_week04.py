"""빅데이터개론 및 분석 — 오픈 API를 이용한 빅데이터 크롤링 보조 영상.

강의자료 `빅데이터개론및분석/[0921]오픈 API를 이용한 빅데이터 크롤링.pptx` 의 시각화 보조자료.
덱의 코드(프로그램 5-1 `nvCrawler.py`, 5-2 `openapi_tour.py`)가 한 줄씩 하는 일을
그 줄이 만드는 산출물로 보여 준다.

소재 규칙(하네스 3.8): 개념을 상자와 화살표로 옮기지 않는다. 화면에 나가는 것은 실제 문자열,
실제 응답, 실제 수치다.
    data/naver_news_sample.json   2026-09-20 네이버 검색 API 실제 응답(200 과 401). 인증키 없음
    data/tour_china_2017_2021.csv 같은 날 출입국관광통계서비스에서 받은 60 개월 값
URL·퍼센트 인코딩·날짜 변환은 씬 안에서 덱과 같은 코드로 계산한다.

렌더 (저장소 루트에서):
    ./render.sh list  _2026/bigdata/bigdata_week04.py
    ./render.sh check _2026/bigdata/bigdata_week04.py
    ./render.sh ppt   _2026/bigdata/bigdata_week04.py PagingLoop
    ./render.sh all   _2026/bigdata/bigdata_week04.py

긴 `self.wait()`(1초 이상)는 동작 단위의 경계다. 클릭 진행형 페이지를 만들 때 그 자리에서 끊는다
(`_2026/probstat/slides_poc.py` 의 `_StepSlide`).
"""
import csv
import datetime
import json
import os
import re
import urllib.parse

from manim_imports_ext import *


# ─────────────────────────────────────────────────────────────
# 강의자료(아주대 템플릿)와 같은 서체·색을 쓴다. bigdata_week01.py 와 같은 약속이다.
# ─────────────────────────────────────────────────────────────
TITLE_FONT = "Ajou"
BODY_FONT = "Arita Buri KR"
CODE_FONT = "D2Coding"

INK = GREY_A
ACCENT = BLUE_B        # 자료·정상 응답
WARN = RED_C           # 오류 응답·중단
CALM = TEAL_B          # 이름표
GOLD_ = YELLOW         # 코드가 채워 넣는 값

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "data", "naver_news_sample.json"), encoding="utf-8") as _f:
    SAMPLE = json.load(_f)
with open(os.path.join(HERE, "data", "tour_china_2017_2021.csv"), encoding="utf-8") as _f:
    TOUR = [(row["yyyymm"], int(row["visit_cnt"])) for row in csv.DictReader(_f)]


def title(text, size=42):
    return Text(text, font=TITLE_FONT, font_size=size).set_color(WHITE)


def body(text, size=30, color=INK):
    return Text(text, font=BODY_FONT, font_size=size).set_color(color)


def mono(text, size=24, color=INK):
    """코드와 자료. 화면 문구가 아니라 덱의 코드·서버가 돌려준 글자 그대로다.

    한글이 든 줄은 본문 서체로 그린다. manimgl 이 D2Coding 의 'ㅔ' 음절(데·레·헤·네·세·메·테·페)을
    속이 빈 윤곽선으로 그리기 때문이다(2026-09-20, Windows 에서 확인). Arita Buri KR 과 Ajou 는
    멀쩡하다. 글자 단위로 잘라 쓰는 URL 문자열에는 한글이 없으므로 조각 계산은 그대로다.
    """
    font = BODY_FONT if re.search("[가-힣]", text) else CODE_FONT
    return Text(text, font=font, font_size=size).set_color(color)


def slide_title(text):
    """왼쪽 위 제목 + 밑줄. 강의 슬라이드 제목 위치와 맞춘다."""
    t = title(text).to_corner(UL, buff=0.5)
    rule = Line(LEFT, RIGHT)
    rule.set_width(FRAME_WIDTH - 1.0).set_stroke(GREY_C, 2)
    rule.next_to(t, DOWN, buff=0.2).align_to(t, LEFT)
    return VGroup(t, rule)


def note(text, size=22, corner=DR):
    t = body(text, size, GREY_C)
    t.to_corner(corner, buff=0.35)
    return t


def code_lines(lines, size=19, buff=0.16, indent=0.22):
    """(들여쓰기 단계, 글, 색) 목록을 왼쪽 맞춤으로 쌓는다.

    Pango 는 줄 앞의 빈칸을 그리지 않는다. 들여쓰기는 글이 아니라 자리 옮김으로 준다.
    """
    group = VGroup(*[mono(text, size, color) for _, text, color in lines])
    group.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    for (level, _, _), mob in zip(lines, group):
        mob.shift(level * indent * RIGHT)
    return group


def clip(text, n):
    return text if len(text) <= n else text[:n - 1] + "…"


def fill_slots(before, template, values, size, color=GOLD_):
    """`"...%s..." % values` 가 하는 일을 글자 단위로 옮긴다.

    before 는 template 을 그린 mono 글이다. 돌려주는 것은 (채운 뒤의 글, 애니메이션 목록 함수).
    빈칸이 없는 글자 열만 다룬다. Pango 글리프 수와 글자 수가 같아야 조각을 자를 수 있다.
    """
    pieces = template.split("%s")
    assert len(pieces) == len(values) + 1
    after_text = pieces[0]
    for piece, (value, _) in zip(pieces[1:], values):
        after_text += value + piece
    after = mono(after_text, size)
    assert len(before) == len(template) and len(after) == len(after_text)
    after.shift(before[0].get_center() - after[0].get_center())

    anims, b, a = [], 0, 0
    for i, piece in enumerate(pieces):
        n = len(piece)
        if n:
            anims.append(ReplacementTransform(before[b:b + n], after[a:a + n]))
        b, a = b + n, a + n
        if i < len(values):
            value, source = values[i]
            after[a:a + len(value)].set_color(color)
            anims.append(FadeOut(before[b:b + 2]))
            anims.append(ReplacementTransform(source, after[a:a + len(value)]))
            b, a = b + 2, a + len(value)
    return after, anims


# ─────────────────────────────────────────────────────────────
# 1. 요청 URL 조립 — 덱 P.20 getNaverSearch() 의 02–06행
# ─────────────────────────────────────────────────────────────
class RequestUrlAssembly(InteractiveScene):
    """`base + node + parameters` 가 만드는 문자열을 글자 단위로 따라간다.

    검색어의 퍼센트 인코딩은 urllib.parse.quote 로 씬 안에서 계산한다. 한글 한 글자가
    UTF-8 세 바이트가 되고 바이트마다 %XX 가 되는 것을 보이는 것이 이 영상의 몫이다.
    """

    def construct(self):
        head = slide_title("요청 URL 조립")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        query = SAMPLE["query"]
        encoded = urllib.parse.quote(query)
        templates = [
            ("base", "https://openapi.naver.com/v1/search"),
            ("node", "/%s.json"),
            ("parameters", "?query=%s&start=%s&display=%s"),
        ]
        size = 23
        names, rows = VGroup(), VGroup()
        for i, (name, text) in enumerate(templates):
            label = mono(name, size, CALM)
            label.move_to([-6.45, 2.1 - 0.85 * i, 0], LEFT)
            value = mono(text, size)
            value.move_to([-4.4, 2.1 - 0.85 * i, 0], LEFT)
            names.add(label)
            rows.add(value)
        self.play(LaggedStart(*[FadeIn(VGroup(n, r), shift=0.2 * RIGHT)
                                for n, r in zip(names, rows)], lag_ratio=0.3))
        self.wait(1)

        # node = "/%s.json" % node
        news = mono("news", size, GOLD_)
        news.next_to(rows[1], RIGHT, buff=1.2)
        self.play(FadeIn(news, shift=0.2 * LEFT))
        node_after, anims = fill_slots(rows[1], templates[1][1], [("news", news)], size)
        self.play(*anims, run_time=1.2)
        self.wait(1)

        # urllib.parse.quote(srcText): 한글 한 글자 → UTF-8 3바이트 → %XX 세 개
        call = mono("urllib.parse.quote(srcText)", 22, CALM)
        call.move_to([-6.45, -0.75, 0], LEFT)
        chars = VGroup(*[body(ch, 44, WHITE) for ch in query])
        chars.arrange(RIGHT, buff=2.2).move_to([0.2, -1.55, 0])
        self.play(FadeIn(call), LaggedStart(*[FadeIn(c) for c in chars], lag_ratio=0.2))

        hexes, percents = VGroup(), VGroup()
        for ch, mob in zip(query, chars):
            raw = ch.encode("utf-8")
            hx = mono(" ".join("%02X" % b for b in raw), 24, ACCENT)
            hx.next_to(mob, DOWN, buff=0.35)
            pc = mono(urllib.parse.quote(ch), 24, GOLD_)
            pc.move_to(hx)
            hexes.add(hx)
            percents.add(pc)
        caption = body("UTF-8 바이트 3개씩", 26, GREY_B)
        caption.next_to(hexes, DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(h, shift=0.2 * DOWN) for h in hexes], lag_ratio=0.2),
                  FadeIn(caption))
        self.wait(1)
        self.play(*[FadeTransform(h, p) for h, p in zip(hexes, percents)])
        self.wait(1)

        joined = mono(encoded, size, GOLD_)
        joined.move_to([0.2, -2.35, 0])
        assert len(joined) == len(encoded)
        self.play(*[ReplacementTransform(p, joined[9 * i:9 * i + 9]) for i, p in enumerate(percents)],
                  FadeOut(chars), FadeOut(caption), FadeOut(call))

        # parameters = "?query=%s&start=%s&display=%s" % (quote(srcText), start, display)
        start = mono("1", size, GOLD_)
        display = mono("100", size, GOLD_)
        start_name = mono("start", 20, CALM)
        display_name = mono("display", 20, CALM)
        start.move_to([3.0, -2.35, 0])
        display.move_to([4.6, -2.35, 0])
        start_name.next_to(start, DOWN, buff=0.2)
        display_name.next_to(display, DOWN, buff=0.2)
        self.play(FadeIn(VGroup(start, start_name)), FadeIn(VGroup(display, display_name)),
                  joined.animate.move_to([-2.2, -2.35, 0]))
        par_after, anims = fill_slots(
            rows[2], templates[2][1],
            [(encoded, joined), ("1", start), ("100", display)], size)
        self.play(*anims, FadeOut(start_name), FadeOut(display_name), run_time=1.6)
        self.wait(1)

        # url = base + node + parameters
        full = templates[0][1] + "/news.json" + "?query=%s&start=%s&display=%s" % (encoded, 1, 100)
        assert full == SAMPLE["request_url"]
        url = mono(full, 16)
        url.set_width(FRAME_WIDTH - 1.6)
        url.move_to([0, -2.0, 0])
        assert len(url) == len(full)
        cuts = [0, len(templates[0][1]), len(templates[0][1]) + len("/news.json"), len(full)]
        colors = [ACCENT, WHITE, GOLD_]
        for lo, hi, color in zip(cuts[:-1], cuts[1:], colors):
            url[lo:hi].set_color(color)
        url_name = mono("url = base + node + parameters", 22, CALM)
        url_name.next_to(url, UP, buff=0.45).align_to(url, LEFT)
        self.play(FadeIn(url_name))
        sources = [rows[0], node_after, par_after]
        self.play(*[ReplacementTransform(src.copy(), url[lo:hi])
                    for src, lo, hi in zip(sources, cuts[:-1], cuts[1:])], run_time=1.8)
        marks = VGroup()
        for (name, _), lo, hi, color in zip(templates, cuts[:-1], cuts[1:], colors):
            bar = Line(url[lo].get_corner(DL), url[hi - 1].get_corner(DR))
            bar.shift(0.12 * DOWN).set_stroke(color, 3)
            tag = mono(name, 18, color)
            tag.next_to(bar, DOWN, buff=0.12)
            marks.add(VGroup(bar, tag))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.3))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 2. 인증 헤더와 상태 코드 — 덱 P.18 getRequestUrl()
# ─────────────────────────────────────────────────────────────
class HeaderAndStatus(InteractiveScene):
    """같은 URL 을 헤더 없이, 헤더를 붙여 두 번 보낸다. 두 응답은 실제로 받은 것이다.

    헤더 값은 길이만 맞춘 별표다. 화면에도 자료 파일에도 인증키는 없다.
    """

    def request_lines(self, with_header):
        encoded = urllib.parse.quote(SAMPLE["query"])
        lines = [
            (0, "GET /v1/search/news.json", INK),
            (2, "?query=%s" % encoded, INK),
            (2, "&start=1&display=100", INK),
            (0, "Host: openapi.naver.com", INK),
        ]
        if with_header:
            lines += [
                (0, "X-Naver-Client-Id: " + "*" * SAMPLE["id_length"], GOLD_),
                (0, "X-Naver-Client-Secret: " + "*" * SAMPLE["secret_length"], GOLD_),
            ]
        return lines

    def block(self, lines):
        return code_lines(lines, size=20, buff=0.2)

    def outcome(self, pairs):
        """코드의 식과 그 값을 두 열로 놓는다. 화면 아래 왼쪽부터 쓴다."""
        rows = VGroup()
        for expr, value, color in pairs:
            rows.add(VGroup(mono(expr, 22, CALM), mono(value, 22, color)))
        for j, row in enumerate(rows):
            row[0].move_to([-6.45, -1.9 - 0.6 * j, 0], LEFT)
            row[1].move_to([-2.9, -1.9 - 0.6 * j, 0], LEFT)
        return rows

    def construct(self):
        head = slide_title("인증 헤더와 상태 코드")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        req_tag = body("요청", 28, CALM).move_to([-6.45, 2.35, 0], LEFT)
        res_tag = body("응답", 28, CALM).move_to([0.75, 2.35, 0], LEFT)
        request = self.block(self.request_lines(False))
        request.next_to(req_tag, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(req_tag), FadeIn(request, lag_ratio=0.1))
        self.wait(1)

        # 1) 헤더 없이 보낸 요청 — 실제로 받은 401
        bad = SAMPLE["no_header"]
        message = bad["body"]["errorMessage"]
        cut = message.index(": ") + 1
        tail = message[cut:].strip()
        paren = tail.index("(")
        bad_lines = [
            (0, "HTTP %d %s" % (bad["status"], bad["reason"]), WARN),
            (0, '{"errorMessage":', INK),
            (2, '"%s' % message[:cut], INK),
            (2, tail[:paren].strip(), INK),
            (2, '%s",' % tail[paren:], INK),
            (0, ' "errorCode": "%s"}' % bad["body"]["errorCode"], INK),
        ]
        bad_res = self.block(bad_lines)
        bad_res.next_to(res_tag, DOWN, buff=0.3, aligned_edge=LEFT)
        ghost = request.copy().set_opacity(0.6)
        self.play(ghost.animate.scale(0.3).move_to(bad_res[0]).set_opacity(0), run_time=1.0)
        self.remove(ghost)
        self.play(FadeIn(res_tag), FadeIn(bad_res, shift=0.3 * LEFT, lag_ratio=0.1))

        result = self.outcome([
            ("print(e)", "HTTP Error %d: %s" % (bad["status"], bad["reason"]), WARN),
            ("getRequestUrl(url)", "None", WARN),
        ])
        self.play(FadeIn(result, lag_ratio=0.2))
        self.wait(2)

        # 2) req.add_header() 두 줄 — 03–04행
        full_request = self.block(self.request_lines(True))
        full_request.next_to(req_tag, DOWN, buff=0.3, aligned_edge=LEFT)
        add = mono("req.add_header( )", 20, CALM)
        add.next_to(full_request, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeOut(bad_res), FadeOut(result))
        self.play(FadeIn(add), LaggedStart(*[FadeIn(line, shift=0.3 * RIGHT)
                                            for line in full_request[4:]], lag_ratio=0.4))
        self.remove(request)
        self.add(full_request)
        self.wait(1)

        ok = SAMPLE["ok"]
        ok_body = ok["body"]
        ok_lines = [
            (0, "HTTP %d %s" % (ok["status"], ok["reason"]), ACCENT),
            (0, '{"lastBuildDate": "%s",' % clip(ok_body["lastBuildDate"], 17), INK),
            (0, ' "total": %d,' % ok_body["total"], INK),
            (0, ' "start": %d,' % ok_body["start"], INK),
            (0, ' "display": %d,' % ok_body["display"], INK),
            (0, ' "items": [ … %d건 … ]}' % ok["items_received"], INK),
        ]
        ok_res = self.block(ok_lines)
        ok_res.next_to(res_tag, DOWN, buff=0.3, aligned_edge=LEFT)
        ghost = full_request.copy().set_opacity(0.6)
        self.play(ghost.animate.scale(0.3).move_to(ok_res[0]).set_opacity(0), run_time=1.0)
        self.remove(ghost)
        self.play(FadeIn(ok_res, shift=0.3 * LEFT, lag_ratio=0.1))

        result = self.outcome([
            ("response.getcode()", "%d" % ok["status"], ACCENT),
            ("getRequestUrl(url)", "response.read().decode('utf-8')", ACCENT),
        ])
        self.play(FadeIn(result, lag_ratio=0.2))
        self.add(note("2026-09-20 실제 응답"))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 3. 응답에서 항목 고르기 — 덱 P.22 getPostData()
# ─────────────────────────────────────────────────────────────
def get_post_data(post, jsonResult, cnt):
    """덱 P.22 의 getPostData() 와 같은 코드. 화면의 레코드는 이 함수가 만든 것이다."""
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description': description, 'org_link':org_link, 'link': org_link, 'pDate':pDate})
    return


class JsonToRecord(InteractiveScene):
    """응답의 items[0] 에서 값이 하나씩 레코드로 옮겨 간다. pubDate 는 옮기면서 모양이 바뀐다.

    덱 10행은 `'link': org_link` 다. 그래서 응답의 link 는 쓰이지 않고 레코드의 link 에는
    originallink 값이 들어간다. 화면은 코드가 하는 대로 그린다.
    """

    def construct(self):
        head = slide_title("응답에서 항목 고르기")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        items = SAMPLE["ok"]["body"]["items"]
        records = []
        for i, post in enumerate(items, 1):
            get_post_data(post, records, i)
        post, record = items[0], records[0]

        size, width = 21, 27
        left_tag = mono("jsonResponse['items'][0]", 22, CALM).move_to([-6.45, 2.45, 0], LEFT)
        keys = ["title", "originallink", "link", "description", "pubDate"]
        json_keys = VGroup(*[mono('"%s":' % k, size, GREY_B) for k in keys])
        json_vals = VGroup(*[mono('"%s"' % (post[k] if k == "pubDate" else clip(post[k], width)), size)
                             for k in keys])
        json_keys.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        json_keys.next_to(left_tag, DOWN, buff=0.35, aligned_edge=LEFT)
        for k, v in zip(json_keys, json_vals):
            v.next_to(k, DOWN, buff=0.08, aligned_edge=LEFT).shift(0.3 * RIGHT)
        self.play(FadeIn(left_tag),
                  LaggedStart(*[FadeIn(VGroup(k, v)) for k, v in zip(json_keys, json_vals)],
                              lag_ratio=0.15))
        self.wait(1)

        right_tag = mono("jsonResult[0]", 22, CALM).move_to([0.9, 2.45, 0], LEFT)
        out_keys = ["cnt", "title", "description", "org_link", "link", "pDate"]
        rec_keys = VGroup(*[mono("'%s':" % k, size, GREY_B) for k in out_keys])
        rec_keys.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        rec_keys.next_to(right_tag, DOWN, buff=0.35, aligned_edge=LEFT)
        rec_vals = VGroup()
        for k, key_mob in zip(out_keys, rec_keys):
            text = str(record[k]) if k == "cnt" else '"%s"' % clip(record[k], width)
            v = mono(text, size, GOLD_)
            v.next_to(key_mob, DOWN, buff=0.08, aligned_edge=LEFT).shift(0.3 * RIGHT)
            rec_vals.add(v)
        self.play(FadeIn(right_tag), FadeIn(rec_keys, lag_ratio=0.1))
        self.play(FadeIn(rec_vals[0]))

        source_of = {"title": 0, "description": 3, "org_link": 1, "link": 1}
        for k in ("title", "description", "org_link"):
            i = out_keys.index(k)
            self.play(ReplacementTransform(json_vals[source_of[k]].copy(), rec_vals[i]), run_time=0.9)
        self.wait(1)

        # 10행 'link': org_link — 응답의 link 는 쓰이지 않는다
        i = out_keys.index("link")
        unused = mono("post['link']", 16, GREY_C)
        unused.next_to(json_keys[2], RIGHT, buff=0.3)
        self.play(ReplacementTransform(json_vals[1].copy(), rec_vals[i]),
                  json_vals[2].animate.set_opacity(0.35), json_keys[2].animate.set_opacity(0.35),
                  run_time=1.0)
        self.wait(1)

        # 07–08행 strptime → strftime
        i = out_keys.index("pDate")
        moving = json_vals[4].copy()
        fmt_in = mono("strptime  '%a, %d %b %Y %H:%M:%S +0900'", 19, CALM)
        fmt_out = mono("strftime  '%Y-%m-%d %H:%M:%S'", 19, CALM)
        formats = VGroup(fmt_in, fmt_out).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        formats.move_to([-6.45, -3.35, 0], LEFT)
        self.play(FadeIn(formats, lag_ratio=0.3))
        self.play(ReplacementTransform(moving, rec_vals[i]), run_time=1.4)
        self.wait(2)

        # 세 건을 돌고 난 jsonResult
        table_tag = mono("jsonResult", 20, CALM)
        rows = VGroup()
        for r in records:
            row = VGroup(mono("%d" % r["cnt"], 21, GOLD_),
                         mono(clip(r["title"], 30), 21),
                         mono(r["pDate"], 21, GOLD_))
            rows.add(row)
        for row in rows:
            row[0].move_to([-6.2, 0, 0], LEFT)
            row[1].move_to([-5.6, 0, 0], LEFT)
            row[2].move_to([3.2, 0, 0], LEFT)
        for j, row in enumerate(rows):
            row.shift((1.1 - 0.8 * j) * UP)
        table_tag.move_to([-6.45, 2.0, 0], LEFT)
        self.play(FadeOut(VGroup(left_tag, json_keys, json_vals, right_tag, rec_keys, formats)),
                  FadeOut(VGroup(*[rec_vals[j] for j in (2, 3, 4)])),
                  ReplacementTransform(rec_vals[0], rows[0][0]),
                  ReplacementTransform(rec_vals[1], rows[0][1]),
                  ReplacementTransform(rec_vals[5], rows[0][2]),
                  FadeIn(table_tag))
        self.play(LaggedStart(*[FadeIn(row, shift=0.2 * UP) for row in rows[1:]], lag_ratio=0.5))
        more = mono("… items %d건" % SAMPLE["ok"]["items_received"], 21, GREY_B)
        more.next_to(rows, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(more))
        self.add(note("2026-09-20 실제 응답"))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 4. 100건씩 수집 — 덱 P.15 main() 의 10–17행
# ─────────────────────────────────────────────────────────────
class PagingLoop(InteractiveScene):
    """start 가 1, 101, … 로 옮겨 가며 100건씩 쌓이고, 1001 에서 멈춘다.

    total 은 실제 응답의 값이다. 검색 결과가 그만큼 있어도 API 가 주는 것은 앞의 1000건이다.
    """

    def construct(self):
        head = slide_title("100건씩 수집")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        total = SAMPLE["ok"]["body"]["total"]
        display = SAMPLE["ok"]["body"]["display"]
        line = NumberLine(x_range=(0, 1000, 100), width=11.0, include_numbers=False,
                          tick_size=0.06)
        line.set_stroke(GREY_B, 2)
        line.move_to([-0.6, -1.5, 0])
        ticks = VGroup()
        for v in range(0, 1001, 200):
            t = body("%d" % v, 22, GREY_B)
            t.next_to(line.n2p(v), DOWN, buff=0.2)
            ticks.add(t)
        tail = DashedLine(line.n2p(1000), line.n2p(1000) + 1.3 * RIGHT).set_stroke(GREY_C, 2)
        total_text = mono("total = %d" % total, 22, GREY_B)
        total_text.next_to(tail, DOWN, buff=0.8).align_to(tail, RIGHT)

        blocks = VGroup()
        for i in range(10):
            lo, hi = line.n2p(100 * i), line.n2p(100 * (i + 1))
            block = Rectangle(width=(hi - lo)[0] - 0.04, height=0.8)
            block.set_stroke(GREY_C, 1).set_fill(ACCENT, 0)
            block.move_to((lo + hi) / 2 + 0.6 * UP)
            blocks.add(block)
        self.play(ShowCreation(line), FadeIn(ticks), ShowCreation(tail), FadeIn(blocks),
                  FadeIn(total_text))

        def state(start, cnt, start_color=GOLD_):
            rows = VGroup(mono("start = %d" % start, 26, start_color),
                          mono("display = %d" % display, 26),
                          mono("cnt = %d" % cnt, 26, ACCENT))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            rows.move_to([-6.45, 1.75, 0], LEFT)
            return rows

        panel = state(1, 0)
        window = Rectangle(width=blocks[0].get_width() + 0.08, height=1.1)
        window.set_stroke(GOLD_, 4).move_to(blocks[0])
        call = mono("getNaverSearch(node, srcText, start, 100)", 22, CALM)
        call.move_to([-1.3, 1.75, 0], LEFT)
        self.play(FadeIn(panel), FadeIn(call), ShowCreation(window))
        self.wait(1)

        cnt = 0
        for i in range(10):
            start = 100 * i + 1
            cnt += display
            filled = state(start, cnt)
            self.play(blocks[i].animate.set_fill(ACCENT, 0.75), run_time=0.6 if i < 2 else 0.25)
            self.remove(panel)
            panel = filled
            self.add(panel)
            nxt = start + display
            moved = state(nxt, cnt, WARN if nxt == 1001 else GOLD_)
            if i < 9:
                self.play(window.animate.move_to(blocks[i + 1]), run_time=0.7 if i < 2 else 0.3)
            self.remove(panel)
            panel = moved
            self.add(panel)
            if i < 2:
                self.wait(1)

        stop = mono("if start == 1001: break", 26, WARN)
        stop.next_to(panel, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeOut(window), FadeIn(stop, shift=0.2 * RIGHT),
                  total_text.animate.set_color(WHITE))
        got = body("수집 %d건" % cnt, 30, ACCENT)
        got.next_to(blocks, UP, buff=0.3)
        self.play(FadeIn(got))
        self.add(note("검색어 %s · 2026-09-20" % SAMPLE["query"]))
        self.wait(2)


# ─────────────────────────────────────────────────────────────
# 5. 월별 수집 — 덱 P.46 getTourismStatsService() 의 07–29행
# ─────────────────────────────────────────────────────────────
class MonthlyCollection(InteractiveScene):
    """연·월 이중 반복이 한 칸씩 돌 때마다 num 이 하나 들어오고 막대가 하나 선다.

    값은 출입국관광통계서비스가 실제로 돌려준 60 개월(중국, 방한외래관광객)이다.
    """

    def construct(self):
        head = slide_title("월별 수집")
        self.play(FadeIn(head[0]), ShowCreation(head[1]))

        years = sorted({ym[:4] for ym, _ in TOUR})
        top = max(v for _, v in TOUR)

        # 위: 연 × 월 격자 (07–08행의 이중 for)
        cw, ch = 0.5, 0.36
        origin = np.array([-5.2, 2.15, 0])
        cells = {}
        grid = VGroup()
        for r, year in enumerate(years):
            tag = body(year, 20, GREY_B)
            tag.move_to(origin + [-0.7, -ch * r, 0])
            grid.add(tag)
            for m in range(12):
                cell = Rectangle(width=cw - 0.04, height=ch - 0.04)
                cell.set_stroke(GREY_D, 1).set_fill(ACCENT, 0)
                cell.move_to(origin + [cw * m, -ch * r, 0])
                cells["%s%02d" % (year, m + 1)] = cell
                grid.add(cell)
        for m in (1, 6, 12):
            tag = body("%d" % m, 18, GREY_B)
            tag.move_to(origin + [cw * (m - 1), 0.36, 0])
            grid.add(tag)
        loops = code_lines([(0, "for year in range(nStartYear, nEndYear+1):", CALM),
                            (2, "for month in range(1, 13):", CALM)], size=18, buff=0.12)
        loops.move_to([1.6, 2.2, 0], LEFT)
        self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(loops))

        # 아래: 막대그래프 (28–29행에서 쌓이는 result)
        x0, y0, w, h = -5.6, -2.85, 11.6, 2.75
        x_axis = Line([x0, y0, 0], [x0 + w, y0, 0]).set_stroke(GREY_B, 2)
        y_axis = Line([x0, y0, 0], [x0, y0 + h, 0]).set_stroke(GREY_B, 2)
        step = 200000
        y_top = step * int(np.ceil(top / step))
        y_ticks = VGroup()
        for v in range(step, y_top + 1, step):
            t = body("%d만" % (v // 10000), 18, GREY_B)
            t.next_to([x0, y0 + h * v / y_top, 0], LEFT, buff=0.12)
            y_ticks.add(t)
        x_ticks = VGroup()
        bw = w / len(TOUR)
        for r, year in enumerate(years):
            t = body(year, 18, GREY_B)
            t.move_to([x0 + bw * (12 * r + 6), y0 - 0.25, 0])
            x_ticks.add(t)
        self.play(ShowCreation(x_axis), ShowCreation(y_axis), FadeIn(y_ticks), FadeIn(x_ticks))

        def status(ym, num):
            rows = VGroup(mono("&YM=%s" % ym, 22, GOLD_), mono("num = %d" % num, 22, ACCENT))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            rows.move_to([1.6, 1.2, 0], LEFT)
            return rows

        cursor = Rectangle(width=cw + 0.04, height=ch + 0.04).set_stroke(GOLD_, 3)
        shown = None
        bars = VGroup()
        for i, (ym, num) in enumerate(TOUR):
            cell = cells[ym]
            bar = Rectangle(width=bw * 0.8, height=max(h * num / y_top, 0.01))
            bar.set_stroke(width=0).set_fill(ACCENT, 0.9)
            bar.move_to([x0 + bw * (i + 0.5), y0, 0], DOWN)
            bars.add(bar)
            text = status(ym, num)
            slow = i < 2
            if i == 0:
                cursor.move_to(cell)
                self.play(ShowCreation(cursor), FadeIn(text))
            else:
                self.remove(shown)
                self.add(text)
                cursor.move_to(cell)
            shown = text
            self.play(cell.animate.set_fill(ACCENT, 0.15 + 0.8 * num / top),
                      GrowFromEdge(bar, DOWN), run_time=0.9 if slow else 0.12)
            if slow:
                self.wait(1)

        self.play(FadeOut(cursor))
        hi = max(range(len(TOUR)), key=lambda i: TOUR[i][1])
        lo = min(range(len(TOUR)), key=lambda i: TOUR[i][1])
        marks = VGroup()
        for i, color in ((hi, GOLD_), (lo, WARN)):
            ym, num = TOUR[i]
            tag = body("%s-%s  %d" % (ym[:4], ym[4:], num), 20, color)
            tag.next_to(bars[i], UP, buff=0.15, aligned_edge=LEFT)
            bars[i].set_fill(color, 1)
            marks.add(tag)
        saved = code_lines([(0, "result  %d행" % len(TOUR), CALM),
                            (0, "중국_방한외래관광객_2017_%s.csv" % TOUR[-1][0], CALM)], size=20)
        saved.move_to([1.6, 0.25, 0], LEFT)
        self.play(FadeIn(marks), FadeIn(saved))
        self.add(note("출입국관광통계서비스 · 중국 · 방한외래관광객", size=20))
        self.wait(2)
