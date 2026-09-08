# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the 3Blue1Brown video creation repository containing the Python code used to generate the mathematical animations and visualizations for the 3Blue1Brown YouTube channel. The project is built on top of the Manim animation library (specifically the 3b1b version, not the community edition).

## Key Commands

### Running Scenes
- `manimgl <file_name> <scene_name>` - Render a scene to video
- `manimgl <file_name> <scene_name> -se <line_number>` - Drop into interactive mode at a specific line (like a debugger)
- `manimgl <file_name> <scene_name> -p` - Preview the scene without rendering to file

### Interactive Development
- `checkpoint_paste()` - In interactive mode, run code from clipboard with state management
- `checkpoint_paste(skip=True)` - Run code without animation (zero runtime)
- `checkpoint_paste(record=True)` - Record animations while running code

### Staging Scenes
- `python stage_scenes.py <module_name>` - Stage rendered scenes in order for a video module

## Architecture

### Directory Structure

이 저장소는 2026-2 전 과목이 함께 쓴다. 예전에는 `AI기초수학/manim_aimath/` 와
`확률과통계/manim_aimath/` 두 벌로 나뉘어 있었고, 두 사본이 갈라지면서 Synology
동기화 충돌 파일이 생겼다. 지금은 `2026-2/manim_songhune/` 한 곳으로 합쳤다.

- `_2026/<과목>/` - 강의용 씬. `aimath`, `probstat`, `bigdata`, `ml`
- `legacy/_YYYY/` - 3b1b 원본 저장소의 연도별 소스. 강의에는 쓰지 않는다
- `videos/<과목>/<파일이름>/` - 렌더 결과. PPT용은 `videos/<과목>/ppt/`
- `videos/_scratch/` - 점검용 산출물과 동기화 충돌본

`render.sh` 가 소스 경로에서 과목을 읽어 `--video_dir` 를 붙인다. 그래서
`_2026/aimath/week01.py` 와 `_2026/probstat/week01.py` 가 한 폴더로 섞이지 않는다.
`outside_videos/` 가 `from _2016.zeta import ...` 를 하므로 `render.sh` 는
PYTHONPATH 에 `legacy` 도 넣는다.

- `_YYYY/` (legacy 안) - Videos organized by year (e.g., `_2025/`, `_2024/`)
- `custom/` - Custom Manim extensions and reusable components
- `once_useful_constructs/` - Legacy utility classes and functions
- `outside_videos/` - Content for external collaborations and one-offs
- `sublime_custom_commands/` - Sublime Text editor integration

### Core Files
- `manim_imports_ext.py` - Universal import file that imports all Manim components plus custom extensions
- `custom_config.yml` - Manim configuration with custom paths and rendering settings
- `playground.py` - Sandbox file for testing and experimentation

### Video Project Structure
Each video project typically contains:
- Main scene files (e.g., `main.py`, `part1.py`, `part2.py`)
- `supplements.py` - Additional scenes and helper functions
- Helper modules for specific mathematical concepts

### Custom Components
- `custom/characters/` - Pi creature animations and scenes
- `custom/backdrops.py` - Background elements and visual themes
- `custom/drawings.py` - Custom drawing utilities
- `custom/end_screen.py` - Standard end screen components

## Development Workflow

### Scene Development
1. Create scene classes inheriting from `InteractiveScene` or `Scene`
2. Use `manimgl` with `-se` flag to develop interactively
3. Use `checkpoint_paste()` to iterate on animation code
4. Preview with `-p` flag before final rendering

### File Organization
- Start with `from manim_imports_ext import *` for all video files
- Organize scenes chronologically within files
- Use descriptive class names that match the video content
- Group related scenes in the same file

### Configuration
- Camera resolution: 4K (3840x2160) at 30fps
- Custom fonts and LaTeX configuration in `custom_config.yml`
- Dropbox integration for asset management and video output

## Code Patterns

