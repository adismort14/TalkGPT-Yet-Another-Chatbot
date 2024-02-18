import streamlit as st
import time
from hugchat import hugchat
from hugchat.login import Login

st.title("TalkGPT")

hf_email = st.secrets['EMAIL']
hf_pass = st.secrets['PASS']

with st.chat_message("user"):
    st.write("Hello. First message")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def generate_response(prompt_input, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

def response_stream_generator(content):
    content=str(content)
    for word in content.split():
        yield word + " "
        time.sleep(0.05)

if prompt := st.chat_input("Enter your prompt here."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            stream_res=response_stream_generator(response)
            st.write_stream(stream_res) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

