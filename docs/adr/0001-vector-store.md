# ADR-0001: Vector store

- **Status:** Accepted
- **Date:** 2026-08-10 (accepted 2026-08-13)
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

---

## Context

Lucid needs somewhere to store chunk embeddings and run nearest-neighbor search for
~50 curated HCI papers. The query path is API Gateway → Lambda → retrieve top-k →
Bedrock. This ADR picks the vector store before S2 packaging depends on it.

**Budget (chosen constraint):** ≤ **$5/month** for the vector-store / storage side of
this project — what the internship budget allows here, not an AWS-imposed floor.

**Region:** `us-east-2` (same as ADR-0002 Bedrock and ADR-0003 corpus bucket —
do not split or ingest pays cross-region transfer).

**Lambda target for packaging numbers below:** Python **3.12**, architecture
**x86_64**. (arm64/Graviton is cheaper per GB-second; if S2 switches arch, redo the
size measurement on aarch64 wheels before locking the zip.)

**Scale (derived estimate, not a measured corpus yet):**


| Step                         | Assumption                                              | Result                                  |
| ---------------------------- | ------------------------------------------------------- | --------------------------------------- |
| Papers                       | ~50                                                     | —                                       |
| Chunks                       | ~512-token chunks; ~10-page paper ≈ ~20 chunks          | ~1,000 chunks                           |
| Dims                         | ADR-0002: Titan Text Embeddings V2 → **1024-d** float32 | 4 bytes × 1024 = **4,096 bytes/vector** |
| Vector bytes                 | 1,000 × 4,096                                           | ≈ **4.0 MB**                            |
| Chunk text + FAISS structure | rough order of magnitude                                | ≈ **1–2 MB**                            |
| **Working total**            | vectors + text + index overhead                         | ≈ **~6 MB**                             |


So the index itself is small (~6 MB). If ADR-0002 changes dimensionality, re-embed and
rebuild. After S3/S4, replace these assumptions with measured chunk counts.

**Packaging constraint:** a zip-based Lambda (including layers) may not exceed
**250 MB unzipped**
([AWS Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)).
`faiss-cpu` + `numpy` dominate the package; see Option C and Decision for the measured
result and conclusion (**zip works; containers not required**).

## Options considered



### Option A: OpenSearch Serverless

- **How it works:** Managed search/vector collections. AWS scales compute (OCUs). No
cluster to size yourself.
- **Cost:** Indexing/search ~$0.24/OCU-hour; hot storage ~$0.024/GB-month. Classic keeps
a minimum OCU floor 24/7 (above the $5 budget). NextGen can scale compute to zero when
idle.
- **Operational burden:** Collection, mappings, IAM, alarms, Lambda → endpoint wiring.
Watch OCU spend and NextGen wake latency.
- **Risks / downsides:** Classic idle cost blows the budget. NextGen cold start after
scale-to-zero is **~10–30 seconds** on the first request to a component
([AWS: Scale to zero for OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-scale-to-zero.html);
AWS blog also cites ~10 seconds for capacity return).
- **What it teaches:** Managed vector search ops — less about how similarity search
works under the hood.



### Option B: pgvector (RDS or Aurora Serverless)

- **How it works:** Postgres + pgvector. Vectors in a table; k-NN via SQL. RDS
(always-on) or Aurora Serverless v2 (ACUs, optional pause).
- **Cost:** e.g. `db.t4g.micro` always-on is already ~$12/month before storage — over
budget. Aurora warm floors are higher; scale-to-zero helps cost but adds resume latency.
- **Operational burden:** DB standup, schema/migrations, credentials/VPC, connection
handling, alarms. More surface than FAISS-in-Lambda.
- **Risks / downsides:** Always-on floors miss the $5 budget; pause/resume adds latency
and Postgres ops you do not need for a tiny corpus.
- **What it teaches:** SQL + relational ops around vectors — useful later, heavy for MVP.



### Option C: FAISS in Lambda, index in the deployment package

