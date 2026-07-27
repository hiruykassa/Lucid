"""
Chunking: split a paper's raw text into overlapping windows small enough to
embed and retrieve individually.

Why chunk at all?
------------------
A whole paper is too big and too topically mixed to embed as one vector — the
embedding would be a blurry average of everything in the paper, and retrieval
would have no way to point at *which passage* actually answers a question. So
we split each paper into smaller passages first, embed each passage
separately, and let retrieval find the specific passage(s) relevant to a
question. The citation Lucid returns is a pointer to one of these chunks.

The two knobs you have to decide on, and why they matter:

- chunk_size: how big each passage is. Too small and a chunk loses the
  surrounding context needed to make sense on its own (e.g. a sentence that
  says "this effect was strongest here" with no antecedent). Too large and
  you're back to the blurry-average problem, and you also retrieve more
  irrelevant text alongside the relevant sentence, which can dilute or
  confuse the generation step.
- overlap: how much consecutive chunks share. Without overlap, a fact that
  happens to fall right at a chunk boundary gets split across two chunks and
  may not be fully retrievable in either one. Overlap costs you index size
  (each token gets embedded roughly `chunk_size / (chunk_size - overlap)`
  times) in exchange for fewer boundary losses.

There's no universally correct answer — it depends on how your papers are
written and what your eval harness (Phase 3) says about recall@k for
different settings. Start with a reasonable guess, and let the eval numbers
tell you if you guessed wrong.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    """One chunk of a source document, plus enough metadata to cite it."""

    text: str
    source_doc: str  # e.g. filename or paper ID
    chunk_index: int  # position of this chunk within the document


def chunk_text(
    text: str,
    source_doc: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[Chunk]:
    """
    Split `text` into a list of overlapping Chunk objects.

    Contract:
    - Every character of `text` should end up in at least one chunk (no
      silently dropped content).
    - Consecutive chunks should overlap by roughly `overlap` units.
    - `chunk_index` should be assigned in document order starting at 0, so a
      citation can later say "paper X, passage 3".

    Questions to work out before you write the loop:
    - Are chunk_size/overlap measured in characters, words, or tokens? Tokens
      most closely match what you're paying for and what the embedding model
      actually sees, but words/characters are simpler to start with.
    - Do you split at arbitrary character boundaries, or try to break on
      sentence/paragraph boundaries so a chunk doesn't start or end
      mid-sentence?
    - What happens on the last chunk, when there isn't a full chunk_size of
      text left?

    TODO(Hiruy): implement this. Delete the NotImplementedError below.
    """
    raise NotImplementedError("chunk_text: implement the sliding-window split")


def chunk_document(path: str, chunk_size: int = 500, overlap: int = 50) -> list[Chunk]:
    """
    Read the file at `path` and return its chunks, tagging each with the
    document's filename as `source_doc`.

    This one's mostly plumbing (open file, call chunk_text) — but write it
    yourself once chunk_text works, so you're not copy-pasting code you
    haven't run.
    """
    raise NotImplementedError("chunk_document: read the file, call chunk_text")
