from fastapi import APIRouter, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from core.agent import root_agent
import uuid
from typing import Optional

APP_NAME = "islamic_guidance_app"

router = APIRouter()

# In-memory services (replace with Redis/DB-backed ones in production)
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service
)

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class ResetRequest(BaseModel):
    session_id: Optional[str] = None

async def get_or_create_sid(request: Request, response: Response, request_body: Optional[QueryRequest] = None) -> str:
    """Return a per-client sid; try request body first, then cookie, then create new."""
    sid = None
    if request_body and request_body.session_id:
        sid = request_body.session_id

    if not sid:
        sid = request.cookies.get("sid")

    if not sid:
        sid = str(uuid.uuid4())
        # Set cookie so the same client reuses the same session if they support cookies
        response.set_cookie(
            key="sid",
            value=sid,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30  # 30 days
        )

    # Ensure the session exists in our in-memory service
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=sid,
            session_id=sid,
            state={}
        )
    except Exception:
        # Likely already exists — ignore.
        pass

    return sid

@router.post("/query")
async def query(request_body: QueryRequest, request: Request, response: Response):
    # Manually call get_or_create_sid to pass request_body
    sid = await get_or_create_sid(request, response, request_body)

    try:
        msg = types.Content(role="user", parts=[types.Part(text=request_body.query)])

        async for event in runner.run_async(
            user_id=sid,
            session_id=sid,
            new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                return {"result": event.content.parts[0].text, "session_id": sid}

        return {"result": "No response", "session_id": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_session(request_body: ResetRequest, request: Request, response: Response):
    # For reset, we can't easily use the same QueryRequest body
    sid = request_body.session_id if request_body.session_id else request.cookies.get("sid")

    if not sid:
        return {"status": "no session to reset"}

    try:
        await session_service.delete_session(
            app_name=APP_NAME,
            user_id=sid,
            session_id=sid
        )
        # Start a fresh one
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=sid,
            session_id=sid,
            state={}
        )
        return {"status": "reset", "session_id": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
