# Plan — Aug 10 to Dec 20, 2026

Read `../CLAUDE.md` for how we work and `ONBOARDING.md` for what the phases are. This
file is the calendar.

- **Start:** Mon Aug 10, 2026
- **Ship by:** Sun Dec 13, 2026
- **Hard stop:** Sun Dec 20, 2026
- **Commitment:** **9 h/week** in fixed calendar blocks — 7.5 h building, 1.5 h Friday
  journal and close-out (see *Capacity*, below)
- **Budget:** **105.5 h of build time** from Aug 31 to Dec 13 (126.5 h including the
  Friday ritual). Measured 2026-08-31, not estimated.

> **Replanned 2026-08-27.** The original figures here — "~20 h/week", "~360 h nominal,
> plan against ~300 h" — were guesses written before the semester schedule existed. They
> were wrong by roughly 2×. The numbers above come from counting actual calendar blocks.
> See *Capacity* for the method and *Scope changes* for what got cut as a result.

**Dec 13 is the deadline, not Dec 20.** Finals week is Dec 14–20. Any work still open on
Dec 14 competes with exams and loses. The last week is buffer and write-up — treat every
date below as if Dec 20 doesn't exist.

---



## Capacity — recounted 2026-08-31

Counted from Google Calendar on **2026-08-31**, covering Aug 31 – Dec 13. Every figure
below is an event that exists on the calendar, not an intention.

| Block | Duration | Occurrences | Hours |
| --- | --- | --- | --- |
| Mon 6:00–7:30pm — build | 1.5 h | 13 | 19.5 |
| Tue 5:00–6:00pm — small tasks | 1.0 h | 13 | 13.0 |
| Wed 6:00–8:00pm — build | 2.0 h | 13 | 26.0 |
| Thu 5:00–6:00pm — small tasks | 1.0 h | 13 | 13.0 |
| Sat 1:00–3:00pm — deep work | 2.0 h | 13 | 26.0 |
| S2 catch-up remaining (Sep 1, 3, 5) | — | 3 | 8.0 |
| | | **Build subtotal** | **105.5** |
| Fri 3:00–4:30pm — journal + week close-out | 1.5 h | 14 | 21.0 |
| | | **Total** | **126.5** |

**Build hours and ritual hours are counted separately on purpose.** The 105.5 h figure
is what's available to actually build the thing; scope estimates are sized against that
number, not against 126.5. The Friday block is overhead, and overhead that gets quietly
counted as capacity is how a plan overruns without anyone noticing.

Thanksgiving week drops the Wed, Thu, and Sat blocks. Finals week (Dec 14–20) has none.

**How this has moved.** Three counts in five days, which is itself the point — capacity
is now something we measure instead of assume:

| Date | Build hours to Dec 13 | Weekly rate | What changed |
| --- | --- | --- | --- |
| 2026-08-27 (first count) | 71.5 | 5.5 h | The original "~20 h/week, ~300 h" was never measured. First real count came to 24% of it. |
| 2026-08-27 (after replan) | 135.5 | 9.5 h | BIOL 105 dropped, freeing 44 h; consolidated into a 4 h Saturday block rather than scattered fragments. |
| **2026-08-31 (current)** | **105.5** | **7.5 h** | Saturday cut 11am–3pm → **1–3pm** (4 h → 2 h) after the real Saturday free windows turned out to be 10–11am and 1–3pm. ~4 h of the drop is the Aug 29 catch-up block simply having passed. |

**Consequence — the buffer is gone.** Trimmed scope was estimated at 105–115 h
(ADR-0004). Available build time is now **105.5 h**. That is the bottom of the range
with nothing spare, and it assumes no further lost weeks.

**Consequence — there is no long block any more.** Saturday 1–3pm and Wednesday 6–8pm
are both 2 h, and nothing is longer. The Saturday block was sized at 4 h specifically to
survive a first deploy or an IAM failure without the session going to context reload.
That property no longer exists, and S2's deploy and S4's Lambda packaging are exactly
the work that needed it. Two hours is workable; it is not comfortable.

**Known conflict:** the daily `Lunch` block (1:00–1:30pm, added 2026-08-31) overlaps the
first 30 minutes of Saturday deep work, making the real figure 1.5 h. Either move lunch
on Saturdays or start the block at 1:30 — but do not leave the calendar claiming 2 h it
does not have.

