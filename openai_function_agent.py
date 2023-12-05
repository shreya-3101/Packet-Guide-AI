import openai
import json
from langchain.chat_models import ChatOpenAI
from db_operations import get_history, delete_history
from network_tools.capture_packets import sniff_count_packets, sniff_packets_duration, get_processed_packet_data, \
    process_predicted_packets
from custom_llm_prompt import set_user_input

# from network_tools.transport_layer_packet_count import transport_layer_packets_count

llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo-1106")

def trim_list_to_size(lst, max_size):
    """
    Trims a list to a specified maximum size, keeping the last 'max_size' elements.

    :param lst: The list to be trimmed.
    :param max_size: The maximum number of elements to retain in the list.
    :return: A trimmed list.
    """
    if len(lst) > max_size:
        return lst[-max_size:]
    return lst


def reduce_messages_size(messages, target_size=5):
    """
    Reduces the size of the messages array by keeping only the most recent messages.

    :param messages: The list of message dictionaries.
    :param target_size: The target number of messages to retain. Default is 5.
    :return: A reduced list of message dictionaries.
    """

    # Separate out system and user prompts from chat history
    system_and_user_prompts = [msg for msg in messages if msg['role'] in ['system', 'user']]
    chat_history = [msg for msg in messages if msg['role'] not in ['system', 'user']]

    # Retain only the most recent chat history messages
    if len(chat_history) > target_size:
        chat_history = chat_history[-target_size:]

    # Combine the retained chat history with system and user prompts
    reduced_messages = chat_history + system_and_user_prompts

    return system_and_user_prompts
    # return reduced_messages


def main_agent(user_input, user_name):
    set_user_input(user_input)
    chat_history = get_history(user_name, user_input)
    # only keep last 10 chat history elements to not surpass token limit
    chat_history = chat_history[-10:]

    ## - If the user opts for a specific number of packets but does not specify a number, default to capturing 50 packets.
    ## - If the user opts for a specific duration in seconds but does not specify a time, default to a 10-second capture.
    system_message = f"""
You are a friendly AI bot that assists users in capturing and analyzing network packets using tools 
like Python and Scapy. You offer two main services:

1. Capturing Network Packets:
- If the user asks to capture network packets, inquire if they prefer to specify the number of packets or 
the duration of the packet capture in seconds.
- If the user specifies the number of packets, then call the "capture_network_packets_with_count" function.
- If the user specifies the duration for the network packets, then call the "capture_network_packets_with_time" 
function.

2. Analyzing Captured Packets:

If the user has captured network packets and seeks an analysis, look into the CAPTURED PACKET DATA SECTION provided in this prompt. You can provide detailed insights, summaries, or specific information about the captured data.
Predict by the User input if the user wants a general summary, detailed analysis, or specific information (such as protocol distribution, IP addresses involved, common ports used, etc.) based on the captured packets.
Feel free to ask for more details or specific requirements regarding the packet capture or analysis.

Note: If the user asks how to get started or what can you do, formulate instructions based on above and give 
them examples based on your expertise. Make sure to not give examples of time greater than 7 seconds and 
packets greater than 100. Make sure to answer in a structured markdown format. Include bullets and format accordingly. 

Important: Do not talk about anything else. If the user asks for anything other than computer networks or packets,
tell them that you cannot help them as you are only an expert in Computer Networks. 

CAPTURED PACKET DATA SECTION STARTS HERE
{trim_list_to_size(get_processed_packet_data(), 100)}
CAPTURED PACKET DATA SECTION ENDS HERE

User Input:
"""

    system_prompt = [
        {"role": "system", "content": system_message},
    ]

    user_prompt = [
        {"role": "user", "content": user_input},
    ]

    # Add chat history to the messages array
    messages = []
    messages.extend(chat_history)
    messages.extend(system_prompt)
    messages.extend(user_prompt)

    # print("Final prompt \n", messages)

    custom_functions = [
        {
            'name': 'capture_network_packets_with_count',
            'description': 'This captures the exact number of network packets on all interfaces and returns those packets.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'number': {
                        'type': 'integer',
                        'description': 'The number of packets to capture.'
                    }
                },
                'required': ['number']
            }
        },
        {
            'name': 'capture_network_packets_with_time',
            'description': 'This captures the network packets for the exact duration the user asks for on all interfaces and returns those packets.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'stop_time': {
                        'type': 'integer',
                        'description': 'The duration of sniffing the packets in seconds.'
                    },
                },
                'required': ['stop_time']
            }
        },
        {
            "name": "predict_packet_protocol",
            "description": "Predicts only one network protocol that the user is asking for in the input and extracts the important information from user input",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "Copy the content in the User role in user_input. The user_input will be the exact same query/message that user sent"
                    },
                    "prediction": {
                        "type": "string",
                        "enum": [
                            "TCP",
                            "UDP",
                            "ICMP",
                            "IP",
                            "Ether",
                            "DNS",
                            "None",
                            "All"
                        ],
                        "description": "The predicted protocols of the packet"
                    }
                },
                "required": [
                    "user_input", "prediction"
                ]
            }
        }
    ]

    # print(f"Input: {messages}")

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-1106',
            messages=messages,
            functions=custom_functions,
            function_call='auto'
        )
    except openai.error.InvalidRequestError as e:
        # Logic to handle the token limit error
        # For example, reduce the size of the messages array
        # print("Retrying with reduced messages and deleting database history")
        print("Exception thrown in Main OpenAI Function: InvalidRequestError", e)
        # messages = reduce_messages_size(messages, 1)
        # Retry the request
        # response = openai.ChatCompletion.create(
        #     model='gpt-3.5-turbo-1106',
        #     # model='gpt-4-preview-1106',
        #     messages=messages,
        #     functions=custom_functions,
        #     function_call='auto'
        # )
    except Exception as ex:
        print("Exception thrown in Main OpenAI Function:", ex)

    response_message = response["choices"][0]["message"]
    print(response_message)

    if response_message.get('function_call'):

        # Which function call was invoked
        function_called = response_message['function_call']['name']

        # Extracting the arguments
        function_args = json.loads(response_message['function_call']['arguments'])
        function_args['user_name'] = user_name
        print(function_args)

        # Function names
        available_functions = {
            "capture_network_packets_with_count": sniff_count_packets,
            "capture_network_packets_with_time": sniff_packets_duration,
            "predict_packet_protocol": process_predicted_packets
        }

        function_to_call = available_functions[function_called]
        response_message = function_to_call(*list(function_args.values()))

    else:
        response_message = response_message['content']

    return response_message
