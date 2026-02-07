"""
MCP Server entry point
Like Spring Boot's @SpringBootApplication
"""
import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent

# Use package-relative import so module runs with `python -m src.main`
from .tools import ToolRegistry, CalculatorToolHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_tools(server: Server):
    """
    Register all tools with the MCP server
    Like Spring's component scanning
    """
    logger.info("Setting up tools...")
    
    # Create registry
    registry = ToolRegistry()
    
    # Register all tool handlers
    registry.register(CalculatorToolHandler())
    # Add more handlers here as you create them:
    # registry.register(WeatherToolHandler())
    # registry.register(DatabaseToolHandler())
    
    logger.info(f"Registered tools: {registry.list_tool_names()}")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """
        List all available tools
        Called by MCP client to discover tools
        """
        logger.info("Client requested tool list")
        return registry.get_all_tools()
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """
        Execute a tool by name
        Routes requests to appropriate handler
        """
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        try:
            # Get handler from registry
            handler = registry.get_handler(name)
            
            # Execute tool
            result = await handler.execute(arguments)
            
            return result
        
        except ValueError as e:
            # Tool not found or validation error
            logger.error(f"Tool error: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Error: {str(e)}"
            )]
        
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error in tool execution: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"❌ Internal Error: {str(e)}"
            )]

async def main():
    """Main entry point"""
    logger.info("Starting MCP Calculator Server...")
    
    # Create MCP server
    server = Server("calculator-server")
    
    # Setup tools
    setup_tools(server)
    
    logger.info("✅ MCP Calculator Server ready!")
    logger.info("Available tools: calculate")
    
    # Run server (stdio transport)
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())