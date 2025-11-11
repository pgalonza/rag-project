from langchain_core.utils.function_calling import convert_to_openai_tool
from typing import Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.tool import ToolMessage
from langchain_openai import ChatOpenAI
from flask import current_app, g
import os
import asyncio


_agent = None


async def init_agent():
    global _agent
    if _agent is None:
        chat_model = ChatOpenAI(
            model=current_app.config['LLM_MODEL_URL'],
            base_url=current_app.config['LLM_BASE_URL'],
            api_key=os.environ.get("YC_API_KEY"),
        )
        mcp_client = MultiServerMCPClient(current_app.config['MCP_SERVERS'])
        tools = await mcp_client.get_tools()
        _agent = create_agent(model=chat_model, tools=tools, system_prompt=current_app.config['ASSISTENT_ROLE'])
    return _agent

async def send_message(message):
    global _agent
    if _agent is None:
        init_agent()
    result = await _agent.ainvoke(message)
    answer_result = ""
    contents = [
        answer.content for answer in result['messages']
        if (isinstance(answer, AIMessage) or isinstance(answer, ToolMessage))
        and answer.content
    ]
    answer_result = "\n".join(contents)
    return answer_result
