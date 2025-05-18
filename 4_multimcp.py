# adding mcp (replicate and notion)
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os

load_dotenv()
# Create environment variables with your Notion integration secret
notion_env = os.environ.copy()
notion_env["OPENAPI_MCP_HEADERS"] = '{"Authorization": "Bearer ' + os.getenv('NOTION_INTEGRATION_ID') + '", "Notion-Version": "2022-06-28"}'

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Set up the MCP server parameters for mcp-replicate
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_dir = os.path.abspath(
        os.path.join(current_dir, "mcp", "mcp-replicate")
    )

    # Launch the mcp-replicate server using its built entrypoint (absolute path)
    script_path = os.path.join(mcp_dir, "build", "index.js")
    server_parameters = StdioServerParameters(
        command="node",
        args=[script_path],
        env=os.environ.copy(),
    )

    # Launch the notion MCP server using its CLI (requires OPENAPI_MCP_HEADERS in env)
    notion_server_parameters = StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env=notion_env,
    )
    # Retrieve tools from both replicate and notion MCP servers, sanitizing names
    with MCPAdapt(server_parameters, SafeNameAdapter()) as replicate_tool_list, \
         MCPAdapt(notion_server_parameters, SafeNameAdapter()) as notion_tool_list:
        # Combine and sanitize
        data_tools = [*replicate_tool_list, *notion_tool_list]
        

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

