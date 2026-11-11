
from src.retriever import build_retriever


def main():

    print("Building Hybrid Retriever...")

    retriever = build_retriever()

    print("\nRetriever successfully initialized.")

    query = "شرایط تعویض کالای دارای عیب ذاتی چیست؟"

    print(f"\nUser Question: {query}")

    results = retriever.search(
        query,
        k=4
    )

    print("\nRetrieved Documents:\n")

    for index, (document, score) in enumerate(results, start=1):

        print(f"Document {index}")
        print(f"Score: {score}")
        print(document["content"])
        print("-" * 60)


if __name__ == "__main__":
    main()
