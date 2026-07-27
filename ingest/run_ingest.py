"""
CLI entry point that wires the ingest pipeline together:

    docs on disk -> chunk_document (chunk.py)
                 -> embed_chunks   (embed.py)
                 -> build_index    (index.py)
                 -> save_index + a metadata sidecar file

This file is plumbing, not core logic — it's provided complete. It won't
actually run end to end until chunk.py, embed.py, and index.py have their
TODOs filled in (they currently raise NotImplementedError on purpose).

Usage:
    python -m ingest.run_ingest --docs-dir ingest/sample_docs --out-dir ingest/output
"""

import argparse
import json
import os

from ingest.chunk import chunk_document
from ingest.embed import embed_chunks
from ingest.index import build_index, save_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk, embed, and index a directory of text docs.")
    parser.add_argument("--docs-dir", default="ingest/sample_docs", help="Directory of .txt docs to ingest")
    parser.add_argument("--out-dir", default="ingest/output", help="Where to write the index + metadata")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=50)
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    doc_paths = [
        os.path.join(args.docs_dir, name)
        for name in sorted(os.listdir(args.docs_dir))
        if name.endswith(".txt")
    ]
    if not doc_paths:
        raise SystemExit(f"No .txt files found in {args.docs_dir}")

    print(f"Chunking {len(doc_paths)} document(s) from {args.docs_dir} ...")
    all_chunks = []
    for path in doc_paths:
        all_chunks.extend(chunk_document(path, chunk_size=args.chunk_size, overlap=args.overlap))
    print(f"  -> {len(all_chunks)} chunks")

    print("Embedding chunks via Bedrock ...")
    vectors = embed_chunks(all_chunks)

    print("Building FAISS index ...")
    index = build_index(vectors)

    index_path = os.path.join(args.out_dir, "index.faiss")
    metadata_path = os.path.join(args.out_dir, "metadata.json")

    save_index(index, index_path)

    # Sidecar file: FAISS only stores vectors, so this maps each vector's
    # position in the index back to the chunk it came from. api/ will load
    # this at query time to turn "nearest vector index 7" into an actual
    # citation (source_doc, chunk_index, text).
    metadata = [
        {"source_doc": c.source_doc, "chunk_index": c.chunk_index, "text": c.text}
        for c in all_chunks
    ]
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Wrote index to {index_path}")
    print(f"Wrote metadata to {metadata_path}")


if __name__ == "__main__":
    main()
