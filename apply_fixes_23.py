import ast, datetime, sys

FP = r"C:\Umbra\core\runtime\runtime_image_generator.py"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

with open(FP, "r", encoding="utf-8") as f:
    src = f.read()

with open(FP + f".bak23_{ts}", "w", encoding="utf-8") as f:
    f.write(src)

OLD1 = '''_NEGATIVE_PROMPT=(
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, long neck, fused fingers, too many fingers, "
    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, "
    "poorly drawn hands, bad proportions, error, out of focus, deformed iris, deformed pupils"
)
_QUALITY_SUFFIX=", masterpiece, best quality, highly detailed, sharp focus, 8k uhd"'''

NEW1 = '''_NEGATIVE_PROMPT=(
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, fewer fingers, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, long neck, fused fingers, too many fingers, "
    "cloned face, distorted face, asymmetric face, asymmetric eyes, crossed eyes, "
    "malformed eyes, extra eyes, deformed eyes, unnatural eyes, lazy eye, uneven eyes, "
    "bad eyes, ugly eyes, blurry eyes, mutated hands and fingers, poorly drawn eyes, "
    "watermark, signature, text, username, worst quality, low quality, normal quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, "
    "poorly drawn hands, bad proportions, error, out of focus, deformed iris, deformed pupils, "
    "extra limb, missing body parts, malformed hands, long body, conjoined, "
    "signature watermark username, artist name, bad composition, cropped, low contrast"
)
_QUALITY_SUFFIX=(
    ", masterpiece, best quality, ultra detailed, professional photography, "
    "sharp focus, symmetrical face, detailed eyes, realistic eyes, natural skin texture, "
    "correct anatomy, 8k uhd, high resolution"
)'''

OLD2 = '''    def __init__(self,output_dir=None,comfyui_url="http://127.0.0.1:8188",
                 default_width=512,default_height=512,default_steps=30,
                 default_cfg=7.0,checkpoint="dreamshaper_8.safetensors"):'''

NEW2 = '''    def __init__(self,output_dir=None,comfyui_url="http://127.0.0.1:8188",
                 default_width=512,default_height=512,default_steps=36,
                 default_cfg=7.5,checkpoint="dreamshaper_8.safetensors"):'''

OLD3 = '''            "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":steps,"cfg":cfg,
                 "sampler_name":"euler_ancestral","scheduler":"karras","denoise":1.0,
                 "model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},'''

NEW3 = '''            "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":steps,"cfg":cfg,
                 "sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,
                 "model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},'''

for OLD, NEW, tag in [(OLD1, NEW1, "negatives/quality"), (OLD2, NEW2, "defaults"), (OLD3, NEW3, "sampler")]:
    if OLD not in src:
        print("FAIL: block not found -> " + tag)
        sys.exit(1)
    if src.count(OLD) != 1:
        print("FAIL: block not unique -> " + tag)
        sys.exit(1)
    src = src.replace(OLD, NEW, 1)

with open(FP, "w", encoding="utf-8") as f:
    f.write(src)

try:
    ast.parse(src)
    print("runtime_image_generator.py AST OK")
except SyntaxError as e:
    print("AST FAIL: " + str(e))
    sys.exit(1)

print("Fix applied: professional-grade negative prompt, dpmpp_2m sampler, steps 36/cfg 7.5 (batch23)")