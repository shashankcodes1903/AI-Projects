import streamlit as st
import time

# page configuration
st.set_page_config(
    page_title="First Chatbot",
    page_icon=":)",
    layout="centered"
)

# it should be a fresh chat whenever the user opens the page
st.session_state.messages = []
st.session_state.bot_name = "Chuchii" # Name of the chatbot

# adding a side-bar
with st.sidebar:
    st.title("Chatbot settings")
    st.session_state.bot_name = st.text_input(
        "Bot Name", value = st.session_state.bot_name
    )

st.header("Welcome to my first chatbot")
st.divider()

# Conversation session
for msg in st.session_state.messages:
    role = msg['role']
    content = msg['content']
    ts = msg.get('time', "")
    with st.chat_message(role):
        st.markdown(content)


user_input = st.text_input("Your prompt to chatbot")
if user_input:
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input,
        'timestamp': time.strftime("%H:%M:%S")
    })

    with st.chat_message('user'):
        st.markdown(user_input)
    
    with st.chat_message('assistant'):
        with st.spinner("Typing....."):
            time.sleep(0.8)
        response = "Bhgg bsdk"
        st.markdown(response)