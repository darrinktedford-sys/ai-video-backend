from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import os
import time
from openai import OpenAI, APIConnectionError, RateLimitError

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,   # important
)

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

    # 🔁 RETRY LOGIC (CRITICAL FOR RENDER FREE)
    attempts = 3
    for attempt in range(attempts):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            return {
                "job_id": job_id,
                "status": "scenes_generated",
                "content": response.output_text
            }

        except (APIConnectionError, RateLimitError) as e:
            if attempt == attempts - 1:
                raise HTTPException(
                    status_code=503,
                    detail="AI service temporarily unavailable. Please try again."
                )
            time.sleep(2)  # wait before retry
