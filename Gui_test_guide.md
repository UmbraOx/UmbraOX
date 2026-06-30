# Umbra v3.0.0 — Manual GUI Test Checklist

Run all tests in order. Each section lists what to TYPE in the Umbra chat input and what to EXPECT.

---

## SETUP
```
cd C:\Umbra
venv\Scripts\activate
python Umbra.py
```
GUI should open with 6-tab Control Center. All output appears in the chat panel.

---

## 1. BASIC HEALTH
| Type this | Expect |
|---|---|
| `hello` | Friendly response from qwen3:14b, streaming live |
| `which model` | Lists available Ollama models |
| `status` | Shows runtime status, model names, paths |
| `run tests` | Runs test suite — should show 67 passed + 39 passed |
| `list games` | Lists built games or "No games built yet" |

---

## 2. SMOKE TEST
```
python umbra_smoke_test.py
```
Must show: **PASSED: 27  FAILED: 0**

---

## 3. VOICE
| Type this | Expect |
|---|---|
| `voice on` | "[UMBRA] Voice enabled." — pyttsx3 installs if needed |
| `hello` | Umbra speaks the response aloud |
| `voice off` | "[UMBRA] Voice disabled." |

---

## 4. GAME BUILD
Type this in the Umbra chat:
```
build a snake game called TestSnake
```
**Expect:**
- 5 popup dialogs asking about theme, enemies, features, art style, extra details
- "[WORLD AGENT] Attempt 1/3..." messages streaming in
- All 7 agents run (world, character, item, mechanic, UI, quest, economy)
- "[STITCH]" output assembling the game
- "Done! Type: play TestSnake" at the end

If any agent fails syntax check, watch for "Attempt 2/3..." — the retry loop should kick in automatically.

---

## 5. PLAY GAME
```
play TestSnake
```
**Expect:**
- Pygame window opens (1280x720)
- Animated starfield + moon + hill silhouette on main menu
- Game title "TestSnake" displayed with purple glow
- Three buttons: New Game, Continue, Quit
- Clicking **New Game** starts gameplay
- HUD visible at bottom: HP/MP/STA bars with inline labels, gold, level, spell hotbar
- Minimap in top-right corner with player dot

---

## 6. FUZZY PLAY
```
play testsnke
```
(deliberate typo)

**Expect:** Game still launches (fuzzy name match)

---

## 7. FIX LAST GAME
```
fix last game
```
**Expect:** "[FIX] Syntax OK" or repairs and reports what it patched.

---

## 8. FIX YOURSELF
```
fix yourself
```
**Expect:**
- "[SELF-FIX] Scanning core/runtime modules..."
- "[SELF-FIX] Running test suite..."
- "[SELF-FIX] Umbra is clean!" (if all OK)

---

## 9. BUILD VARIETY
Try each of these — all should route to the deep build pipeline:
```
make a puzzle game called BrainTest
build a racing game called SpeedRun
make a tower defense game
make overquest
```

---

## 10. DEV ASSISTANT
```
show file Umbra.py
```
**Expect:** Dev assistant tab opens or shows file preview.

---

## PASS CRITERIA
- [ ] GUI opens without errors
- [ ] Chat responds with streaming tokens
- [ ] 27/27 smoke tests pass
- [ ] Game builds without crashing (all 7 agents attempt)
- [ ] Game launches to animated menu
- [ ] New Game button starts gameplay with visible HUD
- [ ] `list games` shows built games
- [ ] `fix last game` runs without error
- [ ] `voice on` enables speech