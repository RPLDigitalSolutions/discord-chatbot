import asyncio
import json

import discord
from langchain_core.messages import HumanMessage

from discord_chatbot.agent import get_agent
from discord_chatbot.config import DISCORD_BOT_TOKEN
from discord_chatbot.utils import chunk_message


class ChatbotClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.agent = get_agent()

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def send_chunks(self, channel, content):
        chunks = chunk_message(content)
        for chunk in chunks:
            await channel.send(chunk)

    async def on_message(self, message):
        print(f"[LOG] Message from {message.author} in {message.channel}: {message.content}")
        
        if message.author == self.user:
            return

        context_text = ""
        if message.reference and isinstance(message.reference.resolved, discord.Message):
            context_text += f"Replying to: {message.reference.resolved.clean_content}\n\n"

        context_text += message.clean_content

        attachments_urls = []
        for att in message.attachments:
            attachments_urls.append(att.url)

        if attachments_urls:
            context_text += "\nAttachments:\n" + "\n".join(attachments_urls)

        config = {"configurable": {"thread_id": str(message.channel.id)}}
        inputs = {"messages": [HumanMessage(content=context_text)]}
        
        final_response = ""
        
        async with message.channel.typing():
            async for event in self.agent.astream(inputs, config=config, stream_mode="updates"):
                for node, data in event.items():
                    if node == "agent":
                        for agent_msg in data.get("messages", []):
                            if agent_msg.content:
                                final_response = agent_msg.content

            if final_response:
                await self.send_chunks(message.channel, final_response)

def run_bot():
    client = ChatbotClient()
    client.run(DISCORD_BOT_TOKEN)
