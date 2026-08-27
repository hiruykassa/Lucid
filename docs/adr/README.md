# Architecture Decision Records

An ADR captures one decision, at the moment it was made, with the information available
at the time. It is not documentation of how the system works — that's `docs/design/`.
It is a record of *why the system is not something else*.

## Rules

- One decision per ADR. If you're writing about two, you have two ADRs.
- Numbered sequentially, never renumbered, never deleted. A decision that turned out
  wrong gets **superseded** by a new ADR that links back to it. The wrong one stays.
  The trail of reversals is the most interesting thing in this directory.
- Written *before* the code, not after. An ADR written after implementation is a
  justification, and everyone can tell.
- Hiruy drafts. Claude reviews. The review will focus on the options dismissed fastest.
- **Only the reviewer flips Status to Accepted.** Do not self-accept.

## The backlog

| ADR | Decision | Status | Blocks |
|---|---|---|---|
| [0001](0001-vector-store.md) | Vector store | **Accepted** | All ingest and retrieval work |
| [0002](0002-bedrock-models.md) | Embedding + generation models | **Accepted** (invoke verified 2026-08-21) | Ingest, generation, cost model |
| [0003](0003-corpus-selection.md) | Which papers, and under what license | **Accepted** (sizing superseded by 0004) | Everything downstream of ingest |
| [0004](0004-corpus-eval-resizing.md) | Corpus and eval set sizing under measured capacity | **Approved** 2026-08-27 | S3 collection, S6 eval set |

**S1 gate (from `docs/PLAN.md`):** **met** 2026-08-14. Three **Accepted** ADRs + billing
alarm test-fired (SNS `lucid-billing-alarms`, CloudWatch delivery 2026-08-13 15:13 UTC;
budget `My Monthly Cost Budget` $20/month). Bedrock invoke smokes **passed** 2026-08-21
(case 178659049300631 closed; RequestIds in ADR-0002). S2 skeleton still does not
need Bedrock.

## How a review goes

1. Hiruy writes the draft and says it's ready.
2. Claude reads it and pushes back — usually on an option dismissed in one sentence,
   a cost figure with no source, or a missing "what gets harder".
3. Hiruy revises or defends. Defending is a legitimate outcome. "I considered that and
   here's why I still disagree" is a better answer than silent compliance, provided
   the reasoning holds.
4. Status flips to Accepted. Only then does code get written.
