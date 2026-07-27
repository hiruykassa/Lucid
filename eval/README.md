# eval/

The evaluation harness — Lucid's differentiator. Holds the ~50-question
labeled test set (question + source passage(s) + reference answer) and the
metrics code: retrieval recall@k, answer faithfulness (LLM-as-judge),
hallucination rate, p50/p95 latency, and cost per query.

Phase 3 (baseline) and Phase 4 (re-measure after reranking/prompt changes) of
the build plan. Metric implementations are core logic — left for guided
implementation. Results get written back into the root README as a table,
using real measured numbers only.
