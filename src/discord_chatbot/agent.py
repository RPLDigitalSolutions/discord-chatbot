from langchain_core.messages import SystemMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from discord_chatbot.config import NVIDIA_API_TOKEN, NVIDIA_MODEL_NAME
from discord_chatbot.memory import get_memory
from discord_chatbot.tools import open_in_new_tab, update_memory

def get_agent():
    llm = ChatNVIDIA(
        model=NVIDIA_MODEL_NAME,
        nvidia_api_key=NVIDIA_API_TOKEN,
        timeout=300,
    )
    tools = [open_in_new_tab, update_memory]
    checkpointer = MemorySaver()
    
    sys_prompt = """You are a helpful Discord chatbot.
You must use Discord markdown format for your responses.
DO NOT use tables, they are not supported in Discord.
Use standard markdown for bold, italic, lists, and code blocks.
DO NOT use emojis in your responses. Keep your tone natural.
You have a long term memory. Use the update_memory tool to save important information from the user on every request.
Here is your current memory:
{memory}
"""
    
    async def state_modifier(state):
        mem = await get_memory()
        messages = state["messages"]
        system_message = SystemMessage(content=sys_prompt.format(memory=mem))
        return [system_message] + messages

    agent = create_react_agent(llm, tools, prompt=state_modifier, checkpointer=checkpointer)
    return agent
