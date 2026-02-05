"""
PR Analyzer - Main Orchestrator

This is the entry point for the CI/CD pipeline.
It coordinates the diff extraction, analysis, and commenting.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from diff_extractor import DiffExtractor
from code_analyzer import CodeAnalyzer
from github_commenter import GitHubCommenter


class PRAnalyzer:
    """Main orchestrator for PR analysis."""
    
    def __init__(
        self,
        github_token: str,
        openai_api_key: str,
        repo: str
    ):
        """
        Initialize the PR analyzer.
        
        Args:
            github_token: GitHub API token
            openai_api_key: OpenAI API key
            repo: Repository in format 'owner/repo'
        """
        self.repo = repo
        self.diff_extractor = DiffExtractor(github_token, repo)
        self.code_analyzer = CodeAnalyzer(openai_api_key)
        self.github_commenter = GitHubCommenter(github_token, repo)
    
    def analyze_pr(self, pr_number: int, full_analysis: bool = True) -> dict:
        """
        Run complete analysis on a pull request.
        
        Args:
            pr_number: The pull request number
            full_analysis: If True, run all analyses. If False, security only.
            
        Returns:
            Result dict with status and details
        """
        print(f"\n🔍 Analyzing PR #{pr_number} in {self.repo}...")
        
        # Step 1: Get PR info
        try:
            pr_info = self.diff_extractor.get_pr_info(pr_number)
            pr_title = pr_info["title"]
            print(f"📋 PR Title: {pr_title}")
        except Exception as e:
            return {"success": False, "error": f"Failed to get PR info: {e}"}
        
        # Step 2: Get changed Python files
        try:
            changed_files = self.diff_extractor.get_pr_files(pr_number)
            print(f"📁 Found {len(changed_files)} Python file(s) to analyze")
            
            if not changed_files:
                # No Python files changed - post a simple comment
                self.github_commenter.post_comment(
                    pr_number,
                    "## ✅ AI Code Review\n\nNo Python files were changed in this PR. Skipping analysis."
                )
                return {"success": True, "files_analyzed": 0, "message": "No Python files to analyze"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get changed files: {e}"}
        
        # Step 3: Analyze each file
        analyses = []
        has_critical = False
        has_high = False
        
        for file in changed_files:
            if not file.content:
                print(f"  ⚠️ Could not get content for {file.filename}, skipping...")
                continue
            
            print(f"  🔍 Analyzing {file.filename}...")
            
            try:
                if full_analysis:
                    result = self.code_analyzer.analyze_file(file.filename, file.content)
                else:
                    result = self.code_analyzer.analyze_security_only(file.filename, file.content)
                
                analyses.append(result)
                
                if result.has_critical_issues:
                    has_critical = True
                    print(f"    🔴 CRITICAL issues found!")
                if result.has_high_issues:
                    has_high = True
                    print(f"    🟠 HIGH issues found!")
                    
            except Exception as e:
                print(f"    ❌ Error analyzing {file.filename}: {e}")
        
        # Step 4: Format and post comment
        if analyses:
            print(f"\n📝 Posting analysis results to PR...")
            
            comment_body = self.github_commenter.format_analysis_comment(
                analyses=analyses,
                pr_title=pr_title,
                has_critical=has_critical,
                has_high=has_high
            )
            
            result = self.github_commenter.post_comment(pr_number, comment_body)
            
            if result.success:
                print(f"✅ Comment posted: {result.comment_url}")
            else:
                print(f"❌ Failed to post comment: {result.error}")
                return {"success": False, "error": result.error}
        
        # Step 5: Return status
        return {
            "success": True,
            "files_analyzed": len(analyses),
            "has_critical": has_critical,
            "has_high": has_high,
            "pr_title": pr_title
        }


def main():
    """Main entry point for CI/CD."""
    parser = argparse.ArgumentParser(description="AI-Powered PR Analyzer")
    parser.add_argument("--pr", "-p", type=int, required=True, help="PR number to analyze")
    parser.add_argument("--repo", "-r", type=str, help="Repository (owner/repo)")
    parser.add_argument("--security-only", action="store_true", help="Run security scan only")
    parser.add_argument("--fail-on-critical", action="store_true", help="Exit with code 1 if critical issues found")
    
    args = parser.parse_args()
    
    # Get configuration from environment
    github_token = os.environ.get("GITHUB_TOKEN")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "ajay-arram0101/development_workflow_automation")
    
    # Validate
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        sys.exit(1)
    
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        sys.exit(1)
    
    # Run analysis
    analyzer = PRAnalyzer(github_token, openai_api_key, repo)
    result = analyzer.analyze_pr(args.pr, full_analysis=not args.security_only)
    
    # Print summary
    print("\n" + "="*50)
    print("📊 ANALYSIS SUMMARY")
    print("="*50)
    
    if result["success"]:
        print(f"✅ Successfully analyzed {result['files_analyzed']} file(s)")
        
        if result.get("has_critical"):
            print("🔴 CRITICAL security issues found!")
            if args.fail_on_critical:
                print("⛔ Failing build due to --fail-on-critical flag")
                sys.exit(1)
        elif result.get("has_high"):
            print("🟠 HIGH severity issues found - review recommended")
        else:
            print("✅ No critical or high severity issues")
    else:
        print(f"❌ Analysis failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
