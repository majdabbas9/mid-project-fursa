#!/bin/bash
path_to_file=$1
telegram_token=$2
# Check if Python 3 is installed
if command -v python3 &> /dev/null
then
    echo "✅ Python 3 is already installed."
else
    echo "⬇️ Python 3 not found. Installing now..."
    sudo apt update && sudo apt install python3
fi
########################################################################################################################
# Check if venv is available
if python3 -m venv --help &> /dev/null
then
    echo "✅ venv module is available."
else
    echo "⬇️ venv module not found. Installing python3-venv..."
    sudo apt install python3-venv
fi
########################################################################################################################
## --- Check pip ---
#if command -v pip3 &> /dev/null
#then
#    echo "✅ pip3 is already installed."
#else
#    echo "⬇️ Installing pip3..."
#    sudo apt install  python3-pip
#fi
########################################################################################################################
# Check if ngrok is installed
if command -v ngrok &> /dev/null
then
    echo "✅ ngrok is already installed."
else
    echo "⬇️ ngrok not found. Installing now..."

    # Install ngrok
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | sudo tee /etc/apt/sources.list.d/ngrok.list \
    && sudo apt update \
    && sudo apt install -y ngrok
    $$ ngrok config add-authtoken 2wKSoZ02WAJ8woqkmFgjtmtqWxH_3h2hacC2fUcvcndDdMBzS
    # Recheck
    if command -v ngrok &> /dev/null
    then
        echo "✅ ngrok installed successfully."
    else
        echo "❌ ngrok installation failed."
        exit 1
    fi
fi
########################################################################################################################
# Check if ollama is installed
if command -v ollama &> /dev/null
then
    echo "✅ Ollama is already installed."
else
    echo "⬇️ Ollama not found. Installing now..."
    curl -fsSL https://ollama.com/install.sh | sh

    # Recheck if installation succeeded
    if command -v ollama &> /dev/null
    then
        echo "✅ Ollama installed successfully."
    else
        echo "❌ Ollama installation failed."
        exit 1
    fi
fi
ollama pull gemma3:1b
sudo cp DeepPicBot.service /etc/systemd/system/

# reload daemon and restart the service
sudo systemctl daemon-reload
sudo systemctl restart DeepPicBot.service
sudo systemctl enable DeepPicBot.service
sudo systemctl start DeepPicBot.service
if ! systemctl is-active --quiet DeepPicBot.service; then
  echo "❌ DeepPicBot.service is not running."
  sudo systemctl status DeepPicBot.service --no-pager
  exit 1
fi

env_file="$path_to_file/Image_processing_bot/.env"
echo "$path_to_file"
echo "TELEGRAM_BOT_TOKEN=$telegram_token" > "$env_file"
if [ ! -f "$env_file" ]; then
    echo ".env file does NOT exist — creating it now."
    echo "TELEGRAM_BOT_TOKEN=$telegram_token" > "$env_file"

    echo ".env file created and token added."
else
    echo ".env file already exists."
fi

# Check if the virtual environment exists
if [ ! -d "$path_to_file/.venv" ]; then  # Check if .venv is a directory
    python3 -m venv "$path_to_file/.venv"
    "$path_to_file/.venv/bin/pip" install -r "$path_to_file/requirements.txt"
else
    echo "Virtual environment already exists."
fi