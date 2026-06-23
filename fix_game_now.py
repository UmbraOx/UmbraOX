"""
fix_game_now.py - Run once from C:/Umbra to fix game crash
Usage: python fix_game_now.py
"""
import os, re

WS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspaces")

def fix_game(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()
    changed = False

    # Rename game loop to main() if main() missing but called
    if "def main():" not in code:
        fns = re.findall(r"^def (\w+)\(\):", code, re.MULTILINE)
        for fn in fns:
            idx  = code.find("def " + fn + "():")
            body = code[idx:idx+3000]
            if any(k in body for k in ["clock.tick","pygame.event.get","pygame.display.flip"]):
                code = code.replace("def " + fn + "():", "def main():", 1)
                code = re.sub(r"\b" + fn + r"\(\)", "main()", code)
                print("  Renamed:", fn + "() -> main()")
                changed = True
                break

    # Ensure __name__ guard
    if "if __name__" not in code:
        code += "\n\nif __name__ == '__main__':\n    main()\n"
        changed = True
        print("  Added __name__ guard")

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        print("  SAVED:", path)
    else:
        print("  OK (no fix needed):", path)
    return changed

print("Scanning workspaces for game files...")
fixed = 0
for root, dirs, files in os.walk(WS):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
    for fname in files:
        if not fname.endswith(".py"): continue
        if any(g in fname.lower() for g in ["game","mygame","optiopia","demiworld","main_game"]):
            fp = os.path.join(root, fname)
            print("\nChecking:", fp)
            if fix_game(fp): fixed += 1

print("\nDone. Fixed", fixed, "file(s).")
print("Now: python Umbra.py  then type: play last")