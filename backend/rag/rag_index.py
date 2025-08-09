# backend/rag/rag_index.py
import json
import math
from typing import List, Dict, Tuple
from llm.llm_api import embed_texts

# Minimum viable RAG: combine each part's data into a single text → generate embeddings → perform cosine similarity retrieval
# No numpy/scikit dependency; cosine similarity calculated purely in Python

_INDEX_BUILT = False
_DOCS: List[Dict] = []          # Each entry: {"part_id": str, "text": str}
_EMBS: List[List[float]] = []   # Corresponding embeddings

def _cosine(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity (pure Python version)"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def build_index(parts_db: Dict[str, Dict]) -> str | None:
    """Build document and embedding index from parts_db; return error message string if failed"""
    global _INDEX_BUILT, _DOCS, _EMBS
    _DOCS = []
    for pid, info in parts_db.items():
        # Concatenate useful fields into a single text (simple formatting)
        text = (
            f"Part {pid}: {info.get('name')} for {info.get('type')}.\n"
            f"Compatible models: {', '.join(info.get('compatible_models', []))}.\n"
            f"Installation: {info.get('install_instructions')}"
        )
        _DOCS.append({"part_id": pid, "text": text})

    # Generate embeddings
    texts = [d["text"] for d in _DOCS]
    embs = embed_texts(texts)
    if isinstance(embs, str):
        # Error occurred (e.g., missing API key)
        return embs
    _EMBS = embs
    _INDEX_BUILT = True
    return None

def retrieve(query: str, top_k: int = 2) -> List[Tuple[float, Dict]]:
    """Retrieve top_k documents for a given query; returns [(score, doc), ...]"""
    if not _INDEX_BUILT:
        return []
    q_embs = embed_texts([query])
    if isinstance(q_embs, str):
        return []
    q = q_embs[0]
    scored = [(_cosine(q, e), d) for e, d in zip(_EMBS, _DOCS)]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

def format_context(chunks: List[Tuple[float, Dict]]) -> str:
    """Format retrieved documents into a prompt context string"""
    lines = []
    for score, doc in chunks:
        lines.append(f"- {doc['text']}")
    return "\n".join(lines)
