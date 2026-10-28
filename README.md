# AI Assistant

A command-line chat assistant built on the OpenAI-compatible chat completions API. At start-up you pick a persona (teacher, Python expert, travel guide, coach or interviewer), and the assistant keeps the conversation history so follow-up questions stay in context.

## Features

- Five selectable personas, each with its own system prompt
- Shared style rules applied to every persona (simple words, real-world examples, polite tone, no buzzwords or emojis)
- Multi-turn conversation: the full message history is sent on every request
- Works with any OpenAI-compatible provider via `BASE_URL`, `API_KEY` and `MODEL`
- Type `quit` to end the session
- Small utility module (`tools.py`) with helpers for time, dice, password generation and file reading (not yet connected to the chat loop, see [Known Issues](#known-issues))

## Tech Stack

- Python 3
- `openai` SDK
- `python-dotenv`

## Project Structure

```
ai-assistant/
├── assistant.py        # Entry point: persona menu and chat loop
├── assistant_role.py   # Persona prompts and get_role_prompt()
├── tools.py            # Helper functions (time, dice, password, read file)
├── .env                # Local configuration (not committed)
└── README.md
```

## Installation

1. Clone the repository and create a virtual environment:

   ```bash
   git clone https://github.com/mishraabhishek11/ai-assistant.git
   cd ai-assistant
   python -m venv .venv
   ```

   Activate it:

   ```bash
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project root:

   ```env
   BASE_URL=https://your-provider.example.com/v1
   API_KEY=your-api-key
   MODEL=your-model-name
   ```

4. Run the assistant:

   ```bash
   python assistant.py
   ```

## Usage

```
========================================
      My AI Assistant
========================================
Choose Your Assistant

1. Friendly School Teacher
2. Senior Python Developer
3. Experienced Travel Guide
4. Motivational Coach
5. Professional Interviewer

Enter your choice : 2

You : What is a list comprehension?
AI  : ...

You : quit
AI  : Goodbye! Have a great day.
```

Any choice other than 1-5 falls back to a generic helpful assistant.

## Personas

| Choice | Persona | Behaviour |
|---|---|---|
| 1 | Friendly School Teacher | Simple language and real-life examples |
| 2 | Senior Python Developer | Clear explanations with Python examples |
| 3 | Experienced Travel Guide | Places, food, transport and travel tips |
| 4 | Motivational Coach | Practical, encouraging advice |
| 5 | Professional Interviewer | One question at a time, feedback after each answer |

To add a persona, add an entry to `roles` in `assistant_role.py` and a matching line to the menu in `assistant.py`.

## Configuration

| Variable | Description |
|---|---|
| `BASE_URL` | Base URL of the OpenAI-compatible API |
| `API_KEY` | API key for that provider |
| `MODEL` | Model name sent with each request |

Keep `.env` out of version control.

## Utility Functions

Defined in `tools.py`:

| Function | Description |
|---|---|
| `get_current_time()` | Current date and time as `DD-MM-YYYY hh:mm:ss AM/PM` |
| `roll_dice()` | Random integer from 1 to 6 |
| `generate_password(length=12)` | Random password using `secrets` |
| `read_text_file(filename)` | Contents of a text file, or an error string |

## Known Issues

- The functions in `tools.py` are imported by `assistant.py` but never called, and they are not registered as model tools (function calling), so the assistant cannot use them yet.
- API errors (bad key, network failure, wrong model name) are not caught and will end the program with a traceback.
- The conversation history grows without limit, so very long sessions may exceed the model's context window.
- `read_text_file` opens files without an explicit encoding and its generic `except Exception` returns the error as normal text.
- There is no `requirements.txt` and no tests yet.

## Future Enhancements

- Wire `tools.py` into the chat loop using function calling
- Handle API errors and retry with a clear message
- Trim or summarise old messages to stay within the context window
- Streaming responses
- Add `requirements.txt` and unit tests
- Save and reload conversations

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-feature`
3. Commit your changes following Conventional Commits
4. Push and open a pull request

## Author

Abhishek Mishra
