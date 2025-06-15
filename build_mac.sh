#!/bin/bash

echo "🧹 Cleaning old builds..."
rm -rf build dist *.spec

echo "⚡ Building fast-start macOS app..."
pyinstaller --windowed watermarker_tool.py

cd dist || exit

echo "📦 Zipping app directory..."
zip -r WatermarkingTool-macOS.zip watermarker_tool

cd ..
echo "✅ Fast-start build ready: dist/WatermarkingTool-macOS.zip"
