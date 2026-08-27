# ADR-0003: Corpus selection and licensing

- **Status:** Accepted
- **Date:** 2026-08-10 (accepted 2026-08-13)
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

## Context

Every eval number Lucid publishes is a claim about *this* corpus. If the paper
list is unexplained, “recall@5 = …” means nothing. Phase 0 needs a written rule
for what gets in, where PDFs live, how this overlaps CISC 369, how eval questions
stay independent of cherry-picking, and how large the set is.

Constraints:

- Topic: AI dark patterns and digital well-being (product scope in `CLAUDE.md`).
- Public GitHub repo — redistributing publisher PDFs is not acceptable.
- Ingest path is S3 → chunk → embed → FAISS (ADR-0001), so PDFs must be readable
from a **private** bucket at ingest time. **Bucket region:** `us-east-2` (same
as ADR-0001 Lambda packaging and ADR-0002 Bedrock — do not split regions).
- Embedding model is English-oriented Titan V2 (ADR-0002) → English papers only.
- Semester budget: collecting and licensing 80+ papers crowds out building.
- CISC 369 lit-review papers may seed the corpus (operating contract); Claude
never touches 369 graded work.
- Corpus changes force **FAISS rebuild + Lambda redeploy** (ADR-0001: index in
package) — the inclusion rule must keep churn low.

---



## Options considered



### Option A: Strict “dark patterns” only, ~25 papers, PDFs in git

- **How it works:** Include only papers that use the phrase “dark pattern.” Commit
PDFs to the repo for easy clone-and-run.
- **Cost:** Cheap to collect; zero S3 until later. Legal risk is the real cost
(publisher ToS / copyright if PDFs land in a public repo).
- **Operational burden:** Tiny corpus; trivial ingest.
- **Risks / downsides:** Misses well-being / attention / recommender-harm work that
Lucid must answer. PDFs in a public repo is the embarrassment case. ~25 papers
makes retrieval too easy — eval flatters the system.
- **What it teaches:** Almost nothing about corpus hygiene or licensing; optimizes
for convenience over honesty.



### Option B: Inclusion rule below, target 40–50, manifest in git / PDFs in private S3

- **How it works:** Written inclusion criteria; 369 papers as the seed; add until
40–50. Git holds metadata only; private S3 (`us-east-2`) holds PDFs allowed for
research use.
- **Cost:** S3 storage for tens of MB is pennies (same ≤$5 storage posture as
ADR-0001). Time cost is selection + license tagging, not dollars.
- **Operational burden:** Maintain `corpus/manifest.json`; upload PDFs privately;
record license per item; rebuild FAISS + redeploy on corpus change (ADR-0001).
- **Risks / downsides:** Must actually apply the rule and not pad with weak papers
to hit 50. Paywalled PDFs require care (personal/research copies only, never public).
- **What it teaches:** How to define a measurable population and keep eval honest —
the internship skill, not just “get papers.”



### Option C: Broad “anything about screens and habits,” 80+ papers, mix of sources

- **How it works:** Wide net across HCI, industry blogs, and unpaid PDFs until the
bucket feels large.
- **Cost:** Time — collection and cleaning dominate S3 of the plan.
- **Operational burden:** Licensing review per item gets skipped under schedule pressure;
more redeploys as the set churns.
- **Risks / downsides:** Scope creep; noisy retrieval; eval set becomes unmaintainable;
higher chance of a ToS mistake; fights ADR-0001’s small-index assumption.
- **What it teaches:** Collection stamina more than evaluation discipline.

---



## Decision

We will use **Option B**: written inclusion criteria, **target 40–50 papers**,
**manifest in git / PDFs in private S3 (**`us-east-2`**)**, with the eval protocol
below — including a required **~15–20% unanswerable slice** so refusal is measured,
not assumed.

**Tie-breaker vs A:** topic coverage + eval discrimination. **vs C:** calendar and
licensing risk. Runner-up is A only if collection blocks the S3 sprint gate.

### Inclusion criteria (a stranger should get nearly the same list)

