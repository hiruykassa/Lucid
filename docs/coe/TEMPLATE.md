# COE: <what broke, plainly>

**Correction of Errors.** Written after something breaks, no matter how small.
Blameless: the subject of every sentence is the system, not the person. You are the only
engineer here, so "blameless" means something specific — it means the finding cannot be
"I was careless." That's never a root cause. If your five whys bottom out at a character
flaw, you stopped one why too early.

- **Date of incident:**
- **Detected at:** and **by what** — an alarm, a test, or you noticing by accident?
- **Resolved at:**
- **Duration:**
- **Impact:** what didn't work, for how long, for whom. If the answer is "only me,
  nobody noticed," say that. Honest scope beats inflated scope.

## Timeline

Times, in order, plainly. Include the wrong turns — the thing you checked that wasn't
it is often the most useful line in the document, because it tells you what your
observability failed to rule out.

| Time | What happened |
|---|---|
| | |

## Five whys

1. **Why did <the impact> happen?**
2. **Why did <that> happen?**
3. **Why did <that> happen?**
4. **Why did <that> happen?**
5. **Why did <that> happen?**

Two independent chains are common: one for why it broke, one for why it took so long to
notice. Run both. The detection chain is usually the more valuable one.

## What went well

Real entries only. If an alarm fired correctly, say so — that's evidence the alarm was
worth building, which is otherwise invisible.

## Action items

Concrete, owned, dated. "Be more careful" is not an action item. "Add a schema check to
the ingest Lambda that fails loudly on an empty chunk list" is.

| # | Action | Prevents | Due |
|---|---|---|---|
| 1 | | | |

## Lessons

One paragraph, in plain language, that would be useful to someone who has never seen
this system. This paragraph is usually a STAR story — cross-link it in
`docs/journal/`.
