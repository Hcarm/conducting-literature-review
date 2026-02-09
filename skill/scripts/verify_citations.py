#!/usr/bin/env python3
"""
Verify citations against the CrossRef REST API.

Checks whether DOIs resolve and retrieves authoritative metadata for comparison
against skill-recorded citation details. Uses only Python stdlib (no pip installs).

Usage:
    python verify_citations.py DOI [DOI ...]
    python verify_citations.py --file dois.txt

Output: JSON array to stdout. Each entry contains:
    - doi: the input DOI
    - resolved: boolean
    - title: from CrossRef metadata (or null)
    - authors: list of "Given Family" strings (or [])
    - journal: container title (or null)
    - year: publication year (or null)
    - match_confidence: "high" | "partial" | "failed"
    - error: error message (if failed, else null)
"""

import json
import sys
import urllib.request
import urllib.error
import urllib.parse


CROSSREF_API = "https://api.crossref.org/works/"
USER_AGENT = "conducting-literature-review/1.0 (mailto:noreply@example.com)"
TIMEOUT_SECONDS = 15


def verify_doi(doi: str) -> dict:
    """Verify a single DOI against CrossRef."""
    result = {
        "doi": doi,
        "resolved": False,
        "title": None,
        "authors": [],
        "journal": None,
        "year": None,
        "match_confidence": "failed",
        "error": None,
    }

    # Normalize DOI
    doi_clean = doi.strip()
    if doi_clean.startswith("https://doi.org/"):
        doi_clean = doi_clean[len("https://doi.org/"):]
    elif doi_clean.startswith("http://doi.org/"):
        doi_clean = doi_clean[len("http://doi.org/"):]
    elif doi_clean.startswith("doi:"):
        doi_clean = doi_clean[len("doi:"):]

    if not doi_clean:
        result["error"] = "Empty DOI after normalization"
        return result

    url = CROSSREF_API + urllib.parse.quote(doi_clean, safe="")

    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            result["error"] = "DOI not found in CrossRef"
        else:
            result["error"] = f"HTTP {e.code}: {e.reason}"
        return result
    except urllib.error.URLError as e:
        result["error"] = f"Network error: {e.reason}"
        return result
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        return result

    result["resolved"] = True

    message = data.get("message", {})

    # Title
    titles = message.get("title", [])
    if titles:
        result["title"] = titles[0]

    # Authors
    authors = message.get("author", [])
    author_names = []
    for a in authors:
        given = a.get("given", "")
        family = a.get("family", "")
        name = f"{given} {family}".strip()
        if name:
            author_names.append(name)
    result["authors"] = author_names

    # Journal
    containers = message.get("container-title", [])
    if containers:
        result["journal"] = containers[0]

    # Year
    published = message.get("published-print") or message.get("published-online") or message.get("issued")
    if published:
        date_parts = published.get("date-parts", [[]])
        if date_parts and date_parts[0]:
            result["year"] = date_parts[0][0]

    # Confidence assessment
    fields_present = sum([
        result["title"] is not None,
        len(result["authors"]) > 0,
        result["journal"] is not None,
        result["year"] is not None,
    ])

    if fields_present == 4:
        result["match_confidence"] = "high"
    elif fields_present >= 2:
        result["match_confidence"] = "partial"
    else:
        result["match_confidence"] = "failed"

    return result


def main():
    dois = []

    if len(sys.argv) < 2:
        print("Usage: python verify_citations.py DOI [DOI ...]", file=sys.stderr)
        print("       python verify_citations.py --file dois.txt", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Error: --file requires a filename argument", file=sys.stderr)
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            dois = [line.strip() for line in f if line.strip()]
    else:
        dois = sys.argv[1:]

    results = [verify_doi(doi) for doi in dois]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
