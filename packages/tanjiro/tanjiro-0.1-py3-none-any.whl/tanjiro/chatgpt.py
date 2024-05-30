# tanjiro/chatgpt.py

import time
import requests

class ChatGPT:
    def __init__(self, api_url='https://chatgpt.apinepdev.workers.dev/?question='):
        self.api_url = api_url

    def ask(self, question):
        start_time = time.time()
        response = requests.get(f'{self.api_url}{question}')
        response_time = time.time() - start_time

        if response.status_code == 200:
            try:
                data = response.json()
                if "answer" in data:
                    return {
                        'answer': data["answer"],
                        'response_time_ms': round(response_time * 1000, 3)
                    }
                else:
                    return {'error': "No 'answer' key found in the response."}
            except ValueError:
                return {'error': "Invalid JSON response."}
        else:
            return {'error': f"Request failed with status code {response.status_code}"}
