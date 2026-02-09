# Architecture

Design rationale for every component of the conducting-literature-review skill. This document explains **why** each design decision was made, not just what each component does. For operational details, see [docs/how-it-works.md](docs/how-it-works.md).

---

## Why 6 Phases

The skill decomposes literature review into six phases: Initialize, Interview, Search, Organize, Antagonize, Synthesize. Each phase exists because omitting it produces a measurably worse review.

**Initialize** exists because full reviews span multiple sessions. Without health checks and state detection at startup, the skill would either re-do completed work or attempt to use unavailable infrastructure.

**Interview** exists because searching without understanding the question produces irrelevant results. The interview captures the user's actual needs (which may differ from their initial framing), identifies artifacts that seed the search, and builds the Core Concepts table that governs all subsequent queries. Skipping the interview is the fastest way to produce a useless review.

**Search** exists as a separate phase (rather than interleaving search and organization) because the search budget and stopping criteria require a global view of discovery across all source types. Interleaving would make convergence assessment impossible.

**Organize** exists because raw search results require deduplication, relevance screening, and structured annotation before they are useful. The three processing levels (Level 2 supporting, Level 3 exemplar, Level 4 deep extraction) allocate annotation effort proportionally to paper importance.

**Antagonize** exists because LLM-conducted reviews have systematic weaknesses: confirmation bias (favoring the user's expected answer), selective reporting (overweighting positive results), and gap blindness (not recognizing what is missing). Phase 4 explicitly adopts an adversarial stance to counteract these tendencies. Removing Phase 4 saves time but produces reviews with undetected biases.

**Synthesize** exists as a distinct phase because structural validation (rebuilding evidence tables after exemplar demotions/promotions) and recall calibration (setting user expectations) are critical to output quality and should not be interleaved with processing.

---

## Why Core Concepts Instead of PICO

PICO (Population, Intervention, Comparison, Outcome) is the standard search framework in evidence-based medicine. It works well for clinical therapy questions but breaks down for:

- **Methodological questions** ("What methods exist for adjusting regression to the mean?") -- there is no population, intervention, or comparison
- **Cross-disciplinary questions** ("How do econometric IV methods apply to clinical QI evaluation?") -- the "intervention" is a concept from one field applied in another
- **Exploratory questions** ("What approaches exist for physician attribution in value-based payment?") -- the scope is too broad for PICO's specificity

Core Concepts preserves PICO's five functional roles (decomposition, term generation, completeness checking, reproducibility, scope control) while supporting any question type. For clinical therapy questions, the skill recommends PICO dimensions as concept labels, so PICO users lose nothing.

---

## Why Demand-Loaded References

The 12 reference modules in `references/` total approximately 75 KB (~19,000 tokens). Loading all of them into the context window at skill invocation would consume significant capacity for no benefit -- most modules are relevant to only one phase or source type.

Instead, SKILL.md contains markdown links (`[search-strategies.md](references/search-strategies.md)`) that the agent follows only when the relevant phase begins. This pattern:

- Conserves context window tokens (a finite resource)
- Allows each module to be comprehensive without a brevity penalty
- Enables updates to individual modules without touching SKILL.md
- Keeps SKILL.md readable as a high-level workflow overview

---

## Why File-Based State

Claude Code sessions end unpredictably (user closes terminal, context window fills, network interruption). Full reviews span 2-4 sessions. Any architecture that relies on in-memory state across sessions fails.

The skill persists all state in three markdown files (REVIEW_PROGRESS.md, Search_Methods.md, Literature_Review.md). On every invocation, it reads these files and reconstructs its position. This design means:

- No database or external storage is required
- State files are human-readable and human-editable
- Users can manually adjust state between sessions (e.g., add papers, change exemplar designations)
- Corrupted state is recoverable by reading the remaining intact files
- The skill works in any project without configuration

---

## Why Source Ordering Matters

The six source types execute in a fixed order: web search, grey literature, PubMed, Semantic Scholar, citation chaining, seed-based recommendation.

**Seed-based recommendation runs last** (source 6). Recommendations use exemplar papers as seeds to find semantically similar work. If recommendations ran before keyword search, the recommended papers would influence the user's perception of the literature and bias subsequent keyword query construction. Running last ensures keyword-based discovery is independent.

**Citation chaining runs after keyword search** (source 5). Citation chaining requires seed papers, which emerge from keyword search in sources 1-4. Running chaining earlier would have no seeds.

**Web search runs first** (source 1). Web search provides the broadest cross-source coverage and identifies terminology that informs subsequent database queries. It also surfaces grey literature that MeSH-indexed databases miss.

---

## Why Two MCP Servers

PubMed and Semantic Scholar provide complementary capabilities:

**PubMed** provides MeSH-indexed biomedical literature with structured abstracts. MeSH (Medical Subject Headings) is a controlled vocabulary that enables precision searches impossible with keyword matching alone. PubMed also provides Similar Articles (the `pubmed_similar_articles` relationship type), which covers the full 36M+ citation corpus with no time restriction.

**Semantic Scholar** provides a broader citation graph covering 200M+ papers across all disciplines. In validation testing, Semantic Scholar's forward citation chaining (`paper_citations`) found papers that PubMed's ELink service missed entirely. Semantic Scholar's citation database has broader journal coverage than PubMed's.

Neither alone is sufficient. PubMed lacks broad citation graph coverage. Semantic Scholar lacks MeSH-indexed precision and has unreliable keyword search. Together, they cover both precision search and broad citation discovery.

---

## Why Graceful Degradation

Academic API infrastructure is unreliable. During validation testing:

- Semantic Scholar keyword search returned HTTP 429 on every attempt
- PubMed's `pubmed_citedin` returned 0 results for well-cited papers

The skill cannot assume both servers are available. It defines compound failure modes:

| Servers Available | Capability |
|-------------------|------------|
| Both | Full pipeline |
| PubMed only | No citation graph; keyword + similar articles |
| S2 only | No MeSH precision; DOI lookup + citation chaining |
| Neither | Web search + grey literature only |
| WebSearch also down | Manual input only |

Each degradation level produces a usable (if reduced-quality) review. The skill always reports what is degraded and why, so the user understands the limitations. No silent failures.

---

## Why Vancouver Citation Format

Vancouver format (numbered references with DOIs) is the standard in biomedical literature. Numbered references:

- Enable precise cross-referencing within evidence tables
- Work with the `verify_citations.py` script for automated DOI verification via CrossRef
- Are the expected format for manuscript drafting in most medical journals

---

## Why Templates as Separate Files

The `init_review.py` script reads templates at runtime from the `templates/` directory rather than embedding template content in the script. This design:

- **DRY principle**: Template content exists in one place. Updating a template field updates all future reviews.
- **Separation of concerns**: The script handles folder creation logic; templates handle content structure.
- **Human readability**: Templates are plain markdown files that anyone can read, understand, and modify.
- **Symlink compatibility**: `Path(__file__).resolve().parent.parent / "templates"` follows the symlink chain, so templates are always found regardless of where the repo is cloned.

---

## Why Exemplar Designations

Not all papers in a review deserve equal annotation effort. The three-tier system (supporting, exemplar, primary exemplar) allocates effort proportionally:

- **Supporting papers** (Level 2): 1-2 sentence summary + quality note. Sufficient to understand what the paper contributes.
- **Exemplar papers** (Level 3-4): Full structured entry with deep extraction. These are the papers the user should read closely, model their methods after, or cite prominently.

This prevents the skill from spending equal time on every paper, which in a 40-paper review would be prohibitively expensive and produce diminishing returns.

---

## Why the Antagonistic Review

Phase 4 is the most unusual component and the one most tempting to skip. Its existence addresses three validated failure modes of LLM-conducted reviews:

1. **Confirmation bias**: The LLM tends to find evidence supporting the user's framing. Phase 4 explicitly searches for opposing viewpoints.
2. **Source dependence**: Multiple papers from the same research group do not provide independent confirmation. Phase 4 checks source independence for critical claims.
3. **Exemplar inertia**: Once a paper is designated as exemplar, the LLM tends to defend that designation. Phase 4 re-evaluates exemplars against quality criteria and can flag (though not unilaterally demote) user-designated exemplars.

For narrow searches, an abbreviated protocol (accuracy + coverage + independence) provides the most important protections with lower overhead.

---

## Why Scripts Use Stdlib Only

Both Python scripts (`init_review.py` and `verify_citations.py`) use only Python standard library modules. No `pip install` is required to run them. This design:

- Eliminates dependency on the user's Python environment (beyond Python 3 itself)
- Avoids conflicts with the Semantic Scholar MCP server's separate venv
- Ensures the scripts work on any machine with Python installed
- Makes the skill fully portable with zero installation for the scripts themselves
