# Watermarking Tool

This program was created by **Tejas Tagra (u7786686)** under the employment of The Australian National University, Canberra.
Developed for the **Statistical Modelling & Marine Megafauna Movement at The Research School of Biology**.

Please contact [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au) for maintenance requests, bugs, or more information.

---

## About

The **Watermarking Tool** is a Python-based utility for watermarking both **images** and **videos**. It supports a graphical interface (GUI) and a command-line interface (CLI) for flexibility and ease of use.

### What it can do:

* Automatically choose a light or dark watermark based on background brightness
* Watermark images in bulk (including subfolders)
* Apply watermarks to video files frame-by-frame
* Customize watermark position, size, and margins
* Preserve original folder structures
* Choose between overwriting or exporting to a different folder

---

## Technical Specs

* Fully offline; no internet required
* Supports:

  * Image formats: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`
  * Video formats: `.mp4`, `.avi`, `.mov`, `.mkv`
* Output:

  * Images: `.png`
  * Videos: `.mp4`
* Cross-platform: macOS, Windows, Linux
* Built-in GUI with back button and mode selection

---

## Requirements

**Python 3.6 or later**
Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

To install dependencies:

```bash
pip3 install -r requirements.txt
```

Or manually:

```bash
pip3 install pillow opencv-python
```

---

## How to Use

### GUI Mode

Launch with:

```bash
python3 watermarker_tool.py --gui
```

The GUI will prompt you to:

* Select image folder or video file
* Add watermark images (light/dark)
* Choose output folder (optional)
* Set watermark location, margin, and scale

If no output folder is selected, images will be overwritten (as `.png`), and videos will get `_watermarked.mp4`.

---

### CLI Mode

```bash
python3 watermarker_tool.py <source> <light_wm> <dark_wm> [options]
```

**Example:**

```bash
python3 watermarker_tool.py ./images ./light.png ./dark.png \
  --output ./out --location bottomright --margin 15 --scale 40
```

---

## Command-Line Options

| Argument     | Required | Description                                                                      |
| ------------ | -------- | -------------------------------------------------------------------------------- |
| `source`     | Yes      | Folder path (images) or file path (video)                                        |
| `light`      | Yes      | Light watermark (for dark backgrounds)                                           |
| `dark`       | Yes      | Dark watermark (for light backgrounds)                                           |
| `--output`   | No       | Output folder path (defaults to source if not specified)                         |
| `--location` | No       | Watermark position: `topleft`, `topright`, `bottomleft`, `bottomright`, `center` |
| `--margin`   | No       | Padding from image edge in pixels (default: 15)                                  |
| `--scale`    | No       | Size as % of image's shortest side (default: 40)                                 |
| `--gui`      | No       | Launch GUI instead of CLI                                                        |

---

## Example Input and Output

### Images

```
Input:
./images/photo1.jpg
./images/album/vacation.png

Output:
./out/photo1.png
./out/album/vacation.png
```

### Videos

```
Input:  ./videos/trailer.mov  
Output: ./out/trailer_watermarked.mp4
```

---

## Notes

* Use transparent `.png` watermarks for best results
* Always back up your originals
* Automatically selects watermark type based on brightness
* For videos, watermark is applied frame-by-frame

---

## Support

For issues, feedback, or feature requests:

**Tejas Tagra**
Email: [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)
Phone: +61 6125 4265
