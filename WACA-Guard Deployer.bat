@echo off
set "python_exe=%ProgramFiles%\Python\python.exe"
set "python_scripts=%ProgramFiles%\Python\Scripts"

echo Checking if Python is installed...
if not exist "%python_exe%" (
    echo Python not found. Downloading and installing the latest version...
    powershell -Command "$latestPython = (Invoke-WebRequest -Uri 'https://www.python.org/downloads/windows/' -UseBasicParsing).Links | Where-Object { $_.href -match 'python-[\d]+(\.[\d]+)+-amd64.msi' } | Select-Object -First 1 -ExpandProperty href; Invoke-WebRequest -Uri $latestPython -OutFile '%TEMP%\python-latest.amd64.msi'"
    msiexec /i "%TEMP%\python-latest.amd64.msi" /qn ADDLOCAL=ALL DEFAULTALLUSERS=1 TARGETDIR="%ProgramFiles%\Python" /log "%TEMP%\PythonInstaller.log"
    echo Python installed successfully.
    echo.
) else (
    echo Python is already installed.
    echo.
)

echo Adding Python to PATH...
setx /M PATH "%PATH%;%python_scripts%"
echo Python added to PATH.
echo.

echo Installing required packages...
"%python_scripts%\pip" install --upgrade pip
"%python_scripts%\pip" install chat-exporter regex asyncio python-Levenshtein aiofiles numpy iris scikit-learn fuzzywuzzy disnake[voice] SpeechRecognition Pydub
echo.
echo All required packages have been installed.

:ask_run_WACA
echo.
set /P user_input="Would you like to run WACA-Guard now? (Y/N): "
if /I "%user_input%"=="Y" (
    if exist "%~dp0WACA-Guard 2.0.py" (
        echo Running WACA-Guard...
        "%python_exe%" "%~dp0WACA-Guard 2.0.py"
    ) else (
        echo Error: WACA-Guard 2.0.py not found in the same directory as the installer.
        echo Please ensure the WACA-Guard 2.0.py file is located in the same directory as this batch file and try again.
    )
) else if /I "%user_input%"=="N" (
    echo WACA-Guard will not be run.
) else (
    echo Invalid input. Please enter Y or N.
    goto ask_run_WACA
)

echo.
pause
