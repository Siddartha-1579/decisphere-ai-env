from huggingface_hub import HfApi
import os

TOKEN = os.getenv("HF_TOKEN")
repo_id = "jaideep-1579/innovatrix-env"
api = HfApi(token=TOKEN)

ignore_patterns = [".git/*", ".github/*", "__pycache__/*", "*.pyc", "push_all.py", "upload_to_hf.py", ".venv/*", "uv.lock"]

api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=ignore_patterns
)

print(f"Success! All files have been uploaded to {repo_id}")
