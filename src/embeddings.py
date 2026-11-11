from openai import OpenAI
from src.config import API_KEY, EMBEDDING_BASE_URL

client = OpenAI(
    api_key=API_KEY,
    base_url=EMBEDDING_BASE_URL
)

def generate_embedding(chunks, model="text-embedding-3-small"):
    """
    Generate embedding vectors for a single text or a list of text chunks.
    """

    is_list = isinstance(chunks, list)
    inputs = chunks if is_list else [chunks]

    embeddings = []

    for chunk in inputs:

        response = client.embeddings.create(
            model=model,
            input=chunk,
        )

        embeddings.append(response.data[0].embedding)

    return embeddings if is_list else embeddings[0]