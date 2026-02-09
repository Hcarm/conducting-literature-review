#!/usr/bin/env python3
"""
Test API connectivity and skill installation for conducting-literature-review.

Checks (without requiring Claude Code or MCP servers running):
  1. Skill symlink exists and contains SKILL.md
  2. Node.js available (for PubMed MCP via npx)
  3. Semantic Scholar venv exists with run.py
  4. PubMed API (NCBI E-utilities) reachable; reports auth status
  5. Semantic Scholar API: DOI lookup (reliable endpoint)
  6. Semantic Scholar API: keyword search (frequently rate-limited -- WARN is normal)
  7. CrossRef API reachable (used by verify_citations.py)

Uses only Python stdlib. No pip dependencies.

Usage:
    python test-apis.py
    python test-apis.py --ncbi-key YOUR_KEY    # test with specific NCBI key
    python test-apis.py --s2-key YOUR_KEY      # test with specific S2 key
"""

import json
import os
import platform
import subprocess
import sys
import urllib.error
import urllib.request


# ── Configuration ──────────────────────────────────────

SKILL_DIR = os.path.join(os.path.expanduser("~"), ".claude", "skills", "conducting-literature-review")
MCP_DIR = os.path.join(os.path.expanduser("~"), ".claude", "mcp-servers", "semantic-scholar-fastmcp")

PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
S2_PAPER_DETAIL = "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature12373"
S2_PAPER_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1"
CROSSREF_DOI = "https://api.crossref.org/works/10.1038/nature12373"

TIMEOUT = 15
USER_AGENT = "conducting-literature-review-test/1.0"


# ── Helpers ────────────────────────────────────────────

class Result:
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"

    def __init__(self, status, name, message):
        self.status = status
        self.name = name
        self.message = message


def http_get(url, headers=None, timeout=TIMEOUT):
    """GET request using urllib. Returns (status_code, body_str) or raises."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8")


def run_cmd(cmd):
    """Run a shell command, return (returncode, stdout)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return proc.returncode, proc.stdout.strip()
    except FileNotFoundError:
        return -1, ""
    except subprocess.TimeoutExpired:
        return -2, ""


# ── Checks ─────────────────────────────────────────────

def check_skill_symlink():
    skill_md = os.path.join(SKILL_DIR, "SKILL.md")
    if os.path.isfile(skill_md):
        return Result(Result.PASS, "Skill symlink", f"SKILL.md found at {SKILL_DIR}")
    elif os.path.isdir(SKILL_DIR):
        return Result(Result.FAIL, "Skill symlink", f"Directory exists but SKILL.md not found in {SKILL_DIR}")
    else:
        return Result(Result.FAIL, "Skill symlink", f"Not found: {SKILL_DIR}. Run the install script first.")


def check_nodejs():
    rc, out = run_cmd(["node", "--version"])
    if rc == -1:
        return Result(Result.WARN, "Node.js", "Not found. PubMed MCP server requires Node.js 18+. Install from https://nodejs.org/")
    if rc != 0:
        return Result(Result.WARN, "Node.js", f"node --version returned exit code {rc}")
    try:
        major = int(out.lstrip("v").split(".")[0])
        if major < 18:
            return Result(Result.WARN, "Node.js", f"Found {out} (minimum is v18)")
        return Result(Result.PASS, "Node.js", f"Found {out}")
    except ValueError:
        return Result(Result.WARN, "Node.js", f"Could not parse version: {out}")


def check_s2_venv():
    if platform.system() == "Windows":
        py_path = os.path.join(MCP_DIR, ".venv", "Scripts", "python.exe")
    else:
        py_path = os.path.join(MCP_DIR, ".venv", "bin", "python")

    run_py = os.path.join(MCP_DIR, "run.py")

    if not os.path.isdir(MCP_DIR):
        return Result(Result.FAIL, "S2 MCP server", f"Directory not found: {MCP_DIR}. Run the install script first.")
    if not os.path.isfile(py_path):
        return Result(Result.FAIL, "S2 MCP server", f"Python venv not found at {py_path}. Run the install script to create it.")
    if not os.path.isfile(run_py):
        return Result(Result.FAIL, "S2 MCP server", f"run.py not found at {run_py}")
    return Result(Result.PASS, "S2 MCP server", f"venv and run.py found at {MCP_DIR}")


