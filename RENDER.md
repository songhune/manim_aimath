# PPT용 씬 렌더링 가이드

강의 슬라이드에 넣을 영상을 이 저장소에서 뽑아내는 방법을 정리한 문서다.
모든 명령은 **저장소 루트에서** 실행한다 (`custom_config.yml`을 현재 디렉터리에서 읽기 때문).

## 0. 환경

| 항목 | 값 |
| --- | --- |
| manimgl | `~/.pyenv/versions/llm/bin/manimgl` (ManimGL v1.7.2) |
| manimlib 소스 | `../../manim` (별도 체크아웃) |
| 필수 환경변수 | `PYTHONPATH=<저장소 루트>` — 씬 파일이 `manim_imports_ext`를 임포트하므로 |
| 출력 위치 | `videos/<파일이름>/<SceneName>.mp4` |

`manimgl`을 그냥 치면 pyenv 전역이 `system`이라 실패한다. `./render.sh`가 위 경로와
`PYTHONPATH`를 알아서 잡아주므로 이 스크립트를 쓰는 것이 가장 안전하다.

직접 치고 싶다면:

```bash
export PYENV_VERSION=llm            # 또는 pyenv shell llm
export PYTHONPATH="$PWD"
manimgl _2016/eola/chapter1.py VectorAddition -w --hd
```

## 1. 명령 체계 (`./render.sh`)

```
./render.sh <명령> <파일.py> [Scene ...] [추가 manimgl 옵션]
```

| 명령 | 하는 일 | 대응하는 manimgl 옵션 |
| --- | --- | --- |
| `list` | 파일 안 Scene 목록을 정의된 순서대로 출력 | — |
| `check` | 파일 안 모든 Scene을 빠르게 시험 렌더 → OK/FAIL 표 | `-s -w -l` |
| `preview` | 창으로 미리보기 (파일 저장 안 함) | (없음) |
| `draft` | 480p mp4, 구도 확인용 | `-w -l` |
| `video` | **1080p mp4 — PPT 기본 권장** | `-w --hd` |
| `4k` | 2160p mp4, 대형 스크린/최종본 | `-w --uhd` |
| `ppt` | 1080p 렌더 후 PowerPoint 호환으로 재인코딩 | `-w --hd` + ffmpeg |
| `png` | 마지막 프레임만 정지 이미지로 | `-s -w --hd` |
| `gif` | gif로 저장 (짧은 씬 전용). 과목 폴더의 영상/gif/ 에 떨어진다 | `-w --hd -i` |
| `alpha` | 투명 배경 `.mov` (Keynote용) | `-w --hd -t` |
| `white` | 흰 배경 1080p mp4 (밝은 팔레트 동시 적용) | `-w --hd --config_file light_config.yml` |
| `all` | 파일 안 모든 Scene을 1080p로 | `-a -w --hd` |
| `dev` | 특정 줄에서 대화형 iPython 진입 | `-e <줄번호>` |
| `env` | 사용 중인 파이썬/manimgl 경로 확인 | — |

Scene 이름 뒤에 붙인 인자는 그대로 manimgl에 전달된다.

```bash
./render.sh video _2016/eola/chapter1.py VectorAddition -o     # 렌더 후 자동 열기
./render.sh video _2016/eola/chapter1.py VectorAddition -n 3,6 # 3~6번째 애니메이션만
```

## 2. 표준 작업 흐름

```bash
# 1) 어떤 씬이 있는지 본다
./render.sh list _2016/eola/chapter1.py

# 2) 그 파일에서 지금 돌아가는 씬이 뭔지 확인한다 (레거시 코드라 일부는 깨져 있다)
./render.sh check _2016/eola/chapter1.py

# 3) 마음에 드는 후보를 저해상도로 빠르게 확인
./render.sh draft _2016/eola/chapter1.py VectorAddition

# 4) 확정되면 PPT용으로 뽑는다
./render.sh ppt _2016/eola/chapter1.py VectorAddition
#    -> videos/ppt/VectorAddition.mp4
```

`check` 결과는 `videos/_check/<파일이름>.txt`에도 저장된다.

## 3. PowerPoint에 넣기

- `ppt` 명령이 만드는 파일은 **1920×1080 / H.264 High / yuv420p / faststart / 오디오 없음**이라
  Windows·macOS 파워포인트 양쪽에서 바로 재생된다.
- 삽입: 리본의 `삽입 → 비디오 → 이 디바이스` 로 `videos/ppt/<Scene>.mp4` 선택.
- 재생 옵션: `재생` 탭에서 **자동 실행** + 필요하면 **반복 재생**을 켠다.
  manim 씬은 끝에서 화면이 멈춘 채 끝나므로, 마지막 상태를 계속 보여주려면 반복 대신
  마지막 프레임 PNG(`./render.sh png ...`)를 다음 슬라이드에 두는 편이 깔끔하다.