A paper is in if **all** of the following hold:

1. **Topic core:** AI/ML UX dark patterns, digital well-being (attention, compulsion,
  manipulative recommendations), or closely related persuasive / attention-economy
   research that **studies harm or manipulation**.
2. **Boundary:** Exclude pure marketing persuasion with no well-being / harm angle.
  Exclude generic “AI ethics” with no design/UX pattern content.
3. **Method:** Empirical studies **or** framework/taxonomy papers (definition papers
  count — they ground answers).
4. **Venue:** Prefer peer-reviewed HCI / adjacent venues (e.g. CHI, CSCW, FAccT,
  TOCHI). arXiv (or author preprint) allowed when that is the citable version and
   the license is explicit.
5. **Date:** Published (or dated preprint) **2015–2026**.
6. **Language:** English.



### Size

**Target 40–50 papers.** Smallest band that still forces retrieval to discriminate;
fits FAISS-in-Lambda and one semester. Do not pad to 50 with off-topic fillers.
If the good set tops out at ~40, stop. Label the frozen set with a **corpus version**
(e.g. `corpus-v0`) in the manifest so eval labels stay paired to a snapshot.

### CISC 369 overlap

**Prefer overlap.** Seed the corpus from papers read for the 369 lit review when
they pass the inclusion rule, then add more until the 40–50 band. Confirm with
Hoefer that this use is allowed **before uploading any 369-overlap PDF to S3**.
**Drop-dead for that confirm:** end of **S2 (Sun Sep 6, 2026)**. If disallowed or
unconfirmed by then, seed without 369 overlap and note it in the manifest README.
Claude still does not assist with 369 graded work.

### Licensing and storage


| Location                         | What lives there                                                                                                                                                                         |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **git**                          | `corpus/manifest.json` (and related docs): title, authors, year, venue, DOI/arXiv id, **license class**, `sha256` of the PDF, one-line inclusion rationale, corpus version. **No PDFs.** |
| **Private S3 (**`us-east-2`**)** | PDF bytes for ingest, only when keeping a copy is allowed under that paper’s license / publisher terms for personal or research use. Bucket name TBD in S3 sprint; region is not TBD.    |
| **Never**                        | ACM/IEEE (or other paywalled) PDFs in the public repo or any public bucket.                                                                                                              |


**License class** (required field on every manifest row) — one of:


| Class                        | Meaning                                                       | OK in private S3?                         |
| ---------------------------- | ------------------------------------------------------------- | ----------------------------------------- |
| `cc-by` / `cc-by-sa` / `cc0` | Explicit open license                                         | Yes                                       |
| `arxiv-nonexclusive`         | arXiv non-exclusive distribution (check per-paper)            | Yes if terms allow personal research copy |
| `publisher-personal`         | Paywalled; personal/research download via library access only | Yes private only; **never** git/public    |
| `unknown`                    | Not yet classified                                            | **Not** uploaded until classified         |


Rule of thumb: **metadata public, PDFs private, paywalled content never redistributed.**

### Corpus / eval independence protocol

Studying the topic first (including via 369) is expected. What we avoid is writing
the quiz while selecting papers or with those PDFs open.

1. Study the topic.
2. **Freeze** the corpus in `corpus/manifest.json` under a version id (`corpus-v0`).
3. **Later**, write eval questions from domain knowledge plus titles/abstracts —
  not with the full PDFs open in the same sitting.
4. **Separate pass:** label which paper (and later, which chunks) answer each question.
5. **Never** add a paper only because an eval question needs it.

**Problem the protocol alone does not solve:** questions written from manifest
titles/abstracts are **answerable by construction**. That measures retrieval on
easy questions only. It does **not** measure:

- **Refusal correctness** — a system hardwired to always answer scores the same.
- **Hallucination under pressure** — only on questions where an answer exists.
- **recall@5** inflated — ~1,000 chunks, questions derived from the same abstracts.



### Unanswerable eval slice (required)

