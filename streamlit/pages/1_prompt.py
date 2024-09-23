import streamlit as st
from modules.chat import *

# Streamlit GUI
st.title("Chat Model with Custom System Prompt")

system_prompt_input = st.text_area("Enter system prompt", value="あなたは親切で知識豊富なアシスタントです。")
user_input = st.text_input("Enter your message")

# ボタンで送信をトリガー
if st.button("Send") and user_input:
    # 1回目の会話
    session_id = "123"
    user_input = "うちの猫の名前は白子です。"
    openai_api_key = os.environ["OPENAI_API_KEY"]
    model_name = os.environ["MODEL_NAME"]
    chat = Chat(openai_api_key, model_name)
    chat.set_system_prompt(system_prompt_input)
    output = chat.run_conversation(session_id, user_input)
    print(output)

    
