# starter code 
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel

load_dotenv()

def main():
    # Initialize the LLM model
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Create agent
    agent = CodeAgent(
        tools=[],
        model=model,
        #add_base_tools=True,
        #additional_authorized_imports=["time", "pandas", "json"],
    )

    # Agent conversation
    while True:
        task = input("\nEnter task (or 'exit' to quit): ")
        if task.lower() in ['exit', 'quit']:
            break
        try:
            result = agent.run(task)
            print("\Agent response:\n", result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()

