# After-Sales Regulations Assistant

A Python-based chatbot designed to answer user questions about the Persian regulatory document:

**"Executive Regulations for After-Sales Services of Furniture, Household Appliances, Final Electrical and Electronic Goods, Audio and Video Equipment, and Communication Devices."**

## Features

- Multi-turn conversation support
- Integration with Claude models through the AvalAI API
- Custom system prompt tailored to the regulatory document
- Conversation history management
- Configurable model parameters and API request settings
- Secure API key management using environment variables (`.env`)
- API request error handling

## Project Structure

```text
Chatbot/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── prompts.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.13
- An AvalAI API key

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Chatbot
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your API key:

```env
ANTHROPIC_API_KEY_AVL=your_api_key
```

## Usage

Run the application from the project root:

```bash
python -m src.main
```

After launching the chatbot, enter your questions in the terminal. To end the conversation, type `exit` or `خروج`.

## Technologies

- Python
- Anthropic Python SDK
- AvalAI API
- python-dotenv

## Development Status

The current version supports interaction with the Claude language model and multi-turn conversation management.

Future development will focus on document processing, information retrieval, and implementing a **Retrieval-Augmented Generation (RAG)** architecture to ground responses in the content of the regulatory document.