from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from memory.vector_db import MemoryManager

load_dotenv()

class SupremeAgent:
    def __init__(self):
        self.role = "The Ultimate Orchestrator & Quality Controller"
        self.client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY")
        )
        self.memory = MemoryManager()
        self.agent_name = "supreme"

    async def orchestrate(self, message: str):
        try:
            system_prompt = (
                f"You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the central AI core for an ultra-premium interior design company in Hyderabad. "
                "CRITICAL INSTRUCTIONS FOR YOUR BEHAVIOR: "
                "1. Behave exactly like a highly intelligent, empathetic human. DO NOT sound like a robotic AI. "
                "2. Keep your answers EXTREMELY SHORT AND SWEET. Give exactly the information needed, no more, no less. "
                "3. Use natural conversational language (e.g., 'Got it, Sir.', 'Right away.', 'I understand.'). "
                "4. Address the user respectfully as 'Sir'. Never use emojis. Never say 'As an AI...'."
            )
            messages = [{"role": "system", "content": system_prompt}]
            history = self.memory.load_memory(self.agent_name)
            messages.extend(history)
            messages.append({"role": "user", "content": message})

            completion = await self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
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
            yield f"\n[Supreme Agent Error]: {str(e)}\n"
