from fastapi import FastAPI, HTTPException, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
import shutil
import os

from .core import OmniCore
from swarm.types import SwarmMessage

app = FastAPI(title="Omni Local API", version="0.9.0")
UPLOAD_DIR = os.path.expanduser("~/.omni/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ... (CORS logic same as before) ...
# CORS (Allow local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton Core
omni = OmniCore()
active_websockets: List[WebSocket] = []

# Hook Swarm Bus to WebSockets
def swarm_hook(msg: SwarmMessage):
    data = msg.to_json()
    # Broadcast to all connected clients
    # Note: This is synchronous, ideally use async queue
    for ws in active_websockets:
        asyncio.create_task(ws.send_text(data))

omni.bus.subscribe("broadcast", swarm_hook)
omni.bus.subscribe("user", swarm_hook)

# -- Data Models --
class ChatRequest(BaseModel):
    message: str
    brain: str = "None"

class ChatResponse(BaseModel):
    response: str

class VisionRequest(BaseModel):
    prompt: str = "Describe this image."

# -- Endpoints --

@app.get("/")
def read_root():
    return {"status": "Omni Online", "version": "v0.9.0"}

@app.get("/brains")
def list_brains():
    return {
        "installed": omni.get_installed_brains(),
        "available": omni.personas
    }

@app.post("/download")
def download_model():
    try:
        omni.download_model()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        resp = omni.run_inference(req.message, req.brain)
        return {"response": resp}
    except Exception as e:
        if "Model not installed" in str(e):
             raise HTTPException(status_code=404, detail="Model missing")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vision")
async def analyze_image(prompt: str = "Describe this", file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        description = omni.run_vision(file_path, prompt)
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        text = omni.run_transcription(file_path)
        return {"transcription": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            # Keep alive
            data = await websocket.receive_text()
            # Handle incoming WS commands if any
    except:
        active_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
