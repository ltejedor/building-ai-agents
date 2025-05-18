# gradio ui
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, GradioUI
import re
import pandas as pd
import time
import os

load_dotenv()

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

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
        add_base_tools=False,
        managed_agents=[research_agent, persona_agent],
        additional_authorized_imports=[],
    )

    GradioUI(manager_agent).launch()

if __name__ == '__main__':
    main()