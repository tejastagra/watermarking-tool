import os
import sys
import argparse
import threading
from PIL import Image, UnidentifiedImageError, ImageStat
import pillow_heif
pillow_heif.register_heif_opener()
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Progressbar
import cv2
import numpy as np

"""
A watermarking tool with both CLI and GUI, now supports images and videos, including HEIC/HEIF input.
"""

def is_dark_background(image):
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    return stat.mean[0] < 128

def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))

def get_position_coordinates(location, img_w, img_h, wm_w, wm_h, margin):
    return {
        'Centre': ((img_w - wm_w) // 2, (img_h - wm_h) // 2),
        'Top left': (margin, margin),
        'Top right': (img_w - wm_w - margin, margin),
        'Bottom left': (margin, img_h - wm_h - margin),
        'Bottom right': (img_w - wm_w - margin, img_h - wm_h - margin)
    }.get(location, (0, 0))

def watermark_images(source_dir, watermark_light, watermark_dark, output_dir=None, location='Centre', margin=15, size_ratio=40, progress_callback=None):
    supported_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.heif')
    try:
        light_wm = Image.open(watermark_light)
        dark_wm = Image.open(watermark_dark)
    except Exception as e:
        print(f"Error loading watermark images: {e}")
        return

    light_mask = light_wm.split()[3] if light_wm.mode == 'RGBA' else None
    dark_mask = dark_wm.split()[3] if dark_wm.mode == 'RGBA' else None

    all_files = [
        os.path.join(dp, f) for dp, _, filenames in os.walk(source_dir)
        for f in filenames if f.lower().endswith(supported_extensions) and f not in [os.path.basename(watermark_light), os.path.basename(watermark_dark)]
    ]
    total_files = len(all_files)
    processed = 0
    failed_images = []

    for image_path in all_files:
        folder_path = os.path.dirname(image_path)
        file_name = os.path.basename(image_path)
        try:
            img = Image.open(image_path)

            use_light = is_dark_background(img)
            wm_img = light_wm if use_light else dark_wm
            wm_mask = light_mask if use_light else dark_mask

            img_w, img_h = img.size
            target_wm_w = int(min(img_w, img_h) * size_ratio / 100)
            aspect_ratio = wm_img.width / wm_img.height
            target_wm_h = int(target_wm_w / aspect_ratio)

            resized_wm = wm_img.resize((target_wm_w, target_wm_h))
            resized_mask = wm_mask.resize((target_wm_w, target_wm_h)) if wm_mask else None

            pos_x, pos_y = get_position_coordinates(location, img_w, img_h, target_wm_w, target_wm_h, margin)
            img.paste(resized_wm, (pos_x, pos_y), resized_mask)

            relative_path = os.path.relpath(folder_path, source_dir)
            final_output_dir = os.path.join(output_dir or source_dir, relative_path)
            os.makedirs(final_output_dir, exist_ok=True)

            new_filename = os.path.splitext(file_name)[0] + ".png"
            output_path = os.path.join(final_output_dir, new_filename)
            img = img.convert("RGBA") if img.mode != "RGBA" else img
            img.save(output_path, format="PNG")
            print(f"Watermarked image: {output_path}")
        except Exception as e:
            print(f"Failed to process image '{image_path}': {e.__class__.__name__}: {e}")
            failed_images.append(image_path)
        processed += 1
        if progress_callback:
            progress_callback(processed / total_files * 100)

    light_wm.close()
    dark_wm.close()

    if failed_images:
        print("\n--- Failed Images ---")
        for path in failed_images:
            print(path)

# Video watermarking
def watermark_video(video_path, wm_light_path, wm_dark_path, output_dir, location='Centre', margin=15, size_ratio=40, progress_callback=None):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Could not open video: {video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = os.path.splitext(os.path.basename(video_path))[0] + "_watermarked.mp4"
        output_path = os.path.join(output_dir, output_filename)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        wm_light = Image.open(wm_light_path)
        wm_dark = Image.open(wm_dark_path)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            use_light = is_dark_background(pil_frame)
            wm = wm_light if use_light else wm_dark

            target_wm_w = int(min(width, height) * size_ratio / 100)
            aspect_ratio = wm.width / wm.height
            target_wm_h = int(target_wm_w / aspect_ratio)
            wm_resized = wm.resize((target_wm_w, target_wm_h)).convert("RGBA")

            pos_x, pos_y = get_position_coordinates(location, width, height, target_wm_w, target_wm_h, margin)
            base = pil_frame.convert("RGBA")
            base.paste(wm_resized, (pos_x, pos_y), wm_resized)
            out_frame = cv2.cvtColor(np.array(base), cv2.COLOR_RGBA2BGR)
            out.write(out_frame)

        cap.release()
        out.release()
        wm_light.close()
        wm_dark.close()
        if progress_callback:
            progress_callback(100)
        print(f"Watermarked video saved to {output_path}")
    except Exception as e:
        print(f"Error processing video '{video_path}': {e}")

# GUI Application class
class WatermarkApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Bulk Watermarking Tool by Tejas Tagra")
        self.show_home()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear()
        tk.Label(self.root, text="Choose media type to watermark:", font=('Arial', 14)).pack(pady=20)
        tk.Button(self.root, text="Watermark Images", width=30, command=self.show_image_gui).pack(pady=10)
        tk.Button(self.root, text="Watermark Video", width=30, command=self.show_video_gui).pack(pady=10)

    def show_image_gui(self):
        self.clear()
        self.build_gui(is_video=False)

    def show_video_gui(self):
        self.clear()
        self.build_gui(is_video=True)

    def build_gui(self, is_video):
        def browse(entry, is_file=True):
            path = filedialog.askopenfilename() if is_file else filedialog.askdirectory()
            if path:
                entry.delete(0, tk.END)
                entry.insert(0, path)

        tk.Button(self.root, text="← Back", command=self.show_home).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Source File:" if is_video else "Source Folder:").grid(row=1, column=0, sticky='e')
        src_entry = tk.Entry(self.root, width=40)
        src_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=lambda: browse(src_entry, is_file=is_video)).grid(row=1, column=2)

        tk.Label(self.root, text="Light Watermark:").grid(row=2, column=0, sticky='e')
        light_entry = tk.Entry(self.root, width=40)
        light_entry.grid(row=2, column=1)
        tk.Button(self.root, text="Browse", command=lambda: browse(light_entry)).grid(row=2, column=2)

        tk.Label(self.root, text="Dark Watermark:").grid(row=3, column=0, sticky='e')
        dark_entry = tk.Entry(self.root, width=40)
        dark_entry.grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=lambda: browse(dark_entry)).grid(row=3, column=2)

        tk.Label(self.root, text="Output Folder:").grid(row=4, column=0, sticky='e')
        out_entry = tk.Entry(self.root, width=40)
        out_entry.grid(row=4, column=1)
        tk.Button(self.root, text="Browse", command=lambda: browse(out_entry, is_file=False)).grid(row=4, column=2)

        tk.Label(self.root, text="Position:").grid(row=5, column=0, sticky='e')
        pos_box = Combobox(self.root, values=["Centre", "Top left", "Top right", "Bottom left", "Bottom right"])
        pos_box.set("Centre")
        pos_box.grid(row=5, column=1)

        tk.Label(self.root, text="Margin (px):").grid(row=6, column=0, sticky='e')
        margin_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        margin_scale.set(15)
        margin_scale.grid(row=6, column=1)

        tk.Label(self.root, text="Scale (%):").grid(row=7, column=0, sticky='e')
        scale_scale = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL)
        scale_scale.set(40)
        scale_scale.grid(row=7, column=1)

        progress_bar = Progressbar(self.root, length=300, mode='determinate')
        progress_bar.grid(row=9, column=1, pady=10)
        progress_label = tk.Label(self.root, text="Progress: 0%")
        progress_label.grid(row=10, column=1)

        def start():
            args = {
                "src": src_entry.get(),
                "wm_light": light_entry.get(),
                "wm_dark": dark_entry.get(),
                "out": out_entry.get(),
                "pos": pos_box.get(),
                "margin": int(margin_scale.get()),
                "scale": float(scale_scale.get())
            }
            if not all(args.values()):
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            def progress_callback(value):
                progress_bar['value'] = value
                progress_label.config(text=f"Progress: {int(value)}%")
                self.root.update_idletasks()

            fn = watermark_video if is_video else watermark_images
            threading.Thread(target=fn, args=(
                args["src"], args["wm_light"], args["wm_dark"], args["out"],
                args["pos"], args["margin"], args["scale"], progress_callback
            ), daemon=True).start()

        tk.Button(self.root, text="Start Watermarking", command=start).grid(row=8, column=1, pady=20)

    def run(self):
        self.root.mainloop()

# CLI Mode
def run_cli():
    parser = argparse.ArgumentParser(description="Bulk Watermarking Tool (Image + Video Watermarker): run via CLI.")
    parser.add_argument('source', help='Folder containing images or videos.')
    parser.add_argument('light', help='Path to light watermark image.')
    parser.add_argument('dark', help='Path to dark watermark image.')
    parser.add_argument('--output', default=None, help='Directory to save output files.')
    parser.add_argument('--location', choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'], default='center')
    parser.add_argument('--margin', type=int, default=15)
    parser.add_argument('--scale', type=float, default=40)
    args = parser.parse_args()

    pos_map = {
        "topleft": "Top left",
        "topright": "Top right",
        "bottomleft": "Bottom left",
        "bottomright": "Bottom right",
        "center": "Centre"
    }
    watermark_images(
        source_dir=args.source,
        watermark_light=args.light,
        watermark_dark=args.dark,
        output_dir=args.output,
        location=pos_map[args.location],
        margin=args.margin,
        size_ratio=args.scale
    )

# Entrypoint
if __name__ == '__main__':
    if '--gui' in sys.argv or len(sys.argv) == 1:
        WatermarkApp().run()
    else:
        run_cli()
