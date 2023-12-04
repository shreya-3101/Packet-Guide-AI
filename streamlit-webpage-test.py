
# BELOW CODE WORKS

import streamlit as st
from openai_function_agent import main_agent
from db_operations import write_history
from network_tools import capture_packets

# App title
st.set_page_config(page_title="📨💬 PacketGuide AI", page_icon="📨💬", layout="wide")

# Hugging Face Credentials
with st.sidebar:
    st.sidebar.header('📨💬 PacketGuide AI')
    user_name = st.text_input("Enter your name:")
    if not user_name:
        st.warning('Please enter your name!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey there! I'm your packet guru ready to sprinkle some assistance magic. What can I do for you today? 🌟"}]

# Create two columns
col1, col2 = st.columns([3, 2])  # Adjust the width ratio as needed

# Left Column: Chatbot
with col1:
    st.subheader('📨💬 PacketGuide AI Chatbot')

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.expander(f"{message['role'].title()} Says:", expanded=True):
            st.markdown(message["content"])

    # Chat input at the bottom
    if user_name:
        with st.form(key='chat_form'):
            prompt = st.text_input("Type your packet capture query here:")
            submit_button = st.form_submit_button(label='Send')

        if submit_button and prompt:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate and add assistant response to chat history
            response = main_agent(prompt, user_name)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Write history to database
            write_history(user_name, [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}])
            st.experimental_rerun()

# Right Column: Dynamic Table
with col2:
    st.subheader('Dynamic Table')
    # Code to handle the dynamic table goes here
    # For example, you can use a form to take inputs and update the table