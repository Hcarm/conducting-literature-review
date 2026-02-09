---
name: conducting-literature-review
description: Conducts focused or comprehensive literature reviews for research projects. Interviews the user to understand needs, searches for relevant papers, organizes findings with exemplar designations, and performs self-assessment for gaps. Use when the user needs background research, wants to find relevant papers, asks for a literature review, or mentions needing to find papers on a topic.
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, mcp__pubmed-mcp-server__pubmed_search_articles, mcp__pubmed-mcp-server__pubmed_fetch_contents, mcp__pubmed-mcp-server__pubmed_article_connections, mcp__pubmed-mcp-server__pubmed_generate_chart, mcp__semantic-scholar__paper_relevance_search, mcp__semantic-scholar__paper_bulk_search, mcp__semantic-scholar__paper_title_search, mcp__semantic-scholar__paper_details, mcp__semantic-scholar__paper_batch_details, mcp__semantic-scholar__paper_citations, mcp__semantic-scholar__paper_references, mcp__semantic-scholar__get_paper_recommendations_single, mcp__semantic-scholar__get_paper_recommendations_multi, mcp__semantic-scholar__author_search, mcp__semantic-scholar__author_details
---

# Literature Review Skill

Conducts focused or comprehensive literature reviews through a 6-phase pipeline: Initialize, Interview, Search, Organize, Antagonize, Synthesize.

**Two modes**:
- **Narrow Search**: Quick answer to a specific question (8-14 papers, 2 source types minimum)
- **Full Review**: Comprehensive background for a project (30-48+ papers, 6 source types)

**Citation format**: Vancouver (numbered, with DOIs)

**This is NOT a systematic review.** It is a rigorous but pragmatic literature review that prioritizes finding the right methods over being exhaustive. It uses structured search, cross-disciplinary translation, exemplar identification, and antagonistic self-assessment.

---

## Phase 0: Initialize

### Step 0a: Permission Check

Verify that required tools are available. If the user denies WebSearch or WebFetch permissions, report the impact:
> "Web search and web fetch are unavailable. The review will rely on database APIs for discovery and MCP metadata for content retrieval. Grey literature discovery is limited to database-indexed sources. Deep extraction (Level 4) may be limited to abstract-available information."

### Step 0b: MCP Health Check

Probe each MCP server with a minimal query:
- **PubMed**: `pubmed_search_articles` with queryTerm "test", maxResults 1
- **Semantic Scholar**: `paper_relevance_search` with query "test", limit 1

Classify each server:

| Response | Classification | Report to User |
|----------|---------------|---------------|
| Structured results returned | **Available** | "PubMed: Available" |
| HTTP 429 or throttling | **Rate-Limited** | "Semantic Scholar: Rate-limited (server reachable but currently throttled). Will attempt during search; if persistent, source will be skipped." |
| No response or error | **Unavailable** | "PubMed: Unavailable. Database search will be skipped." |

Record results in REVIEW_PROGRESS.md Infrastructure Status table.

**Compound failure**: If both MCP servers are unavailable, report: "Both database servers are unavailable. The review will rely on Web search and Grey literature only." See [search-databases.md](references/search-databases.md) for compound degradation handling.

### Step 0c: Check for Existing Reviews

1. Look for `Literature/INDEX.md` in the project
2. If found, read it and check for in-progress reviews
3. If multiple reviews are In Progress, present choice to user via AskUserQuestion (see [state-management.md](references/state-management.md))
4. If one review is In Progress, offer Resume or Start Fresh
5. If no existing reviews or user chooses Start Fresh, proceed to Step 0d

### Step 0d: Create Review Structure

1. Create subfolder: `Literature/YYYY-MM-DD_topic-slug/`
2. Copy REVIEW_PROGRESS.md template to the subfolder (fill in date, topic)
3. Create `Full_text_references/` subfolder
4. Create or update `Literature/INDEX.md` with new review row

Alternatively, use `init_review.py` to automate folder creation:
```bash
python ~/.claude/skills/conducting-literature-review/scripts/init_review.py --project "." --topic "topic-slug"
```

---

## Phase 1: Interview

**Goal**: Understand the user's needs well enough to search effectively. Interview first, always -- never skip to searching.

Load [interview-questions.md](references/interview-questions.md) for question banks.

### Step 1a: Mode Selection

