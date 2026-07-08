from langchain_core.tools import tool

@tool
def get_latest_commit(repo_name: str) -> dict:
    """Get the latest commit message for a repository/service."""
    repo = repo_name.lower()
    if "payment" in repo:
        return {
            "latest_commit": "changed payment config"
        }
    return {
        "latest_commit": "update readme"
    }
