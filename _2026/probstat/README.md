# 확률과통계 시각화 보조자료 (manim)

강의 교안 `2026-2/확률과통계/교육메모/` 의 설명을 움직이는 그림으로 옮긴 것이다.
렌더한 mp4 를 슬라이드에 전체 화면으로 삽입해서 쓴다.

**화면에 나가는 문구는 전부 영어다.** 교재(Walpole 9판)와 같은 낱말이 화면에 보이게 하려는 것이며,
근거는 `2026-2/콘텐츠제작_하네스_PRD.md` 3.6 이다. 씬 이름과 주석은 교수자가 읽는 것이라 한국어로 둔다.

**그리고 문장으로 설명하지 않는다.** 화면에 남는 글자는 이름과 식뿐이고, 여섯 낱말을 넘기지
않는다. 논증은 그림이 한다 — 문장 한 줄을 지웠을 때 뜻이 사라진다면 그림을 더 만들어야 한다는
뜻이다. `ps_common.label()` 이 길이를 강제하며 `./render.sh check` 가 이걸 잡는다.

서체·색·치토·도우미는 `ps_common.py` 에 모여 있다. 주차 파일은 여기서 import 한다.

## 씬 목록

### `week00.py` — 오리엔테이션 강의개요

| Scene | 사용 위치 | 길이 | 무엇을 보여주나 |
|---|---|:--:|---|
| `MontyHall` | 오리엔테이션 슬라이드 4 | 19초 | 문을 바꾸면 1/3 → 2/3. 직관과 어긋나는 결과를 조건부확률이 설명한다 (3주차 예고) |
| `FrequencyView` | 오리엔테이션 슬라이드 5(b) | 23초 | 동전 400번의 앞면 비율이 1/2로 자리를 잡는다. 이어서 "내일은 반복할 수 없다"로 빈도 관점의 한계 |
| `BeliefUpdate` | 오리엔테이션 슬라이드 5(b) | 19초 | 스팸 필터로 사전확률 20% → 데이터 → 사후확률 95%. 베이즈의 구조만 남긴다 (공식은 3주차) |

`FrequencyView` / `BeliefUpdate` 는 보충 대본 `강의자료/01주차_보충_빈도vs믿음_말하기대본.md`
1절·2~3절을 그대로 옮긴 것이다. 대본 순서대로 이어 틀면 된다.

### `week02.py` — 2주차 확률 (1)

| Scene | 교안 위치 | 무엇을 보여주나 |
|---|---|---|
| `SampleSpaceTree` | 2차 [10–35분] | 동전 → 동전/주사위. 가지 끝에 실제 동전과 주사위가 달리고, 그 여덟 개가 S 가 된다 (Walpole Ex 2.2) |
| `EventsAndSetOps` | 2차 [35–65분] | 주사위 A=짝수, B=3의 배수. 여집합·교집합·합집합·배반을 벤 다이어그램에 차례로 칠한다 (Ex 2.26 과 같은 사건) |
| `MultiplicationRule` | 2차 [65–85분] | 6×6 격자를 한 줄씩 채워 36 을 센다. 눈금은 숫자가 아니라 주사위 면이다 (Ex 2.13) |
| `MultiplicationRuleClub` | 2차 [65–85분] | 22명 중 회장이 자리를 뜨면 줄이 21명으로 줄어든다. 22 × 21 이 왜 그런지가 줄 길이로 보인다 (Ex 2.15) |
| `PermVsComb` | 2차 [65–85분] | 순서를 따진 카드 12장이 둘씩 포개져 6장이 된다. 포개는 동작이 2! 로 나누는 일이다 (Ex 2.22) |
| `AdditionRule` | 3차 [25–55분] | 벤의 세 조각에 몇 번 세었는지를 숫자로 단다. 가운데만 2 가 되었다가 1 로 내려간다 (Theorem 2.7) |
| `ComplementTrick` | 3차 [55–80분] | 32칸 중 31칸을 세는 것과 1칸을 빼는 것. 마지막에 32칸이 막대 하나로 접힌다 |

`MultiplicationRule` 과 `MultiplicationRuleClub` 은 예제 두 개를 일부러 나눠 두었다.
한 씬에 두면 Example 2.15 의 답이 그 문제 슬라이드보다 먼저 나온다.

### `week01.py` — 1주차 통계와 데이터 분석 개요

