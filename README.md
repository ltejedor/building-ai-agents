# 🤖 Building AI Agents Workshop

Welcome! This beginner-friendly workshop will teach you how to build AI assistants (agents) powered by large language models like Claude. You'll start with simple agents and gradually build more advanced features - no prior AI experience required!

## 📚 What You'll Learn

In this step-by-step workshop, you'll learn how to:
- Create AI agents that can use tools and run code
- Connect your agents to external services like Notion and image generators
- Build systems where multiple AI agents work together
- Create user-friendly web interfaces for your agents
- Let your agents browse the web and interact with websites

## 🔍 What Are AI Agents?

AI agents are programs that use large language models (LLMs) like Claude or GPT to:
- Understand natural language requests
- Plan how to complete tasks
- Use tools and services to accomplish goals
- Communicate results back to humans

Think of them as smart assistants that can perform tasks for you by combining AI with access to various tools.

## 🛠️ What You'll Build

This workshop includes 7 progressive tutorials, each building on the previous one:

1. **Basic Agent**: A simple AI assistant that can answer questions
2. **Custom Tools**: Add capabilities like creating files to your agent
3. **External Services**: Connect your agent to image generation tools
4. **Multiple Services**: Let your agent use both Notion and image generation
5. **Multi-Agent Systems**: Create specialized agents that work together
6. **Web Interface**: Build a user-friendly chat interface for your agents
7. **Web Navigation**: Enable your agent to browse websites (Coming soon: Local Models)

## ⚙️ Setup Guide

### Prerequisites

Before starting, you'll need:

