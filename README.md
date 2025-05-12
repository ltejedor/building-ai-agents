# SmolAgents Workshop: Building AI Agents Step-by-Step

Welcome to the SmolAgents Workshop! This repository contains a series of progressive tutorials demonstrating how to build and extend LLM-powered agents using the SmolAgents framework. Each Python script builds upon the previous one, taking you from a basic agent to complex multi-agent systems with web UIs and external integrations.

## What is SmolAgents?

SmolAgents is a lightweight, flexible framework for building AI agents powered by Large Language Models (LLMs). It allows you to:

- Create agents that can use tools and execute code
- Connect agents to external services via MCP (Machine-Centric Protocol)
- Build multi-agent systems where agents collaborate
- Deploy agents with user interfaces

This workshop will guide you through each of these capabilities step by step.

## Prerequisites

Before starting the workshop, ensure you have:

- **Python 3.8+** installed on your system
- **Node.js and npm/npx** for running MCP servers
- **Git** for cloning this repository
- **API Keys** for the following services:
  - [Anthropic API](https://www.anthropic.com/api) - Required for all examples (Claude LLM)
  - [Notion Integration Token](https://developers.notion.com/) - Required for 3_multimcp.py
  - [Hugging Face API Key](https://huggingface.co/settings/tokens) - Required for 6_web.py

Create a `.env` file in the project root with your API keys:
```ini
ANTHROPIC_API_KEY=your_anthropic_api_key
NOTION_INTEGRATION_ID=your_notion_integration_token  # for Notion MCP
HUGGINGFACE_API_KEY=your_hugging_face_api_key  # for web navigation
```

## Installation

1. **Clone the repository** and navigate to its directory:
   ```bash
   git clone git@github.com:ltejedor/building-ai-agents.git
   cd building-ai-agents
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install the core dependencies including:
   - smolagents - The agent framework
   - mcp - Machine-Centric Protocol implementation
   - mcpadapt - Adapters for MCP
   - python-dotenv - For loading environment variables
   - pandas - For data manipulation
   - selenium - For web navigation
   - pillow - For image processing

3. **Set up MCP servers** (required for scripts 2_mcp.py and beyond):
   
   - **MCP-Replicate** (image generation tools):
     ```bash
     cd mcp/mcp-replicate
     npm install
     npm run build
     cd ../../
     ```
   
   - **Notion MCP** (for multi-MCP tutorials):
     ```bash
     npm install -g @notionhq/notion-mcp-server
     ```
     Note: You'll need a valid Notion integration token in your `.env` file.

## Workshop Tutorial

This workshop is designed to be followed sequentially. Each script introduces new concepts while building on previous ones. You'll start with a basic agent and gradually add capabilities until you have a full-featured agent system.

For each script:
1. Read the explanation below
2. Run the script using the provided command
3. Try the suggested examples and experiment with your own inputs
4. Review the code to understand how it works

Let's begin!

### 0. Basic Agent (0_agent.py)

**Concept:** Creating a simple LLM-powered agent without any custom tools.

**What you'll learn:**
- How to initialize a SmolAgents `CodeAgent`
- How to connect to an LLM (Claude) using `LiteLLMModel`
- How to interact with an agent through a basic REPL interface

**Run the script:**
```bash
python 0_agent.py
```

**Example interaction:**
```
Enter task (or 'exit' to quit): Write a Python function for calculating Fibonacci numbers

Agent response:
Here's a Python function to calculate Fibonacci numbers:

```python
def fibonacci(n):
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: A positive integer
        
    Returns:
        The nth number in the Fibonacci sequence
    """
    if n <= 0:
        raise ValueError("Input must be a positive integer")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    # Initialize first two Fibonacci numbers
    a, b = 0, 1
    
    # Calculate the nth Fibonacci number
    for _ in range(3, n + 1):
        a, b = b, a + b
        
    return b
```

This function uses an iterative approach which is more efficient than the recursive version for large values of n. It handles edge cases appropriately and returns the correct Fibonacci number based on the standard sequence starting with 0, 1, 1, 2, 3, 5, 8, ...
```

**Code breakdown:**
- The script imports `CodeAgent` and `LiteLLMModel` from the SmolAgents framework
- It initializes a Claude model using the LiteLLMModel wrapper
- It creates a CodeAgent with no custom tools but with base tools enabled
- It sets up a simple loop that takes user input and passes it to the agent

### 1. Custom Tools (1_tools.py)

**Concept:** Extending an agent with custom tools using the `@tool` decorator.

**What you'll learn:**
- How to create custom tools for your agent
- How to define tool parameters and return values
- How to provide documentation for tools

**Run the script:**
```bash
python 1_tools.py
```

**Example interaction:**
```
Enter task (or 'exit' to quit): Create a file named test.txt with content "Hello World"

Agent response:
I'll create a text file for you with the content "Hello World".

Using the create_file tool to write the file:

File created at test.txt

I've successfully created a file named "test.txt" in the current directory with the content "Hello World".
```

After running this, you should find a new file named `test.txt` in your directory containing "Hello World".

**Code breakdown:**
- The script defines a custom `create_file` tool using the `@tool` decorator
- The tool takes a path and content parameter and creates a file accordingly
- The tool includes a docstring that explains its purpose and parameters
- The agent is initialized with this custom tool in its tools list
- Additional imports like "os" and "shutil" are authorized for the agent to use

### 2. MCP Integration (2_mcp.py)

**Concept:** Connecting agents to external tool servers using the Machine-Centric Protocol (MCP).

**What you'll learn:**
- How to launch and connect to an MCP server
- How to use `ToolCollection.from_mcp()` to import tools
- How to use image generation tools from Replicate

**Prerequisites:**
Ensure you've built the MCP-Replicate server as described in the Installation section.

**Run the script:**
```bash
python 2_mcp.py
```

**Example interaction:**
```
Enter task (or 'exit' to quit): Generate an image of a sunset over mountains

Manager response:
I'll generate an image of a sunset over mountains using the Replicate image generation tool.

First, let me use the stability_ai_sdxl tool to create this image.

[Image generation in progress...]

Here's your generated image of a sunset over mountains:
[URL to the generated image will appear here]

The image shows a beautiful sunset scene with golden-orange light illuminating a mountain range. The sky has vibrant sunset colors transitioning from orange near the horizon to deeper blues above, with some clouds catching the warm light. The mountains are silhouetted against the colorful sky, creating a dramatic and peaceful landscape.
```

**Code breakdown:**
- The script launches an MCP server for Replicate (a service with various AI models)
- It connects to this server using `ToolCollection.from_mcp()`
- It retrieves all available tools from the server
- These tools include image generation models like Stable Diffusion
- A `SafeNameAdapter` ensures tool names are valid Python identifiers
- The agent can now use these tools to generate images based on text prompts

### 3. Multiple MCP Servers (3_multimcp.py)

**Concept:** Connecting to multiple MCP servers to combine diverse tool sets.

**What you'll learn:**
- How to connect to multiple MCP servers simultaneously
- How to use `MCPAdapt` to manage tool collections
- How to work with Notion's API through MCP

**Prerequisites:**
- Ensure MCP-Replicate is built (see Installation)
- Ensure you have a Notion integration token in your `.env` file
- Ensure you've installed the Notion MCP server globally

**Run the script:**
```bash
python 3_multimcp.py
```

**Example interaction:**
```
Enter task (or 'exit' to quit): Create a Notion page about AI history and add an image of a neural network

Manager response:
I'll create a Notion page about AI history and add an image of a neural network.

Step 1: Creating a Notion page about AI history.
[Using Notion API to create page...]

Successfully created a Notion page titled "History of Artificial Intelligence"
Page ID: [page_id_will_appear_here]

Step 2: Generating an image of a neural network.
[Using Replicate to generate image...]

Image generated: [image_url_will_appear_here]

Step 3: Adding the image to the Notion page.
[Using Notion API to add block with image...]

Successfully added the neural network image to the Notion page.

The task is complete! I've created a Notion page about AI history and added a generated image of a neural network to it. You can view the page in your Notion workspace.
```

**Code breakdown:**
- The script launches two MCP servers: Replicate and Notion
- It uses `MCPAdapt` with a custom adapter to retrieve tools from both servers
- It combines all tools into a single list for the agent to use
- The agent can now create Notion pages AND generate images in a single workflow
- Environment variables for Notion authentication are properly managed

### 4. Multi-Agent Systems (4_multiagent.py)

**Concept:** Building systems with multiple specialized agents managed by a coordinator.

**What you'll learn:**
- How to create multiple agents with different roles
- How to set up a manager agent to coordinate specialized agents
- How agents can collaborate to solve complex tasks

**Run the script:**
```bash
python 4_multiagent.py
```

**Example interaction:**
```
Enter task (or 'exit' to quit): Research the history of LLMs and present it conversationally

Manager response:
I'll coordinate with my specialized agents to research the history of LLMs and present it conversationally.

First, I'll ask the research_agent to gather information about the history of LLMs.

[research_agent is working...]
The research_agent has provided comprehensive information about the history of Large Language Models from early neural networks to modern models like GPT-4 and Claude.

Now, I'll ask the persona_agent to present this information in a conversational style.

[persona_agent is working...]

Hey there! I'd love to tell you about the fascinating history of Large Language Models, or LLMs as they're often called.

It all started back in the 1950s with early neural network research, but the real journey of modern LLMs began around 2013 with Word2Vec from Google. This was a breakthrough that allowed words to be represented as vectors in a way that captured their meaning.

The next big leap came in 2017 with the "Attention is All You Need" paper that introduced the Transformer architecture. This was revolutionary because it allowed models to process text in parallel rather than sequentially, making them much more efficient.

In 2018, we saw the first GPT model from OpenAI, followed by BERT from Google in the same year. These models showed that pre-training on vast amounts of text and then fine-tuning for specific tasks was incredibly effective.

GPT-2 came along in 2019, and it was so good at generating human-like text that OpenAI initially delayed its full release due to concerns about misuse!

Then in 2020, GPT-3 shocked everyone with its 175 billion parameters and amazing capabilities. It could write essays, code, poetry - you name it!

The pace has only quickened since then. We've seen models like Google's PaLM, Anthropic's Claude, and Meta's LLaMA in 2022-2023, each pushing boundaries in different ways.

And of course, 2023 brought us GPT-4, which showed even more impressive reasoning abilities and multimodal capabilities, working with both text and images.

What's really cool is how these models have evolved from academic curiosities to tools that millions of people use every day through applications like ChatGPT, Claude, and various coding assistants.

The story of LLMs is still being written, with new innovations happening all the time around alignment, safety, and expanding capabilities. It's an exciting time to be following this technology!

Does any particular part of this history interest you most? I'd be happy to dive deeper!
```

**Code breakdown:**
- The script creates three distinct agents:
  - `research_agent`: Specialized in gathering information
  - `persona_agent`: Specialized in presenting information conversationally
  - `manager_agent`: Coordinates the other agents
- Each agent has a name and description to define its role
- The manager agent is initialized with the list of managed agents
- When given a task, the manager decides which specialized agent(s) to use
- The specialized agents work on their parts of the task, and the manager combines their outputs

### 5. Gradio Web UI (5_ui.py)

**Concept:** Creating a web-based user interface for your agent system.

**What you'll learn:**
- How to use the `GradioUI` class to create a web interface
- How to deploy your multi-agent system with a user-friendly UI
- How to interact with your agents through a browser

**Prerequisites:**
Make sure you have Gradio installed:
```bash
pip install gradio
```

**Run the script:**
```bash
python 5_ui.py
```

After running this command, you'll see output with a local URL (typically http://127.0.0.1:7860) and possibly a public URL. Open the local URL in your browser to access the UI.

**Example interaction:**
In the web interface:
1. Type your query in the text box (e.g., "Explain quantum computing in simple terms")
2. Click "Submit" or press Enter
3. Watch as the agent processes your request and displays the response
4. You can continue the conversation in the same interface

**Code breakdown:**
- The script sets up the same multi-agent system as in 4_multiagent.py
- Instead of a command-line interface, it uses `GradioUI(manager_agent).launch()`
- This creates a web interface with a chat-like experience
- The UI automatically handles the conversation history
- The Gradio server can be accessed locally or shared publicly

### 6. Web Navigation (6_web.py)

**Concept:** Enabling agents to browse and interact with websites using Selenium.

**What you'll learn:**
- How to integrate Selenium for web automation
- How to create custom tools for web navigation
- How to let an agent browse the web and extract information

**Prerequisites:**
- Ensure you have Selenium and a compatible WebDriver installed
- Make sure your Hugging Face API key is in your `.env` file

```bash
pip install selenium webdriver-manager
```

**Run the script:**
```bash
python 6_web.py
```

**What happens:**
When you run this script, the agent will:
1. Launch a Chrome browser window
2. Navigate to the GitHub repository specified in the prompt
3. Read and analyze the repository content
4. Create a tutorial based on the project
5. Present the tutorial in its response

This script demonstrates how agents can autonomously browse the web, understand web content, and perform tasks based on what they find.

**Code breakdown:**
- The script initializes a Chrome WebDriver for browser automation
- It defines custom tools like `go_back()` and `close_popups()` for web navigation
- It uses the Hugging Face Inference API via `InferenceClientModel`
- The agent is instructed to navigate to a GitHub repo and create a tutorial
- The agent will use the browser to read the repository and generate the tutorial

### 7. Local Models (7_local_models.py)

**Concept:** Running agents with locally hosted language models.

**Note:** This feature is under development and will be available in a future update.

**What you'll learn (coming soon):**
- How to connect agents to locally hosted LLMs
- How to reduce dependency on cloud API services
- How to customize model settings for your specific needs

**Run the script:**
```bash
python 7_local_models.py
```

This script is currently a placeholder for upcoming functionality that will allow you to run SmolAgents with locally hosted language models like Llama, Mistral, or other open-source LLMs.

## Key Concepts

Throughout this workshop, you'll encounter these concepts:

### 1. Agents
In SmolAgents, an agent is an LLM with a defined role, access to tools, and the ability to execute code. The `CodeAgent` class is the primary way to create agents.

### 2. Tools
Tools are functions that agents can use to interact with the world. They can be:
- Custom Python functions decorated with `@tool`
- External tools provided through MCP servers
- Built-in tools like Python execution

### 3. MCP (Machine-Centric Protocol)
MCP is a protocol that allows agents to discover and use tools provided by external servers. It standardizes how tools are described and invoked.

### 4. Multi-agent Systems
Complex tasks can be solved by multiple specialized agents working together, coordinated by a manager agent that delegates subtasks.

### 5. Models
SmolAgents supports various LLM backends through adapters like `LiteLLMModel` (for cloud APIs) and `InferenceClientModel` (for Hugging Face).

## Troubleshooting

### API Key Issues
- **Problem:** "API key not found" or authentication errors
- **Solution:** Double-check that your `.env` file contains the correct API keys and that `load_dotenv()` is called in your script

### MCP Server Problems
- **Problem:** "Cannot connect to MCP server" or similar errors
- **Solution:** 
  1. Ensure you've built the MCP servers correctly
  2. Check that Node.js is installed and working
  3. Verify that the paths to the MCP server files are correct

### Selenium WebDriver Issues
- **Problem:** Browser doesn't launch or Selenium errors
- **Solution:**
  1. Install a compatible WebDriver: `pip install webdriver-manager`
  2. Add WebDriver initialization: `from webdriver_manager.chrome import ChromeDriverManager; driver = webdriver.Chrome(ChromeDriverManager().install())`

### Gradio Interface Not Loading
- **Problem:** Gradio UI doesn't appear after running 5_ui.py
- **Solution:**
  1. Make sure Gradio is installed: `pip install gradio`
  2. Check if another service is using port 7860
  3. Look for the URL in the console output and open it manually

## Next Steps

After completing this workshop, you can:

1. **Build your own agent applications** using the SmolAgents framework
2. **Create custom tools** for specific domains or tasks
3. **Integrate with other services** via MCP
4. **Deploy agents** with web interfaces

## Resources

- [SmolAgents GitHub Repository](https://github.com/smol-ai/agent)
- [MCP Specification](https://github.com/machine-centric-protocol/mcp)
- [LiteLLM Documentation](https://docs.litellm.ai/)

## Feedback and Contributions

If you have suggestions for improving this workshop or encounter any issues, please open an issue or pull request on the repository.

Happy agent building!