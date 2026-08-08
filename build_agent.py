from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import B_SYSTEM_PROMPT
import os
import json
from time import sleep
import regex as re

load_dotenv()

client = Groq(api_key = os.environ.get('GROQ_API_KEY'))

# Building an agent following ReAct principle (Reasoning + Actions).

# 1st tool: Finding price of Iphone 17 pro
def get_phone_price(phone_name):
    if phone_name.lower() == 'iphone 17':
        return 150000
    elif phone_name.lower() == 'iphone 16':
        return 100000
    else:
        return 0

# Tool 2: Find the remaining amount after purchasing phone, total amount
def calculator(diff_exp):
    return eval(diff_exp)


tools = {
    'get_phone_price': get_phone_price,
    'calculator': calculator
}

def run_agent(prompt:str):
    messages = [
        {
            'role': 'system',
            'content': B_SYSTEM_PROMPT
        },
        {
            'role':'user',
            'content': prompt
            
        }
    ]

    for i in range(5): # assuming the task provided, LLM to find the answer using suitable tools provided.

        print("\n-----------------")
        print(f"Step: {i+1}")
        print("\n-----------------")

        reponse = client.chat.completions.create(
            model = 'openai/gpt-oss-120b',
            messages=messages,
            temperature=0
        )

        answer = reponse.choices[0].message.content
        print(answer)

        if 'Final Answer' in answer:
            break

        #match action
        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )

        if match:

            tool_name = match.group(1)
            tool_args = match.group(2)

            tool_name = tool_name.strip()
            tool_args = tool_args.strip('"')

            if tool_name in tools:
                tool = tools[tool_name]
                observations = tool(tool_args)

            else:
                observations = 'Tool not found!'

            print(f'observation: {observations}')

            # add the observation back to LLM
            messages.append({
                'role': 'assistant',
                'content': answer
            })

            # give tool result back to LLM for next action
            messages.append({
                'role': 'user',
                'content': f"Observation: {observations}"
            })
            sleep(5)

prompt = "I have 250000 rupees. What is the price of an Iphone 17? and how much money will I have left?"
run_agent(prompt)


    
