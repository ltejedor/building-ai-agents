# SmolAgents Agent-Building Tutorial

A step-by-step tutorial demonstrating how to build and extend LLM-powered agents using the SmolAgents framework. Each Python script in this repository builds on the previous one, showing how to start with a basic agent, add custom tools, integrate with MCP servers, orchestrate multiple agents, and launch a Gradio UI.

## Prerequisites
- Python 3.8 or higher
- Node.js (for MCP servers) and npm or npx
- Git
- Create a `.env` file in the project root with the following variables:
  ```ini
  ANTHROPIC_API_KEY=your_anthropic_api_key
  NOTION_INTEGRATION_ID=your_notion_integration_token  # for Notion MCP
  ```

## Installation
1. Clone this repository and enter its directory:
   ```bash
   git clone git@github.com:ltejedor/building-ai-agents.git
   cd building-ai-agents
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If you plan to use the Gradio UI (5_ui.py), also install:
   ```bash
   pip install gradio
   ```
3. Prepare MCP servers:
   - MCP-Replicate:
     ```bash
     cd mcp/mcp-replicate
     npm install
     npm run build
     cd ../../
     ```
   - Notion MCP (optional, for multi-MCP tutorials):
     ```bash
     npm install -g @notionhq/notion-mcp-server
     ```

## Tutorial Scripts
Follow along by running each script in order.

### 0_agent.py: Basic Agent
Initializes a simple agent without any external tools.
```bash
python 0_agent.py
```
*Example:* Enter `Write a Python function for Fibonacci` and see the agent's response.

### 1_tools.py: Custom File Tool
Adds a `create_file` tool to write files to disk.
```bash
python 1_tools.py
```
*Example:* Enter `Create a file named test.txt with content "Hello World"`.

### 2_mcp.py: Integrate MCP-Replicate
Connects to a local MCP server exposing Replicate APIs.
Ensure MCP-Replicate is built (see Installation).
```bash
python 2_mcp.py
```
*Example:* Enter `Generate an image of a sunset over mountains`.

### 3_multmcp.py: Multiple MCP Servers
Combines MCP-Replicate and Notion MCP toolsets via `MCPAdapt`.
Make sure the Notion MCP server is available (see Installation).
```bash
python 3_multimcp.py
```
*Example:* Enter `Create a Notion page summarizing AI breakthroughs. Fill it with relevant graphics using Replicate image generation.`.

### 4_multiagent.py: Multi-Agent Orchestration
Demonstrates two agents (`research_agent`, `persona_agent`) managed by a `manager_agent`.
```bash
python 4_multiagent.py
```
*Example:* Ask `Research the history of LLMs and present it conversationally`.

### 5_ui.py: Gradio Web UI
Launches a Gradio interface for the multi-agent manager.
```bash
python 5_ui.py
```
Open the provided local URL in your browser to interact via a GUI.

### 6_local_models.py: Local Models (Coming Soon)
A placeholder for examples using local LLMs.

