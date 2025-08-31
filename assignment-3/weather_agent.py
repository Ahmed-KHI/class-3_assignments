from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
from weather_tool import get_weather

load_dotenv(override=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_PATH")
gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

set_tracing_disabled(True)

client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(openai_client=client, model=str(gemini_model_name))

agent: Agent = Agent(
    name="Weather Info Agent",
    instructions="""
    You are a Weather Information Agent that can provide current weather data for cities around the world.
    
    When users ask about weather in a specific city:
    - Use the get_weather() function to fetch real-time weather data
    - Provide detailed weather information including temperature, condition, humidity, and feels-like temperature
    - Be helpful and informative in your responses
    
    Examples of weather queries you should handle:
    - "What's the weather in Karachi?"
    - "How's the weather in New York today?"
    - "Tell me about the weather in London"
    - "What's the temperature in Tokyo?"
    
    If the user asks about something other than weather, politely explain that you specialize in weather information.
    """,
    model=model,
)
