"""
Code Analyzer - Send code to OpenAI for comprehensive analysis
"""

import os
from typing import Optional
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# ANALYSIS PROMPTS (Same as ai_code_analyzer.py)
# ============================================================================

SECURITY_PROMPT = """You are a senior security engineer performing a security audit.

Analyze this code for security vulnerabilities:

```python
{code}
```

Identify ALL security issues including:
1. SQL Injection
2. Hardcoded credentials/secrets
3. Weak cryptography
4. Input validation issues
5. Information disclosure
6. Authentication flaws
7. Authorization issues

For EACH finding, provide:
- Severity: 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW
- Line number(s)
- Vulnerability type
- Description
- Secure code fix

Format as a clear security report."""


CODE_QUALITY_PROMPT = """You are a senior software architect reviewing legacy code for modernization.

Analyze this code for quality issues:

```python
{code}
```

Identify:
1. **Code Smells** - Long methods, god classes, magic numbers
2. **Outdated Patterns** - Callbacks that should be async/await, old string formatting
3. **Missing Best Practices** - No type hints, no docstrings, poor error handling
4. **SOLID Violations** - Single responsibility, dependency injection issues
5. **Testability Issues** - Tight coupling, no interfaces

For each issue:
- Location (line number)
- Issue type
- Why it's a problem
- Modern Python solution

Be specific and actionable."""


MIGRATION_PROMPT = """You are a technical lead planning a legacy code migration.

Analyze this codebase for migration to modern architecture:

```python
{code}
```

Provide a migration plan including:

## 1. Current State Assessment
- Tech debt items
- Risk areas
- Dependencies

## 2. Target Architecture
- Recommended patterns (Repository, Service Layer, etc.)
- Framework recommendations (FastAPI, SQLAlchemy, etc.)
- Testing strategy

## 3. Migration Phases
- Phase 1: Quick wins (what can be fixed immediately)
- Phase 2: Refactoring (structural changes)
- Phase 3: Modernization (new patterns/frameworks)

## 4. Effort Estimation
- Small (1-2 days)
- Medium (1 week)
- Large (2+ weeks)

## 5. Risk Mitigation
- How to migrate safely without breaking production

Be specific to THIS codebase."""


REFACTOR_PROMPT = """You are a Python modernization expert.

Refactor this legacy code to modern Python 3.11+ standards:

ORIGINAL CODE:
```python
{code}
```

Requirements:
1. Fix ALL security vulnerabilities (use parameterized queries, env vars for secrets)
2. Add type hints to all functions
3. Convert callbacks to async/await where applicable
4. Add proper error handling with specific exceptions
5. Add docstrings (Google style)
6. Break down god methods into smaller functions
7. Use dataclasses or Pydantic for data structures
8. Follow PEP 8

Suggest the TOP 3 most impactful refactoring improvements with code snippets."""


@dataclass
class AnalysisResult:
    """Result from code analysis."""
    filename: str
    security: str
    quality: str
    migration: str
    refactoring: str
    has_critical_issues: bool = False
    has_high_issues: bool = False


class CodeAnalyzer:
    """Analyze code using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Debug: Show that we have a key (masked)
        print(f"🔑 OpenAI API Key configured: {self.api_key[:8]}...{self.api_key[-4:]}")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ OpenAI API Error: {type(e).__name__}: {e}")
            raise
    
    def analyze_file(self, filename: str, code: str) -> AnalysisResult:
        """
        Run full analysis on a file.
        
        Args:
            filename: Name of the file
            code: File content
            
        Returns:
            AnalysisResult with all analysis types
        """
        # Run all analyses
        security = self._call_openai(SECURITY_PROMPT.format(code=code))
        quality = self._call_openai(CODE_QUALITY_PROMPT.format(code=code))
        migration = self._call_openai(MIGRATION_PROMPT.format(code=code))
        refactoring = self._call_openai(REFACTOR_PROMPT.format(code=code))
        
        # Check for critical/high issues in security analysis
        has_critical = "🔴 CRITICAL" in security or "CRITICAL" in security.upper()
        has_high = "🟠 HIGH" in security or "HIGH" in security.upper()
        
        return AnalysisResult(
            filename=filename,
            security=security,
            quality=quality,
            migration=migration,
            refactoring=refactoring,
            has_critical_issues=has_critical,
            has_high_issues=has_high
        )
    
    def analyze_security_only(self, filename: str, code: str) -> AnalysisResult:
        """Quick security-only scan."""
        security = self._call_openai(SECURITY_PROMPT.format(code=code))
        
        has_critical = "🔴 CRITICAL" in security or "CRITICAL" in security.upper()
        has_high = "🟠 HIGH" in security or "HIGH" in security.upper()
        
        return AnalysisResult(
            filename=filename,
            security=security,
            quality="",
            migration="",
            refactoring="",
            has_critical_issues=has_critical,
            has_high_issues=has_high
        )


if __name__ == "__main__":
    # Test locally
    analyzer = CodeAnalyzer()
    
    test_code = '''
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "'"
    return db.execute(query)
'''
    
    result = analyzer.analyze_security_only("test.py", test_code)
    print(result.security)
    print(f"Critical: {result.has_critical_issues}")
