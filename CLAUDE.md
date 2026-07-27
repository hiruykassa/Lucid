# Lucid — Project Instructions for AI Assistants

Lucid is a small serverless AWS service that answers questions about **AI dark patterns
and digital well-being** using only a curated corpus of ~50 HCI research papers. It returns
answers with **inline citations**, refuses when the corpus doesn't support an answer, and
ships with an **evaluation harness** that measures how grounded and trustworthy the answers are.

This file is the working source of truth for how to help on this repo.

---

## How to help me (read first)

- I'm a rising senior CS student (Univ. of St. Thomas, grad Dec 2027) targeting a 2027
  AI-engineer / SDE internship at Amazon.
- **Be honest about my skill level.** I've vibe-coded past projects I couldn't explain.
  The point of Lucid is the opposite: I must be able to whiteboard every core piece with
  no AI. Verify claims against my actual code before assuming I know something.
- **Prefer guided discovery.** Explain the concept, show me the *shape* of the solution,
  and let me write the code. Do **not** hand me finished implementations for the core logic
  (retrieval, the LLM/Bedrock call, chunking, the eval metrics). Boilerplate, config, and
  glue are fine to generate; the ideas are mine to own.
- **Real numbers only.** Any metric on my resume or in the README must be something I
  actually measured. Never fabricate or pad results.
- **Tie learning to AWS.** I'm studying for AWS Cloud Practitioner; reinforce those
  services as we use them.
- **When I over-scope, pull me back to the MVP** (see Definition of Done). Small-but-done
  beats big-but-half-built.

## What it does (user flow)

1. Curate ~50 papers on dark patterns / persuasive design / digital addiction.
2. Ingest: chunk → embed (Bedrock) → store vectors; raw docs in S3.
3. User asks a question.
4. Retrieve top-k chunks → send chunks + question to a Bedrock LLM → return an answer that
   uses **only** those sources, with citations to the specific paper/passage.
5. If the corpus doesn't support an answer, say so rather than inventing one.

## Evaluation harness (the differentiator — do NOT cut)

- Labeled test set: ~50 questions, each with source passage(s) + a short reference answer.
- Metrics: retrieval **recall@k**; answer **faithfulness** (LLM-as-judge); **hallucination
  rate**; **p50/p95 latency** and **cost per query** (CloudWatch).
- Workflow: run harness → record baseline → make a change (reranking, prompt tweak) →
  re-run → show the numbers move. Commit a results table to the README.

## Architecture (serverless AWS)

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
vector store: OpenSearch Serverless (default) or pgvector/FAISS for a leaner MVP ·
Lambda + API Gateway · S3 (raw docs) · AWS SAM (IaC) · GitHub Actions (CI) · CloudWatch ·
pytest.

## Repo structure

```
lucid/
  infra/    # AWS SAM template + deploy config
  ingest/   # load papers -> chunk -> embed -> index
  api/      # query handler: retrieve -> generate -> cite
  eval/     # labeled test set + metrics harness + results
  tests/    # pytest
  .github/  # CI workflow
  README.md # honest status + architecture + eval results
```

## Concepts I must be able to explain (interview-ready)

RAG (why retrieve then generate) · embeddings (what a vector represents, cosine similarity) ·
chunking (size/overlap trade-offs) · vector search / recall@k · reranking · grounding
prompt / citations · LLM-as-judge evaluation · faithfulness vs. hallucination · serverless
request flow (API Gateway → Lambda → Bedrock) · infrastructure as code · CI. If I can't
explain one, that's the next thing to learn — not skip.

## Build plan (phased, finishable by September 2026)

- **Phase 0 — Scaffold:** repo + honest README (status table, architecture, "in active
  development"). Make the GitHub link live.
- **Phase 1 — Ingest:** ~50 papers in S3; chunk → embed → index. Verify vector search
  returns sensible passages.
- **Phase 2 — Answer:** query path that retrieves top-k and generates a cited answer;
  refuses when unsupported.
- **Phase 3 — Eval baseline:** build the ~50-question labeled set; implement recall@k,
  faithfulness, hallucination, latency, cost; record a baseline.
- **Phase 4 — Improve & re-measure:** add reranking + strict grounding prompt; re-run;
  show numbers move; write results into the README.
- **Phase 5 — Deploy:** SAM deploy; API Gateway + Lambda live; CI green; CloudWatch alarms.
- **Phase 6 — Polish (stretch):** tiny React UI; query rewriting; broader corpus.

## Definition of Done (September MVP)

- [ ] ~50 papers ingested and searchable.
- [ ] Live AWS endpoint that returns cited answers and refuses unsupported ones.
- [ ] Eval harness producing real numbers, with a results table in the README.
- [ ] Infrastructure as code (SAM) + GitHub Actions CI passing.
- [ ] CloudWatch showing latency + cost.
- [ ] README I can defend line-by-line.

Done = small, complete, measured, and mine. Not a polished product.

## Target metrics (TARGETS — replace with measured results)

- Answer faithfulness ≈ 90%; recall@5 ≈ 85% on a 50-question set.
- Hallucination rate ~18% → ~6% after reranking + grounding prompt.
- p95 latency < 2.5 s; cost < $0.01 / query.
- Deploy time < 5 min; ~6 passing CI checks.

## Non-goals (scope guardrails)

No user accounts/auth · no multi-tenant product · no model fine-tuning · no massive corpus ·
no mobile app. Depth over breadth.

## Open decisions to confirm

- Vector store: OpenSearch Serverless vs. pgvector vs. FAISS-in-Lambda (cost vs. simplicity).
- Bedrock models: which embedding model + which answer LLM (cost/quality).
- Corpus sourcing: which ~50 papers, and license/access for full text.
- Faculty buy-in: confirm research sponsor supports building this tool (not just a paper).

## Context

Supports Fall 2026 faculty research **CISC 369** ("AI Dark Patterns & Digital Well-Being")
as a literature-exploration tool. The research's **survey-data analysis is a separate
Pandas track** — Lucid's corpus is the research literature, not the survey data. Sibling
project **Ask the Early Church (ATEC)** is retrieval-only on Render; Lucid is deliberately
different (adds generation + citation + eval, serverless on AWS).

Repo: https://github.com/hiruykassa/Lucid
