
from anthropic import Anthropic
from anthropic.types import Message

from src.config import (
    API_KEY,
    BASE_URL,
    MODEL,
    MAX_TOKENS,
    TEMPERATURE
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
        message (str or Message): User message to append.
    """
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }

    messages.append(user_message)


def add_assistant_message(messages, message):
    """
    Add an assistant response to the conversation history.

    Args:
        messages (list): Conversation history.
        message (str or Message): Assistant response to append.
    """
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }

    messages.append(assistant_message)


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

    while True:
        user_input = input("کاربر: ")

        if user_input.strip().lower() in ["exit", "خروج"]:
            print("دستیار: مکالمه پایان یافت.")
            break

        add_user_message(messages, user_input)

        try:
            response = chat(
                messages=messages,
                system=SYSTEM_PROMPT
            )

            assistant_response = text_from_message(response)

            print(f"\nدستیار: {assistant_response}\n")

            add_assistant_message(messages, assistant_response)

        except Exception as error:
            messages.pop()
            print(f"خطا در پردازش درخواست: {error}")


if __name__ == "__main__":
    main()
