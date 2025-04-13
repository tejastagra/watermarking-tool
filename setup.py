from setuptools import setup, find_packages

setup(
    name='watermarker',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'watermarker=watermarker.__main__:main',
        ],
    },
    author='Tejas Tagra',
    author_email='tejas.tagra@anu.edu.au',
    description='CLI tool to watermark images in bulk using a custom logo.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
