import ast as _ast_check, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak30_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    world_code    = strip_imports(components.get("world",""))
    char_code     = strip_imports(components.get("character",""))
    item_code     = strip_imports(components.get("item",""))
    mechanic_code = strip_imports(components.get("mechanic",""))
    ui_code       = strip_imports(components.get("ui",""))
    quest_code    = strip_imports(components.get("quest",""))
    economy_code  = strip_imports(components.get("economy",""))'''

NEW = '''    def strip_toplevel_calls(code, label=""):
        """Remove stray top-level executable statements (demo/test code agents
        sometimes leave behind, e.g. 'player = Player()' or a bare 'main()')
        from agent-generated modules. These run at import time, before the
        skeleton's own real setup, and are the #1 cause of 'game closes as
        soon as it opens' crashes. Only class/def/import/simple-constant
        top-level statements survive; anything containing a call is dropped.
        Falls back to returning the code unchanged if it doesn't parse
        (the syntax-repair pass elsewhere handles that case)."""
        if not code or not code.strip():
            return code
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code

        def _has_call(node):
            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    return True
            return False

        new_body = []
        dropped = 0
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef,
                                  ast.FunctionDef, ast.AsyncFunctionDef)):
                new_body.append(node); continue
            if isinstance(node, ast.Assign) and not _has_call(node.value):
                new_body.append(node); continue
            if isinstance(node, ast.AnnAssign) and (node.value is None or not _has_call(node.value)):
                new_body.append(node); continue
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                new_body.append(node); continue  # docstring-like, harmless
            if isinstance(node, ast.If):
                # keep guarded blocks (e.g. if __name__=='__main__') — they
                # don't execute on import; also covers any conditional defs
                new_body.append(node); continue
            dropped += 1
        if dropped == 0:
            return code
        tree.body = new_body
        try:
            _umbra_print("  [STITCH] " + label + ": stripped " + str(dropped) +
                          " stray top-level statement(s) (would run at import time)")
        except Exception:
            pass
        try:
            return ast.unparse(tree)
        except Exception:
            return code

    world_code    = strip_toplevel_calls(strip_imports(components.get("world","")), "world")
    char_code     = strip_toplevel_calls(strip_imports(components.get("character","")), "character")
    item_code     = strip_toplevel_calls(strip_imports(components.get("item","")), "item")
    mechanic_code = strip_toplevel_calls(strip_imports(components.get("mechanic","")), "mechanic")
    ui_code       = strip_toplevel_calls(strip_imports(components.get("ui","")), "ui")
    quest_code    = strip_toplevel_calls(strip_imports(components.get("quest","")), "quest")
    economy_code  = strip_toplevel_calls(strip_imports(components.get("economy","")), "economy")'''

if OLD not in src:
    print("FAIL: anchor block not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor block not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    _ast_check.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: strip stray top-level executable statements from agent code before stitching (batch30)")