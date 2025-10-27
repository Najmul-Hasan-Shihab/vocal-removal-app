@echo off
echo Adding FFmpeg to System PATH...
echo.

REM Add WinGet Links folder to User PATH permanently
setx PATH "%PATH%;C:\Users\Shihab\AppData\Local\Microsoft\WinGet\Links"

echo.
echo FFmpeg has been added to your PATH!
echo.
echo IMPORTANT: You must restart your terminal windows for the change to take effect.
echo.
echo After restarting:
echo 1. Close all PowerShell windows
echo 2. Open a NEW PowerShell window
echo 3. Run: ffmpeg -version (to verify)
echo 4. Start your backend server again
echo.
pause
