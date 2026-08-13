# ADR-0002: Embedding and generation models

- **Status:** Accepted (model decision) — invoke access blocked, tracked via Support case 178659049300631 + Sep 5 Plan B trigger
- **Date:** 2026-08-10 (accepted 2026-08-13)
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

## Context

Lucid’s query path embeds the question, retrieves chunks, then calls a generation
model for a cited answer or a refusal. Ingest embeds every chunk once. The eval
harness adds a third model call: an LLM-as-judge for faithfulness.

These choices are coupled:

- Embedding dimensionality locks the FAISS index shape (ADR-0001).
- Generation quality drives refusal behavior and hallucination rate.
- Judge choice decides whether faithfulness scores are trustworthy or just the
generator grading itself (**self-preference bias** — models systematically favor
their own outputs).

Constraints:

- Region: `us-east-2` (account / console region), on-demand Bedrock, no
Provisioned Throughput, no quota request that can block December.
- Corpus scale: ~50 papers → embed cost is noise; **eval re-runs** dominate spend.
- Budget posture matches ADR-0001: keep always-on near $0; pay per token only.
- Must support a grounded refuse path — cheapest model that ignores instructions
fails the product even if the eval bill looks great.

Prices below are on-demand figures cross-checked against
[Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) / Marketplace
listings on **2026-08-12**. Re-check that page before any cost claim in the
README. **A pricing-page listing is not proof this account can call the model** —
see verification below.

**Cross-doc region:** `us-east-2` is the project region for Bedrock, Lambda, and
S3 (ADR-0001 packaging target; ADR-0003 corpus bucket). Do not split regions or
ingest will pay cross-region transfer for no reason.

### Console catalog check (2026-08-12, `us-east-2`)

Checked in the Bedrock **Model catalog** for account `hiruykassa` (not the pricing
page alone):


| Role     | Console name             | Model / profile ID                                                                                                                          | Availability note                                                                                                                                                                                                            |
| -------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Embed    | Titan Text Embeddings V2 | `amazon.titan-embed-text-v2:0`                                                                                                              | Serverless; listed in catalog                                                                                                                                                                                                |
| Generate | Claude Haiku 4.5         | Invoke via `us.anthropic.claude-haiku-4-5-20251001-v1:0` (US geo cross-region profile). Base ID: `anthropic.claude-haiku-4-5-20251001-v1:0` | **Not available via in-region endpoints** in `us-east-2`; inference type = cross-region. Prefer `us.` over `global.` (US-only routing). Fallback: `global.anthropic.claude-haiku-4-5-20251001-v1:0` if `us.` is unavailable. |
| Judge    | Nova Lite                | `amazon.nova-lite-v1:0`                                                                                                                     | Serverless; listed in catalog                                                                                                                                                                                                |


**Catalog visibility ≠ invoke access.** S1 is not done until the invoke smokes below
succeed.

### S1 access gate (Waiting on response from AWS support)

1. Submit Anthropic **use case details** in the Bedrock console (one-time).
2. Smoke-invoke each ID from `us-east-2` (tiny prompt / one-token-class call):
  - `us.anthropic.claude-haiku-4-5-20251001-v1:0`
  - `amazon.titan-embed-text-v2:0`
  - `amazon.nova-lite-v1:0`
3. Log **date**, API exception, HTTP status, and `x-amzn-RequestId` per ID below.

**Billing alarm (S1 — independent of Bedrock):** test-fire the account billing
alarm **before** first Bedrock spend — set threshold at a value already crossed,
or publish directly to the SNS topic, and confirm notification lands in inbox.
An alarm nobody has seen fire is not an alarm.


