
from anthropic import Anthropic

from src.retriever import build_retriever

from src.config import (
    API_KEY,
    BASE_URL,
    MODEL,
    MAX_TOKENS,
   
)

from src.prompts import SYSTEM_PROMPT


# Initialize the Anthropic client using AvalAI as the API provider.
client = Anthropic(
    api_key=API_KEY,
    base_url=BASE_URL
)


def add_user_message(messages, message):
    """
    Add a user message to the conversation history.

    Args:
        messages (list): Conversation history.
        message (str): User message to append.
    """

    messages.append({
        "role": "user",
        "content": message
    })


def add_assistant_message(messages, message):
    """
    Add an assistant response to the conversation history.

    Args:
        messages (list): Conversation history.
        message (str): Assistant response to append.
    """

    messages.append({
        "role": "assistant",
        "content": message
    })


def retrieve_context(retriever, query, k=3):
    """
    Retrieve relevant document chunks using the hybrid retriever.

    Args:
        retriever: Initialized hybrid retriever.
        query (str): User question.
        k (int): Number of relevant chunks to retrieve.

    Returns:
        str: Combined retrieved document context.
    """

    results = retriever.search(query, k=k)

    context_parts = []

    for document, score in results:

        content = document.get("content", "")

        if content:
            context_parts.append(content)

    return "\n\n".join(context_parts)


def build_user_prompt(question, context):
    """
    Combine the retrieved document context with the user question.

    Args:
        question (str): Original user question.
        context (str): Retrieved document context.

    Returns:
        str: Augmented user prompt.
    """

    if not context:
        context = "No relevant document context was retrieved."

    return f"""
Document Context:

<context>
{context}
</context>

User Question:

{question}

Answer the user's question in Persian according to the system instructions.
"""


def chat(
    messages,
    system=None,
    stop_sequences=None,
    tools=None,
    thinking=False,
    thinking_budget=2000,
):
    """
    Send a request to the Claude model and return its response.

    Args:
        messages (list): Conversation history.
        system (str, optional): System prompt.
        stop_sequences (list, optional): Sequences that stop generation.
        tools (list, optional): Tools available to the model.
        thinking (bool): Enable extended thinking.
        thinking_budget (int): Token budget for extended thinking.

    Returns:
        Message: Response returned by the Anthropic API.
    """

    params = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": messages,
    }


    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    if thinking:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    response = client.messages.create(**params)

    return response


def text_from_message(message):
    """
    Extract all text blocks from the model response.

    Args:
        message (Message): Response returned by the Anthropic API.

    Returns:
        str: Extracted text content.
    """

    return "\n".join(
        block.text
        for block in message.content
        if block.type == "text"
    )


def main():

    messages = []

    print("دستیار هوشمند اسناد حقوقی فعال شد.")
    print("برای پایان مکالمه، عبارت «خروج» را وارد کنید.\n")
    
    # Initialize the hybrid retriever using BM25 and vector search
    retriever = build_retriever()

    while True:

        user_input = input("کاربر: ").strip()

        if user_input.lower() in ["exit", "خروج"]:
            print("دستیار: مکالمه پایان یافت.")
            break

        if not user_input:
            continue

        try:

            # Retrieve relevant document chunks.
            context = retrieve_context(
                retriever=retriever,
                query=user_input,
                k=3
            )

            # Build the augmented user prompt.
            augmented_prompt = build_user_prompt(
                question=user_input,
                context=context
            )

            # Store the original user question.
            add_user_message(messages, user_input)

            # Create request history with retrieved context.
            request_messages = messages[:-1] + [
                {
                    "role": "user",
                    "content": augmented_prompt
                }
            ]

            # Send the request to Claude.
            response = chat(
                messages=request_messages,
                system=SYSTEM_PROMPT
            )

            # Extract the assistant response.
            assistant_response = text_from_message(response)

            # Display the response.
            print(f"\nدستیار: {assistant_response}\n")

            # Store the assistant response in conversation history.
            add_assistant_message(
                messages,
                assistant_response
            )

        except Exception as error:

            if messages and messages[-1]["role"] == "user":
                messages.pop()

            print(f"خطا در پردازش درخواست: {error}")


if __name__ == "__main__":
    main()
