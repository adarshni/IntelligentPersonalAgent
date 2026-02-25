"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, Any


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    tool_used: Optional[str] = None
    tool_output: Optional[Any] = None
    thinking: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
