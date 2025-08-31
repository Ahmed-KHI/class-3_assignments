import chainlit as cl
from weather_agent import agent
from agents import Runner
from weather_tool import get_weather
import re

@cl.on_chat_start
async def start():
    await cl.Message(content="🌤️ Hello! I'm your Weather Info Agent. I can provide current weather information for any city around the world. Just ask me something like 'What's the weather in Karachi?' or 'How's the weather in London?'").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.lower()
    
    weather_keywords = ['weather', 'temperature', 'temp', 'climate', 'forecast', 'hot', 'cold', 'rain', 'sunny']
    is_weather_query = any(keyword in user_input for keyword in weather_keywords)
    
    if is_weather_query:
        
        city_patterns = [
            r'weather in ([^?]+)',
            r'temperature in ([^?]+)',
            r'climate in ([^?]+)',
            r'weather of ([^?]+)',
            r'weather for ([^?]+)',
        ]
        
        city = None
        for pattern in city_patterns:
            match = re.search(pattern, user_input)
            if match:
                city = match.group(1).strip()
                break
        
        if city:
            await cl.Message(content=f"🔍 Fetching weather information for {city.title()}...").send()
            
            weather_info = get_weather(city)
            
            await cl.Message(content=weather_info).send()
        else:
            await cl.Message(content="🤔 Let me check the weather for you...").send()
            
            try:
                result = Runner.run_sync(agent, message.content)
                await cl.Message(content=result.final_output).send()
            except Exception as e:
                await cl.Message(content=f"❌ Sorry, I couldn't process your request. Please try asking about the weather in a specific city, like 'What's the weather in Karachi?'").send()
    else:
        await cl.Message(content="🌤️ I'm a weather specialist! I can help you with weather information for any city. Try asking something like 'What's the weather in your city?' or 'How's the temperature in London?'").send()
