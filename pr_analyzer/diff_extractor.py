"""
Diff Extractor - Get changed Python files from a GitHub Pull Request
"""

import os
import requests
from typing import Optional
from dataclasses import dataclass


@dataclass
class ChangedFile:
    """Represents a changed file in a PR."""
    filename: str
    status: str  # added, modified, removed
    additions: int
    deletions: int
    patch: Optional[str]  # The diff patch
    content: Optional[str] = None  # Full file content


class DiffExtractor:
    """Extract changed files from a GitHub Pull Request."""
    
    def __init__(self, github_token: str, repo: str):
        """
        Initialize the diff extractor.
        
        Args:
            github_token: GitHub API token
            repo: Repository in format 'owner/repo'
        """
        self.github_token = github_token
        self.repo = repo
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def get_pr_files(self, pr_number: int) -> list[ChangedFile]:
        """
        Get all changed files in a pull request.
        
        Args:
            pr_number: The pull request number
            
        Returns:
            List of ChangedFile objects
        """
        url = f"{self.api_base}/repos/{self.repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        files = []
        for file_data in response.json():
            # Only include Python files
            if not file_data["filename"].endswith(".py"):
                continue
            
            # Skip deleted files
            if file_data["status"] == "removed":
                continue
            
            changed_file = ChangedFile(
                filename=file_data["filename"],
                status=file_data["status"],
                additions=file_data["additions"],
                deletions=file_data["deletions"],
                patch=file_data.get("patch", "")
            )
            
            # Get full file content for analysis
            changed_file.content = self._get_file_content(
                file_data["filename"], 
                pr_number
            )
            
            files.append(changed_file)
        
        return files
    
    def _get_file_content(self, filepath: str, pr_number: int) -> Optional[str]:
        """
        Get the full content of a file from the PR branch.
        
        Args:
            filepath: Path to the file in the repo
            pr_number: PR number to get the branch ref
            
        Returns:
            File content as string
        """
        # First get the PR to find the head branch
        pr_url = f"{self.api_base}/repos/{self.repo}/pulls/{pr_number}"
        pr_response = requests.get(pr_url, headers=self.headers)
        pr_response.raise_for_status()
        pr_data = pr_response.json()
        
        head_sha = pr_data["head"]["sha"]
        
        # Get file content at that commit
        content_url = f"{self.api_base}/repos/{self.repo}/contents/{filepath}?ref={head_sha}"
        content_response = requests.get(content_url, headers=self.headers)
        
        if content_response.status_code != 200:
            return None
        
        content_data = content_response.json()
        
        # Content is base64 encoded
        import base64
        content = base64.b64decode(content_data["content"]).decode("utf-8")
        return content
    
    def get_pr_info(self, pr_number: int) -> dict:
        """
        Get PR metadata.
        
        Args:
            pr_number: The pull request number
            
        Returns:
            PR information dict
        """
        url = f"{self.api_base}/repos/{self.repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # Test locally
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        extractor = DiffExtractor(token, "ajay-arram0101/development_workflow_automation")
        # Test with a PR number
        # files = extractor.get_pr_files(1)
        # for f in files:
        #     print(f"{f.filename}: {f.status} (+{f.additions}/-{f.deletions})")
        print("DiffExtractor ready!")
    else:
        print("Set GITHUB_TOKEN to test")
