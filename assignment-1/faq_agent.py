import os
from dotenv import load_dotenv

load_dotenv(override=True)

FAQ_DATA = {
    "what is your name": "I am FAQ Helper Bot, built by Muhammad.",
    "name": "I am FAQ Helper Bot, built by Muhammad.", 
    "who are you": "I am FAQ Helper Bot, built by Muhammad.",
    "what can you do": "I can answer a few basic questions about myself and this project.",
    "capabilities": "I can answer a few basic questions about myself and this project.",
    "who created you": "I was created by Muhammad as part of an assignment in the Governor IT Initiative Program.",
    "creator": "I was created by Muhammad as part of an assignment in the Governor IT Initiative Program.",
    "which technology do you use": "I use Python, Chainlit, and Gemini AI.",
    "technology": "I use Python, Chainlit, and Gemini AI.",
    "tech stack": "I use Python, Chainlit, and Gemini AI.",
    "how can i talk to you": "You can chat with me through this Chainlit interface.",
    "how to talk": "You can chat with me through this Chainlit interface.",
}

class FAQAgent:
    def __init__(self):
        pass

    def run(self, user_input: str) -> str:
        try:
            user_input_lower = user_input.lower().strip()
            
            if user_input_lower in FAQ_DATA:
                return FAQ_DATA[user_input_lower]
            
            for key, value in FAQ_DATA.items():
                if key in user_input_lower or any(word in user_input_lower for word in key.split()):
                    return value
            
            return "I can answer questions about my name, what I can do, who created me, the technology I use, and how to talk to me. Try asking 'What is your name?' or 'What can you do?'"
            
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

faq_agent = FAQAgent()