Add **~15–20%** of the full eval set as **in-topic, out-of-corpus** questions:
plausibly about AI dark patterns / digital well-being, **genuinely not answerable**
from `corpus-v0`. Example shape: “What did [Company X]’s 2024 transparency report
say about recommender opt-out defaults?” when that report is not in the corpus.


| Slice                            | Share of ~50 Q set    | Purpose                                   |
| -------------------------------- | --------------------- | ----------------------------------------- |
| Answerable (corpus-supported)    | ~80–85% (~40–42 Q)    | recall@k, faithfulness when answer exists |
| **Unanswerable (out-of-corpus)** | **~15–20% (~8–10 Q)** | **refusal rate, false-answer rate**       |


**Sourcing trap:** do **not** derive unanswerable questions from **rejected** papers
under the inclusion rule — rejected papers are often topic-near-duplicates of
accepted ones, so “unanswerable” quietly becomes “answerable.” Source from domain
knowledge, news, or products **not represented** in the manifest. Same freeze
discipline: write this slice **after** corpus freeze, without corpus PDFs open.

### What a correct refusal looks like

“Refused” and “refused for the right reason” are different events. For the
unanswerable slice, label each question with:


| Label            | Meaning                                                                                                    |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| `refuse-correct` | Model declines to answer **and** cites missing/insufficient corpus support (not a generic “I can't help”). |
| `refuse-wrong`   | Model declines but for the wrong stated reason, or hedges without refusing.                                |
| `false-answer`   | Model answers anyway — **the failure mode we care about most**.                                            |


S6 eval harness reports **refusal precision** on the unanswerable slice separately
from recall@k on the answerable slice. Do not merge into one headline number.

S5 may use a tiny 5-question smoke set (mix 1–2 unanswerable); the full ~50-question
set (S6) must follow this protocol against the frozen manifest version.

---



## Consequences

**What gets easier.**

- Eval numbers have a defined population and version.
- Ingest has a clear S3 layout; git stays legally boring.
- 369 reading can double duty without violating the operating contract (if Hoefer okays).
- 40–50 keeps collection inside the calendar and matches ADR-0001’s small-index math.

**What gets harder.**

- Must maintain the manifest, hashes, and license class; “I’ll just drop PDFs in the
repo” is forbidden.
- Inclusion disputes (“is this persuasive-design paper in?”) need a one-line rationale
per item, not vibes.
- Waiting to write eval questions after freeze slows the urge to measure early —
smoke eval in S5 stays deliberately small.
- Must write and label the **unanswerable slice** with care — the rejected-paper
trap is real.
- Every accepted paper after freeze → new corpus version + FAISS rebuild + redeploy
(ADR-0001), so late adds are expensive on purpose.

**What we are locked into,** and how expensive it is to reverse.

- Locked into the inclusion rule and storage layout until a new ADR supersedes this.
- Adding papers after the eval set is labeled requires a new corpus **version** and
re-label (or keeping eval paired only to the old version).
- Escape hatch: shrink to ~25 only if collection blocks S3; expand past 50 only if
measured recall is saturated and FAISS size still fits Lambda (revisit ADR-0001).

---



## Revisit if

- Hoefer disallows using 369 readings in Lucid (drop overlap; rebuild seed list), **or**
- Hoefer confirmation is still missing at **Sep 6, 2026** (proceed without 369 seed),
**or**
- A licensing incident (PDF found in git or a public bucket) — stop ingest, scrub,
rewrite this rule tighter, **or**
- Frozen corpus < 30 after good-faith search (reconsider scope or date window), **or**
- FAISS index + Lambda memory pressure from a larger-than-planned set (ADR-0001), **or**
- Eval independence was violated in practice (questions written from open PDFs during
selection) — discard that question set and rebuild under the protocol, **or**
- Full eval set has **zero** unanswerable questions, or unanswerable questions were
sourced from rejected/near-duplicate papers — rebuild the slice, **or**
- Refusal rate on the unanswerable slice is never measured separately from recall@k
— fix the harness before S7 baseline.

