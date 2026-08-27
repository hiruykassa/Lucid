# ADR-0004: Resize corpus and eval set to measured capacity

- **Status:** Approved
- **Date:** 2026-08-27
- **Author:** Claude (Senior SDE) — drafted at Hiruy's request
- **Reviewer:** Hiruy Kassa
- **Supersedes:** [ADR-0003](0003-corpus-selection.md), **sizing only.** Inclusion
rule, licensing, S3 layout, manifest discipline, corpus versioning, the
independence protocol, and the refusal labels all stand unchanged.
- **Related:** [ADR-0001](0001-vector-store.md), `[docs/PLAN.md](../PLAN.md)`

## Process note — read this first

The operating contract says Hiruy drafts ADRs and Claude reviews them. This one is
inverted, at his request, so the repo isn't left self-contradicting between sessions.
Two consequences:

1. **Reviewed and Approved by Hiruy on 2026-08-27.** He was the reviewer on this one,
   not Claude — an author cannot accept their own ADR.
2. He must be able to defend these numbers in an interview without notes. If he can't
   explain why 25–30 and not 45, this ADR has failed regardless of whether the
   reasoning is sound. **Approving it is the claim that he can.**

---



## Context

ADR-0003 set a target of **40–50 papers** and a **~50-question** eval set. Both were
chosen on 2026-08-10 against `docs/PLAN.md`'s stated budget of "~20 h/week, ~300 h"
for the semester.

**That budget was never measured.** It was written before the fall schedule existed.
On 2026-08-27 the actual calendar was counted: **135.5 hours** between Aug 27 and
Dec 13, in fixed weekly blocks. The first count, before BIOL 105 was dropped, was
71.5 h — 24% of the planning assumption. See `[docs/PLAN.md](../PLAN.md)` §Capacity
for the method.

So the sizing in ADR-0003 rests on a number that turned out to be wrong by roughly 2×.
The decision itself was sound given what was known; the input was not.

ADR-0003 already contains an escape hatch: *"shrink to ~25 only if collection blocks
S3."* **That trigger does not apply here.** Collection has not started and is not
blocked. The trigger being invoked is different — capacity was measured short *before*
S3 began. Changing the trigger is a decision, not a footnote, which is why this is a
superseding ADR rather than an edit to ADR-0003.

Estimated cost of the ADR-0003 scope is **110–145 h** (estimate, unmeasured — Claude's
judgement, not a measurement). Against 135.5 h available, that fits only at the
optimistic end, with no slack. One lost week consumes the margin; the week of
Aug 17–23 already came in at ~0 h.

---



## Options considered



### Option A: Keep 40–50 papers and ~50 questions, cut S8 instead

- **How it works:** Preserve the corpus and eval set exactly as ADR-0003 specifies.
Drop S8 (improve + re-measure) to pay for it.
- **For:** No ADR churn. Eval numbers keep the wider denominator, so error bars stay
tighter. Nothing to re-defend in interviews.
- **Against:** S8 is the sprint that produces a *before/after delta* — "hallucination
rate went X → Y after I changed Z, here's the command and the SHA." That delta is
the most interview-legible artifact the project can produce, and it demonstrates the
measure-change-remeasure loop that the whole project exists to practise. Trading it
for 15 extra papers trades the strongest story for a weaker denominator.
- **Also against:** it does not actually solve the problem. Corpus collection and
question labeling are front-loaded into S3 and S6. Cutting S8 frees hours in
*November*, after the work that overruns has already overrun.



### Option B (chosen): 25–30 papers, ~35 questions, keep S8

- **How it works:** Shrink both ground-truth sets. Keep every sprint gate.
- **For:** Cuts the two slowest non-code activities in the project. Preserves the
measure-improve-remeasure loop. Fits 135.5 h with ~20 h of real buffer.
- **Against:** Wider error bars on every published metric (quantified below). Weaker
claims about corpus coverage. If retrieval scores well, it is harder to rule out
"because the corpus is small."



### Option C: Shrink hard — ~15 papers, keep ~50 questions

- **How it works:** Minimal corpus, full-size eval set.
- **For:** Maximum hours freed. Best statistical power per hour spent.
- **Against, and this is the disqualifier:** at ~15 papers the corpus produces roughly
400–500 chunks, and top-5 retrieval over that is close to trivial. recall@5 would
measure the corpus's smallness, not the retriever's quality. ADR-0003's reasoning
for 40–50 was "smallest band that still forces retrieval to discriminate" — 15 is
clearly below it. A metric that cannot fail is not a measurement.



### Option D: Keep ADR-0003 sizing, extend the deadline into January

- **How it works:** Full scope, ship mid-January using winter break.
- **For:** No scope loss at all. Winter break genuinely has more free hours.
- **Against:** Fall applications go out before January, so there is no finished result
to point at when it matters most. February interview prep would collide with
finishing the build. And an unmeasured January estimate is the same mistake that
produced this ADR — winter-break capacity has not been counted either.

