from setuptools import setup, find_packages

setup(
    name="DCMake",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "tqdm>=4.66.4"
    ],
    entry_points={
        "console_scripts": [
            "dcmake=dcmake:main",
        ],
    },
    author="Tietu",
    author_email="yhy2637@163.com",
    description="Download github repository to CMake Project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires=">=3.11",
)
