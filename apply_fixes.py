# apply_fixes.py — run once from C:\Umbra with: python apply_fixes.py
import ast, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Fix 1: game_skeleton.py — txt() always defined ──────────────────
sk = open(os.path.join(ROOT, 'core/assets/game_skeleton.py'), encoding='utf-8').read()
old1 = ("# --- Fallback: UI ---\n"
        "if 'draw_hud' not in dir():\n"
        "    _FONT_CACHE = {}\n"
        "    def font(size):\n"
        "        if size not in _FONT_CACHE:\n"
        "            _FONT_CACHE[size] = pygame.font.SysFont(\"Arial\", size)\n"
        "        return _FONT_CACHE[size]\n"
        "    def txt(surf, text, x, y, size=16, col=(255,255,255), center=False):\n"
        "        f = font(size)\n"
        "        s = f.render(str(text), True, col)\n"
        "        if center: x -= s.get_width()//2\n"
        "        surf.blit(s, (x, y))\n"
        "    def draw_bar(")
new1 = ("# --- Always-available helpers ---\n"
        "_FONT_CACHE = {}\n"
        "def font(size):\n"
        "    if size not in _FONT_CACHE:\n"
        "        _FONT_CACHE[size] = pygame.font.SysFont(\"Arial\", size)\n"
        "    return _FONT_CACHE[size]\n"
        "def txt(surf, text, x, y, size=16, col=(255,255,255), center=False):\n"
        "    f = font(size)\n"
        "    s = f.render(str(text), True, col)\n"
        "    if center: x -= s.get_width()//2\n"
        "    surf.blit(s, (x, y))\n"
        "\n"
        "# --- Fallback: UI ---\n"
        "if 'draw_hud' not in dir():\n"
        "    def draw_bar(")
if old1 in sk:
    sk = sk.replace(old1, new1, 1)
    open(os.path.join(ROOT, 'core/assets/game_skeleton.py'), 'w', encoding='utf-8').write(sk)
    print("Fix 1 OK: txt() always defined")
else:
    print("Fix 1 SKIP: already applied")

# ── Fix 2: Umbra.py — per-question build popups ─────────────────────
um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()
old2 = ("        _umbra_print(\"\\n[UMBRA] Before I build, a few quick questions:\")\n"
        "        for _q in _clarify_qs: _umbra_print(\"  \" + _q)\n"
        "        _umbra_print(\"  (or type 'skip' to use defaults)\")\n"
        "        _clarify_ans = _safe_input(\"your answers > \", \"skip\").strip()\n"
        "        if _clarify_ans and _clarify_ans.lower() != \"skip\":\n"
        "            prompt = prompt + \". Details: \" + _clarify_ans")
new2 = ("        _umbra_print(\"\\n[UMBRA] Answer each popup to customise your game (close to skip):\\n\")\n"
        "        _answers = []\n"
        "        for _ql, _qh in [(\"Genre\",\"RPG/platformer/shooter/puzzle/survival/strategy\"),\n"
        "                          (\"Setting\",\"fantasy/sci-fi/horror/modern/post-apocalyptic\"),\n"
        "                          (\"Enemies\",\"how many types? 0-10\"),\n"
        "                          (\"Features\",\"crafting/magic/building/stealth/none\"),\n"
        "                          (\"Art style\",\"pixel/top-down/side-scroll/isometric\")]:\n"
        "            _a = _safe_input(_ql + \"?\\n(\" + _qh + \")\", \"\").strip()\n"
        "            if _a: _answers.append(_ql + \": \" + _a)\n"
        "        if _answers: prompt = prompt + \". Details: \" + \"; \".join(_answers)")
if old2 in um:
    um = um.replace(old2, new2, 1)
    print("Fix 2 OK: per-question popups")
else:
    print("Fix 2 SKIP: already applied")

# ── Fix 3: Umbra.py — clean banner ──────────────────────────────────
old3 = ("    _umbra_print(\"  UMBRA v2.4.0 \u2014 Autonomous AI Runtime OS\")\n"
        "    try:\n"
        "        from core.runtime.runtime_version import get_full_version\n"
        "        _umbra_print(\"  \" + get_full_version())\n"
        "    except Exception:\n"
        "        pass\n"
        "    _umbra_print(\"  type 'help' for commands | 'exit' to quit\")")
new3 = ("    _umbra_print(\"  UMBRA v2.4.0 \u2014 Autonomous AI Runtime OS\")\n"
        "    _umbra_print(\"  type 'help' for commands | 'exit' to quit\")")
if old3 in um:
    um = um.replace(old3, new3, 1)
    print("Fix 3 OK: clean banner")
else:
    print("Fix 3 SKIP: already applied")

# ── Fix 4: Umbra.py — strict item agent prompt ───────────────────────
old4 = ("            \"No imports needed \u2014 just pure data.\"\n"
        "        ),")
new4 = ("            \"No imports needed.\\n\"\n"
        "            \"STRICT RULES: No classes. No functions. No if/for/while. No f-strings. Under 90 lines.\"\n"
        "        ),")
if old4 in um:
    um = um.replace(old4, new4, 1)
    print("Fix 4 OK: strict item agent")
else:
    print("Fix 4 SKIP: already applied")

open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)

try:
    ast.parse(um)
    print("\nSyntax OK — run: git add -A && git commit -m 'Batch fixes' && git push origin main")
except SyntaxError as e:
    print(f"\nSYNTAX ERROR: {e}")