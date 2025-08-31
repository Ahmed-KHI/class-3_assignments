import chainlit as cl
from multi_agent import agent
from agents import Runner
from multi_tools import add, multiply, subtract, divide, get_weather
import re

@cl.on_chat_start
async def start():
    await cl.Message(content="""🤖 Hello! I'm your Multi-Tool Agent!

I can help you with two types of tasks:

🧮 **Math Operations:**
- Addition: "What is 5 + 7?"
- Subtraction: "What is 20 - 8?" 
- Multiplication: "What is 8 * 6?"
- Division: "What is 15 / 3?"

🌤️ **Weather Information:**
- "What's the weather in Karachi?"
- "How's the weather in London?"
- "Tell me about the weather in New York"

Just ask me anything about math or weather!""").send()

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.lower()
    
    math_keywords = ['add', 'plus', 'sum', '+', 'subtract', 'minus', '-', 'multiply', 'times', '*', 'x', 'divide', 'division', '/', 'calculate', 'what is']
    math_patterns = [r'\d+\s*[\+\-\*\/]\s*\d+', r'what is \d+', r'calculate', r'math']
    
    is_math_query = any(keyword in user_input for keyword in math_keywords) or any(re.search(pattern, user_input) for pattern in math_patterns)
    
    weather_keywords = ['weather', 'temperature', 'temp', 'climate', 'forecast', 'hot', 'cold', 'rain', 'sunny']
    is_weather_query = any(keyword in user_input for keyword in weather_keywords)
    
    if is_math_query and not is_weather_query:
        await cl.Message(content="🧮 Let me solve this math problem for you...").send()
        
        add_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:\+|plus|add)\s*(\d+(?:\.\d+)?)', user_input)
        subtract_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:\-|minus|subtract)\s*(\d+(?:\.\d+)?)', user_input)
        multiply_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:\*|x|times|multiply)\s*(\d+(?:\.\d+)?)', user_input)
        divide_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:\/|divide)\s*(\d+(?:\.\d+)?)', user_input)
        
        result = None
        operation = ""
        
        if add_match:
            a, b = float(add_match.group(1)), float(add_match.group(2))
            result = add(a, b)
            operation = f"{a} + {b}"
        elif subtract_match:
            a, b = float(subtract_match.group(1)), float(subtract_match.group(2))
            result = subtract(a, b)
            operation = f"{a} - {b}"
        elif multiply_match:
            a, b = float(multiply_match.group(1)), float(multiply_match.group(2))
            result = multiply(a, b)
            operation = f"{a} * {b}"
        elif divide_match:
            a, b = float(divide_match.group(1)), float(divide_match.group(2))
            result = divide(a, b)
            operation = f"{a} / {b}"
        
        if result is not None:
            await cl.Message(content=f"🧮 **Math Result:**\n{operation} = **{result}**").send()
        else:
            try:
                agent_result = Runner.run_sync(agent, message.content)
                await cl.Message(content=f"🧮 **Math Result:**\n{agent_result.final_output}").send()
            except Exception as e:
                await cl.Message(content="❌ Sorry, I couldn't solve that math problem. Please try a simpler format like '5 + 3' or 'What is 10 * 2?'").send()
    
    elif is_weather_query and not is_math_query:
        
        city_patterns = [
            r'weather in ([^?,.!]+)',
            r'weather of ([^?,.!]+)',
            r'weather for ([^?,.!]+)',
            r'temperature in ([^?,.!]+)',
            r'climate in ([^?,.!]+)',
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
            await cl.Message(content=f"🌤️ **Weather Information:**\n{weather_info}").send()
        else:
            await cl.Message(content="🌤️ I'd be happy to check the weather for you! Please specify a city, like 'What's the weather in Karachi?' or 'How's the weather in London?'").send()
    
    elif is_math_query and is_weather_query:
        await cl.Message(content="🤔 I see you're asking about both math and weather. Could you please ask about one thing at a time? I can help with either math calculations or weather information!").send()
    
    else:
        try:
            agent_result = Runner.run_sync(agent, message.content)
            await cl.Message(content=agent_result.final_output).send()
        except Exception as e:
            await cl.Message(content="""🤖 I specialize in two areas:

🧮 **Math**: Ask me to calculate, add, subtract, multiply, or divide numbers
🌤️ **Weather**: Ask me about the weather in any city

Try asking something like:
- "What is 15 + 25?"
- "What's the weather in Tokyo?"

What would you like to know?""").send()
