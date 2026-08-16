from groq import Groq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import json

load_dotenv()

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

knowledge_base = {
    'age': 'Hermon age is 30 years',
    'networth': "Hermon's networth is 200k"
}

class responsemodel_1(BaseModel):
    assistant:str
    user: str

response_model = responsemodel_1.model_json_schema()

def know_base(question):
    if 'age' in question:
        return knowledge_base.get('age')
    elif 'networth' in question:
        return knowledge_base.get('networth')
    else:
        return None

def format_response(response):
    response = json.loads(response)
    print('user: ', response['user'])
    print('assistant: ', response['assistant'])


def ask_llm(question:str):
    context = know_base(question)
    messages = [
        {
            'role': 'system',
            'content': f'''You are a helping assistant. Refer context: {context}
                            Please dont hallucinate!!. Follow the conversation in multi-turn sessions in below format
                            Follow the provided JSOn format: {response_model}
                            User: What is AI
                            Assistant: AI stands for Artificial Intelligent, where machines mimic just like Humans.'''
        },
        {
            'role':'user',
            'content': question
        }
    ]

    while(True):
        updated_system_prompt = f'''Use the context to provide private information to user: {context}'''
        updated_content = messages[0]['content'] + updated_system_prompt
        messages[0]['content'] = updated_content

        response = client.chat.completions.create(
                    model = 'openai/gpt-oss-120b',
                    messages=messages,
                    temperature=0
        )

        answer = response.choices[0].message.content

        format_response(answer)

        messages.append({
                    'role':'assistant',
                    'content': str(answer)
                })

        if 'Thank you' in answer:
            break

        content=input('continue the chat. Else say Thank you to end\n') 

        messages.append({
                    'role':'user',
                    'content': content +
                               f'''context: {know_base(content)}'''
            })

question = input('Enter your prompt!!\n')
ask_llm(question)