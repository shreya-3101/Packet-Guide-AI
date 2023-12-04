import streamlit as st
from openai_function_agent import main_agent
from db_operations import write_history
from network_tools import capture_packets

# App title
st.set_page_config(page_title="📨💬 PacketGuide AI", page_icon="📨💬", layout="wide")



# # Hugging Face Credentials
with st.sidebar:
    st.sidebar.header('📨💬 PacketGuide AI')
    user_name = st.text_input("Enter your name:")
    if not user_name:
        st.warning('Please enter your name!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
#     if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
#         st.success('HuggingFace Login credentials already provided!', icon='✅')
#         hf_email = st.secrets['EMAIL']
#         hf_pass = st.secrets['PASS']
#     else:
#         hf_email = st.text_input('Enter E-mail:', type='password')
#         hf_pass = st.text_input('Enter password:', type='password')
#         if not (hf_email and hf_pass):
#             st.warning('Please enter your credentials!', icon='⚠️')
#         else:
#             st.success('Proceed to entering your prompt message!', icon='👉')
#     st.markdown(
#         '📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')

# user_name = "test_user"

# with st.sidebar:
#     st.title('📨💬 Packet Capture')
#     try:
#         with open("sniffed_packets_string.txt", "r") as f:
#             st.write(f.read())
#     except FileNotFoundError:
#         st.write("Please capture some network packets first.")

# # Column 1
# col1.title('PacketGuide Viewer')
# # Display data in a table
# col1.write("Packet Data:")
# col1.table(capture_packets.processed_streamlit_data)

# Column 2


## OLD WORKING CODE
# col2.title('PacketGuide AI Chatbot')
# # Store LLM generated responses
# if "messages" not in st.session_state.keys():
#     st.session_state.messages = [{"role": "assistant", "content": "Hey there! I'm your packet guru ready to sprinkle some assistance magic. What can I do for you today? 🌟"}]
#
# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         col2.write(message["content"])
#
#
# # Function for generating LLM response
# def generate_response(input_text, user_name):
#     function_response = main_agent(input_text, user_name)
#     return function_response
#
#
# # User-provided prompt
# if user_name:
#     if prompt := col2.text_input("Enter your message here:"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with col2.chat_message("user"):
#             # col2.write(prompt)
#             col2.markdown(prompt)
# else:
#     col2.warning('Please enter your name first!', icon='⚠️')
#
# # Generate a new response if last message is not from assistant
# if st.session_state.messages[-1]["role"] != "assistant":
#     with col2.chat_message("assistant"):
#         message_placeholder = st.empty()
#         with st.spinner("Thinking..."):
#             response = generate_response(prompt, user_name)
#             message_placeholder.markdown(response)
#             # col2.write(response)
#     message = {"role": "assistant", "content": response}
#     st.session_state.messages.append(message)
#     write_history(user_name, [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}])

# NEW CODE

st.subheader('📨💬 PacketGuide AI Chatbot')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey there! I'm your packet guru ready to sprinkle some assistance magic. What can I do for you today? 🌟"}]


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
            with st.spinner("Thinking..."):
                response = main_agent(prompt, user_name)
                message_placeholder.markdown(response)
                full_response += response
                message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            write_history(user_name, [{"role": "user", "content": prompt}, {"role": "assistant", "content": full_response}])
else:
    st.chat_input('Please enter your name first!', disabled=True)
