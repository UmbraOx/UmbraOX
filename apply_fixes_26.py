import ast, datetime, sys

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
FP = r"C:\Umbra\core\runtime\runtime_animated_gif_generator.py"

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()
with open(FP + f".bak26_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD = '''_NEGATIVE_PROMPT = (
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, fused fingers, too many fingers, "
    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, flicker, "
    "inconsistent, poorly drawn hands, bad proportions, error, out of focus, "
    "wrong subject, incorrect object, missing subject, extra objects, cluttered background, "
    "off-topic, unrelated scene"
)
_QUALITY_SUFFIX = ", masterpiece, best quality, highly detailed, smooth animation, consistent character, accurate to description, clear subject, coherent scene"'''

NEW = '''_NEGATIVE_PROMPT = (
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, fused fingers, too many fingers, "
    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, flicker, flickering, "
    "inconsistent, poorly drawn hands, bad proportions, error, out of focus, "
    "wrong subject, incorrect object, missing subject, extra objects, cluttered background, "
    "off-topic, unrelated scene, neon, neon colors, neon lights, glowing, glow, "
    "flashing lights, strobe, strobing, oversaturated, over-saturated, garish colors, "
    "psychedelic, psychedelic colors, rainbow colors, blacklight, uv colors, "
    "harsh lighting, overexposed, color banding"
)
_QUALITY_SUFFIX = ", masterpiece, best quality, highly detailed, smooth animation, consistent character, accurate to description, clear subject, coherent scene, natural lighting, natural colors, realistic color palette"'''

if OLD not in src:
    print("FAIL: negative prompt block not found")
    sys.exit(1)
if src.count(OLD) != 1:
    print("FAIL: negative prompt block not unique")
    sys.exit(1)
src = src.replace(OLD, NEW, 1)

OLD2 = '''                 frame_count=8, width=384, height=384, steps=20, cfg=8.5, **kwargs):'''
NEW2 = '''                 frame_count=8, width=384, height=384, steps=20, cfg=7.0, **kwargs):'''

if OLD2 not in src:
    print("FAIL: cfg default block not found")
    sys.exit(1)
if src.count(OLD2) != 1:
    print("FAIL: cfg default block not unique")
    sys.exit(1)
src = src.replace(OLD2, NEW2, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("runtime_animated_gif_generator.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: cfg 8.5->7.0 (was causing oversaturation/neon), added neon/flash/glow negatives (batch26)")