# How the Skill Works

An end-to-end walkthrough of what happens when you type `/conducting-literature-review` in Claude Code.

---

## Invocation

When you type `/conducting-literature-review`, Claude Code:

1. Locates `~/.claude/skills/conducting-literature-review/SKILL.md` (via the symlink)
2. Reads the YAML frontmatter to determine which tools the skill can use
3. Loads the skill instructions into the conversation context
4. The agent follows the 6-phase pipeline defined in SKILL.md

The reference modules (`references/*.md`) and templates (`templates/*.md`) are **not** loaded at invocation. They are loaded on demand when the relevant phase or source type executes. This conserves context window tokens.

---

## Phase 0: Initialize

**Goal**: Verify infrastructure and prepare the review folder.

1. **Permission check**: Tests whether WebSearch and WebFetch are available. Reports impact if denied.
2. **MCP health check**: Sends a minimal test query to each MCP server:
   - PubMed: `pubmed_search_articles(queryTerm="test", maxResults=1)`
   - Semantic Scholar: `paper_relevance_search(query="test", limit=1)`
   - Classifies each as Available, Rate-Limited, or Unavailable
3. **Existing review check**: Looks for `Literature/INDEX.md` in the current project. If in-progress reviews exist, offers Resume or Start Fresh.
4. **Folder creation**: Creates `Literature/YYYY-MM-DD_topic-slug/` with REVIEW_PROGRESS.md from the template.

---

## Phase 1: Interview

**Goal**: Understand the user's research needs well enough to search effectively.

The skill loads `references/interview-questions.md` for question banks and follows this sequence:

1. **Mode selection**: User chooses Narrow Search (8-14 papers) or Full Review (30-48+ papers).
2. **Artifact intake**: User provides existing documents (Specific Aims, manuscript drafts, IRB applications, known exemplar papers, reference lists, project code). The skill extracts structured inputs from each.
3. **Core Concepts extraction**: Helps the user decompose their research question into 2-5 Core Concepts, each with search terms, cross-disciplinary variants, and a target depth (Strong/Moderate/Any). Core Concepts replaces PICO as the universal search scaffold while preserving PICO's functional roles for clinical questions.
4. **Interview completion**: Continues asking questions until the research question is clear, scope boundaries are established, and depth requirements are set.

All findings are documented in REVIEW_PROGRESS.md before proceeding.

### Why Core Concepts instead of PICO

PICO (Population, Intervention, Comparison, Outcome) works for clinical therapy questions but fails for methodological, cross-disciplinary, and exploratory questions. Core Concepts provides the same five functional roles (decomposition, term generation, completeness checking, reproducibility, scope control) with a universal structure. For clinical questions, the skill recommends PICO dimensions as concept labels.

---

## Phase 2: Search

**Goal**: Find relevant papers across multiple source types.

The skill loads `references/search-strategies.md` for the search execution protocol, then loads source-specific modules on demand.

### Query generation

From the Core Concepts table, the skill generates five query types:
1. Single-concept queries (each concept independently)
2. Cross-concept queries (pairwise or three-way combinations)
3. Variant queries (cross-disciplinary terminology)
4. Free-form queries (natural language)
5. Negative-framing variants (for critique/limitation questions)

All planned queries are written to Search_Methods.md **before** execution begins. This enables resume after interruption.

### Source type execution order

| Order | Source | Module Loaded | Narrow? | Full? |
|-------|--------|--------------|---------|-------|
| 1 | Web search | search-web.md | Yes | Yes |
| 2 | Grey literature | search-grey-literature.md | As needed | Yes |
| 3 | PubMed | search-pubmed.md | No | Yes |
| 4 | Semantic Scholar | search-semantic-scholar.md | No | Yes |
| 5 | Citation chaining | search-citation-chaining.md | If seeds exist | Yes |
| 6 | Seed-based recommendation | search-recommendations.md | If seeds exist | Yes |

**Why this order**: Source 6 (recommendations) runs last to prevent biasing upstream keyword search. Citation chaining (source 5) runs after keyword search to use discovered papers as seeds.

### Stopping criteria

Applied in priority order:
1. Budget exhaustion (hard stop; asks user for extension)
2. Convergence (>80% overlap with existing candidates)
3. Round cap (3 narrow / 5 full)
4. All source types complete

### User checkpoint

After rounds 2-3, the skill presents: total papers, concept coverage, convergence rate, quality impression, and the option to upgrade from narrow to full review.

---

## Phase 3: Organize

**Goal**: Process candidates into a structured annotated bibliography.

The skill loads `references/quality-criteria.md` for processing rules.

### Sub-steps

**3A -- Triage and Deduplication**: Remove duplicates (DOI primary, fuzzy title fallback), fetch missing metadata, screen on relevance. User-designated exemplars bypass relevance screening.

