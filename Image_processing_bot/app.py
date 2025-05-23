import flask
from flask import request
import os
from Image_processing_bot.bot import Bot,Image_processingBot
from dotenv import load_dotenv

app = flask.Flask(__name__)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_APP_URL = os.getenv('BOT_APP_URL')


@app.route('/', methods=['GET'])
def index():
    return 'Ok'


@app.route(f'/{TELEGRAM_BOT_TOKEN}/', methods=['POST'])
def webhook():
    try:
        req = request.get_json(force=True)
        if 'message' in req:
            bot.handle_message(req['message'])
        return 'OK', 200  # ✅ Always return 200 to Telegram to mark as handled
    except Exception as e:
        # Log the exception for debugging but still return 200 to Telegram
        print(f"Error in webhook: {e}")
        return 'OK', 200  # ✅ Always return 200 to Telegram to mark as handled



if __name__ == "__main__":
    bot = Image_processingBot(TELEGRAM_BOT_TOKEN, BOT_APP_URL)
    app.run(host='0.0.0.0', port=5001)
