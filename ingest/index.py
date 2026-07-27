"""
Vector index: store chunk embeddings so that, given a query vector, you can
quickly find the k nearest chunk vectors (recall@k territory — this is what
Phase 3's eval harness will measure the quality of).

Why not just loop over every vector and compute cosine similarity?
--------------------------------------------------------------------
For ~50 papers you could actually get away with brute-force search — a few
thousand vectors is nothing to compare against with numpy. But building this
on FAISS now means the same code scales if the corpus grows, and it's the
standard tool for this, so it's worth learning properly. FAISS's
`IndexFlatL2` (or `IndexFlatIP` for cosine-style similarity via normalized
vectors) is itself a brute-force index under the hood at this scale — the
API is the point here, not raw performance.

You'll also need a side-channel mapping from FAISS's internal integer IDs
back to your Chunk metadata (source_doc, chunk_index, text), since FAISS
only stores vectors, not the text or citation info that goes with them.

TODO(Hiruy): implement build_index, save_index/load_index, and search below.
Look at the faiss-cpu docs for `IndexFlatL2` / `IndexFlatIP`, `index.add`,
`faiss.write_index` / `faiss.read_index`, and `index.search`.
"""

import faiss  # noqa: F401  (remove this noqa once you're using it)


def build_index(vectors: list[list[float]]):
    """
    Build a FAISS index from a list of embedding vectors and return it.

    Decide: L2 distance or inner product (cosine)? If you go with inner
    product, remember embeddings usually need to be L2-normalized first for
    the inner product to behave like cosine similarity.

    TODO(Hiruy): implement.
    """
    raise NotImplementedError("build_index")


def save_index(index, path: str) -> None:
    """Persist a FAISS index to disk at `path`. TODO(Hiruy): implement."""
    raise NotImplementedError("save_index")


def load_index(path: str):
    """Load a FAISS index previously saved with save_index. TODO(Hiruy): implement."""
    raise NotImplementedError("load_index")


def search(index, query_vector: list[float], k: int = 5) -> list[int]:
    """
    Return the indices of the k nearest vectors to `query_vector`.

    This is the function api/ will eventually call at query time (after
    embedding the user's question) — its return values are what "top-k
    retrieval" means throughout the rest of this project.

    TODO(Hiruy): implement.
    """
    raise NotImplementedError("search")
