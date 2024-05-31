import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube_video_analyzer",
    version="0.3.3",
    author="Cornelius Vincent",
    author_email="pro.cornelius@gmail.com",
    description="A package for downloading YouTube videos, extracting audio and frames, and analyzing sound intervals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cornelius-BobCat/package-video-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pytube",
        "moviepy",
        "librosa",
        "imageio",
        "numpy",
        "opencv-python",
    ],
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
