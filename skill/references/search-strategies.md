# Search Strategies Reference

Source-agnostic search strategy framework. This file provides the Core Concepts methodology, query formulation approach, execution protocol, budget governance (single source of truth), sufficiency criteria, and documentation format. Source-specific strategies are in dedicated modules loaded on demand.

---

## Core Concepts Methodology

Core Concepts is the universal search scaffold for all question types. It replaces the PICO framework as the primary decomposition tool while preserving PICO's five functional roles: decomposition, term generation, completeness checking, reproducibility, and scope control.

### Framework

| Concept | Search Terms | Cross-Disciplinary Variants | Target Depth |
|---------|-------------|---------------------------|--------------|
| {{concept}} | {{term1, term2}} | {{field: variant term}} | {{Strong / Moderate / Any}} |

- **Minimum**: 2 concepts
- **Maximum**: 5 concepts
- **Depth enforcement**: At least one concept must have Target Depth of Moderate or Strong. If the user sets all concepts to Any, advise: "Setting all concepts to Any depth means the search will satisfy sufficiency criteria with minimal evidence. Consider setting at least one concept to Moderate to ensure meaningful coverage." If the user confirms all-Any, proceed but document: "All concepts set to Any depth by user choice. Sufficiency criteria are minimal."

### Target Depth Definitions

| Depth | Meaning |
|-------|---------|
| **Strong** | Multiple high-quality papers directly addressing this concept |
| **Moderate** | At least one good paper addressing this concept |
| **Any** | At least mentioned in the literature found |

### Question-Type Templates

The skill suggests decomposition templates based on question type. These are recommendations, not constraints.

| Question Type | Suggested Concept Labels | Example |
|---------------|-------------------------|---------|
| Clinical therapy | Population, Intervention, Comparison, Outcome (PICO) | P=ICU patients, I=audit and feedback, C=usual care, O=implementation cost |
| Methodological | Problem, Methods/Approaches, Application domain | Problem=regression to the mean, Methods=adjustment approaches, Application=QI evaluation |
| Cross-disciplinary hybrid | Domain A concept, Domain B concept, Bridging concept | IV estimation, Causal inference, Clinical QI |
| Exploratory/scoping | Topic, Measurement/approach, Context | Physician attribution, Measurement approaches, Value-based payment |

For clinical therapy questions, PICO dimensions are **recommended** as concept labels (not merely suggested). Clinical users produce stronger search structures with the familiar PICO framework.

---

## Query Generation from Core Concepts

### Query Types

1. **Single-concept queries**: Search each concept independently for broad discovery
2. **Cross-concept queries**: Combine concepts pairwise or three-way for targeted precision
3. **Variant queries**: Repeat using cross-disciplinary terminology variants from the Variants column
4. **Free-form queries**: Natural language formulation of the research question
5. **Negative-framing variants**: For questions seeking critical or negative evidence

### Negative-Framing Variant Generation

When the research question contains negative framing (evidence against, limitations of, critique of, failure of), apply negative-framing variants to ALL concepts, not only the concept explicitly framed as negative:

- Append to each concept's search terms: "limitations of [concept]", "critique of [concept]", "failure of [concept]", "unintended consequences of [concept]"
- This counteracts positive-result bias in keyword search
- Phase 4 opposing viewpoint search supplements but does not replace this mechanism

### Query Construction Examples

From Core Concepts table with concepts A and B (each with terms a1, a2 and b1, b2):

| Query Type | Example |
|------------|---------|
| Single-concept | `a1 a2` |
| Cross-concept | `a1 AND b1` |
| Variant | `[field_variant_of_a1] [field_variant_of_a2]` |
| Free-form | `"How does [concept A] relate to [concept B]?"` |
| Negative-framing | `"limitations of a1" OR "critique of a1"` |

---

## Search Execution Protocol

### Source-Type Modules

Before executing queries against a source type, load the relevant strategy module:

| Order | Source Type | Module | When to Use |
|-------|------------|--------|-------------|
| 1 | Web search | [search-web.md](search-web.md) | Always (primary discovery tool) |
| 2 | Grey literature | [search-grey-literature.md](search-grey-literature.md) | Always for full reviews; as needed for narrow |
| 3 | PubMed | [search-pubmed.md](search-pubmed.md) | Full reviews when MCP server is available |
| 4 | Semantic Scholar | [search-semantic-scholar.md](search-semantic-scholar.md) | Full reviews when MCP server is available |
| 5 | Citation chaining | [search-citation-chaining.md](search-citation-chaining.md) | When exemplar or high-relevance papers are identified |
| 6 | Seed-based recommendation | [search-recommendations.md](search-recommendations.md) | After sources 1-5 complete; runs last to avoid biasing upstream search |

### Round Structure

**Round 1: Broad Coverage**
1. Execute 3-5 primary queries from Core Concepts (single-concept and cross-concept)
2. Execute 1-2 grey literature queries
3. Identify potential exemplars and note terminology
4. Record planned queries for each source type BEFORE execution begins

**Round 2: Targeted Follow-up**
1. Use terminology from Round 1 papers
2. Execute cross-disciplinary variant queries
3. Fill concept coverage gaps
4. Add database search (PubMed, Semantic Scholar) if available

