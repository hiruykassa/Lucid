# LLD: Query skeleton (S2)

- **Status:** Approved (reviewed 2026-08-21)
- **Date:** 2026-08-17
- **Author:** Hiruy Kassa
- **Reviewer:** Claude (Senior SDE)
- **Related:** ADR-0001, ADR-0002

## Problem

Lucid has no public query URL yet. Until one exists, a later failure could be a dead
deploy, silent logs, or a bad retrieval or model call, and we would not be able to tell
those apart. S5 is when the real answer path lands; if that is also the first time the
HTTP contract and the AWS pipe exist, the first outage is every layer at once.

This component is the empty query skeleton: a public URL (API Gateway in front of
Lambda) that returns hardcoded cited-answer JSON in the shape the real system will
keep. It is deployed with SAM through GitHub Actions, with CloudWatch logs. Retrieval,
embeddings, and Bedrock are out of scope. The fake body is only so the pipe has a
stable response to return while we learn whether the service is even up.

## Requirements

**Functional.**

1. Hitting the public URL returns hardcoded cited-answer JSON.
2. A GitHub push runs the SAM recipe (GitHub Actions) so we do not have to deploy by hand.
3. After a call, we can find a log line from that call in CloudWatch.
4. There is one alarm that means the query URL is failing (not the S1 billing alarm).
5. There is one runbook for what to do when that alarm fires.

**Non-functional.**

- Latency: TARGET (unmeasured). I will fill this after the first deploy.
- Cost: TARGET (unmeasured). No Bedrock on this path.

**Explicit non-requirements.**

- Retrieval, embeddings, and Bedrock
- No real citations from papers (fixtures only)
- No eval, no UI, no login



## Interface

```
POST /query

Request:
{
  "question": "What is the effect of AI in the human brain?"
}

Request body is ignored in S2. Empty body is still 200 + the same JSON.

Success(HTTP 200):
{
  "refused": false,
  "answer": "Hardcoded fixture. Not from the corpus.",
  "citations": [
     { "paper_id": "fixture-1", "page": "page 3" }
   ]
}

Refusal (HTTP 200):
{
  "refused": true,
  "answer": "{query} not supported.",
  "citations": []
}


Errors:
- 5xx: our side failed (Lambda/API Gateway). Caller gets no reliable body.
```

**Citations:** 

- **paper_id -** the paper where the information came from
- **page -** tha page of the paper where we used to answer the query.

**HTTP:**

- **Refusal -** chose 200 because the query will pass even when no answer is found for it.

## Design

**1. Flow**

Caller → API Gateway (`POST /query`) → Lambda → returns the Success JSON from Interface → CloudWatch gets a log line.

No retrieval box. No Bedrock box.

**2. Decisions**

- **Handler:** Python function that returns the Interface Success JSON as a constant (does not read `question` in S2). Why: hardcoded gate.
- **Timeout:** 10 seconds. Why: fake JSON should return immediately; if we wait that long, treat it as hung.
- **What SAM creates:** Lambda + the HTTP API in front of it + logs. Why: that is the public URL.



## Failure modes


| What breaks                                                 | How you find out                          | What you do about it                                            |
| ----------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| Lambda / API returns 5xx (handler crash or Gateway failure) | query URL alarm                           | CloudWatch log line, then last GitHub deploy                    |
| GitHub Actions deploy fails (live URL is old or missing)    | red X on the workflow, not the 5xx alarm. | open the Actions log                                            |
| No log line after a call that you think succeeded           | you look; that is a gap to notice         | confirm you hit the live URL, confirm SAM created the log group |




## Testing

**Unit.** Laptop only, no AWS. Call the handler (or the function that builds the Success dict) and assert the JSON matches Interface: `answer`, `citations` with `paper_id` and `page`. Assert two different `question` values (or empty body) still produce the same bytes.

**Integration.** After deploy: `curl POST /query` on the public URL, expect HTTP 200 and that same JSON. This is the test that the door is wired, not only the Python. Not runnable until SAM has created the URL.

**Skip.** No Bedrock, retrieval, or “is the chunk found in the page.” No TLS tests. Unit tests must not need an AWS account.

**The one regression test:** unit test that handler JSON equals the Interface Success example (keys and fixture values). If someone deletes `citations`, this fails.

## What I considered and rejected

- **GET /query instead of POST.** GET would work for a body we ignore, but S5 needs a question in the body. Freezing POST now means callers do not change method later.
- **Click the console instead of SAM.** Faster once, then the live pipe is not in git and S5 cannot reproduce it. Rejected; recipe is the source of truth.
- **Return plain text or HTML.** The product contract is cited-answer JSON. A string 200 would not catch shape drift before S5.



## Open questions

- What lives in `samconfig.toml` vs. what CI passes as parameter overrides, and where
the deployment role ARN comes from. Raised 2026-08-17 after a gitignore near-miss.
- Exact CloudWatch metric and threshold for the query-URL alarm (5xx count vs Lambda errors). Failure modes names the alarm; the number waits until the first deploy.
- Chunker has to remember tha page it got its information from.