- **Python 3.8 or newer** installed on your computer
- **Node.js and npm** installed (for running tool servers)
- **Git** for downloading this workshop
- **API Keys** (most examples use Claude's API):
  - [Anthropic API Key](https://www.anthropic.com/api) (Required for all examples)
  - [Notion Integration Token](https://developers.notion.com/) (For tutorial #3 and beyond)
  - [Hugging Face API Key](https://huggingface.co/settings/tokens) (For tutorial #6)

> 💡 **New to APIs?** An API key is like a password that lets your code access services like Claude. You'll need to create accounts with these services to get your keys.

### Step 1: Download the Workshop

Open your terminal or command prompt and run:

```bash
git clone https://github.com/ltejedor/building-ai-agents.git
cd building-ai-agents
```

### Step 2: Set Up Your API Keys

Create a file named `.env` in the main folder and add your API keys:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
NOTION_INTEGRATION_ID=your_notion_integration_token  # for tutorial #3
HUGGINGFACE_API_KEY=your_hugging_face_api_key  # for tutorial #6
```

> ⚠️ **Important**: Never share your API keys or commit them to public repositories!

### Step 3: Install Python Dependencies

Run this command to install all required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- `smolagents`: The framework we'll use to build agents
- `mcp`: A protocol for connecting to external tools
- Other helpful libraries for our projects

### Step 4: Set Up External Tool Servers

For tutorials #2 and beyond, you'll need these tool servers:

**For Image Generation (MCP-Replicate)**:
```bash
cd mcp/mcp-replicate
npm install
npm run build
cd ../../
```

**For Notion Integration**:
```bash
npm install -g @notionhq/notion-mcp-server
```

## 🚀 Getting Started

This workshop is designed to be followed in order. Each tutorial builds on skills from previous ones.

For each tutorial:
1. Read the explanation
2. Run the script
3. Try the example and experiment with your own inputs
4. Look at the code to understand how it works

Let's begin!

## 📖 Workshop Tutorials

### Tutorial 1: Basic Agent (0_agent.py)

**What you'll learn**: How to create your first AI agent that can answer questions and write code.

**Run it**:
```bash
python 0_agent.py
```

**Try asking**:
- "Write a Python function for calculating Fibonacci numbers"
- "Explain how solar panels work"
- "Create a simple HTML webpage with CSS"

**How it works**:
This script creates a simple agent powered by Claude. It can understand your questions and generate helpful responses, including code.

### Tutorial 2: Custom Tools (1_tools.py)

**What you'll learn**: How to give your agent special abilities (tools) like creating files.

**Run it**:
```bash
python 1_tools.py
```

**Try asking**:
- "Create a file named test.txt with content 'Hello World'"
- "Write a Python script that prints the current date and save it to date.py"

**How it works**:
We add custom tools to our agent using Python functions. The agent can now interact with your computer by creating files when you ask it to.

### Tutorial 3: External Services (2_mcp.py)

**What you'll learn**: How to connect your agent to external AI services like image generators.

**Run it**:
```bash
python 2_mcp.py
```

**Try asking**:
- "Generate an image of a sunset over mountains"
- "Create a picture of a futuristic robot in a garden"

**How it works**:
This script connects to an external image generation service (Replicate) using a protocol called MCP. Your agent can now create images based on your descriptions.

### Tutorial 4: Multiple Services (3_multimcp.py)

**What you'll learn**: How to connect your agent to multiple services at once.

**Run it**:
```bash
python 3_multimcp.py
```

**Try asking**:
- "Create a Notion page about AI history and add an image of a neural network"
- "Make a Notion page with travel tips and include an image of a tropical beach"

**How it works**:
Your agent can now use both Notion (for creating documents) and image generation services together, combining their capabilities to complete more complex tasks.

### Tutorial 5: Multi-Agent Systems (4_multiagent.py)

**What you'll learn**: How to create a team of specialized AI agents that work together.

**Run it**:
```bash
python 4_multiagent.py
```

**Try asking**:
- "Research the history of LLMs and present it conversationally"
- "Explain quantum computing in a friendly way"

**How it works**:
This script creates three agents: a researcher, a conversational presenter, and a manager. The manager coordinates the other agents to complete your task efficiently.

### Tutorial 6: Web Interface (5_ui.py)

**What you'll learn**: How to create a user-friendly chat interface for your agents.

**Run it**:
```bash
python 5_ui.py
```

After running this command, open the link (usually http://127.0.0.1:7860) in your web browser to see your agent's chat interface.

**How it works**:
This script uses a library called Gradio to create a web-based chat interface for your multi-agent system, making it easier to interact with your agents.

### Tutorial 7: Web Navigation (6_web.py)

**What you'll learn**: How to enable your agent to browse websites and extract information.

**Run it**:
```bash
python 6_web.py
```

**What happens**:
The agent will open a web browser, navigate to a GitHub repository, read its content, and create a tutorial based on what it finds.

**How it works**:
This script uses Selenium (a web automation tool) to give your agent the ability to control a web browser, allowing it to visit websites and interact with web pages.

### Coming Soon: Local Models (7_local_models.py)

**What you'll learn**: How to run your agents using locally hosted language models instead of cloud APIs.

## 🔑 Key Concepts Explained

### What is an Agent?
An agent is an AI assistant that uses a large language model (like Claude) combined with tools to solve problems and complete tasks.

### What are Tools?
Tools are functions that give your agent abilities beyond just generating text. For example, a tool might let your agent create files, generate images, or search the web.

### What is MCP?
MCP (Machine-Centric Protocol) is a way for your agent to discover and use tools provided by external services. Think of it as a universal adapter that lets your agent connect to different tools.

### What is a Multi-Agent System?
A multi-agent system uses multiple specialized agents that work together. For example, one agent might research information while another presents it in a friendly way.

## ❓ Troubleshooting

### API Key Issues
**Problem**: You see "API key not found" or authentication errors
**Solution**: 
- Check that your `.env` file has the correct API keys
- Make sure the file is in the main folder of the project
- Verify there are no spaces around the equals sign

### MCP Server Problems
**Problem**: "Cannot connect to MCP server" errors
**Solution**:
- Make sure you've completed the setup steps for the MCP servers
- Check that Node.js is installed properly
- Try restarting the terminal and running the script again

### Browser Automation Issues
**Problem**: Browser doesn't launch or Selenium errors appear
**Solution**:
- Install the WebDriver Manager: `pip install webdriver-manager`
- Make sure Chrome is installed on your computer
- Check that your Python environment has all required packages

### Web Interface Not Loading
**Problem**: The Gradio UI doesn't appear after running 5_ui.py
**Solution**:
- Make sure Gradio is installed: `pip install gradio`
- Look for the URL in the terminal output and open it manually
- Try a different browser if the interface doesn't load

## 🎓 Next Steps

After completing this workshop, you can:

1. **Create your own agent projects** using what you've learned
2. **Develop custom tools** for specific tasks you need help with
3. **Connect to other services** like Google Calendar or Slack
4. **Share your agents** with others using web interfaces

## 📚 Resources

- [SmolAgents GitHub Repository](https://github.com/smol-ai/agent)
- [MCP Specification](https://github.com/machine-centric-protocol/mcp)
- [LiteLLM Documentation](https://docs.litellm.ai/)

## 🙋‍♀️ Getting Help

If you get stuck or have questions:
- Check the troubleshooting section above
- Read the comments in the example scripts
- Open an issue on the GitHub repository

Happy building! 🚀
