#!/usr/bin/env bash
# PPT용 manim 렌더링 명령 모음.
#   ./render.sh <명령> <파일.py> [Scene ...] [-- manimgl 추가옵션]
# 자세한 설명은 RENDER.md 참고.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# manimlib가 설치된 파이썬 환경 (pyenv virtualenv "llm").
# 다른 환경을 쓰려면 MANIM_PY / MANIM_BIN 환경변수로 덮어쓰면 된다.
MANIM_PY="${MANIM_PY:-$HOME/.pyenv/versions/llm/bin/python}"
MANIM_BIN="${MANIM_BIN:-$HOME/.pyenv/versions/llm/bin/manimgl}"

# 씬 파일들이 `from manim_imports_ext import *` 를 하므로 저장소 루트가 경로에 있어야 한다.
# legacy 도 넣는다. outside_videos/ 가 `from _2016.zeta import ...` 처럼 옛 연도 폴더를 import 한다.
export PYTHONPATH="$REPO_ROOT:$REPO_ROOT/legacy${PYTHONPATH:+:$PYTHONPATH}"

# 결과물 위치: videos/<과목>/<파일이름>/<SceneName>.mp4
# 과목을 경로에 넣는 이유: _2026/aimath/week01.py 와 _2026/probstat/week01.py 가
# 둘 다 videos/week01/ 로 나가 한 폴더에서 섞였다.
VIDEO_DIR="$REPO_ROOT/videos"

die() { echo "오류: $*" >&2; exit 1; }

