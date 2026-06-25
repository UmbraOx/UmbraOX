"""
UMBRA TEST COMMANDS — Run after every update to verify Umbra works
Run: python test_umbra_full.py  first (must be 67/67)
Then: python Umbra.py  and run these in the GUI console tab
"""

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 1 — SYSTEM HEALTH (run first, takes ~5 seconds)
# ════════════════════════════════════════════════════════════════

# Command: status
# Expected output:
#   Provider : Ollama (local, FREE)
#   Model    : qwen2.5-coder:32b
#   Ready    : YES — 10 model(s) available
#   Memory   : N entries
#   Images   : ComfyUI not running  (or "connected" if running)
#   GIF      : ready

# Command: fix all bugs
# Expected output:
#   [SELF-FIX] Scanning core/runtime...
#   [SELF-FIX] All modules clean.
#   (OR lists broken files and attempts fixes)

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 2 — QUESTION ANSWERING (must NOT become a task)
# ════════════════════════════════════════════════════════════════

# Command: what is the capital of Ohio?
# Expected: [UMBRA] Columbus is the capital of Ohio.
# FAIL if: [PLAN] Breaking task into steps...

# Command: who invented pygame?
# Expected: [UMBRA] Pygame was created by Pete Shinners...
# FAIL if: [BUILD] Written:

# Command: how do I make a potion in Skyrim?
# Expected: [UMBRA] In Skyrim, potions are made at an Alchemy Lab...
# FAIL if: [PLAN] or [BUILD]

# Command: whats 2 plus 2
# Expected: [UMBRA] 2 + 2 = 4
# FAIL if: pipeline triggered

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 3 — IMAGE GENERATION
# ════════════════════════════════════════════════════════════════

# Command: make an image of a dark fantasy castle
# Expected:
#   [UMBRA] Generating 1 image(s)...
#   [IMAGE 1] C:\Umbra\workspaces\images\image_placeholder_XXXXXXXX.png
# Then: check C:\Umbra\workspaces\images\ — file must exist
# Check preview tab auto-shows the image

# Command: make 3 images of cats in armor
# Expected:
#   [UMBRA] Generating 3 image(s)...
#   [IMAGE 1] C:\Umbra\workspaces\images\image_placeholder_...png
#   [IMAGE 2] C:\Umbra\workspaces\images\image_placeholder_...png
#   [IMAGE 3] C:\Umbra\workspaces\images\image_placeholder_...png
# FAIL if: only 1 image or no images

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 4 — GIF GENERATION
# ════════════════════════════════════════════════════════════════

# Command: make a gif of fire
# Expected:
#   [GIF] Saved: C:\Umbra\workspaces\videos\gif_fire_XXXXXXXX.gif
# FAIL if: "Not available" or no file created

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 5 — GAME BUILD (takes 20-40 minutes with 32b model)
# ════════════════════════════════════════════════════════════════

# Command: make a game called TestRPG with 1 town and 1 enemy
# Expected:
#   [UMBRA] Building game: TestRPG — launching agents...
#   [WORLD AGENT] ✓
#   [CHARACTER AGENT] ✓
#   [ITEM AGENT] ✓
#   [MECHANIC AGENT] ✓
#   [UI AGENT] ✓
#   [QUEST AGENT] ✓
#   [ECONOMY AGENT] ✓
#   [TEST] All 16 requirements passed!
#   [UMBRA] BUILD COMPLETE
#   Game: C:\Umbra\workspaces\agent_builds\testprg\testprg_game.py
# FAIL if: < 14/16 requirements passed

# Command: play last
# Expected: pygame window opens
# Window should show:
#   - Coloured biome tiles (grass=green, mountain=grey, water=blue)
#   - Player character (head circle + body + arms + legs — NOT a square)
#   - HP/MP bars at bottom
#   - Minimap in top-right
#   - WASD moves player
#   - ESC opens pause menu with X button
#   - I opens inventory with X button
# FAIL if: black screen, crash, or squares only

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 6 — SELF-INSTALL (approval dialog must appear in GUI)
# ════════════════════════════════════════════════════════════════

