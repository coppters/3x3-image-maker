import os
from PIL import Image
import streamlit as st

def crop_to_square(image):
    """
    Crops an image to a square by taking the center region.
    """
    width, height = image.size
    if width == height:
        return image
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    return image.crop((left, top, right, bottom))

def create_image_grid(images, center_image, output_path, grid_size=3, cell_size=300):
    """
    Creates a grid of uploaded images with a specific image at the center.
    """
    # Limit to grid size minus one
    images = images[:(grid_size * grid_size - 1)]
    center_index = (grid_size * grid_size) // 2

    # Crop and resize images
    processed_images = [crop_to_square(image).resize((cell_size, cell_size)) for image in images]
    center_image = crop_to_square(center_image).resize((cell_size, cell_size))

    # Create a blank canvas
    canvas_size = grid_size * cell_size
    canvas = Image.new("RGB", (canvas_size, canvas_size))

    # Paste images onto the canvas
    for index, img in enumerate(processed_images):
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
st.write("Upload your images and select one as the center.")

# Upload multiple images
uploaded_files = st.file_uploader("Upload images (8 total):", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# Select the center image
center_image_file = st.file_uploader("Upload the center image:", type=["jpg", "jpeg", "png"])

# Output file name
output_path = st.text_input("Enter the output file path:", "grid_output.png")

# Process images
if st.button("Create Grid"):
    if len(uploaded_files) < 8:
        st.error("Please upload at least 8 images.")
    elif center_image_file is None:
        st.error("Please upload the center image.")
    else:
        try:
            # Load images
            images = [Image.open(file) for file in uploaded_files]
            center_image = Image.open(center_image_file)

            # Create the grid
            result = create_image_grid(images, center_image, output_path)

            # Display success and the resulting image
            st.success(f"Grid created successfully!")
            st.image(result, caption="Generated Image Grid")
        except Exception as e:
            st.error(f"Error: {e}")
