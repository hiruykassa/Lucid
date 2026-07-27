# infra/

AWS SAM template (IaC) and deploy config for Lucid.

Will define: API Gateway, Lambda functions (query + ingest), the vector store
resource (TBD — leaning FAISS-in-Lambda for MVP simplicity, see root README),
S3 bucket for raw papers, IAM roles, and CloudWatch alarms.

Nothing here yet — this is Phase 5 (Deploy) in the build plan. Phase 0 is just
staking out the folder.
