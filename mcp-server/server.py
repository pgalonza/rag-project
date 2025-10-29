import os
from typing import Annotated
from fastmcp import FastMCP, Context
import requests
from starlette.responses import JSONResponse
from fastmcp.utilities.logging import get_logger

server_logger = get_logger(name="fastmcp.server")

mcp = FastMCP(
    name='Retrieval-Augmented Generation adapter for vector database',
    instructions='A server for interacting with the Retrieval-Augmented Generation project',
    version='1.0'
)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(_):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})

@mcp.tool
async def search_documents(query: Annotated[str, "query to search documents"], ctx: Context) -> str:
    """Function to search documents by query in vector database and return result with Retrieval-Augmented Generation"""

    await ctx.info("Starting searching documents")
    server_logger.info("Searching documents by query: %s", query)

    result = requests.get(os.environ['RAG_URL'], params={'prompt':query}, timeout=20)

    return result.json()['text']


if __name__ == '__main__':
    mcp.run()
