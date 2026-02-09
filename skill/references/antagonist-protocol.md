# Antagonistic Review Protocol

Self-assessment process performed BEFORE presenting results to the user (Phase 4). The antagonistic review identifies gaps, biases, and potential errors. Full reviews receive the complete protocol; narrow searches receive an abbreviated version.

---

## Overview

The antagonistic review asks: "If a hostile reviewer were reading this literature review, what would they criticize?" This produces a critique report that is either addressed (by revising the review) or transparently disclosed to the user.

---

## Step 1: Accuracy Audit

### Claim Classification

Classify every claim in Literature_Review.md:

| Type | Definition | Verification Intensity |
|------|-----------|----------------------|
| **Critical** | Claims that, if wrong, would undermine the user's research direction | Full verification: check original source |
| **Supporting** | Claims that add context but are not foundational | Verify citation exists and summary is accurate |
| **Contextual** | Background framing; common knowledge in the field | No verification required unless challenged |

### Verification Checklist (per paper)

- [ ] Citation matches the actual paper (correct authors, year, title, journal)
- [ ] Summary accurately represents the paper's findings (not selectively quoted)
- [ ] Effect sizes and confidence intervals are correctly reported
- [ ] Quality note identifies genuine strengths and limitations
- [ ] DOI verified via verify_citations.py

---

## Step 2: Coverage Assessment

For each research goal identified in REVIEW_PROGRESS.md:

| Research Goal | Addressed? | Depth | Gap? |
|--------------|------------|-------|------|
| {{goal}} | Yes / Partial / No | Strong / Moderate / Weak | {{describe gap}} |

### Core Concepts Coverage

Verify each concept has reached its Target Depth:
- Strong: multiple high-quality papers
- Moderate: at least one good paper
- Any: at least mentioned

Report any concepts below their target depth.

---

## Step 2.5: Source Independence Check

For each critical claim, assess source independence:

| Critical Claim | Sources | Independence Groups | Flag |
|----------------|---------|--------------------|----|
| {{claim}} | {{papers supporting}} | {{group by author network, institution, dataset}} | {{independent / dependent}} |

**Independence group methodology**:
- Papers from the same research group = one independence group
- Papers using the same dataset = one independence group
- Papers that cite each other in a citation chain = partially dependent

Flag critical claims supported by only one independence group.

---

## Step 3: Bias Detection

Check each bias type:

### Publication Year Bias
- Is the literature skewed toward one time period?
- Are foundational older papers included alongside recent work?

### Journal Bias
- Are papers from a diverse set of journals?
- Is there over-reliance on one journal or publisher?

### Author/Network Bias
- Is the review dominated by one research group or collaboration?
- Are competing perspectives from different groups represented?

### Geographic Bias
- Are findings from multiple countries or health systems?
- If single-country, is that appropriate for the research question?

### Methodology Bias
- Are both quantitative and qualitative perspectives represented (where relevant)?
- Is there over-reliance on one study design?

### Results Bias
- Are negative/null results included?
- Are limitations and failures of interventions represented?

---

## Step 4: Opposing Viewpoint Check

Search explicitly for papers that contradict or challenge the dominant findings:

1. Generate critique-oriented queries: "limitations of [intervention]", "critique of [method]", "failure of [approach]"
2. Execute 2-3 opposing viewpoint queries
3. Document findings: either opposing viewpoints exist (include them) or no credible opposition was found (document the absence)

---

## Step 5: Exemplar Validation

### For All Exemplars

Ask: "Are these truly the best available papers for this topic?"

- Compare each exemplar against quality criteria (quality-criteria.md)
- Check if any supporting papers are stronger than current exemplars
- Verify exemplar designations are justified in the "Why Exemplar" field

### User-Designated Exemplar Demotion Protocol

Phase 4 can **flag but not unilaterally demote** user-designated exemplars:

1. If the antagonistic review identifies methodological problems with a user-designated exemplar (weak identification strategy, underpowered, selective reporting, superseded by better work):
2. Produce a recommendation: "User-designated exemplar [Paper] has [limitation]. Recommend reclassification to supporting paper. Defer to user."
3. Present to user via AskUserQuestion: "The antagonistic review identified potential issues with your designated exemplar [Paper]: [issues]. Would you like to: (a) Keep it as exemplar, (b) Reclassify as supporting paper, (c) Remove it from the review?"
4. User decision is final.

### Demoted Exemplar Handling

When an exemplar is demoted (user-designated or skill-identified):

1. **Retain Level 4 data**: Move to "Demoted Exemplars" subsection within the relevant topic section of Literature_Review.md
2. **Document reason**: Record the demotion reason in the entry
3. **Update evidence table**: Remove the row and add note: "Originally designated exemplar; demoted during antagonistic review due to [reason]."
4. **Phase 5 trigger**: If any demotions or promotions occurred during Phase 4, Phase 5 must rebuild the evidence table before final output

---

## Step 6: Generate Critique Report

Produce a structured critique including:

1. **Accuracy issues found** (with corrections made)
2. **Coverage gaps** (with assessment of severity)
3. **Source independence concerns** (single-source critical claims)
4. **Bias indicators detected** (with mitigation taken)
5. **Opposing viewpoints** (included or absence documented)
6. **Exemplar validation** (confirmed, promoted, or demoted -- with tracking)
7. **Overall assessment**: Confidence level in the review's completeness

Write the critique summary to REVIEW_PROGRESS.md Antagonistic Review section.

---

## Abbreviated Protocol (Narrow Searches)

For narrow searches, perform a reduced version:

1. **Accuracy check**: Verify critical claims only (skip contextual)
2. **Coverage check**: Primary question answered? Key gap identified?
3. **Source independence**: At least 2 independent sources for primary finding
4. **Skip**: Full bias detection, opposing viewpoint search, exemplar validation

---

## When to Iterate vs. Accept Gaps

### Iterate When:
- Critical claims have no independent verification
- A clear opposing viewpoint exists but is not represented
- An exemplar paper has undetected quality issues

### Accept Gap When:
- Literature is genuinely thin (Literature Density: Sparse)
- Opposing viewpoints do not exist for a well-established finding
- A gap is documented and the user acknowledges it

---

## Transparency Principles

- Never suppress negative findings about the user's favored approach
- Report all single-source critical claims, even if the source appears strong
- Document search limitations honestly (servers unavailable, paywalled content, thin literature)
- Present the critique report to the user; do not silently correct errors without disclosure
