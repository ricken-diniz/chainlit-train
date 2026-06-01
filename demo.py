import chainlit as cl
import ollama
import base64
from pathlib import Path

@cl.on_message
async def on_message(message: cl.Message):

    images = []
    for f in (message.elements or []):
        if "image" in f.mime:
            b64 = base64.b64encode(Path(f.path).read_bytes()).decode("utf-8")
            images.append(b64)

    user_message = {"role": "user", "content": message.content}
    if images:
        user_message["images"] = images

    msg = cl.Message(content="")

    response = ollama.chat(
        model="llama3.2-vision:11b-instruct-q4_K_M",
        messages=[user_message],
        stream=False,
    )

    await cl.Message(content=response["message"]["content"]).send()