# UMBRA v2.0 — Quick Start Guide

## Starting Umbra

### Option 1: Desktop App (Recommended — actual window on desktop)
    python umbra_desktop.py

### Option 2: Browser GUI
    python gui_server.py
    Then open: http://localhost:7860

### Option 3: Command Line
    python umbra.py

### Option 4: Desktop Shortcuts (create once)
    python create_shortcuts.py
    Then double-click "UMBRA Desktop" on your desktop.

---

## Using the GUI / Desktop App

1. Type your objective in the input box at the bottom
2. Press Enter or click Run
3. Umbra decomposes it into tasks and generates Python code
4. Generated files appear in the Files tab
5. Click ▶ next to any .py file to run it immediately

---

## Running Generated Game/App Files

After Umbra generates files, find them in:
    C:\Umbra\workspaces\run_XXXX\code\

Files named game.py, main.py, or app.py are the assembled entry points.

Run from Desktop App: Files tab → click ▶
Run from CLI:
    cd C:\Umbra\workspaces\run_0001\code
    python game.py

---

## Tips for Best Results

Use SPECIFIC single-file prompts:
  GOOD: "write a single complete pygame game file with player, enemy, health"
  BAD:  "make a game"

For games, always add:
  "Output as ONE complete Python file. Include all imports. Use if __name__ == '__main__'."

For apps:
  "Single file. Include main() function. All imports at top."

---

## Important Limits

Umbra GENERATES code — it does not run or test it automatically.
You review and run the generated files.

For image generation: Requires Stable Diffusion at localhost:7861
For video generation: Requires ComfyUI at localhost:8188
These are separate tools you install; Umbra integrates with them.

---

## All CLI Commands (python umbra.py)

status | health | analyze | metrics | memory | improve
validate | review | replay | scheduler | handoff
history | resume | config | test | exit
remember <fact> | recall <query>