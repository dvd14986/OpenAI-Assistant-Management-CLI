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

assistant = None  # Initialize assistant as None
threads_dict = {}  # Initialize a dictionary to store threads
assistants = None
assistant_threads = None

# # Open the file in "read binary" (rb) mode, with the "assistants" purpose
# file = client.files.create(
#   file=open("file.txt", "rb"),
#   purpose='assistants'
# )

def create_assistant():
    global assistant
    assistant_name = input("Enter the name for your new assistant: ")
    assistant_prompt = input("Enter the system prompt for the assistant: ")

    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=assistant_prompt,
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        tools=[{"type": "retrieval"}],
        # file_ids=[file.id]
    )
    # Create an empty list of threads for the new assistant
    threads_dict[assistant.id] = []

    # Save threads_dict to a local JSON file
    save_threads_to_file()

def list_assistants():
    global assistants
    assistants = client.beta.assistants.list()
    if assistants.data:
        print("List of existing assistants:")
        for idx, assistant in enumerate(assistants.data):
            print(f"{idx + 1}. {assistant.name}")
    else:
        print("No existing assistants found.")

def select_assistant():
    global assistants
    list_assistants()
    selection = int(input("Enter the number of the assistant you want to select: ")) - 1
    return assistants.data[selection] if 0 <= selection < len(assistants.data) else None

def delete_assistant():
    selected_assistant = select_assistant()
    if selected_assistant:
        confirm = input(f"Do you want to delete the assistant '{selected_assistant.name}'? (yes/no): ")
        if confirm.lower() == "yes":
            client.beta.assistants.delete(id=selected_assistant.id)
            print(f"Assistant '{selected_assistant.name}' has been deleted.")
            # Remove the assistant's threads from the local dictionary
            del threads_dict[selected_assistant.id]
        else:
            print("Deletion canceled.")

def save_threads_to_file():
    # Save threads_dict to a local JSON file
    with open("threads_dict.json", "w") as file:
        json.dump(threads_dict, file)

def create_thread():
    global thread, assistant, threads_dict
    if assistant:
        if assistant.id not in threads_dict:
            threads_dict[assistant.id] = []  # Initialize an empty list for the assistant's threads
        thread = client.beta.threads.create()
        # Add the thread to the local dictionary under the current assistant
        threads_dict[assistant.id].append(thread.id)

        # Save threads_dict to a local JSON file
        save_threads_to_file()
    else:
        print("Please select an assistant first.")

def select_thread():
    global thread, assistant, assistant_threads
    if assistant:
        assistant_id = assistant.id
        list_threads(assistant_id)
        selection = int(input("Enter the thread ID you want to select: "))-1
        try:
            thread_id = assistant_threads[selection]
            if thread_id in threads_dict[assistant_id]:
                thread = client.beta.threads.retrieve(thread_id)
                print(f"Selected thread ID: {thread.id}")
            else:
                print("Thread not found.")
        except:
            print("Thread not found.")
    else:
        print("Please select an assistant first.")

def delete_thread():
    global thread, assistant
    if assistant and thread:
        assistant_id = assistant.id
        thread_id = thread.id
        confirm = input(f"Do you want to delete the current thread (ID: {thread_id})? (yes/no): ")
        if confirm.lower() == "yes":
            client.beta.threads.delete(thread_id)
            print(f"Thread (ID: {thread_id}) has been deleted.")
            # Remove the thread from the local dictionary under the current assistant
            threads_dict[assistant_id].remove(thread_id)
            thread = None
            # Save threads_dict to a local JSON file
            save_threads_to_file()
        else:
            print("Deletion canceled.")
    else:
        print("No thread selected.")

def show_help():
    print("Available commands:")
    print("create_assistant - Create a new assistant.")
    print("list_assistants - List all existing assistants.")
    print("select_assistant - Select an existing assistant.")
    print("delete_assistant - Delete an existing assistant.")
    print("create_thread - Start a new conversation thread.")
    print("select_thread - Select an existing conversation thread.")
    print("delete_thread - Delete the current conversation thread.")
    print("list_threads - List all available threads for the selected assistant.")
    print("list_messages - List all messages in the current thread.")
    print("help - Show available commands.")
    print("exit - Exit the program.")

def list_threads(assistant_id):
    global assistant_threads
    if assistant_id in threads_dict:
        assistant_threads = threads_dict[assistant_id]
        if assistant_threads:
            print(f"List of available threads for the selected assistant (ID: {assistant_id}):")
            for idx, thread_id in enumerate(assistant_threads):
                print(f"{idx + 1}. Thread ID: {thread_id}")
        else:
            print("No existing threads found for the selected assistant.")
    else:
        print("No threads found for the selected assistant.")

def list_messages():
    global thread
    if thread:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages.data:
            role = message.role.capitalize()
            content = message.content[0].text.value
            print(f"{role}: {content}")
    else:
        print("No thread selected.")


import sys
import time

import sys
import time

def send_message(content):
    global thread, assistant
    if thread and assistant:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        response_message = None
        last_status_length = 0

        while run.status != "completed":
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            status_message = f"Assistant is generating... (Status: {keep_retrieving_run.status})"
            sys.stdout.write("\r" + status_message.ljust(last_status_length))
            sys.stdout.flush()

            last_status_length = len(status_message)

            if keep_retrieving_run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                if messages.data:
                    response_message = messages.data[0].content[0].text.value
                break

            # Wait for a moment before checking again
            time.sleep(0.2)

        sys.stdout.write('\n')  # Add a newline after streaming the message
        if response_message:
            print(f"Assistant: {response_message}")
        else:
            print("\nAssistant response could not be retrieved.")
    else:
        print("No thread or assistant selected. Please select an assistant and start a thread.")




# Load threads_dict from a local JSON file if it exists
if os.path.exists("threads_dict.json"):
    with open("threads_dict.json", "r") as file:
        threads_dict = json.load(file)

while True:
    user_input = input("Enter your command: ")
    
    if user_input.lower() == "exit":
        # Save threads_dict to a local JSON file before exiting
        with open("threads_dict.json", "w") as file:
            json.dump(threads_dict, file)
        break
    elif user_input.lower() == "create_assistant":
        create_assistant()
    elif user_input.lower() == "list_assistants":
        list_assistants()
    elif user_input.lower() == "select_assistant":
        assistant = select_assistant()
        if assistant:
            print(f"Selected assistant: {assistant.name}")
            # create_thread() //disabled auto creation of thread, require manual selection
    elif user_input.lower() == "delete_assistant":
        delete_assistant()
    elif user_input.lower() == "create_thread":
        create_thread()
    elif user_input.lower() == "select_thread":
        select_thread()
    elif user_input.lower() == "delete_thread":
        delete_thread()
    elif user_input.lower() == "list_threads":
        if assistant:
            list_threads(assistant.id)
        else:
            print("Please select an assistant first.")
    elif user_input.lower() == "list_messages":
        list_messages()
    elif user_input.lower() == "help":
        show_help()
    elif assistant:
        send_message(user_input)
    else:
        print("No assistant selected. Please create or select an assistant.")
