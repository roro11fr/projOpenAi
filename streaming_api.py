from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat/stream")
async def stream_chat(request: Request):
    body = await request.json()
    history = body.get("history", [])
    model = body.get("model", "gpt-3.5-turbo")

    messages = [{"role": "system", "content": "Ești un detectiv AI român care răspunde clar și logic."}] + history[-10:]

    def generate():
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True
            )
            for chunk in response:
                delta = chunk.choices[0].delta
                content = delta.content if delta and delta.content else ""
                if content:
                    yield content
        except Exception as e:
            yield f"[EROARE_BACKEND] {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")
