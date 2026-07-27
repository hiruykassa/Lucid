"""
Embedding: turn each text chunk into a vector using a Bedrock embedding
model.

What an embedding actually is
------------------------------
An embedding model maps text to a point in a high-dimensional vector space
(e.g. 1024 numbers) such that texts with similar *meaning* end up as nearby
points. "Nearby" is usually measured with cosine similarity — the cosine of
the angle between two vectors, which is 1 for identical direction and 0 for
unrelated. Retrieval later works by embedding the user's question with this
same model, then finding which chunk-vectors are closest to the
question-vector. That's the entire mechanism behind "search by meaning
instead of exact keyword match."

This is why the embedding model matters more than it might seem: everything
downstream (which chunks get retrieved, and therefore what the LLM is even
allowed to answer from) depends on this vector space being a decent semantic
map of your corpus.

Suggested model to start with: Amazon Titan Text Embeddings V2
(`amazon.titan-embed-text-v2:0`) via the Bedrock Runtime `invoke_model` API.
It's cheap, has no separate provisioning step, and outputs a fixed-size
float vector per call. Confirm it's enabled in your Bedrock console/model
access page before running this — Bedrock models must be explicitly enabled
per AWS account/region.

The boto3 client setup below is boilerplate — provided as-is. What Bedrock
actually needs in the request body, and how to pull the vector back out of
the response, is the part you should work out from the Bedrock Runtime docs
and fill in yourself.
"""

import json

import boto3

_BEDROCK_RUNTIME = boto3.client("bedrock-runtime")  # region comes from your AWS config/env

EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_text(text: str) -> list[float]:
    """
    Call Bedrock's embedding model on a single piece of text and return the
    embedding vector.

    Things to look up in the Bedrock Runtime docs for Titan Embeddings:
    - What JSON shape does the request body need (the `body` kwarg to
      `invoke_model` is a JSON string, not a dict)?
    - What does the response body contain, and how do you get from the raw
      `StreamingBody` response back to a Python list of floats?

    TODO(Hiruy): implement the invoke_model call and response parsing.
    """
    raise NotImplementedError("embed_text: call bedrock-runtime invoke_model")


def embed_chunks(chunks: list) -> list[list[float]]:
    """
    Embed a list of Chunk objects (see chunk.py) and return one vector per
    chunk, same order in, same order out.

    Note: this calls embed_text once per chunk in the starter version, which
    is simple but slow and makes a lot of API calls for ~50 papers. Once the
    basic pipeline works end to end, it's worth checking whether Titan
    supports batching multiple texts in one request, and whether that's
    worth the added complexity at this corpus size.

    TODO(Hiruy): implement.
    """
    raise NotImplementedError("embed_chunks: loop chunks through embed_text")
