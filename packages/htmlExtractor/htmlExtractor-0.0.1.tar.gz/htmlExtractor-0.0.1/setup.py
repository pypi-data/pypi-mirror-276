from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='htmlExtractor',
    version='0.0.1',  # Incremented version number for updates
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    author='Md Anisur Rahman',
    author_email='anisurrahman06046@gmail.com',
    description='A simple package to fetch HTML data from a website',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/AnisurRahman06046/fetchHtml_website.git',  # Your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)