**3B -- Process Supporting Papers**: Write Level 2 annotation (1-2 sentence summary, quality note). Detect promotions -- if a supporting paper meets exemplar criteria, flag it for 3C.

**3C -- Process Exemplar Papers**: Retrieve content via fallback chain (MCP metadata -> user PDF -> WebFetch full text -> WebFetch abstract -> flag for user). Write Level 3 annotation (all Paper_Entry.md fields). Write Level 4 deep extraction if full text is available.

**3D -- Build Evidence Table**: Compile from Level 4 fields per topic section.

**3E -- Citation Verification**: Run `verify_citations.py` to check DOIs against CrossRef.

### Processing levels

| Level | Content | Used For |
|-------|---------|----------|
| Level 1 | Citation metadata only | Tracking table entries |
| Level 2 | Citation + summary + quality note | Supporting papers |
| Level 3 | All Paper_Entry.md fields | Exemplar papers |
| Level 4 | Deep extraction from full text | Exemplar papers (when full text available) |

### Batched processing

When candidates exceed 50, processing operates in batches of ~25. Each batch completes 3A-3B before the next begins. Phase 3C processes all exemplars after all batches complete.

---

## Phase 4: Antagonize

**Goal**: Self-assess the review before presenting it.

The skill loads `references/antagonist-protocol.md` for the complete protocol.

**Full reviews** receive the complete protocol:
1. **Accuracy audit**: Classify claims (critical/supporting/contextual), verify critical claims against sources
2. **Coverage assessment**: Each research goal addressed at target depth
3. **Source independence**: Critical claims supported by independent research groups
4. **Bias detection**: Publication year, journal, author network, geographic, methodology, results biases
5. **Opposing viewpoint search**: Execute 2-3 critique-oriented queries
6. **Exemplar validation**: Confirm exemplars are the best available papers

**Narrow searches** receive an abbreviated version: accuracy check (critical claims only), coverage check, source independence (2+ independent sources).

### Why antagonistic review exists

LLM-conducted reviews have known weaknesses: confirmation bias (favoring the user's expected answer), selective reporting (overweighting positive results), and gap blindness (not recognizing what is missing). Phase 4 explicitly adopts an adversarial perspective to counteract these tendencies.

### User-designated exemplar handling

Phase 4 can flag issues with user-designated exemplars but cannot unilaterally demote them. The user makes the final decision via AskUserQuestion.

---

## Phase 5: Synthesize

**Goal**: Produce final deliverables and present results.

1. **Structural validation**: Rebuild evidence tables if exemplars were demoted/promoted. Verify cross-references.
2. **Complete Literature_Review.md**: Finalize Key Methodological Insights, Quantitative Summary, Gaps and Limitations.
3. **Update state files**: Finalize REVIEW_PROGRESS.md, update INDEX.md status.
4. **Present to user**: Summary, exemplars with justification, evidence table, gaps, antagonistic findings, links to output files.

### Recall calibration

Narrow searches recover core on-topic papers (validated at ~100% of the directly relevant methodology cluster) but not the full set of papers a manuscript author cites for context (validated at ~30% overall recall against a published reference list). Users should treat results as a strong starting point, not a complete bibliography.

---

## Multi-Session Operation

Full reviews typically span 2-4 Claude Code sessions. The skill persists all state in markdown files:

- **REVIEW_PROGRESS.md**: Phase status, paper tracking, search budgets, convergence
- **Search_Methods.md**: Planned vs. executed queries
- **Literature_Review.md**: Processed papers with annotations

On re-invocation, the skill reads these files and reconstructs its position. It does not assume any in-memory state persists. The phase detection logic (in `references/state-management.md`) determines where to resume based on the Status field and table contents.

---

## Output Files

| File | Created | Purpose |
|------|---------|---------|
| `Literature/INDEX.md` | Phase 0 | Master index of all reviews in the project |
| `Literature/YYYY-MM-DD_topic/REVIEW_PROGRESS.md` | Phase 0 | Per-review state tracking |
| `Literature/YYYY-MM-DD_topic/Search_Methods.md` | Phase 2 | Query plan and execution log |
| `Literature/YYYY-MM-DD_topic/Literature_Review.md` | Phase 3 | Final annotated bibliography with evidence tables |
| `Literature/YYYY-MM-DD_topic/Full_text_references/` | Phase 0 | User-managed folder for PDF storage |

---

## Graceful Degradation

The skill adapts to any combination of infrastructure failures:

| Scenario | Impact | The Skill Does |
|----------|--------|----------------|
| PubMed unavailable | No MeSH-indexed search | Uses Semantic Scholar + web search |
| Semantic Scholar unavailable | No citation graph | Uses PubMed + web search |
| Both MCP servers unavailable | No database search | Web search + grey literature only |
| WebSearch unavailable | No web discovery | Database APIs only |
| All sources unavailable | Minimal capability | Reports limitation; user provides papers manually |

The skill always reports what is degraded and why. No silent failures.