### Scene Classes
- `InteractiveScene` - Base class for most scenes with interactive development support
- `PiCreatureScene` - Scenes featuring the Pi creature character
- `TeacherStudentsScene` - For Pi creature classroom interactions
- Custom scene classes for specific mathematical contexts

### Animation Patterns
- Use `self.play()` for animations
- `self.wait()` for pauses
- `self.add()` for static elements
- Color constants: `BLUE`, `YELLOW`, `RED`, etc.
- Mathematical typesetting with `Tex()` (use this instead of `MathTex()` which is from ManimCommunity)
- Format LaTeX strings with raw strings: `Tex(R"\pi")`, `Tex(R"\frac{1}{2}")`, etc.
- Use `lag_ratio` parameter for staggered animations: `FadeIn(objects, lag_ratio=0.1)`
- Common sequence: `self.play(Write(equation))` followed by `self.wait()`

### Mathematical Objects
- `NumberPlane` and `ComplexPlane` for coordinate systems
- `ParametricCurve` for mathematical curves
- `VGroup` for grouping related objects
- When creating multiple similar objects (e.g., multiple `NumberLine`s), create them within a `Group` or `VGroup` to avoid code duplication
- Custom mathematical visualization classes in `once_useful_constructs/`

### Code Organization
- Place configuration constants at the top of files
- Use class attributes for scene-specific configuration: `initial_positions = [10.5, 8]`
- Helper methods use `get_*` naming pattern: `get_spring()`, `get_mass()`
- Access frame with `frame = self.frame` for camera operations

### Color and Styling
- Use text-to-color mapping for mathematical expressions: `Tex(formula, t2c={"x": BLUE, "y": RED})`
- Consistent color schemes: earth=BLUE, sun=YELLOW, mathematical variables get specific colors
- Set properties with chained methods: `object.set_stroke(color, width).set_fill(color, opacity)`

### Updaters and Animation Control
- Use updaters for dynamic positioning: `object.add_updater(lambda m: m.move_to(target.get_center()))`
- Alternative syntax: `object.f_always.move_to(reference.get_center)`
- Use `LaggedStart(*animations, lag_ratio=0.1)` for sequential overlapping animations

## Python Code Style
- Do not include indentation spaces on blank lines
- Keep blank lines completely empty (no whitespace)
- Prefer existing utility functions over one-off index math. For example, use `color_gradient(colors, n)` to produce a list of interpolated colors rather than calling `interpolate_color` manually inside a loop with `i / (n - 1)` arithmetic.
- Construct VGroups declaratively when possible. If the full meaning of a group can be expressed in one expression, prefer `VGroup(*[...])` or `VGroup(... for ...)` over a for loop that progressively calls `.add()`. Reserve the progressive style for cases where each iteration has non-trivial side effects.
- Use existing layout methods (`.arrange()`, `.next_to()`, `.move_to()`) instead of manual in-place coordinate logic. A small amount of redundant movement is preferable to bespoke positioning arithmetic that is harder to read and easier to get wrong.

## Notes

- This repository uses the 3b1b version of Manim, not ManimCommunity
- The project integrates with Sublime Text for enhanced development workflow
- Video assets are managed through Dropbox with custom path configurations
- Each year's videos are self-contained in their respective directories
- No formal testing framework - scenes are tested through visual preview and rendering
## Mascot / 기호 디폴트 (2026-2 강의 콘텐츠)

- 씬에서 사람·개체·학생을 나타내는 기호의 **디폴트는 아주대 마스코트 '치토'(chito)**다.
  Pi creature나 speech/thought bubble 예제를 그대로 쓰지 않는다.
