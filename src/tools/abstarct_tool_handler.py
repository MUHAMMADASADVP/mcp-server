"""
Abstract Tool Handler & its methods
"""
from abc import ABC, abstractmethod
from mcp.types import Tool, TextContent
from typing import List


# Base interface (like Spring's Abstract Class)
class AbstractToolHandler(ABC):
    """Base class for all tool handlers"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Tool name"""
        pass
    
    @abstractmethod
    def get_tool_definition(self) -> Tool:
        """Return tool metadata"""
        pass
    
    @abstractmethod
    async def execute(self, arguments: dict) -> List[TextContent]:
        """Execute the tool"""
        pass