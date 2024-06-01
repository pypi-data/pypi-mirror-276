
from setuptools import setup, find_packages


setup(
    name="face_genius",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "face_recognition",
        "numpy"
    ],
    author="Victor Tkachev",
    author_email="vic.tkachev@gmail.com",
    description="A simple face recognition example package",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NeuronsUII/LizaAlert_n",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
