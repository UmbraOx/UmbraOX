import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\core\assets\game_skeleton.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak29_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    def draw_gameover(surf):
        W,H=surf.get_size()
        overlay=pygame.Surface((W,H),pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        surf.blit(overlay,(0,0))
        txt(surf,"GAME OVER",W//2,H//3,64,(220,40,40),center=True)
        txt(surf,"Press R to restart or ESC to quit",W//2,H//2,18,(180,180,180),center=True)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GAME
# ═══════════════════════════════════════════════════════════════════════════'''

NEW = '''    def draw_gameover(surf):
        W,H=surf.get_size()
        overlay=pygame.Surface((W,H),pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        surf.blit(overlay,(0,0))
        txt(surf,"GAME OVER",W//2,H//3,64,(220,40,40),center=True)
        txt(surf,"Press R to restart or ESC to quit",W//2,H//2,18,(180,180,180),center=True)

# --- Guaranteed fallback: draw_main_menu ---
# The block above only runs when the agent didn't supply draw_hud, which
# means draw_main_menu (and its helpers) can end up undefined whenever an
# agent DID supply its own draw_hud. Umbra strips any agent-authored
# draw_main_menu override, so without this independent guard the game has
# no draw_main_menu at all and crashes on launch (NameError). This block
# is self-contained (no dependency on draw_panel) so it always works.
if 'draw_main_menu' not in dir():
    _mm_stars = [(random.randint(0,1280), random.randint(0,720), random.randint(1,3),
                  random.random()*0.5+0.3) for _ in range(120)]
    def draw_main_menu(surf, project_name="__PROJECT_NAME__"):
        W, H = surf.get_size()
        for y in range(H):
            t = y / H
            pygame.draw.line(surf, (int(5+t*15), int(5+t*8), int(15+t*35)), (0, y), (W, y))
        tick = pygame.time.get_ticks()
        for sx, sy, sr, spd in _mm_stars:
            b = int(120 + 100 * abs(math.sin(tick * 0.001 * spd)))
            pygame.draw.circle(surf, (b, b, min(255, b+60)), (sx, sy), sr)
        txt(surf, project_name, W//2, H//4, 56, (230,230,255), center=True)
        labels = ["New Game", "Load Game", "Settings", "Quit"]
        keys = ["new_game", "load_game", "settings", "quit"]
        btns = {}
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            bw, bh = 240, 48
            bx, by = W//2 - bw//2, H//2 + i*60
            r = pygame.Rect(bx, by, bw, bh)
            pygame.draw.rect(surf, (40,40,70), r)
            pygame.draw.rect(surf, (110,110,180), r, 2)
            txt(surf, lbl, bx+bw//2, by+bh//2-8, 18, (220,220,255), center=True)
            btns[key] = r
        return btns

# ═══════════════════════════════════════════════════════════════════════════
# MAIN GAME
# ═══════════════════════════════════════════════════════════════════════════'''

if OLD not in src:
    print("FAIL: anchor block not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor block not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

# game_skeleton.py is a text template (not directly importable - has __PLACEHOLDERS__),
# so validate by substituting placeholders with dummy safe values and parsing.
test_src = (src.replace("__WORLD_CODE__", "").replace("__CHAR_CODE__", "")
               .replace("__ITEM_CODE__", "").replace("__MECH_CODE__", "")
               .replace("__UI_CODE__", "").replace("__QUEST_CODE__", "")
               .replace("__ECON_CODE__", "").replace("__PROJECT_NAME__", "TestGame")
               .replace("__PROJ_SLUG__", "testgame"))
try:
    ast.parse(test_src)
    print("game_skeleton.py AST OK (with placeholders substituted)")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: draw_main_menu now always defined, independent of draw_hud (batch29)")