# 소스 경로에서 과목 폴더 이름을 정한다.
course_of() {
    case "$1" in
        *_2026/aimath/*)   echo aimath  ;;
        *_2026/probstat/*) echo prob    ;;
        *_2026/bigdata/*)  echo bigdata ;;
        *_2026/ml/*)       echo ml      ;;
        *)                 echo legacy  ;;
    esac
}

# manimgl 에 넘길 출력 폴더. manimgl 이 그 아래에 <파일이름>/ 을 스스로 만든다.
video_dir_of() {
    echo "$VIDEO_DIR/$(course_of "$1")"
}

# 실제 결과물이 떨어지는 폴더.
out_dir_of() {
    echo "$VIDEO_DIR/$(course_of "$1")/$(basename "$1" .py)"
}

# GIF 가 떨어지는 폴더. 과목 폴더 안의 영상 폴더다 (하네스 3.6, 2026-09-07).
# manim 저장소의 videos/ 에 두지 않는다. Notability 에 붙일 때 수업 자료 옆에 있어야 찾는다.
# 태그(수업일-순번)가 붙은 날짜별 사본은 과목의 도구/영상_태그.py 가 만든다.
gif_dir_of() {
    case "$(course_of "$1")" in
        prob) echo "$REPO_ROOT/../확률과통계/확통 자료/수업안/영상/gif" ;;
        *)    echo "$VIDEO_DIR/$(course_of "$1")/gif" ;;   # 다른 과목은 영상 폴더를 정하면 여기에 적는다
    esac
}

usage() {
    cat <<'USAGE'
사용법: ./render.sh <명령> <파일.py> [Scene ...] [추가 manimgl 옵션]

  list     <파일.py>                 파일 안의 Scene 목록을 정의 순서대로 출력
  preview  <파일.py> <Scene>         창으로 미리보기 (파일 저장 안 함)
  draft    <파일.py> <Scene ...>     480p mp4 (빠른 확인용)
  video    <파일.py> <Scene ...>     1080p mp4 (PPT 기본 권장)
  4k       <파일.py> <Scene ...>     2160p mp4 (대형 스크린/최종본)
  ppt      <파일.py> <Scene ...>     1080p 렌더 후 PowerPoint 호환으로 재인코딩
                                     -> videos/<과목>/ppt/<Scene>.mp4
  png      <파일.py> <Scene ...>     마지막 프레임만 정지 이미지로 저장
  gif      <파일.py> <Scene ...>     Notability 등에 붙일 gif (1280px·15fps, 팔레트 최적화)
                                     -> 과목 폴더의 영상/gif/<Scene>.gif (확통: 확률과통계/확통 자료/수업안/영상/gif)
                                        태그 붙은 날짜별 사본은 도구/영상_태그.py
                                     크기를 더 줄이려면 GIF_W=720 GIF_FPS=12 ./render.sh gif ...
  alpha    <파일.py> <Scene ...>     투명 배경 .mov (Keynote용, PPT는 지원 제한적)
  white    <파일.py> <Scene ...>     흰 배경 1080p mp4 (밝은 슬라이드용)
                                     light_config.yml의 밝은 팔레트를 함께 적용
  all      <파일.py>                 파일 안 모든 Scene을 1080p로 렌더
  check    <파일.py>                 모든 Scene을 빠르게 시험 렌더해서 OK/FAIL 표로 출력
                                     (레거시 씬 중 어떤 게 지금 돌아가는지 확인용)
  dev      <파일.py> <Scene> <줄번호> 해당 줄에서 대화형(iPython) 세션 진입
  env                                사용 중인 파이썬/manimgl 경로 확인

Scene 이름 뒤에 붙인 인자는 그대로 manimgl에 전달된다.
  예) ./render.sh video _2026/probstat/week01.py MeanVsMedian -o
USAGE
}

require_file() {
    [ -n "${1:-}" ] || { usage; exit 1; }
    [ -f "$1" ] || die "파일을 찾을 수 없음: $1"
}

# manimgl 은 프레임을 한 장씩 이어붙이며 결과 파일을 오래 열어 둔다. videos/ 가
# Synology Drive 동기화 폴더 안이라 그 사이 동기화가 끼어들면 sqlite disk I/O 오류가
# 나거나 "...Conflict.mp4" 사본이 생긴다. 그래서 동기화 밖에서 렌더하고, 다 된 파일만
# videos/ 로 옮긴다. 다른 자리를 쓰려면 MANIM_STAGE 로 덮어쓰면 된다.
STAGE="${MANIM_STAGE:-${TMPDIR:-/tmp}/manim_songhune_render}"

# 스테이징에서 완성된 파일만 videos/ 로 옮긴다. 렌더 중간 산물(_temp)은 두고 온다.
collect() {
    local src="$1" stem out
    stem="$(basename "$src" .py)"
    out="$(out_dir_of "$src")"
    [ -d "$STAGE/$(course_of "$src")/$stem" ] || return 0
    mkdir -p "$out"
    find "$STAGE/$(course_of "$src")/$stem" -maxdepth 1 -type f ! -name '*_temp.*' \
        -exec mv -f {} "$out/" \;
}

run_manim() {
    # 첫 인자가 씬 파일이면 그 과목 폴더로 출력한다
    local extra=() src="" rc=0
    case "${1:-}" in
        *.py) src="$1"
              mkdir -p "$STAGE/$(course_of "$1")"
              extra=(--video_dir "$STAGE/$(course_of "$1")") ;;
    esac
    echo "▶ manimgl $* ${extra[*]:-}" >&2
    "$MANIM_BIN" "$@" "${extra[@]}" || rc=$?
    [ -n "$src" ] && [ "$rc" -eq 0 ] && collect "$src"
    return $rc
}

CMD="${1:-}"
[ -n "$CMD" ] || { usage; exit 1; }
shift || true

case "$CMD" in
    env)
        echo "python : $MANIM_PY"
        echo "manimgl: $MANIM_BIN"
        echo "version: $("$MANIM_BIN" --version 2>&1 | tail -1)"
        echo "출력    : $VIDEO_DIR"
        ;;
    list)
        require_file "${1:-}"
        "$MANIM_PY" tools/list_scenes.py "$1"
        ;;
    preview)
        require_file "${1:-}"
        run_manim "$@"
        ;;
    draft)
        require_file "${1:-}"
        run_manim "$@" -w -l
        ;;
    video)
        require_file "${1:-}"
        run_manim "$@" -w --hd
        ;;
    4k)
        require_file "${1:-}"
        run_manim "$@" -w --uhd
        ;;
    white)
        require_file "${1:-}"
        # 배경만 흰색으로 바꾸면 밝은 회색 글씨가 사라진다.
        # light_config.yml이 팔레트까지 통째로 밝은 테마로 바꿔 준다.
        run_manim "$@" -w --hd --config_file light_config.yml
        ;;
    png)
        require_file "${1:-}"
        run_manim "$@" -s -w --hd
        ;;
    gif)
        # manimgl 의 -i 는 프레임을 그대로 담아 10초에 18MB가 나온다.
        # 1080p mp4 로 렌더한 뒤 ffmpeg 팔레트 방식으로 줄인다 (같은 길이에 0.7MB).
        # Notability 는 mp4 를 필기 위에 못 얹지만 GIF 는 그림처럼 붙는다.
        require_file "${1:-}"
        FILE="$1"; shift
        [ -n "${1:-}" ] || die "Scene 이름이 필요합니다."
        OUT="$(out_dir_of "$FILE")"
        GIF_DIR="$(gif_dir_of "$FILE")"
        GIF_W="${GIF_W:-1920}"          # 가로 픽셀. mp4 와 같게 둔다. 720 까지 줄이면 용량이 1/3 이 된다 (2026-09-07: 1280 → 1920)
        GIF_FPS="${GIF_FPS:-15}"
        GIF_DITHER="${GIF_DITHER:-none}"   # manim 화면은 평면색이라 256색이면 충분하다. 디더링은 격자 무늬만 얹는다
        # 씬 파일보다 새 mp4 가 이미 있으면 다시 렌더하지 않는다. ppt 를 먼저 돌린 뒤
        # gif 를 돌리는 것이 보통이라, 이게 없으면 같은 씬을 두 번 렌더한다.
        NEED=0
        for SCENE in "$@"; do
            case "$SCENE" in -*) continue ;; esac
            [ "$OUT/$SCENE.mp4" -nt "$FILE" ] || NEED=1
        done
        if [ "$NEED" -eq 1 ]; then
            run_manim "$FILE" "$@" -w --hd
        else
            echo "▶ 기존 mp4 재사용 (씬 파일보다 새것)" >&2
        fi
        mkdir -p "$GIF_DIR"
        PAL="$(mktemp -t manimgif).png"
        for SCENE in "$@"; do
            case "$SCENE" in -*) continue ;; esac
            SRC="$OUT/$SCENE.mp4"
            [ -f "$SRC" ] || { echo "건너뜀(렌더 결과 없음): $SRC" >&2; continue; }
            DST="$GIF_DIR/$SCENE.gif"
            ffmpeg -y -loglevel error -i "$SRC" \
                -vf "fps=$GIF_FPS,scale=$GIF_W:-1:flags=lanczos,palettegen=stats_mode=diff" "$PAL"
            ffmpeg -y -loglevel error -i "$SRC" -i "$PAL" \
                -lavfi "fps=$GIF_FPS,scale=$GIF_W:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=$GIF_DITHER:diff_mode=rectangle" \
                "$DST"
            echo "✅ GIF(Notability용): $DST  $(du -h "$DST" | cut -f1)"
        done
        rm -f "$PAL"
        ;;
    alpha)
        require_file "${1:-}"
        run_manim "$@" -w --hd -t
        ;;
    all)
        require_file "${1:-}"
        run_manim "$1" -a -w --hd "${@:2}"
        ;;
    dev)
        require_file "${1:-}"
        [ -n "${3:-}" ] || die "사용법: ./render.sh dev <파일.py> <Scene> <줄번호>"
        run_manim "$1" "$2" -e "$3"
        ;;
    check)
        require_file "${1:-}"
        FILE="$1"
        REPORT_DIR="$VIDEO_DIR/_scratch/_check"
        mkdir -p "$REPORT_DIR"
        REPORT="$REPORT_DIR/$(basename "$FILE" .py).txt"
        : > "$REPORT"
        SCENES=$("$MANIM_PY" tools/list_scenes.py "$FILE" 2>/dev/null | awk '{print $2}')
        for SCENE in $SCENES; do
            printf '%-45s ' "$SCENE"
            if "$MANIM_BIN" "$FILE" "$SCENE" -s -w -l \
                    --video_dir "$STAGE/$(course_of "$FILE")" >/tmp/manim_check.log 2>&1; then
                echo "OK"
                echo "OK    $SCENE" >> "$REPORT"
            else
                ERR=$(tr '\r' '\n' < /tmp/manim_check.log | grep -E '^[A-Za-z_.]*(Error|Exception)' | tail -1)
                echo "FAIL  $ERR"
                echo "FAIL  $SCENE  ::  $ERR" >> "$REPORT"
            fi
        done
        echo "리포트: $REPORT"
        ;;
    ppt)
        require_file "${1:-}"
        FILE="$1"; shift
        [ -n "${1:-}" ] || die "Scene 이름이 필요합니다."
        OUT="$(out_dir_of "$FILE")"
        PPT_DIR="$VIDEO_DIR/$(course_of "$FILE")/ppt"
        run_manim "$FILE" "$@" -w --hd
        mkdir -p "$PPT_DIR"
        for SCENE in "$@"; do
            case "$SCENE" in -*) continue ;; esac
            SRC="$OUT/$SCENE.mp4"
            [ -f "$SRC" ] || { echo "건너뜀(렌더 결과 없음): $SRC" >&2; continue; }
            DST="$PPT_DIR/$SCENE.mp4"
            ffmpeg -y -loglevel error -i "$SRC" \
                -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p \
                -crf 20 -preset slow -movflags +faststart -an "$DST"
            echo "✅ PPT 삽입용: $DST"
        done
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        die "알 수 없는 명령: $CMD (./render.sh --help 참고)"
        ;;
esac
