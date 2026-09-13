from groq import Groq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import json
from sentence_transformers import SentenceTransformer
from utils.quad_utils import quadrant_client, create_collection_points, create_collections

load_dotenv()

# Constant
COLLECTION_NAME = 'knowledge-base-internal'

documents = [
"Company provides a paid leave of 30 days anually.",
"Company provides a transport reimbursement of Rs.2000 monthly.",
"Every employee is entitiled to Rs.500K medical insurance.",
"Every employee is entitled for internet reimbursement of Rs.2000 andvoice & data service of Rs.500 monthly."
]

def groq_client():
    groq_client = Groq(api_key = os.environ.get('GROQ_API_KEY'))
    return groq_client

def create_embedding(documents:str):
    embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(documents)
    return embeddings

def read_documents():
    doc=[]
    with open('company_docx.txt', 'r') as file:
        for f in file:
            doc.append(f.split())
    return doc

def retriever(user_query, collection_name):
    relevant_results=[]
    results = quad_client.query_points(
        collection_name=collection_name,
        query=user_query,
        with_payload=True,
        limit=5
    )

    for result in results.points:
        relevant_results.append((result.score, result.payload.get('text')))

    relevant_results.sort(reverse=True)
    return relevant_results[0][1]

class responsemodel_1(BaseModel):
    assistant:str
    user: str
    context: str

response_model = responsemodel_1.model_json_schema()

def format_response(response):
    response = json.loads(response)
    print('user: ', response['user'])
    print('assistant: ', response['assistant'])
    print('context:', response['context'])


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

        response = groq_client.chat.completions.create(
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

        context = retriever(create_embedding(content), COLLECTION_NAME)

        messages.append({
                    'role':'user',
                    'content': content +
                               f'''context: {context}'''
            })

# Steps to execute the RAG pipeline.
#1. input user query
user_query = input('Hey There😊, please ask your question to LLM\n')

#2. Read the company internal records for context gathering.
# documents = read_documents()

#3. Embed the user query and knowledge base in vectors.
print('Generating')
embed_documents = create_embedding(documents)
embed_user_query = create_embedding(user_query)

#4. connect to groq and quadrant client
groq_client = groq_client()
quad_client = quadrant_client()

#5. Create collection
create_collections(quad_client, COLLECTION_NAME)

#6. Insert records into collection in QuadVDB
create_collection_points(quad_client, COLLECTION_NAME,embed_documents, documents)

#7. Perform relevance search upon VectorDB based on user query and return context
context = retriever(embed_user_query, COLLECTION_NAME)
print(f'Context Retrieved: {context}')

#8. Call ask_llm() with your query and retrieve context
ask_llm(user_query, context)
