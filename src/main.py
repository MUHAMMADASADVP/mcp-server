import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from src.handlers.tool_handler import setup_tools

async def main():
    # Create server
    server = Server("my-calculator-server")
    
    # Register tools (this is where setup_tools gets called)
    setup_tools(server)
    
    # Run server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())