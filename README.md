# OpenAI Assistant Management CLI

This very ugly Python script provides a command-line interface (CLI) for managing OpenAI Assistants and conversation threads. It allows users to create, list, select, and delete Assistants, as well as create, select, and delete conversation threads. Additionally, users can send messages to the Assistant and view the conversation history.

## Getting Started

1. **Install Dependencies:**
   Make sure to install the required Python packages by running:
   ```bash
   pip install openai python-dotenv
   ```

2. **Set Up Environment:**
   Create a `.env` file in the project directory with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Run the Script:**
   Execute the script in a terminal:
   ```bash
   python base_assistant_interactive.py
   ```

## Commands

- `create_assistant`: Create a new OpenAI Assistant by providing a name and system prompt.
- `list_assistants`: List all existing Assistants.
- `select_assistant`: Select an existing Assistant for further actions.
- `delete_assistant`: Delete an existing Assistant.
- `create_thread`: Start a new conversation thread for the selected Assistant.
- `select_thread`: Select an existing conversation thread.
- `delete_thread`: Delete the current conversation thread.
- `list_threads`: List all available threads for the selected Assistant.
- `list_messages`: List all messages in the current thread.
- `help`: Show available commands.
- `exit`: Exit the program.

## Usage

1. Run the script and follow the prompts to create or select an Assistant.
2. Choose a thread or create a new one.
3. Send messages to the Assistant and view its responses.
4. Manage Assistants, threads, and messages using the provided commands.

## Note

- The script stores information about Assistants and threads locally in a `threads_dict.json` file.


## Acknowledgments

Thanks GPT for assistance in generating code and documentation for this project.
