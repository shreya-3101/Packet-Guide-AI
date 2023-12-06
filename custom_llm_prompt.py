from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

global user_input


def collect_messages_from_custom_prompts(human_msg):
    system_msg = """You will be given a summary of the captured network packets. Your job is to convert this summary 
    into a human understandable format. Make it simple and easy to understand. Make sure to keep it crisp, 
    concise and light on technical jargon."""

    # Uses chat-gpt langchain structure to get responses from custom prompts
    custom_llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo-1106", max_retries=1, request_timeout=20)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(
            content=human_msg,
        ),
    ]
    output_msg = custom_llm(messages)

    print("Custom response from LLM", output_msg)

    return output_msg.content


def construct_response_summary(user_query, all_packets_summary, packet_dump):
    global user_input
    system_msg = """You will be given the raw PCAP network packet dump. Your job is to understand and analyze 
    the raw packets. Along with that, you will be given a "All Packets Summary" which will tell you the type 
    of packets in the total capture. Remember, you might not have all the packet types in the Packet Dump 
    so if you cannot find packets of a specific type, tell user to query based on those packet types. 
    You will also be given a User Query which will contain the question that the user wants
    from the analysis. Answer the user's queries with as precision and detail as possible. Remember to add bullet points  
    when answering the questions. Don't display the raw packet data. If you couldn't analyze 
    or find the answer, suggest some better user queries to the user so that they can ask again. """

    if user_input is not None:
        formatted_user_query = user_input
    else:
        formatted_user_query = user_query

    custom_human_message = "User Query: " + formatted_user_query + "\nAll Packets Summary: " + str(
        all_packets_summary) + "\n Packet Dump: \n" + str(packet_dump)
    print("Custom Human Message: ", custom_human_message)

    # Uses chat-gpt langchain structure to get responses from custom prompts ##gpt-3.5-turbo-1106 ##gpt-4-preview-1106
    custom_llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo-1106", max_retries=1, request_timeout=100)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(
            content=custom_human_message,
        ),
    ]
    try:
        output_msg = custom_llm(messages)
    except Exception as e:
        print("Error while constructing response summary: ", e)


    print("Custom response from LLM", output_msg)

    return output_msg.content


def construct_dns_response_summary(human_msg):
    system_msg = """You will be given a summary of the captured DNS query and answer network packets. Your job is to 
    convert this summary into a human understandable format. List down in bullet points which domain name is mapped with what IP address.
    Make it simple and easy to understand."""

    # Uses chat-gpt langchain structure to get responses from custom prompts
    custom_llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo-1106", max_retries=1, request_timeout=20)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(
            content=human_msg,
        ),
    ]
    output_msg = custom_llm(messages)

    print("Custom response from LLM", output_msg)

    return output_msg.content


def set_user_input(input_string):
    global user_input
    user_input = input_string
