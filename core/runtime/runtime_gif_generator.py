import os
from PIL import Image

class RuntimeGifGenerator:
    def __init__(self, **kwargs):
        self.ready = True
        try:
            from PIL import Image
        except ImportError:
            self.ready = False

    def is_available(self) -> bool:
        return self.ready

    def generate_gif(self, image_paths: list, output_path: str, duration: int = 100) -> dict:
        if not self.is_available():
            return {'status': 'error', 'result': 'Pillow library is not installed'}

        images = [Image.open(img_path) for img_path in image_paths]
        try:
            images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
            return {'status': 'ok', 'result': f'GIF saved to {output_path}'}
        except Exception as e:
            return {'status': 'error', 'result': str(e)}