import ast, datetime, sys

FP = r"C:\Umbra\Umbra.py"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()

with open(FP + f".bak22_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

LOCK_ANCHOR = '_gui_input_queue = _queue.Queue()\n'
if "_umbra_gen_lock" not in src:
    if LOCK_ANCHOR not in src:
        print("FAIL: lock anchor not found")
        sys.exit(1)
    src = src.replace(
        LOCK_ANCHOR,
        LOCK_ANCHOR + '_umbra_gen_lock = threading.Lock()  # serializes gif/image gen (shared GPU)\n',
        1,
    )

OLD = '''    _gif_words = ["make a gif","create a gif","generate a gif","make gif","make an animated"]
    if any(kw in lower_direct for kw in _gif_words):
        gif_gen = runtime.get("animated_gif_generator")
        if gif_gen and gif_gen.is_available():
            _umbra_print("[UMBRA] Generating GIF...")
            _gr = gif_gen.run(prompt)
            if isinstance(_gr, dict):
                _gpath = _gr.get("path") or _gr.get("file_path") or _gr.get("output")
            else:
                _gpath = str(_gr) if _gr else None
            if _gpath and str(_gpath) != "None":
                _umbra_print("[GIF] Saved: " + str(_gpath))
                _umbra_mem(runtime) and _umbra_mem(runtime).store("last_gif", str(_gpath), tags=["gif"])
            else:
                # Direct fallback using our generator
                try:
                    from core.runtime.runtime_animated_gif_generator import RuntimeAnimatedGifGenerator as _RAGG
                    import os as _osg
                    _gdir = _osg.path.join(_UMBRA_ROOT,"workspaces","videos")
                    _osg.makedirs(_gdir, exist_ok=True)
                    _gagg = _RAGG(output_dir=_gdir)
                    _gr2  = _gagg.run(prompt)
                    _gpath2 = _gr2.get("path") if isinstance(_gr2,dict) else None
                    _umbra_print("[GIF] Saved: " + str(_gpath2))
                except Exception as _ge2:
                    _umbra_print("[GIF] Error: " + str(_ge2))
        else:
            _umbra_print("[GIF] Not available. Run: install a gif generator into umbra")
        return None

    _img_pattern = re.compile(
        r"\\b(make|create|generate|draw)\\b.{0,15}\\b(an?|\\d+)?\\s*(image|images|picture|pictures|art|artwork)\\b"
    )
    if _img_pattern.search(lower_direct):
        _count_m = re.search(r"(\\d+)\\s+image", lower_direct)
        _count = int(_count_m.group(1)) if _count_m else 1
        _count = min(_count, 10)
        _umbra_print("[UMBRA] Generating " + str(_count) + " image(s)...")
        # Try runtime image_generator first, fall back to our own
        img_gen = runtime.get("image_generator")
        for _ci in range(_count):
            if img_gen and hasattr(img_gen, "generate"):
                try:
                    _ir = img_gen.generate(prompt)
                    _umbra_print("[IMAGE " + str(_ci+1) + "] " + (str(_ir.file_path) if _ir.success else str(getattr(_ir,"fallback_description","failed"))))
                    continue
                except Exception: pass
            # Fallback: use RuntimeImageGenerator directly
            try:
                from core.runtime.runtime_image_generator import RuntimeImageGenerator as _RIG
                import os as _os2
                _idir = _os2.path.join(_UMBRA_ROOT, "workspaces", "images")
                _os2.makedirs(_idir, exist_ok=True)
                _rig = _RIG(output_dir=_idir)
                _ir2 = _rig.generate(prompt)
                _umbra_print("[IMAGE " + str(_ci+1) + "] Saved: " + str(_ir2.file_path))
                _umbra_mem(runtime) and _umbra_mem(runtime).store("last_image", _ir2.file_path, tags=["image"])
            except Exception as _ie:
                _umbra_print("[IMAGE] Error: " + str(_ie))
        return None

'''

NEW = '''    _gif_words = ["make a gif","create a gif","generate a gif","make gif","make an animated"]
    if any(kw in lower_direct for kw in _gif_words):
        gif_gen = runtime.get("animated_gif_generator")
        if gif_gen and gif_gen.is_available():
            if not _umbra_gen_lock.acquire(blocking=False):
                _umbra_print("[GIF] Busy generating — try again shortly.")
                return None
            _umbra_print("[UMBRA] Generating GIF in background — Umbra stays responsive...")
            def _gif_worker(_prompt=prompt, _runtime=runtime, _gen=gif_gen):
                try:
                    _gr = _gen.run(_prompt)
                    if isinstance(_gr, dict):
                        _gpath = _gr.get("path") or _gr.get("file_path") or _gr.get("output")
                    else:
                        _gpath = str(_gr) if _gr else None
                    if _gpath and str(_gpath) != "None":
                        _umbra_print("[GIF] Saved: " + str(_gpath))
                        _umbra_mem(_runtime) and _umbra_mem(_runtime).store("last_gif", str(_gpath), tags=["gif"])
                    else:
                        try:
                            from core.runtime.runtime_animated_gif_generator import RuntimeAnimatedGifGenerator as _RAGG
                            import os as _osg
                            _gdir = _osg.path.join(_UMBRA_ROOT,"workspaces","videos")
                            _osg.makedirs(_gdir, exist_ok=True)
                            _gagg = _RAGG(output_dir=_gdir)
                            _gr2  = _gagg.run(_prompt)
                            _gpath2 = _gr2.get("path") if isinstance(_gr2,dict) else None
                            _umbra_print("[GIF] Saved: " + str(_gpath2))
                        except Exception as _ge2:
                            _umbra_print("[GIF] Error: " + str(_ge2))
                except Exception as _gwe:
                    _umbra_print("[GIF] Error: " + str(_gwe))
                finally:
                    _umbra_gen_lock.release()
            threading.Thread(target=_gif_worker, daemon=True, name="UmbraGifGen").start()
        else:
            _umbra_print("[GIF] Not available. Run: install a gif generator into umbra")
        return None

    _img_pattern = re.compile(
        r"\\b(make|create|generate|draw)\\b.{0,15}\\b(an?|\\d+)?\\s*(image|images|picture|pictures|art|artwork)\\b"
    )
    if _img_pattern.search(lower_direct):
        _count_m = re.search(r"(\\d+)\\s+image", lower_direct)
        _count = int(_count_m.group(1)) if _count_m else 1
        _count = min(_count, 10)
        img_gen = runtime.get("image_generator")
        if not _umbra_gen_lock.acquire(blocking=False):
            _umbra_print("[IMAGE] Busy generating — try again shortly.")
            return None
        _umbra_print("[UMBRA] Generating " + str(_count) + " image(s) in background — Umbra stays responsive...")
        def _image_worker(_prompt=prompt, _runtime=runtime, _gen=img_gen, _n=_count):
            try:
                for _ci in range(_n):
                    if _gen and hasattr(_gen, "generate"):
                        try:
                            _ir = _gen.generate(_prompt)
                            _umbra_print("[IMAGE " + str(_ci+1) + "] " + (str(_ir.file_path) if _ir.success else str(getattr(_ir,"fallback_description","failed"))))
                            continue
                        except Exception: pass
                    try:
                        from core.runtime.runtime_image_generator import RuntimeImageGenerator as _RIG
                        import os as _os2
                        _idir = _os2.path.join(_UMBRA_ROOT, "workspaces", "images")
                        _os2.makedirs(_idir, exist_ok=True)
                        _rig = _RIG(output_dir=_idir)
                        _ir2 = _rig.generate(_prompt)
                        _umbra_print("[IMAGE " + str(_ci+1) + "] Saved: " + str(_ir2.file_path))
                        _umbra_mem(_runtime) and _umbra_mem(_runtime).store("last_image", _ir2.file_path, tags=["image"])
                    except Exception as _ie:
                        _umbra_print("[IMAGE] Error: " + str(_ie))
            finally:
                _umbra_gen_lock.release()
        threading.Thread(target=_image_worker, daemon=True, name="UmbraImageGen").start()
        return None

'''

if OLD not in src:
    print("FAIL: OLD block not found")
    sys.exit(1)

if src.count(OLD) != 1:
    print("FAIL: OLD block not unique, count=" + str(src.count(OLD)))
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

print("Fix applied: background-thread gif/image generation (batch22)")