| ID                                            | Date       | Exception             | HTTP    | RequestId                              | Note                                                                                                                                                                                                                                                                                  |
| --------------------------------------------- | ---------- | --------------------- | ------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `us.anthropic.claude-haiku-4-5-20251001-v1:0` | 2026-08-12 | `ValidationException` | **400** | `d7af2a9e-b7d3-4345-b6a9-2ed4a881accd` | `Converse` via `us.` profile. Message: `Error 002: Access to Bedrock models is not allowed for this account`. Use-case form stored; `CreateFoundationModelAgreement` also `ValidationException` / RequestId `8e7d2ece-e907-4a83-bed8-d2ee88f830d7`. Support case **178659049300631**. |
| `amazon.titan-embed-text-v2:0`                | 2026-08-12 | `ValidationException` | **400** | `243ec4e8-75e1-453d-952c-2a66cb39c493` | `InvokeModel`. Same Error 002 message.                                                                                                                                                                                                                                                |
| `amazon.nova-lite-v1:0`                       | 2026-08-12 | `ValidationException` | **400** | `1bea0fa4-397d-4c9c-a9c4-b1364909868c` | `Converse` + Playground. `get-foundation-model-availability` was AUTHORIZED/AVAILABLE; invoke still blocked. Captured with `aws … --debug`.                                                                                                                                           |
| `amazon.nova-lite-v1:0`                       | 2026-08-13 | `ValidationException` | **400** | *(not captured)*                       | Retest after payment fix (USD currency, Visa default, backup ACH). Same Error 002 body.                                                                                                                                                                                               |




### Support case log (account `562280272865`)


| Date       | Event                                                                                                                                     |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-12 | Case **178659049300631** opened (Account / Bedrock Error 002).                                                                            |
| 2026-08-13 | Automated recommendation: payment **authorization** failure (generic card message). Default was ACH ****1792; payment currency was unset. |
| 2026-08-13 | **Peter (Support):** valid payment on file, models AVAILABLE — **internal review** initiated. Case status: **Pending amazon action**.     |
| 2026-08-13 | Remediation: currency → **USD**; default → **Visa ****9061**; backup **ACH ****1792** enabled. Nova retest still Error 002.               |


**Working theory:** account-level Bedrock block pending AWS internal review (and/or payment authorization retry). Not IAM, not per-model enablement, not wrong model IDs. Plan B schedule unchanged (drop-dead **Sep 5, 2026**).

**S1 status:** **Accepted** (model decision). **Invoke access** on account
`562280272865` remains blocked (`ValidationException` / HTTP 400 / Error 002 body)
and tracked via Support case **178659049300631** + the schedule/Plan B section. Do not
treat catalog visibility as a closed access gate.

### Pre-Support checks (run while case is open)

Error 002 on **Amazon's own** Titan and Nova confirms an **account-level** block
(not per-model enablement — Bedrock auto-enables serverless models since Oct 2025).
Before waiting on Support:


| Check                         | Command / action                          | If it fails                                                                                                                                       |
| ----------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Org SCP?**                  | `aws organizations describe-organization` | Member of an Org you don't control → SCP may deny `bedrock:`*. **Invalidates Plan B** if a second account sits under the same Org. Run **first**. |
| **Regional or account-wide?** | Retry one Nova smoke in `us-east-1`       | Same Error 002 → account-level. Different result → reframes as regional.                                                                          |
| **Billing verified**          | Console → payment method active           | New/unverified billing produces this block class.                                                                                                 |
| **Force verification path**   | Launch `t3.micro` ~60 s, terminate        | Reported to unblock stuck new-account verification (~$0.01).                                                                                      |


Log results in the smoke table notes or journal.


| Check                 | Result (2026-08-13)                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| Org SCP               | **Pending** — run `aws organizations describe-organization`                                       |
| us-east-1 Nova smoke  | **Pending**                                                                                       |
| Billing verified      | **Partial** — USD + Visa default + backup ACH; ~$6.03 spend in `us-east-2`; Bedrock still blocked |
| t3.micro verification | **Pending**                                                                                       |




### Bedrock access schedule risk (managed)


| Sprint                  | Needs Bedrock?                                               |
| ----------------------- | ------------------------------------------------------------ |
| **S2** (Aug 24 – Sep 6) | **No** — hardcoded JSON skeleton. Safe to run while blocked. |
| **S3** (Sep 7 – Sep 20) | **Yes** — corpus ingest path leads to embed.                 |
| **S4+**                 | **Yes** — embed, generate, judge.                            |


