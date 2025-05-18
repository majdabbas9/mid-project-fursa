from Image_processing_bot.generate_filter import generate_code
import os
import cv2

def send_message_to_ollama(message, filename):
    ext = filename.split('.')[-1]
    file_name = filename.split('.')[-2].split('/')[-1]
    code = generate_code(f'{message} , the image name is {filename} and end with .{ext}', file_name, ext)
    return code

def run_code(message,filename):
    i = 0
    last_code = None
    codes_error = None
    while i < 10:
        i += 1
        try:
            if i == 1:
                code = send_message_to_ollama(message, filename)
            else:
                # Prepare context of previous code and error
                previous_info = f"\nThe last code was:\n{last_code}\nAnd it failed with this error:\n{codes_error}"
                retry_message = message + previous_info + "\nPlease try avoiding those mistakes."
                code = send_message_to_ollama(retry_message, filename)

            last_code = code
            print(code)

            print("Code executed successfully.")
            return code # Exit loop if successful

        except Exception as e:
            codes_error = str(e)
            print(f"Attempt {i}: Error occurred - {e}")
            continue  # Try again
