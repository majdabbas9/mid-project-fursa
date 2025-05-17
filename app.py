from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3:1b', messages=[
    {'role': 'system', 'content': 'you are a software developer , your mission to return a python function based on the user input'},
    {'role': 'user', 'content': 'a python function that takes a list of numbers and returns the list rotated by one position to the right'},
])
print(response['message']['content'])  # "rotate" is expected
