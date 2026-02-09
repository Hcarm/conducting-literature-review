# Web Search Strategies

Search strategies for executing literature queries via WebSearch and WebFetch. Load this module before executing web-based search rounds (source type 1).

---

## Query Templates

### From Core Concepts

Generate queries from the Core Concepts table:

- **Single-concept**: `"[concept search term 1] [concept search term 2]"`
- **Cross-concept**: `"[concept A term] [concept B term] [setting/context]"`
- **Variant**: `"[cross-disciplinary variant term] [concept B term]"`
- **Free-form**: `"[natural language research question]"`

### Implementation Science / Health Services Research

```
"[intervention] implementation cost [setting]"
"cost of implementing [intervention] in [setting]"
"[intervention] personnel time labor cost"
"micro-costing [intervention type] healthcare"
"economic evaluation [intervention] [study design]"
```

### Methodological Searches

```
"how to measure [outcome] in [context]"
"[method name] methodology [field]"
"best practices [activity] research"
"[framework name] framework application"
```

### Exemplar Searches

```
"[method] published results [setting] [year range]"
"exemplar [analysis type] [field] reporting"
"[journal name] [topic] [year]"
```

---

## Query Refinement

### If Too Many Results
- Add more specific terms
- Restrict time frame
- Add setting/context terms
- Use exact phrases in quotes

### If Too Few Results
- Remove restrictive terms
- Expand time frame
- Try synonyms and cross-disciplinary variants
- Broaden setting/context

### If Wrong Results
- Review terminology used in the field
- Check a known-good paper for terms
- Reframe the question
- Try different concept combinations from the Core Concepts table

---

## WebSearch Considerations

- Good for broad discovery across all source types
- Natural language queries work well
- Returns a mix of journal articles, institutional pages, and grey literature
- May miss very recent papers not yet indexed by search engines
- Use cross-disciplinary terminology variants (from Core Concepts Variants column) to avoid home-discipline bias

---

## WebFetch Domain Guidance

The skill has pre-approved WebFetch access to medical/research domains. When retrieving abstracts or full text:

- **PubMed/PMC**: `pubmed.ncbi.nlm.nih.gov`, `pmc.ncbi.nlm.nih.gov`, `ncbi.nlm.nih.gov`
- **AHRQ/Patient Safety**: `psnet.ahrq.gov`, `ahrq.gov`, `hhs.gov`
- **Journals**: `jamanetwork.com`, `biomedcentral.com`, `springer.com`, `journals.plos.org`, `sciencedirect.com`

For domains not in the approved list, WebFetch will prompt for user approval. Open-access journals and institutional repositories generally allow retrieval.

---

## PubMed via WebSearch (Fallback)

When PubMed MCP server is unavailable, surface PubMed results via targeted web queries:

- `site:pubmed.ncbi.nlm.nih.gov [topic] [key terms]`
- `site:pmc.ncbi.nlm.nih.gov [topic] full text`

This returns individual PubMed entries but lacks MeSH term support, field tags, and Boolean operators. Prefer the MCP-based PubMed search (search-pubmed.md) when available.

---

## Documentation

Record web search rounds per the documentation format in search-strategies.md. Source Type: "Web search". Tool: "WebSearch".
