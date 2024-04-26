import os
from PIL import Image
import pillow_heif
from rembg import remove
import numpy as np
import io

def convert_heic_to_jpg_and_remove_bg(heic_path, jpg_path):
    try:
        # Read HEIC file
        heif_file = pillow_heif.read_heif(heic_path)
        # Convert HEIC data to a PIL image
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )

        # Remove background
        input_bytes = io.BytesIO()
        image.save(input_bytes, format='PNG')  # Save image to a bytes buffer
        input_bytes.seek(0)
        output_removed_bg = remove(input_bytes.read())  # Process the image in memory

        # Convert the result to a PIL image
        image_with_transparency = Image.open(io.BytesIO(output_removed_bg))

        # Create a white background image
        white_background = Image.new("RGBA", image_with_transparency.size, "WHITE")
        # Paste the image on white background, using itself as the mask
        white_background.paste(image_with_transparency, mask=image_with_transparency.split()[3])

        # Convert to RGB and save as JPEG
        final_image = white_background.convert("RGB")
        final_image.save(jpg_path, "JPEG")
        
    except Exception as e:
        print(f"Failed to convert {heic_path}: {e}")

def batch_convert_heic_to_jpg(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each HEIC file in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.heic'):
            heic_path = os.path.join(input_directory, filename)
            jpg_filename = filename[:-5] + '.jpg'
            jpg_path = os.path.join(output_directory, jpg_filename)
            print(f"Converting {filename} to {jpg_filename}...")
            convert_heic_to_jpg_and_remove_bg(heic_path, jpg_path)
            print(f"Saved to {jpg_path}")

# Example usage
input_directory = '/Users/sirapolwareechuensuk/Desktop/Shopee'
output_directory = '/Users/sirapolwareechuensuk/Desktop/Shopee/jpg2/'
batch_convert_heic_to_jpg(input_directory, output_directory)
