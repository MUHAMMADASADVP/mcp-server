#!/usr/bin/env python3
"""Test MCP server using the mcp library's built-in stdio client.

This uses the official MCP client transport, which handles framing correctly.
"""
import subprocess
import asyncio
import os
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.server.lowlevel import StdioServerParameters

PYTHON_BIN = os.path.expanduser("/Users/asadvp/My-MCP-Server/venv/bin/python")
CWD = os.path.expanduser("/Users/asadvp/My-MCP-Server")

async def main():
    # Create server parameters
    server = StdioServerParameters(
        command=PYTHON_BIN,
        args=["-m", "src.main"]
    )
    
    # Connect to server via stdio
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            print("Initializing...")
            await session.initialize()
            
            # List tools
            print("Listing tools...")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Call the calculate tool
            print("\nCalling calculate (add 10 + 5)...")
            result = await session.call_tool(
                "calculate",
                {"operation": "add", "a": 10, "b": 5}
            )
            
            print(f"Result: {result}")
            print(f"Content: {result.content[0].text if result.content else 'No content'}")

if __name__ == '__main__':
    asyncio.run(main())
