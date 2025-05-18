# adding mcp (rime) from https://github.com/MatthewDailey/rime-mcp
# Will not work in Code Spaces - only locally
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

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    # Set up the MCP server parameters for Rime MCP
    # Update this to point to the Rime MCP location specified in your documentation
    rime_mcp_dir = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp", "rime-mcp")
    )
    
    # Configure environment variables for Rime
    rime_env = os.environ.copy()
    # Add required API key - make sure this is in your .env file
    if 'RIME_API_KEY' not in rime_env:
        raise ValueError("RIME_API_KEY environment variable is required")
    
    # Optional Rime configuration - these can be set in your .env file
    # or uncomment and set them directly here
    # rime_env['RIME_GUIDANCE'] = "Be concise and informative when speaking"
    # rime_env['RIME_WHO_TO_ADDRESS'] = "User"
    # rime_env['RIME_WHEN_TO_SPEAK'] = "when asked to speak or when finishing a command"
    # rime_env['RIME_VOICE'] = "cove"  # Default voice
    
    # Launch the Rime MCP server using npx
    server_parameters = StdioServerParameters(
        command="npx",
        args=["rime-mcp"],
        env=rime_env,
    )

    # Retrieve tools from the Rime MCP server, sanitizing names
    with MCPAdapt(server_parameters, SafeNameAdapter()) as rime_tool_list:
        rime_tools = [*rime_tool_list]
        
        # Manager agent orchestrates the workflow
        agent = CodeAgent(
            tools=rime_tools,
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