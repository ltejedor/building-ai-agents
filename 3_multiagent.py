# multiagent# adding mcp
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os

load_dotenv()

# Set up the MCP server parameters for Google Sheets
current_dir = os.path.dirname(os.path.abspath(__file__))
mcp_dir = os.path.abspath(
    os.path.join(current_dir, "mcp", "google-sheets-mcp")
)

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)
 

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    server_parameters = StdioServerParameters(
        command="node",
        args=["dist/index.js"],
        env=os.environ.copy(),
        cwd=mcp_dir,
    )

    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as gs_tool_collection:
        data_tools = [*gs_tool_collection.tools]

        research_agent=CodeAgent(
            tools=data_tools,
            model=model,
            add_base_tools=True,
            name="research_agent",
            description="research and gather information from the internet and other sources",
        )

        persona_agent=CodeAgent(
            tools=[],
            model=model,
            add_base_tools=True,
            name="persona_agent",
            description="act as a persona and provide responses based on the given context",
        )

        # Manager agent orchestrates the workflow
        manager_agent = CodeAgent(
            tools=data_tools,
            model=model,
            add_base_tools=True,
            managed_agents=[research_agent, persona_agent],
            additional_authorized_imports=["time", "pandas", "numpy"],
        )

        # Interactive REPL via manager
        while True:
            task = input("\nEnter task (or 'exit' to quit): ")
            if task.lower() in ['exit', 'quit']:
                break
            try:
                result = manager_agent.run(task)
                print("\nManager response:\n", result)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    main()