---



## Decision

**Option B.**


| Parameter               | ADR-0003           | ADR-0004          |
| ----------------------- | ------------------ | ----------------- |
| Corpus target           | 40–50 papers       | **25–30 papers**  |
| Full eval set           | ~50 questions      | **~35 questions** |
| Unanswerable slice      | ~15–20% (~8–10 Q)  | **~25% (~9 Q)**   |
| Answerable slice        | ~80–85% (~40–42 Q) | **~75% (~26 Q)**  |
| S8 improve + re-measure | in plan            | **kept**          |


**The unanswerable slice gets a larger share, not a smaller one.** This is the one
place where the naive proportional cut is wrong. Refusal behaviour is the product's
differentiator and already had the smallest denominator in the design. Holding the
ADR-0003 percentage would put it at 5–7 questions; at n=6 a single misclassification
moves refusal precision by **16.7 percentage points**. Weighting it to ~25% keeps the
count at ~9, close to ADR-0003's original ~8–10, and takes the loss on the answerable
slice where 26 questions still support a usable estimate.

### What the smaller n actually costs

Computed, not measured — normal approximation, 95% interval, assuming p = 0.80.
Reproduce with `1.96 * sqrt(p*(1-p)/n)`.


| Slice                       | n      | 95% half-width | One misclassification moves it |
| --------------------------- | ------ | -------------- | ------------------------------ |
| Answerable (ADR-0003)       | 42     | ±12.1 pp       | 2.4 pp                         |
| **Answerable (this ADR)**   | **26** | **±15.4 pp**   | **3.8 pp**                     |
| Unanswerable (ADR-0003)     | 8      | ±27.7 pp       | 12.5 pp                        |
| **Unanswerable (this ADR)** | **9**  | **±26.1 pp**   | **11.1 pp**                    |


The honest reading: **at either size, the unanswerable slice is directional, not
precise.** ADR-0003 did not make refusal precision statistically strong either — it
was always going to be ~8 questions. This ADR does not meaningfully worsen it and
slightly improves it. The real cost lands on the answerable slice, ±12 pp → ±15 pp.

**Every metric in the README and the journal carries its** `n`**.** "Faithfulness 0.82
(n=26)" is a result. "Faithfulness 0.82" is a claim this project cannot support at
this sample size, and per rule 3 it does not get written.

---



## Consequences

**What gets easier.**

- Corpus collection and license-checking — the slowest non-code work in the project —
drops by roughly 40%, in S3, which is the sprint most at risk of overrunning into
the CISC 369 collision.
- Question labeling in S6 drops from ~50 to ~35 hand-labeled items.
- S8 survives, so the project can still produce a before/after delta.
- Smaller FAISS index, comfortably inside ADR-0001's measured 116 MB margin. The
cold-start risk flagged in ADR-0001 gets slightly smaller too.
- Fewer Bedrock embedding calls at ingest, so more headroom under the $20/mo budget.

**What gets harder.**

- **Every published number gets wider error bars, and they must be stated.** This is
now a permanent obligation on the README, the journal, and any resume bullet.
- Harder to attribute good retrieval scores to the retriever rather than to a small
corpus. Mitigation: report corpus size and chunk count next to recall@k, always.
- Less margin in the inclusion rule — with a 25–30 band there is little room to reject
borderline papers and still hit target. Expect the "is this persuasive-design paper
in?" disputes from ADR-0003 to bite sooner.
- The unanswerable-slice sourcing trap from ADR-0003 gets *more* dangerous, not less:
a smaller corpus means more of the topic space is genuinely out-of-corpus, which
makes it easier to write unanswerable questions that are trivially unanswerable.
Keep them plausibly in-topic.

**What we are locked into.**

- Corpus version and eval set stay paired, exactly as ADR-0003 requires. Resizing
after the eval set is labeled means a new corpus version and a re-label.
- This ADR does **not** relax any ADR-0003 discipline. Manifest, hashes, license class,
private S3, freeze-before-questions, and the refusal labels all still apply.

---



## What would make us revisit this

- **recall@5 exceeds ~0.95 on the first real S6 run.** That is the signature of a
corpus too small to discriminate — the metric has stopped being able to fail.
Response: add papers toward 40 and re-label, or report recall@1 instead.
- **Collection comes in well under estimate.** If 25–30 papers are manifested with
meaningful S3 time left, spend it on more papers before spending it anywhere else.
Ceiling stays 50 (ADR-0001 index math).
- **Measured capacity changes again by more than ~20 h in either direction.** Recount
the calendar and re-run this decision; do not eyeball it. The failure that produced
this ADR was trusting an uncounted number.
- **Any sprint gate slips a full sprint.** Then the question stops being corpus size
and becomes which sprint to cut, and S8 goes first after all.

