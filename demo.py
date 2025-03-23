import pathlib
import textwrap
import os
import PIL.Image
import json
import argparse
#from openai import OpenAI
from IPython.display import display
from IPython.display import Markdown
from utils.decision_generation import decision_generation
from utils.split_task import split_task
from utils.execute_modularization import execute_modularization, summary
from utils.execute_synthesis import execute_synthesis
import dashscope
import pickle
import numpy as np

def getFilename():
    dir = "data\GeoQA+"
    listfile = os.listdir(dir)
    test_filename,train_filename = '',''
    for i in range(len(listfile)):
        if listfile[i].find('test.pk') > 0:  # 没找到子串返回-1，找到返回索引位置
            test_filename = dir + '\\' + listfile[i]
        if listfile[i].find('train.pk')>0:
            train_filename=dir+'\\'+listfile[i]
    return test_filename,train_filename
 
#将读到的pk文件的数据写入新文件

"""
if not os.path.exists(args.decision_path):
    dic = {}
    with open(args.decision_path, 'w') as json_file:
        json.dump(dic, json_file , indent=4)
"""


def run_demo(args):
    decision_generation(args)
    split_task(args)
    execute_modularization(args)
    summary(args)
    return execute_synthesis(args)


def write_TestdataOrTraindata(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    """
    f=open(filename[filename.find('_t')+1:filename.find('.')]+'.txt','w',encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--decision_path', type=str, default='./data/decision.json')
    parser.add_argument('--image_path', type=str, default='./images/image.png')
    parser.add_argument('--query', type=str, default="Which month is the hottest on average in Detroit?")
    parser.add_argument('--api_key', type=str, default='')
    args = parser.parse_args()
    run_demo(args)    
        """
    print(data[0])

    for i in range(len(data)):

        f1=open(filename[filename.find('_t')+1:filename.find('.')]+"_ask"+"\\"+str(data[i]["id"])+".json",'w',encoding='utf-8')
        f2=filename[filename.find('_t')+1:filename.find('.')]+"_photo"+"\\"+str(data[i]["id"])+".png"
        dict={"query":data[i]["subject"]+"选项："+str(data[i]["choices"]),
              "decision":"",
              "answer":data[i]["answer"],
              "ans_choice":data[i]["ans_choice"]
              }
        json_object = json.dumps(dict, indent=4)
        f1.write(json_object)
        random_data_arr = np.array(data[i]["image"], np.uint8)  # Convert random_data to NumPy array of type 'uint8'
        pil_image = PIL.Image.fromarray(random_data_arr)  # Convert the NumPy array to PIL image
        pil_image.save(f2)  # Save the image in PNG format

def run_muti(path):
    dir_list = os.listdir(path[path.find('_t')+1:path.find('.')]+"_ask")
    for i in dir_list:
        f1=open(path[path.find('_t')+1:path.find('.')]+"_ask"+"\\"+i,'r',encoding='utf-8')
        decision = json.load(f1)
        f1.close()
        parser = argparse.ArgumentParser()
        parser.add_argument('--decision_path', type=str, default=path[path.find('_t')+1:path.find('.')]+"_ask"+"\\"+i)
        parser.add_argument('--image_path', type=str, default=path[path.find('_t')+1:path.find('.')]+"_photo"+"\\"+i[i.find('_t')+1:i.find('.')]+".png")
        parser.add_argument('--query', type=str, default=(decision["query"]))
        parser.add_argument('--api_key', type=str, default='')
        args = parser.parse_args()
        run_demo(args)
        print('-----------------')

#run_demo(args)
"""
a=getFilename()
print(a)
for i in a:
    #write_TestdataOrTraindata(i)
    run_muti(i)
"""


