# Onboarding — Lucid

Read `../CLAUDE.md` first. That's how we work. This is what you work on.

---

## Day one

You've joined a team of one, on a service that doesn't exist yet, with three unmade
decisions blocking all implementation. That's roughly the real thing — interns usually
arrive to a project scoped by someone else with the hard parts still open.

Your first week is not code. Interns at Amazon typically spend the opening stretch of a
twelve-week project on design: read, prototype, write a low-level design doc, pitch it to
senior engineers, get approval, *then* implement. We're compressing that but not skipping
it.

**Your first assignment is [ADR-0001: vector store](adr/0001-vector-store.md).** Read the
brief. Write the ADR yourself. Badly is acceptable and expected — a bad draft that exists
is worth more than a good one you're still planning. Then say it's ready and I'll review
it the way a senior SDE would.

Expect the review to be uncomfortable. That's the product.

---

## Phases

| # | Phase | Gate to leave it |
|---|---|---|
| 0 | Decide + deploy an empty skeleton | ADRs 0001–0003 Accepted; hardcoded-JSON endpoint live via SAM + CI; CloudWatch logging |
| 1 | Ingest | Papers in S3, chunked, embedded, indexed; you can explain chunk size out loud |
| 2 | Answer | Query path returns a cited answer, or refuses; LLD written before the code |
| 3 | Eval baseline | ~50 labeled questions; recall@k, faithfulness, hallucination rate, p50/p95, cost — all real |
| 4 | Improve and re-measure | One change (reranking or grounding prompt), re-run, before/after delta in the README |
| 5 | Operate | Alarms, runbooks, and at least one real COE from something that actually broke |
| 6 | Polish | README you can defend line by line |

**Phase 0 ends with a deploy.** Not phase 5. A Lambda behind API Gateway returning
hardcoded JSON, shipped by SAM through GitHub Actions, with logs in CloudWatch — before
there is any real logic to deploy. Two reasons: every phase after that is a change to a
running system, which is what the job actually is, and it removes "deploy" from the
end of the calendar where it sits as an unbounded risk you can't estimate.

---

## Schedule

**Settled.** The internship starts Mon Aug 10, 2026 and ships by Sun Dec 13, with
Dec 14–20 held as finals buffer. Roughly 20 h/week, taken opportunistically — nine
two-week sprints, each with a single binary gate.

The calendar, the hour budget, and the named risks live in [PLAN.md](PLAN.md).

Sprints S1 and S2 are specified in detail because they're technology-independent.
S3 onward is milestones and gates only, and gets broken into tickets at each sprint
kickoff — a detailed task list built on three undecided technologies is fiction, and
the previous version of this file was exactly that.

---

## Definition of done for the whole project

- [ ] Corpus ingested and searchable
- [ ] Live endpoint returns cited answers and refuses unsupported ones
- [ ] Eval harness with real numbers and a results table in the README
- [ ] SAM deploy + GitHub Actions CI passing
- [ ] CloudWatch showing latency and cost
- [ ] At least one COE from a real failure
- [ ] ~14 STAR journal entries
- [ ] A README you can defend line by line

No target metrics are recorded in this repo. The previous version of this project
carried a table of aspirational numbers — faithfulness, recall@5, hallucination rate —
that had never been measured, and they leaked onto a resume. Numbers enter this repo
only after a run produces them, with the date, the command, and the SHA. See rule 3 in
the operating contract.

---

## The gap I can't close

Four things separate this from a real internship. Three we simulate (design review,
code review, on-call, ambiguous asks — see the table in `../CLAUDE.md`). The fourth is
reading a large codebase you didn't write, and no amount of solo project work produces
it.

The cheapest partial fix is landing one real pull request in an open-source repository
you've never seen, and letting a stranger review it. One is enough. Put it on the
calendar for a low-intensity week rather than "sometime" — it's the item most likely to
never happen, and it patches the largest gap.
