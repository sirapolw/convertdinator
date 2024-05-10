import os
from PIL import Image
from rembg import remove
import io

def convert_image_and_customize(image_path, jpg_path, remove_bg=True, make_square=True, compress=False):
    try:
        # Open the image file
        image = Image.open(image_path)

        if remove_bg:
            # Remove background
            input_bytes = io.BytesIO()
            image.save(input_bytes, format='PNG')  # Save image to a bytes buffer
            input_bytes.seek(0)
            output_removed_bg = remove(input_bytes.read())  # Process the image in memory
            image = Image.open(io.BytesIO(output_removed_bg))

        if make_square:
            # Determine the size for a square image
            max_size = max(image.size)
            # Create a white background image that is square
            white_background = Image.new("RGB", (max_size, max_size), "WHITE")
            # Calculate the position to paste the image onto the white background
            left = (max_size - image.width) // 2
            top = (max_size - image.height) // 2
            # Paste the image on white background
            white_background.paste(image, (left, top))
            image = white_background

        # Convert to RGB and save as JPEG
        if compress:
            # Find the best quality to ensure the file is under 2MB
            quality = 95
            temp_bytes = io.BytesIO()
            while temp_bytes.tell() > 2 * 1024 * 1024 or quality == 95:  # Initial run or size too large
                temp_bytes = io.BytesIO()
                image.save(temp_bytes, format="JPEG", quality=quality)
                quality -= 5
            image.save(jpg_path, "JPEG", quality=quality)
        else:
            image.save(jpg_path, "JPEG")

    except Exception as e:
        print(f"Failed to convert {image_path}: {e}")

def batch_convert_images(input_directory, output_directory, remove_bg, make_square, compress):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each image file in the input directory
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.heic') or filename.lower().endswith('.jpg'):
            image_path = os.path.join(input_directory, filename)
            jpg_filename = filename[:-4] + '.jpg'
            jpg_path = os.path.join(output_directory, jpg_filename)
            print(f"Converting {filename} to {jpg_filename}...")
            convert_image_and_customize(image_path, jpg_path, remove_bg, make_square, compress)
            print(f"Saved to {jpg_path}")

# Gather user input to configure the process
remove_bg = input("Remove and replace white background? (y/n): ").strip().lower() == 'y'
make_square = input("Make 1:1 ratio? (y/n): ").strip().lower() == 'y'
compress = input("Compress the image to be under 2MB? (y/n): ").strip().lower() == 'y'

# Example usage
input_directory = '/Users/sirapolwareechuensuk/Desktop/Shopee/'
output_directory = '/Users/sirapolwareechuensuk/Desktop/Shopee/compressed/'
batch_convert_images(input_directory, output_directory, remove_bg, make_square, compress)
