# Runbook: <symptom, as the alarm states it>

> A runbook is written for you at 2am, tired, months from now, having forgotten
> everything. Write it in the imperative. No theory, no background, no "as you know."
> If a step requires thinking, the runbook has failed at that step.

## Symptom

What you actually observe. The alarm name, the error string, the graph shape.

## Severity

What is broken for whom, and what's the blast radius. Does this take down answers, or
only degrade them? Can users still get a refusal instead of a wrong answer? A system
that fails toward "I don't know" is less urgent than one that fails toward confident
nonsense — say which this is.

## Check first

Ordered. Cheapest and most likely first. Each step: the exact command, and what a
healthy result looks like next to what an unhealthy one looks like.

1. `<command>` — healthy: … / unhealthy: …
2.
3.

## Most likely causes

Ranked by how often it has actually been this. Update the ranking when reality disagrees
with you.

## Fix

The remediation, step by step, with the exact commands. Note anything destructive or
irreversible in bold **before** the step, not after.

## If that didn't work

The escalation path, or the next diagnostic branch. Say plainly when the answer is
"stop, gather state, and come back in the morning" — that's a legitimate step.

## After the fact

Did this need a COE? Anything that surprised you or took more than one attempt to
diagnose does. Link it: `docs/coe/`.
