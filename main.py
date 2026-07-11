from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.supreme_agent import SupremeAgent
from agents.interior_agent import InteriorDesignAgent
from agents.marketing_agent import MarketingAgent
from agents.admin_agent import AdminAgent
from memory.vector_db import init_memory

app = FastAPI(title="Supreme Agent Orchestrator API", description="Ultra-Premium AI Backend")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
supreme = SupremeAgent()
interior = InteriorDesignAgent()
marketing = MarketingAgent()
admin = AdminAgent()

# Initialize Memory
init_memory()

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Ultra-Premium System Online", "version": "3.0", "agents": ["supreme", "interior", "marketing", "admin"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/chat/{agent_name}")
async def chat_with_agent(agent_name: str, req: MessageRequest):
    if agent_name == "interior":
        generator = interior.process_message(req.message)
    elif agent_name == "marketing":
        generator = marketing.process_message(req.message)
    elif agent_name == "admin":
        generator = admin.process_message(req.message)
    else:
        generator = supreme.orchestrate(req.message)

    return StreamingResponse(
        generator,
        media_type="text/plain; charset=utf-8",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
            "Access-Control-Allow-Origin": "*"
        }
    )
