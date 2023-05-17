@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

set LOG_DIR=ErrorLogs
mkdir %LOG_DIR% 2>nul

set "LOG_FILE=%LOG_DIR%\%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%.log"

rem Detect if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo Python not installed, installing now...
    rem Download and install Python
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe' -OutFile 'python-installer.exe'"
    if errorlevel 1 (
        echo Error downloading Python installer, please install manually. >> %LOG_FILE%
        goto end
    )
    python-installer.exe /passive InstallAllUsers=1 PrependPath=1
    if errorlevel 1 (
        echo Error installing Python, please check the log and try again. >> %LOG_FILE%
        goto end
    )
    del python-installer.exe
) else (
    echo Python is installed.
)

rem Check if Python is in PATH
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not in PATH, adding to PATH now.
    setx /M PATH "C:\Python310\;%PATH%"
    if errorlevel 1 (
        echo Error adding Python to PATH, please check the log and try again. >> %LOG_FILE%
        goto end
    )
)

echo Installing required packages...
python -m pip install chat-exporter regex asyncio python-Levenshtein aiofiles numpy iris scikit-learn fuzzywuzzy disnake[voice] SpeechRecognition Pydub
if errorlevel 1 (
    echo Error installing packages, please check the log and try again. >> %LOG_FILE%
    echo To manually install the packages, run:
    echo python -m pip install chat-exporter regex asyncio python-Levenshtein aiofiles numpy iris scikit-learn fuzzywuzzy disnake[voice] SpeechRecognition Pydub
    goto end
)

echo Dependencies installed successfully.

echo Verifying files are in proper positions...
rem Add your file validation logic here, or remove this section if not needed

echo Do you want to run WACA-Guard 2.0.py now? (Y/N)
set /p RUN_WACA=
if /i %RUN_WACA% EQU Y (
    echo Running WACA-Guard 2.0.py
    start python WACA-Guard 2.0.py
) else (
    echo Exiting.
)

:end
pause
