# starter code 
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel

load_dotenv()

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Create agent
    agent = CodeAgent(
        tools=[],
        model=model,
        add_base_tools=True,
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

