# First Step: Basic HTTP Client to MCP Server

# import requests

# URL = "http://localhost:8000/mcp"
# PAYLOAD = {
#     "jsonrpc": "2.0",
#     "method": "tools/list",
#     "params": {},
#     "id": 2
# }
# HEADER = {
#     "Content-Type": "application/json",
#     "Accept": "application/json, text/event-stream"
# }


# response = requests.post(URL, json=PAYLOAD, headers=HEADER, stream=True)

# for line in response.iter_lines():
#     if line:
#         print(line.decode('utf-8'))  # Decode bytes to string and print each line   




# Second Step: Context Management with AsyncContextManager
#-------------------------- Starting Session with AsyncExitStack



# from mcp.client.streamable_http import streamablehttp_client
# from mcp import ClientSession
# from contextlib import AsyncExitStack
# import asyncio

# class MCPClient:
#     def __init__(self, url):
#         self.url = url
#         self.stack = AsyncExitStack()
#         self._sess = None

#     async def list_tools(self):
#         async with self.session as session:
#             response = (await session.list_tools()).tools
#             return response

#     async def __aenter__(self):
#        read,write, _ = await self.stack.enter_async_context(
#             streamablehttp_client(self.url)
#         )
#        self._sess = await self.stack.enter_async_context(
#             ClientSession(read, write)
#         )
#        await self._sess.initialize()
#        return self

#     async def __aexit__(self, *args):
#            await self.stack.aclose()

#     async def list_tools(self):
#         return (await self._sess.list_tools()).tools
   
       


# async def main():
#     async with MCPClient("http://localhost:8000/mcp") as client:
#         tools = await client.list_tools()
#         print(tools, "Available tools:")
#         # for tool in tools:
#         #     print(tool)

# asyncio.run(main())     






# # ----------------------------- Third Step:





# from mcp.client.streamable_http import streamablehttp_client
# from mcp import ClientSession
# from contextlib import AsyncExitStack
# import asyncio

# class MCPClient:
#     def __init__(self, url):
#         self.url = url
#         self.stack = AsyncExitStack()
#         self._sess = None

#     async def __aenter__(self):
#         read, write, _ = await self.stack.enter_async_context(
#             streamablehttp_client(self.url)
#         )
#         self._sess = await self.stack.enter_async_context(
#             ClientSession(read, write)
#         )
#         await self._sess.initialize()
#         return self

#     async def __aexit__(self, *args):
#         await self.stack.aclose()

#     async def list_tools(self):
#         return (await self._sess.list_tools()).tools
    
#     async def call_tool(self, tool_name, *args, **kwargs):
#         return await self._sess.call_tool(tool_name, *args, **kwargs)


# async def main():
#     async with MCPClient("http://localhost:8000/mcp") as client:
#         tools = await client.list_tools()
#         print("Available tools:", tools)


# asyncio.run(main())



# Fourth Step: Using AsyncExitStack for Context Management
# ------------------------------------tool/list



# import types
# from mcp.client.streamable_http import streamablehttp_client
# from mcp import ClientSession
# from contextlib import AsyncExitStack
# import asyncio

# class MCPClient:
#     def __init__(self, url):
#         self.url = url
#         self.stack = AsyncExitStack()
#         self._sess = None

#     async def __aenter__(self):
#         read, write, _ = await self.stack.enter_async_context(
#             streamablehttp_client(self.url)
#         )
#         self._sess = await self.stack.enter_async_context(
#             ClientSession(read, write)
#         )
#         await self._sess.initialize()
#         return self

#     async def __aexit__(self, *args):
#         await self.stack.aclose()

#     async def list_tool_names(self):
#         tools = (await self._sess.list_tools()).tools
#         # Extract only the names
#         return [tool.name for tool in tools]
    
#     async def call_tool(self, tool_name: str, tool_input: dict) -> types.CallToolResult | None:
#      return await self.session().call_tool(tool_name, tool_input)

# async def main():
#     async with MCPClient("http://localhost:8000/mcp") as client:
#         tool_names = await client.list_tool_names()
#         print("Available tools:", tool_names)

# asyncio.run(main())





# ------------------------------------------tool/call



from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from mcp.types import CallToolResult  # ✅ Correct import
from contextlib import AsyncExitStack
import asyncio

class MCPClient:
    def __init__(self, url):
        self.url = url
        self.stack = AsyncExitStack()
        self._sess = None

    async def __aenter__(self):
        read, write, _ = await self.stack.enter_async_context(
            streamablehttp_client(self.url)
        )
        self._sess = await self.stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._sess.initialize()
        return self

    async def __aexit__(self, *args):
        await self.stack.aclose()

    async def list_tool_names(self):
        tools = (await self._sess.list_tools()).tools
        return [tool.name for tool in tools]  # ✅ Only names
    
    async def call_tool(self, tool_name: str, tool_input: dict) -> CallToolResult | None:
        return await self._sess.call_tool(tool_name, tool_input)  # ✅ Fixed _sess usage

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        # Example: Call a tool
        tool_call = await client.call_tool("get_greeting", {"name": "Alice"})
        print("Tool output:", tool_call.structuredContent)  # ✅ Accessing result directly

asyncio.run(main())