def check_pubmed_api(api_key=None):
    params = "?db=pubmed&term=test&retmax=1&retmode=json"
    if api_key:
        params += f"&api_key={api_key}"
    url = PUBMED_ESEARCH + params

    try:
        status, body = http_get(url)
        data = json.loads(body)
        count = data.get("esearchresult", {}).get("count", "0")
        if int(count) > 0:
            auth_status = "authenticated, 10 req/sec" if api_key else "unauthenticated, 3 req/sec"
            return Result(Result.PASS, "PubMed API", f"Reachable ({auth_status}). Test query returned {count} results.")
        return Result(Result.WARN, "PubMed API", "Reachable but test query returned 0 results.")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return Result(Result.WARN, "PubMed API", "Rate-limited (HTTP 429). Try again in a moment.")
        return Result(Result.FAIL, "PubMed API", f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return Result(Result.FAIL, "PubMed API", f"Network error: {e.reason}")
    except Exception as e:
        return Result(Result.FAIL, "PubMed API", f"Error: {e}")


def check_s2_doi_lookup(api_key=None):
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    try:
        status, body = http_get(S2_PAPER_DETAIL + "?fields=title,year", headers=headers)
        data = json.loads(body)
        title = data.get("title", "unknown")
        return Result(Result.PASS, "S2 DOI lookup", f"Paper found: \"{title[:60]}\"")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return Result(Result.WARN, "S2 DOI lookup", "Rate-limited (HTTP 429). This endpoint is usually reliable; try again shortly.")
        return Result(Result.FAIL, "S2 DOI lookup", f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return Result(Result.FAIL, "S2 DOI lookup", f"Network error: {e.reason}")
    except Exception as e:
        return Result(Result.FAIL, "S2 DOI lookup", f"Error: {e}")


def check_s2_keyword_search(api_key=None):
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    try:
        status, body = http_get(S2_PAPER_SEARCH, headers=headers)
        data = json.loads(body)
        total = data.get("total", 0)
        return Result(Result.PASS, "S2 keyword search", f"Returned {total} results. (This endpoint is often rate-limited; PASS means it is currently available.)")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return Result(Result.WARN, "S2 keyword search",
                         "Rate-limited (HTTP 429). This is normal for unauthenticated access. "
                         "The skill falls back to DOI lookup + citation chaining, which is the validated workflow.")
        return Result(Result.FAIL, "S2 keyword search", f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return Result(Result.FAIL, "S2 keyword search", f"Network error: {e.reason}")
    except Exception as e:
        return Result(Result.FAIL, "S2 keyword search", f"Error: {e}")


def check_crossref():
    try:
        status, body = http_get(CROSSREF_DOI)
        data = json.loads(body)
        title = data.get("message", {}).get("title", ["unknown"])[0]
        return Result(Result.PASS, "CrossRef API", f"DOI resolved: \"{title[:60]}\"")
    except urllib.error.HTTPError as e:
        return Result(Result.FAIL, "CrossRef API", f"HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        return Result(Result.FAIL, "CrossRef API", f"Network error: {e.reason}")
    except Exception as e:
        return Result(Result.FAIL, "CrossRef API", f"Error: {e}")


# ── Main ───────────────────────────────────────────────

def main():
    ncbi_key = None
    s2_key = None

    # Parse simple args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--ncbi-key" and i + 1 < len(args):
            ncbi_key = args[i + 1]
            i += 2
        elif args[i] == "--s2-key" and i + 1 < len(args):
            s2_key = args[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            sys.exit(1)

    print("=== Conducting Literature Review -- Dependency Check ===")
    print()

    results = [
        check_skill_symlink(),
        check_nodejs(),
        check_s2_venv(),
        check_pubmed_api(ncbi_key),
        check_s2_doi_lookup(s2_key),
        check_s2_keyword_search(s2_key),
        check_crossref(),
    ]

    # Print results
    for r in results:
        tag = {"PASS": "\033[32m", "WARN": "\033[33m", "FAIL": "\033[31m"}.get(r.status, "")
        reset = "\033[0m"
        print(f"[{tag}{r.status}{reset}] {r.name}: {r.message}")

    print()

    passes = sum(1 for r in results if r.status == Result.PASS)
    warns = sum(1 for r in results if r.status == Result.WARN)
    fails = sum(1 for r in results if r.status == Result.FAIL)

    summary_parts = [f"{passes} passed"]
    if warns:
        summary_parts.append(f"{warns} warning{'s' if warns > 1 else ''}")
    if fails:
        summary_parts.append(f"{fails} failed")

    print(f"{', '.join(summary_parts)} out of {len(results)} checks.")

    if fails == 0:
        print("The skill is ready to use.")
    elif fails <= 2:
        print("Some checks failed. Review the messages above and consult TROUBLESHOOTING.md.")
    else:
        print("Multiple checks failed. Run the install script first, then re-test.")

    sys.exit(1 if fails > 0 else 0)


if __name__ == "__main__":
    main()