- **How it works:** Build a FAISS index file of embeddings. **Ship that file inside the
Lambda deployment package (zip)** with the function code. On invoke, Lambda loads the
index into memory and runs similarity search in-process. Corpus / re-embed updates
mean rebuild the index and **redeploy** the function (new package). Not stored in S3
for the query path.
- **Cost:** Idle vector service ≈ $0. Pay Lambda per invoke / GB-second when queries run.
No always-on OpenSearch/Postgres floor. Fits the ≤$5 storage budget easily.
- **Operational burden:** Own index build, bake into package, FAISS packaging (layer).
Breakages: stale index after a corpus change without redeploy, OOM, cold start while
loading FAISS from local disk.
- **Risks / downsides:**
  - **Index size is not the main risk** (~6 MB). **Library size is** — see measured
  footprint below. Must stay under **250 MB** unzipped.
  - Every corpus update is a redeploy. Cold start still pays FAISS load time (no S3
  download).
- **What it teaches:** How in-process nearest-neighbor search works end to end — load
vectors, score similarity, return top-k. That is whiteboardable without a managed
search product in the middle, which is a real criterion for this internship, not only
a cost win.



#### Library size measurement (reproducible)

**Date:** 2026-08-12. **Host Python:** 3.14 locally only used to run `pip download` /
unzip; **target ABI:** cp312, **platform:** `manylinux_2_28_x86_64` (Lambda x86_64).

**Pinned artifacts:**


| Package        | Version    | Wheel                                                                         | Unzipped     |
| -------------- | ---------- | ----------------------------------------------------------------------------- | ------------ |
| `faiss-cpu`    | **1.15.0** | `faiss_cpu-1.15.0-cp310-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl` | **65.9 MB**  |
| `numpy`        | **2.5.2**  | `numpy-2.5.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl`     | **57.1 MB**  |
| **Total libs** |            |                                                                               | **123.0 MB** |


**Command** (rerun this; do not trust the table alone):

```bash
mkdir -p /tmp/lucid-vs-size/{wheels,extract} && cd /tmp/lucid-vs-size
python3 -m pip download --only-binary=:all: \
  --platform manylinux_2_28_x86_64 \
  --python-version 312 --implementation cp --abi cp312 \
  -d wheels 'faiss-cpu==1.15.0' 'numpy==2.5.2'
python3 - <<'PY'
import zipfile
from pathlib import Path
total = 0
for whl in sorted(Path("wheels").glob("*.whl")):
    dest = Path("extract") / whl.stem
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(whl) as z:
        z.extractall(dest)
    size = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    total += size
    print(f"{whl.name}: unzipped={size/1e6:.1f} MB")
print(f"TOTAL={total/1e6:.1f} MB")
PY
```

**Caveat:** `--platform manylinux2014_x86_64` only resolves older `faiss-cpu` (e.g.
1.9.0.post1 ≈ **113 MB** unzipped alone; with `numpy` 2.2.6 ≈ **168.5 MB** total). That
is a different artifact set — pin versions and the platform tag together.

**Strip note (if we ever ship 1.9.x-style wheels):** those builds embed multiple CPU
variants (`_swigfaiss.so`, `_swigfaiss_avx2.so`, `_swigfaiss_avx512.so`, ~37 MB each).
Keep one; delete the others at package time (~70 MB saved). `faiss-cpu` **1.15.0** as
measured above does not ship that triple; stripping is optional insurance if the pin
moves backward.

## Decision

We will use **FAISS loaded in the Lambda, with the index file baked into the deployment
package** (Option C), on **Python 3.12 / x86_64**, with **zip** packaging (not a
container image).

**Tie-breaker:** A and B’s always-on floors exceed the **≤$5/month** storage budget we
set for this project; C is ~$0 idle. The derived index size (~6 MB) fits in Lambda
memory. We accept redeploy-on-corpus-change for a simpler cold path and fewer moving
parts.

**Learning criterion (said out loud):** being able to whiteboard in-process similarity
search is worth something here; the call is not purely economic.

**Packaging conclusion (S1 zip-size check — closed):**


| Piece                              | Size        | Source                                                   |
| ---------------------------------- | ----------- | -------------------------------------------------------- |
| `faiss-cpu` 1.15.0 + `numpy` 2.5.2 | **123 MB**  | **Measured** 2026-08-12 (command above)                  |
| Index                              | ~6 MB       | **Derived** from scale table (not a measured corpus yet) |
| App / deps headroom                | ~5 MB       | **Allowance** (boto3, handler code — not measured yet)   |
| **Working total**                  | **~134 MB** | 123 + 6 + 5                                              |
| Lambda zip/layer ceiling           | 250 MB      | AWS quota                                                |
| **Margin**                         | **~116 MB** | 250 − 134                                                |


