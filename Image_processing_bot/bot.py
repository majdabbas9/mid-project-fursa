import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from collections import defaultdict
import re
import requests
import cv2

from Image_processing_bot.generate_filter import generate_code
class Bot:
    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_help(self, chat_id, help_text):
        self.telegram_bot_client.send_message(chat_id, help_text, parse_mode="HTML")

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        file_name = 'img.'+file_info.file_path.split('.')[-1]
        folder_name = 'Image_processing_bot/images/'
        full_path = os.path.join(folder_name,file_name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(full_path, 'wb') as photo:
            photo.write(data)
        return full_path

    def send_photo(self, chat_id, img_path):
        print(img_path)
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        #self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')
        self.send_photo(msg['chat']['id'],'Image_processing_bot/images/img.png')

def send_message_to_ollama(message, filename):
    ext = filename.split('.')[-1]
    file_name = filename.split('.')[-2].split('/')[-1]
    code = generate_code(f'{message} , the image name is {filename} and end with .{ext}', file_name, ext)
    return code

class Image_processingBot(Bot):
    def handle_message(self, msg):
        if 'caption' not in msg:
            if msg["text"].lower() in ["hi","hello","hi!","hello!","start","start!"]:
                self.send_text(msg['chat']['id'], "Hello! I'm DeepPicBot, your image processing assistant. Type 'help' to see what I can do!")
            if msg["text"].lower() in ["help","help!"]:
                self.send_text(msg['chat']['id'] , "Just send me an image, and then tell me what you'd like me to do with it! you can apply any image processing operation on it.")
        else :
            prompt = msg["caption"]
            file_path = self.download_user_photo(msg)
            last_code = ""
            sent_image = False
            try:
                code = send_message_to_ollama(prompt, file_path)
                last_code = code
                print(code)
                exec(code)
                self.send_photo(msg['chat']['id'], 'Image_processing_bot/images/output.jpg')
                print("Code executed successfully.")
                time.sleep(2)
                os.remove(file_path)
                os.remove('Image_processing_bot/images/output.jpg')
                sent_image = True
            except Exception as e:
                print(f"Error occurred - {e}")
            if not sent_image:
                self.send_text(msg['chat']['id'], f"Sorry, I couldn't process the image. Please try again with a different request. and this is the code {last_code}")
                os.remove(file_path)













