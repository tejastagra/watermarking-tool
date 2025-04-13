# 📸 Watermarker Tool by Sequeira Lab

This repository belongs to the **Sequeira Lab**.  
This program was created by **Tejas Tagra (u7786686)**.  
Do not modify this code or use it elsewhere without the written permission of the author.  
Please contact [tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au) for maintenance requests, bugs, or more info.

---

## ⚡ About This Tool

This is a Python-based watermarking tool built from scratch to help you apply a custom logo to batches of images inside a folder — including all subfolders. You can customize the logo’s position, size, and padding. You can also choose whether to overwrite the original images or output to a new folder, all while keeping the folder structure intact.

---

## ✅ Features

- Recursively scans folders and subfolders for images
- Supports `.jpg`, `.jpeg`, and `.png` formats
- Custom watermark placement: any corner or center
- Logo scales proportionally to each image
- Optional padding around the watermark
- Maintains original folder structure if saving elsewhere
- Lightweight and runs fully offline

---

## ⚙️ Requirements

### Python 3.x

Make sure Python is installed. If not:

👉 [Download Python](https://www.python.org/downloads/)

### Pillow (Python Imaging Library)

Install it via pip:

```bash
pip install pillow
```

---

## 🚀 How to Use

### 📦 Installation (Local CLI Tool)

If you're using the CLI version with `setup.py`, navigate to the root folder and install it:

```bash
pip3 install .
```

Then you can run the tool anywhere using:

```bash
watermarker <ImageDirectory> <LogoPath> [options]
```

### 🧪 Or, Run Manually

If you prefer not to install:

```bash
python3 -m watermarker <ImageDirectory> <LogoPath> [options]
```

---

## 🔢 Command-Line Options

| Argument       | Required | Description |
|----------------|----------|-------------|
| `source`       | ✅        | Path to the folder containing your images |
| `logo`         | ✅        | Path to the watermark logo image (preferably PNG with transparency) |
| `--output`     | ❌        | Output folder for watermarked images (preserves folder structure). If not set, overwrites originals |
| `--location`   | ❌        | Watermark position. Default: `center` |
| `--margin`     | ❌        | Padding in pixels around the logo. Default: `0` |
| `--scale`      | ❌        | Logo size as percentage of the image’s shortest side. Default: `20` |

---

## 🔍 Watermark Positions

You can place the watermark at any of the following positions:

- `topleft`
- `topright`
- `bottomleft`
- `bottomright`
- `center` *(default)*

Example:

```bash
--location bottomright
```

---

## 💡 Example Usage

```bash
watermarker ./images ./logo-light.png --location bottomright --output ./watermarked --margin 15 --scale 25
```

This will:

- Recursively watermark all `.jpg`, `.jpeg`, and `.png` images in `./images`
- Place the watermark at the bottom right with 15px margin
- Scale the watermark to 25% of the image’s shorter side
- Save everything inside `./watermarked/`, preserving original folder structure

---

## 📂 Folder Structure Example

Input:

```
./images/
├── photo1.jpg
├── photo2.png
└── album/
    └── vacation.jpeg
```

Command:

```bash
watermarker ./images ./logo.png --location bottomright --output ./watermarked --scale 25
```

Output:

```
./watermarked/
├── photo1.jpg
├── photo2.png
└── album/
    └── vacation.jpeg
```

All with the watermark applied.

---

## ⚠️ Notes

- Works on macOS, Linux, and Windows (though you may need to adjust path syntax on Windows).
- Recommended logo format: `.png` with transparency.
- For production use, test on copies of your images first.

---

## 📬 Support

If something isn’t working or if you’d like a feature added, reach out directly:

**Tejas Tagra**  
[tejas.tagra@anu.edu.au](mailto:tejas.tagra@anu.edu.au)  
+61 6125 4265

---

