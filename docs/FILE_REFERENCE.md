# LeetCode Auto-Solver - File Reference

## 📁 Complete File Listing

### Core Agent Files (`/app/agent/`)

| File | Purpose | Lines | Key Functions |
|------|---------|-------|---------------|
| **main.py** | Controller/Orchestrator | ~300 | `solve_problem()`, `solve_all_problems()`, `extract_problem_slug()` |
| **browser.py** | Selenium Automation | ~250 | `scrape_problem_description()`, `inject_code()`, `run_tests()`, `get_test_result()` |
| **brain.py** | Gemini AI Integration | ~200 | `generate_solution()`, `_clean_code_response()`, `_enforce_rate_limit()` |
| **memory.py** | JSON Persistence | ~150 | `get()`, `save()`, `get_all_solved()`, `get_stats()` |
| **config.py** | Configuration Constants | ~50 | SELECTORS, TIMEOUTS, RETRY_CONFIG |
| **test_setup.py** | Setup Verification | ~250 | `test_environment()`, `test_imports()`, `test_chrome_connection()` |
| **demo.py** | Demo Script | ~50 | `demo()` |
| **launch_chrome.sh** | Chrome Launcher | ~30 | Shell script |

### Configuration Files

| File | Purpose |
|------|----------|
| **.env** | Environment variables (API keys, timeouts, paths) |
| **.env.example** | Template for environment setup |
| **requirements.txt** | Python dependencies (selenium, emergentintegrations, python-dotenv) |

### Documentation Files (`/app/docs/`)

| File | Purpose | Size |
|------|---------|------|
| **SYSTEM_DESIGN.md** | Complete architecture documentation | ~12,000 words |
| **QUICKSTART.md** | Quick start guide | ~2,000 words |
| **CHECKLIST.md** | Implementation checklist | ~1,000 words |
| **FILE_REFERENCE.md** | This file - Complete file listing | ~500 words |

### User Documentation (`/app/agent/`)

| File | Purpose | Size |
|------|---------|------|
| **README.md** | User guide, installation, usage, troubleshooting | ~3,000 words |

### Runtime Directories

| Directory | Purpose | Content |
|-----------|---------|----------|
| **data/** | Persistent storage | `problems.json` - Solved problems database |
| **logs/** | Execution logs | `solver.log` - Runtime logs |

## 📊 Statistics

### Code Metrics

```
Total Files: 15
Code Files: 8
Config Files: 3
Documentation Files: 4
Total Lines of Code: ~2,500+
Total Documentation: ~15,000+ words
```

### Module Breakdown

| Module | Responsibility | Dependencies |
|--------|----------------|---------------|
| main.py | State machine orchestration | browser, brain, memory |
| browser.py | DOM interaction, code injection | selenium |
| brain.py | AI code generation | emergentintegrations |
| memory.py | Data persistence | json, threading |
| config.py | Constants | none |

## 🔍 Quick Navigation

### For Users

1. **Getting Started**: Read `/app/agent/README.md`
2. **Quick Start**: Read `/app/docs/QUICKSTART.md`
3. **Run Setup Test**: `cd /app/agent && python test_setup.py`
4. **Solve Problem**: `python main.py <url>`

### For Developers

1. **Architecture**: Read `/app/docs/SYSTEM_DESIGN.md`
2. **Component Specs**: See Section 2 of SYSTEM_DESIGN.md
3. **Error Handling**: See Section 5 of SYSTEM_DESIGN.md
4. **Testing**: See Section 7 of SYSTEM_DESIGN.md

### For Troubleshooting

1. **Setup Issues**: Run `python test_setup.py`
2. **Chrome Issues**: See README.md Troubleshooting section
3. **API Issues**: Check logs at `logs/solver.log`
4. **Memory Issues**: Inspect `data/problems.json`

## 📦 Dependencies

### Python Packages

```
selenium==4.16.0           # Browser automation
emergentintegrations==0.1.0 # Unified LLM API
python-dotenv==1.0.0       # Environment management
```

### System Requirements

- Python 3.11+
- Google Chrome browser
- Chrome DevTools access (port 9222)
- Internet connection
- LeetCode account (for login)

## 🔧 File Modification Guide

### To Change AI Behavior

Edit `brain.py`:
```python
def _get_system_prompt(self) -> str:
    return """Your custom prompt here..."""
```

### To Change DOM Selectors

Edit `config.py`:
```python
SELECTORS = {
    "problem_description": "your-new-selector",
    # ...
}
```

### To Change Timeout Values

Edit `.env`:
```bash
RESULT_TIMEOUT=60
MAX_RETRIES=3
```

### To Add New Features

1. **Browser actions**: Add methods to `LeetCodeBrowser` class in `browser.py`
2. **AI features**: Add methods to `CodeBrain` class in `brain.py`
3. **Storage queries**: Add methods to `MemoryStore` class in `memory.py`
4. **Workflow states**: Modify state machine in `solve_problem()` in `main.py`

## 📝 Data Files

### problems.json Structure

```json
{
  "problem-slug": {
    "slug": "problem-slug",
    "status": "pass",
    "code": "class Solution:\n    def method(self): pass",
    "timestamp": "2025-01-15T10:30:45.123456+00:00",
    "attempts": 1
  }
}
```

### solver.log Format

```
2025-01-15 10:30:45,123 - main - INFO - Starting to solve: two-sum
2025-01-15 10:30:46,456 - browser - INFO - Navigating to https://leetcode.com/problems/two-sum/
2025-01-15 10:30:48,789 - brain - INFO - Generating solution with Gemini...
2025-01-15 10:30:52,012 - browser - INFO - Code injected successfully
2025-01-15 10:30:55,345 - browser - INFO - ✓ Tests passed!
2025-01-15 10:30:56,678 - memory - INFO - Saved two-sum: pass (attempts: 1)
```

## ⚡ Performance Notes

### Expected File Sizes

- `problems.json`: ~1-5 KB per problem
- `solver.log`: ~10-50 KB per problem
- Total for 100 problems: ~1-5 MB

### Resource Usage

- Memory: ~100-200 MB (Chrome + Python)
- CPU: Minimal (mostly waiting for API/browser)
- Network: ~1-5 MB per problem (API calls + page loads)

## 🔒 Security Notes

### Sensitive Files (DO NOT COMMIT)

- `.env` - Contains API keys
- `data/problems.json` - May contain problem solutions
- `logs/solver.log` - May contain sensitive data

### Safe to Commit

- All `.py` files
- `.env.example`
- `requirements.txt`
- All documentation files
- Helper scripts

## 🔗 Related Files

### Backend Integration

The agent can optionally integrate with the FastAPI backend:

- `/app/backend/server.py` - Main FastAPI app
- `/app/backend/.env` - Backend environment (includes EMERGENT_LLM_KEY)
- `/app/backend/requirements.txt` - Backend dependencies

### Frontend (Not Used)

The agent is a standalone CLI tool and doesn't use the React frontend.

## 📌 Version Info

- **Version**: 1.0
- **Status**: Production Ready
- **Last Updated**: January 2025
- **Python**: 3.11+
- **License**: MIT

---

**For the complete architecture, see**: [SYSTEM_DESIGN.md](/app/docs/SYSTEM_DESIGN.md)

**For usage instructions, see**: [README.md](/app/agent/README.md)

**For quick start, see**: [QUICKSTART.md](/app/docs/QUICKSTART.md)
