# apply_fixes_3.py — run from C:\Umbra with: python apply_fixes_3.py
import ast, os

ROOT = os.path.dirname(os.path.abspath(__file__))
um = open(os.path.join(ROOT, 'Umbra.py'), encoding='utf-8').read()

old = (
    '        # Ensure project_name variable exists in game scope\n'
    '        if \'project_name = \' not in game_code and \'project_name=\' not in game_code:\n'
    '            game_code = game_code.replace(\n'
    '                \'def main():\',\n'
    '                \'project_name = \' + repr(project_name) + \'\\n\\ndef main():\'\n'
    '            )\n'
    '\n'
    '    game_code, report = _test_game('
)
new = (
    '        # Ensure project_name variable exists in game scope\n'
    '        if \'project_name = \' not in game_code and \'project_name=\' not in game_code:\n'
    '            game_code = game_code.replace(\n'
    '                \'def main():\',\n'
    '                \'project_name = \' + repr(project_name) + \'\\n\\ndef main():\'\n'
    '            )\n'
    '        # Patch draw_main_menu to always return a dict\n'
    '        if \'UMBRA_MENU_PATCH\' not in game_code:\n'
    '            game_code += \'\'\'\n'
    '# UMBRA_MENU_PATCH\n'
    'try:\n'
    '    _omm = draw_main_menu\n'
    '    def draw_main_menu(surf, project_name=\'\'):\n'
    '        result = _omm(surf, project_name)\n'
    '        if isinstance(result, dict):\n'
    '            return result\n'
    '        import pygame as _pg2\n'
    '        W,H = surf.get_size()\n'
    '        keys = [\'new_game\',\'load_game\',\'settings\',\'quit\',\'start\',\'play\',\'continue\',\'exit\']\n'
    '        if isinstance(result, (list, tuple)):\n'
    '            out = {}\n'
    '            for i,item in enumerate(result):\n'
    '                k = keys[i] if i < len(keys) else \'btn_\'+str(i)\n'
    '                if isinstance(item, _pg2.Rect): out[k] = item\n'
    '                elif isinstance(item, tuple) and len(item)==2 and isinstance(item[1],_pg2.Rect): out[k] = item[1]\n'
    '            return out if out else {\'new_game\':_pg2.Rect(W//2-100,H//2-20,200,40)}\n'
    '        return {\'new_game\':_pg2.Rect(W//2-100,H//2-20,200,40)}\n'
    'except Exception: pass\n'
    '\'\'\'\n'
    '\n'
    '    game_code, report = _test_game('
)

if old in um:
    um = um.replace(old, new, 1)
    open(os.path.join(ROOT, 'Umbra.py'), 'w', encoding='utf-8').write(um)
    try:
        ast.parse(um)
        print("Fix OK: UMBRA_MENU_PATCH added — draw_main_menu always returns dict")
        print("Syntax OK")
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {e}")
else:
    print("SKIP: already applied or not found")