**The Saturday block is the one that matters.** It is the only session long enough to
absorb a first deploy, an IAM failure, or a Lambda packaging problem without the whole
block going to context reload. Treat 1-hour slots as docs, review, and journal time —
not as places to start something hard.

---

## Sprints

Two weeks each, Monday to Sunday. Nine of them.


| #      | Dates           | Goal                     | Gate — the thing that either exists or doesn't                                                                                                                         |
| ------ | --------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **S1** | Aug 10 – Aug 23 | Decide                   | ADRs 0001, 0002, 0003 all **Accepted**. AWS account has a billing alarm that has actually fired a test notification.                                                   |
| **S2** | Aug 24 – Sep 6  | Deploy an empty skeleton | A public URL returns hardcoded cited-answer JSON. Shipped by SAM, through GitHub Actions, logging to CloudWatch. One alarm, one runbook entry. LLD-0001 approved 2026-08-21. |
| **S3** | Sep 7 – Sep 20  | Corpus + chunking        | **25–30** papers in S3 per ADR-0004, inclusion rule per ADR-0003. Chunker written by you, LLD approved first — must preserve **page numbers** (LLD-0001 citation shape). You can explain the chunk size out loud without notes. |
| **S4** | Sep 21 – Oct 4  | Embeddings + index       | Every chunk embedded via Bedrock and indexed. You can run a query by hand and eyeball that the top-5 are relevant.                                                     |
| **S5** | Oct 5 – Oct 18  | Answer path + eval v0    | Endpoint returns a cited answer or refuses. **Plus a 5-question smoke eval that prints a recall number.** See the risk section.                                        |
| **S6** | Oct 19 – Nov 1  | Real eval set            | **~35** labeled questions (~26 answerable, ~9 unanswerable) per ADR-0004, built under ADR-0003's independence protocol. recall@k implemented properly. Report n alongside every metric. |
| **S7** | Nov 2 – Nov 15  | **Baseline measured**    | Faithfulness, hallucination rate, p50/p95, cost per query — all real, all in `docs/journal/` with date, command, and SHA.                                              |
| **S8** | Nov 16 – Nov 29 | Improve, re-measure      | One change (reranking *or* a stricter grounding prompt, not both). Re-run. Before/after delta recorded. Thanksgiving is Nov 26 — this sprint is effectively 1.5 weeks. |
| **S9** | Nov 30 – Dec 13 | Operate + write up       | Alarms and runbooks complete. At least one real COE. README results table with measured numbers. Done.                                                                 |
| —      | Dec 14 – Dec 20 | Finals                   | Buffer. Nothing scheduled.                                                                                                                                             |


**S7 is the sprint that matters.** Everything before it is setup and everything after it
is improvement. If the project produces exactly one thing, it should be a measured
baseline with an honest number attached.

---

## Scope changes — 2026-08-27

Cut so the plan fits 135.5 measured hours with real slack, rather than betting on the
optimistic end of an estimate. Estimated cost of the current scope is **110–145 h**
(estimate, unmeasured). Trimmed scope is roughly **105–115 h**, leaving ~20 h of buffer.

| What | Was | Now | Why |
| --- | --- | --- | --- |
| Corpus size | 40–50 papers | **25–30** | Collection and license-checking is the slowest non-code work in the project and buys the least. Retrieval over 25 papers is still non-trivial. |
| Eval set | ~50 questions | **~35** | Hand-labeling ground truth is slower than writing the harness that consumes it. Wider error bars, stated honestly, not hidden. |
| Unanswerable slice | ~15–20% (~8–10 Q) | **~25% (~9 Q)** | Refusal is the differentiator and already had the smallest denominator. A proportional cut would put it at 5–7 Q, where one misclassification moves the number 16.7 pp. Take the loss on the answerable slice instead. |

Recorded in **[ADR-0004](adr/0004-corpus-eval-resizing.md)**, which supersedes
ADR-0003's sizing only. Error-bar arithmetic is in that ADR.
| S8 improve + re-measure | at risk | **kept** | The before/after delta is worth more than a larger corpus. Affordable at 135.5 h. |

**What did not get cut:** the deployed endpoint, the alarm, the runbook, the COE, the
Friday journal, and the measured baseline. Those are the project.

