# adding mcp from https://github.com/ltejedor/newsfeed-mcp

from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from mcp import StdioServerParameters
import re
import pandas as pd
import time
import os

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
    
    # Set up the MCP server parameters for newsfeed-mcp
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_dir = os.path.abspath(
        os.path.join(current_dir, "mcp", "newsfeed-mcp")
    )
    
    # Launch the newsfeed-mcp server
    server_parameters = StdioServerParameters(
        command="python",
        args=[os.path.join(mcp_dir, "news_mcp.py")],
        env=os.environ.copy(),
    )
    
    # Retrieve tools from the News MCP server, sanitizing names
    with MCPAdapt(server_parameters, SafeNameAdapter()) as news_tool_list:
        news_tools = [*news_tool_list]
        
        print(f"Loaded {len(news_tools)} news tools from MCP server")
        
        # News agent with access to the newsfeed tools
        agent = CodeAgent(
            tools=news_tools,
            model=model,
            add_base_tools=True,
            additional_authorized_imports=["time", "pandas", "json"],
        )
        
        # Interactive REPL
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