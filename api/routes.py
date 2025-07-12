from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from core.agent import root_agent

router = APIRouter()

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

runner = Runner(
    app_name="islamic_guidance_app",
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service
)

class QueryRequest(BaseModel):
    query: str

@router.on_event("startup")
async def setup():
    await session_service.create_session(
        app_name="islamic_guidance_app",
        user_id="user",
        session_id="session",
        state={}
    )

@router.on_event("shutdown")
async def cleanup():
    await session_service.delete_session(
        app_name="islamic_guidance_app",
        user_id="user",
        session_id="session"
    )

@router.post("/query")
async def query(request: QueryRequest):
    try:
        msg = types.Content(role="user", parts=[types.Part(text=request.query)])
        async for event in runner.run_async(
            user_id="user",
            session_id="session",
            new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                return {"result": event.content.parts[0].text}
        return {"result": "No response"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
