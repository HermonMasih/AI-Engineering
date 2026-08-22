from groq import Groq
from dotenv import load_dotenv
import os
import numpy as np
from pydantic import BaseModel
import json
from sentence_transformers import SentenceTransformer

load_dotenv()

documents = [
"Company provides a paid leave of 30 days anually.",
"Company provides a transport reimbursement of Rs.2000 monthly.",
"Every employee is entitiled to Rs.500K medical insurance.",
"Every employee is entitled for internet reimbursement of Rs.2000 andvoice & data service of Rs.500 monthly."
]

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))


def create_embedding(documents:str):
    embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(documents)
    return embeddings

def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a) * np.linalg.norm(b))

def retriever(embed_query, embed_documents):
    relevant_info=[]
    for i, document in enumerate(embed_documents):
        score = cosine_similarity(embed_query, document)
        relevant_info.append((score, documents[i]))
    relevant_info.sort(reverse=True)
    return relevant_info[0]

class responsemodel_1(BaseModel):
    assistant:str
    user: str

response_model = responsemodel_1.model_json_schema()

def format_response(response):
    response = json.loads(response)
    print('user: ', response['user'])
    print('assistant: ', response['assistant'])


def ask_llm(question:str, context: str):
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

        content=input('continue the chat. Else say Thank you to end\n')

        if 'Thank you' in content:
            break

        _, context = retriever(create_embedding([content]), embed_documents)

        messages.append({
                    'role':'user',
                    'content': content +
                               f'''context: {context}'''
            })

question = input('Enter your prompt!!\n')
embed_query = create_embedding([question])
embed_documents = create_embedding(documents)
score, context = retriever(embed_query,embed_documents)
ask_llm(question, context)