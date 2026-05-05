# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Keep your replies extremely concise and focus on conveying the key information. No unnecessary fluff, no long code snippets.

## Build & Run Commands

### Docker (recommended)
```bash
docker build -t oktaverse .
docker run --rm -p 5000:5000 --name oktaverse oktaverse
```

### Local Development
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`. WeasyPrint requires system libraries for PDF export (included in Docker image).

### No Tests or Linting
This codebase has no test suite or linting configuration.

## Architecture

**OktaVerse** is a monolithic Flask application providing four Okta analysis tools:

| Tool | Route | Purpose |
|------|-------|---------|
| OktaCompare | `/` | Compare two Okta environments |
| OktaSnapshot | `/snapshot` | Export single org configuration |
| OktaEvaluate | `/evaluate` | Security assessment with validation checks |
| OktaMigrate | `/migrate` | Compare and migrate entities (Groups demo) |

### Key Files & Directories

- **`app.py`** (~205KB) - All Flask routes, business logic, validation helpers, export functions
- **`modules/`** (39 files) - Entity comparison functions
- **`scripts/`** (70+ files) - Okta API extraction and snapshot builders
- **`templates/`** - HTML templates for web UI

## Patterns

### Comparison Modules (`modules/*.py`)
Each module implements:
```python
def compare_<entity>(envA_domain, envA_token, envB_domain, envB_token):
    # Returns tuple: (diffs_list, matches_list)
```

### Extraction Scripts (`scripts/`)
- `extract_<entity>.py` - Fetch data from Okta APIs
- `oktasnapshot_<entity>.py` - Build structured snapshot rows

### Unified Diff Structure
All comparisons return dicts with:
- `Category`, `Object`, `Attribute`
- `Env A Value`, `Env B Value`
- `Difference Type` (Missing/Extra/Mismatch)
- `Impact`, `Recommended Action`
- `Priority` (Critical/Medium/Low/Match)

## Okta API Integration

All Okta calls use `requests` with SSWS token auth. Pagination handled via `Link` headers. Token validation occurs on form submission with specific error handling for 401/403/404.

Global state dictionaries cache export data: `LAST_EXPORT`, `OKTASNAPSHOT_EXPORT`, `OKTAEVALUATE_EXPORT`, `OKTAMIGRATE_EXPORT`.