Even under the larger alternate wheel set (~168.5 MB libs + ~11 MB index/app ≈
**~180 MB**), margin is still **~70 MB**. **Zip deploy works. Containers are not
required for S2.**

**Lambda memory (open until measured):** memory setting controls CPU allocation,
which controls how long `import faiss` + index load take — the dominant cold-start
cost. **Decision deferred to measurement**, not guessed here. Target settings to
probe: **512, 1024, 1769, 3008 MB** (1769 MB ≈ one vCPU per AWS docs).

### Cold-start measurement (S1 — no Bedrock required)

Bedrock invoke is verified (ADR-0002, 2026-08-21). This measurement still does
**not** need Bedrock and remains the largest open packaging risk in this ADR:

1. Deploy a throwaway Lambda in `us-east-2` with the measured `faiss-cpu` +
  `numpy` package (same pins as above).
2. Bake in a **synthetic** index: 1,000 × 1024 float32 vectors (random is fine —
  Titan produced vectors are not required).
3. At handler init: load FAISS, load index, run one top-5 search.
4. Log **init duration** (import + load) at each memory setting above.
5. After ≥15 min idle, invoke enough times to estimate **p95** request → first byte.

Record date, git SHA, memory setting chosen, and measured p95 in `docs/journal/`.
Compare to the pre-registered trigger: **p95 > 5.0 s** after idle → revisit.

**End-to-end query cost (worksheet stub, TARGET):** ADR-0002 covers Bedrock tokens
(~$0.004/query). This ADR owns the Lambda side — not yet computed:


| Piece             | Assumed                                  | Cost (TARGET, not measured)  |
| ----------------- | ---------------------------------------- | ---------------------------- |
| Lambda GB-seconds | TBD after memory pick + cold/warm timing | pennies at this scale        |
| API Gateway       | ~1 request                               | ~$0.0000035 (HTTP API class) |


README end-to-end cost must sum Bedrock (0002) + Lambda + API Gateway once memory
is chosen and a timed invoke exists.

**Runner-up:** pgvector (B) if we later need SQL/metadata filters or a shared DB and can
raise the budget. OpenSearch (A) last for this MVP.

## Consequences

**What gets easier.**

- Stays under the ≤$5/month storage budget: no always-on vector service.
- One artifact to deploy: code + FAISS libs + index file (zip).
- Matches API Gateway → Lambda without standing up OpenSearch or Postgres.
- Forces learning the retrieval path in-process.

**What gets harder.**

- Corpus or embedding changes require **rebuild index + redeploy** (coupled to
ADR-0003 corpus version bumps).
- Cold starts: first request after idle waits on Lambda wake + loading FAISS from disk.
- We own packaging FAISS (pin versions; optional AVX strip if an older wheel returns).
- Less room to grow without a redesign: huge indexes, shared DB, or rich SQL filters
push toward B or A.

**What we are locked into,** and how expensive it is to reverse.

- Locked into “FAISS index-as-file inside the Lambda package” on **x86_64** until we
migrate.
- Escape hatch: move index to S3-load-on-start (still FAISS), switch to arm64 (remeasure
wheels), or migrate to pgvector / OpenSearch. Cost = rebuild/re-ingest + change the
retrieval client; embeddings can stay if dimensionality does not change.



## Revisit if

- Unzipped package (libs + index + app) exceeds **200 MB** (leaves <50 MB margin under
the 250 MB ceiling — time to strip wheels or reconsider containers), **or**
- Measured index size approaches Lambda memory limits, **or**
- We raise / drop the ≤$5/month storage budget and can afford B or A, **or**
- Redeploy-on-every-corpus-change becomes unacceptable and we want index-in-S3 instead,
**or**
- We need SQL/metadata-heavy retrieval FAISS-in-process cannot do cleanly, **or**
- We switch Lambda architecture to **arm64** (remeasure aarch64 wheels before deploy),
**or**
- **Cold-start trigger (chosen before measurement):** after ≥15 minutes idle, if
**p95** latency from request received → first response byte on a cold invoke is
**> 5.0 seconds**, revisit (keep-warm, provisioned concurrency, or packaging change).
Run the synthetic-index measurement in **S1** (see above); do not move this
threshold after seeing the number, **or**
- Synthetic cold-start measurement at chosen memory still exceeds **5.0 s p95**
after idle (escape hatches get expensive in December).

