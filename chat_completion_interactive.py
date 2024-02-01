# Imports
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import sys
import time

# Load environment variables
load_dotenv()

# Update with your API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Global Variables
current_chat = None
chats_history = {}
stream_responses = False

# Functions

def show_help():
    print("Available commands:")
    print("create_chat - Create a new chat session")
    print("close_chat - Close the current chat session")
    print("list_chat - List all stored chats")
    print("select_chat - Select a chat session to load")
    print("send_message - Send a message in the current chat session")
    print("exit - Exit the script")

def save_chats_to_file():
    with open("chats_history.json", "w") as file:
        json.dump(chats_history, file, indent=4)

def load_chats_from_file():
    global chats_history
    if os.path.exists("chats_history.json"):
        with open("chats_history.json", "r") as file:
            chats_history = json.load(file)

def create_chat():
    global current_chat, stream_responses
    system_message = input("Enter the system message: ")
    stream_choice = input("Stream responses? (yes/no): ").lower()
    stream_responses = stream_choice == 'yes'
    current_chat = {'system': system_message, 'messages': [{'role': 'system', 'content': system_message}]}
    # Note: We don't save the chat here yet as it has no user interaction.


def update_chat(message):
    global current_chat
    if current_chat:
        current_chat['messages'].append(message)
        save_chats_to_file()

def close_chat():
    global current_chat, chats_history
    if current_chat:
        if 'id' in current_chat:
            chat_id = current_chat['id']
        else:
            chat_id = str(len(chats_history) + 1)
            current_chat['id'] = chat_id
        chats_history[chat_id] = current_chat
        save_chats_to_file()
        current_chat = None
        print(f"Chat saved with ID: {chat_id}")
    else:
        print("No active chat to close.")


def list_chat():
    if chats_history:
        print("List of stored chat:")
        for chat_id in chats_history:
            print(f"ID: {chat_id}, System Message: {chats_history[chat_id]['system']}")
    else:
        print("No chat stored.")

def select_chat():
    global current_chat, stream_responses
    list_chat()
    chat_number = input("Enter the number of the chat to select: ")
    try:
        chat_number = int(chat_number)
        chat_id = str(chat_number)
        if chat_id in chats_history:
            current_chat = chats_history[chat_id]
            print(f"Loaded chat ID: {chat_id}")

            # Ask for stream responses
            stream_choice = input("Stream responses for this chat? (yes/no): ").lower()
            stream_responses = stream_choice == 'yes'
        else:
            print("Chat number not found.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")



def send_message(content):
    global current_chat, stream_responses
    if current_chat:
        update_chat({'role': 'user', 'content': content})

        # Assign a chat ID and save the chat after the first user message
        if 'id' not in current_chat:
            chat_id = str(len(chats_history) + 1)
            current_chat['id'] = chat_id
            chats_history[chat_id] = current_chat
            save_chats_to_file()

        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106"
        if stream_responses:
            assistant_message = ""
            stream = client.chat.completions.create(
                model=model,
                messages=current_chat['messages'],
                stream=True,
                temperature=0.7,
                n=1
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    assistant_message_part = chunk.choices[0].delta.content
                    print(assistant_message_part, end="")
                    assistant_message += assistant_message_part
            # Once streaming is done, update chat with the complete assistant message
            if assistant_message:
                update_chat({'role': 'assistant', 'content': assistant_message})
        else:
            completion = client.chat.completions.create(
                model=model,
                messages=current_chat['messages'],
                temperature=0.7,
                n=1
            )
            # Correctly access the response content
            response = completion.choices[0].message.content
            print(response)
            update_chat({'role': 'assistant', 'content': response})
    else:
        print("No active chat. Please create or select a chat first.")


def exit_script():
    sys.exit()

# Load previous chats
load_chats_from_file()

# Main Loop
while True:
    user_input = input("\nEnter your command: ")
    
    if user_input.lower() == "exit":
        exit_script()
    elif user_input.lower() == "create_chat":
        create_chat()
    elif user_input.lower() == "close_chat":
        close_chat()
    elif user_input.lower() == "list_chat":
        list_chat()
    elif user_input.lower() == "select_chat":
        select_chat()
    elif user_input.lower() == "send_message":
        user_message = input("Enter your message: ")
        send_message(user_message)
    elif user_input.lower() == "help":
        show_help()
    else:
        if current_chat:
            send_message(user_input)
        else:
            print("No active chat selected. Please select a chat first.")