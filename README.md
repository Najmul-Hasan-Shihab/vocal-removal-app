# Vocal Removal App

A full-stack application for separating vocals from music using **Demucs**, a state-of-the-art AI-powered vocal separation model. Perfect for creating karaoke tracks!

## Features

- 🎤 **High-Quality Vocal Separation** - Uses Facebook Research's Demucs model
- 🎵 **Multiple Format Support** - Works with MP3, WAV, FLAC, and more
- 🚀 **Fast Processing** - Efficient vocal/instrumental separation
- 💻 **Easy to Use** - Simple web interface
- 📥 **Downloadable Results** - Get both vocal and instrumental tracks

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- Demucs - State-of-the-art music source separation
- Python 3.13

**Frontend:**
- React 18 - UI framework
- Vite - Build tool and dev server

## Prerequisites

- Python 3.11+
- Node.js 18+
- FFmpeg (required for audio processing)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/vocal-removal-app.git
cd vocal-removal-app
```

### 2. Install FFmpeg

FFmpeg is required for audio file processing.

**Windows:**
```bash
# Using winget (recommended)
winget install --id=Gyan.FFmpeg -e

# OR using Chocolatey
choco install ffmpeg -y

# OR run the included script
add-ffmpeg-to-path.bat
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Windows (if FFmpeg not in PATH):**
```bash
$env:Path = "C:\Users\YOUR_USERNAME\AppData\Local\Microsoft\WinGet\Links;" + $env:Path
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Usage

1. Open your browser to `http://localhost:5173`
2. Upload an audio file (MP3, WAV, etc.)
3. Click "Separate" to process
4. Wait for processing to complete (typically 30-60 seconds for a 3-4 minute song)
5. Download the separated vocals and instrumental tracks

## How It Works

1. **Upload**: Audio file is uploaded to the backend
2. **Conversion**: MP3 files are converted to WAV format
3. **Separation**: Demucs AI model separates vocals from instrumentals
4. **Output**: Two files are created:
   - `vocals.wav` - Isolated vocal track
   - `instrumental.wav` - Background music without vocals (perfect for karaoke!)

## Project Structure

```
vocal-removal-app/
├── backend/
│   ├── app.py              # FastAPI endpoints
│   ├── model.py            # Demucs separation logic
│   ├── requirements.txt    # Python dependencies
│   └── outputs/            # Temporary output files
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── UploadForm.jsx # Upload and download UI
│   │   └── main.jsx       # React entry point
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── .gitignore
└── README.md
```

## API Endpoints

### `POST /separate/`
Upload an audio file for vocal separation.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (audio file)

**Response:**
```json
{
  "vocals": "filename_vocals.wav",
  "instrumental": "filename_instrumental.wav"
}
```

### `GET /download/{filename}`
Download a processed audio file.

**Response:** Audio file (WAV format)

## Troubleshooting

### FFmpeg not found
- Make sure FFmpeg is installed and in your PATH
- On Windows, restart your terminal after installation
- Run `ffmpeg -version` to verify

### Processing timeout
- Large audio files (>10 minutes) may exceed the timeout
- Try shorter clips or increase timeout in `model.py`

### Out of memory
- Demucs requires significant RAM for processing
- Close other applications or use shorter audio clips

### CORS errors
- Make sure both backend and frontend are running
- Backend should be on port 8000, frontend on port 5173

## Performance Notes

- **First run**: Demucs downloads its AI model (~300MB) on first use
- **Processing time**: Typically 30-60 seconds for a 3-4 minute song
- **Quality**: Demucs produces professional-grade separation suitable for karaoke

## License

This project is for educational purposes. Demucs is released under the MIT license.

## Credits

- [Demucs](https://github.com/facebookresearch/demucs) - Music source separation by Facebook Research
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Vite](https://vitejs.dev/) - Next generation frontend tooling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues, please check the troubleshooting section or create an issue on GitHub.

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

### 2. Run the Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. Start both the backend and frontend servers
2. Open your browser to `http://localhost:5173`
3. Upload an audio file (MP3, WAV, etc.)
4. Click "Separate" to process the file
5. Download the separated vocals and instrumental tracks

## API Endpoints

- `POST /separate/` - Upload audio file for vocal separation
  - Request: multipart/form-data with `file` field
  - Response: JSON with `vocals` and `instrumental` filenames

- `GET /download/{filename}` - Download processed audio file
  - Response: WAV audio file

## Docker Deployment (Optional)

```bash
cd backend
docker build -t vocal-removal-backend .
docker run -p 8000:8000 -v $(pwd)/models:/app/models vocal-removal-backend
```

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**Model not found:**
- Verify the ONNX model is in `backend/models/` directory
- Check the filename matches what's specified in `app.py`

**CORS errors:**
- The backend is configured to allow requests from `localhost:3000` and `localhost:5173`
- If using a different port, update `app.py` CORS settings

### Frontend Issues

**Blank page:**
- Check browser console for errors
- Verify `npm install` completed successfully
- Ensure the backend is running

**Upload fails:**
- Verify backend is running on port 8000
- Check browser network tab for error details
- Ensure the audio file format is supported

## Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- ONNX Runtime - AI model inference
- librosa - Audio processing
- soundfile - Audio I/O

**Frontend:**
- React 18 - UI framework
- Vite - Build tool and dev server

## License

This project is for educational purposes.
