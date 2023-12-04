import streamlit as st
from dotenv import load_dotenv
from scapy.all import *
import openai
import json
from langchain.chat_models import ChatOpenAI
from openai_function_agent import main_agent
import openai_function_agent
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from db_operations import write_history, retrieve_packets

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Authentication
headers = {
    "authorization": openai.api_key,
    "content-type": "application/json"
    }

user_name = "test_user"
# llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")

st.title('PacketGuide AI')

input_text = st.text_input("Chat here:")
submit = st.button('Send')

# Instructions or descriptions if any
# st.write('Please press the button below to capture 50 network packets.')

# Button to trigger packet capturing
# if st.button('Capture Packets'):
#     st.write('Capturing... Please wait.')
#     # Call the function to capture packets
#     packets = sniff(count=50)
#     st.success('Done Capturing!')

# input_text = "How many transport layer packets are there in the captured network packets?"
# input_text = "I want to capture 15 network packets on the wifi interface."
# input_text = "What is transport layer packet?"
# input_text = "Capture on wifi for 5 seconds."

response = main_agent(input_text, user_name)
# print("Response:", response)
write_history(user_name, [{"role": "user", "content": input_text}, {"role": "assistant", "content": response}])
# print(ai_msg.content)
st.info(response)

# To run this project write the following command in your terminal
# streamlit run main.py