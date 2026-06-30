# apply_fixes_5.py -- Umbra batch 5: HUD polish, version v3.0.0, smoke test script
# Run from C:\Umbra:  python apply_fixes_5.py
import shutil, os, sys, ast
from datetime import datetime

TARGET = "Umbra.py"
SKEL   = os.path.join("core", "assets", "game_skeleton.py")
BACKUP_U = "Umbra.py.bak_batch5_" + datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_S = SKEL + ".bak_batch5_" + datetime.now().strftime("%Y%m%d_%H%M%S")

for f in [TARGET, SKEL]:
    if not os.path.exists(f):
        print("ERROR: Missing", f); sys.exit(1)

shutil.copy2(TARGET, BACKUP_U)
shutil.copy2(SKEL,   BACKUP_S)
print("Backups:", BACKUP_U, "|", BACKUP_S)

with open(TARGET, "r", encoding="utf-8") as f: src = f.read()
with open(SKEL,   "r", encoding="utf-8") as f: sk  = f.read()
fixes = 0

# ==============================================================================
# FIX 1 (game_skeleton.py): polished HUD + better minimap
# ==============================================================================
OLD_HUD = '''if 'draw_hud' not in dir():
    def draw_bar(surf, x, y, w, h, val, mx, col, bg=(40,40,40)):
        pygame.draw.rect(surf, bg, (x, y, w, h))
        if mx > 0:
            ratio = max(0, min(1, val/mx))
            pygame.draw.rect(surf, col, (x, y, int(w*ratio), h))
        pygame.draw.rect(surf, (100,100,100), (x, y, w, h), 1)
    def draw_x_button(surf, rx, ry, rw, rh):
        bx = rx + rw - 24; by = ry + 4
        r = pygame.Rect(bx, by, 20, 20)
        pygame.draw.rect(surf, (160,40,40), r)
        pygame.draw.rect(surf, (220,80,80), r, 2)
        f = font(14)
        xs = f.render("X", True, (255,255,255))
        surf.blit(xs, (bx+6, by+3))
        return r
    def draw_panel(surf, rx, ry, rw, rh, title=""):
        pygame.draw.rect(surf, (30,30,45), (rx, ry, rw, rh))
        pygame.draw.rect(surf, (80,80,130), (rx, ry, rw, rh), 2)
        if title:
            txt(surf, title, rx+10, ry+8, 18, (200,200,255))
        return draw_x_button(surf, rx, ry, rw, rh)
    def draw_hud(surf, player):
        sw, sh = surf.get_size()
        # Bars
        draw_bar(surf, 10, sh-90, 200, 16, player.hp,  player.max_hp,  (200,40,40))
        draw_bar(surf, 10, sh-68, 200, 16, player.mp,  player.max_mp,  (40,80,200))
        draw_bar(surf, 10, sh-46, 200, 16, player.sta, player.max_sta, (40,180,60))
        txt(surf, "HP " + str(player.hp)+"/"+str(player.max_hp), 10, sh-92, 12, (255,180,180))
        txt(surf, "MP " + str(player.mp)+"/"+str(player.max_mp), 10, sh-70, 12, (160,200,255))
        txt(surf, "STA "+str(player.sta)+"/"+str(player.max_sta),10, sh-48, 12, (160,255,160))
        txt(surf, "Gold: " + str(player.gold),  10, sh-26, 14, (255,220,0))
        txt(surf, "Lv " + str(player.level) + "  " + player.cls, 220, sh-90, 14, (200,200,200))
        xp_pct = int(100 * player.xp / max(1, player.xp_next))
        txt(surf, "XP: " + str(player.xp)+"/"+str(player.xp_next)+" ("+str(xp_pct)+"%)",220, sh-72, 12, (180,220,180))
        weap = player.equipped.get("weapon","---")
        armor = player.equipped.get("armor","---")
        txt(surf, "W: " + (weap or "---"), 220, sh-52, 12, (220,200,160))
        txt(surf, "A: " + (armor or "---"), 220, sh-36, 12, (180,180,220))
        # Spell bar
        spells = player.spells or []
        for si, sp in enumerate(spells[:5]):
            sx2 = sw - 280 + si*56
            sy2 = sh - 60
            col = (60,60,80) if si != player.current_spell else (80,80,150)
            pygame.draw.rect(surf, col, (sx2, sy2, 48, 48))
            pygame.draw.rect(surf, (120,120,200), (sx2, sy2, 48, 48), 2)
            sdata = next((x for x in SPELLS if x["name"]==sp), None)
            scol = sdata["col"] if sdata else (200,200,200)
            pygame.draw.circle(surf, scol, (sx2+24, sy2+20), 12)
            txt(surf, sp[:6], sx2+2, sy2+34, 10, (200,200,200))
    def draw_minimap(surf, player, enemies):
        sw, sh = surf.get_size()
        ms = 120
        mx = sw - ms - 10; my = 10
        pygame.draw.rect(surf, (20,20,30), (mx, my, ms, ms))
        pygame.draw.rect(surf, (80,80,120), (mx, my, ms, ms), 2)
        T = 32
        scale = ms / (200*T)
        for e in enemies:
            if not e.alive: continue
            ex2 = int(e.x * scale) + mx
            ey2 = int(e.y * scale) + my
            if mx<=ex2<mx+ms and my<=ey2<my+ms:
                pygame.draw.circle(surf, (200,40,40), (ex2, ey2), 2)
        px2 = int(player.x * scale) + mx
        py2 = int(player.y * scale) + my
        px2 = max(mx, min(mx+ms-3, px2))
        py2 = max(my, min(my+ms-3, py2))
        pygame.draw.circle(surf, (100,200,255), (px2, py2), 4)'''

