from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="manim-progress-bar",
    version="0.2.0",
    author="Zhiku Zhang",
    author_email="zhangzk1205@163.com",
    description="A customizable progress bar component for Manim animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangzk-code/manim-progress-bar",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords="manim, animation, progress-bar, progress, bar",
    project_urls={
        "Bug Reports": "https://github.com/zhangzk-code/manim-progress-bar/issues",
        "Source": "https://github.com/zhangzk-code/manim-progress-bar",
    },
)
