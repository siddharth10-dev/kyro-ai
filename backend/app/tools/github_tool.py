import subprocess
from langchain_core.tools import tool

@tool
def get_latest_commit(repo_name: str) -> dict:
    """Get the latest commit message and modified files for the repository to check what changed recently."""
    try:
        # Get the latest commit hash, author, message, and list of changed files
        cmd = ["git", "log", "-n", "1", "--name-only", "--pretty=format:%H|%an|%s"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        output = res.stdout.strip()
        if not output:
            return {"latest_commit": "No commits found", "changed_files": []}
            
        lines = output.splitlines()
        header = lines[0].split("|")
        commit_hash = header[0]
        author = header[1]
        message = header[2]
        changed_files = [line.strip() for line in lines[1:] if line.strip()]
        
        return {
            "latest_commit": f"[{commit_hash[:7]}] {message} (by {author})",
            "changed_files": changed_files
        }
    except Exception as e:
        return {
            "latest_commit": f"Error querying git repository: {str(e)}",
            "changed_files": []
        }
