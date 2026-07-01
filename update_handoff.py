NEW_HANDOFF = """# UMBRA HANDOFF v3.1.0 — Paste at start of every new chat

## HOW TO START
1. Pull repo: `cd C:\\Umbra && git pull origin main`
2. Read this file
3. Continue from CURRENT PRIORITY
4. Send patch scripts only — no explanations

---

## REPO
- GitHub: https://github.com/UmbraOx/UmbraOX (PUBLIC)
- Main: `C:\\Umbra\\Umbra.py` (~4500+ lines, v3.1.0)
- GUI: `C:\\Umbra\\core\\gui\\control_center.py`
- Game skeleton: `C:\\Umbra\\core\\assets\\game_skeleton.py`
- Dev assistant: `C:\\Umbra\\umbra_dev_assistant.py`
- Tests: `test_umbra_full.py` (67) + `test_dev_assistant.py` (39)
- Crash test: `test_gameplay_crash.py` (headless, run directly not via pytest)

## SYSTEM
- Windows 11, AMD Ryzen 9 3900XT, RX 7900 XT 20GB GPU, 64GB RAM
- Python 3.12 venv: `C:\\Umbra\\venv\\` — activate: `venv\\Scripts\\activate`
- Python 3.10 also installed — games launch with 3.10 (pygame installed there)
- Ollama running: qwen3:14b (chat), qwen2.5-coder:32b (builds), 15 total models
- ComfyUI: `C:\\Umbra\\run_directml.bat` — must be running for images/GIFs
  - WARNING: ComfyUI reports only 1GB VRAM on DirectML despite RX 7900 XT having 20GB
  - This is a DirectML bug — causes OOM on heavy workloads like AnimateDiff
- ComfyUI-Manager: installed (V3.41)
- AnimateDiff-Evolved: installed (v1.5.7, 146 nodes)
- Motion module: `C:\\ComfyUI\\models\\animatediff_models\\mm_sd_v15_v2.ckpt`
- Checkpoints: dreamshaper_8.safetensors, realisticVisionV60B1, v1-5-pruned-emaonly.ckpt

## PATCH WORKFLOW
Claude sends apply_fixes_N.py + push_batchN.py — you run them:
```powershell
cd C:\\Umbra
venv\\Scripts\\activate
python apply_fixes_N.py
python push_batchN.py
python Umbra.py   # to test
```
Always use numbered patches. Push after every batch. Backup baks are auto-created.

## REPLY RULES — NEVER BREAK
- **COMPRESSED REPLIES ONLY — patch scripts and results, zero prose explanations**
- No narration, no "I will now...", no "This fix addresses..."
- Full drop-in patch scripts only. Never snippets or descriptions of changes.
- Fix support/core files before Umbra.py
- Push every batch to git
- Run tests before shipping: `python -m pytest -q` then `python test_umbra_full.py`
- Never send heredocs — PowerShell encoding breaks them. Send .py files only.
- When stuck on exact source text, send a dump_lines.py script first, then fix.

---

## CURRENT STATUS v3.1.0

### FULLY WORKING
- Boot: `python Umbra.py` launches clean, GUI opens, status correct
- ComfyUI auto-launches at boot via `run_directml.bat` (C:\\ComfyUI)
- **Real image generation via ComfyUI** — dreamshaper_8 default, 30 steps
- **Real animated GIF via AnimateDiff-Evolved** — 8 frames, 384x384, mm_sd_v15_v2
- Image command routing: robust regex catches all phrasings ("make a image", "draw art", etc)
- Memory: `remember X` stores to sessions/memory_store.json, `memory` recalls all
- 67/67 + 39/39 tests passing, full pytest suite clean (zero failures)
- Game builds: 7-agent pipeline, games launch headlessly (2/2 crash test passing)
- ComfyUI-Manager installed, AnimateDiff-Evolved installed
- Voice/TTS boots (pyttsx3 + SpeechRecognition auto-installed)
- `fix yourself` / `fix all bugs` properly guarded
- _ollama_stream: real retry loop with backoff (3x, delays 5/15/30s)
- Version: v3.1.0

### KNOWN ISSUES (CURRENT PRIORITY)

#### 🔴 HIGH
1. **AnimateDiff OOM on second run** — DirectML reports 1GB VRAM despite 20GB card.
   Fix in progress: apply_fixes_21.py was being written (8 frames, 384x384, 16 steps,
   reduced context_overlap). Still needs to be sent and tested.
   Root issue: DirectML VRAM detection bug — not fixable in code, but settings can help.

2. **GIF generation blocks Umbra** — AnimateDiff runs synchronously (9+ minutes on DirectML).
   Any command typed during GIF generation queues but Ollama also starved of GPU.
   Fix needed: run gif/image generation in background thread so GUI/chat stays responsive.

3. **Image distortion / missing limbs** — SD1.5-based models struggle with anatomy.
   Partial fix: switched to dreamshaper_8 + stronger negative prompts.
   Still needs: higher CFG, better anatomy-specific negative prompt additions,
   possibly switch to SDXL checkpoint (would need new download).

#### 🟡 MEDIUM
4. **GIF quality** — AnimateDiff produced a real animated dragon (not stick figures!) but
   quality is limited by DirectML speed/VRAM constraints. 8 frames at 384x384 is the
   working sweet spot — do not increase without confirming VRAM budget.

5. **`build X` game name extraction** — "build optiopia" sometimes names game "MyGame".
   Project name parsing from build command needs robustness check.

6. **PyAudio missing** — `Error initializing microphone listener: Could not find PyAudio`
   Fix: `C:\\Umbra\\venv\\Scripts\\pip install pyaudio` (may need Visual C++ build tools)

7. **OpenCV not available** — `OpenCV is not available` prints at boot.
   Non-critical but noisy. Install if video pipeline needed: `pip install opencv-python`

#### 🟢 LOW / POLISH
8. Accumulated .bak_* files in repo — clean up periodically
9. test_umbra_full.py / test_dev_assistant.py generate PytestReturnNotNoneWarnings
   (tests return bool instead of None/assert) — cosmetic, all pass
10. `datetime.utcnow()` deprecation warning in runtime_self_improvement_loop.py
11. DirectML "barely works" warning at ComfyUI startup — informational only
12. UMBRA_HANDOFF.md needs updating after next session (always update at session end)

---

## ARCHITECTURE (do not change)
```
Umbra.py → build_runtime() → interactive_mode() → _launch_gui() → mainloop()
_process_command() routes all input
  → image regex → RuntimeImageGenerator → ComfyUI HTTP API
  → gif regex → RuntimeAnimatedGifGenerator → ComfyUI AnimateDiff-Evolved
  → build/game → _run_deep_build() → 7-agent pipeline → _stitch_game()
  → remember/recall → RuntimeMemoryStore → sessions/memory_store.json
  → fix yourself → handle_self_fix()
  → dev assistant → umbra_dev_assistant.process() (hooks in _process_command)
RuntimeLauncher auto-starts ComfyUI at boot (run_directml.bat)
```

## KEY FILES & LINE REFS
| What | File | Approx line |
|---|---|---|
| Command router | Umbra.py | ~3570 |
| Image command match | Umbra.py | ~3573 (regex now) |
| GIF generation call | Umbra.py | ~3540 |
| Ollama stream | Umbra.py | 687 |
| Game stitch | Umbra.py | ~957 |
| ComfyUI launcher | core/runtime/runtime_launcher.py | full file |
| Image generator | core/runtime/runtime_image_generator.py | full file |
| GIF generator | core/runtime/runtime_animated_gif_generator.py | full file |
| Memory store | core/runtime/runtime_memory_store.py | full file |
| Game skeleton | core/assets/game_skeleton.py | full file |

## WHAT STILL NEEDS DOING FOR 100%
Priority order:
1. Send + test apply_fixes_21.py (AnimateDiff OOM params + image quality)
2. Background-thread GIF/image generation (non-blocking Umbra during generation)
3. Fix PyAudio install for real voice input
4. Game name extraction fix ("build optiopia" → game named Optiopia)
5. Image anatomy quality (higher steps, better negatives, or SDXL switch)
6. Full live test: image, gif, game build, game play, memory, self-fix — all in one session
7. Update UMBRA_HANDOFF.md after every session

## COMPLETION
- Boot + GUI + ComfyUI auto-launch: 100%
- Image generation (real SD): 85% (quality issues remain)
- GIF generation (real AnimateDiff): 75% (OOM on 2nd run, blocks Umbra)
- Memory system: 100%
- Game build pipeline: 82%
- Voice/TTS: 70% (boots, PyAudio missing for mic)
- Tests: 100% (67+39 passing, pytest clean)
- Self-repair: 60%
- **Overall: ~88%**
"""

with open("UMBRA_HANDOFF.md", "w", encoding="utf-8") as f:
    f.write(NEW_HANDOFF)
print("UMBRA_HANDOFF.md updated")