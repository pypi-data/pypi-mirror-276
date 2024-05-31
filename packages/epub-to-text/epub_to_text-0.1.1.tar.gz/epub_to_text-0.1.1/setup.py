from setuptools import setup, find_packages
import os

# Read the contents of README.md
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='epub_to_text',
    version='0.1.1',
    description='A Python package to extract text from EPUB files',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'ebooklib==0.17.1',
        'beautifulsoup4==4.9.3',
        'markdown==3.3.4'
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
