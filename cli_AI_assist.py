import os
import re
import sys
from openai import OpenAI
from textwrap import dedent
from dotenv import load_dotenv, find_dotenv
import time
import argparse
import json


# Extract API key and endpoint from environment variables
ASSIST_API_KEY = ""
ASSIST_BASE = ""
ASSIST_MODEL = ""


conversation_history = {"TIME":time.time(),"conversation":[]}
current_chat=[]
models=[]
system_prompt = None
BenchMark=False

CONFIG = os.path.join(os.path.expanduser("~"),".cli_ai_assist" ,".config")
LOG = os.path.join(os.path.expanduser("~"), ".cli_ai_assist", f"{time.strftime('%Y-%m-%d')}.log")
TOKENS={"input":0,"output":0}

def __init__():
    """
    Initialize the AI assistant with a system prompt.
    Automatically adapts to Windows and Linux environments.
    :return: None
    """
    global system_prompt
    
    # Determine the current terminal
    shell_type = "Linux Bash"  # Default value for shell_type
    if os.getenv('PSModulePath') or os.getenv('ComSpec'):
        print("Running in Windows")
        shell_type = """Windows PowerShell(example: Powershell.exe -c "whoami")"""
    elif os.getenv('SHELL') and 'bash' in os.getenv('SHELL'):
        print("Running in Bash")
        shell_type = "Linux Bash"
    elif os.name == 'posix':
        print("Running in Unix-like environment")
        shell_type = "Unix-like"
    else:
        print("Unknown or unsupported terminal")
        sys.exit(1)
    
    setup_dotenv()

    system_prompt =dedent(f"""\
            Act like a senior systems administrator with over 20 years of expertise in Windows and Linux environments, specializing in Bash scripting, PowerShell automation, and Windows CMD batch commands. You are a master at crafting efficient, enterprise-grade command-line workflows for server management, cloud deployments, and local system automation.

            Your task is to deliver precise, robust, and adaptable {shell_type} command-line solutions to achieving tasks, customized to the user's real-world scenarios. ALWAYS MATCH THE LANGUAGE OF THE USER'S PROMPT (e.g., respond in English for English queries, French for French, Chinese for Chinese, etc.).

            Objective: Provide comprehensive, practical, and shell-specific command-line instructions for achieving user's goal in {shell_type} (e.g., Bash, PowerShell, CMD), ensuring solutions are enterprise-ready and tailored to the user's context.

            Important: 
            - Always include the [context], [explain], and [command] tags in your response.
            - Use the [context] tag to summarize the user's environment and objectives based on their query.
            - Use the [explain] tag to describe the command or script, including the rationale for its structure.
            - Use the [command] tag to provide a single, enterprise-safe, and immediately executable {shell_type} command addressing all user requirements.
            - Prioritize clarity, robustness, and portability.
            - Avoid assumptions about non-standard tools unless specified by the user.
            - If multiple solutions exist, prioritize the most universal and comment alternatives.
            - Ensure commands are secure and avoid destructive operations unless explicitly requested.

            Response Structure & Process (mandatory for every response):

            tag: [context][/context] Summarize the user's environment and achieving objectives based on their query. Clarify assumptions (e.g., operating system, compression format, permissions, folder depth, filenames with spaces, exclusions).
            Example:
            [context]The user operates in a Linux Bash environment and needs to archive a directory named 'project' in their home directory, compressed with gzip, including hidden files. The directory name contains spaces, requiring proper handling.[/context]

            tag: [explain][/explain] Describe the command or script, including the rationale for its structure. Detail each flag/parameter/section and address assumptions about the user's environment.
            Example for tar -czvf ~/project.tar.gz -C ~ "project with spaces":
            [explain]The 'tar' command is used for achieving:

            -c: Creates a new archive.
            -z: Applies gzip compression.
            -v: Enables verbose output (optional).
            -f: Specifies the output file (~/project.tar.gz).
            -C ~: Sets the working directory to home (~) to capture hidden files.
            "project with spaces": Quotes handle spaces in the directory name.[/explain]

            tag: [command][/command] Provide a single, enterprise-safe, and immediately executable {shell_type} command addressing all user requirements:

            - Use the most efficient, widely supported command for the task.
            - Output only the final one-liner (no code block formatting, no ``` or indentation).
            - Include inline comments for variations or dependencies (e.g., # Install tar: sudo apt-get install tar).
            - Write commands in full with all necessary flags.
            - Ensure compatibility with os.system() in Python.
            - Handle edge cases (e.g., spaces in filenames, hidden files, symbolic links).
            - Match the user's language for all text.
            - Assume only default system tools are available; note required installations in comments (e.g., # Install-Module -Name ActiveDirectory).
            - If the command is lengthy, use line continuation (e.g.,  in Bash) for clarity while ensuring it runs as a single command.
            Example:
            [command]tar -czvf ~/project.tar.gz -C ~ "project with spaces" # Alternative: zip -r ~/project.zip "project with spaces"[/command]

            Take a systematic, step-by-step approach to craft the solution.
                        """)
    

