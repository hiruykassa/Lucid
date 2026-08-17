# LLD: Query skeleton (S2)

- **Status:** Draft
- **Date:** 2026-08-17
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)
- **Related:** ADR-0001, ADR-0002

> A low-level design doc describes *how one component works* before it exists. An ADR
> chooses between technologies; an LLD designs the thing you chose. If you're about to
> write a component and you can't fill this in, you don't understand it well enough to
> write it yet — and that's the point of catching it here rather than at line 200.

## Problem

What this component is for, in the reader's terms, not yours. Two paragraphs maximum.

## Requirements

**Functional.** What it must do. Numbered, testable, each one something you could write
a failing test for today.

**Non-functional.** Latency budget, cost ceiling, failure tolerance. Numbers.

**Explicit non-requirements.** What this component deliberately does not handle, so a
reviewer doesn't waste time asking about it.

## Interface

The contract, before the implementation. Function signatures or the API shape: inputs,
outputs, error cases. Someone should be able to write a caller against this section
alone.

```
# signature / request / response shape
```

## Design

How it works. A diagram if the data flow is non-obvious.

Then the part that matters: **the decisions inside the component.** Chunk size. Overlap.
Top-k. Timeout values. Retry policy. Each one gets a sentence on why that value and not
the neighbouring one. "512 tokens" is a magic number; "512 tokens, because the abstracts
in this corpus run 200–400 and I want one whole abstract per chunk" is a design.

## Failure modes

| What breaks | How you find out | What you do about it |
|---|---|---|
| | | |

Every row here should end up in a runbook entry and, where it matters, an alarm. If the
"how you find out" column says "a user tells me," that's a gap, not an answer.

## Testing

What gets a unit test, what needs an integration test, and what you're choosing not to
test and why. Name the one test that would actually catch a regression here.

## What I considered and rejected

Short. Two or three alternatives inside the component, and why not.

## Open questions

Things you want the reviewer to weigh in on. Bring these to review explicitly rather
than guessing and hoping nobody notices.

- What lives in `samconfig.toml` vs. what CI passes as parameter overrides, and where
  the deployment role ARN comes from. Raised 2026-08-17 after a gitignore near-miss.