NEW_HUD = '''if 'draw_hud' not in dir():
    def draw_bar(surf, x, y, w, h, val, mx, col, bg=(20,20,28), label="", label_col=(220,220,220)):
        # Shadow
        pygame.draw.rect(surf, (0,0,0), (x+2, y+2, w, h))
        # Background
        pygame.draw.rect(surf, bg, (x, y, w, h))
        if mx > 0:
            ratio = max(0.0, min(1.0, val / max(1, mx)))
            fill_w = int(w * ratio)
            if fill_w > 0:
                # Gradient: bright centre strip
                pygame.draw.rect(surf, col, (x, y, fill_w, h))
                hi = tuple(min(255, c + 60) for c in col)
                pygame.draw.rect(surf, hi, (x, y, fill_w, max(1, h//3)))
        # Border
        pygame.draw.rect(surf, (80,80,100), (x, y, w, h), 1)
        # Inline label
        if label:
            lbl_s = font(10).render(label, True, label_col)
            surf.blit(lbl_s, (x + 4, y + (h - lbl_s.get_height())//2))
    def draw_x_button(surf, rx, ry, rw, rh):
        bx = rx + rw - 24; by = ry + 4
        r = pygame.Rect(bx, by, 20, 20)
        pygame.draw.rect(surf, (160,40,40), r)
        pygame.draw.rect(surf, (220,80,80), r, 2)
        xs = font(14).render("X", True, (255,255,255))
        surf.blit(xs, (bx+6, by+3))
        return r
    def draw_panel(surf, rx, ry, rw, rh, title=""):
        # Drop shadow
        pygame.draw.rect(surf, (0,0,0), (rx+4, ry+4, rw, rh))
        pygame.draw.rect(surf, (22,22,38), (rx, ry, rw, rh))
        pygame.draw.rect(surf, (70,70,140), (rx, ry, rw, 2))
        pygame.draw.rect(surf, (70,70,120), (rx, ry, rw, rh), 1)
        if title:
            txt(surf, title, rx+10, ry+8, 16, (180,180,255))
        return draw_x_button(surf, rx, ry, rw, rh)
    def draw_hud(surf, player):
        sw, sh = surf.get_size()
        PAD = 12
        BW, BH = 210, 14
        bx = PAD
        # Semi-transparent HUD backing
        hud_surf = pygame.Surface((BW + 230, 80), pygame.SRCALPHA)
        hud_surf.fill((0, 0, 0, 140))
        surf.blit(hud_surf, (0, sh - 90))
        # Stat bars with inline labels
        draw_bar(surf, bx, sh-84, BW, BH, player.hp,  player.max_hp,  (190,35,35),  label="HP  "+str(player.hp)+"/"+str(player.max_hp),  label_col=(255,200,200))
        draw_bar(surf, bx, sh-65, BW, BH, player.mp,  player.max_mp,  (35,70,200),  label="MP  "+str(player.mp)+"/"+str(player.max_mp),  label_col=(180,210,255))
        draw_bar(surf, bx, sh-46, BW, BH, player.sta, player.max_sta, (35,160,55),  label="STA "+str(player.sta)+"/"+str(player.max_sta), label_col=(180,255,180))
        xp_ratio = player.xp / max(1, player.xp_next)
        draw_bar(surf, bx, sh-27, BW, 8,  player.xp,  player.xp_next, (160,100,220), label="", label_col=(200,180,255))
        # Right-side info block
        ix = bx + BW + 12
        txt(surf, "Lv " + str(player.level) + " " + getattr(player,"cls","Hero"), ix, sh-86, 13, (220,210,160))
        txt(surf, "XP " + str(int(xp_ratio*100)) + "%", ix, sh-70, 11, (180,150,220))
        txt(surf, str(player.gold) + "g", ix, sh-54, 13, (255,210,0))
        weap  = player.equipped.get("weapon", None)
        armr  = player.equipped.get("armor",  None)
        if weap:  txt(surf, "[W] " + str(weap)[:14],  ix, sh-38, 11, (220,195,150))
        if armr:  txt(surf, "[A] " + str(armr)[:14],  ix, sh-24, 11, (170,170,220))
        # Spell hotbar (bottom-right)
        spells = getattr(player, "spells", []) or []
        for si, sp in enumerate(spells[:6]):
            sx2 = sw - 380 + si * 58
            sy2 = sh - 64
            active = (si == getattr(player, "current_spell", 0))
            bg_col = (70,70,120) if active else (30,30,50)
            border_col = (160,130,255) if active else (80,80,120)
            pygame.draw.rect(surf, bg_col, (sx2, sy2, 50, 50))
            pygame.draw.rect(surf, border_col, (sx2, sy2, 50, 50), 2)
            sdata = next((x for x in SPELLS if x.get("name") == sp), None)
            scol = sdata["col"] if sdata else (180,180,200)
            pygame.draw.circle(surf, scol, (sx2+25, sy2+20), 13)
            if active:
                pygame.draw.circle(surf, (255,255,200), (sx2+25, sy2+20), 13, 2)
            txt(surf, sp[:7], sx2+2, sy2+36, 9, (210,210,210))
            txt(surf, str(si+1), sx2+38, sy2+2, 9, (120,120,150))
    def draw_minimap(surf, player, enemies):
        sw, sh = surf.get_size()
        MS = 140
        mx = sw - MS - 10
        my = 10
        # Dark backing with border glow
        pygame.draw.rect(surf, (0,0,0),    (mx-2, my-2, MS+4, MS+4))
        pygame.draw.rect(surf, (12,12,25), (mx, my, MS, MS))
        pygame.draw.rect(surf, (60,60,110),(mx, my, MS, MS), 1)
        # Render world tiles (sampled)
        if "WORLD_MAP" in dir() and "BIOME_COL" in dir():
            wm = WORLD_MAP
            rows = len(wm); cols = len(wm[0]) if rows else 1
            cell = MS / max(rows, cols)
            for ty in range(rows):
                for tx in range(cols):
                    col = BIOME_COL.get(wm[ty][tx], (40,40,40))
                    dark = tuple(max(0, c//3) for c in col)
                    px3 = int(mx + tx * cell)
                    py3 = int(my + ty * cell)
                    cw = max(1, int(cell))
                    pygame.draw.rect(surf, dark, (px3, py3, cw, cw))
        # Enemies
        T = 32
        scale = MS / max(1, 200 * T)
        for e in enemies:
            if not getattr(e, "alive", True): continue
            ex2 = int(e.x * scale) + mx
            ey2 = int(e.y * scale) + my
            if mx <= ex2 < mx+MS and my <= ey2 < my+MS:
                pygame.draw.circle(surf, (220,50,50), (ex2, ey2), 2)
        # Player dot with glow
        px2 = max(mx+3, min(mx+MS-4, int(player.x * scale) + mx))
        py2 = max(my+3, min(my+MS-4, int(player.y * scale) + my))
        pygame.draw.circle(surf, (60,180,255),  (px2, py2), 5)
        pygame.draw.circle(surf, (200,240,255), (px2, py2), 3)
        # Label
        txt(surf, "MAP", mx+4, my+MS-16, 9, (80,80,130))'''

