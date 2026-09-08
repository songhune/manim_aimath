# legacy — 3b1b 원본 저장소의 연도별 영상 소스

`_2015` ~ `_2025` 는 3Blue1Brown 원본 저장소(fork)의 영상 소스다. 강의에는 쓰지 않는다.
직접 만드는 강의용 씬은 `_2026/<과목>/` 에 둔다.

`outside_videos/` 와 `once_useful_constructs/sed.py` 가 `from _2016.zeta import ...` 처럼
이 폴더 안을 import 한다. `render.sh` 가 PYTHONPATH 에 `legacy` 를 넣어 주므로
옮기기 전과 똑같이 동작한다. 다른 방법으로 실행할 때는 다음을 직접 넣어야 한다.

    export PYTHONPATH="<저장소 루트>:<저장소 루트>/legacy:$PYTHONPATH"
