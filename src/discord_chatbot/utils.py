def chunk_message(message: str, chunk_size: int = 1900) -> list[str]:
    chunks = []
    current_chunk = ""
    lines = message.split("\n")

    for line in lines:
        if len(current_chunk) + len(line) + 1 > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            while len(line) > chunk_size:
                chunks.append(line[:chunk_size])
                line = line[chunk_size:]
                
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return [c.strip() for c in chunks if c.strip()]