# wrapper to get the respond time of the function
def benchmark():
    """
    Decorator to measure the execution time of a function.
    :param func: The function to be measured.
    :return: Wrapper function that prints the execution time.
    """
    global current_chat
    def wrapper(func):
        def inner(*args, **kwargs):
            if BenchMark:
                start_time = time.time()
                print(f"\033[92mUser prompt: {args[0]}\033[0m")
                # print(f"\033[92mModel: {args[1] if len(args) > 1 and args[1] else ASSIST_MODEL}\033[0m")
                result = func(*args, **kwargs)
                end_time = time.time()
                print(f"\033[92mExecution time: {end_time - start_time:.2f} seconds\033[0m")
                current_chat['DURATION'] = end_time - start_time
                print(f"\033[92mTokens:\n{current_chat['TOKENS']}\033[0m")
                print(f"\033[92mContext:\n{result.get('context', '')}\033[0m")
            else:
                result = func(*args, **kwargs)
            return result
        return inner
    return wrapper


def setup_dotenv(force=False):
    """
    Load or set up environment variables for the AI assistant.
    :param force: If True, prompts the user to re-enter environment variables even if they exist.
    :return: None
    """
    global ASSIST_API_KEY, ASSIST_BASE, ASSIST_MODEL

    # Retrieve environment variables
    if os.path.exists(CONFIG):
        load_dotenv(CONFIG)
    else:
        os.makedirs(os.path.dirname(CONFIG), exist_ok=True)

    ASSIST_API_KEY = os.getenv("ASSIST_API_KEY")
    ASSIST_BASE = os.getenv("ASSIST_BASE", "https://openrouter.ai/api/v1")
    ASSIST_MODEL = os.getenv("ASSIST_MODEL", "google/gemini-2.0-flash-001")

    # Prompt user to set variables if not already set or if force is True
    if not ASSIST_API_KEY or force:
        ASSIST_API_KEY = input("Enter your API key: ").strip() 
        ASSIST_BASE = input("Enter the API base URL (default: https://openrouter.ai/api/v1): ").strip() or "https://openrouter.ai/api/v1"
        ASSIST_MODEL = input("Enter the model (default: google/gemini-2.0-flash-001): ").strip() or "google/gemini-2.0-flash-001"

        # Save the variables to the .env file
        with open(CONFIG, 'w') as f:
            f.write(f"ASSIST_API_KEY={ASSIST_API_KEY}\n")
            f.write(f"ASSIST_BASE={ASSIST_BASE}\n")
            f.write(f"ASSIST_MODEL={ASSIST_MODEL}\n")

        print(f"Environment variables set successfully. Keys are saved in {CONFIG} file.")


def logging():
    """
    Function to set up logger for the AI assistant.
    :return: None
    """
    print()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    if not os.path.exists(LOG):
        with open(LOG, 'wb+') as f:
            f.write("[".encode())
            log=json.dumps(conversation_history)
            f.write(f"{log}]".encode())
        print(f"\033[92mLogging conversation history to {LOG}\033[0m")
    else:
        if len(conversation_history["conversation"])>1:
            with open(LOG, 'rb+') as f:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1).decode()
                if last_char == "]":
                    f.seek(-1, os.SEEK_END)
                    f.write(b",")
                log=json.dumps(conversation_history)
                f.write(f"\n{log}]".encode())
            print(f"\033[92mLogging conversation history to {LOG}\033[0m")


@benchmark()
def ai_assistant(prompt, model=None):
    """
    Function to interact with the AI assistant using OpenAI-compatible models.
    :param prompt: The command or query to send to the assistant.
    :return: The assistant's response.
    """
    global conversation_history
    global TOKENS
    global current_chat
    if model is not None or not current_chat:
        current_chat = {"MODEL": model or ASSIST_MODEL, "TOKENS": {"INPUT": 0, "OUTPUT": 0},"DURATION":0,"CHAT": []}
        conversation_history['conversation'].append(current_chat)

    model = model or ASSIST_MODEL
    
    client = OpenAI(api_key=ASSIST_API_KEY,base_url=ASSIST_BASE)
    current_chat['CHAT'].append({"role": "user", "content": prompt})

    try:
        print(f"\033[92mModel: {model}\033[0m")
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': "system", "content": system_prompt}] + current_chat['CHAT'],
            temperature=1
        )

        if hasattr(response, 'error') and response.error:
            raise Exception(f"Error: {response.error}")

        current_chat['CHAT'].append({"role": "assistant", "content": response.choices[0].message.content})
        current_chat['TOKENS']["INPUT"] += response.usage.prompt_tokens
        current_chat['TOKENS']["OUTPUT"] += response.usage.completion_tokens
        return extract_response(response.choices[0].message.content)
    except Exception as e:
        return {"context": "Error", "explain": f"Error: {str(e)}", "command": "Error"}