Ask the user to choose Narrow Search or Full Review. If unclear, default to Narrow Search -- the user can upgrade later.

### Step 1b: Artifact Intake

Ask the user for existing project documents:
> "Do you have existing project documents I can read to inform this review? For example: Specific Aims, manuscript draft, IRB application, known exemplar articles, an existing reference list, or project code."

If artifacts are provided:
1. Read each artifact using the Read tool
2. Extract structured inputs per the artifact extraction table in [interview-questions.md](references/interview-questions.md)
3. Record what was extracted in REVIEW_PROGRESS.md Artifact Intake Record
4. Record pre-populated reference count for convergence exclusion

If a single paper is provided, ask the follow-up question about intent (same topic / methods transfer / find similar).

If a reference list is provided, ask about intent (update existing / seeds for new review).

### Step 1c: Core Concepts Extraction

Help the user identify 2-5 core concepts with search terms and target depths. This replaces the PICO framework as the primary search scaffold while preserving PICO's functional roles.

1. Identify question type (clinical therapy / methodological / cross-disciplinary / exploratory)
2. Suggest decomposition template. For clinical therapy questions, **recommend** PICO dimensions as concept labels.
3. Build Core Concepts table: per-concept search terms, cross-disciplinary variants, target depths
4. Enforce minimum depth: at least one concept must be Moderate or Strong
5. For negative-framing questions: enable negative-framing modifier (all concepts get critique/limitation variants)

Record the Core Concepts table in REVIEW_PROGRESS.md before proceeding.

### Step 1d: Complete Interview

Continue asking questions from the interview question bank until:
- Research question is clearly defined
- Core Concepts table is complete
- Scope boundaries (inclusions and exclusions) are established
- Mode-appropriate depth is achieved

Document all goals in REVIEW_PROGRESS.md. Update Status to "Phase 2 -- Searching".

---

## Phase 2: Search

**Goal**: Find relevant papers across multiple source types using Core Concepts-driven query generation.

Load [search-strategies.md](references/search-strategies.md) for the search execution protocol. Budget governance, sufficiency criteria, and stopping hierarchy are defined there (single source of truth).

### Step 2a: Generate Query Plan

From the Core Concepts table, generate queries using:
1. **Single-concept queries**: each concept independently
2. **Cross-concept queries**: pairwise or three-way combinations
3. **Variant queries**: cross-disciplinary terminology
4. **Free-form queries**: natural language formulation
5. **Negative-framing variants**: if enabled, all concepts get critique/limitation terms

Write planned queries per source type to Search_Methods.md BEFORE execution begins.

### Step 2b: Execute Search by Source Type

Execute in order. Load the relevant strategy module before each source type:

| Order | Source Type | Module | Narrow? | Full? |
|-------|------------|--------|---------|-------|
| 1 | Web search | [search-web.md](references/search-web.md) | Yes | Yes |
| 2 | Grey literature | [search-grey-literature.md](references/search-grey-literature.md) | As needed | Yes |
| 3 | PubMed | [search-pubmed.md](references/search-pubmed.md) | No | Yes (if available) |
| 4 | Semantic Scholar | [search-semantic-scholar.md](references/search-semantic-scholar.md) | No | Yes (if available) |
| 5 | Citation chaining | [search-citation-chaining.md](references/search-citation-chaining.md) | If seeds exist | Yes |
| 6 | Seed-based recommendation | [search-recommendations.md](references/search-recommendations.md) | If seeds exist | Yes |

**Per-source execution protocol**:
1. Write "In Progress" status to REVIEW_PROGRESS.md Search Status table
2. Execute planned queries
3. Apply incremental deduplication after results (see [quality-criteria.md](references/quality-criteria.md) dedup protocol)
4. Add new candidates to REVIEW_PROGRESS.md Paper Tracking table
5. Update Search_Methods.md with executed queries and results
6. Write "Complete" status to Search Status table

**Error handling**: On HTTP 429 or timeout, wait 60 seconds, retry once. If retry fails, skip remaining queries for this source type. Record partial completion status.

**Budget redistribution**: When a source type completes with zero relevant results, its remaining budget is available for other sources with unfilled concept gaps.

### Step 2c: Assess Sufficiency

After each round, assess sufficiency criteria (defined in [search-strategies.md](references/search-strategies.md)):

