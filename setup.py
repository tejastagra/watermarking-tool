import os
from setuptools import setup, find_packages

setup(
    name='aquamark',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'aquamark=watermarker_tool:run_cli',
        ],
    },
    include_package_data=True,
    author='Tejas Tagra',
    author_email='tejas.tagra@anu.edu.au',
    description='A CLI and GUI tool for watermarking images and videos using light/dark detection.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Multimedia :: Video',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Environment :: X11 Applications :: GTK',
    ],
    python_requires='>=3.6',
)
