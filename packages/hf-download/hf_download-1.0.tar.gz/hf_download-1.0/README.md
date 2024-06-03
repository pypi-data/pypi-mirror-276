# Hugging Face Downloader

A tool to download models from Hugging Face.

## Link to PyPI

You can find this package on PyPI: [hf_download](https://pypi.org/project/hf_download/)

## Installation

```bash
pip install hf_download
```

## Usage

```bash
hf_download user/repo filename
```

## Obtaining a Hugging Face Token

1. Go to the [Hugging Face website](https://huggingface.co/).
2. Log in to your account or create a new one.
3. Navigate to your profile settings.
4. Under the "Access Tokens" section, create a new token.
5. Copy the generated token.

Now, set the token as an environment variable:

## Setting Up Environment Variables

### Linux/MacOS

```bash
export HF_TOKEN=your_huggingface_token_here
```

### Windows

```cmd
set HF_TOKEN=your_huggingface_token_here
```