| Scene | 교안 위치 | 길이 | 무엇을 보여주나 |
|---|---|:--:|---|
| `PopulationAndSample` | 1교시 [15–40분] | 14초 | 모집단 → 표본 → 추론의 순환. **학기 내내 재사용하는 도식** |
| `WhyVariability` | 1교시 [15–40분] 도입 | 16초 | 한 자리에 모여 있던 부품 10개가 실제 측정값으로 흩어진다. 흩어짐이 없으면 통계는 할 일이 없다 |
| `ProbabilityVsInference` | 1교시 [40–65분] | 10초 | 같은 두 상자, 화살표만 반대. 확률(1–7주차)과 통계(9–15주차)의 방향 |
| `BiasedSample` | 1교시 [65–85분] | 32초 | 불만인 치토가 등을 돌려 나가면 만족도가 60%에서 89%로 부푼다. 이어서 n 을 40 → 400 → 4000 으로 올려, 구간은 좁아지되 참값 자리로는 오지 않는 것을 보인다 |
| `MeanVsMedian` | 2교시 [0–30분] | 19초 | 극단값을 오른쪽으로 끌면 평균(받침점)은 따라가고 중앙값은 버틴다 |
| `VarianceFormula` | 2교시 [30–60분] 정의 직전 | 29초 | s² 공식을 편차 → 제곱 → 합 → n−1 순서로 쌓는다. 편차를 그냥 더하면 0이 되는 화면이 n−1 설명의 앞자리다 |
| `VarianceAsSquares` | 2교시 [30–60분] 예제 뒤 | 20초 | 편차 → 정사각형 넓이 → 넓이의 평균이 분산. 왜 제곱하는지가 눈에 보인다 |
| `BarVsHistogram` | 2교시 [60–85분] | 10초 | 떨어져 있다(범주형) vs 붙어 있다(연속형) |
| `HistogramFromTable` | 2교시 [60–85분] | 18초 | 슬라이드 12 의 도수표가 히스토그램이 되고, 세로축을 n 으로 나누면 넓이의 합이 1 이 된다 (6주차 밀도함수로 가는 다리) |
| `Skewness` | 2교시 [60–85분] | 10초 | 꼬리가 있는 쪽으로 평균이 끌려간다 |

## 렌더

저장소 루트(`manim_songhune/`)에서 실행한다.

```bash
./render.sh list    _2026/probstat/week01.py              # 씬 목록
./render.sh check   _2026/probstat/week01.py              # 전 씬 빠른 점검 (OK/FAIL)
./render.sh preview _2026/probstat/week01.py MeanVsMedian # 창으로 미리보기
./render.sh video   _2026/probstat/week01.py MeanVsMedian # 1080p mp4
./render.sh ppt     _2026/probstat/week01.py MeanVsMedian # PPT 삽입용 재인코딩
./render.sh png     _2026/probstat/week01.py Skewness     # 마지막 프레임 이미지
./render.sh all     _2026/probstat/week01.py              # 전부 1080p
```

결과물은 `videos/prob/week01/<SceneName>.mp4` 에 생긴다.
Notability 에 붙일 GIF 는 `./render.sh gif ...` 로 만들고 `확률과통계/확통 자료/수업안/영상/gif/` 에 떨어진다(1920px·15fps·디더링 없음). 수업일-순번 태그가 제목에 붙은 mp4·gif 사본은 `확률과통계/도구/영상_태그.py` 가 `영상/<MMDD>/` 에 만든다(원천 `영상/영상태그.csv`).

## 슬라이드에 넣기

영상이 들어간 슬라이드는 원본과 따로 둔다. 파일 이름 끝에 `_영상` 을 붙인다.

| 원본 | 영상판 | 담긴 씬 |
|---|---|---|
| `[0901]오리엔테이션.pptx` (15장) | `[0901]오리엔테이션_영상.pptx` (19장) | MontyHall, FrequencyView, BeliefUpdate, WhyVariability, PopulationAndSample, ProbabilityVsInference |
| `PS1_01_restyled.pptx` (14장) | `PS1_01_restyled_영상.pptx` (23장) | WhyVariability, ProbabilityVsInference, BiasedSample, MeanVsMedian, VarianceFormula, VarianceAsSquares, BarVsHistogram, HistogramFromTable, Skewness |
| `PS1_01_restyled_한글.pptx` (14장) | `PS1_01_restyled_한글_영상.pptx` (23장) | 위와 같음 |
| `PS1_02_restyled.pptx` (59장) | `PS1_02_restyled_영상.pptx` (66장) | SampleSpaceTree, EventsAndSetOps, MultiplicationRule, MultiplicationRuleClub, PermVsComb, AdditionRule, ComplementTrick |
| `PS1_02_restyled_한글.pptx` (59장) | `PS1_02_restyled_한글_영상.pptx` (66장) | 위와 같음 |

