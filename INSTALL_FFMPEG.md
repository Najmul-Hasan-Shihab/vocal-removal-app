# Install FFmpeg for Windows

Your vocal removal app needs FFmpeg to process audio files. Follow these steps:

## Option 1: Using Chocolatey (Recommended - Easiest)

1. Open PowerShell as Administrator
2. Run: `choco install ffmpeg -y`
3. Restart your terminals (backend and frontend)

## Option 2: Manual Installation (If Chocolatey doesn't work)

1. **Download FFmpeg:**
   - Go to: https://github.com/BtbN/FFmpeg-Builds/releases
   - Download: `ffmpeg-master-latest-win64-gpl.zip`

2. **Extract the ZIP file:**
   - Extract to: `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH:**
   - Open "Edit the system environment variables" from Start menu
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\ffmpeg\bin`
   - Click "OK" on all windows

4. **Verify Installation:**
   - Open a NEW PowerShell window
   - Run: `ffmpeg -version`
   - You should see version information

5. **Restart your app:**
   - Stop the backend server (Ctrl+C)
   - Run: `cd backend; python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000`

## Option 3: Using Windows Package Manager (winget)

1. Open PowerShell
2. Run: `winget install ffmpeg`
3. Restart your terminals

## After Installation

Once FFmpeg is installed:
1. Restart your backend server
2. Upload an MP3 file
3. Click "Separate"
4. It should work! 🎵

## Troubleshooting

If it still doesn't work after installing FFmpeg:
- Make sure you opened a NEW terminal window after installation
- Verify FFmpeg is in PATH by running: `ffmpeg -version`
- Restart VS Code entirely
