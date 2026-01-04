from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

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
    return {"status": "ok", "mode": "faceless-video-backend"}

@app.post("/generate")
def generate_video(req: VideoRequest):
    job_id = str(uuid.uuid4())
    return {
        "job_id": job_id,
        "status": "accepted",
        "prompt": req.prompt,
        "platform": req.platform
    }
