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

## The backlog

| ADR | Decision | Status | Blocks |
|---|---|---|---|
| [0001](0001-vector-store.md) | Vector store | Not started | All ingest and retrieval work |
| [0002](0002-bedrock-models.md) | Embedding + generation models | Not started | Ingest, generation, cost model |
| [0003](0003-corpus-selection.md) | Which papers, and under what license | Not started | Everything downstream of ingest |

## How a review goes

1. Hiruy writes the draft and says it's ready.
2. Claude reads it and pushes back — usually on an option dismissed in one sentence,
   a cost figure with no source, or a missing "what gets harder".
3. Hiruy revises or defends. Defending is a legitimate outcome. "I considered that and
   here's why I still disagree" is a better answer than silent compliance, provided
   the reasoning holds.
4. Status flips to Accepted. Only then does code get written.
