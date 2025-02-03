import streamlit as st
import os
import requests  
import json  
  

from navigation import make_sidebar
make_sidebar()

col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

with col1:
    chat_model = st.selectbox('Please select a chat model.', ["Deepseek-R1"])

with col2:
    if st.button('Clean Chat History'):
        if 'free_messages' in st.session_state:
            del st.session_state['free_messages']
            st.rerun()

# # st.write('You selected:', chat_model)

ENDPOINT = "https://bowa-m6lyjdht-westus3.openai.azure.com/models/chat/completions?api-version=2024-05-01-preview"  
subscription_key = os.environ["DeepSeek-R1-Key"]

  
# 设置请求的 headers  
headers = {  
    "Content-Type": "application/json",  
    "api-key": subscription_key  
}  

# Generate Stream
def stream_processor(response):
    for line in response.iter_lines():  
        if line:  
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):  # 检查是否以 "data：" 开头  
                decoded_line = decoded_line[6:]  # 删除开头的 6 个字符  
            try:  
                json_line = json.loads(decoded_line)  
                if "choices" in json_line and len(json_line["choices"]) > 0: 
                    content = json_line["choices"][0].get("delta", {}).get("content", None)  
                    if content:
                        if content == "<think>":
                            yield "``` \n\n thinking..."
                        elif content == "</think>":
                            yield "```"
                        else:
                            yield content
            except json.JSONDecodeError:  
                print("无法解析的行：", decoded_line)  

if "free_messages" not in st.session_state:
    st.session_state.free_messages =  []

for message in st.session_state.free_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.free_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.free_messages ]
        history.insert(0, {"role": "system", "content": "You are an AI assistant that helps people find information."})

        payload = {  
            "model": "deepseek-r1",  
            "stream": True,  
            "messages": history,  
            "temperature": 0.7,  
            "top_p": 0.95,  
            "frequency_penalty": 0,  
            "presence_penalty": 0,  
            # "max_tokens": 2000,  
            "stop": None  
        }  

        response = requests.post(ENDPOINT, headers=headers, json=payload, stream=True)  
    
        # 检查响应状态码  
        if response.status_code == 200:  
            streamlit_response = st.write_stream(stream_processor(response))
        else:  
            print(f"请求失败，状态码：{response.status_code}")  
            print("响应内容：", response.text)  


    st.session_state.free_messages.append({"role": "assistant", "content": streamlit_response})