# Command: install image pipeline into umbra
# Expected:
#   [INSTALL] Building: image pipeline
#   [APPROVAL REQUIRED] popup appears in GUI window
#   Click YES in the popup
#   [INSTALL] Import OK
#   [INSTALL] Run: integrate runtime_imagepipeline
# FAIL if: [INSTALL] Cancelled.  (auto-cancel = approval dialog broken)

# Command: install music pipeline into umbra
# Expected: same approval flow, creates runtime_musicpipeline.py

# Command: install video pipeline into umbra
# Expected: same approval flow, creates runtime_videopipeline.py

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 7 — SELF-REPAIR
# ════════════════════════════════════════════════════════════════

# Command: fix all bugs
# Expected:
#   [SELF-FIX] Scanning core/runtime...
#   [SELF-FIX] X broken module(s):  (or "All modules clean")
#   [SELF-FIX] Fixed N/N

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 8 — FILE BROWSER
# ════════════════════════════════════════════════════════════════

# Click FILES tab in GUI
# Expected: workspaces/ tree shows your built games and images
# Double-click a .py game file
# Expected: pygame window launches

# Click PREVIEW tab
# Click "Latest" button
# Expected: most recently generated image shows in preview

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 9 — MEMORY
# ════════════════════════════════════════════════════════════════

# Command: remember my favorite game is Skyrim
# Expected: [UMBRA] Stored: my favorite game is Skyrim

# Command: recall favorite game
# Expected: [MEMORY] ... Skyrim

# Click MEMORY tab
# Expected: stored entries appear in the table

# ════════════════════════════════════════════════════════════════
# TEST BLOCK 10 — EXIT
# ════════════════════════════════════════════════════════════════

# Command: exit
# Expected: "Close Umbra completely?" dialog appears
# Click YES → Umbra closes cleanly
# FAIL if: terminal just hangs

# ════════════════════════════════════════════════════════════════
# WHAT EACH STATUS MEANS
# ════════════════════════════════════════════════════════════════

STATUS_MEANINGS = {
    "ComfyUI not running": "PIL placeholder images only. Start ComfyUI for real AI images.",
    "Memory: 0 entries":   "Normal on first launch. Grows as you use Umbra.",
    "GAMING MODE":         "Resource manager detected a game running — normal.",
    "LLM not configured":  "Ollama not running. Start Ollama first.",
    "GIF: ready":          "animated_gif_generator module loaded OK.",
    "TTS: ready|disabled": "Text to speech available but off. Type 'tts on' to enable.",
}

# ════════════════════════════════════════════════════════════════
# QUICK REFERENCE — UMBRA COMMANDS
# ════════════════════════════════════════════════════════════════

COMMANDS = """
SYSTEM
  status                              system health check
  fix all bugs                        scan and repair broken modules
  help                                show all commands
  exit                                close Umbra

GAMES
  make a game called <name>           build with all 7 agents
  build a full game called <name>     same — full deep build
  make a game like Skyrim called <x>  with style/inspiration
  play last                           launch most recent game
  play <name>                         launch specific game

IMAGES  (saves to workspaces/images/)
  make an image of <description>      generate 1 image
  make 5 images of <description>      generate batch
  make an image in graveyard keeper style of a castle

GIF  (saves to workspaces/videos/)
  make a gif of <description>

QUESTIONS (just ask, no "make" or "build")
  what is the capital of Ohio?
  how does X work?
  who invented Y?

SELF-UPGRADE
  install image pipeline into umbra
  install music pipeline into umbra
  install video pipeline into umbra
  install blender pipeline into umbra
  install tiktok pipeline into umbra

MEMORY
  remember <fact>
  recall <query>

FILES
  list files
  clean up old files

VOICE
  tts on / tts off
  voice on / voice off
  listen
"""