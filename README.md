## OpenAI Assistant, Chat, Image Management CLI

## OpenAI Assistant Management CLI

This very ugly Python script provides a command-line interface (CLI) for managing OpenAI Assistants and conversation threads. It allows users to create, list, select, and delete Assistants, as well as create, select, and delete conversation threads. Additionally, users can send messages to the Assistant and view the conversation history.

### Getting Started

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

### Commands

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

### Usage

1. Run the script and follow the prompts to create or select an Assistant.
2. Choose a thread or create a new one.
3. Send messages to the Assistant and view its responses.
4. Manage Assistants, threads, and messages using the provided commands.

### Note

- The script stores information about Assistants and threads locally in a `threads_dict.json` file.


## OpenAI Chat Management CLI

This ugly Python script offers a command-line interface (CLI) for managing OpenAI chat sessions and their histories. It enables users to create, close, list, and select chat sessions. Users can also send messages within a chat session and have the option to stream responses from the OpenAI Assistant.

### Getting Started

1. **Install Dependencies:**
   Ensure the necessary Python packages are installed by executing:
   ```bash
   pip install openai python-dotenv
   ```

2. **Set Up Environment:**
   Generate a `.env` file in your project directory and include your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Run the Script:**
   Launch the script via a terminal:
   ```bash
   python chat_completion_interactive.py
   ```

### Commands

- `create_chat`: Initiates a new chat session by requesting a system message.
- `close_chat`: Terminates the current chat session and saves its history.
- `list_chat`: Displays all stored chat sessions.
- `select_chat`: Loads a previously stored chat session for interaction.
- `send_message`: Sends a message in the current chat session and receives a response.
- `exit`: Exits the application.

### Features

- **Chat Session Management:** Create and manage multiple chat sessions.
- **Persistent Chat Histories:** Save and load chat histories to and from a file.
- **Stream Responses:** Optionally stream responses from the OpenAI Assistant for a more interactive experience.
- **Easy Interaction:** Use simple commands to interact with the OpenAI Assistant and manage chat sessions.

### Usage

1. Start the script and use the `create_chat` command to initiate a new chat session.
2. Send messages to the Assistant within the chat session using the `send_message` command.
3. Optionally, enable streaming of responses for real-time interaction.
4. Manage chat sessions by closing the current session, listing all sessions, or selecting an existing session for further interaction.

### Note

- Chat session information, including messages and system prompts, is stored locally in a `chats_history.json` file for persistence and retrieval.



## OpenAI Image Generation CLI

This ugly Python script provides a command-line interface (CLI) for generating images using OpenAI's Image API. It allows for customization of image generation parameters such as model, size, quality, style, and response format.


### Getting Started

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
   python image_generation_interactive.py
   ```

### Features

- **Custom Image Generation**: Generate images based on textual prompts with options to customize the model, image size, quality, style, and response format.
- **Interactive Parameter Selection**: Choose your preferred settings through an interactive menu for each image generation request.
- **Escape Option**: At any parameter selection step, you have the option to go back to the main command prompt, enhancing the script's usability.

### Commands

- `generate`: Initiates the process to generate a new image. You will be prompted to enter a text prompt and select your preferences for each parameter.
- `exit`: Exits the application.

### Usage

1. **Start the Script**: Run the script from your terminal.
2. **Generate Image**: Type `generate` and follow the prompts to specify your image preferences. You can choose to go back or exit at any point.
3. **View Results**: After generating an image, the script displays the URL of the generated image. If the response format is not `url`, it will print the response directly in the terminal.
4. **Help**: Type `help` to display the list of available commands.

### Customization Options

- **Model**: Choose between available models like `dall-e-2` and `dall-e-3`.
- **Image Size**: Select from sizes such as `256x256`, `512x512`, `1024x1024`, `1024x1792`, `1792x1024`.
- **Quality**: Options include `hd`, `medium`, `standard`.
- **Style**: Choose the style of your image, like `natural`, `vivid`.
- **Response Format**: Select how you'd like to receive your image, either as a `url` or `b64_json`.

## Acknowledgments

Thanks GPT for assistance in generating code and documentation for this project.
