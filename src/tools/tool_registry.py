"""
Tool registry - manages all tool handlers
Like Spring's ApplicationContext
"""
from typing import Dict
from . import AbstractToolHandler
from mcp.types import Tool
import logging

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Central registry for all tool handlers"""
    
    def __init__(self):
        self.handlers: Dict[str, ToolHandler] = {}
        logger.info("Tool registry initialized")
    
    def register(self, handler: ToolHandler) -> None:
        """Register a new tool handler"""
        name = handler.get_name()
        
        if name in self.handlers:
            raise ValueError(f"Tool '{name}' already registered")
        
        self.handlers[name] = handler
        logger.info(f"✅ Registered tool: {name}")
    
    def get_all_tools(self) -> list[Tool]:
        """Get all tool definitions for MCP client"""
        return [
            handler.get_tool_definition() 
            for handler in self.handlers.values()
        ]
    
    def get_handler(self, name: str) -> ToolHandler:
        """Get a specific tool handler by name"""
        if name not in self.handlers:
            available = ", ".join(self.handlers.keys())
            raise ValueError(
                f"Unknown tool: '{name}'. Available tools: {available}"
            )
        return self.handlers[name]
    
    def list_tool_names(self) -> list[str]:
        """Get list of all registered tool names"""
        return list(self.handlers.keys())


# Setup function
def setup_tools(server: Server):
    """Register all tools - like Spring Boot's component scanning"""
    
    # Create registry
    registry = ToolRegistry()
    
    # Register all handlers (like @ComponentScan)
    registry.register(CalculatorToolHandler())
    registry.register(WeatherToolHandler())
    # Add more handlers here...
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return registry.get_all_tools()
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            handler = registry.get_handler(name)
            return await handler.execute(arguments)
        except ValueError as e:
            logger.error(f"Tool error: {e}")
            return [TextContent(type="text", text=f"Error: {str(e)}")]
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return [TextContent(type="text", text=f"Internal error: {str(e)}")]