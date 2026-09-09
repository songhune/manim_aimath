# -*- coding: utf-8 -*-
"""클릭 진행형 영상 페이지를 만든다: 렌더(manim-slides --GL) → 변환(RevealJS 한 파일) → 목차·표.

    python tools/build_slides_site.py --chapter ps1_02 --module _2026/probstat/slides_ps1_02.py
    python tools/build_slides_site.py --chapter ps1_02 --module ... --only AdditionRule Combinations
    python tools/build_slides_site.py --chapter ps1_02 --module ... --skip-render      # 변환·목차만

만드는 것 (저장소 루트 기준)
    docs/<chapter>/<Scene>.html     씬마다 한 페이지 (영상 base64 내장, reveal.js 내장 → file:// 로도 열린다)
    docs/<chapter>/index.html       목차
    docs/<chapter>/pages.json       [{scene, title, url, slides}] — 덱에 링크를 넣을 때 읽는 표
    docs/index.html                 장 목록
    docs/.nojekyll

렌더 중간물(slides/, video)은 동기화 폴더 밖 $TMPDIR/manim_songhune_slides 에 둔다.
--GL 은 -w 를 스스로 넣으므로 다시 주지 않는다. 한 씬이 실패해도 다음 씬으로 간다.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = Path(sys.executable)
MANIM_SLIDES = PY.parent / "manim-slides"
STAGE = Path(os.environ.get("MANIM_STAGE_SLIDES", Path(tempfile.gettempdir()) / "manim_songhune_slides"))
SLIDES_DIR = STAGE / "slides"
VIDEO_DIR = STAGE / "video"
SITE = "https://songhune.github.io/manim_aimath"

# ── 과목·장 메타 ─────────────────────────────────────────────────────
# 장 이름의 앞머리(am, ps1)로 과목을 가른다. 새 장을 넣을 때 CHAPTER_TITLE 과
# SECTIONS 두 곳만 채우면 목차가 따라 만들어진다.
COURSE_OF_PREFIX = {"am": "aimath", "ps1": "probstat"}

COURSE = {
    "aimath": {
        "title": "AI기초수학",
        "sub": "아주대학교 2026-2",
        "how": "영상 하나를 동작 단위로 끊어 둔 페이지다. → 또는 스페이스(화면의 화살표 클릭)로 "
               "다음 단계, ←로 앞 단계. F를 누르면 전체 화면이다.",
        "steps": "단계",
        "back": "다른 장 보기",
    },
    "probstat": {
        "title": "Probability and Statistics",
        "sub": "Walpole 9e · Ajou University 2026 Fall",
        "how": "Each page is one animation split into steps. Press → or Space (or click the arrow) "
               "to play the next step; ← goes back. Fullscreen: F.",
        "steps": "steps",
        "back": "All chapters",
    },
}

CHAPTER_TITLE = {
    "am_00": "오리엔테이션 · 강좌소개",
    "am_01": "Chapter 01 · 연립선형방정식과 행렬",
    "am_02": "Chapter 02 · 가우스-조르당 소거법과 여러 가지 행렬",
    "ps1_02": "Chapter 2 · Probability",
}


def course_of(chapter):
    """장 이름에서 과목 열쇠를 얻는다. 모르는 앞머리는 확률통계로 둔다."""
    return COURSE_OF_PREFIX.get(chapter.split("_")[0], "probstat")


def load_pages(module_path):
    spec = importlib.util.spec_from_file_location("slides_module", module_path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault("MANIM_API", "manimgl")
    spec.loader.exec_module(mod)
    return list(mod.PAGES)


def env():
    e = dict(os.environ)
    e["MANIM_API"] = "manimgl"
    e["PYTHONPATH"] = f"{ROOT}:{ROOT / 'legacy'}" + (":" + e["PYTHONPATH"] if e.get("PYTHONPATH") else "")
    e["SLIDES_DIR"] = str(SLIDES_DIR)
    return e


def render(module, scene):
    cmd = [str(MANIM_SLIDES), "render", "--GL", module, scene + "Slides", "--hd",
           "--video_dir", str(VIDEO_DIR)]
    log = STAGE / f"render_{scene}.log"
    with open(log, "w") as fh:
        r = subprocess.run(cmd, cwd=ROOT, env=env(), stdout=fh, stderr=subprocess.STDOUT)
    return r.returncode == 0, log


def convert(scene, title, out_html):
    out_html.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(MANIM_SLIDES), "convert", "--folder", str(SLIDES_DIR), "--one-file", "--offline",
           "-ccontrols=true", "-cprogress=true", "-cslide_number=true", f"-ctitle={title}",
           scene + "Slides", str(out_html)]
    log = STAGE / f"convert_{scene}.log"
    with open(log, "w") as fh:
        r = subprocess.run(cmd, cwd=ROOT, env=env(), stdout=fh, stderr=subprocess.STDOUT)
    return r.returncode == 0 and out_html.exists(), log


def n_slides(scene):
    p = SLIDES_DIR / f"{scene}Slides.json"
    if not p.exists():
        return None
    return len(json.loads(p.read_text())["slides"])


STYLE = """
body{margin:0;background:#111;color:#e8e8e8;font-family:-apple-system,'Apple SD Gothic Neo','Noto Sans KR',sans-serif}
main{max-width:860px;margin:0 auto;padding:36px 20px 60px}
h1{font-size:26px;margin:0 0 6px}p.sub{color:#9a9a9a;margin:0 0 26px;font-size:14px}
table{width:100%;border-collapse:collapse;font-size:15px}td,th{padding:9px 8px;border-bottom:1px solid #2a2a2a;text-align:left}
th{color:#9a9a9a;font-weight:500}td.n{color:#9a9a9a;width:2.5em}td.s{color:#9a9a9a;width:5em;text-align:right}
a{color:#8fd3ff;text-decoration:none}a:hover{text-decoration:underline}
tr.sec td{padding-top:22px;color:#f0c419;font-weight:600;border-bottom:none}
p.how{color:#bdbdbd;font-size:14px;line-height:1.6}
h2{font-size:19px;margin:34px 0 4px;color:#e8e8e8}
h2+p.sub{margin-bottom:12px}
"""

SECTIONS = {
    "am_00": [
        ("다루는 내용", ["CourseRoadmap"]),
        ("강의 개요", ["PixelsAreDiscrete", "ImageAsMatrix", "GradientDescentGlimpse"]),
    ],
    "am_01": [
        ("1.2 행렬의 정의", ["EntryNotation", "ArrayDimensions", "SquareMatrixDiagonal",
                          "Transpose", "SymmetricMatrix"]),
        ("1.3 행렬의 연산", ["MatrixAddition", "ScalarMultiple", "MatrixProduct",
                          "ProductOrder", "ProductShapeRule", "MatrixPower"]),
        ("1.4 행렬과 연립선형방정식의 관계", ["RowOperations", "EchelonForms"]),
        ("보충 · 곱이라 부르는 연산들", ["OneExampleThreeProducts", "CrossProduct",
                                "FrobeniusInner", "KroneckerProduct",
                                "ProductSizeMap"]),
    ],
    "am_02": [
        ("2.1 가우스-조르당 소거법", ["GaussJordan"]),
        ("2.2 역행렬", ["InverseByRowOps"]),
    ],
    "ps1_02": [
        ("2.1 Sample Space", ["SampleSpace"]),
        ("2.2 Events", ["EventsAndSetOps"]),
        ("2.3 Counting Sample Points", ["MultiplicationRule", "Example213Dice", "Example215Club", "Example217EvenNumbers",
                                        "Permutations", "Combinations", "Example218Awards", "Example222Cartridges"]),
        ("2.4 Probability of an Event", ["ProbabilityOfEvent", "Example225LoadedDie", "Example228Poker"]),
        ("2.5 Additive Rules", ["AdditionRule", "Example229Jobs", "Example233Cable"]),
        ("2.6 Conditional Probability, Independence, and the Product Rule",
         ["ConditionalProbability", "Example234Flights", "Independence", "ProductRule", "Example236Fuses", "Example238Emergency"]),
        ("2.7 Bayes' Rule", ["TotalProbability", "Example241Machines", "BayesRule", "Example242Bayes"]),
    ]
}


def write_index(chapter, rows):
    by_scene = {r["scene"]: r for r in rows}
    course = COURSE[course_of(chapter)]
    lang = "ko" if course_of(chapter) == "aimath" else "en"
    head = CHAPTER_TITLE.get(chapter, chapter)
    body = []
    k = 0
    for sec, scenes in SECTIONS.get(chapter, [(head, [r["scene"] for r in rows])]):
        body.append(f'<tr class="sec"><td colspan="3">{sec}</td></tr>')
        for s in scenes:
            r = by_scene.get(s)
            if not r:
                continue
            k += 1
            body.append(f'<tr><td class="n">{k}</td><td><a href="{s}.html">{r["title"]}</a></td>'
                        f'<td class="s">{r["slides"]} {course["steps"]}</td></tr>')
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{head} · {course["title"]}</title><style>{STYLE}</style></head><body><main>
<h1>{head}</h1><p class="sub">{course["title"]} · {course["sub"]}</p>
<p class="how">{course["how"]}</p>
<table><tr><th>#</th><th>{"영상" if lang == "ko" else "Animation"}</th><th></th></tr>{''.join(body)}</table>
<p class="sub" style="margin-top:28px"><a href="../">{course["back"]}</a></p></main></body></html>"""
    (ROOT / "docs" / chapter / "index.html").write_text(html, encoding="utf-8")


def write_root_index():
    """과목별로 묶은 장 목록. docs/ 에 실제로 있는 장만 싣는다."""
    docs = ROOT / "docs"
    chapters = sorted(p.name for p in docs.iterdir() if p.is_dir() and (p / "index.html").exists())
    blocks = []
    for key in ("aimath", "probstat"):
        mine = [c for c in chapters if course_of(c) == key]
        if not mine:
            continue
        course = COURSE[key]
        rows = "".join(f'<tr><td><a href="{c}/">{CHAPTER_TITLE.get(c, c)}</a></td></tr>' for c in mine)
        blocks.append(f'<h2>{course["title"]}</h2><p class="sub">{course["sub"]}</p>'
                      f'<table>{rows}</table>')
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>강의 영상 · Lecture Animations</title><style>{STYLE}</style></head><body><main>
<h1>강의 영상 · Lecture Animations</h1>
<p class="sub">클릭으로 한 단계씩 넘기는 강의 영상. 아주대학교 2026-2.<br>
Click-through versions of the lecture animations. Ajou University, 2026 Fall.</p>
{''.join(blocks)}</main></body></html>"""
    (docs / "index.html").write_text(html, encoding="utf-8")
    (docs / ".nojekyll").touch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", required=True)
    ap.add_argument("--module", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--skip-convert", action="store_true")
    args = ap.parse_args()

    STAGE.mkdir(parents=True, exist_ok=True)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    pages = load_pages(str(ROOT / args.module))
    todo = [(s, t) for s, t in pages if not args.only or s in args.only]
    out_dir = ROOT / "docs" / args.chapter
    failures = []

    for scene, title in todo:
        if not args.skip_render:
            ok, log = render(args.module, scene)
            print(f"render  {scene:24s} {'OK' if ok else 'FAIL  ' + str(log)}", flush=True)
            if not ok:
                failures.append(scene)
                continue
        if not args.skip_convert:
            ok, log = convert(scene, title, out_dir / f"{scene}.html")
            print(f"convert {scene:24s} {'OK' if ok else 'FAIL  ' + str(log)}", flush=True)
            if not ok:
                failures.append(scene)

    rows = []
    for scene, title in pages:
        html = out_dir / f"{scene}.html"
        n = n_slides(scene)
        if html.exists() and n:
            rows.append({"scene": scene, "title": title, "url": f"{SITE}/{args.chapter}/{scene}.html",
                         "slides": n, "kb": html.stat().st_size // 1024})
    (out_dir / "pages.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    write_index(args.chapter, rows)
    write_root_index()

    print(f"\n{'scene':24s} {'steps':>5s} {'KB':>7s}")
    for r in rows:
        print(f"{r['scene']:24s} {r['slides']:5d} {r['kb']:7d}")
    print(f"{len(rows)} pages · {sum(r['kb'] for r in rows) // 1024} MB · docs/{args.chapter}/")
    if failures:
        print("FAIL:", ", ".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
