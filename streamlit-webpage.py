import streamlit as st
from openai_function_agent import main_agent
from db_operations import write_history, delete_history
from network_tools import capture_packets


# App title
st.set_page_config(page_title="📨💬 PacketGuide AI", page_icon="📨💬", layout="wide")

with st.sidebar:
    st.sidebar.header('📨💬 PacketGuide AI')
    user_name = st.text_input("Enter your name:")
    if not user_name:
        st.warning('Please enter your name!', icon='⚠️')
    else:
        delete_history(user_name)
        print("Database History deleted!!")
        st.success('Proceed to entering your prompt message!', icon='👉')

    # Display data in a table
    st.sidebar.title('PacketGuide Viewer')
    # st.sidebar.dataframe(capture_packets.processed_streamlit_data)

st.subheader('📨💬 PacketGuide AI Chatbot')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "Hey there! I'm your packet guru ready to sprinkle some assistance magic. What can I do for you today? 🌟"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_name:
    if prompt := st.chat_input("Type your packet capture query here:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Processing..."):
                try:
                    response = main_agent(prompt, user_name)
                    st.sidebar.dataframe(capture_packets.processed_streamlit_data)
                except Exception as e:
                    print("Exception thrown:", e)
                    response = "I am sorry, I couldn't process your request."
                message_placeholder.markdown(response)
                if response:
                    full_response += response
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            write_history(user_name,
                          [{"role": "user", "content": prompt}, {"role": "assistant", "content": full_response}])
else:
    st.chat_input('Please enter your name first!', disabled=True)