- **배경**: 기본 씬 배경은 검정이고 글자·수식은 흰색이다. 어두운 슬라이드 테마와 잘 맞는다.
- **흰 배경으로 렌더하기**: `./render.sh white <파일.py> <Scene>` 을 쓴다.
  배경색만 바꾸는 `-c "#FFFFFF"` 로는 밝은 회색 글씨(GREY_A 등)가 흰 바탕에 묻혀 사라지므로,
  이 명령은 `light_config.yml` 을 함께 물려 **팔레트 전체를 밝은 테마로 뒤집는다.**
  - 무채색 램프(GREY_A~E)와 각 색상 램프의 명암 순서가 뒤집힌다. 어두운 테마에서
    "가장 밝아서 가장 잘 보이던" A 슬롯이, 밝은 테마에서는 "가장 어두워서 가장 잘 보이는" 값이 된다.
    따라서 `INK = GREY_A`, `ACCENT = BLUE_B` 같은 기존 별칭을 그대로 두어도 의미가 유지된다.
  - 씬 코드에 남아 있는 `WHITE`/`BLACK` 도 서로 뒤집히므로 그대로 보인다.
  - 노랑은 흰 바탕에서 읽히지 않아 앰버 계열로 내렸다. 채도 보정(1.5)도 1.0으로 되돌린다.
  - 다른 명령에서도 쓰고 싶으면 옵션을 그대로 붙이면 된다:
    `./render.sh ppt _2026/probstat/week01.py MeanVsMedian --config_file light_config.yml`
  - 색을 조정하려면 `light_config.yml` 의 `colors:` 항목만 고치면 되고, 씬 코드는 건드리지 않는다.
- **투명 배경**: `alpha` 명령은 ProRes 4444 `.mov`를 만든다. Keynote는 알파를 살려주지만
  파워포인트는 사실상 지원하지 않으니, PPT용이면 그냥 검정 배경으로 두는 것을 권한다.
- 파일 용량이 걱정되면 `-n 시작,끝`으로 필요한 구간만 잘라 렌더하는 것이 재인코딩보다 깔끔하다.

## 4. 어떤 씬을 쓸 것인가 — Essence of Linear Algebra 지도

`_2016/eola/`가 선형대수 시리즈이고, AI기초수학 슬라이드에 바로 쓸 만한 소재가 여기 다 있다.

| 파일 | 주제 |
| --- | --- |
| `chapter0.py` | 시리즈 소개, 핵심 직관 미리보기 |
| `chapter1.py` | 벡터란 무엇인가 (덧셈, 스칼라배) |
| `chapter2.py` | 일차결합, 생성(span), 기저 |
| `chapter3.py` | 선형변환과 행렬 |
| `chapter4.py` | 행렬 곱 = 변환의 합성 |
| `chapter5.py` | 행렬식 |
| `chapter6.py` | 역행렬, 열공간, 영공간 |
| `chapter7.py` | 내적과 쌍대성 |
| `chapter8.py`, `chapter8p2.py` | 외적 |
| `chapter9.py` | 기저 변환 |
| `chapter10.py` | 고유벡터와 고윳값 |
| `chapter11.py` | 추상 벡터공간 |
| `footnote.py` | 비정방행렬 |
| `footnote2.py` | 3×2 행렬 등 보충 |

바로 확인해 본 추천 씬:

```bash
./render.sh ppt _2016/eola/chapter1.py  VectorAddition             # 벡터 덧셈
./render.sh ppt _2016/eola/chapter5.py  StretchingTransformation   # 공간이 늘어나는 변환
./render.sh ppt _2016/eola/chapter10.py ExampleTranformationScene  # 기저벡터와 행렬
```

## 5. 레거시 씬 주의사항

`_2016/` 코드는 2016년 manim 기준이라 현재 manimlib(1.7.2)와 맞지 않는 부분이 남아 있다.
공통으로 걸리던 부분은 이번에 호환 레이어(`manim_imports_ext.py`)와
`once_useful_constructs/vector_space_scene.py`에서 정리했다.

이미 처리해 둔 것:

- `LinearTransformationScene` 전체 (옛 `x_max`/`color` 평면 인자, `add_coordinates`,
  `Scene.play(path_arc=...)`) → 3·5·6·9·10장의 변환 애니메이션이 돌아간다
- `Arrow(color=...)`가 회색으로 나오던 문제 (새 manimlib은 화살표를 fill로 칠한다)
- `Axes`/`NumberPlane`의 옛 인자(`x_radius`, `x_min`, `secondary_line_ratio`, `color`)
- `Matrix`에 1차원 벡터를 넘기는 옛 관용구, `get_mob_matrix()`의 numpy 배열 반환
- `TexText(["a", "b"])`처럼 리스트로 넘기던 호출, `matrix_to_mobject` 헬퍼

씬마다 개별적으로 남아 있는 문제는 그 씬을 직접 고쳐야 한다. 자주 보이는 것:

| 증상 | 원인 |
| --- | --- |
| `ValueError: too many values to unpack` (`title.split()`) | 옛 `TexText(...).split()`가 부분식 단위로 쪼개진다고 가정 |
| `AttributeError: get_coordinate_labels` | 메서드 이름 변경 (`add_coordinate_labels`) |
| `Exception: All submobjects must be of type VMobject` | 옛 `Mobject` 계열 혼합 사용 |
| `TypeError: Mobject.get_shape() missing 1 required positional argument` | 이름이 겹치는 옛 헬퍼 호출 |

그래서 **쓸 씬을 고르기 전에 `./render.sh check <파일>`을 먼저 돌리는 흐름**을 권한다.
참고로 `chapter1.py`는 현재 22개 중 15개가 정상 렌더된다.

## 6. 강의용 씬을 직접 만들 때

```python
# my_lecture.py
from manim_imports_ext import *


class DotProductIntro(InteractiveScene):
    def construct(self):
        plane = NumberPlane()
        v = Arrow(ORIGIN, [2, 1, 0], buff=0, fill_color=YELLOW)
        self.add(plane)
        self.play(GrowArrow(v))
        self.wait()
```

```bash
./render.sh preview my_lecture.py DotProductIntro   # 창으로 확인
./render.sh ppt     my_lecture.py DotProductIntro   # 슬라이드용 mp4
```

화살표 색은 `color=` 대신 `fill_color=`를 쓰는 것이 현재 manimlib에서 확실하다
(호환 레이어가 `color=`도 채워주지만, 새로 쓰는 코드는 명시적인 쪽이 낫다).

## 웹 슬라이드 (클릭 진행형, GitHub Pages)

한 영상을 동작 단위로 끊어 → / 스페이스로 넘기는 RevealJS 페이지. manim-slides 가 manimgl 로 렌더한다.

    python tools/build_slides_site.py --chapter am_01  --module _2026/aimath/slides_am_01.py
    python tools/build_slides_site.py --chapter ps1_02 --module _2026/probstat/slides_ps1_02.py
    python tools/build_slides_site.py --chapter am_01  --module ... --only MatrixProduct     # 한 씬만
    python tools/build_slides_site.py --chapter am_01  --module ... --skip-render            # 변환·목차만

지금 있는 장이다. 새 장을 넣을 때는 슬라이드 모듈 하나를 만들고
`tools/build_slides_site.py` 의 `CHAPTER_TITLE` 과 `SECTIONS` 두 곳을 채운다.

| 장 | 슬라이드 모듈 | 씬 정의 | 편 수 |
|---|---|---|---|
| `am_00` | `_2026/aimath/slides_am_00.py` | `_2026/aimath/week01.py` | 4 |
| `am_01` | `_2026/aimath/slides_am_01.py` | `_2026/aimath/week02.py` | 20 |
| `am_02` | `_2026/aimath/slides_am_02.py` | `_2026/aimath/week03.py` | 2 |
| `ps1_02` | `_2026/probstat/slides_ps1_02.py` | `_2026/probstat/week02.py`·`week03.py` | 26 |

- **단계를 나누는 기준이 과목마다 다르다.** 확률통계 씬은 단락마다 `wait()` 를 두고 쓰여 있어
  `wait()` 가 0.5초 이상이면 끊는다(씬별 조정은 `STEP_AT`). AI기초수학 씬은 `wait()` 가 씬당
  두세 번뿐이고 단계를 `play()` 로 나눠서, 같은 규칙을 쓰면 한 영상이 두 장이 된다. 그래서
  `_2026/aimath/slides_common.py` 는 `play()` 의 재생 시간을 쌓아 `min_step`(0.8초)을 넘을 때
  끊는다. 0.3~0.45초짜리 강조 동작이 한 클릭씩 차지하지 않게 묶어 주는 값이다.
- **`wait()` 도 한 동작으로 세어야 한다.** manimgl 은 `wait()` 에도 부분 영상 파일을 하나
  만드는데(`num_plays` 로 번호를 매긴다) manim-slides 의 `_current_animation` 은 `play()` 에서만
  올라간다. 맞춰 주지 않으면 첫 `wait()` 뒤부터 슬라이드마다 한 칸씩 밀린 영상이 붙는다.
  두 슬라이드 모듈 모두 `wait()` 에서 `_current_animation` 을 직접 올린다.
- 검산: 슬라이드 길이의 합이 `videos/<과목>/<파일>/<Scene>.mp4` 의 길이와 같아야 한다.
  짧으면 위의 밀림이 남아 있다는 뜻이다.
- 결과는 `docs/<chapter>/<Scene>.html` (영상·reveal.js 내장, `file://` 로도 열린다), 목차 `index.html`,
  덱 링크용 `pages.json`. 중간물은 `$TMPDIR/manim_songhune_slides/` 에 둔다.
- 배포: 브랜치 `26-2nd` 의 `/docs` 를 GitHub Pages 가 서비스한다.
  `https://songhune.github.io/manim_aimath/<chapter>/<Scene>.html`
- 학생 배포본의 영상 슬라이드는 `확률과통계/도구/학생배포본_생성.py` 가 이 표를 읽어 링크 슬라이드로 바꾼다.