if OLD_HUD in sk:
    sk = sk.replace(OLD_HUD, NEW_HUD, 1); fixes += 1
    print("Fix 1 applied: polished HUD + minimap (game_skeleton.py)")
else:
    print("WARN Fix 1: HUD block not matched")

with open(SKEL, "w", encoding="utf-8") as f: f.write(sk)

# Skeleton AST check
try:
    sk_test = sk.replace("__WORLD_CODE__","pass").replace("__CHAR_CODE__","pass") \
                .replace("__ITEM_CODE__","pass").replace("__MECH_CODE__","pass") \
                .replace("__UI_CODE__","pass").replace("__QUEST_CODE__","pass") \
                .replace("__ECON_CODE__","pass").replace("__PROJECT_NAME__","Umbra")
    ast.parse(sk_test)
    print("  Skeleton AST OK")
except SyntaxError as e:
    print("  SKELETON AST ERROR line", e.lineno, ":", e.msg)
    shutil.copy2(BACKUP_S, SKEL); print("  Restored skeleton")

# ==============================================================================
# FIX 2 (Umbra.py): version bump to v3.0.0 everywhere
# ==============================================================================
for old_v, new_v in [
    ("UMBRA -- Autonomous AI Runtime OS  v2.3.0", "UMBRA -- Autonomous AI Runtime OS  v3.0.0"),
    ("Fixes & Upgrades in v2.3.0:", "Fixes & Upgrades in v3.0.0:"),
    ("  UMBRA v2.4.0 \u2014 Autonomous AI Runtime OS", "  UMBRA v3.0.0 \u2014 Autonomous AI Runtime OS"),
    ("[UMBRA CONFIG v2.3.0 \u2014 CONFIG & COMMANDS \u2014 LLM: Ollama]", "[UMBRA CONFIG v3.0.0 \u2014 CONFIG & COMMANDS \u2014 LLM: Ollama]"),
    ('title + " v2.3.0"', 'title + " v3.0.0"'),
]:
    if old_v in src:
        src = src.replace(old_v, new_v); fixes += 1
        print("Fix 2 applied:", old_v[:50])
    else:
        print("INFO: version string not found:", old_v[:50])

