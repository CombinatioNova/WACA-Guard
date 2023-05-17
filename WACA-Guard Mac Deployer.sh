#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python not found. Downloading and installing the latest version..."
    curl -L -o /tmp/python-latest.pkg "https://www.python.org/ftp/python/latest/python-latest.pkg"
    sudo installer -pkg /tmp/python-latest.pkg -target /
    echo "Python installed successfully."
else
    echo "Python is already installed."
fi

echo "Installing required packages..."
python3 -m ensurepip --default-pip --user
python3 -m pip install --upgrade pip --user
python3 -m pip install --user chat-exporter asyncio python-Levenshtein aiofiles numpy iris scikit-learn fuzzywuzzy disnake[voice]
echo "All required packages have been installed."

read -p "Would you like to run WACA-Guard now? (Y/N): " user_input
if [[ "$user_input" =~ ^[Yy]$ ]]; then
    if [[ -f "$(dirname "$0")/WACA-Guard 2.0.py" ]]; then
        echo "Running WACA-Guard..."
        python3 "$(dirname "$0")/WACA-Guard 2.0.py"
    else
        echo "Error: WACA-Guard 2.0.py not found in the same directory as the installer."
        echo "Please ensure the WACA-Guard 2.0.py file is located in the same directory as this script and try again."
    fi
elif [[ "$user_input" =~ ^[Nn]$ ]]; then
    echo "WACA-Guard will not be run."
else
    echo "Invalid input. Please enter Y or N."
fi
