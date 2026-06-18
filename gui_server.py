"""
UMBRA GUI Server v2.0 - Fixed
Start: python gui_server.py
Open:  http://localhost:7860
"""

import sys
import os
import json
import threading
import time
from datetime import datetime

_UMBRA_ROOT = os.path.dirname(os.path.abspath(__file__))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)

try:
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("[GUI] Run: pip install flask flask-cors")
    sys.exit(1)

app = Flask(__name__, static_folder=os.path.join(_UMBRA_ROOT, "gui_static"))
CORS(app)

_runtime = None
_runtime_lock = threading.Lock()
_runtime_ready = False
_runtime_error = None


def _build_runtime_bg():
    global _runtime, _runtime_ready, _runtime_error
    try:
        print("[GUI] Building Umbra runtime...")
        from umbra import build_runtime
        _runtime = build_runtime()
        _runtime_ready = True
        print("[GUI] Runtime ready.")
    except Exception as e:
        _runtime_error = str(e)
        print(f"[GUI] Runtime error: {e}")


# Start runtime in background immediately
threading.Thread(target=_build_runtime_bg, daemon=True).start()


def get_runtime():
    if _runtime_ready and _runtime:
        return _runtime
    return None


@app.route("/")
def index():
    return send_from_directory(os.path.join(_UMBRA_ROOT, "gui_static"), "index.html")


@app.route("/api/ready")
def api_ready():
    return jsonify({
        "ready": _runtime_ready,
        "error": _runtime_error,
        "loading": not _runtime_ready and _runtime_error is None,
    })


@app.route("/api/status")
def api_status():
    rt = get_runtime()
    if not rt:
        return jsonify({
            "ready": False,
            "loading": _runtime_error is None,
            "error": _runtime_error,
            "provider": "loading...",
            "model": "loading...",
            "free": False,
            "runs_this_session": 0,
            "memory_entries": 0,
            "memory_pct": 0,
            "gaming_detected": False,
            "gaming_processes": [],
            "scheduler_jobs": 0,
            "version": "2.0.0",
        })
    llm = rt["llm"]
    runs = rt["pipeline"].get_run_history()
    mem = rt["memory"]
    rm = rt.get("resource_manager")
    rs = rm.get_current_status() if rm else {}
    return jsonify({
        "ready": True,
        "provider": llm.get_provider(),
        "model": llm.get_model(),
        "free": llm.is_free(),
        "runs_this_session": len(runs),
        "memory_entries": mem.size(),
        "memory_pct": rs.get("memory_pct", 0),
        "gaming_detected": rs.get("gaming_detected", False),
        "gaming_processes": rs.get("gaming_processes", []),
        "scheduler_jobs": len(rt["scheduler"].jobs) if rt.get("scheduler") else 0,
        "version": "2.0.0",
    })