**Primary path:** keep case **178659049300631** active. Check for a Support reply **twice per week** (Mon/Thu). If there is **no meaningful reply by Fri Aug 29, 2026**, reply on the case asking for escalation / Bedrock entitlement review — do not wait silently until drop-dead.

**Drop-dead:** **Fri Sep 5, 2026** (last weekday of S2, two calendar days before S3).  
That morning: re-run the three smokes on account `562280272865`. If any still returns `ValidationException` / HTTP 400 / Error 002 body, **execute Plan B the same day**. Do not start S3 on a hope that Support clears mid-sprint.

**Plan B (senior default if still blocked on Sep 5):** open a **second personal AWS account**, attach a payment method, re-run S1 catalog + invoke smokes there the same day, and move Lucid’s Bedrock / Lambda / S3 to that account (prefer `us-east-2` if invokes work; otherwise the region where smokes pass). Update ADR-0001 / 0002 / 0003 account+region notes (or a short superseding note). Leave case **178659049300631** open on the original account as a parallel recovery path — do not abandon it.

**Why this Plan B (and not the tempting ones):**

- **Not “embed locally in the zip Lambda.”** Ingest can be offline and the FAISS index can still ship in the package (ADR-0001). Query-time embedding must use the **same** model as ingest. A local embed stack (torch / sentence-transformers) in a **zip** Lambda blows the **250 MB** ceiling already measured. Generation + judge are **also** blocked by Error 002 today, so local-embed-only does not unblock S3/S4.
- **Not “slip S3 with no date.”** Calendar risk without a trigger is how December arrives with no baseline.
- **Not “switch to a non-Bedrock API mid-semester” as first escape.** That rewrites ADR-0002 under deadline. A second AWS account preserves the decided Bedrock shape with one afternoon of account bootstrap + smoke re-verify.

**Success criterion to leave Plan B unused:** all three smoke rows show a successful invoke (not `ValidationException`) on the project account before Sep 5 EOD.

### Cost worksheet assumptions (labeled, not measured)


| Piece                                              | Assumed tokens |
| -------------------------------------------------- | -------------- |
| Query embed                                        | 50             |
| Generator input (system + question + top-5 chunks) | 2,500          |
| Generator output (cited answer or refusal)         | 300            |
| Judge input (rubric + answer + evidence)           | 2,000          |
| Judge output                                       | 150            |
| Eval set                                           | 50 questions   |
| Re-runs this semester (TARGET)                     | 10 full passes |


**Dependency (explicit):** the **2,500** generator-input figure assumes ~**500
tokens per chunk** × top-5, plus system/question overhead. **Chunk size is not
decided until S3** (chunking LLD). If S3 lands near **1,024 tokens/chunk**,
top-5 context roughly doubles, generation cost scales up, and the per-pass /
semester Bedrock ceilings below must be recomputed before trusting them.

**Cost triggers (chosen now, before measured runs):**

- **Per-pass:** revisit if one 50-question harness pass exceeds **$0.50** in
Bedrock tokens (worksheet today ≈ **$0.21** gen+judge).
- **Semester ceiling:** revisit if cumulative Bedrock **eval** token spend
approaches **~$5** (worksheet 10×50 ≈ **~$2.10**; leaves headroom for chunk-size
drift and extra passes).

---



## Options considered — embedding



### Option A: Amazon Titan Text Embeddings V2 (`amazon.titan-embed-text-v2:0`)

- **How it works:** Bedrock embed API returns a dense vector for each chunk and
each query. Output size is configurable: 256, 512, or 1024.
- **Cost:** Idle $0. On-demand ≈ **$0.02 / 1M input tokens**. Query embed at 50
tokens ≈ **$0.000001**. Full ingest of ~50 papers is still cents.
- **Operational burden:** One `InvokeModel` call; model listed in `us-east-2`
catalog (verified 2026-08-12).
- **Risks / downsides:** English GA (100+ languages in preview). Dim choice is
permanent until re-embed + rebuild FAISS.



