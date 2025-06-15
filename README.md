### Watermarking Tool v1.2 – macOS and Windows Release

**Release Date:** June 15, 2025
**Build Types:**

* macOS: Directory-based application (GUI app included in release)
* Windows: Single-file executable (GUI app included in release)

---

#### What's New

* Introduced standalone GUI apps for both macOS and Windows in the release section
* macOS version now uses a directory-based build with `--windowed` for faster startup
* Added Windows support with a PyInstaller-built `.exe` file
* Full offline functionality on both platforms
* Intelligent watermark selection (light/dark) based on image brightness
* Support for image and video watermarking via GUI or CLI

---

#### Included in This Release

* `WatermarkingTool-macOS.zip`: Contains the full application folder. Unzip and run `watermarker_tool` inside. GUI launches automatically.
* `WatermarkingTool-Windows.exe`: Standalone executable for Windows. No installation required. GUI launches on double-click.

---

#### Notes

* Do not separate files inside the macOS app folder. All contents are required for the app to function.
* The Windows `.exe` may take slightly longer to launch on first run due to onefile packaging.
* CLI functionality is also retained in the Python source code version.

---

## Documentation

# Watermarking Tool

This program was created by **Tejas Tagra** under the employment of The Australian National University, Canberra.
Developed for the **Statistical Modelling & Marine Megafauna Movement at The Research School of Biology**.

Please contact [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au) for maintenance requests, bugs, or more information.

---

## About

The **Watermarking Tool** is a Python-based utility for watermarking both **images** and **videos**. It supports a graphical interface (GUI) and a command-line interface (CLI) for flexibility and ease of use.

### Key Features

* Automatically selects light or dark watermark based on background brightness
* Batch watermarking for image folders (including subfolders)
* Video watermarking applied frame-by-frame
* Customizable watermark position, size, and margins
* Option to preserve original folder structure
* Option to overwrite images or export to a different folder
* Cross-platform support (macOS and Windows)
* GUI available in latest releases (no Python required)

---

## Technical Specs

* Works fully offline
* Supported image formats: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`
* Supported video formats: `.mp4`, `.avi`, `.mov`, `.mkv`
* Output formats:

  * Images: `.png`
  * Videos: `.mp4`
* Built-in GUI with back navigation, mode selection, and progress tracking

---

## Requirements (for Python source users)

**Python 3.6 or later**
Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)

Install dependencies with:

```bash
pip3 install -r requirements.txt
```

Or manually:

```bash
pip3 install pillow opencv-python pillow-heif
```

---

## How to Use

### GUI Mode (included in release binaries)

Just unzip and run:

* `watermarker_tool` on macOS
* `WatermarkingTool-Windows.exe` on Windows

No Python required for these versions.

### GUI Mode (from Python source)

```bash
python3 watermarker_tool.py --gui
```

The GUI will prompt you to:

* Select image folder or video file
* Add watermark images (light and dark)
* Choose an output folder (optional)
* Set watermark position, margin, and scale

If no output folder is selected, images are overwritten (as `.png`), and videos get `_watermarked.mp4`.

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

* Use transparent `.png` watermarks for best visual results
* Always back up your originals before batch processing
* GUI provides progress feedback and is recommended for most users
* CLI remains useful for automation, scripting, and batch workflows

---

## Support

For issues, feedback, or feature requests:

**Tejas Tagra**
Email: [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)
