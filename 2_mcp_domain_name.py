# adding mcp from https://github.com/bingal/FastDomainCheck-MCP-Server/

from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os
import json

# Load environment variables
load_dotenv()

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Path to the compiled binary (not the folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_binary_path = os.path.join(
        current_dir, "mcp", "FastDomainCheck-MCP-Server", "FastDomainCheck-MCP-Server"
    )

    # Launch the FastDomainCheck-MCP-Server
    server_parameters = StdioServerParameters(
        command=mcp_binary_path,
        args=[],  # No additional arguments needed
        env=os.environ.copy(),
    )

    # Retrieve tools from the MCP server
    with MCPAdapt(server_parameters, SafeNameAdapter()) as domain_tool_list:
        domain_tools = [*domain_tool_list]

        print(f"Loaded {len(domain_tools)} domain tools from MCP server")

        # Set up the agent
        agent = CodeAgent(
            tools=domain_tools,
            model=model,
            add_base_tools=True,
            additional_authorized_imports=["time", "pandas", "json"],
        )

        # REPL loop
        while True:
            task = input("\nEnter news query (or 'exit' to quit): ")
            if task.lower() in ['exit', 'quit']:
                break

            try:
                print("\nThinking...")
                result = agent.run(task)
                print("\nAgent response:\n", result)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == '__main__':
    main()