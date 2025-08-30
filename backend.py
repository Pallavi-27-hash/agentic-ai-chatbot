# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from ai_agent import get_response_from_ai_agent

# Allowed models
ALLOWED_MODEL_NAMES = [
    "llama3-70b-8192",
    "gpt-4o-mini",
    "mixtral-8x7b-32768",
    "llama-3.3-70b-versatile"
]

# Pydantic models
class MessageItem(BaseModel):
    role: str
    content: str

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[MessageItem]
    allow_search: bool

# FastAPI app
app = FastAPI(title="Langgraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    # Validate model
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Model not allowed."}

    # Combine all user messages into a single string for the AI agent
    query = " ".join([msg.content for msg in request.messages if msg.role == "user"])

    # Call AI agent
    response = get_response_from_ai_agent(
        llm_id=request.model_name,
        query=query,
        allow_search=request.allow_search,
        system_prompt=request.system_prompt,
        provider=request.model_provider
    )

    return {"response": response}

# Run app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)