- 낱장은 `2026-2/확률과통계/이미지/치토/` 에 있다. 두 자세 × 다섯 색 × (테두리 유/무).
  검은 배경(manim)에서는 `_outline` 판을, 흰 배경 슬라이드에서는 테두리 없는 쪽을 쓴다.

  | 자세 | 색 | 파일 이름 |
  |---|---|---|
  | front / back | 기본(파랑) | `chito_{front,back}_outline.png` |
  | front / back | teal · red · gold · grey | `chito_{front,back}_{tint}_outline.png` |

  기본 네 장은 `extract_chito.py` 가, 색 판본은 `tint_chito.py` 가 만든다. 색 판본은
  몸통 파랑(H 190°–250°)만 돌린 것이라 크림색 얼굴과 살색은 원본 그대로 남는다.
- 씬에서는 `_2026/probstat/ps_common.py` 의 `chito(pose, tint, height)` 와
  `crowd(n, rows, cols, ...)` 를 쓴다. 주차 파일마다 상수를 복사하지 않는다.
- **무리를 가를 때는 색과 자세를 함께 바꾼다.** 색만으로는 강의실 뒷자리에서 구분되지 않고
  색을 가리기 어려운 학생에게는 아무 정보도 아니다. 자세에는 뜻을 담는다 — 등을 돌린 치토는
  응답하지 않은 사람이다 (`week01.py` 의 `BiasedSample`).
- `ImageMobject` 는 `VMobject` 가 아니므로 `Group` 으로 묶는다. 강조는 `ring()`,
  무리 테두리는 `panel()`, 흐리게는 개체별 `set_opacity()` 다.
- **`Transform` 으로는 그림이 바뀌지 않는다.** 점만 보간되고 텍스처는 원본 그대로 남는다.
  자세나 색을 바꾸려면 `ps_common.swap_pose(scene, mobs, pose, tint)` 를 쓴다
  (옛 판을 지우고 새 판을 같은 자리에 띄운다).

## 확률과통계 공용 모듈 (`_2026/probstat/ps_common.py`)

week00~week02 가 함께 쓰는 서체·색·치토·도우미가 여기 있다. 새 주차 파일은 상수를
복사하지 말고 여기서 import 한다.

| 이름 | 하는 일 |
|---|---|
| `chito` / `crowd` / `swap_pose` | 마스코트 한 마리 / 격자로 세운 무리 / 자세·색 갈아 끼우기 |
| `ring` / `panel` | 개체 하나를 감싸는 둥근 테두리 / 무리를 감싸는 상자 |
| `label` / `note` / `title` / `slide_title` / `under` | 화면 문구 |
| `counter` / `named_counter` / `freeze` | 트래커를 따라가는 숫자 |
| `sweep` | 무리를 훑는 동작 (조사·측정·검사) |
| `swap` | 같은 자리의 문구를 갈아 끼우기 |

**`label()` 은 여섯 낱말을 넘으면 예외를 낸다.** 하네스 3.6 의 규칙이고, 넘길 만큼
설명이 길어졌다면 그 설명은 화면이 아니라 교안의 대본으로 가야 한다는 뜻이다.
`./render.sh check` 가 이걸 잡아 준다.

**`counter()` 가 만든 숫자는 매 프레임 글리프를 다시 만든다.** 그 상태로 `FadeOut` 이나
`.animate` 를 걸면 애니메이션이 붙잡아 둔 사본과 점 개수가 어긋나 broadcast 오류가 난다.
사라뜨리거나 옮기기 전에 `freeze()` 를 먼저 부른다.

## 렌더 결과물과 Synology 동기화

`videos/` 는 Synology Drive 동기화 폴더 안에 있다. manimgl 이 프레임을 이어붙이는
동안 동기화가 끼어들면 `sqlite3.OperationalError: disk I/O error` 가 나거나
`...Conflict.mp4` 사본이 생긴다. 그래서 `render.sh` 는 동기화 밖(`$TMPDIR`)에서
렌더한 뒤 **다 된 파일만** `videos/` 로 옮긴다. 다른 자리를 쓰려면 `MANIM_STAGE` 로
덮어쓴다. manimgl 을 직접 부를 때는 `--video_dir` 을 동기화 밖으로 두는 것이 안전하다.
