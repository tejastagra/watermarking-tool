import os
import argparse
import threading
from PIL import Image, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox

"""
A single-file watermarking tool with both a CLI (command-line interface) and a basic Tkinter GUI.

CLI usage example:
    python3 watermark_tool.py <SourceDirectory> <WatermarkImagePath> [options]

GUI usage:
    python3 watermark_tool.py --gui

The program outputs watermarked images as PNG.
"""

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

###########################
# TKINTER GUI SECTION
###########################

def browse_source():
    path = filedialog.askdirectory()
    if path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, path)


def browse_watermark():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")])
    if path:
        watermark_entry.delete(0, tk.END)
        watermark_entry.insert(0, path)


def browse_output():
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)


def start_watermarking_gui():
    src = source_entry.get()
    wm = watermark_entry.get()
    out = output_entry.get()
    pos = position_box.get()
    margin_val = int(margin_scale.get())
    scale_val = float(scale_scale.get())

    if not src or not wm:
        messagebox.showerror("Missing Input", "Please specify both source folder and watermark file.")
        return

    def run_in_bg():
        watermark_images(
            source_dir=src,
            watermark_file=wm,
            output_dir=out,
            location=pos,
            margin=margin_val,
            size_ratio=scale_val
        )

    # Run watermarking in a thread to prevent GUI freeze
    threading.Thread(target=run_in_bg, daemon=True).start()


def run_gui():
    global source_entry, watermark_entry, output_entry, position_box, margin_scale, scale_scale

    window = tk.Tk()
    window.title("Watermarker Tool - GUI")

    tk.Label(window, text="Source Folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    source_entry = tk.Entry(window, width=40)
    source_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(window, text="Browse", command=browse_source).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(window, text="Watermark File:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    watermark_entry = tk.Entry(window, width=40)
    watermark_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(window, text="Browse", command=browse_watermark).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(window, text="Output Folder:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    output_entry = tk.Entry(window, width=40)
    output_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(window, text="Browse", command=browse_output).grid(row=2, column=2, padx=5, pady=5)

    tk.Label(window, text="Watermark Position:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    position_box = Combobox(window, values=["center", "topleft", "topright", "bottomleft", "bottomright"])
    position_box.set("center")
    position_box.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(window, text="Margin (px):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    margin_scale = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL)
    margin_scale.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(window, text="Scale (%):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
    scale_scale = tk.Scale(window, from_=1, to=100, orient=tk.HORIZONTAL)
    scale_scale.set(20)
    scale_scale.grid(row=5, column=1, padx=5, pady=5)

    tk.Button(window, text="Start Watermarking", command=start_watermarking_gui).grid(row=6, column=1, pady=10)

    window.mainloop()

###########################
# CLI Entry Point
###########################
def main():
    parser = argparse.ArgumentParser(
        description="Single-file Watermarker: run via CLI or GUI."
    )

    # If --gui is present, we skip CLI arguments and launch the GUI
    parser.add_argument('--gui', action='store_true', help='Launch the GUI instead of running in CLI mode.')

    # Only relevant if in CLI mode
    parser.add_argument('source', nargs='?', default=None, help='Path to the folder containing your images.')
    parser.add_argument('watermark', nargs='?', default=None, help='Path to the watermark image file.')
    parser.add_argument('--output', default=None, help='Optional directory to save watermarked images. If not provided, overwrites originals.')
    parser.add_argument('--location', choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'],
                        default='center', help='Where to place the watermark on each image. Default is center.')
    parser.add_argument('--margin', type=int, default=0, help='Padding (in pixels) between the watermark and image edge. Default is 0.')
    parser.add_argument('--scale', type=float, default=20, help="Size of the watermark as a percentage of the image's shortest side. Default is 20.")

    args = parser.parse_args()

    if args.gui:
        run_gui()
    else:
        if not args.source or not args.watermark:
            parser.print_help()
            return
        watermark_images(
            source_dir=args.source,
            watermark_file=args.watermark,
            output_dir=args.output,
            location=args.location,
            margin=args.margin,
            size_ratio=args.scale
        )

if __name__ == '__main__':
    main()
