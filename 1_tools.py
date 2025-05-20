# add custom tools
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, tool
import os

load_dotenv()

@tool
def create_file(path: str, content: str) -> str:
    """
    Creates a file at the specified path with the given content.

    Args:
        path: The filesystem path where the file will be created.
        content: The text content to write into the file.
        Returns a success message or an error description.
    
    Returns: 
        The location and name of the file was created, or an error.
    """
    try:
        # Ensure directory exists
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File created at {path}"
    except Exception as e:
        return f"Error creating file: {e}"

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Create agent
    agent = CodeAgent(
        tools=[create_file],
        model=model,
        add_base_tools=True,
        additional_authorized_imports=["os", "shutil"],
    )

    # Agent conversation
    while True:
        task = input("\nEnter task (or 'exit' to quit): ")
        if task.lower() in ['exit', 'quit']:
            break
        try:
            result = agent.run(task)
            print("\nAgent response:\n", result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
