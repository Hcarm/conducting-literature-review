# State Management Reference

How the skill tracks progress and enables resume functionality. Multi-session operation is the default for full reviews, not an edge case.

---

## State Tracking Philosophy

All state is persisted in markdown files within the review subfolder. The skill never assumes in-memory state persists across sessions. On every invocation, the skill reconstructs its understanding from files alone.

---

## Two-Tier State Architecture

### INDEX.md (Project-Level Master)

Tracks all reviews across the project. Located at `Literature/INDEX.md`.

| Field | Purpose |
|-------|---------|
| Date | When the review was started |
| Topic | Brief description |
| Mode | Narrow Search or Full Review |
| Status | In Progress, Complete, Abandoned |
| Papers | Count of papers found |
| Key Finding | One-line summary of main finding |

### REVIEW_PROGRESS.md (Per-Review State)

Tracks the current state of a single review. Located at `Literature/YYYY-MM-DD_topic-slug/REVIEW_PROGRESS.md`. This is the primary state file that drives resume, phase detection, and multi-session continuity.

---

## Phase Detection Logic

On resume, the skill reads REVIEW_PROGRESS.md and determines the current phase:

| Phase | Detection Signal |
|-------|-----------------|
| Phase 0 (Initializing) | Status line says "Phase 0"; Core Concepts table empty |
| Phase 1 (Interview) | Status line says "Phase 1"; Core Concepts table empty or incomplete; Research Goals may be partially filled |
| Phase 2 (Searching) | Status line says "Phase 2"; Core Concepts table populated; Search Status table has at least one source "In Progress" or "Complete" |
| Phase 3 (Organizing) | Status line says "Phase 3"; All sources in Search Status are "Complete" or "Skipped"; Paper Tracking table has entries |
| Phase 4 (Antagonizing) | Status line says "Phase 4"; Literature_Review.md exists with exemplar/supporting entries |
| Phase 5 (Synthesizing) | Status line says "Phase 5"; Antagonistic Review section is completed |

### Phase 2 Sub-State Detection

Within Phase 2, determine which source types remain:

1. Read Search Status by Source table
2. Skip sources with Status = "Complete" or "Skipped"
3. Resume the first source with Status = "In Progress" or "Pending"
4. For "In Progress" sources: read planned queries from Search_Methods.md, diff against executed queries, execute remaining

### Phase 3 Sub-State Detection

Within Phase 3, determine which papers remain:

1. Read Paper Tracking table Status column
2. Papers with Status = "Candidate" or "Included" need Phase 3A triage
3. Papers with Status = "Included" but not "Level-2-Complete" need Phase 3B processing
4. Exemplar papers without "Level-3-Complete" or "Level-4-Complete" need Phase 3C processing
5. If any papers have been processed but no evidence table exists, Phase 3D is pending
6. If DOI verification has not run, Phase 3E is pending

---

## Resume Protocol

### Step 1: Detect Existing State

On invocation, check for `Literature/INDEX.md`:
- If INDEX.md exists: read it, check for in-progress reviews
- If no INDEX.md: this is a new project with no prior reviews

### Step 2: Handle Multiple In-Progress Reviews

When INDEX.md contains multiple reviews with Status = "In Progress":

Present to user via AskUserQuestion:
> "You have N reviews in progress:
> 1. [Topic A] (started [date], N papers found)
> 2. [Topic B] (started [date], N papers found)
> Which would you like to continue, or would you like to start a new review?"

Do not default to "most recent" -- always ask when multiple are in progress.

### Step 3: Resume or Start Fresh

If one in-progress review exists, present options:
1. **Resume**: Continue from where the review left off
2. **Start Fresh**: Create a new review (previous review remains accessible)

### Step 4: On Resume

1. Re-read all state files: REVIEW_PROGRESS.md, Search_Methods.md, Literature_Review.md (if exists)
2. Detect current phase using Phase Detection Logic above
3. Report to user: "Resuming review on [topic]. Currently at Phase [N]: [phase name]. [Brief status summary]."
4. Continue from next action in the detected phase

---

## State Update Triggers

Update REVIEW_PROGRESS.md:
- After completing interview (Phase 1 complete)
- After each search round (paper tracking, search status, convergence)
- Before starting each source type ("In Progress" status)
- After completing each source type ("Complete" status)
- After processing each paper (status column update)
- After antagonistic review (Phase 4 section filled)
- After generating final outputs (Phase 5 complete)

---

## Planned Query Persistence

When a source type begins in Phase 2:

1. Generate the planned query list based on Core Concepts and query generation rules
2. Write the planned queries to Search_Methods.md BEFORE executing the first query
3. After each query executes, move it from "Remaining" to "Executed"
4. On resume: diff planned vs. executed to identify remaining queries

This enables resume after interruption without regenerating the query plan.

---

## Per-Paper Processing Status

The Paper Tracking table Status column provides granular tracking:

| Status Value | Meaning |
|-------------|---------|
| Candidate | Found but not yet triaged |
| Included | Passed triage, queued for processing |
| Excluded | Failed relevance screening or deduplication |
| Level-2-Complete | Summary and quality note written (Phase 3B) |
| Level-3-Complete | All Paper_Entry.md fields populated (Phase 3C) |
| Level-4-Complete | Deep extraction populated from full text (Phase 3C) |
| Processed | Fully processed and added to Literature_Review.md |

---

## Mode Upgrade Protocol

Mode upgrade (narrow to full) is supported at user checkpoints:

1. User requests upgrade or skill suggests it based on question complexity
2. Update REVIEW_PROGRESS.md mode to "Full Review"
3. Expand search budgets to full review targets
4. Conduct supplementary interview questions (the full review questions not asked during narrow mode)
5. Expand Phase 4 from abbreviated to complete antagonistic review
6. Phase 2 progress is retained -- completed sources count toward expanded budgets

Mode downgrade (full to narrow) is not supported after search has begun.

---

## Output Files and Their Creation Points

| File | Created When | Updated By |
|------|-------------|------------|
| INDEX.md | Phase 0 (if not exists) | Phase 0 (new row), Phase 5 (status update) |
| REVIEW_PROGRESS.md | Phase 0 | Every phase (ongoing state) |
| Search_Methods.md | Phase 2 (first search round) | Phase 2 (each round) |
| Literature_Review.md | Phase 3 (first paper processed) | Phase 3 (each paper), Phase 4 (corrections), Phase 5 (synthesis) |
| Full_text_references/ | Phase 0 (folder created) | User-managed (PDF storage) |

---

## File Structure

```
[Project]/Literature/
├── INDEX.md
└── YYYY-MM-DD_topic-slug/
    ├── REVIEW_PROGRESS.md
    ├── Search_Methods.md
    ├── Literature_Review.md
    └── Full_text_references/
```

---

## Manual State Editing

Users may edit REVIEW_PROGRESS.md directly. The skill accepts reasonable edits and re-syncs on next invocation:
- Adding or removing papers from the tracking table
- Changing exemplar designations
- Updating status values
- Adding session notes

The skill validates structural consistency on resume but does not reject user edits.

---

## Error Recovery

If state files are corrupted or inconsistent:

1. Report the inconsistency to the user
2. Offer to reconstruct from available files (e.g., rebuild tracking table from Literature_Review.md entries)
3. If unrecoverable, offer to start fresh (preserving the corrupted review in its subfolder)
