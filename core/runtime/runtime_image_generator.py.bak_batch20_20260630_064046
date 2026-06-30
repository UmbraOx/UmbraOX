# C:\Umbra\core\runtime\runtime_image_generator.py  v2.1
import os,time,logging
log=logging.getLogger("umbra.imggen")
_ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_NEGATIVE_PROMPT=(
    "lowres, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
    "missing limbs, deformed, blurry, bad face, poorly drawn face, mutation, mutated, "
    "extra arms, extra legs, disfigured, gross proportions, malformed limbs, missing arms, "
    "missing legs, extra feet, multiple feet, long neck, fused fingers, too many fingers, "
    "cloned face, watermark, signature, text, username, worst quality, low quality, "
    "jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, "
    "poorly drawn hands, bad proportions, error, out of focus, deformed iris, deformed pupils"
)
_QUALITY_SUFFIX=", masterpiece, best quality, highly detailed, sharp focus, 8k uhd"
_STYLE_MAP={
    "pixel_art":"pixel art, 16-bit style, ",
    "dark_fantasy":"dark fantasy art, gothic, dramatic lighting, ",
    "graveyard_keeper":"graveyard keeper art style, pixel art, dark humour, medieval, muted colours, ",
    "skyrim":"skyrim concept art, nordic fantasy, epic landscape, ",
    "photorealistic":"photorealistic, DSLR photo, ",
    "anime":"anime art style, cel shaded, ",
    "painterly":"oil painting, painterly, impressionist, ",
}

class ImageResult:
    def __init__(self,success,file_path=None,error=None,fallback_description=None,width=512,height=512,seed=-1,prompt_used=""):
        self.success=success; self.file_path=file_path; self.error=error
        self.fallback_description=fallback_description; self.width=width
        self.height=height; self.seed=seed; self.prompt_used=prompt_used

class RuntimeImageGenerator:
    def __init__(self,output_dir=None,comfyui_url="http://127.0.0.1:8188",
                 default_width=512,default_height=512,default_steps=25,
                 default_cfg=7.0,checkpoint="v1-5-pruned-emaonly.ckpt"):
        self.output_dir=output_dir or os.path.join(_ROOT,"workspaces","images")
        self.comfyui_url=comfyui_url.rstrip("/")
        self.width=default_width; self.height=default_height
        self.steps=default_steps; self.cfg=default_cfg
        self.checkpoint=checkpoint; self._ok=None
        os.makedirs(self.output_dir,exist_ok=True)

    def is_available(self):
        if self._ok is not None: return self._ok
        try:
            import requests as _r
            self._ok=_r.get(self.comfyui_url+"/system_stats",timeout=3).status_code==200
        except Exception: self._ok=False
        return self._ok

    def generate(self,prompt,width=None,height=None,steps=None,cfg=None,seed=None,style=None):
        w=width or self.width; h=height or self.height
        s=steps or self.steps; c=cfg or self.cfg
        seed=seed if seed is not None else (int(time.time())%2**31)
        prefix=_STYLE_MAP.get((style or "").lower(),"")
        full=prefix+prompt+_QUALITY_SUFFIX
        if self.is_available():
            try:
                path=self._comfyui(full,w,h,s,c,seed)
                if path: return ImageResult(True,file_path=path,width=w,height=h,seed=seed,prompt_used=full)
            except Exception as e:
                log.warning("ComfyUI failed: %s",e); self._ok=None
        path=self._pil_placeholder(prompt,w,h,style)
        if path: return ImageResult(True,file_path=path,fallback_description="ComfyUI offline — PIL placeholder",width=w,height=h,seed=seed,prompt_used=full)
        return ImageResult(False,error="Both ComfyUI and PIL failed",fallback_description="Requested: "+prompt)

    def generate_batch(self,prompts,style=None):
        return [self.generate(p,style=style) for p in prompts]

    def _comfyui(self,prompt,w,h,steps,cfg,seed):
        import requests as _r
        wf={
            "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":steps,"cfg":cfg,
                 "sampler_name":"euler_ancestral","scheduler":"karras","denoise":1.0,
                 "model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
            "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":self.checkpoint}},
            "5":{"class_type":"EmptyLatentImage","inputs":{"width":w,"height":h,"batch_size":1}},
            "6":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["4",1]}},
            "7":{"class_type":"CLIPTextEncode","inputs":{"text":_NEGATIVE_PROMPT,"clip":["4",1]}},
            "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
            "9":{"class_type":"SaveImage","inputs":{"images":["8",0],"filename_prefix":"umbra_"}},
        }
        r=_r.post(self.comfyui_url+"/prompt",json={"prompt":wf},timeout=15)
        if r.status_code!=200: raise RuntimeError("ComfyUI HTTP "+str(r.status_code))
        pid=r.json().get("prompt_id")
        if not pid: raise RuntimeError("No prompt_id")
        for _ in range(180):
            time.sleep(1)
            hr=_r.get(f"{self.comfyui_url}/history/{pid}",timeout=5)
            if hr.status_code!=200: continue
            data=hr.json().get(pid,{})
            if not data.get("status",{}).get("completed"): continue
            for no in data.get("outputs",{}).values():
                for img in no.get("images",[]):
                    ir=_r.get(self.comfyui_url+"/view",
                               params={"filename":img["filename"],"subfolder":img.get("subfolder",""),"type":img.get("type","output")},
                               timeout=15)
                    if ir.status_code==200:
                        ts=time.strftime("%Y%m%d_%H%M%S")
                        out=os.path.join(self.output_dir,f"image_{ts}_{seed}.png")
                        with open(out,"wb") as f: f.write(ir.content)
                        return out
        raise RuntimeError("Timeout")

    def _pil_placeholder(self,prompt,w,h,style=None):
        try:
            from PIL import Image,ImageDraw,ImageFilter
            import random,hashlib,textwrap
            seed=int(hashlib.md5(prompt.encode()).hexdigest(),16)%(2**31)
            rng=random.Random(seed)
            style_cols={"dark_fantasy":[(10,5,20),(40,10,60)],"graveyard_keeper":[(15,20,10),(40,50,30)],
                        "pixel_art":[(20,20,40),(60,60,100)]}
            c1,c2=style_cols.get((style or "").lower(),[(15,15,30),(40,30,70)])
            img=Image.new("RGB",(w,h))
            for y in range(h):
                t=y/h
                img.paste(tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)),
                          box=(0,y,w,y+1))
            draw=ImageDraw.Draw(img)
            for _ in range(20):
                x=rng.randint(0,w); y=rng.randint(0,h); r=rng.randint(10,60)
                col=(rng.randint(40,120),rng.randint(20,80),rng.randint(60,140))
                draw.ellipse([x-r,y-r,x+r,y+r],fill=col)
            img=img.filter(ImageFilter.GaussianBlur(2))
            draw=ImageDraw.Draw(img)
            draw.rectangle([8,8,w-8,58],fill=(0,0,0))
            draw.text((12,12),"UMBRA IMAGE",fill=(140,100,255))
            draw.text((12,30),"ComfyUI offline — styled placeholder",fill=(160,160,160))
            for i,ln in enumerate(textwrap.wrap(prompt,max(20,w//9))[:5]):
                draw.text((12,64+i*20),ln,fill=(200,200,220))
            ts=time.strftime("%Y%m%d_%H%M%S")
            out=os.path.join(self.output_dir,f"image_placeholder_{ts}.png")
            img.save(out); return out
        except Exception as e:
            log.warning("PIL placeholder failed: %s",e); return None