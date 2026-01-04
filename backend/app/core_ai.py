
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class CoreAI:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_mock = False
        
        if not self.api_key or "your_gemini_api_key" in self.api_key:
            print("Warning: GEMINI_API_KEY not set. Using Mock Mode.")
            self.is_mock = True
        else:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                google_api_key=self.api_key,
                temperature=0.2
            )
            
    async def generate_response(self, system_prompt: str, user_message: str):
        if self.is_mock:
            return "[MOCK RESPONSE] Analysis complete. System secure."
            
        messages = [
            ("system", system_prompt),
            ("human", user_message)
        ]
        response = await self.llm.ainvoke(messages)
        return response.content
