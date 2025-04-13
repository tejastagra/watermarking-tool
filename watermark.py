
import os
import argparse
from PIL import Image, UnidentifiedImageError

def watermark_images(source_dir, logo_file, output_dir=None, location='center', margin=0, size_ratio=20):
    supported_extensions = ('.jpg', '.jpeg', '.png')

    try:
        logo_img = Image.open(logo_file)
    except UnidentifiedImageError:
        print(f"Error: Unable to open logo image at '{logo_file}'. Please provide a valid image file.")
        return
    except Exception as e:
        print(f"Unexpected error loading logo: {e}")
        return

    logo_mask = logo_img.split()[3] if logo_img.mode == 'RGBA' else None

    for folder_path, _, files in os.walk(source_dir):
        for file_name in files:
            if not file_name.lower().endswith(supported_extensions) or file_name == os.path.basename(logo_file):
                continue

            image_path = os.path.join(folder_path, file_name)

            try:
                with Image.open(image_path) as img:
                    img_w, img_h = img.size
                    target_logo_w = int(min(img_w, img_h) * size_ratio / 100)
                    aspect_ratio = logo_img.width / logo_img.height
                    target_logo_h = int(target_logo_w / aspect_ratio)

                    resized_logo = logo_img.resize((target_logo_w, target_logo_h))
                    resized_mask = logo_mask.resize((target_logo_w, target_logo_h)) if logo_mask else None

                    positions = {
                        'topleft': (margin, margin),
                        'topright': (img_w - target_logo_w - margin, margin),
                        'bottomleft': (margin, img_h - target_logo_h - margin),
                        'bottomright': (img_w - target_logo_w - margin, img_h - target_logo_h - margin),
                        'center': ((img_w - target_logo_w) // 2, (img_h - target_logo_h) // 2),
                    }

                    pos_x, pos_y = positions.get(location, positions['center'])
                    img.paste(resized_logo, (pos_x, pos_y), resized_mask)

                    relative_path = os.path.relpath(folder_path, source_dir)
                    final_output_dir = os.path.join(output_dir or source_dir, relative_path)
                    os.makedirs(final_output_dir, exist_ok=True)

                    output_path = os.path.join(final_output_dir, file_name)
                    img = img.convert("RGB") if img.mode == "RGBA" else img
                    img.save(output_path)
                    print(f"Watermarked: {output_path}")
            except UnidentifiedImageError:
                print(f"Skipped: '{image_path}' - Unsupported or corrupt image.")
            except Exception as e:
                print(f"Failed to process '{image_path}': {e}")

    logo_img.close()

def main():
    parser = argparse.ArgumentParser(
        description="Batch watermark images with a logo. Maintains folder structure and supports output to a new location."
    )

    parser.add_argument('source', metavar='SourceDirectory', help='Path to the folder containing your images.')
    parser.add_argument('logo', metavar='WatermarkLogoPath', help='Path to the watermark logo image.')

    parser.add_argument('--output', metavar='DestinationDirectory', default=None,
                        help='Optional directory to save watermarked images. If not provided, overwrites originals.')

    parser.add_argument('--location', choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'],
                        default='center', help='Where to place the watermark on each image. Default is center.')

    parser.add_argument('--margin', type=int, default=0,
                        help='Padding (in pixels) between the watermark and image edge. Default is 0.')

    parser.add_argument('--scale', type=float, default=20,
                        help="Size of the watermark logo as a percentage of the image's shortest side. Default is 20.")

    args = parser.parse_args()

    watermark_images(
        source_dir=args.source,
        logo_file=args.logo,
        output_dir=args.output,
        location=args.location,
        margin=args.margin,
        size_ratio=args.scale
    )

if __name__ == '__main__':
    main()
