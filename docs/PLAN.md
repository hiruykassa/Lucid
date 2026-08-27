# Plan — Aug 10 to Dec 20, 2026

Read `../CLAUDE.md` for how we work and `ONBOARDING.md` for what the phases are. This
file is the calendar.

- **Start:** Mon Aug 10, 2026
- **Ship by:** Sun Dec 13, 2026
- **Hard stop:** Sun Dec 20, 2026
- **Commitment:** ~20 h/week, taken opportunistically rather than in fixed blocks
- **Nominal budget:** 18 weeks × 20 h ≈ **360 h**. Plan against **~300 h.** School,
CISC 369 deadlines, and two holiday weeks will take the rest, and pretending otherwise
is how a December project becomes a February project.

**Dec 13 is the deadline, not Dec 20.** Finals week is Dec 14–20. Any work still open on
Dec 14 competes with exams and loses. The last week is buffer and write-up — treat every
date below as if Dec 20 doesn't exist.

---



## Sprints

Two weeks each, Monday to Sunday. Nine of them.


| #      | Dates           | Goal                     | Gate — the thing that either exists or doesn't                                                                                                                         |
| ------ | --------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **S1** | Aug 10 – Aug 23 | Decide                   | ADRs 0001, 0002, 0003 all **Accepted**. AWS account has a billing alarm that has actually fired a test notification.                                                   |
| **S2** | Aug 24 – Sep 6  | Deploy an empty skeleton | A public URL returns hard coded cited-answer JSON. Shipped by SAM, through GitHub Actions, logging to CloudWatch. One alarm, one runbook entry.                        |
| **S3** | Sep 7 – Sep 20  | Corpus + chunking        | Papers in S3 per ADR-0003. Chunker written by you, LLD approved first. You can explain the chunk size out loud without notes.                                          |
| **S4** | Sep 21 – Oct 4  | Embeddings + index       | Every chunk embedded via Bedrock and indexed. You can run a query by hand and eyeball that the top-5 are relevant.                                                     |
| **S5** | Oct 5 – Oct 18  | Answer path + eval v0    | Endpoint returns a cited answer or refuses. **Plus a 5-question smoke eval that prints a recall number.** See the risk section.                                        |
| **S6** | Oct 19 – Nov 1  | Real eval set            | ~50 labeled questions built under the independence protocol from ADR-0003. recall@k implemented properly.                                                              |
| **S7** | Nov 2 – Nov 15  | **Baseline measured**    | Faithfulness, hallucination rate, p50/p95, cost per query — all real, all in `docs/journal/` with date, command, and SHA.                                              |
| **S8** | Nov 16 – Nov 29 | Improve, re-measure      | One change (reranking *or* a stricter grounding prompt, not both). Re-run. Before/after delta recorded. Thanksgiving is Nov 26 — this sprint is effectively 1.5 weeks. |
| **S9** | Nov 30 – Dec 13 | Operate + write up       | Alarms and runbooks complete. At least one real COE. README results table with measured numbers. Done.                                                                 |
| —      | Dec 14 – Dec 20 | Finals                   | Buffer. Nothing scheduled.                                                                                                                                             |


**S7 is the sprint that matters.** Everything before it is setup and everything after it
is improvement. If the project produces exactly one thing, it should be a measured
baseline with an honest number attached.

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

**3. "As much as I can squeeze in" has no floor.**
Variable effort is fine — irregular effort with no measurement isn't, because a slipping
week looks identical to a busy one until three have gone by. Two mitigations:

- Log actual hours in the Friday journal entry. One line. If a sprint comes in under
~25 h, that's data, not a failure, and we re-plan around it rather than pretending.
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
| Every Friday, 10 min               | STAR journal entry, with hours logged                   |
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