### Option B: Cohere Embed English v3 (`cohere.embed-english-v3`)

- **How it works:** Same embed-at-ingest / embed-at-query pattern; fixed 1024-d
vectors.
- **Cost:** Idle $0. On-demand ≈ **$0.10 / 1M tokens** (~5× Titan V2).
- **Operational burden:** Same Bedrock wiring.
- **Risks / downsides:** Pays 5× for no clear win on an English HCI corpus.



### Option C: Amazon Titan Embeddings G1 – Text (`amazon.titan-embed-text-v1`)

- **How it works:** Previous-gen Titan embed; fixed **1536-d** vectors.
- **Cost:** Similar class to V2 historically; larger vectors → bigger FAISS index.
- **Operational burden:** Still Bedrock; no reason to start a greenfield index on G1.
- **Risks / downsides:** Legacy path. Larger dim with no quality case for this MVP.

---



## Options considered — generation



### Option A: Amazon Nova Micro

- **How it works:** Smallest Nova text model on Bedrock; Lambda sends retrieved
context + question, model returns answer JSON or refusal.
- **Cost:** Idle $0. ≈ **$0.035 / 1M in**, **$0.14 / 1M out** →
~**$0.00013 / query** under the worksheet above.
- **Operational burden:** AWS-native ID; on-demand Bedrock.
- **Risks / downsides:** Weakest instruction following of the three. Confident
hallucination breaks the refuse requirement; eval metrics look “interesting”
while the product looks broken.



### Option B: Anthropic Claude Haiku 4.5

(`us.anthropic.claude-haiku-4-5-20251001-v1:0`)

- **How it works:** Current fast Claude tier on Bedrock (replaces Claude 3 Haiku
in this account’s catalog). Same RAG prompt shape; better at obeying “answer
only from context or refuse.”
- **Cost:** Idle $0. On-demand class ≈ **$1.00 / 1M in**, **$5.00 / 1M out**
(Bedrock/Marketplace figures on **2026-08-12**; re-check before README claims)
→ under the worksheet ≈ **$0.004 / query** generation
(2,500 × $1/1M + 300 × $5/1M).
  - 50 questions × 1 pass ≈ **$0.20** generation
  - 50 × 10 re-runs ≈ **~$2.00** generation only
- **Operational burden:** Call the `us.` inference profile from `us-east-2`
(in-region endpoints unavailable for this model). IAM needs
`bedrock:InvokeModel` on the **inference profile ARN** *and* on the underlying
foundation-model ARNs in **every region that profile can route to** — not only
the profile ID string. No Provisioned Throughput. One-time Anthropic **Submit
use case details** before first invoke (**S1**, with the smoke table above).
- **Risks / downsides:** ~30× Nova Micro per query. Cross-region routing adds IAM
surface and latency variance (request may be served outside `us-east-2`). Still
not Sonnet-class on hard multi-paper synthesis.



### Option C: Anthropic Claude Sonnet 5 (Bedrock)

- **How it works:** Stronger current Claude Sonnet tier (`anthropic.claude-sonnet-5`
/ `us.anthropic.claude-sonnet-5`). Best refusal/citation headroom of the set.
Same cross-region pattern as Haiku 4.5. **Not invoke-verified in this account**
— rejected on **eval-iteration cost**, not on a smoke test. (Catalog showed
Sonnet 4.6 in Aug 2026; current Bedrock Sonnet SKU is **Sonnet 5** per AWS
model card — pricing class unchanged for the rejection argument.)
- **Cost:** Idle $0. Sonnet-class Bedrock pricing ≈ **~$3 / 1M in** and
**~$15 / 1M out** (AWS model card / pricing page on **2026-08-12**) → roughly
**~$0.01+ / query**, so **several dollars** for 50 × 10 re-runs before judge
tokens. Affordable once; painful if the harness is flaky.
- **Operational burden:** Same Anthropic access + cross-region profile pattern;
higher spend if eval loops.
- **Risks / downsides:** Eval iteration cost dominates. Quality headroom we may
not need before a measured baseline exists.

