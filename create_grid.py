import os
from PIL import Image

def crop_to_square(image):
    """
    Crops an image to a square by taking the center region.
    
    :param image: A PIL Image object.
    :return: A cropped square PIL Image object.
    """
    width, height = image.size
    if width == height:
        return image
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    return image.crop((left, top, left + min_dim, top + min_dim))

def create_image_grid(folder_path, output_path, grid_size=3, cell_size=300):
    """
    Creates a grid of cropped images with a specific image at the center.

    :param folder_path: Path to the folder containing images.
    :param output_path: File path for the output image.
    :param grid_size: Number of rows and columns in the grid.
    :param cell_size: Size (width and height) of each grid cell.
    """
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if "pfp.jpg" not in image_files:
        raise FileNotFoundError("The image 'pfp.jpg' must be present in the folder.")

    image_files.remove("pfp.jpg")
    image_files = image_files[:(grid_size * grid_size - 1)]
    center_index = (grid_size * grid_size) // 2

    images = [
        crop_to_square(Image.open(os.path.join(folder_path, f))).resize((cell_size, cell_size))
        for f in image_files
    ]
    center_image = crop_to_square(Image.open(os.path.join(folder_path, "pfp.jpg"))).resize((cell_size, cell_size))

    canvas_size = grid_size * cell_size
    canvas = Image.new("RGB", (canvas_size, canvas_size))

    for index, img in enumerate(images):
        if index >= center_index:
            index += 1  # Shift index to make space for the center image
        x = (index % grid_size) * cell_size
        y = (index // grid_size) * cell_size
        canvas.paste(img, (x, y))

    center_x = (center_index % grid_size) * cell_size
    center_y = (center_index // grid_size) * cell_size
    canvas.paste(center_image, (center_x, center_y))

    canvas.save(output_path)

# Example usage
if __name__ == "__main__":
    folder_path = "D:\\PIXEL_ART\\Portfolio\\Year2024"  # Replace with your folder path
    output_path = "grid_output.png"
    create_image_grid(folder_path, output_path)
