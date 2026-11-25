"""OpenAI-compatible API adapter for external tooling and clients."""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.modules.legal_assistant.schemas import LegalAskRequest
from app.modules.legal_assistant.service import LegalAssistantService

router = APIRouter(tags=["OpenAI Compatibility"])


class ChatMessage(BaseModel):
    role: str = "user"
    content: str = ""


class ChatCompletionRequest(BaseModel):
    model: str = "nyayasetu-legal-assistant"
    messages: List[ChatMessage] = Field(default_factory=list)
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


def _get_available_models() -> List[Dict[str, Any]]:
    active_groq_model = settings.GROQ_LLM_MODEL or "qwen/qwen3.8-27b"
    active_gemini_model = settings.GEMINI_LLM_MODEL or "gemini-2.5-flash"
    now_ts = int(time.time())

    return [
        {
            "id": "nyayasetu-legal-assistant",
            "object": "model",
            "created": now_ts,
            "owned_by": "nyayasetu",
            "permission": [],
            "root": "nyayasetu-legal-assistant",
            "parent": None,
        },
        {
            "id": active_groq_model,
            "object": "model",
            "created": now_ts,
            "owned_by": "groq",
            "permission": [],
            "root": active_groq_model,
            "parent": None,
        },
        {
            "id": active_gemini_model,
            "object": "model",
            "created": now_ts,
            "owned_by": "google",
            "permission": [],
            "root": active_gemini_model,
            "parent": None,
        },
    ]


@router.get("/models", summary="List OpenAI-compatible Models")
async def list_models() -> Dict[str, Any]:
    """Returns available model identifiers compatible with OpenAI clients."""
    return {
        "object": "list",
        "data": _get_available_models(),
    }


@router.get("/models/{model_id}", summary="Get Model Details")
async def get_model(model_id: str) -> Dict[str, Any]:
    """Returns details for a specific model ID."""
    models = _get_available_models()
    for m in models:
        if m["id"] == model_id:
            return m
    return {
        "id": model_id,
        "object": "model",
        "created": int(time.time()),
        "owned_by": "nyayasetu",
        "permission": [],
        "root": model_id,
        "parent": None,
    }


@router.post("/chat/completions", summary="OpenAI-compatible Chat Completions")
async def create_chat_completion(
    payload: ChatCompletionRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Accepts OpenAI chat completions payload and returns grounded legal assistant response."""
    user_query = ""
    for msg in reversed(payload.messages):
        if msg.role == "user" and msg.content.strip():
            user_query = msg.content.strip()
            break

    if not user_query and payload.messages:
        user_query = payload.messages[-1].content.strip()

    if not user_query:
        user_query = "Hello"

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    ask_req = LegalAskRequest(query=user_query, max_sources=5)
    answer_res = await LegalAssistantService.ask(
        db=db,
        payload=ask_req,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    content = answer_res.answer
    prompt_tokens = len(user_query.split())
    completion_tokens = len(content.split())

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