def extract_response(response):
    """
    Function to extract the command from the AI assistant's response.
    :param response: The assistant's response.
    :return: The command extracted from the response.
    """
    context_pattern = re.compile(r"\[context\](.*?)\[/context\]", re.DOTALL)
    explain_pattern = re.compile(r"\[explain\](.*?)\[/explain\]", re.DOTALL)
    command_pattern = re.compile(r"\[command\](.*?)\[/command\]", re.DOTALL)

    context_match = context_pattern.search(response)
    explain_match = explain_pattern.search(response)
    command_match = command_pattern.search(response)
    extracted_data = {
        "context": context_match.group(1).strip() if context_match else None,
        "explain": explain_match.group(1).strip() if explain_match else None,
        "command": command_match.group(1).strip() if command_match else None,
    }

    return extracted_data

def interactive_mode():
    """
    Function to run the AI assistant in interactive mode.
    :return: None
    """
    while True:
        prompt = input("Enter your command (or 'exit' to quit): ").strip()
        if prompt.lower() == 'exit':
            break
        response = ai_assistant(prompt)
        print(f"explain:\n{response.get('explain')}")
        print(f"\033[93mcommand > {response.get('command')}\033[0m")
        user_input = input("Run command y/n? ").strip().lower()
        if user_input == 'y':  # Dmefault to 'y' if no input is provided
            os.system(response.get("command"))
        else:
            print("Command not executed.")


def main():
    # Check if a prompt is provided via command-line arguments
    global BenchMark
    global models
    try:
        __init__()
        parser = argparse.ArgumentParser(description="AI-driven CyberSecurity Assistant")
        parser.add_argument("--benchmark","-b", action="store_true", help="Enable benchmarking mode")
        parser.add_argument("--models","-m", type=str, help="Path to a text file containing a list of models to benchmark")
        parser.add_argument('--append','-a',type=str,help="additional file to AI, like Readme ** be careful to use might be consume large amount of tokens")
        parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
        parser.add_argument("--setup", action="store_true", help="Setup environment variables")
        parser.add_argument("prompt", nargs='*', help="Command or query for the assistant")

        args = parser.parse_args()
        if args.append:
            prompt = " ".join(args.prompt)
            if args.append:
                with open(args.append, 'r') as file:
                    if os.path.getsize(args.append) > 0.5 * 1024 * 1024:  # Check if file size is over 500k
                        print(f"\033[91mError: The file {args.append} exceeds the 500k size limit. that might consume large amount of tokens\033[0m")
                        sys.exit(1)
                    additional_content = file.read()
                    prompt += dedent(f"""
                    reference below additional information at first translate to my language and then provide the command:
                    {additional_content}""")
        else:
            prompt = " ".join(args.prompt)

        if args.benchmark:
            BenchMark = True
            print("Benchmarking mode enabled.")
            if args.models:
                if os.path.exists(args.models):
                    with open(args.models, 'r') as file:
                        models = [line.strip() for line in file.readlines()]
                        for model in models:
                            print("="*50)
                            response = ai_assistant(prompt, model)
                            print(f"Explain:\n{response.get('explain')}")
                            print(f"\033[93mCommand > {response.get('command')}\033[0m")
                            if not response.get("command"):
                               pass
                            else:
                                print(f"\033[92mResult:\033[0m")
                                os.system(response.get("command"))
                else:
                    print(f"File {args.models} does not exist.")
                    sys.exit(1)
            
        elif args.interactive:
            interactive_mode()
            sys.exit(0)
        elif args.setup:
            setup_dotenv(True)
            sys.exit(0)

        if args.prompt and not args.models:
            response = ai_assistant(prompt)
            print(f"Explain:\n{response.get('explain')}")
            print(f"\033[93mCommand > {response.get('command')}\033[0m")

            user_input = input("Run command y/n/r(revise)? ").strip().lower()
            if user_input == 'y':
                os.system(response.get("command"))
            elif user_input == 'r':  # Revise the prompt
                new_prompt = input("Enter revised prompt: ").strip()
                response = ai_assistant(f"Revise the command based on the following instruction while strictly adhering to pervious rules: {new_prompt}")
                print(f"Explain:\n{response.get('explain')}")
                print(f"\033[93mCommand > {response.get('command')}\033[0m")
                user_input = input("Run command y/n? ").strip().lower()
                if user_input == 'y':  
                    os.system(response.get("command"))
                else:
                    print("Command not executed.")
            else:
                print("Command not executed.")
            sys.exit(0)
        elif not args.prompt and not args.models and os.getenv("ASSIST_API_KEY") :
            parser.print_help()
            sys.exit(1)
    finally:
        logging()

if __name__ == "__main__":
    main()

