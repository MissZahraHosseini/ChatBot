
import re


def chunk_by_sentence(text, max_sentences_per_chunk=5, overlap_sentences=1):
    """
    Split text into sentence-based chunks with configurable overlap.
    """

    sentences = re.split(r'(?<=[.!?؟؛])\s+', text.strip())

    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    start_idx = 0

    while start_idx < len(sentences):

        end_idx = min(
            start_idx + max_sentences_per_chunk,
            len(sentences)
        )

        current_chunk = sentences[start_idx:end_idx]
        chunks.append(" ".join(current_chunk))

        start_idx += max_sentences_per_chunk - overlap_sentences

    return chunks

def load_document(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return text