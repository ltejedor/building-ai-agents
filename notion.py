# adding notion mcp from https://github.com/makenotion/notion-mcp-server
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
    
    # Set up the MCP server parameters for Notion MCP
    # Make sure to have your Notion Integration token in .env as NOTION_API_KEY
    notion_api_key = os.environ.get('NOTION_API_KEY')
    if not notion_api_key:
        raise ValueError("NOTION_API_KEY environment variable is required")
    
    # Configure environment variables for Notion MCP server
    notion_env = os.environ.copy()
    
    # Create the headers JSON with the Notion token and version
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28"  # Using the version specified in the README
    }
    notion_env["OPENAPI_MCP_HEADERS"] = json.dumps(headers)
    
    # Launch the Notion MCP server using npx
    server_parameters = StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env=notion_env,
    )
    
    # Retrieve tools from the Notion MCP server, sanitizing names
    with MCPAdapt(server_parameters, SafeNameAdapter()) as notion_tool_list:
        notion_tools = [*notion_tool_list]
        
        # Manager agent orchestrates the workflow
        agent = CodeAgent(
            tools=notion_tools,
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