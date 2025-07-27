from fastapi import APIRouter, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from core.agent import root_agent
import uuid

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

async def get_or_create_sid(request: Request, response: Response) -> str:
    """Return a per-client sid stored in a cookie; create session if new."""
    sid = request.cookies.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
        # Create a brand-new session for this sid
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=sid,
            session_id=sid,
            state={}
        )
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
        # If the app restarts, the cookie may exist but the in-memory session won't.
        # Ensure the session exists (best-effort).
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

        msg = types.Content(role="user", parts=[types.Part(text=request_body.query)])

        async for event in runner.run_async(
            user_id=sid,
            session_id=sid,
            new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                return {"result": event.content.parts[0].text}

        return {"result": "No response"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: allow a client to wipe its own session/history
@router.post("/reset")
async def reset_session(request: Request, response: Response, sid: str = Depends(get_or_create_sid)):
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
        return {"status": "reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
