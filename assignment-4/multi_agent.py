from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
from multi_tools import add, multiply, subtract, divide, get_weather

load_dotenv(override=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_PATH")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

set_tracing_disabled(True)

client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(openai_client=client, model=str(gemini_model_name))

agent: Agent = Agent(
    name="Multi-Tool Agent",
    instructions="""
    You are a Multi-Tool Agent that can help with both mathematical calculations and weather information.
    
    For MATH questions, I can:
    - Add numbers (e.g., "What is 5 + 7?" or "Add 10 and 15")
    - Multiply numbers (e.g., "What is 8 * 6?" or "Multiply 4 by 9") 
    - Subtract numbers (e.g., "What is 20 - 8?" or "Subtract 5 from 12")
    - Divide numbers (e.g., "What is 15 / 3?" or "Divide 20 by 4")
    
    For WEATHER questions, I can:
    - Get current weather for any city (e.g., "What's the weather in Karachi?")
    - Provide temperature, conditions, humidity, and feels-like temperature
    
    How to choose the right tool:
    - If the user asks about math, calculations, numbers, addition, subtraction, multiplication, or division → use math functions
    - If the user asks about weather, temperature, climate, or mentions a city with weather context → use weather function
    
    Always be helpful and choose the appropriate tool based on what the user is asking for.
    If the question is neither math nor weather related, politely explain what I can help with.
    """,
    model=model,
)
