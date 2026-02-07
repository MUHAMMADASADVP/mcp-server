"""
Tool handlers - like Spring @RestController
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Tool input model (like DTO)
class CalculatorInput(BaseModel):
    operation: str
    a: float
    b: float

def setup_tools(server: Server):
    """Register all tools with the server"""
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available tools - like Spring's endpoint discovery"""
        return [
            Tool(
                name="calculate",
                description="Perform basic arithmetic operations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "The operation to perform"
                        },
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Execute tool - like Spring @RequestMapping handler"""
        
        if name == "calculate":
            # Validate input
            input_data = CalculatorInput(**arguments)
            
            # Business logic
            result = perform_calculation(
                input_data.operation,
                input_data.a,
                input_data.b
            )
            
            return [TextContent(
                type="text",
                text=f"Result: {result}"
            )]
        
        raise ValueError(f"Unknown tool: {name}")

def perform_calculation(operation: str, a: float, b: float) -> float:
    """Business logic - like a @Service method"""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }
    return operations[operation](a, b)
