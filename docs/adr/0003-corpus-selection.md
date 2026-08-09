# ADR-0003: Corpus selection and licensing

- **Status:** Not started — assigned to Hiruy
- **Date:** —
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)

> **Assignment brief. Delete below the line and write the ADR from `TEMPLATE.md`.**

---

## The ask

Decide which ~50 papers make up Lucid's corpus, on what inclusion criteria, and under
what licensing you may store and redistribute them.

This is the ADR that's easiest to skip and most likely to embarrass you. Every number in
your eval harness is a statement about *this specific corpus*. If the corpus is a pile of
whatever you found, "recall@5 = 0.85" means nothing, and the first person who asks
"selected how?" will get an honest shrug.

## Questions I'll ask in review

1. **What's the inclusion rule?** Written down, before you start collecting, specific
   enough that someone else applies it and gets nearly your list. Venue? Date range?
   Empirical only, or theory too? Where's the boundary of "dark patterns" — does
   persuasive design count, does attention economy, does habit-formation research?

2. **Can you legally store the PDF?** Publisher paywalls, ACM DL terms, arXiv licenses,
   and preprint versions are all different answers. This is a public repo. Decide what
   goes in git, what goes in a private S3 bucket, and what you only ever store a citation
   and a hash of. Write down the rule.

3. **Does the corpus overlap the 369 lit review, and is that allowed?** Per the operating
   contract this is the one permitted overlap — papers you read for the lit review can
   become Lucid's corpus. Confirm that reading with Hoefer and record the date you did.

4. **How do you avoid selecting a corpus that flatters your eval questions?** If you pick
   papers and then write questions from the same papers in the same sitting, your recall
   number is measuring your memory, not your system. Propose a protocol that breaks this.
   This is the interesting problem in this ADR and I will spend most of the review on it.

5. **What's the smallest corpus that still proves the thing?** ~50 is a guess someone
   wrote down in August. Defend the number or change it.

## Definition of done

Follows `TEMPLATE.md`. Inclusion criteria are written such that a stranger could apply
them. Licensing decision is explicit per storage location. The corpus/eval independence
protocol is described, not hand-waved.
