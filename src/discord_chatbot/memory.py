import os
import asyncio

MEMORY_FILE_PATH = "memory.md"
_memory_lock = asyncio.Lock()

async def get_memory() -> str:
    if not os.path.exists(MEMORY_FILE_PATH):
        return ""
    
    def read_file():
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()
            
    async with _memory_lock:
        return await asyncio.to_thread(read_file)

async def append_memory(content: str) -> None:
    def append_file():
        with open(MEMORY_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{content}")
            
    async with _memory_lock:
        await asyncio.to_thread(append_file)
