import openai
import json
from langchain.chat_models import ChatOpenAI
from db_operations import get_history
from network_tools.capture_packets import sniff_count_packets, sniff_packets_duration
from network_tools.transport_layer_packet_count import transport_layer_packets_count

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")


def main_agent(user_input, user_name):
    chat_history = get_history(user_name, user_input)
    # only keep last 10 chat history elements to not surpass token limit
    chat_history = chat_history[-10:]

    system_message = """
    You are a friendly AI bot that helps a user capture the network packets using the tools and analyze those network packets in a human understandable way. 
    If the user asks to capture network packets, always first ask the user about the interface. Then ask, whether the user wants to specify the number of packets or the duration of network packet capture in seconds.
    If the user chooses to specify the number of packets, but no number is specified still, then use 50 as default and if no interface is specified, use wifi interface as default.
    If the user chooses to specify the duration in seconds of the packet capture, but no time is specified still, then use 10 seconds as default and if no interface is specified, use wifi interface as default.
    User Input:"""

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

    custom_functions = [
        {
            'name': 'capture_network_packets_with_count',
            'description': 'This captures the exact number of network packets on the interface and returns those packets.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'interface': {
                        'type': 'string',
                        'description': 'The interface to capture packets on.'
                    },
                    'number': {
                        'type': 'integer',
                        'description': 'The number of packets to capture.'
                    }
                },
                'required': ['interface', 'number']
            }
        },
        {
            'name': 'capture_network_packets_with_time',
            'description': 'This captures the network packets for the exact duration the user asks for on the interface and returns those packets.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'interface': {
                        'type': 'string',
                        'description': 'The interface to capture packets on.'
                    },
                    'stop_time': {
                        'type': 'integer',
                        'description': 'The duration of sniffing the packets in seconds.'
                    },
                },
                'required': ['interface', 'stop_time']
            }
        },
        {
            'name': 'transport_layer_packets_count',
            'description': 'This gives an overall and individual count of all the transport layer packets.',
            "parameters": {
                "type": "object",
                "properties": {
                    "dummy_property": {
                        "type": "null",
                    }
                }
            }
        }
    ]

    # print(f"Input: {messages}")

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        functions=custom_functions,
        function_call='auto'
    )

    response_message = response["choices"][0]["message"]

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
            "transport_layer_packets_count": transport_layer_packets_count
        }

        function_to_call = available_functions[function_called]
        response_message = function_to_call(*list(function_args.values()))

    else:
        response_message = response_message['content']

    return response_message