with open(TARGET, "w", encoding="utf-8") as f: f.write(src)

try:
    ast.parse(src)
    print(f"\nUmbra.py AST OK -- {fixes} total fixes applied")
except SyntaxError as e:
    print(f"\nUmbra.py AST ERROR line {e.lineno}: {e.msg}")
    print("Restore:", BACKUP_U)

# ==============================================================================
# (Re-apply) FIX 3 (Umbra.py): _ollama_stream HTTP 500 retry -- was lost in git reset
# ==============================================================================
with open(TARGET, "r", encoding="utf-8") as f: src = f.read()

OLD_STREAM = (
    'def _ollama_stream(prompt, model=None, timeout=1800, num_predict=-1, token_cb=None):\n'
    '    """\n'
    '    Stream tokens directly from Ollama HTTP API.\n'
    '    num_predict=-1 means unlimited (model stops when it finishes).\n'
    '    token_cb: optional callable(token_str) called for each streamed token (for GUI live output).\n'
    '    Returns full response string, or "" on failure.\n'
    '    """\n'
    '    import urllib.request as _ur\n'
    '    import json as _j\n'
    '\n'
    '    if model is None:\n'
    '        model = _get_agent_model()\n'
    '\n'
    '    payload = _j.dumps({\n'
    '        "model": model,\n'
    '        "prompt": prompt,\n'
    '        "stream": True,\n'
    '        "options": {\n'
    '            "num_predict": num_predict,\n'
    '            "temperature": 0.15,\n'
    '            "top_p": 0.9,\n'
    '            "repeat_penalty": 1.1,\n'
    '        }\n'
    '    }).encode("utf-8")\n'
    '\n'
    '    req = _ur.Request(\n'
    '        "http://localhost:11434/api/generate",\n'
    '        data=payload,\n'
    '        headers={"Content-Type": "application/json"},\n'
    '        method="POST",\n'
    '    )\n'
    '\n'
    '    parts = []\n'
    '    try:'
)

NEW_STREAM = r'''def _ollama_stream(prompt, model=None, timeout=1800, num_predict=-1, token_cb=None):
    """
    Stream tokens from Ollama HTTP API.
    Retries up to 3x on HTTP 500 / empty response (Ollama overload).
    Returns full response string, or "" on failure.
    """
    import urllib.request as _ur
    import urllib.error as _ue
    import json as _j
    import time as _time

    if model is None:
        model = _get_agent_model()

    payload = _j.dumps({
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_predict": num_predict,
            "temperature": 0.15,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    }).encode("utf-8")

    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 15, 30]

    for attempt in range(MAX_RETRIES + 1):
        req = _ur.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        parts = []
        try:'''