PS1_02 의 한글판·판서·학생 배포본까지의 순서는
`도구/한글판_생성.py` → `insert_videos.py` → `도구/판서_주석_추가.py` → `도구/학생배포본_생성.py` 다.

**영상은 그 영상이 다루는 개념 슬라이드 바로 앞에 넣는다** (2026-09-04 변경. 그전에는 뒤였다).
예제 풀이 영상만은 문제 슬라이드 다음, 풀이 슬라이드 앞이다. 답을 미리 보여 주지 않기 위해서다.
job 의 `place` 가 이것을 정하며, 이미 나간 오리엔테이션·PS1_01 덱은 교안의 슬라이드 표와 판서
덱이 옛 순서에 맞춰져 있어 `place="after"` 로 남겨 두었다.
삽입 위치의 근거는 `insert_videos.py` 의 `anchors` 에 적혀 있고, 스크립트가 만들어진 pptx 에서
실제 순서를 다시 세어 확인한다.

영상은 **16:9 전체 화면 슬라이드**로 넣는다. 본문 슬라이드 한구석에 작게 넣으면 축 이름과 자막이
강의실 스크린에서 읽히지 않는다. 재생은 PowerPoint 기본값인 **클릭할 때**이며, 교안의 진행 순서
(말 → 판서 → 영상)와 맞는다. 자동 재생으로 바꾸려면 영상을 고르고 `재생 → 시작: 자동 실행`.

손으로 한 장씩 넣지 않고 스크립트로 만든다. 씬을 다시 렌더한 뒤 같은 스크립트를 돌리면
슬라이드 구성은 그대로 두고 영상만 새것으로 바뀐다.

`MeanVsMedian` 은 마지막에 원래 값으로 되돌아가므로 **반복 재생**으로 두면
수업 중 몇 번이고 다시 보여 줄 수 있다.

한글판 `PS1_01_restyled_한글.pptx` 는 `확률과통계/도구/한글판_생성.py` 가 영문 원본에서 만든다.
본문을 고쳤으면 그 스크립트를 먼저 돌리고 이 스크립트를 돌린다. 순서가 바뀌면 한글판이 옛 본문으로 덮인다.

렌더한 mp4는 `확률과통계/확통 자료/수업안/영상/` 에 복사해 둔다.
재생 시점은 `교육메모/01주차.md` 의 차시별 슬라이드 항목에 적혀 있다.

**영상은 교수자용 슬라이드에만 넣는다.** 학생 배포본은 PDF라 영상이 살아남지 않고,
배포본의 성격(풀이가 비어 있는 문서)과도 맞지 않는다.

## 이 파일들의 약속

- 서체는 강의 템플릿과 같은 것을 쓴다 — 제목 `Ajou`, 본문 `Arita Buri KR`
- 색 의미를 고정한다
  - `MEAN_COLOR`(노랑) = 평균
  - `MED_COLOR`(청록) = 중앙값
  - `ACCENT`(파랑) = 표본·자료
  - `WARN`(빨강) = 극단값·음의 편차
- `slide_title()` 로 제목 위치를 슬라이드와 맞춘다
- 같은 자리에서 문구를 갈아 끼울 때는 `FadeOut` 과 `FadeIn` 을 **다른 play 로 나눈다**.
  한 play 에 묶으면 두 문장이 겹쳐 보이는 구간이 생기고, 문장이 긴 영문에서는 읽을 수 없게 된다
- 새 주차를 만들 때는 상수를 복사하지 말고 `ps_common.py` 에서 import 한다
- 무리를 가를 때는 치토의 색과 자세를 함께 바꾼다. 색만으로는 뒷자리에서 구분되지 않는다
- `counter()` 로 만든 숫자를 사라뜨리거나 옮기기 전에 `freeze()` 를 부른다.
  글리프가 매 프레임 다시 만들어져서 애니메이션과 점 개수가 어긋난다

## 주의 (ManimGL 1.7.2)

- ManimCommunity가 아니다. `MathTex` 대신 `Tex`, `Create` 대신 `ShowCreation`
- `f_always.method(...)` 는 **모든 인자가 함수**여야 한다.
  `DOWN`, `buff=0.05` 처럼 값이 섞이면 `add_updater(lambda m: ...)` 를 쓴다
- 점 구름 같은 도형 묶음에 `set_shape()` 를 쓰면 원이 타원으로 눌린다.
  좌표를 만들 때 비율을 주는 편이 안전하다
