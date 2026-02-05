"""
GitHub Commenter - Post analysis results as PR comments
"""

import os
import requests
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CommentResult:
    """Result of posting a comment."""
    success: bool
    comment_url: Optional[str] = None
    error: Optional[str] = None


class GitHubCommenter:
    """Post comments to GitHub Pull Requests."""
    
    def __init__(self, github_token: str, repo: str):
        """
        Initialize the commenter.
        
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
    
    def post_comment(self, pr_number: int, body: str) -> CommentResult:
        """
        Post a comment to a pull request.
        
        Args:
            pr_number: The pull request number
            body: Comment body in markdown
            
        Returns:
            CommentResult with success status
        """
        url = f"{self.api_base}/repos/{self.repo}/issues/{pr_number}/comments"
        
        payload = {"body": body}
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            return CommentResult(
                success=True,
                comment_url=data.get("html_url")
            )
        else:
            return CommentResult(
                success=False,
                error=f"Failed to post comment: {response.status_code} - {response.text}"
            )
    
    def format_analysis_comment(
        self,
        analyses: list,
        pr_title: str,
        has_critical: bool,
        has_high: bool
    ) -> str:
        """
        Format analysis results into a PR comment.
        
        Args:
            analyses: List of AnalysisResult objects
            pr_title: Title of the PR
            has_critical: Whether any file has critical issues
            has_high: Whether any file has high issues
            
        Returns:
            Formatted markdown comment
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Header with status
        if has_critical:
            status_emoji = "🚨"
            status_text = "CRITICAL ISSUES FOUND"
            status_color = "red"
        elif has_high:
            status_emoji = "⚠️"
            status_text = "HIGH SEVERITY ISSUES FOUND"
            status_color = "orange"
        else:
            status_emoji = "✅"
            status_text = "No Critical Issues"
            status_color = "green"
        
        comment = f"""## {status_emoji} AI Code Review - {status_text}

> **PR:** {pr_title}  
> **Scanned:** {len(analyses)} Python file(s)  
> **Time:** {timestamp}

---

"""
        
        # Add analysis for each file
        for analysis in analyses:
            comment += f"""### 📄 `{analysis.filename}`

<details>
<summary>🔒 Security Analysis</summary>

{analysis.security}

</details>

<details>
<summary>📊 Code Quality</summary>

{analysis.quality}

</details>

<details>
<summary>📋 Migration Assessment</summary>

{analysis.migration}

</details>

<details>
<summary>🔧 Refactoring Suggestions</summary>

{analysis.refactoring}

</details>

---

"""
        
        # Footer with merge guidance
        if has_critical:
            comment += """
## ⛔ Merge Recommendation

**Critical security issues were found.** Please address these before merging:

- [ ] Review and fix all 🔴 CRITICAL findings
- [ ] Review and fix all 🟠 HIGH findings
- [ ] Re-run the security scan

<details>
<summary>🤔 Need help fixing these issues?</summary>

Run the refactoring tool locally:
```bash
python ai_code_analyzer.py --file <your-file> --refactor
```

</details>
"""
        elif has_high:
            comment += """
## ⚠️ Merge Recommendation

**High severity issues were found.** Consider addressing these before merging:

- [ ] Review all 🟠 HIGH findings
- [ ] Decide if fixes are needed before merge or can be addressed later

**Proceed with caution.**
"""
        else:
            comment += """
## ✅ Merge Recommendation

No critical or high severity issues found. **Safe to proceed with merge** after standard code review.

<details>
<summary>💡 Pro tip</summary>

Even without critical issues, consider reviewing the quality and refactoring suggestions for improvement opportunities.

</details>
"""
        
        comment += f"""

---
<sub>🤖 Powered by AI Code Analyzer | [View Documentation](https://github.com/{self.repo})</sub>
"""
        
        return comment


if __name__ == "__main__":
    # Test locally
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        commenter = GitHubCommenter(token, "ajay-arram0101/development_workflow_automation")
        print("GitHubCommenter ready!")
    else:
        print("Set GITHUB_TOKEN to test")