1. **Concept coverage**: Each concept at its Target Depth?
2. **Concept intersection**: Each concept pair addressed? If an intersection is empty for a cross-disciplinary question, ask the user: "No papers found connecting [A] and [B]. Is this a known gap?" Record as "Satisfied" or "Gap Documented" -- both count as addressed.
3. **Convergence**: >80% overlap with existing candidates? (Exclude pre-populated references from artifact intake.)
4. **Source diversity**: At least one grey literature source? (Waive if genuinely absent.)

### Step 2d: Classify Literature Density

When convergence is high but paper count is low, classify as "Literature Density: Sparse" in REVIEW_PROGRESS.md. This distinguishes genuine sparsity from search failure.

### Step 2e: User Checkpoint

Present to user before proceeding to Phase 3:
- Total papers found by source type
- Concept coverage status
- Convergence rate
- Preliminary quality impression (e.g., "mostly observational studies, limited RCTs")
- Budget utilization
- Mode upgrade option (if narrow, offer: "Would you like to expand to a full review?")

**Mode upgrade**: If user accepts, follow the mode upgrade protocol in [state-management.md](references/state-management.md).

### Stopping Hierarchy

Applied in priority order:
1. **Budget exhaustion** (hard stop; AskUserQuestion for targeted extension)
2. **Convergence** (>80% overlap)
3. **Round cap** (3 narrow / 5 full)
4. **All source types complete**

Update Status to "Phase 3 -- Organizing".

---

## Phase 3: Organize

**Goal**: Process candidate papers into a structured annotated bibliography with exemplar deep extraction and evidence tables.

Phase 3 decomposes into five sub-steps. See [quality-criteria.md](references/quality-criteria.md) for the processing sequence, deduplication protocol, exemplar criteria, and batched processing rules.

### Phase 3A: Triage and Deduplication

1. Apply comprehensive deduplication (DOI primary, fuzzy title fallback, field-level union merge)
2. Fetch metadata via MCP tools or WebFetch for any candidates lacking structured data
3. Screen candidates on title/abstract for relevance against Core Concepts
4. Mark non-relevant papers as Excluded in Paper Tracking table
5. User-designated exemplars bypass relevance screening but go through dedup

### Phase 3B: Process Supporting Papers

1. For each non-exemplar candidate passing triage:
   - Write Level 2 annotation (1-2 sentence summary, quality note)
   - Verify DOI
   - Update Paper Tracking Status to "Level-2-Complete"
2. **Promotion detection**: If a paper meets exemplar criteria during processing, flag it (Exemplar? = "Promoted") for Phase 3C

### Phase 3C: Process Exemplar Papers

For each pre-designated exemplar and promoted paper:

1. **Content retrieval** via fallback chain:
   - MCP metadata (abstract + structured fields)
   - User PDF in Full_text_references/ (check via Glob)
   - WebFetch full text (for open-access papers)
   - WebFetch abstract page (for paywalled papers)
   - Flag for user: "Could you provide the PDF for [Paper]? Place it in Full_text_references/."

2. **Level 3 annotation**: All Paper_Entry.md fields
3. **Level 4 deep extraction** (if full text available): TL;DR, research question, identification strategy, data, statistical specifications, key finding with effect size, contributions, replication feasibility, author-noted limitations

If full text unavailable: extract what is possible from abstract. Mark unavailable fields: "N/A -- full text required" or "Abstract only: [partial info]".

Update Paper Tracking Status to "Level-3-Complete" or "Level-4-Complete".

### Phase 3D: Build Evidence Table

Compile evidence table per topic section from Level 4 fields:

| Exemplar | TL;DR | Method | Data (N, period) | Key Finding | Effect Size (95% CI) | Replication? |
|----------|-------|--------|-------------------|-------------|---------------------|-------------|

For abstract-only exemplars: "Abstract only -- [available fields]".

### Phase 3E: Citation Verification

Run `verify_citations.py` on all papers with DOIs:
```bash
python ~/.claude/skills/conducting-literature-review/scripts/verify_citations.py --file Literature_Review.md
```

Papers without DOIs: skip verification, record "N/A (no DOI)".

### Batched Processing

When candidate count exceeds 50: process in batches of ~25. Each batch completes 3A-3B before the next begins. Phase 3C processes all exemplars after all batches complete 3B. Track per-batch status in REVIEW_PROGRESS.md.

