# ADR-0002: Embedding and generation models

- **Status:** Not started — assigned to Hiruy
- **Date:** —
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

> **Assignment brief. Delete below the line and write the ADR from `TEMPLATE.md`.**

---

## The ask

Two model choices, one ADR, because they're coupled by cost and by the eval harness:

- **Embedding model** — used at ingest for every chunk and at query time for every
  question. Determines vector dimensionality, which feeds straight back into ADR-0001.
- **Generation model** — takes retrieved chunks plus the question and produces the cited
  answer or the refusal.

There is a third, quieter choice hiding in here: **the judge model** for LLM-as-judge
faithfulness scoring. Decide whether it's the same model as the generator, and defend it.
Using a model to grade its own output has a name and a known failure mode. Find out what
it is before review.

## Questions I'll ask in review

1. **Cost per query, end to end.** Embedding tokens plus input tokens plus output tokens,
   at real prices, for a realistic query. Then multiply by ~50 eval questions times
   however many times you'll re-run the harness. That second number is the one that
   decides whether you can afford to iterate. Show it.

2. **What's the dimensionality, and did you tell ADR-0001?** If these two ADRs disagree
   about vector size, one of them is wrong.

3. **Is the model available in your region, on demand, without a quota request?** Check.
   Model availability varies by region and this has ended projects in December.

4. **Cheap generator or good generator?** You have a refusal requirement. A weaker model
   that hallucinates confidently makes your hallucination metric look interesting but
   your product look broken. Argue the trade rather than defaulting to the cheapest.

5. **What's your fallback if the chosen model is deprecated mid-semester?** One sentence
   is enough, but have one.

## Definition of done

Follows `TEMPLATE.md`. Prices sourced and dated. Dimensionality stated and consistent
with ADR-0001. The judge-model decision is addressed explicitly, not skipped.
