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

---

## Requirements

### Python 3.6

Ensure Python 3 is installed. You can download it from:
https://www.python.org/downloads/

### Required Library: Pillow

This tool uses the Pillow library for image processing. Install it using pip:

```bash
pip3 install pillow
```

---

## How to Use

### Installation as CLI Tool

If you're installing it using the provided `setup.py`, run:

```bash
pip3 install .
```

Once installed, you can execute the tool anywhere using:

```bash
watermarker <ImageDirectory> <WatermarkPath> [options]
```
### Uninstall the CLI Tool

To remove the installed command-line version of this tool, run:

```bash
pip3 uninstall watermarker
```

### Run Without Installing

Alternatively, run it directly as a script:

```bash
python3 -m watermarker <ImageDirectory> <WatermarkPath> [options]
```

---

## Command-Line Arguments

| Argument       | Required | Description |
|----------------|----------|-------------|
| `source`       | Yes      | Path to the image directory (images are scanned recursively) |
| `watermark`    | Yes      | Path to the watermark image (preferably a transparent PNG, e.g. `watermark-light.png` or `watermark-dark.png`) |
| `--output`     | No       | Path to output directory. If not provided, images will be overwritten in-place |
| `--location`   | No       | Position of watermark: `topleft`, `topright`, `bottomleft`, `bottomright`, or `center`. Default: `center` |
| `--margin`     | No       | Number of pixels between the watermark and the edge of the image. Default: `0` |
| `--scale`      | No       | Percentage of the image's shortest side to use as the watermark width. Default: `20` |

---

## Watermark Position Options

You can specify where the watermark should be placed on each image using the `--location` flag:

- `topleft`: Top-left corner
- `topright`: Top-right corner
- `bottomleft`: Bottom-left corner
- `bottomright`: Bottom-right corner
- `center`: Center of the image (default if none specified)

Example usage:

```bash
--location bottomright
```

---

## Example Command

```bash
python3 -m watermarker ./images ./watermark-light.png --location bottomright --output ./watermarked --margin 15 --scale 40
```

This will:
- Search `./images` for all `.jpg`, `.jpeg`, and `.png` images recursively
- Add the watermark in the bottom right corner
- Apply 15 pixels of padding between the watermark and the image edge
- Scale the watermark to 25% of the image's shortest side
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

Running:
```bash
python3 -m watermarker ./images ./watermark-light.png --location bottomright --output ./watermarked --scale 40
```

Output folder:
```
./watermarked/
├── photo1.png
├── photo2.png
└── album/
    └── vacation.png
```

Each image in the output will have the watermark applied.

---

## Notes

- Compatible with macOS, Linux, and Windows. On Windows, make sure paths are in the correct format (e.g. use `\` or raw strings).
- For best results, use a `.png` watermark with a transparent background.
- Use `watermark-light.png` for dark image backgrounds and `watermark-dark.png` for light image backgrounds to ensure visibility.
- Always test with copies before applying watermarks to critical or original files.

---

## Support

If you need assistance, want a new feature, or encounter an issue, please reach out to:

**Tejas Tagra**  
Email: [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)  
Phone: +61 6125 4265

---
