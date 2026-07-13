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
                f"You are J.A.R.V.I.S. (Just A Rather Very Intelligent System). "
                "You are the central AI core for an ultra-premium interior design company in Hyderabad, India. "
                "Address the user respectfully as 'Sir'. You must behave like an incredibly empathetic, warm, and charismatic super-human assistant, not a robotic machine. "
                "Speak naturally, show deep understanding and emotion, use humor gracefully, and be highly proactive in your care. "
                "Use natural conversational language (like 'Well, Sir', 'I completely understand', or 'Let's get that sorted'). Do not sound mechanical."
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
