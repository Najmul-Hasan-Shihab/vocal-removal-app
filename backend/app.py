from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from model import VocalSeparator
from tempfile import NamedTemporaryFile
import shutil

app = FastAPI()

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:5173",
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

        # Use unique filenames based on temp file
        base_name = os.path.basename(tmp.name)
        vocals_path = os.path.join("outputs", f"{base_name}_vocals.wav")
        instrumental_path = os.path.join("outputs", f"{base_name}_instrumental.wav")

        out_v, out_i = separator.separate(tmp.name, vocals_path, instrumental_path)

        # Return the file IDs for download
        return {
            "vocals": os.path.basename(out_v),
            "instrumental": os.path.basename(out_i)
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
            media_type="audio/wav",
            filename=filename
        )
    return {"error": "File not found"}
