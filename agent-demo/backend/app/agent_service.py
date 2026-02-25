"""
Agent Service Module.
Handles the LangChain Agent creation and execution using LangGraph.
"""

import logging
import warnings
from typing import Dict, Any, Optional

# Suppress Pydantic V1 warning for Python 3.14
warnings.filterwarnings("ignore", message=".*Pydantic V1.*")

from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

from app.config import settings
from app.tools import ALL_TOOLS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AgentService:
    """
    Service class for managing the LangChain Agent.
    Handles agent initialization, execution, and response formatting.
    Uses LangGraph's ReAct agent for tool calling.
    """

    def __init__(self):
        """Initialize the Agent Service with Azure OpenAI and tools."""
        self.llm: Optional[AzureChatOpenAI] = None
        self.agent = None
        self.chat_history: list = []
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize the LangChain agent with Azure OpenAI."""
        if not settings.validate():
            logger.error("Azure OpenAI settings are not properly configured!")
            raise ValueError("Missing Azure OpenAI configuration. Please check your .env file.")

        logger.info("Initializing Azure OpenAI LLM...")
        
        # Initialize Azure OpenAI Chat Model
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
            max_tokens=1000,
        )

        # System prompt for the agent
        system_prompt = """You are a helpful AI assistant with access to various tools. 
Use the tools when appropriate to help answer user questions.

Available tools:
- calculate_sum: Sum a list of numbers
- convert_currency: Convert between USD, EUR, and INR
- get_current_date: Get current date and time
- get_weather: Get weather for Bangalore, Berlin, or New York
- search_web: Search the web for information

Always explain what you're doing and provide clear, helpful responses.
After using a tool, summarize the result in a user-friendly way."""

        # Create the ReAct agent using LangGraph
        self.agent = create_react_agent(
            model=self.llm,
            tools=ALL_TOOLS,
            prompt=system_prompt,
        )

        logger.info("Agent initialized successfully!")

    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process a user message through the agent.

        Args:
            message: The user's input message.

        Returns:
            Dictionary containing response, tool info, and thinking process.
        """
        logger.info(f"Processing message: {message}")

        try:
            # Build messages with history
            messages = self.chat_history + [HumanMessage(content=message)]
            
            # Execute the agent
            result = await self.agent.ainvoke({"messages": messages})

            # Extract response and tool usage from the result
            response_text = ""
            tool_used = None
            tool_output = None
            thinking = None
            
            # Process the messages in the result
            output_messages = result.get("messages", [])
            
            for msg in output_messages:
                # Check for tool calls (AI message with tool calls)
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_used = tool_call.get('name', tool_call.get('type', 'unknown'))
                        thinking = f"Decided to use '{tool_used}' with input: {tool_call.get('args', {})}"
                
                # Check for tool messages (tool outputs)
                if msg.type == "tool":
                    tool_output = msg.content
                
                # Get the final AI response
                if msg.type == "ai" and msg.content and not hasattr(msg, 'tool_calls'):
                    response_text = msg.content
                elif msg.type == "ai" and msg.content:
                    # AI message with content (might be final response)
                    response_text = msg.content

            # If no clean response found, get the last AI message content
            if not response_text:
                for msg in reversed(output_messages):
                    if msg.type == "ai" and msg.content:
                        response_text = msg.content
                        break
            
            if not response_text:
                response_text = "I apologize, but I couldn't process your request."

            # Update chat history
            self.chat_history.append(HumanMessage(content=message))
            self.chat_history.append(AIMessage(content=response_text))
            
            # Keep chat history manageable (last 10 exchanges)
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]

            logger.info(f"Response generated. Tool used: {tool_used}")
            
            return {
                "response": response_text,
                "tool_used": tool_used,
                "tool_output": tool_output,
                "thinking": thinking,
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "tool_used": None,
                "tool_output": None,
                "thinking": None,
            }

    def clear_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []
        logger.info("Chat history cleared")


# Global agent service instance
agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """
    Get or create the global agent service instance.
    
    Returns:
        The AgentService instance.
    """
    global agent_service
    if agent_service is None:
        agent_service = AgentService()
    return agent_service
