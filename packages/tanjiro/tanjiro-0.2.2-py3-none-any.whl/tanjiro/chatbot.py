# tanjiro/chatbot.py

import requests

def chat(prompt, query):
    """
    Interact with the chatbot API.

    Parameters:
    prompt (str): The initial prompt for the chatbot.
    query (str): The user's query.

    Returns:
    str: The chatbot's response.

    Usage:
    ------
    from tanjiro import chat

    response = chat("i am natasha, i am girl", "hello")
    print(response)
    """
    url = f"https://noxapi-0a195c5b9f8f.herokuapp.com/chatbot/{prompt}/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"
