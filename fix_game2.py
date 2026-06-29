# fix_game2.py — run from C:\Umbra: python fix_game2.py
import ast, os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
KEYS = ["new_game", "continue", "quit", "settings", "load_game", "credits"]

def fix_file(path):
    src = open(path, encoding='utf-8').read()
    lines = src.splitlines()
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        # Find draw_main_menu function
        if ln.startswith('def draw_main_menu'):
            fn_lines = [ln]
            i += 1
            # Collect entire function
            while i < len(lines) and (lines[i].startswith('    ') or lines[i] == ''):
                fn_lines.append(lines[i])
                i += 1
            fn = '\n'.join(fn_lines)
            # Check if it returns a list (not already a dict)
            if 'return btns' in fn or (fn.count('return [') > 0):
                # Replace the return with dict version
                # Find button labels from btn() calls
                import re
                labels = re.findall(r"btn\([^,]+,[^,]+,[^,]+,[^,]+,[^,]+,\s*['\"]([^'\"]+)['\"]", fn)
                if not labels:
                    labels = ['Start', 'Load Game', 'Exit']
                key_map = {
                    'start': 'new_game', 'play': 'new_game', 'new game': 'new_game',
                    'load': 'continue', 'load game': 'continue', 'continue': 'continue',
                    'exit': 'quit', 'quit': 'quit',
                    'settings': 'settings', 'credits': 'credits',
                }
                # Build new function that returns dict
                new_fn = fn
                # Replace 'return btns' with dict comprehension
                new_fn = re.sub(
                    r'(\n    btns = \[\].*?return btns)',
                    lambda m: build_dict_version(m.group(0), labels, key_map),
                    new_fn,
                    flags=re.DOTALL
                )
                # Also fix literal list returns
                new_fn = re.sub(
                    r'    return \[([^\]]+)\]',
                    lambda m: fix_list_return(m.group(1), labels, key_map),
                    new_fn
                )
                out.extend(new_fn.splitlines())
            else:
                out.extend(fn_lines)
        else:
            out.append(ln)
            i += 1
    
    result = '\n'.join(out)
    try:
        ast.parse(result)
        if result != src:
            open(path, 'w', encoding='utf-8').write(result)
            print(f"FIXED: {os.path.basename(path)}")
        else:
            print(f"NO CHANGE: {os.path.basename(path)}")
    except SyntaxError as e:
        print(f"SYNTAX ERROR in fix: {e} — applying direct patch instead")
        apply_direct_patch(path, src)

def build_dict_version(match, labels, key_map):
    import re
    # Keep all the drawing code, just change the return
    lines = match.strip().splitlines()
    new_lines = []
    btn_var_names = []
    for ln in lines:
        if ln.strip().startswith('btns = []') or ln.strip().startswith('btns.append('):
            continue  # remove list building
        m = re.match(r'\s+(\w+)\s*=\s*btn\(', ln)
        if m:
            btn_var_names.append(m.group(1))
            new_lines.append(ln)
            continue
        new_lines.append(ln)
    
    # Generate dict return using label-to-key mapping
    btn_calls = re.findall(r"(\w+)\s*=\s*btn\([^)]+,\s*['\"]([^'\"]+)['\"]", match)
    if btn_calls:
        pairs = ', '.join(
            f'"{key_map.get(label.lower(), KEYS[i] if i < len(KEYS) else \"btn_\"+str(i))}": {var}'
            for i, (var, label) in enumerate(btn_calls)
        )
        new_lines = [l for l in new_lines if 'return btns' not in l and 'btns = []' not in l and 'btns.append' not in l]
        new_lines.append(f'    return {{{pairs}}}')
    else:
        new_lines = [l for l in new_lines if 'return btns' not in l]
        new_lines.append('    return {"new_game": pygame.Rect(400, 200, 200, 40)}')
    return '\n' + '\n'.join(new_lines)

def fix_list_return(items_str, labels, key_map):
    items = [x.strip() for x in items_str.split(',')]
    pairs = ', '.join(
        f'"{key_map.get(labels[i].lower(), KEYS[i] if i < len(KEYS) else \"btn_\"+str(i))}": {v}'
        for i, v in enumerate(items)
    )
    return f'    return {{{pairs}}}'

def apply_direct_patch(path, src):
    # Nuclear option: wrap draw_main_menu at the end of file
    if 'UMBRA_MENU_PATCH' not in src:
        patch = '''
# UMBRA_MENU_PATCH
try:
    _omm = draw_main_menu
    def draw_main_menu(surf, project_name=''):
        import pygame as _pg
        result = _omm(surf, project_name)
        if isinstance(result, dict): return result
        W, H = surf.get_size()
        KEYS = ['new_game','continue','quit','settings','load_game','credits']
        if isinstance(result, (list, tuple)):
            out = {}
            for i, item in enumerate(result):
                k = KEYS[i] if i < len(KEYS) else 'btn_'+str(i)
                if isinstance(item, _pg.Rect): out[k] = item
                elif isinstance(item, (list, tuple)) and item and isinstance(item[-1], _pg.Rect): out[k] = item[-1]
            return out or {'new_game': _pg.Rect(W//2-100, H//2, 200, 50)}
        return {'new_game': _pg.Rect(W//2-100, H//2, 200, 50)}
except Exception: pass
'''
        src2 = src + patch
        try:
            ast.parse(src2)
            open(path, 'w', encoding='utf-8').write(src2)
            print(f"PATCHED (wrapper): {os.path.basename(path)}")
        except SyntaxError as e:
            print(f"FAILED: {e}")

# Fix all game files
games = glob.glob(os.path.join(ROOT, 'workspaces', 'agent_builds', '**', '*_game.py'), recursive=True)
if not games:
    print("No game files found")
for g in games:
    apply_direct_patch(g, open(g, encoding='utf-8').read())

print("\nDone. Run: python Umbra.py then: play last")