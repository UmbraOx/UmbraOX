import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\Umbra.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak51_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''    if 'WORLD_MAP' in dir() and isinstance(WORLD_MAP, list):
        for _wrow in WORLD_MAP:
            if isinstance(_wrow, list):
                for _wi in range(len(_wrow)):
                    if _wrow[_wi] is None:
                        _wrow[_wi] = "GRASS"
except Exception:
    pass'''

NEW = '''    if 'WORLD_MAP' in dir() and isinstance(WORLD_MAP, list):
        for _wrow in WORLD_MAP:
            if isinstance(_wrow, list):
                for _wi in range(len(_wrow)):
                    if _wrow[_wi] is None:
                        _wrow[_wi] = "GRASS"

    # The fix above only covers WORLD_MAP shaped as list-of-lists. Some
    # agents instead build WORLD_MAP as a dict (sparse coordinates, or a
    # dict-of-dicts), and draw_world's own raw "WORLD_MAP[i][j]" indexing
    # (not going through get_biome/get_tile at all) then raises KeyError
    # for any coordinate the agent didn't happen to populate - which the
    # patch above can't see since it isn't a list. Fix this at the data-
    # structure level instead of chasing every possible shape: wrap
    # WORLD_MAP in a proxy whose __getitem__ can never raise, no matter
    # what the underlying structure actually is.
    class _UmbraSafeRow:
        __slots__ = ('_row', '_default')
        def __init__(self, row, default):
            self._row = row
            self._default = default
        def __getitem__(self, j):
            try:
                v = self._row[j]
                return v if v is not None else self._default
            except Exception:
                return self._default
        def __len__(self):
            try:
                return len(self._row)
            except Exception:
                return 0

    class _UmbraSafeGrid:
        __slots__ = ('_data', '_default')
        def __init__(self, data, default="GRASS"):
            self._data = data
            self._default = default
        def __getitem__(self, i):
            try:
                row = self._data[i]
            except Exception:
                return _UmbraSafeRow({}, self._default)
            if isinstance(row, (list, dict, tuple)):
                return _UmbraSafeRow(row, self._default)
            return row if row is not None else self._default
        def __len__(self):
            try:
                return len(self._data)
            except Exception:
                return 0
        def __iter__(self):
            try:
                return iter(self._data)
            except Exception:
                return iter([])

    if 'WORLD_MAP' in dir() and not isinstance(WORLD_MAP, _UmbraSafeGrid):
        WORLD_MAP = _UmbraSafeGrid(WORLD_MAP)
except Exception:
    pass'''

if OLD not in src:
    print("FAIL: anchor not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: anchor not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("Umbra.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: WORLD_MAP wrapped in a universal safe-grid proxy (batch51)")