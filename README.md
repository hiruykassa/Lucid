# Lucid

A small serverless AWS service that answers questions about **AI dark patterns and
digital well-being** using only a curated corpus of ~50 HCI research papers. Answers
come with inline citations, refuse when the corpus doesn't support them, and are
measured by an evaluation harness (retrieval recall, faithfulness, hallucination rate,
latency, cost).

**Status: in active development — Phase 0 (scaffold).** No papers ingested yet, no
live endpoint, no eval numbers. Everything below marked "target" is a goal, not a
measured result.

## Status

| Phase | What | Status |
|---|---|---|
| 0 | Scaffold + honest README | In progress |
| 1 | Ingest: chunk → embed → index ~50 papers | Not started |
| 2 | Query path: retrieve → generate cited answer → refuse when unsupported | Not started |
| 3 | Eval baseline: 50-question labeled set, recall@k, faithfulness, hallucination, latency, cost | Not started |
| 4 | Improve (reranking, stricter grounding prompt) + re-measure | Not started |
| 5 | Deploy: SAM + API Gateway + Lambda live, CI green, CloudWatch alarms | Not started |
| 6 | Polish (stretch): tiny UI, query rewriting, broader corpus | Not started |

## Architecture

```
User --HTTPS--> API Gateway --> Lambda (query)
                                  1. embed question (Bedrock)
                                  2. retrieve top-k (vector store)
                                  3. generate cited answer (Bedrock LLM)
                                --> JSON answer + citations

Ingestion (Lambda or script): S3 (raw papers) --> chunk --> embed (Bedrock) --> vector store
IaC: AWS SAM   |   CI: GitHub Actions (lint, tests, eval)   |   Observability: CloudWatch
```

## Tech stack

Python (ingestion, API handler, eval) · Amazon Bedrock (embeddings + answer LLM) ·
vector store: **FAISS-in-Lambda** (tentative — see Open decisions) · Lambda + API Gateway ·
S3 (raw docs) · AWS SAM (IaC) · GitHub Actions (CI) · CloudWatch · pytest.

## Repo structure

```
lucid/
  infra/    # AWS SAM template + deploy config
  ingest/   # load papers -> chunk -> embed -> index
  api/      # query handler: retrieve -> generate -> cite
  eval/     # labeled test set + metrics harness + results
  tests/    # pytest
  .github/  # CI workflow
  README.md # this file
```

## Definition of Done (September 2026 MVP)

- [ ] ~50 papers ingested and searchable
- [ ] Live AWS endpoint that returns cited answers and refuses unsupported ones
- [ ] Eval harness producing real numbers, with a results table below
- [ ] Infrastructure as code (SAM) + GitHub Actions CI passing
- [ ] CloudWatch showing latency + cost
- [ ] README defensible line-by-line

## Eval results

Not measured yet. This table gets filled in after Phase 3 (baseline) and updated
again after Phase 4 (reranking + grounding prompt). Target ranges from the project
plan, **not real numbers**:

| Metric | Target |
|---|---|
| Recall@5 | ≈ 85% |
| Faithfulness | ≈ 90% |
| Hallucination rate | ~18% → ~6% after reranking + grounding prompt |
| p95 latency | < 2.5 s |
| Cost / query | < $0.01 |

## Open decisions

- **Vector store**: tentatively FAISS-in-Lambda for MVP simplicity (no extra AWS
  service to provision or pay for). pgvector or OpenSearch Serverless remain options
  if FAISS-in-Lambda hits a scaling or persistence wall — revisit in Phase 1.
- Bedrock models: which embedding model + which answer LLM (cost/quality) — TBD in Phase 1/2.
- Corpus sourcing: which ~50 papers, and license/access for full text — TBD in Phase 1.
- Faculty buy-in: confirm CISC 369 research sponsor supports building this tool.

## Context

Supports Fall 2026 faculty research **CISC 369** ("AI Dark Patterns & Digital
Well-Being") as a literature-exploration tool. The survey-data analysis is a
separate Pandas track — Lucid's corpus is the research literature only. Sibling
project **Ask the Early Church (ATEC)** is retrieval-only on Render; Lucid adds
generation + citation + eval, serverless on AWS.

Repo: https://github.com/hiruykassa/Lucid
