"""
Main FastAPI Application Module.
Entry point for the Agent Demo backend API.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.agent_service import get_agent_service, AgentService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes resources on startup and cleans up on shutdown.
    """
    # Startup
    logger.info("Starting Agent Demo Backend...")
    
    # Validate configuration
    if not settings.validate():
        logger.warning("Azure OpenAI configuration is incomplete. Please check your .env file.")
    else:
        logger.info("Configuration validated successfully.")
        # Pre-initialize the agent service
        try:
            get_agent_service()
            logger.info("Agent service pre-initialized.")
        except Exception as e:
            logger.error(f"Failed to pre-initialize agent service: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agent Demo Backend...")


# Create FastAPI application
app = FastAPI(
    title="Intelligent Personal Agent API",
    description="A demo API for an Agentic AI system using LangChain and Azure OpenAI",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "message": "Intelligent Personal Agent API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    config_valid = settings.validate()
    return {
        "status": "healthy" if config_valid else "degraded",
        "configuration_valid": config_valid,
        "azure_endpoint_configured": bool(settings.AZURE_OPENAI_ENDPOINT),
        "api_key_configured": bool(settings.AZURE_OPENAI_API_KEY),
        "deployment_configured": bool(settings.AZURE_OPENAI_DEPLOYMENT_NAME),
    }


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Process a chat message through the AI agent.
    
    Args:
        request: ChatRequest containing the user's message.
    
    Returns:
        ChatResponse with the agent's response and tool execution info.
    
    Raises:
        HTTPException: If agent processing fails.
    """
    logger.info(f"Received chat request: {request.message[:100]}...")
    
    try:
        # Get the agent service
        agent = get_agent_service()
        
        # Process the message
        result = await agent.process_message(request.message)
        
        return ChatResponse(
            response=result["response"],
            tool_used=result.get("tool_used"),
            tool_output=result.get("tool_output"),
            thinking=result.get("thinking"),
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Agent service is not properly configured. Please check Azure OpenAI settings."
        )
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.post("/clear-history", tags=["Chat"])
async def clear_history():
    """Clear the chat history."""
    try:
        agent = get_agent_service()
        agent.clear_history()
        return {"status": "success", "message": "Chat history cleared"}
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools", tags=["Tools"])
async def list_tools():
    """List all available tools."""
    from app.tools import ALL_TOOLS
    
    tools_info = []
    for tool in ALL_TOOLS:
        tools_info.append({
            "name": tool.name,
            "description": tool.description,
        })
    
    return {"tools": tools_info}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
