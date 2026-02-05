# 🎯 Interview Demo Guide

## Quick Start (30 seconds)

```powershell
cd c:\Users\ajayr\Desktop\deep_research_from_scratch\interview_demo

# Run the demo (works WITHOUT API key - has built-in sample outputs)
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --full
```

---

## Demo Script for Interview

### 1️⃣ Opening (30 seconds)

Say: *"Let me show you a tool I built for exactly this use case — analyzing and refactoring legacy code with AI."*

```powershell
python ai_code_analyzer.py
```

This shows the banner and usage options.

---

### 2️⃣ Show the Legacy Code (1 minute)

Say: *"First, here's a typical legacy file we might encounter — an order service with several issues."*

```powershell
# Open the file or show it
cat legacy_code_samples/order_service.py
```

Point out:
- Line 12-14: "See these hardcoded credentials?"
- Line 27: "This has SQL injection"
- Line 44: "Callback hell - outdated pattern"

---

### 3️⃣ Run Security Analysis (1 minute)

Say: *"Let's run the security scanner."*

```powershell
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --security
```

**Talking points:**
- "It found 3 critical SQL injection vulnerabilities"
- "It shows the exact line numbers"
- "It provides the secure fix for each"
- "This runs automatically on every PR in CI/CD"

---

### 4️⃣ Run Code Quality Analysis (1 minute)

Say: *"Now let's look at code quality for modernization."*

```powershell
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --quality
```

**Talking points:**
- "It identifies the god method with 7 parameters"
- "It flags the callback hell pattern"
- "It suggests modern async/await approach"
- "These are the issues that slow down your team"

---

### 5️⃣ Generate Refactored Code (1 minute)

Say: *"Here's the powerful part — AI can generate the refactored version."*

```powershell
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --refactor
```

**Talking points:**
- "Credentials moved to environment variables"
- "All queries are parameterized now"
- "Added type hints and docstrings"
- "Converted callbacks to async/await"
- "Developer reviews and refines — AI drafts, human approves"

---

### 6️⃣ Show Migration Plan (1 minute)

Say: *"For larger migrations, it can generate a phased plan."*

```powershell
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --migrate
```

**Talking points:**
- "Phase 1 is quick security fixes — done in a day"
- "Phase 2 is code quality — takes a week"
- "Phase 3 is architecture modernization"
- "This helps product managers understand the effort"

---

### 7️⃣ Full Report (Optional)

Say: *"And we can generate a complete report for documentation."*

```powershell
python ai_code_analyzer.py --file legacy_code_samples/order_service.py --full --output analysis_report.md
```

---

## Key Messages to Emphasize

1. **"AI drafts, human refines"**
   - The tool generates suggestions
   - Developer reviews and approves
   - AI doesn't auto-commit anything

2. **"This runs in CI/CD, not just IDE"**
   - Security scan on every PR automatically
   - No developer has to remember to run it
   - Consistent enforcement

3. **"Works with your existing tools"**
   - GitHub Actions, Jenkins, GitLab CI
   - Uses Claude/Bedrock API
   - Doesn't replace Copilot — complements it

4. **"Phased migration approach"**
   - Start with security fixes (quick wins)
   - Then code quality
   - Then architecture
   - Never big-bang rewrites

---

## If They Ask Technical Questions

### "How does it work?"

> *"It sends the code to Claude API with a specialized prompt for security/quality analysis. The prompt includes specific patterns to look for — SQL injection, hardcoded secrets, code smells. Claude analyzes and returns structured findings."*

### "Can it handle large codebases?"

> *"Yes. Claude has a 200K token context window — about 150,000 lines of code. For larger codebases, we analyze file by file and aggregate the reports. The CI/CD integration only analyzes changed files in each PR."*

### "What about false positives?"

> *"That's why human review is required. The AI flags potential issues, developers verify. Over time, we tune the prompts to reduce noise. We can also add ignore comments for intentional patterns."*

### "How do you handle sensitive code?"

> *"For enterprise, we use Claude Enterprise or AWS Bedrock — data isn't used for training. We can also self-host models if needed. The tool supports configuring which files to exclude from analysis."*

---

## Backup: If Demo Fails

If Python or API issues occur, open the README and walk through the architecture:

```powershell
# Show the comprehensive documentation
cat ..\AI_Automation_Bots_README.md
```

Say: *"Let me walk you through the architecture instead..."*

---

## Files in This Demo

```
interview_demo/
├── ai_code_analyzer.py          # Main demo tool
├── DEMO_GUIDE.md                # This guide
└── legacy_code_samples/
    ├── order_service.py         # Sample legacy code (eCommerce)
    └── user_auth.py             # Sample legacy code (Auth)
```

---

## Pre-Interview Checklist

- [ ] Test the demo runs: `python ai_code_analyzer.py --file legacy_code_samples/order_service.py --security`
- [ ] Have terminal open and ready
- [ ] Know the 4 key messages (AI drafts, CI/CD, existing tools, phased migration)
- [ ] Have backup plan (walk through README)
- [ ] Practice the flow 2-3 times

---

**Good luck! 🚀**
