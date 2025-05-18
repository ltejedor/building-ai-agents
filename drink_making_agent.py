# drink_making_agent.py — for a SmolAgents Workshop Mocktail Station
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, GradioUI, tool
import random

load_dotenv()

@tool
def get_available_ingredients() -> list[str]:
    """
    Returns a list of available mocktail ingredients.
    Participants can add or remove ingredients from this function to match their setup.
    """
    return [
        "Pineapple seltzer",
        "Lime seltzer",
        "Iced coffee",
        "Limes",
        "Lemons",
        "Cranberry juice",
        "Watermelon lemonade seltzer",
        "Black cherry vanilla seltzer",
        "Plain seltzer",
        "Oranges",
        "Jalapeno limeade",
        "Margarita mix",
    ]

@tool
def drink_generator(name: str, ingredients: list[str]) -> str:
    """
    Given a mocktail name and list of ingredients, returns a fun recipe script.
    The agent can choose how to interpret the name — literally, by vibe, or through flavor logic.
    
    Args:
        name (str): A name or theme for the drink (e.g. 'Sunset Glow', 'Boss Energy').
        ingredients (list[str]): List of available ingredients.

    Returns:
        A whimsical mocktail recipe script as a string.
    """
    base = random.choice([i for i in ingredients if "seltzer" in i or "juice" in i])
    citrus = random.choice([i for i in ingredients if "lime" in i.lower() or "lemon" in i.lower() or "orange" in i.lower()])
    twist = random.choice([i for i in ingredients if i not in [base, citrus]])

    steps = [
        f"🔸 Start with a cold glass — chilled like your best ideas.",
        f"🔸 Pour 3 oz of {base} as your base — fizzy foundations matter.",
        f"🔸 Add a squeeze of {citrus} for a zesty punch.",
        f"🔸 Stir in a dash of {twist} — trust your instincts here.",
        f"🔸 Optional: Garnish with something that sparks joy.",
        f"🔸 Name your creation: *{name}*. Serve with flair.",
    ]
    
    return "\n".join(steps)

def main():
    model = InferenceClientModel(model_id="Qwen/Qwen2.5-72B-Instruct")

    agent = CodeAgent(
        tools=[get_available_ingredients, drink_generator],
        model=model,
        add_base_tools=True,
        name="mocktail_maker",
        description=(
            "A customizable mocktail-making agent. "
            "Give it a theme or a vibe and let it choose ingredients and steps. "
            "The tools don't prescribe; they invite creativity and experimentation."
        ),
    )

    print("🍹 Welcome to the Mocktail Station 🍹\nType a drink name and let the agent invent something delicious.\nType 'exit' to leave.")

    GradioUI(agent).launch()

if __name__ == "__main__":
    main()
