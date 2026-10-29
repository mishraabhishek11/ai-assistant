# AI Assistant

A command-line chat assistant built on the OpenAI-compatible chat completions API. At start-up you pick a persona (teacher, Python expert, travel guide, coach or interviewer), and the assistant keeps the conversation history so follow-up questions stay in context.

## Features

- Five selectable personas, each with its own system prompt
- Shared style rules applied to every persona (simple words, real-world examples, polite tone, no buzzwords or emojis)
- Multi-turn conversation: the full message history is sent on every request
- Works with any OpenAI-compatible provider via `BASE_URL`, `API_KEY` and `MODEL`
- Type `quit` to end the session
- Simple tool planner (`planner.py`): before each reply, an LLM call picks one of the tools in `tools.py` (current time, dice roll, password) or `none`, and the chosen tool's result is passed to the model to phrase the answer
- Utility module (`tools.py`) with helpers for time, dice, password generation and file reading (`read_text_file` is not yet exposed to the planner)

## Tech Stack

- Python 3
- `openai` SDK
- `python-dotenv`

## Project Structure

```
ai-assistant/
├── assistant.py        # Entry point: persona menu, tool dispatch and chat loop
├── planner.py          # choose_tool(): LLM-based tool selection
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

You : Roll a dice
AI  : You rolled a 4.

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

## Tool Planner

Each turn works in two steps:

1. `choose_tool(user_input)` in `planner.py` sends the request to the model with a planner prompt and gets back a single tool name (`get_current_time`, `roll_dice`, `generate_password`) or `none`.
2. `assistant.py` runs the matching function from `tools.py` and sends the user's question plus the tool result to the model, which answers in the chosen persona. With `none`, the model answers on its own.

This is prompt-based routing, not OpenAI function calling. It costs one extra API call per message, and tools run with default arguments (for example, a password is always 12 characters).

To add a tool, write the function in `tools.py`, describe it in the planner prompt in `planner.py`, and add a branch for it in `assistant.py`.

## Utility Functions

Defined in `tools.py`:

| Function | Description |
|---|---|
| `get_current_time()` | Current date and time as `DD-MM-YYYY hh:mm:ss AM/PM` |
| `roll_dice()` | Random integer from 1 to 6 |
| `generate_password(length=12)` | Random password using `secrets` |
| `read_text_file(filename)` | Contents of a text file, or an error string |

## Known Issues

- Tool selection relies on the model returning an exact tool name; extra text or a different casing is treated as no tool and falls through to a plain answer.
- The planner cannot pass arguments (such as a password length), and `read_text_file` is not wired in.
- The user message stored in the history is the wrapped prompt containing the tool result, not the raw input, and the wrapper text is repeated every turn.
- Each message makes two API calls (planner, then answer).
- API errors (bad key, network failure, wrong model name) are not caught and will end the program with a traceback.
- The conversation history grows without limit, so very long sessions may exceed the model's context window.
- `read_text_file` opens files without an explicit encoding and its generic `except Exception` returns the error as normal text.
- There is no `requirements.txt` and no tests yet.

## Future Enhancements

- Replace the prompt-based planner with native function calling (with arguments and `read_text_file`)
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
