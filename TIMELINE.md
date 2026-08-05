# Fall 2026 Timeline — CISC 369 & Lucid

*Drafted Aug 5, 2026. Semester: Sep 9 – Dec 22.*

The only link between the two: papers read for 369's lit review can become Lucid's
corpus. Nothing else crosses — survey data never goes into Lucid, Lucid's code never
goes into the 369 repo, no AI help on 369's graded work.

**Open item:** survey collection is assumed to run Sep 9 – Oct 7 (first month), with
Pandas analysis starting ~Oct 7. Not yet confirmed with Hoefer — confirm at the first
check-in, along with mentioning Lucid to him.

## Week-by-week

| Week | Date | CISC 369 | Lucid |
|---|---|---|---|
| 1 | Sep 9 | Check-in. Survey collection opens. Lit review reading starts. Mention Lucid to Hoefer. | Phase 0: repo scaffold, honest README, GitHub link live |
| 2 | Sep 16 | Check-in. Collection ongoing, lit review continues. | Phase 1: pick ~50 papers, get into S3 |
| 3 | Sep 23 | Check-in. Collection ongoing. | Chunking: size/overlap tradeoffs, write the chunker |
| 4 | Sep 30 | Check-in. Collection closes end of week. | Embeddings via Bedrock, sanity-check retrieval quality |
| 5 | Oct 7 | Check-in. Data in hand — start the Pandas pipeline. Annotated bibliography checkpoint. | Phase 2: query handler — embed question → retrieve top-k |
| 6 | Oct 14 | Check-in. Analysis underway. | Generation: chunks + question → Bedrock LLM, force citations |
| 7 | Oct 21 | Check-in. Analysis underway. | Add refusal logic |
| 8 | Oct 28 | Check-in. Analysis wrapping / draft findings. | Phase 3: build the 50-question labeled eval set |
| 9 | Nov 4 | Check-in. Fold findings into paper. | recall@k + faithfulness (LLM-as-judge) + hallucination rate |
| 10 | Nov 11 | Check-in. Paper drafting. | Latency/cost tracking, record first real baseline |
| 11 | Nov 18 | Check-in. Paper drafting. | Phase 4: reranking or stricter grounding prompt, re-run eval |
| 12 | Nov 25 | Light week — paper drafting. | Before/after comparison, write results into README |
| 13 | Dec 2 | Check-in. Paper draft due for review. | Phase 5: SAM deploy, API Gateway + Lambda live |
| 14 | Dec 9 | Check-in. Design recommendations section. | CI green, CloudWatch showing latency + cost |
| 15 | Dec 16 | Finals week: paper + repo finalized, public. | Buffer / stretch if ahead |
