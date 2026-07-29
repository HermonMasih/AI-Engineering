from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from prompts import SYSTEM_PROMPT
import json

load_dotenv()

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

class Response_Model(BaseModel):
    Question: str
    Response: str

response_schema_model = Response_Model.model_json_schema()

messages = [
    {
        'role': 'system',
        'content': f'''{SYSTEM_PROMPT}.
         Use the provided JSON model {response_schema_model} to tailor your response'''
    },
    {
        'role': 'user',
        'content': input('Enter User Question!! \n')
    }
]

response = client.chat.completions.create(
    model = 'openai/gpt-oss-120b',
    messages = messages
)

final_response = response.choices[0].message.content
# print(type(final_response))

data = json.loads(final_response)
# print(data, type(data))

print('Question:',  data['Question'])
print('Response:',  data['Response'])