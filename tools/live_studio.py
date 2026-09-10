# -*- coding: utf-8 -*-
"""라이브 코딩 실험: 왼쪽 영상, 오른쪽 코드. 코드를 돌리면 manimgl 이 뒤에서 렌더해 왼쪽에 띄운다.

    PYENV_VERSION=llm python tools/live_studio.py            # http://127.0.0.1:5077
    PYENV_VERSION=llm python tools/live_studio.py --port 5080 --hd

두 가지 모드
  코드  : construct 본문(또는 Scene 클래스 전체)을 쓰고 ⌘↩. 씬이 그대로 렌더된다.
  쉘    : IPython 처럼 한 줄씩 친다(`n = 6`, `p = 0.4`). 변수는 세션에 쌓인다.
          '렌더' 를 누르면 고른 템플릿(_2026/probstat/live_templates.py)을 상속한
          `class Live(템플릿): n = 6 ...` 파일을 만들어 렌더한다.

렌더는 480p(-l) 로 4–11초. 중간물은 동기화 폴더 밖 $TMPDIR/manim_songhune_live 에 둔다.
GitHub Pages 같은 정적 호스팅에서는 돌지 않는다(서버가 manimgl 을 실행해야 한다).
임의 코드를 실행하므로 127.0.0.1 에만 묶는다. 강의실에서 교수자 노트북으로 쓰는 용도다.
"""
import argparse
import ast
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import traceback
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, Response

ROOT = Path(__file__).resolve().parent.parent
PY = Path(sys.executable)
MANIMGL = PY.parent / "manimgl"
STAGE = Path(os.environ.get("MANIM_STAGE_LIVE", Path(tempfile.gettempdir()) / "manim_songhune_live"))
STAGE.mkdir(parents=True, exist_ok=True)
TEMPLATES = ROOT / "_2026" / "probstat" / "live_templates.py"

HEADER = (
    "from manim_imports_ext import *\n"
    "from _2026.probstat.ps_common import *\n"
    "from _2026.probstat.live_templates import *\n"
    "import itertools, math, random\n"
)

app = Flask(__name__)
SHELL_NS = {}          # 쉘 모드의 세션 네임스페이스 (한 사람이 쓰는 도구라 하나면 된다)
QUALITY = ["-l"]


# ── 템플릿 목록: import 하지 않고 ast 로 읽는다 ─────────────────────────
def list_templates():
    tree = ast.parse(TEMPLATES.read_text(encoding="utf-8"))
    out = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or node.name == "LiveScene":
            continue
        bases = [getattr(b, "id", "") for b in node.bases]
        if "LiveScene" not in bases:
            continue
        params, order = {}, []
        for st in node.body:
            if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
                name = st.targets[0].id
                try:
                    val = ast.literal_eval(st.value)
                except Exception:
                    continue
                if name == "params":
                    order = list(val)
                elif name != "heading":
                    params[name] = val
        order = order or list(params)
        out.append({"name": node.name, "doc": ast.get_docstring(node) or "",
                    "params": {k: params[k] for k in order if k in params}})
    return out


# ── 소스 만들기 ─────────────────────────────────────────────────────
def source_from_scene_code(code):
    """class ... Scene 이 있으면 그대로, 없으면 construct 본문으로 감싼다. (소스, 씬이름)"""
    m = re.search(r"^class\s+(\w+)\s*\(", code, re.M)
    if m:
        return HEADER + "\n" + code, m.group(1)
    body = textwrap.indent(code.rstrip() or "pass", " " * 8)
    src = HEADER + "\nclass Live(InteractiveScene):\n    def construct(self):\n" + body + "\n"
    return src, "Live"


def source_from_shell(template, ns):
    tpl = next((t for t in list_templates() if t["name"] == template), None)
    if tpl is None:
        raise ValueError("모르는 템플릿: %s" % template)
    lines = []
    for k in tpl["params"]:
        if k in ns:
            v = ns[k]
            if not isinstance(v, (int, float, str, bool, list, tuple)):
                raise ValueError("%s 는 숫자·문자열·리스트여야 한다: %r" % (k, v))
            lines.append("    %s = %r" % (k, v))
    body = "\n".join(lines) or "    pass"
    src = "from _2026.probstat.live_templates import *\n\nclass Live(%s):\n%s\n" % (template, body)
    return src, "Live"


