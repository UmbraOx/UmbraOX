import os

class RuntimeMapGenerator:
    def __init__(self, **kwargs):
        self.ready = False
        try:
            import PIL
            from PIL import ImageDraw, ImageFont
            self.PIL = PIL
            self.ImageDraw = ImageDraw
            self.ImageFont = ImageFont
            self.ready = True
        except ImportError:
            pass

    def is_available(self) -> bool:
        return self.ready

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"error": "PIL library is not available"}

        # Create a blank image
        width, height = 800, 600
        image = self.PIL.Image.new('RGB', (width, height), color = (73, 109, 137))

        # Draw text on the image
        draw = self.ImageDraw.Draw(image)
        font = self.ImageFont.truetype("arial.ttf", 24)  # Replace with a valid font path if necessary
        text = prompt
        text_width, text_height = draw.textsize(text, font=font)
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        draw.text((x, y), text, font=font, fill=(255, 255, 0))

        # Save the image to a file
        output_path = "map.png"
        image.save(output_path)

        return {"output_path": output_path}