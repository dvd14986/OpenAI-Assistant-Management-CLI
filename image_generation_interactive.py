# Imports
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Update with your API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to generate image with customization
def generate_image(prompt, model, size, quality, style, response_format):
    print("Generating image...")
    try:
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size=size,
            model=model,
            quality=quality,
            response_format=response_format,
            style=style
        )
        print("Image generated successfully.")
        if response_format == 'url':
            return response.data[0].url
        else:
            print(response)
            return None
    except Exception as e:
        print(f"Failed to generate image: {e}")
        return None

# Function to display help
def show_help():
    print("Available commands:")
    print("generate - Generate a new image with custom parameters")
    print("exit - Exit the script")

# Function to get user choice with escape option
def user_choice(prompt, options):
    print(f"{prompt}\n0. Go back")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input("Enter your choice (number): ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return None
            elif 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print("Choice out of range. Please enter a valid number.")
        else:
            print("Invalid input. Please enter a number.")

# Main Loop
def main():
    while True:
        user_input = input("\nEnter your command: ")

        if user_input.lower() == "exit":
            sys.exit()
        elif user_input.lower() == "generate":
            prompt = input("Enter your prompt for the image: ")

            # Customization options
            models = ["dall-e-2","dall-e-3"]
            sizes = ["256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"]
            qualities = ["hd", "medium", "standard"]
            styles = ["natural", "vivid"]
            response_formats = ["url", "b64_json"]

            model = user_choice("Choose a model:", models)
            if model is None: continue
            size = user_choice("Choose image size:", sizes)
            if size is None: continue
            quality = user_choice("Choose image quality:", qualities)
            if quality is None: continue
            style = user_choice("Choose image style:", styles)
            if style is None: continue
            response_format = user_choice("Choose response format:", response_formats)
            if response_format is None: continue

            if None not in [model, size, quality, style, response_format]:
                image_url = generate_image(prompt, model, size, quality, style, response_format)
                if image_url:
                    print(f"Image URL: {image_url}")
        elif user_input.lower() == "help":
            show_help()
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()
