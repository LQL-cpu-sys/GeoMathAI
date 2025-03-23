import streamlit as st
import demo  # 假设 demo.py 在同一目录下
import argparse

# 设置页面基础配置
st.set_page_config(
    page_title="几何助手",
    page_icon=":triangular_ruler:"
)


# 侧边栏内容（简化版）
with st.sidebar:
    custom_title = '<h1 style="color: blue; font-style: italic;font-size: 18px;">欢迎使用几何助手</h1>'
    st.markdown(custom_title, unsafe_allow_html=True)
    st.image("logo.jpg", use_container_width=True)
    if st.button('开启新对话'):
        st.session_state['session'] = []  # 清除当前会话状态并初始化为空列表
       

custom_style = """
<style>
/* 覆盖所有可能的侧边栏选择器 */
[data-testid="stSidebar"],
.st-emotion-cache-6qob1r {
    background: linear-gradient(160deg, #E0F7FA 0%, #B2EBF2 100%) !important;
    padding: 20px !important;
}

/* 主界面渐变背景（从侧边栏颜色过渡到蓝紫色） */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        to right,
        #B2EBF2 15%,
        #B4C1ED 30%,  /* 增加蓝紫过渡层 */
        #C7B5E3 50%,  /* 强化紫色转折点 */
        #D3BCEB 75%,
        #D8CEEB 100%
    ) !important;
    min-height: 100vh;
}

/* 侧边栏文字颜色 */
[data-testid="stSidebar"] * {
    color: #2A4E6C !important;  /* 深蓝灰色保持可读性 */
}

/* 按钮样式适配新配色 */
button[data-testid="baseButton-secondary"] {
    background: #9F8FBF !important;
    border: 1px solid #7A6F8F !important;
    border-radius: 8px;
    color: white !important;
    transition: all 0.3s;
}

/* 鼠标悬停效果 */
button[data-testid="baseButton-secondary"]:hover {
    background: #8875A9 !important;
    transform: scale(1.02);
}
</style>
"""

# 应用样式
st.markdown(custom_style, unsafe_allow_html=True)



# 自定义标题样式：仅修改字体颜色和字体样式
custom_title = '''
<h1 style="
    color: #5E35B1;  /* 更改为你想要的颜色 */
    font-family: 'SimSun', '宋体', serif; /* 确保字体可以回退到通用字体 */
    font-weight: bold; /* 加粗字体 */
">
几何助手
</h1>
'''

# 将自定义样式的标题渲染到页面上
st.markdown(custom_title, unsafe_allow_html=True)




# 定义CSS样式
message_style = """
    <style>
        .user-message {
            text-align: left;
            margin-bottom: 10px;
            background-color: #FCFCFC;
            padding: 10px;
            border-radius: 10px;
            display: block;
            max-width: 100%;
        }
        .assistant-message {
            text-align: left;
            margin-bottom: 10px;
            background-color:#d0d0d0;
            padding: 10px;
            border-radius: 10px;
            display: block;
            max-width: 100%;
        }
    </style>
"""
st.markdown(message_style, unsafe_allow_html=True)


# 初始化会话计数器
if 'session_counter' not in st.session_state:
    st.session_state['session_counter'] = 0


# 显示历史会话
for message in st.session_state['session']:
    if message.startswith("您:"):
        st.markdown(f'<div class="user-message">{message[3:]}</div>', unsafe_allow_html=True)
        st.session_state.user_input = ""  # 清空输入框
    elif message.startswith("几何助手:"):
        st.markdown(f'<div class="assistant-message">{message[6:]}</div>', unsafe_allow_html=True)


# 确保会话状态正确初始化
if 'session' not in st.session_state:
    st.session_state['session'] = []


# 输入框与发送按钮
col1, col2 = st.columns([4, 1])

# 使用唯一键来避免重复键错误
if 'input_text_key' not in st.session_state:
    st.session_state['input_text_key'] = f'input_text_{st.session_state["session_counter"]}'
if 'file_uploader_key' not in st.session_state:
    st.session_state['file_uploader_key'] = f'file_uploader_{st.session_state["session_counter"]}'


# 用户输入
user_input = col1.text_input("请输入您的几何问题:", key=st.session_state['input_text_key'])
uploaded_file = col1.file_uploader("上传图片:", type=["png", "jpg", "jpeg"], key=st.session_state['file_uploader_key'])

# 用户输入


if col2.button('发送'):
    if user_input or uploaded_file is not None:
        # 记录用户输入或上传的图片
        if user_input:
            st.session_state['session'].append(f"您: {user_input}")
            st.session_state.user_input = ""  # 清空输入框
            #st.markdown(f'<div class="user-message">{message[3:]}</div>', unsafe_allow_html=True)
            #st.markdown(f'<div class="assistant-message">{user_input}</div>', unsafe_allow_html=True)
            #st.session_state.user_input = ""  # 清空输入框
            
        if uploaded_file is not None:
            temp_image_path = 'temp_image.png'
            with open(temp_image_path, 'wb') as f:
                f.write(uploaded_file.read())
            st.session_state['session'].append(f"您上传了图片: {uploaded_file.name}")
        
        # 准备调用外部模型的参数
        args = argparse.Namespace(
            decision_path='./data/decision.json' if user_input else None,
            image_path=temp_image_path if uploaded_file is not None else None,
            query=user_input if user_input else None,
            api_key='sk-38c0234d6f1044fd8a75bcba360d6295'
        )
        
        try:
            with st.spinner('正在处理中...'):
               response = demo.run_demo(args)
               if response and isinstance(response, str) and len(response.strip()) > 0:  # 确认返回值有效且为非空字符串
                  st.session_state['session'].append(f"几何助手: {response}")
                  #st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
               else:
                  st.error("未能获得有效的回复，请稍后重试！")
        except Exception as e:
            st.error(f"Error during processing: {e}")

        # 更新计数器，并重新设置唯一的key值
        st.session_state['session_counter'] += 1
        st.session_state['input_text_key'] = f'input_text_{st.session_state["session_counter"]}'
        st.session_state['file_uploader_key'] = f'file_uploader_{st.session_state["session_counter"]}'

