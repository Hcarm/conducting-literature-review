# Grey Literature Search Strategies

Search strategies for discovering non-indexed sources: dissertations, theses, working papers, preprints, technical reports, and conference proceedings. Load this module before executing grey literature search rounds (source type 2).

---

## What Counts as Grey Literature

| Source Type | Examples | Value Proposition |
|-------------|----------|-------------------|
| PhD/Master's theses | ProQuest Dissertations, university repositories | Comprehensive literature reviews of exact questions; complete reference lists; methodological detail journals compress; negative results |
| Working papers | NBER, IZA, institutional series | Methods and findings before formal publication; may never reach journals |
| Preprints | arXiv, bioRxiv, medRxiv, SSRN | Most recent work; often identical to eventual publication |
| Technical reports | AHRQ, CDC, WHO, government agencies | Policy-relevant analyses; large datasets; implementation details |
| Conference proceedings | Society meeting abstracts, poster presentations | Early-stage work; pilot results; niche topics |

---

## Why Grey Literature Matters

Formal databases index published journal articles. Grey literature lives outside these indexes but may contain the single most relevant source for a specific question. A thesis from a methods-focused graduate program that reviews the complete landscape of a specific analytical approach provides:

- A ready-made literature review of the exact question
- Every relevant publication the thesis author identified
- Methodological depth that journal word limits compress
- Negative results and dead-end analyses that journals decline to publish
- Advisory committee oversight as a quality signal (for theses from strong programs)

Omitting grey literature creates systematic bias toward indexed publications and against the sources most likely to have addressed the exact question.

---

## Search Strategies by Source Type

### Theses and Dissertations

```
"[topic keywords] thesis OR dissertation"
"[topic keywords] site:proquest.com"
"[topic keywords] doctoral dissertation [field]"
"[topic keywords] master's thesis [university or program type]"
```

Also try institutional repository searches for specific universities known in the field.

### Preprints

```
"[topic keywords] site:arxiv.org"
"[topic keywords] site:biorxiv.org"
"[topic keywords] site:medrxiv.org"
"[topic keywords] site:ssrn.com"
```

### Government and Technical Reports

```
"[topic keywords] site:ahrq.gov"
"[topic keywords] site:cdc.gov"
"[topic keywords] site:who.int technical report"
"[topic keywords] site:gov report OR guideline OR evidence review"
```

### Working Papers

```
"[topic keywords] working paper [field]"
"[topic keywords] site:nber.org" (economics)
"[topic keywords] site:iza.org" (labor economics)
```

---

## Evaluation Criteria for Grey Literature

Grey literature is not peer-reviewed in the traditional sense. Assess quality independently:

| Signal | Meaning |
|--------|---------|
| Thesis from strong program | Advisory committee provides methodological oversight |
| Government agency report | Institutional review processes; typically conservative claims |
| Preprint with journal submission | Will undergo peer review; treat as provisional |
| Working paper from recognized series | Editorial standards vary; assess methods directly |
| Conference abstract only | Insufficient detail for critical claims; use as lead for further search |

**Do not exclude grey literature solely because it lacks peer review.** Assess methodological rigor on its own terms. A well-conducted thesis with a transparent methods section is more reliable than a peer-reviewed paper with vague methods.

---

## Source Diversity Waiver

If grey literature search produces zero results after exhaustive queries, the source diversity criterion is **waived** and the absence is documented in REVIEW_PROGRESS.md: "Grey literature search produced zero relevant results after N queries across M source types. Source diversity criterion waived; absence documented as finding."

---

## Documentation

Record grey literature search rounds per the documentation format in search-strategies.md. Source Type: "Grey literature". Tool: "WebSearch".
