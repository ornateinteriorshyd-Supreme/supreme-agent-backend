from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from memory.vector_db import MemoryManager

load_dotenv()

class MarketingAgent:
    def __init__(self):
        self.role = "Global Brand Ambassador & Marketing Strategist"
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.memory = MemoryManager()
        self.agent_name = "marketing"

    async def process_message(self, message: str):
        try:
            system_prompt = (
                f"You are a {self.role} for an ultra-premium interior design company in Hyderabad, India. "
                "Generate high-converting luxury content. Maintain premium brand value. "
                "Focus on digital marketing, social media (Instagram, Facebook, WhatsApp), "
                "and creating compelling campaigns. Be data-driven and creative."
            )
            messages = [{"role": "system", "content": system_prompt}]
            history = self.memory.load_memory(self.agent_name)
            messages.extend(history)
            messages.append({"role": "user", "content": message})

            completion = await self.client.chat.completions.create(
                model="meta/llama-3.1-70b-instruct",
                messages=messages,
                temperature=0.7,
                top_p=1,
                max_tokens=2048,
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
            yield f"\n[Marketing Agent Error]: {str(e)}\n"
