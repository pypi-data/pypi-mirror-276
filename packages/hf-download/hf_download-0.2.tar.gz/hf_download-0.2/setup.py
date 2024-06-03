from setuptools import setup, find_packages

setup(
    name="hf_download",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "huggingface_hub",
    ],
    entry_points={
        "console_scripts": [
            "hf_download=hf_download.downloader:main",
        ],
    },
    author="jfk",
    author_email="fumikazu.kiyota@gmail.com",
    description="A tool to download models from Hugging Face",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jfk/huggingface_downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
