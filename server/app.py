from fastapi import FastAPI, HTTPException, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import shutil
import os

from .core import OmniCore
from swarm.types import SwarmMessage

app = FastAPI(title="Omni Local API", version="1.0.0")
UPLOAD_DIR = os.path.expanduser("~/.omni/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

omni = OmniCore()
active_websockets: List[WebSocket] = []

def swarm_hook(msg: SwarmMessage):
    data = msg.to_json()
    for ws in active_websockets:
        asyncio.create_task(ws.send_text(data))

omni.bus.subscribe("broadcast", swarm_hook)
omni.bus.subscribe("user", swarm_hook)

class ChatRequest(BaseModel):
    message: str
    brain: str = "None"

class ChatResponse(BaseModel):
    response: Dict[str, Any]

class SpeakRequest(BaseModel):
    text: str

class PilotRequest(BaseModel):
    instruction: str
    
class RunRequest(BaseModel):
    filename: str
    language: str

@app.get("/")
def read_root():
    return {"status": "Omni Online", "version": "v1.0.0"}

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
        # Returns { text: "...", artifacts: [...] }
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

@app.post("/speak")
async def speak_text(req: SpeakRequest):
    try:
        output_path = os.path.join(UPLOAD_DIR, "speech_out.wav")
        omni.run_tts(req.text, output_path)
        return FileResponse(output_path, media_type="audio/wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pilot")
async def run_pilot(req: PilotRequest):
    try:
        result = omni.run_pilot_action(req.instruction)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute")
async def execute_code(req: RunRequest):
    try:
        if req.language in ["python", "py"]:
            res = omni.executor._run_python(req.filename)
        elif req.language in ["bash", "sh"]:
            res = omni.executor._run_bash(req.filename)
        else:
            res = "Unsupported language."
        return {"status": "executed", "log": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lock for inference to prevent concurrent access to Metal resources
inference_lock = asyncio.Lock()

@app.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json() # { message, brain }
        prompt = data.get("message")
        brain = data.get("brain", "None")
        
        print(f"[CHAT] Prompt: {prompt} | Brain: {brain}") # LOGGING ADDED
        
        # Accumulate full text for final processing (saving)
        full_response = ""
        
        # Acquire Lock
        async with inference_lock:
            # Stream Tokens
            for token in omni.stream_generate(prompt, brain):
                if token.startswith("__BRAIN__:"):
                    # Send Brain Update Event
                    new_brain = token.split(":", 1)[1]
                    await websocket.send_json({"type": "brain_update", "brain": new_brain})
                    continue
                    
                full_response += token
                await websocket.send_json({"type": "token", "content": token})
                await asyncio.sleep(0.001) # Yield to event loop
            
        # Post-Processing (Save Artifacts)
        # We process the FULL text at the end to extract files cleanly
        processed = omni.executor.process(full_response)
        
        # Send Artifacts Metadata
        if processed.get("artifacts"):
            await websocket.send_json({"type": "artifacts", "data": processed["artifacts"]})
            
        await websocket.send_json({"type": "done"})
        
    except Exception as e:
        print(f"WS Error: {e}")
        await websocket.send_json({"type": "error", "content": str(e)})
    finally:
        await websocket.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_websockets.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
