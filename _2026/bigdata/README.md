# 빅데이터개론 및 분석 시각화 보조자료 (manim)

강의자료 `2026-2/빅데이터개론및분석/week01_자료/[1주차]*.md` 의 시각화 보조자료.
`[0903]Introduction.pptx` 에 mp4로 삽입해서 쓴다.

파일 이름에 과목 접두어를 붙인 이유는 출력 폴더가 파일 이름을 따라가기 때문이다
(`videos/<파일이름>/<Scene>.mp4`). `week01.py` 로 두면 `_2026/probstat/week01.py`,
`_2026/aimath/week01.py` 와 출력이 한 폴더에 섞인다.

## 소재 규칙

하네스 3.8을 따른다. 개념을 상자와 화살표로 옮긴 도식은 만들지 않는다.
그 과목에서 실제로 다루는 그래프(산점도·히스토그램·결정경계·회귀직선)를 소재로 쓰고,
화면의 수치는 씬 안에서 numpy 로 계산한다. 합성 자료는 화면에 예시임을 표시한다.

1주차는 오리엔테이션이므로 학기에 배울 기법의 예고로 만든다. 원리 설명이 아니라
그 기법으로 무엇을 만드는지를 결과 그림으로 먼저 보여 주는 것이 목적이다.

## 씬 목록

### `bigdata_week01.py` — 1주차 오리엔테이션

| Scene | 강의자료 | 슬라이드 | 소재 기법 | 예고 차시 |
|---|---|---|---|---|
| `AnalysisSteps` | 17-4절 | `[0903]` 8쪽 | 결측 처리, 히스토그램, 산점도와 회귀직선 | 6주차, 9주차 |
| `RuleVsStatistical` | 18-1절 | `[0903]` 11쪽 | 산점도, 결정경계, 정확도 비교 | 10주차 |

`AnalysisSteps` 는 같은 자료가 단계를 지날 때마다 산출물이 바뀌는 것을 보여 준다.
결측이 섞인 표 → 결측 제거 → 히스토그램 → 산점도와 회귀직선 순이며, 평균·표준편차·
기울기·상관계수는 모두 그 자료에서 계산한 값이다.

`RuleVsStatistical` 은 산점도 하나에 두 경계를 차례로 얹는다. 사람이 정한 임계값은
축에 평행한 경계를, 로지스틱 회귀는 기울어진 경계를 만든다. 정확도와 오분류 개수는
씬 안에서 세므로 그림과 수치가 어긋나지 않는다.

## 렌더

저장소 루트(`manim_songhune/`)에서 실행한다.

```bash
./render.sh list    _2026/bigdata/bigdata_week01.py                  # 씬 목록
./render.sh check   _2026/bigdata/bigdata_week01.py                  # 전 씬 빠른 점검
./render.sh preview _2026/bigdata/bigdata_week01.py AnalysisSteps    # 창으로 미리보기
./render.sh png     _2026/bigdata/bigdata_week01.py AnalysisSteps    # 마지막 프레임
./render.sh ppt     _2026/bigdata/bigdata_week01.py AnalysisSteps    # PPT 삽입용
./render.sh all     _2026/bigdata/bigdata_week01.py                  # 전부 1080p
```

결과물은 `videos/bigdata_week01/`, PPT용은 `videos/ppt/` 에 생긴다.
강의 폴더로 옮기고 슬라이드까지 다시 만들려면 강의 폴더 쪽 스크립트를 쓴다.

```bash
빅데이터개론및분석/week01_자료/build_week01.sh videos   # 렌더 + 강의 폴더로 복사
빅데이터개론및분석/week01_자료/build_week01.sh all      # 이미지·pptx·pdf 재생성
```

## 이 파일들의 약속

- 서체는 강의 템플릿과 같은 것을 쓴다 — 제목 `Ajou`, 본문 `Arita Buri KR`
- 색 의미를 고정한다
  - `ACCENT`(파랑) = 자료·통계적 분석
  - `GOLD_`(노랑) = 사람이 정한 규칙·추정 결과
  - `WARN`(빨강) = 오분류·결측
  - `CALM`(청록) = 단계 표시
- 제목은 명사구로 쓴다(하네스 3.1). 마무리를 표어로 맺지 않는다(하네스 3.6).
  그림이 이미 보여 준 것을 문장으로 다시 말하지 않는다.
- 상단 상수와 헬퍼는 `_2026/probstat/week01.py` 와 같은 것을 쓴다

## manimgl 주의점

1. **`Axes` 는 0 이 범위 밖이면 화면 밖으로 나간다.** `create_axis()` 에서
   `axis.shift(-axis.n2p(0))` 를 하기 때문이다. 연도(1950–2030)처럼 0 이 멀리 있는 축은
   `NumberLine` 으로 직접 세우고 좌표를 `line.n2p(x)` 로 계산한다.
2. **y축 눈금 숫자는 `include_numbers` 로 붙이면 누워서 나온다.** `Axes` 가 y축을 만든 뒤
   90도 회전시키므로 숫자까지 같이 돈다. 이 파일의 `axis_numbers()` 처럼 직접 놓는다.
   같은 헬퍼가 본문 서체를 쓰므로 숫자와 축 이름의 서체도 맞는다.
