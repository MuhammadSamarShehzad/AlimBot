from fastapi import APIRouter, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from core.agent import root_agent
import uuid
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

APP_NAME = "islamic_guidance_app"

router = APIRouter()

# In-memory services (replace with Redis/DB-backed ones in production)
# Dictionary mapping session ID to InMemoryChatMessageHistory
session_store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

runner = RunnableWithMessageHistory(
    root_agent,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

class QueryRequest(BaseModel):
    query: str

async def get_or_create_sid(request: Request, response: Response) -> str:
    """Return a per-client sid stored in a cookie; create session if new."""
    sid = request.cookies.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
        # Set cookie so the same client reuses the same session
        response.set_cookie(
            key="sid",
            value=sid,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30  # 30 days
        )
    return sid

@router.post("/query")
async def query(request_body: QueryRequest, request: Request, response: Response, sid: str = Depends(get_or_create_sid)):
    try:
        # Run the agent with memory
        result = await runner.ainvoke(
            {"input": request_body.query},
            config={"configurable": {"session_id": sid}}
        )
        
        return {"result": result["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: allow a client to wipe its own session/history
@router.post("/reset")
async def reset_session(request: Request, response: Response, sid: str = Depends(get_or_create_sid)):
    try:
        if sid in session_store:
            session_store[sid].clear()
        return {"status": "reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
