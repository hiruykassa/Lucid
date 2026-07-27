# ingest/

Loads the ~50 curated papers, chunks them, embeds each chunk with Bedrock, and
writes vectors + metadata to the vector store. Raw PDFs live in S3; this is
the pipeline that turns them into something searchable.

Phase 1 of the build plan. Core chunking/embedding logic is intentionally
left for guided implementation, not generated wholesale — see CLAUDE.md.
