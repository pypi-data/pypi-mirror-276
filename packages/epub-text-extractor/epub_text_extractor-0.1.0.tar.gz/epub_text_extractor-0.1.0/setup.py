# setup.py
from setuptools import setup, find_packages

setup(
    name='epub_text_extractor',
    version='0.1.0',
    description='A Python package to extract text from EPUB files',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'ebooklib',
        'beautifulsoup4',
        'markdown'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'epub-extract=epub_text_extractor.cli:main',
        ],
    },
)
