# ADR-NNNN: <short title, a noun phrase — the decision, not the question>

- **Status:** Proposed | Accepted | Superseded by ADR-NNNN
- **Date:** YYYY-MM-DD
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

## Context

What is true right now that forces a decision? Constraints, not preferences: budget,
timeline, what you already know, what the grader/interviewer needs to see. Someone who
has never seen this repo should be able to read this section and understand why a
decision is required at all.

State the constraints as numbers where you can. "Cheap" is not a constraint. "Under
$15/month with no idle cost" is.

## Options considered

At least three. For each:

### Option A: <name>

- **How it works:** two sentences.
- **Cost:** idle cost and per-query cost, with a source for each figure.
- **Operational burden:** what breaks, who fixes it, how long to stand up.
- **What it teaches:** does building this make you better at explaining something in an
  interview, or is it a black box you'd be bluffing about?
- **Why it might be wrong:** the strongest argument against, written by you, in good faith.

### Option B: <name>

### Option C: <name>

## Decision

The option chosen, in one sentence, in the active voice. "We will use X."

Then: why this one and not the runner-up specifically. Not "it's the best" — name the
one factor that broke the tie.

## Consequences

**What gets easier.**

**What gets harder.** This section is the one that shows seniority. Every decision costs
something. If you cannot name what this makes worse, you have not finished thinking.

**What we are now locked into,** and how expensive the escape hatch is.

## Revisit if

The concrete signal that would make us reopen this. A number, a date, or an event —
not "if it stops working well."
