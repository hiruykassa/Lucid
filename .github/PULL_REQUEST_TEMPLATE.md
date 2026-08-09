# <what this change does, in one line, imperative>

## Why

The problem this solves. Link the ADR or LLD that authorized it. If there isn't one and
this is a new component, stop — the doc comes first.

## What changed

Bullets, at the level of "a reviewer deciding where to look," not a file listing. Git
already knows which files changed.

## How I tested it

The actual commands and their output. "Tested locally" is not testing.

## Numbers

If this touches retrieval, generation, or the eval harness, the before/after goes here
with the command and the git SHA that produced each. A change to the answer path with no
numbers attached is not reviewable.

| Metric | Before | After |
|---|---|---|
| | | |

## Risk

What could this break, and how would you know? What's the rollback?

---

## Self-review checklist

**Do this the morning after you open the PR, not the same night.** Read the diff cold,
as if someone else wrote it. The delay is the mechanism — you cannot review code you
wrote twenty minutes ago, you can only re-read it.

- [ ] I slept on it, then read the full diff top to bottom before requesting review
- [ ] There is a design doc or ADR behind this, and this change matches it
- [ ] Every magic number is either named or explained in a comment
- [ ] Failure paths are handled — not just the happy path
- [ ] No secrets, keys, or account IDs in the diff
- [ ] Tests cover the case I would have gotten wrong
- [ ] No number in the docs or README that I did not actually measure
- [ ] I left at least one comment on my own diff explaining a decision a reviewer
      would reasonably question

That last box is the one that does the work. If you can't find anything on your own diff
worth explaining, you probably haven't read it carefully enough yet.
