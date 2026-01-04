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
    return {"status": "ok", "mode": "faceless-video-backend-ai"}

@app.post("/generate")
def generate_video(req: VideoRequest):
    job_id = str(uuid.uuid4())

    system_prompt = (
        "You are a short-form video strategist for TikTok and YouTube Shorts. "
        "Create a viral, faceless video script with a strong hook, fast pacing, "
        "and clear beats."
    )

    user_prompt = f"""
Topic: {req.prompt}
Platform: {req.platform}

Return:
- Hook (1 sentence)
- 5 short beats (1 line each)
- Call to action
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    script = response.output_text

    return {
        "job_id": job_id,
        "status": "script_generated",
        "script": script
    }
