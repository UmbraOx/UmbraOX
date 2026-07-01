import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_and_read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        s = f.read()
    with open(fp + f".bak24_{ts}", "w", encoding="utf-8") as f:
        f.write(s)
    return s

def apply(fp, replacements, label):
    src = backup_and_read(fp)
    for OLD, NEW in replacements:
        if OLD not in src:
            print("FAIL (" + label + "): block not found")
            sys.exit(1)
        if src.count(OLD) != 1:
            print("FAIL (" + label + "): block not unique")
            sys.exit(1)
        src = src.replace(OLD, NEW, 1)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(src)
    try:
        ast.parse(src)
        print(label + " AST OK")
    except SyntaxError as e:
        print("AST FAIL (" + label + "): " + str(e))
        sys.exit(1)

# --- 1. Image generator: fix teeth ---
IMG_FP = r"C:\Umbra\core\runtime\runtime_image_generator.py"
IMG_OLD = '''    "extra limb, missing body parts, malformed hands, long body, conjoined, "
    "signature watermark username, artist name, bad composition, cropped, low contrast"
)'''
IMG_NEW = '''    "extra limb, missing body parts, malformed hands, long body, conjoined, "
    "signature watermark username, artist name, bad composition, cropped, low contrast, "
    "bad teeth, deformed teeth, crooked teeth, missing teeth, extra teeth, unnatural teeth, "
    "bad mouth, deformed mouth, ugly smile"
)'''
apply(IMG_FP, [(IMG_OLD, IMG_NEW)], "runtime_image_generator.py")

# --- 2. GIF generator: better prompt adherence / quality ---
GIF_FP = r"C:\Umbra\core\runtime\runtime_animated_gif_generator.py"
GIF_OLD1 = '''    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, flicker, "
    "inconsistent, poorly drawn hands, bad proportions, error, out of focus"
)
_QUALITY_SUFFIX = ", masterpiece, best quality, highly detailed, smooth animation, consistent character"'''
GIF_NEW1 = '''    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, flicker, "
    "inconsistent, poorly drawn hands, bad proportions, error, out of focus, "
    "wrong subject, incorrect object, missing subject, extra objects, cluttered background, "
    "off-topic, unrelated scene"
)
_QUALITY_SUFFIX = ", masterpiece, best quality, highly detailed, smooth animation, consistent character, accurate to description, clear subject, coherent scene"'''

GIF_OLD2 = '''                 frame_count=8, width=384, height=384, steps=16, cfg=7.0, **kwargs):'''
GIF_NEW2 = '''                 frame_count=8, width=384, height=384, steps=20, cfg=8.5, **kwargs):'''

apply(GIF_FP, [(GIF_OLD1, GIF_NEW1), (GIF_OLD2, GIF_NEW2)], "runtime_animated_gif_generator.py")

print("Fix applied: teeth negatives + gif cfg 8.5/steps 20 for prompt adherence (batch24)")