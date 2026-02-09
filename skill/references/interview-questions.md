# Interview Questions Reference

Question banks for the interview phase. The skill asks questions until it has sufficient context to search effectively -- there is no fixed number of questions.

---

## Mode Selection (Always Start Here)

Present the user with two options:

1. **Narrow Search**: Quick answer to a specific question. Targets 8-14 papers across web + grey literature. Abbreviated antagonistic review.
2. **Full Review**: Comprehensive background for a project. Targets 30-48+ papers across all 6 source types. Full antagonistic review with exemplar validation.

---

## Artifact Intake (Before Questions)

Ask the user for existing project documents before beginning the question bank:

> "Do you have existing project documents I can read to inform this review? For example:
> - Specific Aims page
> - Manuscript draft or partial manuscript
> - IRB application
> - Known exemplar articles (papers you consider models)
> - An existing reference list
> - Project code"

### Per-Artifact Extraction

| Artifact | What the Skill Extracts |
|----------|------------------------|
| Specific Aims | Research question, significance framing (search scope), key terms, methodology keywords |
| Partial manuscript | Existing reference list with DOIs (seed papers), background framing (relevance criteria), methods section (methodology search terms) |
| IRB application | Study design, population, intervention/exposure, outcomes (direct concept extraction), significance section (search scope) |
| Known exemplar article | DOI for citation chaining and recommendation seeding, quality benchmark, reporting pattern to match |
| Existing reference list | DOIs for batch citation chaining, coverage baseline to search beyond |
| Project code | Packages/methods in use (methodological literature), variable names (domain terminology) |

### Artifact Follow-Up Questions

When the user provides a single paper as the starting artifact:
> "What is the relationship between this paper and your review goal?
> (a) I want to review the same topic this paper addresses
> (b) I want to use this paper's methods/approach for a different question
> (c) I want to find similar papers to this one"

When the user provides an existing reference list:
> "You provided an existing reference list. Do you want to:
> (a) Update this review with new literature (search beyond these references)
> (b) Use these as seeds for a new review on a related topic"

### DOI Extraction from Reference Lists

When extracting DOIs from formatted reference lists:
1. Attempt direct DOI parsing (regex for DOI patterns in reference text)
2. For references without explicit DOIs, search CrossRef or PubMed by title to retrieve DOIs
3. Record extraction confidence per reference

---

## Core Concepts Extraction

After artifact intake, help the user identify 2-5 core concepts with search terms and target depths.

### Step 1: Identify Question Type

Based on the research question (from interview or artifact):
- **Clinical therapy**: Patient/population, intervention, comparator, outcome
- **Methodological**: Problem/phenomenon, methods/approaches, application domain
- **Cross-disciplinary hybrid**: Domain A concept, Domain B concept, bridging concept
- **Exploratory/scoping**: Topic, measurement/approach, context

### Step 2: Suggest Decomposition Template

For clinical therapy questions, **recommend** PICO dimensions as concept labels:
> "For your clinical therapy question, I recommend using PICO dimensions as your core concepts: Population, Intervention, Comparison, and Outcome. PICO provides a familiar, well-tested structure for this type of question. Would you like to use PICO, or would you prefer a different decomposition?"

For methodological questions, suggest Problem/Approach/Domain:
> "For your methodological question, I suggest decomposing into: (1) the Problem or phenomenon, (2) the Methods or approaches, and optionally (3) the Application domain."

### Step 3: Build Core Concepts Table

For each concept:
1. Identify 2+ search terms
2. Identify cross-disciplinary variants (ask: "How would researchers in [other field] describe this?")
3. Set target depth (Strong / Moderate / Any)

**Minimum depth enforcement**: At least one concept must have Target Depth of Moderate or Strong. If the user sets all concepts to Any:
> "Setting all concepts to Any depth means the search will satisfy sufficiency criteria with minimal evidence. Consider setting at least one concept to Moderate to ensure meaningful coverage."

If the user confirms all-Any after this advisory, proceed but document in REVIEW_PROGRESS.md.

### Step 4: Validate Completeness

Confirm with user:
> "Here are your core concepts: [table]. Does this capture all the important dimensions of your research question? Is anything missing?"

---

## Narrow Search Essential Questions

1. **What specific question are you trying to answer?**
   - Map to Core Concepts immediately
2. **What context is this for?** (manuscript section, grant, methods decision, etc.)
3. **What do you already know?** (existing knowledge, known papers)

## Narrow Search Clarifying Questions (as needed)

4. What would a "good enough" answer look like?
5. Are there trusted sources or known exemplars?
6. What timeframe is relevant?

---

## Full Review Research Context Questions

1. **What is the research question?** (exact formulation)
2. **What key concepts need literature support?** (map to Core Concepts)
3. **What will this literature support?** (introduction, methods, discussion, all)

## Full Review Methodological Questions

4. **What methodological approaches are you considering?** (add to Core Concepts if not covered)
5. **Do you need exemplar papers?** (papers to model methodology/reporting)
6. **Are there known papers or authors?** (seeds for citation chaining)

## Full Review Scope Definition Questions

7. **What domains/fields should we search?** (feeds cross-disciplinary variants)
8. **What is NOT relevant?** (explicit exclusions)
9. **What timeframe is relevant?**
10. **What level of thoroughness do you need?** (informs budget allocation)

## Full Review Quality Criteria Questions

11. **What makes a paper high-quality for your purposes?** (calibrates exemplar criteria)
12. **Are there specific reporting standards relevant?** (CONSORT, STROBE, CHEERS, etc.)

---

## Interview Best Practices

- Ask open-ended questions first, then clarify with specific follow-ups
- Reflect back understanding before proceeding
- Do not assume the meaning of ambiguous terms -- ask
- Document goals in REVIEW_PROGRESS.md as you go
- Establish stopping criteria before searching
- Get explicit exclusions to prevent scope creep
- Record Core Concepts table in REVIEW_PROGRESS.md before proceeding to Phase 2
