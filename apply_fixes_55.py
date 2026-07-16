import datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\UMBRA_HANDOFF.md"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak55_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD_START = "## CURRENT STATUS v3.1.0"
OLD_END = "## COMPLETION"

start_idx = src.find(OLD_START)
end_idx = src.find(OLD_END)
if start_idx == -1 or end_idx == -1:
    print("FAIL: could not locate status section boundaries")
    sys.exit(1)

# find the end of the COMPLETION section (end of file, or next ## heading)
tail_from_completion = src[end_idx:]
next_heading = tail_from_completion.find("\n## ", 4)
if next_heading == -1:
    completion_end = len(src)
else:
    completion_end = end_idx + next_heading

NEW_SECTION = '''## CURRENT STATUS v3.1.0 (updated after batch 54)

### TESTING PLAN
Per explicit direction: test and confirm everything EXCEPT the game
builder first (games are deferred to last, see GAME PORTION below).
Test in this order:
1. Boot: `python Umbra.py` - clean start, correct STATUS block, no
   unexpected errors in the console
2. Image generation: `make an image of <description>` - background
   thread, doesn't block GUI, reasonable quality
3. GIF generation: `make a gif of <description>` - background thread,
   no neon/flicker artifacts, doesn't block GUI
4. Voice: `listen`, `voice on`/`voice off`, `tts on`/`tts off` - all via
   the GUI (not just CLI)
5. Gaming mode: `gaming mode on` while running something GPU/CPU heavy,
   confirm Umbra actually throttles (lower priority, task delays); then
   `gaming mode off` / `gaming mode auto` to confirm it releases
6. Memory: `remember <fact>`, `recall <query>`, `memory`
7. Self-repair / diagnostics: `fix all bugs`, `status`, `health`, `test`
8. File browser: `list files`, `list workspace files`, `clean up old files`
9. Projects: `projects`, `work on <name>`
10. Generic (non-game) build pipeline: something like "write me a
    <script/tool>" that goes through the step-planner, not the game
    builder - confirm it still works and isn't accidentally caught by
    the broadened verb+noun game-detection from batch41

### FULLY WORKING (as of batch 54)
- Boot: `python Umbra.py` launches clean, GUI opens, status correct
- ComfyUI auto-launches at boot via `run_directml.bat`
- Real image generation via ComfyUI (dreamshaper_8, dpmpp_2m, 36 steps,
  professional-grade negative prompts incl. face/eyes/teeth)
- Real animated GIF via AnimateDiff-Evolved (8 frames, 384x384, 20 steps,
  cfg 7.0, neon/flicker negatives) - gif/image generation run in a
  background thread, GUI stays responsive during generation
- Voice: PyAudio auto-installs (pipwin fallback); `listen`/`voice on`/
  `tts on` all wired into the GUI command path
- Gaming mode: detection broadened beyond a fixed game-name whitelist to
  cover platform launchers (Steam/Epic/Battle.net/GOG/Ubisoft Connect),
  plus a manual override - `gaming mode on` / `gaming mode off` /
  `gaming mode auto` - since name-based detection can never be complete.
  NOT YET LIVE-TESTED that throttling actually reduces lag - next test.
- `play last` / `play <name>` refuses to launch a build that already
  failed its smoke test, unless explicitly told `play last anyway`
- .gitignore matches our actual backup/build-artifact naming; repo
  cleaned of orphaned scripts
- Memory: `remember X` / `memory` working
- README.md and this handoff reflect current architecture and conventions
- Version: v3.1.0

### GAME PORTION - DEFERRED TO LAST (per explicit direction)
Extensive contract-safety work has been done (see git log batches 22-54:
draw_main_menu, UI contract functions, stray top-level code, adaptive
signature calling, Player/Enemy/NPC construction safety, generic
update()/draw() fallback for every entity, WORLD_MAP wrapped in a
universal safe-grid proxy regardless of shape, check_quest_kill call
sites wrapped, automated headless smoke test before every "BUILD
COMPLETE"). This is NOT considered finished or fully verified - the
user has hit a new distinct bug on nearly every test cycle, most
recently NPC construction (batch54). Do not resume game-builder testing
until explicitly directed to.

**Open architectural question, not yet started:** the 7 agents (world,
character, item, mechanic, ui, quest, economy) generate independently
with no visibility into each other's output, which is the root cause of
the whole "mismatched contract" bug class. User has proposed an 8th
"integration/reviewer" pipeline stage that runs after all 7 agents
finish and before stitching - reads all 7 components together, detects
cross-file incompatibilities, and either fixes them or sends targeted
correction back to the responsible agent. This is agreed as the right
direction but is unbuilt - real design + implementation work, not a
quick patch. Pick this up when game-portion work resumes.

### KNOWN ISSUES

1. GIF pipeline general quality - still rough (motion/detail limited by
   DirectML speed/VRAM ceiling at 384x384/8 frames). Deferred/backlog.
2. OpenCV not available warning at boot - cosmetic only.
3. UI agent output size has ballooned as large as 3159 lines in one
   build (vs ~100 for other agents) - slows builds, more bug surface.
   No prompt/scope constraint added yet. Game-portion item, deferred.
4. Gaming mode fix (batch54) is untested live - confirm on next session.

### NOT YET BUILT - FUTURE SCOPE (confirm/prioritize with user)
- Full large-scale game generation (Skyrim/Fable/Runescape scale):
  persistent world state, save systems, streaming/larger maps, NPC
  schedules and personalities, live economy simulation ("world brain")
- Music generation
- Video generation - `make a video of X` / `assemble video frames` appear
  in the help text but have not been exercised/verified; status unknown
- 3D asset generation
- AI companion/girlfriend feature
- General-purpose multi-AI-agent helper framework (beyond game building)
- General application building (beyond games)

## ARCHITECTURE (do not change)
```
Umbra.py -> build_runtime() -> interactive_mode() -> _launch_gui() -> mainloop()
_process_command() routes all input
  -> image regex -> RuntimeImageGenerator -> ComfyUI HTTP API (threaded)
  -> gif regex -> RuntimeAnimatedGifGenerator -> ComfyUI AnimateDiff-Evolved (threaded)
  -> listen/voice/tts -> RuntimeVoiceInput (handled directly in _process_command)
  -> gaming mode on/off/auto -> RuntimeResourceManager.set_manual_gaming_mode()
  -> build/game (verb+noun match) -> _run_deep_build() -> 7-agent pipeline -> _stitch_game()
       -> strip_imports() strips agent overrides of contract fn/class names
       -> _run_smoke_test() headless subprocess validation before BUILD COMPLETE
       -> smoke_status.json tracks pass/fail per build path for play-last gating
  -> remember/recall -> RuntimeMemoryStore -> sessions/memory_store.json
  -> fix yourself -> handle_self_fix()
RuntimeLauncher auto-starts ComfyUI at boot (run_directml.bat)
RuntimeResourceManager auto-starts at boot, monitors gaming/memory every 30s
```

## KEY FILES & LINE REFS (approximate, drifts each batch - grep to confirm)
| What | File | Approx line |
|---|---|---|
| Command router | Umbra.py | ~3570 |
| Game detection (verb+noun) | Umbra.py | ~3783 |
| GIF/image generation (threaded) | Umbra.py | ~3543 |
| Gaming mode commands | Umbra.py | ~3510 |
| Ollama stream (wall-clock timeout) | Umbra.py | ~692 |
| Syntax repair call | Umbra.py | ~886 |
| _run_smoke_test + harness | Umbra.py | ~1451 |
| Game stitch (strip_imports, method-safety patch) | Umbra.py | ~1001, ~1700 |
| UMBRA_PLAYER_PATCH / UMBRA_NPC_PATCH / UMBRA_ENEMY_PATCH | Umbra.py | ~1620-1780 |
| Resource manager (gaming detection) | core/runtime/runtime_resource_manager.py | full file |
| ComfyUI launcher | core/runtime/runtime_launcher.py | full file |
| Image generator | core/runtime/runtime_image_generator.py | full file |
| GIF generator | core/runtime/runtime_animated_gif_generator.py | full file |
| Game skeleton (_umbra_flex, contract fallbacks, WORLD_MAP proxy) | core/assets/game_skeleton.py | full file |

## WHAT STILL NEEDS DOING
Priority order:
1. Run the TESTING PLAN above (non-game features) and confirm/report
2. Once non-game testing is confirmed clean, resume game-portion work:
   design + build the integration/reviewer agent (8th pipeline stage)
3. Constrain UI agent output size/scope
4. Verify `make a video of X` / `assemble video frames` actually work
5. Update UMBRA_HANDOFF.md every session without fail

## COMPLETION
- Boot + GUI + ComfyUI auto-launch: 100%
- Image generation (real SD): 95%
- GIF generation (real AnimateDiff): 85%
- Voice/TTS: 95%
- Gaming mode: fix applied, live-test pending
- Memory system: 100%
- Game build pipeline: contract-safety extensive but NOT considered
  finished - new distinct bugs still surfacing each test cycle; true
  fix (integration agent) not yet started
- Self-repair: 60%
- Large-scale game generation / world brain / economy / music / video /
  3D / AI companion / general app building: 0% (not started)
- **Overall on non-game core features: ~90%, pending live confirmation**
- **Overall on game builder: contract-safety layer extensive, but
  integration-level correctness still unresolved**
'''

new_src = src[:start_idx] + NEW_SECTION + src[completion_end:]

with open(FP, "w", encoding="utf-8") as f:
    f.write(new_src)

print("UMBRA_HANDOFF.md updated - reflects batches 45-54, restructured around non-game testing plan")