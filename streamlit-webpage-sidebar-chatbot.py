import streamlit as st

# Function representing a simple chatbot logic (echoes back the user input)
def chatbot_response(user_input):
    return f"Bot: You said '{user_input}'"

# Initialize chat history in session state if it's not already there
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar interface
with st.sidebar:
    st.title("Chatbot")
    user_input = st.text_input("Say something to the bot")

    # When the user submits a message
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(f"You: {user_input}")

        # Generate a response and add it to the chat history
        bot_response = chatbot_response(user_input)
        st.session_state.chat_history.append(bot_response)

        # Clear the input box after the message is sent
        st.rerun()

    # Display chat history
    for message in st.session_state.chat_history:
        st.text(message)

# Main page content (optional)
st.write("This is the main area of the app.")
