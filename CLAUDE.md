# Lucid — Project Instructions for AI Assistants

Serverless AWS RAG service that answers questions about **AI dark patterns and
digital well-being** from a curated ~50-paper HCI corpus. Every answer cites its
sources; the system refuses when the corpus doesn't support an answer. Ships with an
**evaluation harness** that measures grounding and trustworthiness.

## How to help me

- Rising senior CS (St. Thomas), targeting a 2027 AI-engineer/SDE internship at Amazon.
- I must be able to whiteboard every core piece with no AI. **Guided discovery**:
  explain the concept, show the shape, let me write the code — especially retrieval,
  the Bedrock call, chunking, and eval metrics. Boilerplate/config/glue is fine to
  generate outright.
- **Real numbers only** — nothing on the resume or in the README that I haven't
  actually measured.
- Tie explanations to AWS services (studying for Cloud Practitioner).
- Pull me back to the MVP when I over-scope.

## Flow

Papers → S3 → chunk → embed (Bedrock) → vector store. Query: embed question →
retrieve top-k → Bedrock LLM generates a cited answer, or refuses if unsupported.

## Eval harness (the differentiator — do not cut)

~50 labeled questions, each with source passages + a reference answer. Metrics:
recall@k, faithfulness (LLM-as-judge), hallucination rate, p50/p95 latency, cost/query
(CloudWatch). Workflow: baseline → change (reranking/prompt) → re-run → show the delta
in the README.

## Architecture

```
User → API Gateway → Lambda: embed question → retrieve top-k → Bedrock LLM → cited JSON answer
Ingestion: S3 (raw papers) → chunk → embed (Bedrock) → vector store
IaC: SAM | CI: GitHub Actions | Observability: CloudWatch
```

## Stack

Python · Bedrock (embeddings + LLM) · OpenSearch Serverless (or pgvector/FAISS for a
leaner MVP) · Lambda + API Gateway · S3 · SAM · GitHub Actions · CloudWatch · pytest.

## Repo structure

```
lucid/
  infra/  ingest/  api/  eval/  tests/  .github/  README.md
```

## Must be able to explain (interview-ready)

RAG · embeddings/cosine similarity · chunking trade-offs · recall@k · reranking ·
grounding prompts/citations · LLM-as-judge · faithfulness vs. hallucination ·
API Gateway → Lambda → Bedrock request flow · IaC · CI.

## Build plan → December 2026

Retimed to the CISC 369 semester (Sep 9 – Dec 22, 2026). Week-by-week mapping against
both Lucid and 369 lives in `TIMELINE.md`.

Phase 0 Scaffold → 1 Ingest → 2 Answer → 3 Eval baseline → 4 Improve & re-measure →
5 Deploy → 6 Polish (stretch).

## Definition of Done

- [ ] ~50 papers ingested and searchable
- [ ] Live endpoint returns cited answers, refuses unsupported ones
- [ ] Eval harness with real numbers + results table in README
- [ ] SAM + GitHub Actions CI passing
- [ ] CloudWatch showing latency + cost
- [ ] README I can defend line-by-line

Small, complete, measured, mine — not a polished product.

## Target metrics (unmeasured — do not put these on a resume until real)

Faithfulness ≈90%, recall@5 ≈85%, hallucination ~18%→~6% after reranking, p95 <2.5s,
cost <$0.01/query, deploy <5min, ~6 CI checks passing.

## Non-goals

No user accounts/auth, no multi-tenant, no fine-tuning, no massive corpus, no mobile app.

## Open decisions

Vector store (OpenSearch vs. pgvector vs. FAISS-in-Lambda) · which Bedrock models ·
which ~50 papers + licensing · faculty buy-in for building the tool.

## Boundary with CISC 369 / ATEC

Supports CISC 369 as a lit-exploration tool; the survey-analysis Pandas track is
separate and never touches Lucid. Sibling project ATEC (live prod app, hybrid RRF
search) has a synthesis feature but not per-answer citations — that's ATEC's future
roadmap, not Lucid's. Lucid's citations + eval harness are core from day one.

Repo: https://github.com/hiruykassa/Lucid