Update Status to "Phase 4 -- Antagonizing".

---

## Phase 4: Antagonize (Full Reviews Only)

**Goal**: Self-assess the review for accuracy, gaps, bias, and exemplar quality before presenting to the user.

Load [antagonist-protocol.md](references/antagonist-protocol.md) for the complete protocol.

### Full Review Protocol

1. **Accuracy audit**: Classify claims (critical/supporting/contextual), verify critical claims against sources
2. **Coverage assessment**: Each research goal addressed at appropriate depth
3. **Source independence**: Critical claims supported by independent sources
4. **Bias detection**: Year, journal, author, geographic, methodology, results biases
5. **Opposing viewpoint search**: Execute 2-3 critique-oriented queries
6. **Exemplar validation**: Confirm exemplars are best available

### User-Designated Exemplar Handling

Phase 4 can flag but not unilaterally demote user-designated exemplars. If issues are found, present to user via AskUserQuestion with options: keep as exemplar, reclassify as supporting, or remove.

### Demoted Exemplar Handling

When any exemplar is demoted:
- Move to "Demoted Exemplars" subsection in Literature_Review.md (retain Level 4 data)
- Remove evidence table row, add demotion note
- Phase 5 rebuilds evidence table after all demotions/promotions

### Narrow Search Protocol

Abbreviated version: accuracy check (critical claims only), coverage check (primary question answered), source independence (2+ independent sources for primary finding).

Write critique summary to REVIEW_PROGRESS.md Antagonistic Review section. Update Status to "Phase 5 -- Synthesizing".

---

## Phase 5: Synthesize

**Goal**: Produce final deliverables and present to the user.

### Step 5a: Structural Validation

Before final output:
- If Phase 4 produced any exemplar demotions or promotions, **rebuild the evidence table**
- Verify all papers in Paper Tracking table have a corresponding entry in Literature_Review.md
- Verify all DOIs have verification status
- Verify Core Concepts coverage is documented

### Step 5b: Complete Literature_Review.md

Finalize:
- Key Methodological Insights synthesis
- Quantitative Summary (effect sizes across studies)
- Gaps and Limitations (including Literature Density classification if Sparse)
- References in Vancouver format

**Thin literature framing**: If Literature Density is Sparse, include: "Despite comprehensive search across N sources with M queries, only K relevant papers were identified. The high convergence rate (X%) suggests this reflects genuine literature sparsity rather than search inadequacy."

### Step 5c: Finalize REVIEW_PROGRESS.md

Update:
- Status to "Phase 5 -- Complete"
- All paper tracking statuses to final values
- Gaps Identified table
- Output Files checklist

### Step 5d: Update INDEX.md

Update the review's row: Status = Complete, Papers = final count, Key Finding = one-line summary.

### Step 5e: Present to User

**Recall calibration**: Narrow searches recover core on-topic papers (validation: 100% of the directly relevant methodology cluster) but not the full set of papers a manuscript author eventually cites for context, adjacent evidence, or methodological utilities (validation: 29.6% overall recall against a published reference list). Users should treat narrow search results as a strong starting point for the primary question, not a complete manuscript bibliography.

Provide:
1. Summary of findings (3-5 key points)
2. Exemplar papers with brief justification
3. Evidence table (for full reviews)
4. Identified gaps
5. Antagonistic review findings (for full reviews)
6. Links to all output files

---

## Mode Comparison

| Feature | Narrow Search | Full Review |
|---------|--------------|-------------|
| Target papers | 8-14 | 30-48+ |
| Source types | Web + grey lit + available MCP | All 6 |
| Core Concepts | 2-3 concepts | 3-5 concepts |
| Exemplar extraction | Level 3 | Level 3-4 with evidence table |
| Antagonistic review | Abbreviated | Full protocol |
| Phase 4 | Abbreviated | Complete |
| Round cap | 3 | 5 |
| Typical sessions | 1 | 2-4 |

---

## State Management

All state is persisted in markdown files. The skill reconstructs its understanding from files on every invocation -- it never assumes in-memory state persists.

See [state-management.md](references/state-management.md) for:
- Phase detection logic
- Resume protocol
- Multi-review disambiguation
- Mode upgrade protocol
- Per-paper processing status tracking
- Planned query persistence for resume
