from setuptools import setup, find_packages
from pathlib import Path

root = Path(__file__).parent
long_description = (root / "docs" / "README_EN.md").read_text(encoding="utf-8")

setup(
    name="LoopHalter",
    version="1.0.0",
    author="Jacopos311",
    author_email="",
    description="AI Agent Interaction Tracker and Loop Detection Middleware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