---



## Options considered — judge (faithfulness)



### Option A: Same model as the generator

- **How it works:** Haiku also scores faithfulness.
- **Cost:** Cheapest operationally (one model ID).
- **Operational burden:** Trivial wiring.
- **Risks / downsides:** **Self-preference bias** — the judge favors its own
phrasing and under-reports hallucinations. Faithfulness numbers become
self-congratulation.



### Option B: Amazon Nova Lite (`amazon.nova-lite-v1:0`)

- **How it works:** Eval-only second call with a fixed rubric over answer +
retrieved chunks. Never on the live query path. Different provider family from
Anthropic Haiku.
- **Cost:** Idle $0. ≈ **$0.06 / 1M in**, **$0.24 / 1M out** →
~**$0.00016 / judge call**. 50 × 10 ≈ **~$0.08** semester judge spend.
- **Operational burden:** Second model ID + prompt; listed in `us-east-2` catalog
(verified 2026-08-12).
- **Risks / downsides:** Weaker judge than the generator has a **capability ceiling**
— it may miss fluent, plausible, subtly-unsupported hallucinations. Rubric quality
alone does not fix that. **Must validate the judge** before any faithfulness number
goes in the README (see Decision).



### Option C: Stronger cross-family judge (e.g. Nova Pro or Sonnet)

- **How it works:** Spend more on the grader than the generator.
- **Cost:** Multiplies eval cost; can exceed generation spend.
- **Operational burden:** Another SKU to keep available.
- **Risks / downsides:** Overkill before the harness exists. Revisit after the
first real faithfulness number looks noisy or gamed.

---



## Decision

**Embedding:** We will use **Amazon Titan Text Embeddings V2** at **1024
dimensions** (`amazon.titan-embed-text-v2:0`).

**Generation:** We will use **Claude Haiku 4.5** via the US geo inference profile
`us.anthropic.claude-haiku-4-5-20251001-v1:0` from `us-east-2` (on-demand,
cross-region; not in-region).

**Judge:** We will use **Amazon Nova Lite** (`amazon.nova-lite-v1:0`) for
LLM-as-judge faithfulness — not the generator.

Embedding tie-breaker vs Cohere: English corpus + 5× price gap; Titan wins.

**Dimensionality:** **1024**. At this corpus scale, index size is **not a binding
constraint** (ADR-0001 working estimate ~6 MB for ~1,000 × 1024-d vectors). So we
take Titan V2’s full width for retrieval quality — not because “512 wouldn’t save
much RAM.” ADR-0001 must treat vectors as **1024-d**.

Generation tie-breaker vs Nova Micro: refusal and instruction following. Micro
wins on price and loses the product. vs Sonnet 5: Haiku 4.5 is enough to ship a
refuse path while keeping ~10 full eval re-runs in the low-dollar range under the
worksheet (conditional on S3 chunk size — see above).

Judge tie-breaker: different provider family from Haiku to avoid self-preference
bias; Nova Lite keeps judge spend negligible for v0.

### Judge validation (S6 gate — before README faithfulness claims)

Cross-family judge kills self-preference bias but does not prove the judge works.
Before publishing faithfulness:

1. Hand-label **~15** generator outputs yourself (mix of faithful, partial, and
  hallucinated against retrieved chunks).
2. Run Nova Lite judge on the same 15 with the fixed rubric.
3. Report **agreement** (date, command, git SHA). Target: good enough to trust the
  metric directionally — no invented threshold; if agreement is poor, faithfulness
   is noise and we revisit judge choice (Option C) **before** S7 baseline.

Estimated effort: ~2 hours. This is the difference between a metric and a number.

### End-to-end cost (worksheet, TARGET)


