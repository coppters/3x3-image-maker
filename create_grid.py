import os
from PIL import Image
import streamlit as st

def crop_to_square(image):
    """Crops an image to a square by taking the center region."""
    width, height = image.size
    if width == height:
        return image
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    return image.crop((left, top, right, bottom))

def create_image_grid(folder_path, output_path, grid_size=3, cell_size=300):
    """Creates a grid of cropped images with a specific image at the center."""
    # Get all image files from the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    # Ensure the special image "pfp.jpg" is in the folder
    if "pfp.jpg" not in image_files:
        raise FileNotFoundError("The image 'pfp.jpg' must be present in the folder.")

    # Remove "pfp.jpg" from the list and place it at the center
    image_files.remove("pfp.jpg")
    image_files = image_files[:(grid_size * grid_size - 1)]  # Limit to the grid size minus one
    center_index = (grid_size * grid_size) // 2

    # Load, crop, and resize images
    images = [crop_to_square(Image.open(os.path.join(folder_path, f))).resize((cell_size, cell_size)) for f in image_files]
    center_image = crop_to_square(Image.open(os.path.join(folder_path, "pfp.jpg"))).resize((cell_size, cell_size))

    # Create a blank canvas
    canvas_size = grid_size * cell_size
    canvas = Image.new("RGB", (canvas_size, canvas_size))

    # Paste images onto the canvas
    for index, img in enumerate(images):
        if index == center_index:
            continue
        x = (index % grid_size) * cell_size
        y = (index // grid_size) * cell_size
        if index > center_index:
            x = ((index + 1) % grid_size) * cell_size
            y = ((index + 1) // grid_size) * cell_size
        canvas.paste(img, (x, y))

    # Paste the center image
    center_x = (center_index % grid_size) * cell_size
    center_y = (center_index // grid_size) * cell_size
    canvas.paste(center_image, (center_x, center_y))

    # Save the final image
    canvas.save(output_path)
    return output_path

# Streamlit UI
st.title("Image Grid Creator")
st.write("Upload your images and ensure `pfp.jpg` is included for the center.")

# Input folder
folder_path = st.text_input("Enter the folder path containing images:", "D:/PIXEL_ART/Portfolio/2024")

# Output file
output_path = st.text_input("Enter the output file path:", "grid_output.png")

# Process images
if st.button("Create Grid"):
    try:
        result = create_image_grid(folder_path, output_path)
        st.success(f"Grid created successfully! Saved at: {result}")
        st.image(result, caption="Generated Image Grid")
    except Exception as e:
        st.error(f"Error: {e}")
