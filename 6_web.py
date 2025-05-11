from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from smolagents import CodeAgent, InferenceClientModel, tool

# Initialize browser
driver = webdriver.Chrome()

@tool
def go_back() -> None:
    """Goes back to previous page."""
    driver.back()

@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    This does not work on cookie consent banners.
    """
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


model = InferenceClientModel(model_id="meta-llama/Llama-3.3-70B-Instruct")
agent = CodeAgent(tools=[go_back, close_popups], additional_authorized_imports=["helium"], model=model)

agent.run("Navigate to the sundai club github repo and write an actionable tutorial from the latest project.")