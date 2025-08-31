from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv(override=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_PATH")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

set_tracing_disabled(True)

def add(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

def subtract(a: float, b: float) -> float:
    """Subtract second number from first number"""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide first number by second number"""
    if b == 0:
        return float('inf')
    return a / b

client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(openai_client=client, model=str(gemini_model_name))

agent: Agent = Agent(
    name="Math Tool Agent",
    instructions="""
    You are a Math Agent that can perform calculations using built-in math functions.
    When users ask math questions:
    - For addition like "5 + 7" or "what is 5 plus 7", calculate the sum
    - For multiplication like "8 * 6" or "what is 8 times 6", calculate the product
    - For subtraction like "20 - 8" or "what is 20 minus 8", calculate the difference  
    - For division like "15 / 3" or "what is 15 divided by 3", calculate the quotient
    
    Show your work and provide clear answers.
    If the question is not math related, politely decline to answer.
    """,
    model=model,
)