**Smaller n is a result, not an embarrassment.** Every metric in the README gets its
sample size printed next to it. "Faithfulness 0.82 (n=35)" is honest; "faithfulness
0.82" is not.

---



## Detail level, and why S3 onward is thin

S1 and S2 are specified because they're technology-independent — writing decisions and
deploying an empty endpoint don't depend on which vector store you pick.

S3 onward is deliberately milestones and gates, not task lists. Per `ONBOARDING.md`, a
week-by-week task breakdown built on three undecided technologies is fiction, and the
previous version of this project had exactly that. Each sprint gets broken into tickets
at its kickoff, once the preceding sprint has told us what's actually true.

---



## Risks, named

**1. The first real number lands in week 14.**
Highest risk in the plan. If S6 or S7 slips even one sprint, the eval harness — the
entire differentiator — arrives with no time left to act on what it says, and you finish
with a RAG demo instead of a measured system.

*Mitigation, already folded into S5:* build a deliberately terrible 5-question eval the
same sprint the answer path lands. Hardcode the questions, compute recall only, print it
to stdout. It will produce an embarrassing number. That's fine — the point is that the
plumbing exists by mid-October, so S6 and S7 are filling in a harness rather than
building one under deadline.

**2. October–November is a collision.**
CISC 369 survey analysis starts around Oct 7 and paper drafting runs through November.
That lands squarely on S5–S8, the most technically demanding stretch. This is the reason
to spend August hard: every hour banked before Sep 9 is an hour that isn't competing
with a research deadline.

*Concretely:* the semester schedule does not begin until Sep 9. Aug 27 – Sep 6 is
otherwise empty, which is why the 12 h of S2 catch-up blocks sit there. That window is
the cheapest time in the whole plan — nothing competes with it.

**3. ~~"As much as I can squeeze in" has no floor.~~ Fixed 2026-08-27 — capacity is now
measured and blocked.**
This risk fired before the project was three weeks old, exactly as described: effort was
never measured, so a 5.5 h/week schedule looked identical to a 20 h/week one until
someone counted. It is now counted, in fixed blocks, in *Capacity* above. The remaining
version of the risk is **blocks getting skipped**, not blocks not existing:

- Log actual hours in the Friday journal entry. One line. If a sprint comes in under
**~15 h** against the ~19 h now scheduled, that's data, not a failure, and we re-plan
around it rather than pretending.
- **Recorded:** week of Aug 17–23 came in at ~0 h (illness). Absorbed by the nine days
of slack banked when S1 closed early on Aug 14. No downstream date moved.
- **Every session ends with the next step written down.** Irregular sessions pay a
context-reload tax on every restart, and the only cheap fix is leaving yourself a note
that says exactly where to pick up. Last commit message or a scratch line at the top of
the journal entry, doesn't matter which.

**4. AWS spend.**
S1's gate includes a billing alarm on purpose. It goes in before the first dollar is
spent, not after a surprise. Budget alarms are the cheapest insurance in this project.

**5. Scope creep.**
The React UI, the second corpus, the hybrid search, the agent loop. Not this semester.
Flagging this in advance so that when I say it in October you've already agreed to it.

---



## Standing rituals


| When                               | What                                                    |
| ---------------------------------- | ------------------------------------------------------- |
| Every work session, first 2 min    | Standup — done / next / blocked (`engineering:standup`) |
| Sprint kickoff (alternate Mondays) | Break the sprint into tickets, agree the gate           |
| Before any new component           | LLD or ADR, reviewed, before code                       |
| Before any merge                   | PR + sleep on it + cold self-review + my review         |
| **Every Friday, 3:00–4:30pm**      | STAR journal entry + week close-out, with hours logged  |
| Sprint close (alternate Sundays)   | Gate met or not — binary. Retro if not.                 |


Sprint gates are binary on purpose. "80% done" is the most expensive sentence in
software estimation.

---



## Milestone reviews

Real internships have a midpoint check-in and a final presentation. Both go on the
calendar:

- **Midpoint — Sun Oct 18 (end of S5).** Am I on track to have a measured baseline?
If the answer is no, S6–S9 get re-scoped that week, not in December.
- **Final — Sun Dec 13 (end of S9).** A 15-minute talk you could actually deliver:
what it does, what you measured, what you'd do next, what you got wrong. Written up
in `docs/journal/`. This is the artifact you'll mine for interviews in February.

