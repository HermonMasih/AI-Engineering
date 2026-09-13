from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

messages = [
    {
        'role': 'system',
        'content': 'You are a helping assistant.'
    },
    {
        'role': 'user',
        'content': input('Enter User Question!! \n')
    }
]
streaming = True

if streaming:
    # with streaming
    stream = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = messages,
        stream = True
    )

    for chunk in stream:
        response = chunk.choices[0].delta.content
        if response:
            print(response, end="", flush=True)
else:
    # Without streaming
        response = client.chat.completions.create(
            model = 'openai/gpt-oss-120b',
            messages = messages
        )
    
        final_response = response.choices[0].message.content
