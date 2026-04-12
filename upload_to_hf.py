from huggingface_hub import HfApi
import os

# Put your Hugging Face Access Token here
TOKEN = os.getenv("HF_TOKEN")

repo_id = "jaideep-1579/innovatrix-env"

api = HfApi(token=TOKEN)

try:
    api.delete_file("tasks", repo_id=repo_id, repo_type="space")
    print("Deleted conflicting 'tasks' file on Hugging Face.")
except Exception:
    pass

print("Starting direct API upload of the tasks folder...")

api.upload_folder(
    folder_path="tasks",
    path_in_repo="tasks",
    repo_id=repo_id,
    repo_type="space"
)

print(f"Success! The tasks folder has been completely uploaded to {repo_id}")
