import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
from openai import OpenAI
import dashscope
import re
import pickle
from transformers import AutoModel, AutoTokenizer
from IPython.display import display
from IPython.display import Markdown

def execute_modularization(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    image = PIL.Image.open(args.image_path)
    # 定义提示语
    decision["sub-answers"] =[]
    prompts = decision["sub-tasks"]
    print("\n\nExecute_Modularization:")
    for prompt in prompts:
        print(prompt)
        """
        response = model.generate_content([prompt, image], 
                                        safety_settings={'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                                        'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                                        'HARM_CATEGORY_HARASSMENT': 'block_none',
                                                        'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
        """
        """response = client.chat.responses.create(
    model,  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{"role": "user","content": [
            {"type": "text","text": prompt},
            {"type": "image_url",
             "image_url": {"url": image}}
            ]}],
            stream=True
    )"""
        messages = [
        {
            "role": "user",
            "content": [
                {"image": args.image_path},
                {"text": prompt}
            ]
    }
    ]
        response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen2.5-vl-3b-instruct", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        )
        try:
            print(response)
        except:
            print(response.prompt_feedback) 
        else:
            try:
                print(response.output.choices[0].message.content[0]["text"])
                decision["sub-answers"].append(response.output.choices[0].message.content[0]["text"]) 
            except:
                decision["sub-answers"].append(" ") 
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)

def summary(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    
    matches = re.findall(r'Answer\*{0,2}:{0,1}\*{0,2}\s*(.*?)\s*\*{0,2}Modules{0,1}\'s{0,1} [tT]asks{0,1}\*{0,2}:', decision["decision"], re.DOTALL)  #Image Understanding Module + Image Understanding Agent
    matches2 = re.findall(r'Rationale\*{0,2}:\*{0,2}\s*(.*?)\n\*{0,2}Modules{0,1}\'s{0,1} [tT]asks{0,1}\*{0,2}:', decision["decision"], re.DOTALL)
    
    if matches: 
        supplementary_information = ' '.join(matches)
    else:
        if matches2:
            supplementary_information = ' '.join(matches2)
        else:
            supplementary_information = decision["decision"]
    sub_questions = decision["sub-tasks"]
    sub_answers = decision["sub-answers"]
    
    if sub_questions:
        supplementary_information +=  "\nModules\' tasks:\n"
    
    for sub_q, sub_a in zip(sub_questions, sub_answers):
        reform_sub = f"{sub_q} Answer:{sub_a}\n"
        supplementary_information += reform_sub
    
    decision["supplementary_information"] = supplementary_information
    
    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)
    
