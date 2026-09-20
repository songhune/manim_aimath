# -*- coding: utf-8 -*-
"""BD_05 (오픈 API를 이용한 빅데이터 크롤링) 영상 5편의 클릭 진행형 판.

    python tools/build_slides_site.py --chapter bd_05 --module _2026/bigdata/slides_bd_05.py

씬 정의는 `_2026/bigdata/bigdata_week04.py` 에 있다. 끊는 규칙은 `_2026/aimath/slides_common.py` 참고.
장 번호는 주차가 아니라 교재 장 번호다(하네스 3.6).

`PagingLoop` 과 `MonthlyCollection` 은 0.1~0.3초짜리 play 가 수십 번 이어진다. 기본 `min_step`(0.8초)으로
끊으면 한 영상이 수십 클릭이 되므로 올려 둔다. 그래도 씬 안의 긴 `wait()` 는 경계로 남는다.
"""
# manim_slides 를 먼저 들여온다. 이유는 `_2026/aimath/slides_am_00.py` 의 주석과 같다.
from _2026.aimath.slides_common import build
from _2026.bigdata import bigdata_week04

PAGES = build(globals(), [
    ("RequestUrlAssembly", "요청 URL 조립"),
    ("HeaderAndStatus", "인증 헤더와 상태 코드"),
    ("JsonToRecord", "응답에서 항목 고르기"),
    ("PagingLoop", "100건씩 수집"),
    ("MonthlyCollection", "월별 수집"),
], (bigdata_week04,), step_at={"PagingLoop": 6.0, "MonthlyCollection": 30.0})
