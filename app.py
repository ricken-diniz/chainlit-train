import os
import base64
from pathlib import Path

import httpx
import chainlit as cl

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llava:7b")
CHAT_URL = f"{OLLAMA_HOST}/api/chat"

@cl.on_message
async def on_message(message: cl.Message):
    
    images: list[str] = []
    for f in (message.elements or []):
        if f.mime and "image" in f.mime:
            b64 = base64.b64encode(Path(f.path).read_bytes()).decode("utf-8")
            images.append(b64)

    user_msg: dict = {"role": "user", "content": message.content}
    if images:
        user_msg["images"] = images

    payload = {
        "model":    OLLAMA_MODEL,
        "messages": [user_msg],
        "stream":   False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(CHAT_URL, json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            await cl.Message(
                content=f"❌ Ollama returned an error: {e.response.status_code}\n{e.response.text}"
            ).send()
            return
        except httpx.RequestError as e:
            await cl.Message(
                content=f"❌ Could not reach Ollama at `{OLLAMA_HOST}`: {e}"
            ).send()
            return

    data    = resp.json()
    content = data["message"]["content"]
    await cl.Message(content=content).send()
