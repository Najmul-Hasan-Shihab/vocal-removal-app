@echo off
echo Installing FFmpeg...
echo.

REM Try winget first
echo Attempting installation with winget...
winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements

if %ERRORLEVEL% EQU 0 (
    echo.
    echo FFmpeg installed successfully!
    echo Please close this window and restart your backend server.
    echo.
    pause
    exit
)

echo.
echo Winget failed, trying Chocolatey...
choco install ffmpeg -y

if %ERRORLEVEL% EQU 0 (
    echo.
    echo FFmpeg installed successfully!
    echo Please close this window and restart your backend server.
    echo.
    pause
    exit
)

echo.
echo Automatic installation failed.
echo Please follow manual installation instructions in INSTALL_FFMPEG.md
echo.
pause
