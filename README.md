# 数学几何题问答代理

## 项目简介
本项目是一个基于图像和文本的数学几何问题AI，旨在通过结合视觉和文本信息来回答复杂的几何问题。项目使用了多个专门模块来处理图像中的文本、对象、视觉数据和图表信息，并通过大模型生成详细的推理过程和答案。

## 主要功能
- **TextIntel 提取器**：从图像中提取并转换文本为可编辑文本格式。
- **ObjectQuant 定位器**：识别并定位图像中的对象。
- **VisionIQ 分析师**：处理和解释视觉数据，回答关于图像内容的问题。
- **ChartSense 专家**：分析和解释图表中的信息，提取数据点和趋势。
- **多模态推理**：结合图像和文本信息，生成详细的推理过程和答案。

## 安装与使用

### 依赖项

```bash
pip install openai dashscope pillow numpy transformers datasets streamlit
```
使用方法
1.克隆项目：
git clone https://github.com/yourusername/GeoMathAI.git
cd GeoMathAI

2.配置 API 密钥：
在 config.py 文件中设置你的 OpenAI 和 Dashscope API 密钥：
# config.py
OPENAI_API_KEY = "your_openai_api_key"  # 替换为你的 OpenAI API 密钥
DASHSCOPE_API_KEY = "your_dashscope_api_key"  # 替换为你的 DashscopeAPI密钥

3.运行示例：
运行 app.py 文件来执行示例问题:
streamlit run app.py
```

## 项目结构
GeoMathAI/
├── data/                  # 数据文件夹
│   ├── GeoQA+/            # GeoQA+ 数据集
│   │   └── decision.json  # 决策文件
│   └── static/            # 静态资源文件夹
├── utils/                 # 工具函数文件夹
│   ├── __pycache__/       # Python 编译缓存文件夹
│   ├── __init__.py        # 初始化文件
│   ├── decision_generation.py  # 决策生成模块
│   ├── execute_modularization.py  # 模块化执行模块
│   ├── execute_synthesis.py  # 综合执行模块
│   ├── prompt_pre.py      # 提示预处理模块
│   ├── prompt.py          # 提示模板模块
│   ├── split_task.py      # 任务拆分模块
├── app.py                 # Streamlit 应用入口
├── demo.py                # 演示脚本
├── index.html             # 网页入口文件
├── logo.png               # 项目 Logo
├── README.md              # 项目说明文件
└── temp_image.png         # 处理问题时的临时图像文件
