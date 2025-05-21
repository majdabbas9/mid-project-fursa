#!/bin/bash
path_to_file=$1
telegram_token=$2
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
sudo apt-get update && sudo apt-get install -y libgl1
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
    # Recheck
    if command -v ngrok &> /dev/null
    then
        echo "✅ ngrok installed successfully."
    else
        echo "❌ ngrok installation failed."
        exit 1
    fi
fi
ngrok config add-authtoken 2wKSoZ02WAJ8woqkmFgjtmtqWxH_3h2hacC2fUcvcndDdMBzS
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
echo "TELEGRAM_BOT_TOKEN=$telegram_token" > "$env_file"
# Check if the virtual environment exists
if [ ! -d "$path_to_file/.venv" ]; then  # Check if .venv is a directory
    python3 -m venv "$path_to_file/.venv"
    "$path_to_file/.venv/bin/pip" install -r "$path_to_file/requirements.txt"
else
    echo "Virtual environment already exists."
fi