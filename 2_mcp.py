# adding mcp (replicate)
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, InferenceClientModel
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os

load_dotenv()

# Set up the MCP server parameters for mcp-replicate
current_dir = os.path.dirname(os.path.abspath(__file__))
mcp_dir = os.path.abspath(
    os.path.join(current_dir, "mcp", "mcp-replicate")
)

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Launch the mcp-replicate server using its built entrypoint (absolute path)
    script_path = os.path.join(mcp_dir, "build", "index.js")
    server_parameters = StdioServerParameters(
        command="node",
        args=[script_path],
        env=os.environ.copy(),
    )

    # Connect to the MCP server and retrieve tools exposed by mcp-replicate
    with ToolCollection.from_mcp(server_parameters) as mcp_tool_collection:
        data_tools = [*mcp_tool_collection.tools]
        

        # Manager agent orchestrates the workflow
        agent = CodeAgent(
            tools=data_tools,
            model=model,
            add_base_tools=True,
            additional_authorized_imports=["time", "pandas", "numpy"],
        )

        # Interactive REPL via manager
        while True:
            task = input("\nEnter task (or 'exit' to quit): ")
            if task.lower() in ['exit', 'quit']:
                break
            try:
                result = agent.run(task)
                print("\nManager response:\n", result)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    main()

