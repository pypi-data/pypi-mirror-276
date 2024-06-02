import os
from huggingface_hub import HfApi, create_repo, upload_file

# Set your repository details
repo_name = "phi3-mini-WeatherBot"
repo_id = f"VatsalPatel18/{repo_name}"
local_dir = "../model/phi-3-gguf"

# Authenticate using the token from the environment variable
token = os.getenv("HUGGINGFACE_HUB_TOKEN")

if not token:
    raise ValueError("The Hugging Face token is not set in the environment variable.")

# Initialize the HfApi object
api = HfApi()

# Create the repository if it doesn't exist
create_repo(repo_id, token=token, exist_ok=True)

# Upload each file in the local directory
for root, dirs, files in os.walk(local_dir):
    for file in files:
        if file.startswith("."):
            # Skip hidden files and folders
            continue
        local_file_path = os.path.join(root, file)
        repo_file_path = os.path.relpath(local_file_path, local_dir)
        upload_file(
            path_or_fileobj=local_file_path,
            path_in_repo=repo_file_path,
            repo_id=repo_id,
            token=token
        )

print("Files uploaded successfully.")

