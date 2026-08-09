# ADR-0001: Vector store

- **Status:** Not started — assigned to Hiruy
- **Date:** —
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

> **This file is an assignment, not a document.** Delete everything below the line and
> write the ADR using `TEMPLATE.md`. The material below is the brief, not the answer.

---

## The ask

Lucid needs somewhere to put roughly 50 papers' worth of embedded chunks and query them
by vector similarity. Pick where. Write the ADR. Nothing else in the ingest or retrieval
path can start until this is Accepted.

## Candidates you must cover

At minimum: **OpenSearch Serverless**, **pgvector** (on RDS or Aurora Serverless v2),
and **FAISS loaded in the Lambda**. If you find a fourth that's genuinely in the running,
add it — but don't pad the list with options you never seriously considered. A padded
options section is worse than three honest ones.

## Questions I'll ask in review, so answer them first

1. **What does each option cost me at 3am on a Tuesday when nobody is using it?** Idle
   cost is the number that kills student projects. Find it, cite the pricing page, and
   put the date you looked next to it. One of these three has an idle floor that should
   end the discussion on its own — I want to see you find it rather than me tell you.

2. **How big is the corpus, actually?** ~50 papers → how many chunks → how many vectors
   → at what dimensionality → how many megabytes? Estimate it before you shop. If the
   whole index fits in memory, an entire category of infrastructure becomes unnecessary,
   and you can't know that without the number. Show the arithmetic.

3. **What happens on a cold start?** If the index has to be pulled from S3 and loaded
   into the Lambda, how long is that, and what does it do to the p95 you're going to
   report in the README? If it's a managed service, what's the network hop cost per query?

4. **Which one can you whiteboard?** You have to explain retrieval in an interview with
   no notes. "The managed service does it" is not an explanation. Weigh this explicitly —
   it's a legitimate criterion for this project and you should say so in the ADR rather
   than pretending the decision is purely technical.

5. **What's the migration cost if you're wrong in November?** If your retrieval layer
   is behind an interface, the answer might be "an afternoon." If it isn't, say so.

## What a bad version of this ADR looks like

- Three options where two exist only to make the third look good.
- Cost stated as "cheap" / "expensive" / "free tier" with no figure and no source.
- No consequences section, or a consequences section that only lists upsides.
- The decision announced in the context section, so the options are theater.

## Definition of done

Follows `TEMPLATE.md`. Every cost figure has a source and a date. The "what gets harder"
section is non-empty and specific. Status flips to Accepted only after review.
