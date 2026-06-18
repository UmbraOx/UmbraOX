from PIL import Image
import os

def create_animated_gif(image_paths, output_path, duration=100, loop=0):
    """
    Create an animated GIF from a list of image paths.

    Parameters:
    - image_paths: List[str] - A list of file paths to the images.
    - output_path: str - The path where the output GIF will be saved.
    - duration: int - Duration (in milliseconds) for each frame.
    - loop: int - Number of times the GIF should loop. 0 means infinite.

    Raises:
    - FileNotFoundError: If any of the image files do not exist.
    - ValueError: If the image_paths list is empty.
    """
    if not image_paths:
        raise ValueError("The image_paths list cannot be empty.")
    
    images = []
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")
        img = Image.open(path)
        images.append(img)

    # Save the images as an animated GIF
    try:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=loop
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create animated GIF: {e}")

if __name__ == "__main__":
    # Example usage
    image_paths = [
        "path/to/image1.png",
        "path/to/image2.png",
        "path/to/image3.png"
    ]
    output_path = "output.gif"
    
    try:
        create_animated_gif(image_paths, output_path)
        print(f"Animated GIF created successfully at {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
