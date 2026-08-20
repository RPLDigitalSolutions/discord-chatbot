import aiohttp
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from urllib.parse import urljoin

@tool
async def open_in_new_tab(url: str) -> str:
    """Open a URL in a new tab, read its text content, and extract visible links for navigation."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                html = await response.text()
                
        soup = BeautifulSoup(html, "html.parser")
        
        for script in soup(["script", "style"]):
            script.extract()
            
        links = []
        for a in soup.find_all('a', href=True):
            link_text = a.get_text(strip=True)
            href = a['href']
            if link_text and href:
                full_url = urljoin(url, href)
                if full_url not in [l[1] for l in links]:
                    links.append((link_text, full_url))
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        page_text = "\n".join(chunk for chunk in chunks if chunk)
        
        output = f"--- PAGE TEXT ---\n{page_text[:10000]}\n\n--- LINKS FOUND ---\n"
        for text_val, link_val in links[:50]:
            output += f"- {text_val}: {link_val}\n"
            
        return output
    except Exception as e:
        return f"Error opening tab: {e!s}"

@tool
async def update_memory(information: str) -> str:
    """Save important information to long term memory."""
    from discord_chatbot.memory import append_memory
    await append_memory(information)
    return "Memory updated successfully."
