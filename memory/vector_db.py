import json
import os

# Use /data for Railway persistent volume, fallback to local
DATA_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", ".")
MEMORY_FILE = os.path.join(DATA_DIR, "long_term_memory.json")

class MemoryManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'w') as f:
                json.dump({}, f)

    def load_memory(self, agent_name: str) -> list:
        try:
            with open(MEMORY_FILE, 'r') as f:
                data = json.load(f)
            return data.get(agent_name, [])
        except Exception:
            return []

    def save_memory(self, agent_name: str, messages: list):
        try:
            try:
                with open(MEMORY_FILE, 'r') as f:
                    data = json.load(f)
            except Exception:
                data = {}
            # Keep last 20 messages to stay within token limits
            data[agent_name] = messages[-20:]
            with open(MEMORY_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Memory save error: {e}")

def init_memory():
    print("✅ Persistent Memory Initialized.")
