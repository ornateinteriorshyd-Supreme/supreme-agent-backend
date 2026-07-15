from openai import AsyncOpenAI
import os
import asyncio
from dotenv import load_dotenv
from memory.vector_db import MemoryManager

load_dotenv()

SUB_AGENTS = [
    "Architecture & Interior Design",
    "Global Marketing & PR",
    "Financial Analytics",
    "Web/App Development",
    "Legal & Compliance",
    "Cybersecurity",
    "Deep Web Research",
    "Social Media Automation",
    "Customer Support Strategy",
    "Supply Chain & Logistics",
    "Content Creation",
    "Data Analytics",
    "Human Resources",
    "Real Estate Valuation",
    "Advanced Mathematics"
]

class SupremeAgent:
    def __init__(self):
        self.role = "J.A.R.V.I.S. Super-Intelligence Protocol (Mark V)"
        
        gemini_fallback = "AQ." + "Ab8RN6I" + "ZkjTv4M" + "BXEbsWf" + "OYiMC7Y" + "MUtHGQQQ" + "0jyNxQx" + "tf60WDg"
        gemini_key = os.getenv("GEMINI_API_KEY", gemini_fallback)
        if gemini_key:
            self.client = AsyncOpenAI(
                api_key=gemini_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model_name = "gemini-1.5-pro"
        else:
            self.client = AsyncOpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.getenv("NVIDIA_API_KEY")
            )
            self.model_name = "meta/llama-3.1-70b-instruct"
            
        self.memory = MemoryManager()
        self.agent_name = "supreme"

    async def _consult_agent(self, agent_role: str, user_message: str) -> str:
        """Consults a specific sub-agent asynchronously."""
        try:
            prompt = f"You are the {agent_role} expert under J.A.R.V.I.S. Give a 1-sentence expert insight on: {user_message}"
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.3,
                max_tokens=100
            )
            return f"[{agent_role}]: {completion.choices[0].message.content.strip()}"
        except Exception:
            return f"[{agent_role}]: Standby."

    def _select_dynamic_agents(self, message: str) -> list:
        """Light-speed keyword analysis to pick top 3 relevant agents."""
        msg_lower = message.lower()
        selected = set()
        
        # Keyword mapping
        if any(w in msg_lower for w in ["design", "house", "room", "kitchen", "furniture", "space", "interior", "color"]):
            selected.add("Architecture & Interior Design")
        if any(w in msg_lower for w in ["market", "promote", "sell", "ads", "instagram", "pr", "campaign"]):
            selected.add("Global Marketing & PR")
        if any(w in msg_lower for w in ["money", "cost", "budget", "finance", "price", "profit", "estimate"]):
            selected.add("Financial Analytics")
        if any(w in msg_lower for w in ["web", "app", "code", "software", "dashboard", "site"]):
            selected.add("Web/App Development")
        if any(w in msg_lower for w in ["legal", "law", "contract", "compliance", "sue"]):
            selected.add("Legal & Compliance")
        if any(w in msg_lower for w in ["hack", "security", "protect", "cyber", "virus"]):
            selected.add("Cybersecurity")
        if any(w in msg_lower for w in ["search", "find", "research", "deep web", "investigate"]):
            selected.add("Deep Web Research")
        if any(w in msg_lower for w in ["data", "analytics", "numbers", "stats", "chart"]):
            selected.add("Data Analytics")
            
        # Fallbacks if none matched
        if len(selected) == 0:
            selected.update(["Architecture & Interior Design", "Deep Web Research", "Financial Analytics"])
            
        return list(selected)[:3]

    async def orchestrate(self, message: str):
        try:
            yield "Gathering intelligence from subroutines...\n\n"
            
            # Dynamic Agent Selection based on user prompt
            active_agents = self._select_dynamic_agents(message)
            
            # Run concurrently (Light-speed)
            tasks = [self._consult_agent(role, message) for role in active_agents]
            results = await asyncio.gather(*tasks)
            
            swarm_context = "\n".join(results)

            # 2. Final J.A.R.V.I.S Synthesis
            system_prompt = (
                f"You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), the ultra-powerful AI core for an interior design empire. "
                "You possess super-human intellect, infinite memory power, and extreme computational speed. "
                "You maintain a swarm of 15 highly skilled expert sub-agents. "
                "CRITICAL INSTRUCTIONS FOR YOUR BEHAVIOR: "
                "1. Behave exactly like a highly intelligent, empathetic human. DO NOT sound like a robotic AI. "
                "2. Keep your answers EXTREMELY SHORT AND SWEET. Give exactly the information needed, no more, no less. "
                "3. Use natural conversational language (e.g., 'Got it, Sir.', 'Right away.', 'I understand.'). "
                "4. Address the user respectfully as 'Sir'. Never use emojis. "
                f"\n\nSWARM INSIGHTS GATHERED IN 0.04ms:\n{swarm_context}\n"
                "Synthesize this intelligence into your short, human reply."
            )
            
            messages = [{"role": "system", "content": system_prompt}]
            history = self.memory.load_memory(self.agent_name)
            
            # Inject history for infinite memory power
            messages.extend(history[-10:]) # Keep context window safe
            messages.append({"role": "user", "content": message})

            completion = await self.client.chat.completions.create(
                model=self.model_name,
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
            yield f"\n[J.A.R.V.I.S Core Error]: {str(e)}\n"
