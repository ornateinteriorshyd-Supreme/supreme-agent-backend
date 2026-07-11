from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from memory.vector_db import MemoryManager

load_dotenv()

class AdminAgent:
    def __init__(self):
        self.role = "Operations & Financial Manager"
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.memory = MemoryManager()
        self.agent_name = "admin"

    async def process_message(self, message: str):
        try:
            system_prompt = (
                f"You are an {self.role} for an ultra-premium interior design company in Hyderabad, India. "
                "Handle operations, budgets, vendor management, and financial planning with extreme accuracy. "
                "Be professional, precise, and results-oriented. "
                "Always provide structured, actionable information."
            )
            messages = [{"role": "system", "content": system_prompt}]
            history = self.memory.load_memory(self.agent_name)
            messages.extend(history)
            messages.append({"role": "user", "content": message})

            completion = await self.client.chat.completions.create(
                model="meta/llama-3.1-8b-instruct",
                messages=messages,
                temperature=0.2,
                top_p=1,
                max_tokens=1024,
                stream=True
            )

            final_answer = ""
            async for chunk in completion:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    final_answer += content

            # Save to persistent memory
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": final_answer})
            self.memory.save_memory(self.agent_name, history)

        except Exception as e:
            yield f"\n[Admin Agent Error]: {str(e)}\n"
