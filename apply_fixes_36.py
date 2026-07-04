import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\core\assets\game_skeleton.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak36_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''def _umbra_flex(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except TypeError:
        pass
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        raise
    params = [p for p in sig.parameters.values()
              if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                             inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL
                       for p in sig.parameters.values())
    max_pos = len(params) if not has_varargs else len(args)
    call_args = list(args[:max_pos])
    for i in range(len(call_args), min(max_pos, len(params))):
        p = params[i]
        if p.default is not inspect.Parameter.empty:
            break
        nl = p.name.lower()
        if nl in ("sw", "screen_w", "width", "w"):
            call_args.append(1280)
        elif nl in ("sh", "screen_h", "height", "h"):
            call_args.append(720)
        elif nl in ("dt", "delta", "delta_time"):
            call_args.append(0.016)
        elif "name" in nl:
            call_args.append("Entity")
        elif nl in ("cls", "class_name", "player_class", "job"):
            call_args.append("Warrior")
        elif nl in ("x", "y", "ex", "ey", "nx", "ny"):
            call_args.append(0)
        else:
            call_args.append(None)
    return fn(*call_args, **kwargs)'''

NEW = '''_COORD_X_NAMES = {"x","px","dx","ex","nx","bx","tx"}
_COORD_Y_NAMES = {"y","py","dy","ey","ny","by","ty"}
_OBJECT_NAMES  = {"player","entity","target","obj","actor","self_entity","p"}

def _umbra_flex(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except TypeError:
        pass
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        raise
    params = [p for p in sig.parameters.values()
              if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                             inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL
                       for p in sig.parameters.values())
    max_pos = len(params) if not has_varargs else len(args)
    target_params = params[:max_pos]

    def _is_plain(v):
        return isinstance(v, (int, float, str, bool, list, dict, tuple, type(None)))

    # Build a pool of (value, tag_set) candidates. Object-like args (e.g. a
    # Player/Entity instance) also contribute their .x/.y as separate
    # coordinate candidates, since an agent's version of a method may want
    # raw coordinates where the skeleton passes a whole object (or vice
    # versa). This is what makes the adapter type/semantic-aware instead
    # of purely positional.
    pool = []          # list of [value, tags, used]
    plain_fifo = []     # original args, for pure positional fallback
    for a in args:
        plain_fifo.append(a)
        if not _is_plain(a) and hasattr(a, "x") and hasattr(a, "y"):
            pool.append([a, {"object"}, False])
            try:
                pool.append([getattr(a, "x"), set(_COORD_X_NAMES), False])
            except Exception:
                pass
            try:
                pool.append([getattr(a, "y"), set(_COORD_Y_NAMES), False])
            except Exception:
                pass
        else:
            pool.append([a, {"scalar"}, False])

    call_args = []
    fifo_idx = 0
    for p in target_params:
        nl = p.name.lower()
        want_tags = set()
        if nl in _COORD_X_NAMES: want_tags |= _COORD_X_NAMES
        if nl in _COORD_Y_NAMES: want_tags |= _COORD_Y_NAMES
        if nl in _OBJECT_NAMES:  want_tags |= {"object"}

        matched = None
        if want_tags:
            for cand in pool:
                if not cand[2] and cand[1] & want_tags:
                    matched = cand
                    break
        if matched:
            matched[2] = True
            call_args.append(matched[0])
            continue

        if fifo_idx < len(plain_fifo):
            call_args.append(plain_fifo[fifo_idx])
            fifo_idx += 1
            continue

        if p.default is not inspect.Parameter.empty:
            break
        if nl in ("sw", "screen_w", "width", "w"):
            call_args.append(1280)
        elif nl in ("sh", "screen_h", "height", "h"):
            call_args.append(720)
        elif nl in ("dt", "delta", "delta_time"):
            call_args.append(0.016)
        elif "name" in nl:
            call_args.append("Entity")
        elif nl in ("cls", "class_name", "player_class", "job"):
            call_args.append("Warrior")
        elif want_tags:
            call_args.append(0)
        else:
            call_args.append(None)
    return fn(*call_args, **kwargs)'''

if OLD not in src:
    print("FAIL: anchor not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

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

print("Fix applied: _umbra_flex is now name/type-aware, not just arity-based (batch36)")