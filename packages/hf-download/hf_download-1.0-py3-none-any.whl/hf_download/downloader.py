import os
import logging
from huggingface_hub import hf_hub_download
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(repo_id, filename):
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        logger.error("HF_TOKEN environment variable is not set.")
        return

    try:
        logger.info(f"Starting download for {filename} from {repo_id}")
        # Use the API token directly for authentication
        file_path = hf_hub_download(repo_id=repo_id, filename=filename, use_auth_token=hf_token)
        logger.info(f"File downloaded to {file_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Hugging Face File Downloader")
    parser.add_argument("repo_id", help="Hugging Face repository ID (e.g., user/repo)")
    parser.add_argument("filename", help="File name to download (e.g., model.pth)")
    args = parser.parse_args()
    download_file(args.repo_id, args.filename)

if __name__ == "__main__":
    main()
