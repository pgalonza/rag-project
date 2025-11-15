from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.tool import ToolMessage
from langchain_openai import ChatOpenAI
from flask import current_app, g
import os
from typing import Any, List, Dict, Optional


_agent: Optional[Any] = None


async def init_agent() -> Any:
    global _agent
    if _agent is None:
        chat_model: ChatOpenAI = ChatOpenAI(
            model=current_app.config['LLM_MODEL_URL'],
            base_url=current_app.config['LLM_BASE_URL'],
            api_key=os.environ.get("YC_API_KEY"),
        )
        mcp_client: MultiServerMCPClient = MultiServerMCPClient(current_app.config['MCP_SERVERS'])
        tools: List[Any] = await mcp_client.get_tools()
        _agent = create_agent(model=chat_model, tools=tools, system_prompt=current_app.config['ASSISTENT_ROLE'])
    return _agent

async def send_message(message: Dict[str, List[Any]]) -> str:
    global _agent
    if _agent is None:
        await init_agent()
    result: Dict[str, Any] = await _agent.ainvoke(message)
    answer_result: str = ""
    contents: List[Any] = [
        answer.content for answer in result['messages']
        if (isinstance(answer, AIMessage) or isinstance(answer, ToolMessage))
        and answer.content
    ]
    answer_result = "\n".join(contents)
    return answer_result
