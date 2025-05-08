# gradio ui
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel, GradioUI
import re
import pandas as pd
import time
import os

load_dotenv()

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    research_agent=CodeAgent(
        tools=[],
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
        tools=[],
        model=model,
        add_base_tools=True,
        managed_agents=[research_agent, persona_agent],
        additional_authorized_imports=["time", "pandas", "numpy"],
    )

    GradioUI(manager_agent).launch()
