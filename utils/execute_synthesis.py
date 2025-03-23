import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
from openai import OpenAI
import dashscope
#import torch
#import torchvision.transforms as T
# Used to securely store your API key
# from google.colab import userdata
from datasets import load_dataset
from IPython.display import display
from IPython.display import Markdown
from .prompt import prompt_template
#from torchvision.transforms.functional import InterpolationMode
from transformers import AutoModel, AutoTokenizer
def execute_synthesis(args):
    with open(args.decision_path, 'r') as file:
        decision = json.load(file)
    image = PIL.Image.open(args.image_path)
    client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)
    model = 'qwen2.5-vl-3b-instruct'
    
    supplementary_information = decision["supplementary_information"]
    
    query = decision["query"]
    base_prompt = prompt_template["execute_synthesis_prompt"]
    prompt =  f"{base_prompt}\nPlease answer the following case:\n Question:{query}\nSupplementary information:{supplementary_information}"
    """
    response = model.generate_content([prompt, image], stream=True, 
                                    safety_settings={'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                    'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                    'HARM_CATEGORY_HARASSMENT': 'block_none',
                                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
    """
    """
    completion = client.chat.completions.create(
    model,  # 此处以qwen-vl-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[{"role": "user","content": [
            {"type": "text","text": prompt},
            {"type": "image_url",
             "image_url": {"url": image}}
            ]}],
            stream=True
    )
    """
    
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
            print("\n\nExecute_Synthesis:")
            print(response.output.choices[0].message.content[0]["text"])
            decision["response"] = response.output.choices[0].message.content[0]["text"]
        except:
            decision["response"] = " "

    with open(args.decision_path, 'w') as json_file:
        json.dump(decision, json_file , indent=4)
        
    return response.output.choices[0].message.content[0]["text"]