@app.route("/api/run", methods=["POST"])
def api_run():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "Runtime not ready yet. Please wait a moment and try again."}), 503
    data = request.json or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    try:
        run = rt["pipeline"].run(prompt)
        rt["monitor"].record(run)
        rt["memory"].store(
            f"run:{run.run_id}",
            {"prompt": prompt, "status": run.status, "files": len(run.written_files)},
            tags=["run", run.status],
        )
        # Auto-assemble if game/app files written
        assembled = None
        if run.written_files and len(run.written_files) > 2:
            assembled = _try_assemble_run(run, prompt)

        return jsonify({
            "run_id": run.run_id,
            "status": run.status,
            "tasks": len(run.tasks),
            "files_written": len(run.written_files),
            "files": [{"file": f["file"], "lines": f["lines"]} for f in run.written_files],
            "error": run.error,
            "completed_at": run.completed_at,
            "succeeded_tasks": [r.task_id for r in run.results if r.success],
            "failed_tasks": [r.task_id for r in run.results if not r.success],
            "assembled_file": assembled,
            "workspace": os.path.join(_UMBRA_ROOT, "workspaces", run.run_id),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _try_assemble_run(run, prompt):
    """Try to assemble multiple generated files into one runnable main.py"""
    try:
        ws_base = os.path.join(_UMBRA_ROOT, "workspaces", run.run_id)
        code_dir = os.path.join(ws_base, "code")
        if not os.path.exists(code_dir):
            return None

        # Collect all valid Python files sorted by task number
        py_files = sorted([
            f for f in os.listdir(code_dir)
            if f.endswith(".py") and f.startswith("run_") and "_task_" in f
        ])

        if not py_files:
            return None

        # Check if any file already has a full game loop or main block
        for fname in py_files:
            fpath = os.path.join(code_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if "pygame.init()" in content and "while True" in content and "pygame.display" in content:
                # This is a complete game file, copy it as game.py
                game_path = os.path.join(code_dir, "game.py")
                with open(game_path, "w", encoding="utf-8") as out:
                    out.write(content)
                return game_path
            if "__name__" in content and "main()" in content and "if __name__" in content:
                # Has a main entry point
                app_path = os.path.join(code_dir, "app.py")
                with open(app_path, "w", encoding="utf-8") as out:
                    out.write(content)
                return app_path

        # Find the largest/most complete file as the entry point
        best_file = max(
            [os.path.join(code_dir, f) for f in py_files],
            key=lambda p: os.path.getsize(p)
        )
        main_path = os.path.join(code_dir, "main.py")
        if not os.path.exists(main_path):
            import shutil
            shutil.copy(best_file, main_path)
        return main_path
    except Exception:
        return None


@app.route("/api/history")
def api_history():
    rt = get_runtime()
    if not rt:
        return jsonify({"runs": [], "total": 0})
    runs = rt["pipeline"].get_run_history()
    return jsonify({"runs": runs[-20:], "total": len(runs)})


@app.route("/api/metrics")
def api_metrics():
    rt = get_runtime()
    if not rt:
        return jsonify({"total_runs": 0, "successful_runs": 0, "failed_runs": 0,
                        "success_rate_pct": 0, "total_files_written": 0,
                        "total_tasks_executed": 0, "avg_duration_seconds": 0})
    return jsonify(rt["monitor"].get_summary())


@app.route("/api/health")
def api_health():
    rt = get_runtime()
    if not rt:
        return jsonify({"overall_status": "loading", "checks": [],
                        "pass_count": 0, "warn_count": 0, "fail_count": 0})
    report = rt["health"].run_all_checks()
    return jsonify(report.to_dict())


@app.route("/api/memory")
def api_memory():
    rt = get_runtime()
    if not rt:
        return jsonify({"stats": {"total_entries": 0, "max_entries": 1000, "total_accesses": 0}, "keys": []})
    mem = rt["memory"]
    return jsonify({"stats": mem.get_stats(), "keys": mem.list_keys()[:50]})


@app.route("/api/memory/store", methods=["POST"])
def api_memory_store():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    data = request.json or {}
    key = data.get("key") or f"note:{datetime.now().isoformat()}"
    value = data.get("value", "")
    tags = data.get("tags", ["user_note"])
    rt["memory"].store(key, value, tags=tags)
    rt["memory"].save()
    return jsonify({"stored": True, "key": key})


@app.route("/api/memory/search", methods=["POST"])
def api_memory_search():
    rt = get_runtime()
    if not rt:
        return jsonify({"results": []})
    data = request.json or {}
    query = data.get("query", "")
    results = rt["memory"].search(query, top_k=10)
    return jsonify({"results": [{"key": r.key, "value": str(r.value)[:200]} for r in results]})


@app.route("/api/workspaces")
def api_workspaces():
    ws_dir = os.path.join(_UMBRA_ROOT, "workspaces")
    workspaces = []
    if os.path.exists(ws_dir):
        for d in sorted(os.listdir(ws_dir), reverse=True)[:30]:
            ws_path = os.path.join(ws_dir, d)
            if not os.path.isdir(ws_path):
                continue
            code_dir = os.path.join(ws_path, "code")
            files = []
            runnable = None
            if os.path.exists(code_dir):
                for f in sorted(os.listdir(code_dir)):
                    if f.endswith(".py"):
                        fp = os.path.join(code_dir, f)
                        try:
                            with open(fp) as fh:
                                lines = len(fh.readlines())
                            files.append({"name": f, "lines": lines, "path": fp})
                            if f in ("game.py", "main.py", "app.py"):
                                runnable = fp
                        except Exception:
                            pass
            workspaces.append({
                "run_id": d,
                "files": files,
                "file_count": len(files),
                "runnable": runnable,
            })
    return jsonify({"workspaces": workspaces})


@app.route("/api/file")
def api_file():
    path = request.args.get("path", "")
    if not path or not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    # Security: must be inside umbra root
    try:
        real = os.path.realpath(path)
        root = os.path.realpath(_UMBRA_ROOT)
        if not real.startswith(root):
            return jsonify({"error": "access denied"}), 403
    except Exception:
        return jsonify({"error": "invalid path"}), 403
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return jsonify({"content": content, "path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/run_file", methods=["POST"])
def api_run_file():
    """Run a generated Python file and return output."""
    data = request.json or {}
    path = data.get("path", "")
    if not path or not os.path.exists(path):
        return jsonify({"error": "file not found"}), 404
    try:
        real = os.path.realpath(path)
        root = os.path.realpath(_UMBRA_ROOT)
        if not real.startswith(root):
            return jsonify({"error": "access denied"}), 403
    except Exception:
        return jsonify({"error": "invalid path"}), 403

    # For game files, launch in new window
    if path.endswith(".py"):
        try:
            import subprocess
            if sys.platform == "win32":
                subprocess.Popen(
                    [sys.executable, path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    cwd=os.path.dirname(path),
                )
            else:
                subprocess.Popen([sys.executable, path], cwd=os.path.dirname(path))
            return jsonify({"launched": True, "path": path})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "not a Python file"}), 400


@app.route("/api/config")
def api_config_get():
    rt = get_runtime()
    if not rt:
        return jsonify({})
    return jsonify(rt["config"].to_dict())


@app.route("/api/config", methods=["POST"])
def api_config_set():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    data = request.json or {}
    for key, val in data.items():
        rt["config"].set(key, val)
    rt["config"].save()
    return jsonify({"saved": True})


@app.route("/api/ollama/models")
def api_ollama_models():
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as resp:
            data = json.loads(resp.read())
            models = [m["name"] for m in data.get("models", [])]
            return jsonify({"models": models, "available": True})
    except Exception:
        return jsonify({"models": [], "available": False})


@app.route("/api/validate_last", methods=["POST"])
def api_validate_last():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    last = rt["pipeline"].get_last_run()
    if last and last.written_files:
        ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
        result = rt["run_validator"].validate_run(last, workspace_base=ws_base)
        return jsonify(result.to_dict())
    return jsonify({"error": "no recent run"}), 404


@app.route("/api/review_last", methods=["POST"])
def api_review_last():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    last = rt["pipeline"].get_last_run()
    if last and last.written_files:
        ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
        reviews = rt["reviewer"].review_pipeline_run(last, workspace_base=ws_base)
        avg = rt["reviewer"].get_aggregate_score(reviews)
        return jsonify({
            "run_id": last.run_id,
            "average_score": avg,
            "file_count": len(reviews),
            "reviews": [r.to_dict() for r in reviews],
        })
    return jsonify({"error": "no recent run"}), 404

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Natural language chat endpoint.
    Classifies intent, asks clarifying questions, routes appropriately.
    """
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "Runtime not ready"}), 503

    data = request.json or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "message required"}), 400

    conv = rt.get("conversation")
    if not conv:
        return jsonify({"error": "Conversation engine not available"}), 503

    # Add user turn to history
    conv.add_turn("user", message, "input")

    # Classify intent
    classification = conv.classify(message)

    response = {
        "intent": classification.intent,
        "confidence": classification.confidence,
        "needs_clarification": classification.needs_clarification,
        "clarification_question": None,
        "response": None,
        "run_result": None,
        "image_result": None,
    }

    # Handle clarification needed
    if classification.needs_clarification and classification.clarification_questions:
        question = conv.start_clarification(classification, message)
        response["clarification_question"] = question
        response["response"] = question
        conv.add_turn("umbra", question, "clarification")
        return jsonify(response)

    # Route by intent
    if classification.intent == "command":
        cmd = classification.metadata.get("command", "")
        response["response"] = _handle_command(rt, cmd)

    elif classification.intent == "question":
        answer = conv.answer_question(message)
        response["response"] = answer
        conv.add_turn("umbra", answer, "answer")

    elif classification.intent == "game_request":
        game_prompt = conv.build_game_prompt(
            classification.metadata.get("raw", message)
        )
        run = rt["pipeline"].run(game_prompt)
        rt["monitor"].record(run)

        # Auto-test the result
        if run.written_files:
            ws_base = os.path.join(_UMBRA_ROOT, "workspaces")
            tester = rt.get("game_tester")
            if tester:
                best_path, test_result = tester.find_best_runnable(run.run_id,
                    os.path.join(_UMBRA_ROOT, "workspaces"))
                test_info = test_result.to_dict() if test_result else None
            else:
                best_path, test_info = None, None

        assembled = _try_assemble_run(run, message)
        msg = (f"Game generated! Run: {run.run_id} | Status: {run.status} | "
               f"Files: {len(run.written_files)}")
        if assembled:
            msg += f"\nRunnable file: {assembled}"
        response["response"] = msg
        response["run_result"] = {
            "run_id": run.run_id,
            "status": run.status,
            "files": [{"file": f["file"], "lines": f["lines"]} for f in run.written_files],
            "assembled": assembled,
        }
        conv.add_turn("umbra", msg, "task_result")

    elif classification.intent == "image_request":
        img_gen = rt.get("image_generator")
        if img_gen:
            result = img_gen.generate(classification.metadata.get("raw", message))
            if result.success:
                response["response"] = f"Image generated: {result.file_path}"
            else:
                response["response"] = result.fallback_description or result.error
            response["image_result"] = result.to_dict()
        else:
            response["response"] = ("Image generation requires Stable Diffusion. "
                                     "Install it at localhost:7861 to enable this feature.")

    elif classification.intent == "video_request":
        vid_gen = rt.get("video_generator")
        if vid_gen:
            result = vid_gen.generate(classification.metadata.get("raw", message))
            response["response"] = result.fallback_description if not result.success else f"Video: {result.file_path}"
        else:
            response["response"] = ("Video generation requires ComfyUI. "
                                     "Install it at localhost:8188 to enable.")

    elif classification.intent == "task":
        run = rt["pipeline"].run(message)
        rt["monitor"].record(run)
        assembled = _try_assemble_run(run, message)
        msg = f"Done! {run.run_id} | {run.status} | {len(run.written_files)} files"
        if assembled:
            msg += f"\nAssembled: {assembled}"
        response["response"] = msg
        response["run_result"] = {
            "run_id": run.run_id,
            "status": run.status,
            "files": [{"file": f["file"], "lines": f["lines"]} for f in run.written_files],
            "assembled": assembled,
        }
        conv.add_turn("umbra", msg, "task_result")

    else:
        # General chat — use LLM for a natural response
        if rt["llm"].is_configured():
            system = ("You are Umbra, an autonomous AI runtime OS. "
                      "Be helpful, friendly, and direct. You can build games, apps, scripts, APIs. "
                      "If the user seems to want to build something, say so and ask what they want.")
            llm_resp = rt["llm"].complete(message, system_prompt=system, max_tokens=300)
            ans = llm_resp.content.strip() if llm_resp.success else "I'm here! Tell me what you'd like to build."
        else:
            ans = "I'm Umbra — tell me what you'd like to build!"
        response["response"] = ans
        conv.add_turn("umbra", ans, "chat")

    return jsonify(response)


def _handle_command(rt, cmd):
    if cmd == "health":
        report = rt["health"].run_all_checks()
        d = report.to_dict()
        return f"Health: {d['overall_status'].upper()} | Pass: {d['pass_count']} Warn: {d['warn_count']}"
    if cmd == "metrics":
        m = rt["monitor"].get_summary()
        return (f"Metrics: {m['total_runs']} runs | {m['success_rate_pct']}% success | "
                f"{m['total_files_written']} files written")
    if cmd == "history":
        runs = rt["pipeline"].get_run_history()
        if not runs:
            return "No runs this session."
        return "\n".join(f"{r['run_id']}: {r['status']} | {r['prompt'][:50]}" for r in runs[-5:])
    if cmd == "memory":
        mem = rt["memory"]
        return f"Memory: {mem.size()} entries stored."
    return f"Command '{cmd}' acknowledged."


@app.route("/api/voice/listen", methods=["POST"])
def api_voice_listen():
    """Listen for one voice command."""
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    voice = rt.get("voice_input")
    if not voice:
        return jsonify({"error": "Voice module not available", "available": False})
    if not voice.is_available():
        return jsonify({"error": "SpeechRecognition not installed", "available": False})
    result = voice.listen_once(timeout=8, phrase_limit=20)
    return jsonify(result.to_dict())


@app.route("/api/game/test", methods=["POST"])
def api_game_test():
    """Test a generated game file."""
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    data = request.json or {}
    file_path = data.get("path", "")
    tester = rt.get("game_tester")
    if not tester:
        return jsonify({"error": "Game tester not available"}), 503
    result = tester.test_file(file_path)
    return jsonify(result.to_dict())


@app.route("/api/image/generate", methods=["POST"])
def api_image_generate():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    data = request.json or {}
    prompt = data.get("prompt", "")
    img_gen = rt.get("image_generator")
    if not img_gen:
        return jsonify({"error": "Image generator not available"}), 503
    result = img_gen.generate(
        prompt,
        negative_prompt=data.get("negative_prompt", ""),
        width=data.get("width", 512),
        height=data.get("height", 512),
        steps=data.get("steps", 20),
    )
    return jsonify(result.to_dict())


@app.route("/api/image/list")
def api_image_list():
    rt = get_runtime()
    if not rt:
        return jsonify({"images": []})
    img_gen = rt.get("image_generator")
    if not img_gen:
        return jsonify({"images": []})
    return jsonify({"images": img_gen.list_generated_images()})


@app.route("/api/video/generate", methods=["POST"])
def api_video_generate():
    rt = get_runtime()
    if not rt:
        return jsonify({"error": "not ready"}), 503
    data = request.json or {}
    prompt = data.get("prompt", "")
    vid_gen = rt.get("video_generator")
    if not vid_gen:
        return jsonify({"error": "Video generator not available"}), 503
    result = vid_gen.generate(prompt, frames=data.get("frames", 16))
    return jsonify(result.to_dict())


@app.route("/api/conversation/history")
def api_conversation_history():
    rt = get_runtime()
    if not rt:
        return jsonify({"history": []})
    conv = rt.get("conversation")
    if not conv:
        return jsonify({"history": []})
    return jsonify({"history": conv.get_history()})


@app.route("/api/conversation/clear", methods=["POST"])
def api_conversation_clear():
    rt = get_runtime()
    if not rt:
        return jsonify({"cleared": False})
    conv = rt.get("conversation")
    if conv:
        conv.clear_history()
    return jsonify({"cleared": True})


def create_static_files():
    static_dir = os.path.join(_UMBRA_ROOT, "gui_static")
    os.makedirs(static_dir, exist_ok=True)

    html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>UMBRA v2.0 — Autonomous AI Runtime OS</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0d0d;color:#e0e0e0;font-family:'Segoe UI',monospace;height:100vh;display:flex;flex-direction:column;overflow:hidden}
header{background:#1a1a2e;padding:10px 16px;border-bottom:1px solid #30305a;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
header h1{color:#7c83fd;font-size:1.1rem;letter-spacing:1px}
#status-bar{font-size:0.75rem;display:flex;gap:10px;align-items:center}
.pill{background:#1e1e3a;padding:3px 10px;border-radius:20px;border:1px solid #30305a;color:#888;transition:all 0.3s}
.pill.green{border-color:#4caf50;color:#4caf50}
.pill.red{border-color:#f44336;color:#f44336}
.pill.yellow{border-color:#ff9800;color:#ff9800}
.pill.blue{border-color:#2196f3;color:#2196f3}
#loading-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:#0d0d0d;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:100}
#loading-overlay h2{color:#7c83fd;margin-bottom:16px}
#loading-overlay p{color:#888;font-size:0.9rem}
.spinner-large{width:40px;height:40px;border:3px solid #333;border-top-color:#7c83fd;border-radius:50%;animation:spin 0.8s linear infinite;margin-bottom:20px}
@keyframes spin{to{transform:rotate(360deg)}}
.main{display:flex;flex:1;overflow:hidden}
.sidebar{width:220px;background:#111122;border-right:1px solid #222244;padding:14px;overflow-y:auto;flex-shrink:0}
.sidebar h3{color:#7c83fd;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;margin-top:14px}
.sidebar h3:first-child{margin-top:0}
.stat{display:flex;justify-content:space-between;margin-bottom:6px;font-size:0.8rem}
.stat-val{color:#7c83fd;font-weight:bold;max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gaming-badge{background:#ff990020;border:1px solid #ff9900;color:#ff9900;border-radius:4px;padding:4px 8px;font-size:0.72rem;margin-top:8px;text-align:center;display:none}
.sidebar button{width:100%;margin-bottom:5px;background:#1e1e3a;border:1px solid #30305a;color:#ccc;border-radius:5px;padding:7px;cursor:pointer;font-size:0.8rem;text-align:left;transition:background 0.2s}
.sidebar button:hover{background:#30305a;color:#fff}
.nav-tabs{display:flex;background:#111122;border-bottom:1px solid #222244;padding:0 14px;flex-shrink:0}
.nav-tab{padding:9px 16px;cursor:pointer;font-size:0.83rem;color:#888;border-bottom:2px solid transparent;transition:all 0.2s;user-select:none}
.nav-tab:hover{color:#ccc}
.nav-tab.active{color:#7c83fd;border-bottom-color:#7c83fd}
.content-area{flex:1;display:flex;flex-direction:column;overflow:hidden}
.tab-panel{display:none;flex:1;flex-direction:column;padding:14px;overflow:hidden}
.tab-panel.active{display:flex}
#chat-output{flex:1;overflow-y:auto;background:#0a0a1a;border:1px solid #222244;border-radius:6px;padding:12px;margin-bottom:10px;font-size:0.82rem;line-height:1.7}
.msg{margin-bottom:10px;padding:6px 10px;border-radius:4px}
.msg.user{color:#a0a8ff;border-left:3px solid #7c83fd;background:#1a1a3a}
.msg.umbra{color:#e0e0e0;border-left:3px solid #333}
.msg.system{color:#666;font-style:italic;font-size:0.78rem}
.msg.success{color:#4caf50;border-left:3px solid #4caf50;background:#0a1a0a}
.msg.error{color:#f44336;border-left:3px solid #f44336;background:#1a0a0a}
.msg.file{color:#888;font-size:0.78rem;padding:3px 10px;border-left:2px solid #333}
.chat-row{display:flex;gap:8px;flex-shrink:0}
#chat-input{flex:1;background:#111122;border:1px solid #30305a;border-radius:6px;padding:10px 14px;color:#e0e0e0;font-size:0.88rem;outline:none;resize:none;height:44px}
#chat-input:focus{border-color:#7c83fd}
.btn{background:#7c83fd;color:#fff;border:none;border-radius:6px;padding:10px 16px;cursor:pointer;font-size:0.85rem;transition:background 0.2s;white-space:nowrap}
.btn:hover{background:#6c73ed}
.btn:disabled{background:#333;cursor:not-allowed;color:#666}
.btn-secondary{background:#222244;border:1px solid #30305a;color:#ccc}
.btn-secondary:hover{background:#30305a;color:#fff}
.btn-green{background:#1a4a1a;border:1px solid #4caf50;color:#4caf50}
.btn-green:hover{background:#2a5a2a}
.metrics-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px;flex-shrink:0}
.metric-card{background:#111122;border:1px solid #222244;border-radius:8px;padding:14px}
.metric-card .label{font-size:0.68rem;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px}
.metric-card .value{font-size:1.5rem;color:#7c83fd;font-weight:bold}
.scroll-list{background:#0a0a1a;border:1px solid #222244;border-radius:6px;padding:10px;flex:1;overflow-y:auto}
.list-item{padding:7px 0;border-bottom:1px solid #1a1a2a;font-size:0.8rem}
.list-item:last-child{border-bottom:none}
.health-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:8px;flex-shrink:0}
.dot-pass{background:#4caf50}
.dot-warn{background:#ff9800}
.dot-fail{background:#f44336}
.file-row{display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #1a1a2a}
.file-row .fname{color:#aaa;cursor:pointer;text-decoration:underline;font-size:0.78rem;flex:1}
.file-row .fname:hover{color:#7c83fd}
.run-btn-small{padding:3px 8px;font-size:0.72rem;background:#1a3a1a;border:1px solid #4caf50;color:#4caf50;border-radius:4px;cursor:pointer}
.run-btn-small:hover{background:#2a4a2a}
.two-col{display:flex;gap:12px;flex:1;overflow:hidden}
.file-preview-box{background:#0a0a1a;border:1px solid #222244;border-radius:6px;padding:12px;flex:1;overflow-y:auto;font-family:monospace;font-size:0.78rem;white-space:pre;color:#bbb}
.input-row{display:flex;gap:8px;margin-bottom:8px;flex-shrink:0}
.input-row input{flex:1;background:#111122;border:1px solid #30305a;border-radius:6px;padding:8px 12px;color:#e0e0e0;font-size:0.83rem;outline:none}
.input-row input:focus{border-color:#7c83fd}
select{background:#111122;border:1px solid #30305a;border-radius:6px;padding:8px;color:#e0e0e0;font-size:0.88rem;width:100%}
label{font-size:0.8rem;color:#888;display:block;margin-bottom:4px;margin-top:12px}
label:first-child{margin-top:0}
.settings-panel{max-width:480px}
.spinner{display:inline-block;width:12px;height:12px;border:2px solid #555;border-top-color:#7c83fd;border-radius:50%;animation:spin 0.8s linear infinite;vertical-align:middle;margin-right:6px}
.ws-header{color:#7c83fd;font-size:0.82rem;margin-bottom:3px;cursor:pointer}
.ws-header:hover{text-decoration:underline}
.run-badge{font-size:0.7rem;padding:2px 7px;border-radius:10px;display:inline-block;margin-left:8px}
.badge-ok{background:#0a2a0a;border:1px solid #4caf50;color:#4caf50}
.badge-fail{background:#2a0a0a;border:1px solid #f44336;color:#f44336}
.badge-partial{background:#2a1a0a;border:1px solid #ff9800;color:#ff9800}
</style>
</head>
<body>

<div id="loading-overlay">
  <div class="spinner-large"></div>
  <h2>UMBRA v2.0 Starting...</h2>
  <p id="loading-msg">Initializing runtime, please wait...</p>
</div>

<header>
  <h1>&#9670; UMBRA v2.0 &mdash; Autonomous AI Runtime OS</h1>
  <div id="status-bar">
    <span class="pill" id="pill-provider">loading</span>
    <span class="pill" id="pill-model">...</span>
    <span class="pill" id="pill-ready">loading</span>
    <span class="pill yellow" id="pill-gaming" style="display:none">GAMING MODE</span>
  </div>
</header>

<div class="main">
  <div class="sidebar">
    <h3>System</h3>
    <div class="stat"><span>Provider</span><span class="stat-val" id="s-provider">-</span></div>
    <div class="stat"><span>Model</span><span class="stat-val" id="s-model">-</span></div>
    <div class="stat"><span>Runs</span><span class="stat-val" id="s-runs">0</span></div>
    <div class="stat"><span>Memory</span><span class="stat-val" id="s-memory">0</span></div>
    <div class="stat"><span>RAM</span><span class="stat-val" id="s-ram">0%</span></div>
    <div class="stat"><span>Jobs</span><span class="stat-val" id="s-jobs">-</span></div>
    <div class="gaming-badge" id="gaming-badge">&#127918; Gaming Mode<br><small>Umbra throttled</small></div>
    <h3>Actions</h3>
    <button onclick="doHealthCheck()">&#9679; Health Check</button>
    <button onclick="switchTab('metrics')">&#128200; View Metrics</button>
    <button onclick="switchTab('files')">&#128193; Browse Files</button>
    <button onclick="doValidate()">&#10003; Validate Last Run</button>
    <button onclick="doReview()">&#128269; Review Last Run</button>
    <h3>Info</h3>
    <div style="font-size:0.72rem;color:#555;line-height:1.6">
      608 tests passing<br>
      Gaming priority: ON<br>
      Auto-save: ON<br>
      v2.0.0 Autonomous
    </div>
  </div>

  <div class="content-area">
    <div class="nav-tabs">
      <div class="nav-tab active" onclick="switchTab('chat')" id="tab-chat">&#128172; Chat</div>
      <div class="nav-tab" onclick="switchTab('metrics')" id="tab-metrics">&#128200; Metrics</div>
      <div class="nav-tab" onclick="switchTab('health')" id="tab-health">&#9679; Health</div>
      <div class="nav-tab" onclick="switchTab('files')" id="tab-files">&#128193; Files</div>
      <div class="nav-tab" onclick="switchTab('memory')" id="tab-memory">&#129504; Memory</div>
      <div class="nav-tab" onclick="switchTab('settings')" id="tab-settings">&#9881; Settings</div>
    </div>

    <!-- CHAT -->
    <div class="tab-panel active" id="panel-chat">
      <div id="chat-output">
        <div class="msg system">UMBRA v2.0 ready. Type any objective below and press Enter or click Run.</div>
        <div class="msg system">Examples: "write a pygame game with player and enemy" | "build a REST API" | "write a Python data analysis script"</div>
        <div class="msg system">Files are written to workspaces/ and the Files tab shows runnable outputs you can launch.</div>
      </div>
      <div class="chat-row">
        <input id="chat-input" type="text" placeholder="Type your objective here and press Enter..." onkeydown="handleKey(event)">
        <button class="btn" id="run-btn" onclick="sendPrompt()">Run</button>
        <button class="btn btn-secondary" onclick="clearChat()">Clear</button>
      </div>
    </div>

    <!-- METRICS -->
    <div class="tab-panel" id="panel-metrics">
      <div class="metrics-grid">
        <div class="metric-card"><div class="label">Total Runs</div><div class="value" id="m-total">0</div></div>
        <div class="metric-card"><div class="label">Successful</div><div class="value" id="m-ok">0</div></div>
        <div class="metric-card"><div class="label">Success Rate</div><div class="value" id="m-rate">0%</div></div>
        <div class="metric-card"><div class="label">Files Written</div><div class="value" id="m-files">0</div></div>
        <div class="metric-card"><div class="label">Tasks Run</div><div class="value" id="m-tasks">0</div></div>
        <div class="metric-card"><div class="label">Avg Duration</div><div class="value" id="m-dur">0s</div></div>
      </div>
      <div class="scroll-list" id="history-list"><div style="color:#555">No runs yet.</div></div>
    </div>

    <!-- HEALTH -->
    <div class="tab-panel" id="panel-health">
      <div style="margin-bottom:10px;flex-shrink:0">
        <button class="btn" onclick="loadHealth()">Run Health Check</button>
      </div>
      <div class="scroll-list" id="health-list"><div style="color:#555">Click "Run Health Check" above.</div></div>
    </div>

    <!-- FILES -->
    <div class="tab-panel" id="panel-files">
      <div style="margin-bottom:10px;flex-shrink:0;display:flex;gap:8px;align-items:center">
        <button class="btn" onclick="loadWorkspaces()">Refresh</button>
        <span style="color:#666;font-size:0.78rem">Click a filename to preview. Click &#9654; to run it.</span>
      </div>
      <div class="two-col">
        <div class="scroll-list" style="width:300px;flex-shrink:0" id="ws-list">
          <div style="color:#555">Loading workspaces...</div>
        </div>
        <div class="file-preview-box" id="file-preview">Select a file to preview.</div>
      </div>
    </div>

    <!-- MEMORY -->
    <div class="tab-panel" id="panel-memory">
      <div class="input-row" style="flex-shrink:0">
        <input id="mem-search" type="text" placeholder="Search memory..." onkeydown="if(event.key==='Enter')searchMem()">
        <button class="btn" onclick="searchMem()">Search</button>
        <button class="btn btn-secondary" onclick="loadMemory()">All</button>
      </div>
      <div class="input-row" style="flex-shrink:0">
        <input id="mem-key" type="text" placeholder="Key (optional)">
        <input id="mem-val" type="text" placeholder="Store a note or fact..." onkeydown="if(event.key==='Enter')storeMem()">
        <button class="btn" onclick="storeMem()">Store</button>
      </div>
      <div class="scroll-list" id="memory-list"><div style="color:#555">Loading...</div></div>
    </div>

    <!-- SETTINGS -->
    <div class="tab-panel" id="panel-settings">
      <div class="settings-panel">
        <label>LLM Provider</label>
        <select id="cfg-provider">
          <option value="ollama">Ollama (local, free, unlimited)</option>
          <option value="groq">Groq (free cloud)</option>
          <option value="openai">OpenAI</option>
          <option value="anthropic">Anthropic</option>
        </select>
        <label>Model</label>
        <select id="cfg-model"><option value="qwen2.5-coder:14b">qwen2.5-coder:14b</option></select>
        <label>API Key (for Groq/OpenAI/Anthropic)</label>
        <input style="width:100%;background:#111122;border:1px solid #30305a;border-radius:6px;padding:8px;color:#e0e0e0;font-size:0.88rem;outline:none" type="password" id="cfg-key" placeholder="sk-... or gsk_...">
        <div style="margin-top:14px;display:flex;gap:8px;align-items:center">
          <button class="btn" onclick="saveConfig()">Save Config</button>
          <span id="cfg-msg" style="font-size:0.8rem;color:#4caf50"></span>
        </div>
        <label style="margin-top:20px">Available Ollama Models</label>
        <div id="ollama-models" style="color:#666;font-size:0.8rem">Checking...</div>
        <div id="cfg-raw" style="margin-top:16px;background:#0a0a1a;border:1px solid #222;border-radius:6px;padding:10px;font-family:monospace;font-size:0.72rem;color:#888;max-height:180px;overflow-y:auto;white-space:pre"></div>
      </div>
    </div>
  </div>
</div>

<script>
var _ready = false;
var _checkInterval = null;

// Poll until runtime is ready
function checkReady() {
  fetch('/api/ready').then(r => r.json()).then(d => {
    if (d.ready) {
      _ready = true;
      document.getElementById('loading-overlay').style.display = 'none';
      clearInterval(_checkInterval);
      loadStatus();
      loadWorkspaces();
    } else if (d.error) {
      document.getElementById('loading-msg').textContent = 'Error: ' + d.error;
      document.getElementById('loading-msg').style.color = '#f44336';
    } else {
      document.getElementById('loading-msg').textContent = 'Loading Umbra runtime... this takes about 3-5 seconds.';
    }
  }).catch(() => {
    document.getElementById('loading-msg').textContent = 'Connecting to server...';
  });
}
_checkInterval = setInterval(checkReady, 800);
checkReady();

function api(path, method, body) {
  var opts = {method: method || 'GET', headers: {'Content-Type': 'application/json'}};
  if (body) opts.body = JSON.stringify(body);
  return fetch(path, opts).then(r => r.json()).catch(e => ({error: String(e)}));
}

function switchTab(name) {
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  document.getElementById('panel-' + name).classList.add('active');
  if (name === 'metrics') loadMetrics();
  if (name === 'health') loadHealth();
  if (name === 'files') loadWorkspaces();
  if (name === 'memory') loadMemory();
  if (name === 'settings') loadSettings();
}

function addMsg(text, cls) {
  var out = document.getElementById('chat-output');
  var d = document.createElement('div');
  d.className = 'msg ' + (cls || 'umbra');
  d.textContent = text;
  out.appendChild(d);
  out.scrollTop = out.scrollHeight;
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendPrompt();
  }
}

function sendPrompt() {
  if (!_ready) { addMsg('Umbra is still loading, please wait...', 'system'); return; }
  var input = document.getElementById('chat-input');
  var prompt = input.value.trim();
  if (!prompt) return;
  input.value = '';
  addMsg(prompt, 'user');
  var btn = document.getElementById('run-btn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Running';
  addMsg('Processing: ' + prompt.substring(0, 80) + '...', 'system');

  api('/api/chat', 'POST', {message: prompt}).then(function(d) {
    btn.disabled = false;
    btn.textContent = 'Run';
    if (d.error) {
      addMsg('ERROR: ' + d.error, 'error');
      return;
    }
    var status_class = d.status === 'completed' ? 'success' : 'umbra';
    addMsg('Done! Status: ' + d.status + ' | Run: ' + d.run_id + ' | Tasks: ' + d.tasks, status_class);
    if (d.files_written > 0) {
      addMsg('Files written (' + d.files_written + '):', 'umbra');
      d.files// Handle chat API response
    if (d.response) {
      addMsg(d.response, d.intent === 'question' || d.intent === 'chat' ? 'umbra' : 'success');
    }
    if (d.clarification_question) {
      addMsg('Umbra needs clarification: ' + d.clarification_question, 'system');
    }
    if (d.run_result) {
      var rr = d.run_result;
      if (rr.files && rr.files.length > 0) {
        addMsg('Files written (' + rr.files.length + '):', 'umbra');
        rr.files.forEach(function(f) {
          addMsg('  -> ' + f.file + ' (' + f.lines + ' lines)', 'file');
        });
      }
      if (rr.assembled) {
        addMsg('Ready to run: ' + rr.assembled, 'success');
        addMsg('Go to Files tab and click Play.', 'system');
      }
    }
    if (d.image_result && d.image_result.success) {
      addMsg('Image saved: ' + d.image_result.file_path, 'success');
    }.forEach(function(f) {
        addMsg('  -> ' + f.file + ' (' + f.lines + ' lines)', 'file');
      });
    }
    if (d.assembled_file) {
      addMsg('Assembled runnable file: ' + d.assembled_file, 'success');
      addMsg('Go to Files tab to preview and launch it.', 'system');
    }
    if (d.failed_tasks && d.failed_tasks.length > 0) {
      addMsg('Failed tasks: ' + d.failed_tasks.join(', '), 'error');
    }
    loadStatus();
    loadWorkspaces();
  });
}

function clearChat() {
  document.getElementById('chat-output').innerHTML =
    '<div class="msg system">Chat cleared. Ready for new objective.</div>';
}

function loadStatus() {
  api('/api/status').then(function(d) {
    if (!d.provider) return;
    document.getElementById('s-provider').textContent = d.provider + (d.free ? ' (FREE)' : '');
    document.getElementById('s-model').textContent = d.model;
    document.getElementById('s-runs').textContent = d.runs_this_session;
    document.getElementById('s-memory').textContent = d.memory_entries + ' entries';
    document.getElementById('s-ram').textContent = d.memory_pct + '%';
    document.getElementById('s-jobs').textContent = d.scheduler_jobs + ' jobs';
    document.getElementById('pill-provider').textContent = d.provider || 'loading';
    document.getElementById('pill-model').textContent = d.model || '...';
    var rp = document.getElementById('pill-ready');
    rp.textContent = d.ready ? 'READY' : 'NOT READY';
    rp.className = 'pill ' + (d.ready ? 'green' : 'red');
    var pg = document.getElementById('pill-gaming');
    var gb = document.getElementById('gaming-badge');
    if (d.gaming_detected) {
      pg.style.display = 'inline-block';
      gb.style.display = 'block';
    } else {
      pg.style.display = 'none';
      gb.style.display = 'none';
    }
  });
}

function loadMetrics() {
  api('/api/metrics').then(function(m) {
    document.getElementById('m-total').textContent = m.total_runs || 0;
    document.getElementById('m-ok').textContent = m.successful_runs || 0;
    document.getElementById('m-rate').textContent = (m.success_rate_pct || 0) + '%';
    document.getElementById('m-files').textContent = m.total_files_written || 0;
    document.getElementById('m-tasks').textContent = m.total_tasks_executed || 0;
    document.getElementById('m-dur').textContent = (m.avg_duration_seconds || 0) + 's';
  });
  api('/api/history').then(function(h) {
    var list = document.getElementById('history-list');
    if (!h.runs || !h.runs.length) {
      list.innerHTML = '<div style="color:#555;padding:8px">No runs yet. Type an objective in the Chat tab.</div>';
      return;
    }
    list.innerHTML = h.runs.slice().reverse().map(function(r) {
      var badge = r.status === 'completed' ? 'badge-ok' :
                  r.status === 'completed_with_failures' ? 'badge-partial' : 'badge-fail';
      var files = (r.written_files || []).length;
      return '<div class="list-item"><span style="color:#7c83fd">' + r.run_id + '</span>' +
             '<span class="run-badge ' + badge + '">' + r.status + '</span>' +
             '<span style="color:#555;margin-left:8px">' + files + ' files</span>' +
             '<div style="color:#666;font-size:0.75rem;margin-top:2px">' +
             (r.prompt || '').substring(0, 70) + '</div></div>';
    }).join('');
  });
}

function doHealthCheck() {
  switchTab('health');
  loadHealth();
}

function loadHealth() {
  var list = document.getElementById('health-list');
  list.innerHTML = '<div style="color:#666"><span class="spinner"></span>Running health check...</div>';
  api('/api/health').then(function(d) {
    if (!d.checks) {
      list.innerHTML = '<div style="color:#f44336">Failed to get health data.</div>';
      return;
    }
    var color = d.overall_status === 'healthy' ? '#4caf50' :
                d.overall_status === 'degraded' ? '#ff9800' : '#f44336';
    var html = '<div style="margin-bottom:12px;color:' + color + ';font-weight:bold;font-size:0.9rem">' +
               'Overall: ' + d.overall_status.toUpperCase() +
               ' | Pass: ' + d.pass_count + ' Warn: ' + d.warn_count + ' Fail: ' + d.fail_count + '</div>';
    html += d.checks.map(function(c) {
      var dc = c.status === 'pass' ? 'dot-pass' : c.status === 'warn' ? 'dot-warn' : 'dot-fail';
      return '<div class="list-item" style="display:flex;align-items:center">' +
             '<span class="health-dot ' + dc + '"></span>' +
             '<span style="flex:1;color:#bbb">' + c.name + '</span>' +
             '<span style="color:#666;font-size:0.75rem">' + (c.message || c.status) + '</span></div>';
    }).join('');
    list.innerHTML = html;
  });
}

function loadWorkspaces() {
  var list = document.getElementById('ws-list');
  list.innerHTML = '<div style="color:#555"><span class="spinner"></span>Loading...</div>';
  api('/api/workspaces').then(function(d) {
    if (!d.workspaces || !d.workspaces.length) {
      list.innerHTML = '<div style="color:#555;padding:8px">No workspaces yet. Run a task first.</div>';
      return;
    }
    list.innerHTML = d.workspaces.map(function(ws) {
      var runnable = ws.runnable ? '<span class="run-btn-small" onclick="launchFile(\'' +
        ws.runnable.replace(/\\/g,'\\\\') + '\')">&#9654; Run</span>' : '';
      var files = ws.files.map(function(f) {
        return '<div class="file-row"><span class="fname" onclick="previewFile(\'' +
          f.path.replace(/\\/g, '\\\\') + '\')">' + f.name + ' <span style="color:#555">(' + f.lines + 'L)</span>' +
          '</span>' + (f.name.endsWith('.py') ?
          '<span class="run-btn-small" onclick="launchFile(\'' + f.path.replace(/\\/g,'\\\\') + '\')">&#9654;</span>' : '') +
          '</div>';
      }).join('');
      return '<div style="margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #1a1a2a">' +
             '<div class="ws-header" onclick="toggleWs(this)">' + ws.run_id +
             ' <span style="color:#555;font-size:0.72rem">(' + ws.file_count + ' files)</span>' +
             runnable + '</div>' +
             '<div class="ws-files" style="display:none;padding-left:8px;margin-top:4px">' + files + '</div></div>';
    }).join('');
  });
}

function toggleWs(el) {
  var files = el.nextElementSibling;
  files.style.display = files.style.display === 'none' ? 'block' : 'none';
}

function previewFile(path) {
  api('/api/file?path=' + encodeURIComponent(path)).then(function(d) {
    var box = document.getElementById('file-preview');
    box.textContent = d.error ? 'Error: ' + d.error : d.content;
  });
}

function launchFile(path) {
  api('/api/run_file', 'POST', {path: path}).then(function(d) {
    if (d.error) {
      addMsg('Launch error: ' + d.error, 'error');
    } else {
      addMsg('Launched: ' + path, 'success');
    }
  });
}

function loadMemory() {
  api('/api/memory').then(function(d) {
    var list = document.getElementById('memory-list');
    if (!d.keys || !d.keys.length) {
      list.innerHTML = '<div style="color:#555">No memory entries yet.</div>';
      return;
    }
    list.innerHTML = d.keys.map(function(k) {
      return '<div class="list-item"><span style="color:#7c83fd;margin-right:8px">' + k + '</span></div>';
    }).join('');
  });
}

function searchMem() {
  var q = document.getElementById('mem-search').value.trim();
  if (!q) return;
  api('/api/memory/search', 'POST', {query: q}).then(function(d) {
    var list = document.getElementById('memory-list');
    if (!d.results || !d.results.length) {
      list.innerHTML = '<div style="color:#555">Nothing found for "' + q + '"</div>';
      return;
    }
    list.innerHTML = d.results.map(function(r) {
      return '<div class="list-item"><span style="color:#7c83fd;margin-right:8px">' + r.key + '</span>' +
             '<span style="color:#888">' + String(r.value).substring(0, 120) + '</span></div>';
    }).join('');
  });
}

function storeMem() {
  var key = document.getElementById('mem-key').value.trim() || null;
  var val = document.getElementById('mem-val').value.trim();
  if (!val) return;
  api('/api/memory/store', 'POST', {key: key, value: val, tags: ['user_note']}).then(function() {
    document.getElementById('mem-key').value = '';
    document.getElementById('mem-val').value = '';
    loadMemory();
  });
}

function doValidate() {
  api('/api/validate_last', 'POST').then(function(d) {
    if (d.error) { addMsg('Validate: ' + d.error, 'system'); return; }
    addMsg('Validation score: ' + d.score + '/100 | Passed: ' + d.passed, d.passed ? 'success' : 'error');
    if (d.issues && d.issues.length) {
      d.issues.slice(0, 3).forEach(function(i) { addMsg('  ! ' + i, 'system'); });
    }
    switchTab('chat');
  });
}

function doReview() {
  api('/api/review_last', 'POST').then(function(d) {
    if (d.error) { addMsg('Review: ' + d.error, 'system'); return; }
    addMsg('Code review: ' + d.file_count + ' files | Avg score: ' + d.average_score + '/100', 'success');
    switchTab('chat');
  });
}

function loadSettings() {
  api('/api/config').then(function(d) {
    if (d.llm_provider) document.getElementById('cfg-provider').value = d.llm_provider;
    document.getElementById('cfg-raw').textContent = JSON.stringify(d, null, 2);
  });
  api('/api/ollama/models').then(function(d) {
    var sel = document.getElementById('cfg-model');
    if (d.available && d.models.length) {
      sel.innerHTML = d.models.map(function(m) {
        return '<option value="' + m + '">' + m + '</option>';
      }).join('');
      document.getElementById('ollama-models').textContent = d.models.join(', ');
    } else {
      document.getElementById('ollama-models').textContent = 'Ollama not reachable';
    }
  });
}

function saveConfig() {
  var cfg = {
    llm_provider: document.getElementById('cfg-provider').value,
    llm_model: document.getElementById('cfg-model').value,
  };
  var key = document.getElementById('cfg-key').value.trim();
  if (key) cfg.llm_api_key = key;
  api('/api/config', 'POST', cfg).then(function(d) {
    var msg = document.getElementById('cfg-msg');
    msg.textContent = d.saved ? 'Saved!' : 'Error saving';
    msg.style.color = d.saved ? '#4caf50' : '#f44336';
    setTimeout(function() { msg.textContent = ''; }, 2000);
    loadSettings();
  });
}

// Auto-refresh status every 20 seconds
setInterval(function() { if (_ready) loadStatus(); }, 20000);
</script>
</body>
</html>"""
    with open(os.path.join(static_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    import webbrowser
    print("\n" + "="*60)
    print("  UMBRA GUI Server v2.0")
    print("  http://localhost:7860")
    print("  Ctrl+C to stop")
    print("="*60 + "\n")
    create_static_files()
    threading.Thread(target=lambda: (time.sleep(2), webbrowser.open("http://localhost:7860")), daemon=True).start()
    app.run(host="0.0.0.0", port=7860, debug=False, threaded=True)