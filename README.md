# AquaMark: Image & Video Watermarking Tool

This program was created by **Tejas Tagra (u7786686)**.
Please contact [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au) for maintenance requests, bugs, or more information.

---

## About This Tool

**AquaMark** is a Python-based watermarking utility that supports both **images** and **videos**. Designed for simplicity and flexibility, it provides both a command-line interface (CLI) and a user-friendly graphical interface (GUI).

With AquaMark, you can:

* Automatically choose the light or dark watermark based on background brightness
* Watermark images in bulk (including subfolders)
* Watermark video files frame-by-frame
* Customize watermark position, size, and margin
* Choose between overwriting originals or saving to a separate output directory

---

## Key Features

* CLI and GUI support
* Batch image watermarking
* Video watermarking (frame-by-frame)
* Automatic brightness detection (light/dark watermark)
* Preserves original folder structure
* Fully offline; no internet required
* Supports:

  * Images: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`
  * Videos: `.mp4`, `.avi`, `.mov`, `.mkv`
* Output: `.png` for images, `.mp4` for videos
* Built-in GUI navigation with back button and mode selection

---

## Requirements

### Python 3.6 or later

Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Required Libraries

All dependencies are listed in the `requirements.txt` file. To install them, simply run:

```bash
pip3 install -r requirements.txt
```

If you'd prefer to install them manually, you can use:

```bash
pip3 install pillow opencv-python
```

---

## How to Use

### Option 1: GUI Mode

Run the following command to launch the graphical interface:

```bash
python3 watermarker_tool.py --gui
```

The GUI will guide you through the process:

* Choose to watermark **images** or a **video file**
* Provide the source folder (for images) or file (for video)
* Provide paths to the light and dark watermark images
* Set the output directory
* Choose the watermark position (Centre, Top left, Top right, Bottom left, Bottom right)
* Adjust margin and scale

You can return to the main menu at any time to switch between image and video modes.

If no output directory is specified, AquaMark will save over the original images (converted to `.png`) or append `_watermarked.mp4` for videos.

---

### Option 2: CLI Mode

Run the script directly via command-line:

```bash
python3 watermarker_tool.py <source> <light_wm> <dark_wm> [options]
```

#### Example:

```bash
python3 watermarker_tool.py ./images ./light.png ./dark.png \
  --output ./out --location bottomright --margin 15 --scale 40
```

This will recursively watermark all images and videos found in `./images`.

---

## Command-Line Options

| Argument     | Required | Description                                                                      |
| ------------ | -------- | -------------------------------------------------------------------------------- |
| `source`     | Yes      | Path to folder (images) or file (video)                                          |
| `light`      | Yes      | Path to light watermark (for dark backgrounds)                                   |
| `dark`       | Yes      | Path to dark watermark (for light backgrounds)                                   |
| `--output`   | No       | Output folder path (defaults to source if not specified)                         |
| `--location` | No       | Watermark position: `topleft`, `topright`, `bottomleft`, `bottomright`, `center` |
| `--margin`   | No       | Padding in pixels from image edge (default: 15)                                  |
| `--scale`    | No       | Watermark size as a percentage of the image's shortest side (default: 40)        |
| `--gui`      | No       | Launch the graphical interface instead of CLI                                    |

---

## Image Input and Output Example

Input folder:

```
./images/
├── photo1.jpg
├── photo2.png
└── album/
    └── vacation.png
```

After watermarking:

```
./out/
├── photo1.png
├── photo2.png
└── album/
    └── vacation.png
```

---

## Video Input and Output Example

Input file:

```
./videos/trailer.mov
```

After watermarking:

```
./out/trailer_watermarked.mp4
```

---

## Notes

* Cross-platform: supports macOS, Windows, and Linux
* Use transparent `.png` files for best watermark results
* Automatic watermark selection based on background brightness
* For video watermarking, AquaMark applies the watermark to each frame
* Always back up your original files before overwriting

---

## Support

If you encounter any issues, require a feature, or want to suggest an improvement, please contact:

**Tejas Tagra**
Email: [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)
Phone: +61 6125 4265