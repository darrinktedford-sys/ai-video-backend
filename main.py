from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    prompt: str
    platform: str = "both"

@app.get("/")
def root():
    return {"status": "ok", "mode": "faceless-video-backend-scenes"}

@app.post("/generate")
def generate_video(req: VideoRequest):
    job_id = str(uuid.uuid4())

    system_prompt = (
        "You are an expert faceless short-form video creator. "
        "You create viral scripts AND visual scene descriptions. "
        "Visuals must not include people or faces."
    )

    user_prompt = f"""
Topic: {req.prompt}
Platform: {req.platform}

Return exactly in this format:

HOOK:
<one sentence>

BEATS:
1. <beat text> | VISUAL: <faceless visual description>
2. <beat text> | VISUAL: <faceless visual description>
3. <beat text> | VISUAL: <faceless visual description>
4. <beat text> | VISUAL: <faceless visual description>
5. <beat text> | VISUAL: <faceless visual description>

CTA:
<call to action>
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.output_text

    return {
        "job_id": job_id,
        "status": "scenes_generated",
        "content": content
    }
