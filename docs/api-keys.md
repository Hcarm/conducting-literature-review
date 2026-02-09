# API Keys

This skill integrates two academic database APIs, each with its own authentication model. Both API keys are free. Neither requires institutional affiliation.

---

## NCBI API Key (PubMed)

### Why you need it

The PubMed MCP server queries NCBI E-utilities (ESearch, EFetch, ELink). Without an API key, NCBI rate-limits requests to **3 per second**. With a key, the limit increases to **10 per second**. A full literature review issues 15-25 PubMed queries across search, metadata retrieval, and citation network calls. The unauthenticated rate is workable but slower; the authenticated rate avoids any noticeable delay.

The key is free, requires no justification, and has no usage caps beyond the per-second rate.

### How to obtain one

1. Go to [NCBI Account Registration](https://www.ncbi.nlm.nih.gov/account/)
2. Create an NCBI account (email verification required)
3. After signing in, go to **Settings** (top-right menu)
4. Scroll to **API Key Management**
5. Click **Create an API Key**
6. Copy the generated key

### Where to put it

Add the key to the `NCBI_API_KEY` field in your `~/.claude.json` MCP server configuration. See [setup/examples/claude-json-snippet.json](../setup/examples/claude-json-snippet.json).

### How to verify it works

Run `setup/test-apis.py`. The PubMed test reports whether authentication is active:

```
[PASS] PubMed API reachable (authenticated, 10 req/sec)
```

vs.

```
[PASS] PubMed API reachable (unauthenticated, 3 req/sec)
```

Both pass. The authenticated version is faster.

---

## Semantic Scholar API Key (Optional)

### Why it is optional

The Semantic Scholar API allows unauthenticated access at **100 requests per 5 minutes** (~0.33 req/sec). The skill's validated workflow for Semantic Scholar is **DOI lookup + forward citation chaining**, not keyword search. This workflow uses relatively few API calls -- typically 5-15 per review (2-3 seed lookups, 2-3 citation chain calls, a few detail lookups). Unauthenticated access is sufficient for this volume.

### Why keyword search is unreliable regardless of authentication

During validation testing, every `paper_relevance_search` and `paper_bulk_search` call returned HTTP 429 (rate limited), even within a fresh session. All Semantic Scholar contributions to completed reviews came through the DOI lookup + citation chaining pathway. The keyword search endpoints may work with authentication but are untested in that configuration. The skill is designed to fall back to DOI lookup + citation chaining automatically.

### Why you might still want one

An API key provides **1 request per second** sustained throughput, which allows more aggressive use of Semantic Scholar endpoints. If you run multiple reviews in quick succession or want to attempt keyword search, authentication prevents quota exhaustion.

### How to obtain one

1. Go to the [Semantic Scholar API Portal](https://www.semanticscholar.org/product/api)
2. Click **Request API Key** (or equivalent signup link)
3. Complete the registration form
4. The API key is delivered via email (may take up to 24 hours)
5. Copy the key

### Where to put it

Add the key to the `SEMANTIC_SCHOLAR_API_KEY` field in your `~/.claude.json` MCP server configuration. An empty string (`""`) means unauthenticated access. See [setup/examples/claude-json-snippet.json](../setup/examples/claude-json-snippet.json).

### How to verify it works

Run `setup/test-apis.py`. The Semantic Scholar tests check both DOI lookup and keyword search:

```
[PASS] Semantic Scholar API: paper lookup by DOI works
[WARN] Semantic Scholar API: keyword search returned 429 (rate-limited)
```

The WARN for keyword search is expected. DOI lookup passing is sufficient for the skill to operate.

---

## CrossRef (No Key Required)

The skill's `verify_citations.py` script calls the CrossRef REST API to verify DOIs. CrossRef does not require an API key. There are no rate limits for polite usage (the script includes a User-Agent header per CrossRef's guidelines). No configuration is needed.

---

## Summary

| API | Key Required? | Free? | Rate (Unauthenticated) | Rate (Authenticated) | Where to Configure |
|-----|--------------|-------|----------------------|--------------------|--------------------|
| PubMed (NCBI) | Recommended | Yes | 3 req/sec | 10 req/sec | `NCBI_API_KEY` in `~/.claude.json` |
| Semantic Scholar | Optional | Yes | 100 req/5 min | 1 req/sec | `SEMANTIC_SCHOLAR_API_KEY` in `~/.claude.json` |
| CrossRef | No | N/A | No limit (polite use) | N/A | None |