if OLD_STREAM in src:
    # Also need to replace the closing of the old try block
    # Find and replace the full old function body up to "return "".join(parts)"
    OLD_CLOSE = (
        '    parts = []\n'
        '    try:\n'
        '        with _ur.urlopen(req, timeout=timeout) as resp:\n'
        '            while True:\n'
        '                line = resp.readline()\n'
        '                if not line:\n'
        '                    break\n'
        '                try:\n'
        '                    chunk = _j.loads(line.decode("utf-8", errors="replace"))\n'
        '                    tok = chunk.get("response", "")\n'
        '                    if tok:\n'
        '                        parts.append(tok)\n'
        '                        if token_cb:\n'
        '                            try:\n'
        '                                token_cb(tok)\n'
        '                            except Exception:\n'
        '                                pass\n'
        '                    if chunk.get("done", False):\n'
        '                        break\n'
        '                except Exception:\n'
        '                    continue\n'
        '    except Exception as ex:\n'
        '        _umbra_print("  [STREAM ERROR] " + str(ex))\n'
        '        return ""\n'
        '    return "".join(parts)'
    )
    NEW_CLOSE = (
        '        parts = []\n'
        '        try:\n'
        '            with _ur.urlopen(req, timeout=timeout) as resp:\n'
        '                while True:\n'
        '                    line = resp.readline()\n'
        '                    if not line:\n'
        '                        break\n'
        '                    try:\n'
        '                        chunk = _j.loads(line.decode("utf-8", errors="replace"))\n'
        '                        if chunk.get("error"):\n'
        '                            err_msg = chunk["error"]\n'
        '                            _umbra_print("  [OLLAMA ERROR] " + err_msg)\n'
        '                            if any(kw in err_msg.lower() for kw in ("500", "overload", "busy", "queue", "memory")):\n'
        '                                parts = []; break\n'
        '                        tok = chunk.get("response", "")\n'
        '                        if tok:\n'
        '                            parts.append(tok)\n'
        '                            if token_cb:\n'
        '                                try: token_cb(tok)\n'
        '                                except Exception: pass\n'
        '                        if chunk.get("done", False):\n'
        '                            break\n'
        '                    except Exception:\n'
        '                        continue\n'
        '            result = "".join(parts)\n'
        '            if result: return result\n'
        '            if attempt < MAX_RETRIES:\n'
        '                wait = RETRY_DELAYS[attempt]\n'
        '                _umbra_print("  [STREAM] Empty -- retry " + str(attempt+1) + "/" + str(MAX_RETRIES) + " in " + str(wait) + "s...")\n'
        '                _time.sleep(wait); continue\n'
        '            return ""\n'
        '        except _ue.HTTPError as http_err:\n'
        '            code = http_err.code\n'
        '            if code == 500 and attempt < MAX_RETRIES:\n'
        '                wait = RETRY_DELAYS[attempt]\n'
        '                _umbra_print("  [STREAM] HTTP 500 -- retry " + str(attempt+1) + "/" + str(MAX_RETRIES) + " in " + str(wait) + "s...")\n'
        '                _time.sleep(wait); continue\n'
        '            _umbra_print("  [STREAM ERROR] HTTP " + str(code))\n'
        '            return ""\n'
        '        except _ue.URLError as url_err:\n'
        '            _umbra_print("  [STREAM ERROR] Ollama unreachable: " + str(url_err.reason))\n'
        '            if attempt < MAX_RETRIES:\n'
        '                _time.sleep(RETRY_DELAYS[attempt]); continue\n'
        '            return ""\n'
        '        except Exception as ex:\n'
        '            _umbra_print("  [STREAM ERROR] " + str(ex))\n'
        '            if attempt < MAX_RETRIES:\n'
        '                _time.sleep(RETRY_DELAYS[attempt]); continue\n'
        '            return ""\n'
        '    return ""'
    )
    src2 = src.replace(OLD_STREAM, NEW_STREAM, 1)
    src2 = src2.replace(OLD_CLOSE, NEW_CLOSE, 1)
    if src2 != src:
        src = src2
        print("Fix 3 applied: _ollama_stream HTTP 500 retry (re-applied)")
    else:
        print("WARN Fix 3: close block not matched for _ollama_stream")
else:
    print("INFO Fix 3: _ollama_stream already has retry logic or sig changed")

with open(TARGET, "w", encoding="utf-8") as f: f.write(src)
import ast as _ast2
try:
    _ast2.parse(src)
    print("Final AST OK")
except SyntaxError as e:
    print("FINAL AST ERROR line", e.lineno, ":", e.msg)