# ── 렌더 ─────────────────────────────────────────────────────────────
def render(src, scene, frame_only=False):
    run_id = time.strftime("%H%M%S") + "_" + uuid.uuid4().hex[:6]
    work = STAGE / run_id
    work.mkdir()
    (work / "live.py").write_text(src, encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = "%s:%s" % (ROOT, ROOT / "legacy")
    env.pop("PYENV_VERSION", None)
    cmd = [str(MANIMGL), "live.py", scene, "-w", *QUALITY, "--video_dir", str(work)]
    if frame_only:
        cmd.append("-s")
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=300)
    dt = time.time() - t0
    log = re.sub(r"\x1b\[[0-9;]*m", "", (proc.stdout + proc.stderr).replace("\r", "\n"))
    log = "\n".join(l for l in log.splitlines() if l.strip() and "%|" not in l)
    ext = "png" if frame_only else "mp4"
    produced = list(work.rglob("*.%s" % ext))
    if proc.returncode != 0 or not produced:
        err = [l for l in log.splitlines() if re.match(r"^[A-Za-z_.]*(Error|Exception)", l)]
        shutil.rmtree(work, ignore_errors=True)
        return {"ok": False, "seconds": round(dt, 1), "log": log, "error": err[-1] if err else "렌더 실패",
                "source": src}
    out = STAGE / ("%s.%s" % (run_id, ext))
    shutil.copy(produced[0], out)
    shutil.rmtree(work, ignore_errors=True)
    return {"ok": True, "seconds": round(dt, 1), "log": log[-3000:], "url": "/out/" + out.name,
            "kind": ext, "source": src}


# ── 라우트 ─────────────────────────────────────────────────────────────
@app.get("/")
def index():
    return Response(PAGE, mimetype="text/html")


@app.get("/api/templates")
def api_templates():
    return jsonify(list_templates())


@app.post("/api/run")
def api_run():
    d = request.get_json(force=True)
    try:
        if d.get("mode") == "shell":
            src, scene = source_from_shell(d.get("template"), SHELL_NS)
        else:
            src, scene = source_from_scene_code(d.get("code", ""))
        return jsonify(render(src, scene, bool(d.get("frame_only"))))
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "log": traceback.format_exc(), "seconds": 0})


@app.post("/api/exec")
def api_exec():
    """IPython 처럼: 식이면 값을 보여 주고, 문이면 실행한다."""
    line = request.get_json(force=True).get("line", "")
    buf = io.StringIO()
    result, err = None, None
    with contextlib.redirect_stdout(buf):
        try:
            try:
                result = eval(compile(line, "<shell>", "eval"), SHELL_NS)
            except SyntaxError:
                exec(compile(line, "<shell>", "exec"), SHELL_NS)
        except Exception:
            err = traceback.format_exc(limit=1).strip().splitlines()[-1]
    ns = {k: repr(v) for k, v in SHELL_NS.items()
          if not k.startswith("_") and isinstance(v, (int, float, str, bool, list, tuple))}
    return jsonify({"out": buf.getvalue(), "result": None if result is None else repr(result),
                    "error": err, "ns": ns})


@app.post("/api/reset")
def api_reset():
    SHELL_NS.clear()
    return jsonify({"ok": True})


@app.get("/out/<path:name>")
def out_file(name):
    return send_from_directory(STAGE, name, max_age=0)


