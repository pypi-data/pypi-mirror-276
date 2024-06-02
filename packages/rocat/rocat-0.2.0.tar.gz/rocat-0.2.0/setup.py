# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rocat",
    version="0.2.0",
    description="A simple and user-friendly library for AI services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YumetaLab",
    author_email="root@yumeta.kr",
    url="https://github.com/Yumeta-Lab/rocat-dev",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "altair==5.3.0",
        "anthropic==0.26.1",
        "beautifulsoup4==4.12.3",
        "docx2txt==0.8",
        "google_search_results==2.4.2",
        "openai==1.30.3",
        "openpyxl==3.1.2",
        "pandas==2.2.2",
        "pillow==10.3.0",
        "PyPDF2==3.0.1",
        "python-docx==1.1.2",
        "python-pptx==0.6.23",
        "requests==2.32.2",
        "serpapi==0.1.5",
        "xlrd==2.0.1",
        "XlsxWriter==3.2.0",
        "youtube-transcript-api==0.6.2",
    ],
    entry_points={
        'console_scripts': [
            'rocat=rocat.__main__:main',
        ],
    },
    package_data={
        "": ["*.py"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
