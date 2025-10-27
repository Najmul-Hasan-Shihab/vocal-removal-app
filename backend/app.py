from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from model import VocalSeparator
from tempfile import NamedTemporaryFile
import shutil
import asyncio
import json

app = FastAPI()

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

separator = VocalSeparator()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Vocal Removal API is running"}

@app.post("/separate/")
async def separate(file: UploadFile = File(...)):
    # save upload
    tmp = NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    try:
        content = await file.read()
        with open(tmp.name, "wb") as f:
            f.write(content)
        
        tmp.close()  # Close the file before processing

        # Preserve original filename (without extension) and add suffixes
        original_name = os.path.splitext(file.filename)[0]
        vocals_path = os.path.join("outputs", f"{original_name}_vocals.mp3")
        instrumental_path = os.path.join("outputs", f"{original_name}_instrumental.mp3")

        out_v, out_i = separator.separate(tmp.name, vocals_path, instrumental_path)

        # Return the file IDs for download
        return {
            "vocals": os.path.basename(out_v),
            "instrumental": os.path.basename(out_i),
            "original_name": original_name
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up the uploaded temp file
        try:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
        except PermissionError:
            # File might still be locked, ignore for now
            pass

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("outputs", filename)
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="audio/mpeg",
            filename=filename
        )
    return {"error": "File not found"}

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_progress(self, client_id: str, progress: int, message: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json({
                    "progress": progress,
                    "message": message
                })
            except:
                self.disconnect(client_id)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        # Keep connection alive and wait for messages
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)

@app.post("/separate/{client_id}")
async def separate_with_progress(client_id: str, file: UploadFile = File(...)):
    """Separate with progress updates via WebSocket"""
    tmp = NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    try:
        # Send initial progress
        await manager.send_progress(client_id, 0, "Uploading file...")
        
        content = await file.read()
        with open(tmp.name, "wb") as f:
            f.write(content)
        
        tmp.close()
        
        await manager.send_progress(client_id, 10, "File uploaded. Starting separation...")

        # Preserve original filename (without extension) and add suffixes
        original_name = os.path.splitext(file.filename)[0]
        vocals_path = os.path.join("outputs", f"{original_name}_vocals.mp3")
        instrumental_path = os.path.join("outputs", f"{original_name}_instrumental.mp3")

        # Run separation with progress callback
        out_v, out_i = await separator.separate_with_progress(
            tmp.name, 
            vocals_path, 
            instrumental_path,
            lambda prog, msg: asyncio.create_task(manager.send_progress(client_id, prog, msg))
        )

        await manager.send_progress(client_id, 100, "Separation complete!")

        # Return the file IDs for download
        return {
            "vocals": os.path.basename(out_v),
            "instrumental": os.path.basename(out_i),
            "original_name": original_name
        }
    except Exception as e:
        await manager.send_progress(client_id, -1, f"Error: {str(e)}")
        return {"error": str(e)}
    finally:
        # Clean up the uploaded temp file
        try:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
        except PermissionError:
            pass
