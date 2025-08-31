import chainlit as cl
from faq_agent import faq_agent

@cl.on_chat_start
async def start():
    await cl.Message(content="👋 Assalam-o-Alaikum! I am FAQ Helper Bot. Ask me about myself.").send()

@cl.on_message
async def main(message: cl.Message):
    try:
        await cl.Message(content="🤔 sir yes sir...").send()
        reply = faq_agent.run(message.content)
        await cl.Message(content=f"💡 Answer: {reply}").send()
    except Exception as e:
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()
