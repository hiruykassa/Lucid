# api/

The query-time Lambda handler: embed the question -> retrieve top-k chunks ->
call the Bedrock LLM with a grounding prompt -> return a JSON answer with
inline citations, or a refusal if the corpus doesn't support an answer.

Phase 2 of the build plan. Retrieval and the Bedrock call are core logic —
left for guided implementation, not generated wholesale.
