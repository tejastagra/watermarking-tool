# Watermarker Tool

This program was created by **Tejas Tagra (u7786686)**.  
Please contact [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au) for maintenance requests, bugs, or more information.

---

## About This Tool

This Python-based watermarking tool allows you to apply a custom watermark to multiple images within a directory, including its subdirectories. It is designed for batch processing and customization, making it ideal for professional or academic use where branded or identified images are necessary.

You can:
- Choose where the watermark should appear
- Set the watermark's size relative to the image
- Add optional margin (padding) from image edges
- Save results in-place or in a separate output folder
- Maintain original folder structure when exporting
- Select the appropriate watermark style (`watermark-light.png` or `watermark-dark.png`) depending on the background brightness of your images

A sample image is included in the `/images` folder for testing purposes. You may safely delete this file without affecting the tool’s functionality.

---

## Features

- Recursively scans folders and subfolders for image files
- Supports common image formats: `.jpg`, `.jpeg`, `.png`
- Allows watermark placement in any corner or the center
- Watermark resizes proportionally to image dimensions
- Padding ensures the watermark doesn’t touch image edges
- Option to overwrite original images or save to new directory
- Preserves the input folder structure when exporting
- Fully offline operation; no internet connection required
- All watermarked images are saved in `.png` format
- Includes a user-friendly GUI for non-technical users

---

## Requirements

### Python 3.6+

Ensure Python 3 is installed. You can download it from:  
https://www.python.org/downloads/

### Required Library: Pillow

Install the image-processing library using pip:

```bash
pip3 install pillow
```

---

## How to Use

### Option 1: Run the GUI

If you prefer using a graphical interface, simply run:

```bash
python3 watermark_tool.py --gui
```

This will launch a GUI where you can:
- Select a **source folder** containing your images
- Choose your **watermark image**
- Optionally choose an **output folder**
- Pick the **watermark position** (top left, center, bottom right, etc.)
- Adjust the **margin** (padding from the edge)
- Set the **scale** (how big the watermark should be)

Once everything’s set, just click **"Start Watermarking"**, and the tool will process your images without freezing the interface.

> 💡 Tip: If you leave the output folder blank, it will overwrite the images in place (with `.png` versions). Use a separate folder if you want to preserve originals.

---

### Option 2: Use the CLI

If you prefer the command line, you can also use the tool that way.

Run it directly as a script:

```bash
python3 watermark_tool.py <ImageDirectory> <WatermarkPath> [options]
```

---

## Command-Line Arguments

| Argument       | Required | Description |
|----------------|----------|-------------|
| `source`       | Yes      | Path to the image directory (images are scanned recursively) |
| `watermark`    | Yes      | Path to the watermark image (preferably a transparent PNG, e.g. `watermark-light.png`) |
| `--output`     | No       | Path to output directory. If not provided, images will be overwritten in-place |
| `--location`   | No       | Position of watermark: `topleft`, `topright`, `bottomleft`, `bottomright`, or `center`. Default: `center` |
| `--margin`     | No       | Number of pixels between the watermark and the edge of the image. Default: `0` |
| `--scale`      | No       | Percentage of the image's shortest side to use as the watermark width. Default: `20` |
| `--gui`        | No       | Launches the graphical interface (GUI) |

---

## Watermark Position Options

You can specify where the watermark should be placed on each image using the `--location` flag:

- `topleft`: Top-left corner
- `topright`: Top-right corner
- `bottomleft`: Bottom-left corner
- `bottomright`: Bottom-right corner
- `center`: Center of the image (default)

Example:
```bash
--location bottomright
```

---

## Example Command

```bash
python3 watermark_tool.py ./images ./watermark-light.png --location bottomright --output ./watermarked --margin 15 --scale 40
```

This will:
- Search `./images` for all `.jpg`, `.jpeg`, and `.png` images recursively
- Add the watermark in the bottom right corner
- Apply 15 pixels of padding between the watermark and the image edge
- Scale the watermark to 40% of the image's shortest side
- Save all processed images into the `./watermarked` directory
- Preserve the folder structure

---

## Input and Output Folder Example

Input folder:
```
./images/
├── photo1.jpg
├── photo2.png
└── album/
    └── vacation.png
```

After running the tool:
```
./watermarked/
├── photo1.png
├── photo2.png
└── album/
    └── vacation.png
```

Each image in the output will have the watermark applied in your selected position.

---

## Notes

- Compatible with macOS, Linux, and Windows. On Windows, use correct path formats (e.g., double backslashes `\\` or raw strings).
- For best results, use a transparent `.png` file as your watermark.
- Use `watermark-light.png` on dark images and `watermark-dark.png` on light ones for better visibility.
- Always test on copies of your images to avoid accidental loss or overwrite.

---

## Support

If you need assistance, want a new feature, or encounter an issue, please reach out to:

**Tejas Tagra**  
Email: [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)  
Phone: +61 6125 4265