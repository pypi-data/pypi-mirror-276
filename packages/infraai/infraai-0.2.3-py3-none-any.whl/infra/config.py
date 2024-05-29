import os
import configparser
import google.generativeai as genai
import platform
import distro

from rich.console import Console
from rich.markdown import Markdown
from rich import print as rprint

CONFIG_PATH = os.path.expanduser('~/.infrashrc')

console = Console()

def get_config():
    """Retrieve the API key and model from the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    api_key = config.get('DEFAULT', 'api_key', fallback=None)
    model = config.get('DEFAULT', 'model', fallback='gemini-pro')  # Default to gemini-pro if not set
    return api_key, model

def set_key(api_key):
    """Set the API key in the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config['DEFAULT']['api_key'] = api_key
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def set_model(model):
    """Set the Gemini model in the config file."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    config['DEFAULT']['model'] = model
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)


def ask_ai(prompt, api_key, model="gemini-pro"):
    # configure the api key
    genai.configure(api_key=api_key)
    
    # Get the OS name
    os_name = platform.system().lower()  # will return 'windows', 'darwin' (for macOS), or 'linux'
    if os_name == 'darwin':
        os_name = 'macos'
    elif os_name == 'linux':
        # Get more detailed distribution information on Linux
        os_name = distro.id() 
    
    instructions = f"Provide precise terminal commands for {os_name} without introductory explanations. Assume the user is already in the terminal and understands basic command execution. Provide only essential options."
    full_prompt = f"{prompt}\n{instructions}"

    # Generate the response
    try:
        modell = genai.GenerativeModel(model_name=model)
        response = modell.generate_content(full_prompt)
        rprint("[bold green]Here![/bold green] We got your response:")
        md = Markdown(response.candidates[0].content.parts[0].text)
        console.print(md)
        #new line added to create space between next console input
        print() 

    except Exception as e:
        return f"An error occurred: {str(e)}"
