from typing import Any, List, Dict, Tuple, Protocol
from pathlib import Path

from src.indexes import VectorIndex, BM25Index
from src.embeddings import generate_embedding
from src.document import load_document, chunk_by_sentence

class SearchIndex(Protocol):
    """
    Define the interface for search index implementations.
    """

    def add_document(self, document: Dict[str, Any]) -> None:
        """
        Add a single document to the search index.
        """

    # Added the 'add_documents' method to avoid rate limiting errors from VoyageAI
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add multiple documents to the search index.
        """

    def search(
        self, query: Any, k: int = 1
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search the index and return the top-k documents with their scores.
        """


class Retriever:
    """
    Combine multiple search indexes and retrieve documents using RRF.
    """

    def __init__(self, *indexes: SearchIndex):
        """
        Initialize the retriever with one or more search indexes.

        Raises:
            ValueError: If no search index is provided.
        """
        if len(indexes) == 0:
            raise ValueError("At least one index must be provided")
        self._indexes = list(indexes)

    def add_document(self, document: Dict[str, Any]):
        """
        Add a single document to all registered search indexes.
        """
        for index in self._indexes:
            index.add_document(document)

    # Added the 'add_documents' method to avoid rate limiting errors from VoyageAI
    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Add multiple documents to all registered search indexes.
        """
        for index in self._indexes:
            index.add_documents(documents)

    def search(
        self, query_text: str, k: int = 1, k_rrf: int = 60
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Retrieve and rank documents by combining results from all indexes
        using Reciprocal Rank Fusion (RRF).

        Args:
            query_text: The text query used for searching.
            k: Maximum number of documents to return.
            k_rrf: Constant used in the RRF scoring formula.

        Returns:
            A list of document-score pairs, sorted by descending RRF score.

        Raises:
            TypeError: If query_text is not a string.
            ValueError: If k is not positive or k_rrf is negative.
        """
        if not isinstance(query_text, str):
            raise TypeError("Query text must be a string.")
        if k <= 0:
            raise ValueError("k must be a positive integer.")
        if k_rrf < 0:
            raise ValueError("k_rrf must be non-negative.")

        all_results = [
            index.search(query_text, k=k * 5) for index in self._indexes
        ]

        doc_ranks = {}
        for idx, results in enumerate(all_results):
            for rank, (doc, _) in enumerate(results):
                doc_id = id(doc)
                if doc_id not in doc_ranks:
                    doc_ranks[doc_id] = {
                        "doc_obj": doc,
                        "ranks": [float("inf")] * len(self._indexes),
                    }
                doc_ranks[doc_id]["ranks"][idx] = rank + 1

        def calc_rrf_score(ranks: List[float]) -> float:
            """
            Calculate the Reciprocal Rank Fusion score for a document.
            """
            return sum(1.0 / (k_rrf + r) for r in ranks if r != float("inf"))

        scored_docs: List[Tuple[Dict[str, Any], float]] = [
            (ranks["doc_obj"], calc_rrf_score(ranks["ranks"]))
            for ranks in doc_ranks.values()
        ]

        filtered_docs = [
            (doc, score) for doc, score in scored_docs if score > 0
        ]
        filtered_docs.sort(key=lambda x: x[1], reverse=True)

        return filtered_docs[:k]

from pathlib import Path


def build_retriever():

    project_root = Path(__file__).resolve().parent.parent
    document_path = project_root / "data" / "content.md"

    # Load document
    document_text = load_document(document_path)

    # Create chunks
    chunks = chunk_by_sentence(
        document_text,
        max_sentences_per_chunk=5,
        overlap_sentences=1
    )

    # Prepare documents
    documents = [
        {"content": chunk}
        for chunk in chunks
    ]

    # Create indexes
    vector_index = VectorIndex(
        embedding_fn=generate_embedding
    )

    bm25_index = BM25Index()

    # Create retriever
    retriever = Retriever(
        bm25_index,
        vector_index
    )

    # Add documents to indexes
    retriever.add_documents(documents)

    print(f"Total indexed chunks: {len(documents)}")

    return retriever