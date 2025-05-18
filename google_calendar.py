# adding mcp (google calendar) from https://github.com/nspady/google-calendar-mcp
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os

load_dotenv()

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Set up the MCP server parameters for google-calendar-mcp
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_dir = os.path.abspath(
        os.path.join(current_dir, "mcp", "google-calendar-mcp")
    )

    # Launch the google-calendar-mcp server using its built entrypoint (absolute path)
    script_path = os.path.join(mcp_dir, "build", "index.js")
    server_parameters = StdioServerParameters(
        command="node",
        args=[script_path],
        env=os.environ.copy(),
    )

    # Retrieve tools from the Google Calendar MCP server, sanitizing names
    with MCPAdapt(server_parameters, SafeNameAdapter()) as calendar_tool_list:
        calendar_tools = [*calendar_tool_list]
        
        # Manager agent orchestrates the workflow
        agent = CodeAgent(
            tools=calendar_tools,
            model=model,
            add_base_tools=True,
            additional_authorized_imports=["time"],
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