| Path                                                   | Approx $                                            |
| ------------------------------------------------------ | --------------------------------------------------- |
| One live query — Bedrock only (embed + Haiku 4.5)      | ~$0.004                                             |
| One eval item — Bedrock only (query + Nova Lite judge) | ~$0.0042                                            |
| 50 × 10 eval passes — Bedrock only (gen + judge)       | **~$2.10**                                          |
| Ingest embed (~50 papers)                              | cents                                               |
| Lambda + API Gateway per query                         | **not computed here** — see ADR-0001 worksheet stub |


These are **Bedrock token** worksheet estimates — **not measured runs**, and
**conditional on ~500-token chunks**. End-to-end per-query cost in the README must
add ADR-0001 Lambda GB-seconds + API Gateway once memory is measured. Recompute
after S3 locks chunk size.

### Deprecation fallback

If a chosen model ID is deprecated or loses on-demand / profile access
mid-semester: switch to the nearest Bedrock peer in the same role (embed → other
Titan/Cohere embed; Haiku 4.5 → next Claude Haiku SKU first; Nova Lite on the live
path only as last resort). **Coupling:** if Nova Lite ever becomes the
**generator**, the **judge must move** to a different provider family — otherwise
self-preference bias returns and this ADR’s judge rationale is void. If `us.`
profile fails, try `global.` for the same Haiku SKU before changing models. If
embedding dims change, re-embed and rebuild FAISS, then re-run eval. One afternoon
of work, not a redesign.

---



## Consequences

**What gets easier.**

- Single AWS account path: Bedrock only, no external embed API keys.
- Embed bill stays invisible; FAISS index shape is fixed at 1024-d.
- Cross-family judge gives faithfulness a chance of meaning something.
- Region matches the real account (`us-east-2`).

**What gets harder.**

- Haiku 4.5 requires **cross-region inference profile** IAM (profile ARN +
foundation-model ARNs in all routeable regions) and a one-time Anthropic
use-case form before first invoke (**S1 smoke**, not deferred to S5).
- Cross-region routing: requests may be served from a US region we did not pick,
which adds latency variance into the p95 we will report in November (same
discipline as ADR-0001’s cold-start threshold — acknowledge now, measure later).
- Two generation-capable model IDs to prompt for (Haiku + Nova Lite).
- Haiku can still refuse poorly — we own the grounding prompt and must measure it.
- Nova Lite-as-judge may be noisy; early faithfulness is not gospel.
- Cost worksheet is coupled to an undecided S3 chunk size.
- Locked to Titan V2 vector space until we pay a full re-embed.
- Account currently cannot invoke Bedrock (`ValidationException` / Error 002);
managed via Support case + Sep 5 Plan B above.

**What we are locked into,** and how expensive it is to reverse.

- **1024-d Titan V2** index format (ADR-0001 FAISS file). Escape = re-embed all
chunks + rebuild index + redeploy artifact.
- Haiku 4.5 request/response shape + `us.` profile in the answer Lambda. Escape =
swap model/profile ID + re-tune prompts + re-run eval (embeddings unchanged).
- Judge protocol in the harness. Escape = swap judge ID; live users unaffected.
- `us-east-2` as the service region for Bedrock calls from Lambda.

---



## Revisit if

- Bedrock removes on-demand / inference-profile access for Haiku 4.5 or Titan V2
from `us-east-2`, **or**
- S3 picks a chunk size materially above ~512 tokens → **recompute the cost
worksheet** and the $0.50 / ~$5 triggers before treating them as binding, **or**
- Measured hallucination / refusal failure rate after S5 smoke eval is
unacceptable and a single Sonnet 5 A/B on the same 5 questions clearly wins,
**or**
- Judge validation (15-label agreement) is poor → faithfulness metric is unreliable;
swap judge before S7 baseline, **or**
- Faithfulness scores are unstable across judge re-runs and a stronger
cross-family judge is needed, **or**
- One 50-question harness pass exceeds **$0.50** in Bedrock tokens, **or**
cumulative Bedrock **eval** token spend approaches the **~$5** semester
ceiling (re-price from the AWS page and reassess Sonnet / Micro), **or**
- Drop-dead **Sep 5, 2026** smokes still fail → execute Plan B (second AWS
account) the same day.

