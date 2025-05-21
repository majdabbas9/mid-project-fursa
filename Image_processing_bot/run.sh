#!/bin/bash
path_to_file=$1
llama_path=$2
if [ -z "$path_to_file" ]; then
    echo "You didn't give all the arguments"
    exit 1
fi

echo "Path to file: $path_to_file"

NGROK_PID=$(pgrep -f "ngrok http 5001")
if [ -z "$NGROK_PID" ]; then
    echo "Starting ngrok on port 5001..."
    nohup ngrok http 5001 > /dev/null 2>&1 &
    sed -i '/BOT_APP_URL=/d' $path_to_file/Image_processing_bot/.env
    sleep 3
else
    echo "ngrok already running (PID $NGROK_PID)"
    echo "running"
    cd $path_to_file
    .venv/bin/python -m Image_processing_bot.app
fi

# Step 2: Get ngrok public URL
BOT_APP_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo $BOT_APP_URL
sed -i '/BOT_APP_URL=/d' "$path_to_file"/Image_processing_bot/.env
sed -i '/MY_LLAMA_IP=/d' "$path_to_file"/Image_processing_bot/.env
echo "MY_LLAMA_IP=$llama_path" >> "$path_to_file"/Image_processing_bot/.env
echo "BOT_APP_URL=$BOT_APP_URL" >> "$path_to_file"/Image_processing_bot/.env
echo "running.."
sleep 2
cd $path_to_file
.venv/bin/python -m Image_processing_bot.app
