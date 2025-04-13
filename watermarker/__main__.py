import os
import argparse
from PIL import Image, UnidentifiedImageError

# Main image watermarking function
def watermark_images(source_dir, watermark_file, output_dir=None, location='center', margin=0, size_ratio=20):
    supported_extensions = ('.jpg', '.jpeg', '.png')

    # Load the watermark image
    try:
        watermark_img = Image.open(watermark_file)
    except UnidentifiedImageError:
        print(f"Error: Unable to open watermark image at '{watermark_file}'. Please provide a valid image file.")
        return
    except Exception as e:
        print(f"Unexpected error loading watermark: {e}")
        return

    # Extract alpha channel mask if it exists
    watermark_mask = watermark_img.split()[3] if watermark_img.mode == 'RGBA' else None

    # Recursively walk through the source directory
    for folder_path, _, files in os.walk(source_dir):
        for file_name in files:
            # Skip non-image files and the watermark file itself
            if not file_name.lower().endswith(supported_extensions) or file_name == os.path.basename(watermark_file):
                continue

            image_path = os.path.join(folder_path, file_name)

            try:
                with Image.open(image_path) as img:
                    # Resize watermark based on image size
                    img_w, img_h = img.size
                    target_wm_w = int(min(img_w, img_h) * size_ratio / 100)
                    aspect_ratio = watermark_img.width / watermark_img.height
                    target_wm_h = int(target_wm_w / aspect_ratio)

                    resized_wm = watermark_img.resize((target_wm_w, target_wm_h))
                    resized_mask = watermark_mask.resize((target_wm_w, target_wm_h)) if watermark_mask else None

                    # Define position options
                    positions = {
                        'topleft': (margin, margin),
                        'topright': (img_w - target_wm_w - margin, margin),
                        'bottomleft': (margin, img_h - target_wm_h - margin),
                        'bottomright': (img_w - target_wm_w - margin, img_h - target_wm_h - margin),
                        'center': ((img_w - target_wm_w) // 2, (img_h - target_wm_h) // 2),
                    }

                    # Get coordinates to paste watermark
                    pos_x, pos_y = positions.get(location, positions['center'])
                    img.paste(resized_wm, (pos_x, pos_y), resized_mask)

                    # Create output directory, preserving structure
                    relative_path = os.path.relpath(folder_path, source_dir)
                    final_output_dir = os.path.join(output_dir or source_dir, relative_path)
                    os.makedirs(final_output_dir, exist_ok=True)

                    # Always save as PNG
                    new_filename = os.path.splitext(file_name)[0] + ".png"
                    output_path = os.path.join(final_output_dir, new_filename)
                    img = img.convert("RGBA") if img.mode != "RGBA" else img
                    img.save(output_path, format="PNG")
                    print(f"Watermarked: {output_path}")

            except UnidentifiedImageError:
                print(f"Skipped: '{image_path}' - Unsupported or corrupt image.")
            except Exception as e:
                print(f"Failed to process '{image_path}': {e}")

    watermark_img.close()

# CLI entry point

def main():
    parser = argparse.ArgumentParser(
        description="Batch watermark images with a custom watermark. Maintains folder structure and supports output to a new location."
    )

    # Source image directory
    parser.add_argument('source', metavar='SourceDirectory', help='Path to the folder containing your images.')

    # Watermark image path
    parser.add_argument('watermark', metavar='WatermarkImagePath', help='Path to the watermark image file.')

    # Optional output directory
    parser.add_argument('--output', metavar='DestinationDirectory', default=None,
                        help='Optional directory to save watermarked images. If not provided, overwrites originals.')

    # Location of watermark
    parser.add_argument('--location', choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'],
                        default='center', help='Where to place the watermark on each image. Default is center.')

    # Padding/margin from image edges
    parser.add_argument('--margin', type=int, default=0,
                        help='Padding (in pixels) between the watermark and image edge. Default is 0.')

    # Scale of watermark relative to image size
    parser.add_argument('--scale', type=float, default=20,
                        help="Size of the watermark as a percentage of the image's shortest side. Default is 20.")

    # Parse and execute
    args = parser.parse_args()

    watermark_images(
        source_dir=args.source,
        watermark_file=args.watermark,
        output_dir=args.output,
        location=args.location,
        margin=args.margin,
        size_ratio=args.scale
    )

# Script entry point
if __name__ == '__main__':
    main()