# ── 화면 ───────────────────────────────────────────────────────────────
PAGE = r"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<title>Manim Live Studio</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/material-darker.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
<style>
  :root { --bg:#111; --panel:#1b1b1b; --ink:#ddd; --mute:#888; --acc:#58c4dd; --warn:#fc6255; --ok:#83c167; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font: 14px/1.45 -apple-system, "Apple SD Gothic Neo", sans-serif; height:100vh; display:flex; flex-direction:column; }
  header { padding:8px 14px; border-bottom:1px solid #2a2a2a; display:flex; gap:14px; align-items:center; }
  header b { color:var(--acc); }
  header .q { margin-left:auto; color:var(--mute); font-size:12px; }
  main { flex:1; display:grid; grid-template-columns: 1fr 1fr; min-height:0; }
  .left { display:flex; flex-direction:column; border-right:1px solid #2a2a2a; min-height:0; }
  .stage { flex:1; display:flex; align-items:center; justify-content:center; background:#000; min-height:0; }
  .stage video, .stage img { width:100%; height:100%; object-fit:contain; background:#000; }
  .status { padding:6px 12px; font-size:12px; color:var(--mute); border-top:1px solid #2a2a2a; display:flex; gap:12px; align-items:center; }
  .status .err { color:var(--warn); }
  .status .ok { color:var(--ok); }
  .log { max-height:160px; overflow:auto; font: 11px/1.4 Menlo, monospace; color:#999; padding:6px 12px; white-space:pre-wrap; border-top:1px solid #2a2a2a; display:none; }
  .right { display:flex; flex-direction:column; min-height:0; }
  .tabs { display:flex; border-bottom:1px solid #2a2a2a; }
  .tabs button { background:none; border:0; color:var(--mute); padding:8px 16px; cursor:pointer; font-size:14px; }
  .tabs button.on { color:var(--ink); border-bottom:2px solid var(--acc); }
  .pane { flex:1; display:none; flex-direction:column; min-height:0; }
  .pane.on { display:flex; }
  .CodeMirror { flex:1; height:auto; font: 13px/1.5 Menlo, monospace; }
  textarea.plain { flex:1; background:var(--panel); color:var(--ink); border:0; font:13px/1.5 Menlo, monospace; padding:10px; resize:none; }
  .bar { padding:8px 12px; border-top:1px solid #2a2a2a; display:flex; gap:10px; align-items:center; }
  .bar button { background:var(--acc); color:#000; border:0; padding:6px 14px; border-radius:4px; font-weight:600; cursor:pointer; }
  .bar button.sec { background:#333; color:var(--ink); font-weight:400; }
  .bar button:disabled { opacity:.5; cursor:wait; }
  .bar label { color:var(--mute); font-size:12px; }
  select { background:#222; color:var(--ink); border:1px solid #333; padding:4px 8px; border-radius:4px; }
  .shell { flex:1; display:grid; grid-template-rows: auto 1fr auto; min-height:0; }
  .tpl { padding:8px 12px; border-bottom:1px solid #2a2a2a; display:flex; gap:10px; align-items:center; font-size:13px; }
  .tpl .doc { color:var(--mute); font-size:12px; }
  .repl { overflow:auto; font: 13px/1.5 Menlo, monospace; padding:8px 12px; }
  .repl .in { color:var(--acc); }
  .repl .in::before { content: "In: "; color:#3a8; }
  .repl .out::before { content: "Out: "; color:#c66; }
  .repl .err { color:var(--warn); }
  .repl .sys { color:var(--mute); font-style:italic; }
  .inrow { display:flex; border-top:1px solid #2a2a2a; }
  .inrow span { padding:8px 4px 8px 12px; color:#3a8; font: 13px/1.5 Menlo, monospace; }
  .inrow input { flex:1; background:none; border:0; color:var(--ink); font: 13px/1.5 Menlo, monospace; padding:8px; outline:none; }
  .ns { padding:6px 12px; font-size:12px; color:var(--mute); border-top:1px solid #2a2a2a; }
  .ns code { color:var(--ink); margin-right:10px; }
  details.src { border-top:1px solid #2a2a2a; }
  details.src summary { padding:6px 12px; font-size:12px; color:var(--mute); cursor:pointer; }
  details.src pre { margin:0; padding:6px 12px 10px; font: 12px/1.4 Menlo, monospace; color:#bbb; max-height:140px; overflow:auto; }
</style></head><body>
<header><b>Manim Live Studio</b><span>왼쪽 영상 · 오른쪽 코드 · 실행하면 다시 그린다</span><span class="q" id="q"></span></header>
<main>
  <section class="left">
    <div class="stage" id="stage"><span style="color:#555">아직 렌더한 것이 없다. 오른쪽에서 ⌘↩ 또는 '실행'.</span></div>
    <div class="status"><span id="st">대기</span><label style="margin-left:auto"><input type="checkbox" id="showlog"> 로그</label></div>
    <div class="log" id="log"></div>
  </section>
  <section class="right">
    <div class="tabs"><button class="on" data-p="code">코드</button><button data-p="shell">쉘</button></div>
    <div class="pane on" id="pane-code">
      <textarea id="code" class="plain">head = slide_title("Live")
self.play(FadeIn(head))

# 치토 6마리를 세우고 셋을 고른다
people = crowd(6, 2, 3, height=0.8)
self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.1))
picked = Group(*[ring(people[i], MEAN_COLOR) for i in (0, 2, 5)])
self.play(ShowCreation(picked))
self.play(Write(Tex(r"\binom{6}{3} = 20").next_to(people, DOWN, buff=0.6)))
self.wait(0.5)</textarea>
      <div class="bar">
        <button id="run">실행 ⌘↩</button>
        <label><input type="checkbox" id="frame"> 마지막 프레임만 (빠름)</label>
        <span style="margin-left:auto;color:#666;font-size:12px">construct 본문만 쓰거나, class 를 통째로 써도 된다</span>
      </div>
    </div>
    <div class="pane" id="pane-shell">
      <div class="shell">
        <div class="tpl">템플릿 <select id="tpl"></select><span class="doc" id="tpldoc"></span></div>
        <div class="repl" id="repl"><div class="sys">변수를 한 줄씩 넣는다. 예: n = 6 · p = 0.4 · total = 9 · 그 뒤 '렌더'. 식을 치면 값을 보여 준다.</div></div>
        <div>
          <div class="inrow"><span>In:</span><input id="line" placeholder="n = 6" autocomplete="off"></div>
          <div class="ns" id="ns">변수 없음</div>
          <details class="src"><summary>렌더할 소스</summary><pre id="src">(아직 없음)</pre></details>
          <div class="bar"><button id="render">렌더</button><button class="sec" id="reset">변수 비우기</button>
            <span style="margin-left:auto;color:#666;font-size:12px">템플릿의 매개변수만 반영된다</span></div>
        </div>
      </div>
    </div>
  </section>
</main>
<script>
const $ = s => document.querySelector(s);
let cm = null;
if (window.CodeMirror) {
  cm = CodeMirror.fromTextArea($('#code'), {mode:'python', theme:'material-darker', lineNumbers:true, indentUnit:4,
       extraKeys: {'Cmd-Enter': runCode, 'Ctrl-Enter': runCode}});
} else {
  $('#code').addEventListener('keydown', e => { if ((e.metaKey||e.ctrlKey) && e.key==='Enter') runCode(); });
}
const getCode = () => cm ? cm.getValue() : $('#code').value;

document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('on', x===b));
  document.querySelectorAll('.pane').forEach(p => p.classList.toggle('on', p.id==='pane-'+b.dataset.p));
  if (b.dataset.p==='shell') $('#line').focus(); else if (cm) cm.refresh();
});
$('#showlog').onchange = e => $('#log').style.display = e.target.checked ? 'block' : 'none';

let busy = false;
async function submit(payload) {
  if (busy) return; busy = true;
  $('#run').disabled = $('#render').disabled = true;
  $('#st').innerHTML = '렌더 중…';
  const t0 = performance.now();
  const tick = setInterval(() => $('#st').textContent = '렌더 중… ' + ((performance.now()-t0)/1000).toFixed(1) + 's', 200);
  try {
    const r = await fetch('/api/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
    const d = await r.json();
    $('#log').textContent = d.log || '';
    $('#src').textContent = d.source || '';
    if (d.ok) {
      const el = d.kind==='png' ? Object.assign(document.createElement('img'), {src:d.url}) :
                 Object.assign(document.createElement('video'), {src:d.url, controls:true, autoplay:true, loop:true, muted:true});
      $('#stage').replaceChildren(el);
      $('#st').innerHTML = '<span class="ok">완료</span> manimgl ' + d.seconds + 's';
    } else {
      $('#st').innerHTML = '<span class="err">' + (d.error||'실패') + '</span> ' + (d.seconds||'') + 's';
      $('#showlog').checked = true; $('#log').style.display = 'block';
    }
  } catch (e) { $('#st').innerHTML = '<span class="err">' + e + '</span>'; }
  clearInterval(tick); busy = false;
  $('#run').disabled = $('#render').disabled = false;
}
function runCode() { submit({mode:'code', code:getCode(), frame_only: $('#frame').checked}); }
$('#run').onclick = runCode;
$('#render').onclick = () => submit({mode:'shell', template: $('#tpl').value, frame_only: $('#frame').checked});

let TPL = [];
fetch('/api/templates').then(r => r.json()).then(list => {
  TPL = list;
  $('#tpl').replaceChildren(...list.map(t => Object.assign(document.createElement('option'), {value:t.name, textContent:t.name})));
  showDoc();
});
function showDoc() {
  const t = TPL.find(x => x.name === $('#tpl').value); if (!t) return;
  $('#tpldoc').textContent = t.doc.split('\n')[0] + '  ·  매개변수: ' +
    Object.entries(t.params).map(([k,v]) => k + ' = ' + JSON.stringify(v)).join(', ');
}
$('#tpl').onchange = showDoc;

const hist = []; let hi = 0;
$('#line').addEventListener('keydown', async e => {
  if (e.key === 'ArrowUp') { if (hi > 0) { hi--; e.target.value = hist[hi]; } e.preventDefault(); return; }
  if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; e.target.value = hist[hi] || ''; } e.preventDefault(); return; }
  if (e.key !== 'Enter') return;
  const line = e.target.value.trim(); if (!line) return;
  hist.push(line); hi = hist.length; e.target.value = '';
  const repl = $('#repl');
  repl.insertAdjacentHTML('beforeend', '<div class="in">' + esc(line) + '</div>');
  const r = await fetch('/api/exec', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({line})});
  const d = await r.json();
  if (d.out) repl.insertAdjacentHTML('beforeend', '<div>' + esc(d.out) + '</div>');
  if (d.result !== null && d.result !== undefined) repl.insertAdjacentHTML('beforeend', '<div class="out">' + esc(d.result) + '</div>');
  if (d.error) repl.insertAdjacentHTML('beforeend', '<div class="err">' + esc(d.error) + '</div>');
  repl.scrollTop = repl.scrollHeight;
  const ks = Object.entries(d.ns);
  $('#ns').innerHTML = ks.length ? ks.map(([k,v]) => '<code>' + esc(k) + ' = ' + esc(v) + '</code>').join('') : '변수 없음';
});
$('#reset').onclick = async () => { await fetch('/api/reset', {method:'POST'}); $('#ns').textContent = '변수 없음';
  $('#repl').insertAdjacentHTML('beforeend', '<div class="sys">변수를 비웠다</div>'); };
const esc = s => String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
$('#q').textContent = 'QUALITY_LABEL';
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5077)
    ap.add_argument("--hd", action="store_true", help="1080p 로 렌더 (느리다)")
    ap.add_argument("--medium", action="store_true", help="720p 로 렌더")
    a = ap.parse_args()
    global PAGE
    if a.hd:
        QUALITY[:] = ["--hd"]
    elif a.medium:
        QUALITY[:] = ["-m"]
    PAGE = PAGE.replace("QUALITY_LABEL", "render: manimgl " + " ".join(QUALITY) + " · stage: " + str(STAGE))
    if not MANIMGL.exists():
        sys.exit("manimgl 이 없다: %s (PYENV_VERSION=llm 으로 실행할 것)" % MANIMGL)
    print("Manim Live Studio → http://127.0.0.1:%d  (stage: %s)" % (a.port, STAGE))
    app.run(host="127.0.0.1", port=a.port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