**Round 3+: Refinement (Full Reviews Only)**
1. Citation chaining from exemplars (source 5)
2. Seed-based recommendation (source 6)
3. Search for opposing viewpoints
4. Verify no major papers missed

**Round Cap**: Maximum 3 rounds for narrow search, 5 rounds for full review. If convergence has not reached 80% after maximum rounds, stop and report: "Search completed N rounds without reaching convergence (X% overlap in final round). This may indicate a broad or evolving literature."

### User Checkpoint (After Round 2 or 3)

Present candidate list to user with:
- Source type counts and budget status
- Concept coverage status (which concepts at which depth)
- Convergence rate
- Preliminary quality impression: "Initial assessment: [brief note on evidence quality, e.g., mostly pilot studies, limited RCTs, strong observational evidence]"
- Mode upgrade option (if narrow, offer upgrade to full)

### Incremental Persistence

After each source type completes:
1. Update Search_Methods.md with executed queries and results
2. Update REVIEW_PROGRESS.md Search Status by Source table
3. Update REVIEW_PROGRESS.md Paper Tracking table with new candidates
4. Write "In Progress" status BEFORE first query per source; update to "Complete" after last query

---

## Search Budget Governance

This is the SINGLE SOURCE OF TRUTH for search budgets. Other files reference this table; do not define budgets independently.

| Source Type | Narrow Search | Full Review |
|-------------|---------------|-------------|
| Web search | 5-8 papers | 10-15 papers |
| Grey literature | 1-3 papers | 5-8 papers |
| PubMed | -- | 10-15 papers |
| Semantic Scholar | -- | 10-15 papers |
| Citation chaining | 2-3 papers | 5-10 papers |
| Seed-based recommendation | 1-3 papers | 5-10 papers |

**Budget exhaustion is a hard stop.** When budget is exhausted with concept coverage gaps, report: "Search budget exhausted. Concept [X] has not reached [target] depth. Options: (a) Accept current coverage and proceed to Phase 3. (b) Extend search budget by [N] papers for targeted [concept] search." Present via AskUserQuestion. Default: accept and proceed, documenting the gap.

**Budget redistribution**: When a source type completes with zero relevant results, its remaining budget is available for additional queries on other source types, prioritized by sources with the most unfilled concept gaps.

**Throughput note**: Unauthenticated Semantic Scholar is limited to 100 requests per 5 minutes. Plan query volume accordingly. PubMed unauthenticated: 3 requests/second.

---

## Sufficiency Criteria

### Concept Coverage

Each core concept has reached its Target Depth:
- **Strong**: Multiple high-quality papers directly addressing this concept
- **Moderate**: At least one good paper
- **Any**: At least mentioned in the literature found

### Concept Intersection (Dual-Outcome Mode)

Each pair of adjacent concepts is assessed for connecting literature. Two resolution modes, both counting as "addressed" for sufficiency:

1. **Intersection Satisfied**: At least one paper connects the concept pair
2. **Intersection Gap Documented**: No connecting papers found. The skill asks the user: "No papers found connecting [Concept A] and [Concept B]. Is this a known gap in the literature, or should I search further?" If the user confirms the gap is expected (common in cross-disciplinary questions where the disconnect IS the finding), record as "Gap Documented" in REVIEW_PROGRESS.md Concept Intersection Status table. If the user wants further search, allocate targeted queries.

### Convergence

Successive search rounds produce >80% overlap with existing candidate list. Convergence calculation **excludes pre-populated references** from artifact intake -- compare only newly-discovered papers against the prior round's newly-discovered papers.

### Source Type Diversity

Full reviews: at least one grey literature source identified. If grey literature search produces zero results after exhaustive queries, the source diversity criterion is **waived** and the absence is documented: "Grey literature search produced zero relevant results. Source diversity criterion waived; absence documented as finding."

### Literature Density Classification

When convergence is high (>80%) but paper count is below the minimum budget target, classify as Literature Density: Sparse rather than search failure. Report in Phase 5: "Despite comprehensive search across N sources with M queries, only K relevant papers were identified. The high convergence rate (X%) suggests this reflects genuine literature sparsity rather than search inadequacy."

---

## Stopping Hierarchy

Applied in this priority order:

1. **Budget exhaustion** (hard stop; AskUserQuestion for extension)
2. **Convergence** (>80% overlap with existing candidates, excluding pre-populated)
3. **Round cap** (3 narrow / 5 full)
4. **All source types complete**

---

## Documentation Format

This format is the single definition for search round documentation. All source-type modules reference this format rather than defining their own.

For each search round, record in Search_Methods.md:

1. **Date** of search
2. **Source type**: Web search / Grey literature / PubMed / Semantic Scholar / Citation chaining / Seed-based recommendation
3. **Tool** used (WebSearch, WebFetch, pubmed_search_articles, paper_relevance_search, etc.)
4. **Strategy module** loaded (search-web.md, search-grey-literature.md, etc.)
5. **Queries executed** (exact text)
6. **Results**: N total, N new unique, N duplicates
7. **Key findings** (brief notes)
8. **Rationale for next round** (if applicable)
