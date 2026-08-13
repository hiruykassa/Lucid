# ADR-NNNN: <short title, a noun phrase — the decision, not the question>

- **Status:** Proposed | Accepted | Superseded by ADR-NNNN
- **Date:** YYYY-MM-DD
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

## Context

What forces this decision now? Constraints, not preferences: requirements, budget,
timeline, dependencies, scale. A reader new to the service should understand why a
decision is required.

State constraints as numbers where you can. "Cheap" is not a constraint. "Under
$15/month with no idle cost" is.

## Options considered

At least three. For each:

### Option A: <name>

- **How it works:** two sentences.
- **Cost:** idle cost and per-query cost, with a source for each figure.
- **Operational burden:** what breaks, who fixes it, how long to stand up.
- **Risks / downsides:** strongest argument against this option, in good faith.

### Option B: <name>

### Option C: <name>

## Decision

The option chosen, in one sentence, active voice. "We will use X."

Why this one over the runner-up. Name the factor that broke the tie.

## Consequences

**What gets easier.**

**What gets harder.** Every decision costs something — name it.

**What we are locked into,** and how expensive it is to reverse.

## Revisit if

The concrete signal that would reopen this: a number, a date, or an event —
not "if it stops working well."
