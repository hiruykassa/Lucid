# Lucid

A serverless AWS RAG service that answers questions about **AI dark patterns and digital
well-being** from a curated corpus of HCI papers. Every answer cites its sources. The
system refuses when the corpus doesn't support an answer. It ships with an evaluation
harness that measures grounding and trustworthiness.

**Status: nothing is built yet.** As of 2026-08-08 this repository contains an operating
contract, document templates, and three unwritten architecture decision records. There is
no code, no deployed endpoint, and no measured result. This section will say something
different only when that changes.

## Intended architecture

```
Query:     API Gateway → Lambda → embed question → retrieve top-k → Bedrock LLM → cited JSON
Ingestion: S3 (raw papers) → chunk → embed (Bedrock) → vector store
```

Python · Bedrock · Lambda · API Gateway · S3 · SAM · GitHub Actions · CloudWatch ·
pytest. The vector store and the models are undecided — see `docs/adr/`.

## Results

None yet. When this project has measured something, the numbers appear here with the
date, the command, and the commit that produced them. Until then this section stays
empty rather than aspirational.

## Repository

```
docs/ONBOARDING.md   what to build, in what order
docs/adr/            decisions, and why the system isn't something else
docs/design/         how each component works, written before it exists
docs/runbooks/       what to do when it breaks
docs/coe/            what broke, why, and what changed as a result
docs/journal/        weekly engineering log
CLAUDE.md            how this project is run
```

## About

Built by [Hiruy Kassa](https://github.com/hiruykassa) as a self-directed engineering
project. It's run deliberately like a team project rather than a side project: designs
are written and reviewed before code, nothing merges without review, and no number
appears in this repository that wasn't actually measured.
