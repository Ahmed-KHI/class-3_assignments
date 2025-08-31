import chainlit as cl
from math_agent import agent
from agents import Runner

@cl.on_chat_start
async def start():
    await cl.Message(content="I am your Math Tool Agent. I can help you with calculations using my math tools: addition, subtraction, multiplication, and division.").send()

@cl.on_message
async def main(message: cl.Message):
    
    await cl.Message(content="Let me solve this using my math tools...").send()
    
    prompt = message.content
    
    result = Runner.run_sync(agent, prompt)
    
    await cl.Message(content=f"Result: {result.final_output}").send()