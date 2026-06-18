"""
RuntimeAnimatedGifGenerator
Generates animated GIFs using PIL by creating frames programmatically.
No external image files needed. Uses only stdlib + Pillow.
"""
import os
import shutil
import tempfile
import math


class RuntimeAnimatedGifGenerator:
    def __init__(self, output_dir=None, **kwargs):
        self.ready = False
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "workspaces", "videos"
        )
        try:
            from PIL import Image, ImageDraw
            self._Image = Image
            self._ImageDraw = ImageDraw
            self.ready = True
        except ImportError:
            self.ready = False

    def is_available(self):
        return self.ready

    def _parse_subject(self, prompt):
        """Extract a simple subject description from the prompt."""
        prompt_lower = prompt.lower()
        if "bear" in prompt_lower:
            return "bear", (139, 90, 43)
        elif "cat" in prompt_lower:
            return "cat", (200, 150, 100)
        elif "dog" in prompt_lower:
            return "dog", (160, 120, 80)
        elif "robot" in prompt_lower:
            return "robot", (150, 150, 170)
        elif "dragon" in prompt_lower:
            return "dragon", (50, 150, 50)
        else:
            return "character", (100, 100, 200)

    def _draw_dancing_frame(self, draw, subject, color, frame_idx, total_frames, w, h):
        """Draw a simple animated character doing a dance move."""
        cx, cy = w // 2, h // 2
        t = frame_idx / total_frames
        angle = math.sin(t * 2 * math.pi)

        # Body
        body_x = cx + int(angle * 10)
        body_y = cy + int(abs(angle) * 5)
        draw.ellipse([body_x - 20, body_y - 30, body_x + 20, body_y + 30],
                     fill=color, outline=(0, 0, 0), width=2)

        # Head
        head_x = body_x + int(angle * 5)
        head_y = body_y - 50
        draw.ellipse([head_x - 15, head_y - 15, head_x + 15, head_y + 15],
                     fill=color, outline=(0, 0, 0), width=2)

        # Eyes
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 0)
        for ex_off in [-6, 6]:
            draw.ellipse([head_x + ex_off - 4, head_y - 5,
                          head_x + ex_off + 4, head_y + 3],
                         fill=eye_color, outline=pupil_color)
            draw.ellipse([head_x + ex_off - 2, head_y - 3,
                          head_x + ex_off + 2, head_y + 1],
                         fill=pupil_color)

        # Smile
        draw.arc([head_x - 8, head_y, head_x + 8, head_y + 10],
                 start=0, end=180, fill=(0, 0, 0), width=2)

        # Arms - waving
        left_arm_end_x = body_x - 40 + int(angle * 20)
        left_arm_end_y = body_y - 10 + int(angle * 15)
        draw.line([body_x - 20, body_y - 10, left_arm_end_x, left_arm_end_y],
                  fill=(0, 0, 0), width=3)

        right_arm_end_x = body_x + 40 - int(angle * 20)
        right_arm_end_y = body_y - 10 - int(angle * 15)
        draw.line([body_x + 20, body_y - 10, right_arm_end_x, right_arm_end_y],
                  fill=(0, 0, 0), width=3)

        # Legs - stepping
        left_leg_x = body_x - 10 + int(angle * 15)
        left_leg_y = body_y + 50
        draw.line([body_x - 10, body_y + 30, left_leg_x, left_leg_y],
                  fill=(0, 0, 0), width=3)

        right_leg_x = body_x + 10 - int(angle * 15)
        right_leg_y = body_y + 50
        draw.line([body_x + 10, body_y + 30, right_leg_x, right_leg_y],
                  fill=(0, 0, 0), width=3)

        # Draw armour if mentioned
        # Helmet
        draw.arc([head_x - 17, head_y - 20, head_x + 17, head_y + 5],
                 start=180, end=360, fill=(180, 180, 200), width=3)

        # Chest plate
        draw.rectangle([body_x - 18, body_y - 25, body_x + 18, body_y + 5],
                        outline=(180, 180, 200), width=2)

        # Label
        draw.text((5, 5), subject.upper(), fill=(50, 50, 50))

    def generate_dancing_gif(self, subject, color, output_path, frames=16, size=(200, 200), duration=80):
        """Generate an animated dancing GIF."""
        Image = self._Image
        ImageDraw = self._ImageDraw

        gif_frames = []
        w, h = size
        bg_colors = [(230, 230, 255), (225, 235, 255), (220, 230, 255), (225, 235, 255)]

        for i in range(frames):
            bg = bg_colors[i % len(bg_colors)]
            frame = Image.new("RGB", (w, h), bg)
            draw = ImageDraw.Draw(frame)
            # Ground
            draw.line([(0, h - 20), (w, h - 20)], fill=(100, 80, 60), width=3)
            # Music notes for fun
            note_x = (i * 15) % (w + 20) - 10
            draw.text((note_x, 10), "♪", fill=(200, 100, 200))
            draw.text(((note_x + 40) % w, 15), "♫", fill=(100, 200, 100))
            self._draw_dancing_frame(draw, subject, color, i, frames, w, h)
            gif_frames.append(frame)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            duration=duration,
            loop=0,
            optimize=False,
        )

    def run(self, prompt: str) -> dict:
        if not self.is_available():
            return {"status": "error", "error": "Pillow not installed. Run: pip install Pillow"}

        try:
            subject, color = self._parse_subject(prompt)
            os.makedirs(self.output_dir, exist_ok=True)

            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = "gif_" + subject + "_" + ts + ".gif"
            output_path = os.path.join(self.output_dir, fname)

            self.generate_dancing_gif(subject, color, output_path, frames=20, size=(240, 240))

            return {
                "status": "ok",
                "path": output_path,
                "subject": subject,
                "frames": 20,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}