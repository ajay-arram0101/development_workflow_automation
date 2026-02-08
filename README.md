# AI-Powered Development Workflow Automation

Automated code analysis bots that run on every Pull Request to catch security vulnerabilities, code quality issues, and provide migration recommendations — before code reaches production.

## What It Does

| Bot | Trigger | Output |
|-----|---------|--------|
| 🔒 Security Bot | PR opened | Finds SQL injection, hardcoded credentials, auth flaws |
| 📊 Quality Bot | PR opened | Detects code smells, tech debt, outdated patterns |
| 🔧 Refactor Bot | On-demand | Generates modernized code with fixes |
| 📋 Migration Bot | On-demand | Creates phased migration plan with effort estimates |

## Why Not Just Use Copilot/Amazon Q?

- **Automated** — Runs on every PR without developer action
- **Enforced** — Can block merge until issues are fixed
- **Trackable** — Produces reports with severity levels and metrics
- **Customizable** — Uses your company's coding standards

---

## Analysis Report Example

> From [PR #2](https://github.com/ajay-arram0101/development_workflow_automation/pull/2)

### 🔒 Security Vulnerabilities Found

| Severity | Issue | Location |
|----------|-------|----------|
| 🔴 CRITICAL | SQL Injection | order_service.py Line 27, 34 |
| 🔴 CRITICAL | Hardcoded Credentials | order_service.py Line 12-14 |
| 🟠 HIGH | Hardcoded SMTP Password | order_service.py Line 78 |
| 🟡 MEDIUM | No Input Validation | order_service.py Line 40 |

### 📊 Code Quality Score

**Tech Debt: 7/10 (High)**

- God method with 7 parameters
- Callback hell (4 levels deep)
- Magic numbers throughout
- Missing type hints
- No error handling

### 📋 Migration Estimate

| Phase | Tasks | Effort |
|-------|-------|--------|
| Phase 1 | Security fixes | 3 hours |
| Phase 2 | Code quality | 1 week |
| Phase 3 | Architecture | 3 weeks |

---

## Quick Start

    # Run security analysis
    python ai_code_analyzer.py --file your_code.py --security

    # Run code quality analysis
    python ai_code_analyzer.py --file your_code.py --quality

    # Generate refactored code
    python ai_code_analyzer.py --file your_code.py --refactor

    # Generate migration plan
    python ai_code_analyzer.py --file your_code.py --migrate

---

## How It Works

    Developer pushes code → GitHub triggers workflow → AI analyzes changes → Posts report on PR

---
