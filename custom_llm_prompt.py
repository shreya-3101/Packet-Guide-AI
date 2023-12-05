from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def collect_messages_from_custom_prompts(human_msg):
    system_msg = """
        You will be given a summary of the captured network packets. Your job is to convert this summary into a human understandable format.
        Make it simple and easy to understand. Make sure to keep it crisp, concise and light on technical jargon. If possible use analogies.
        """

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
    system_msg = """You will be given the raw PCAP packet dump. Your job is to understand and analyze the raw dump 
    and answer the user's queries with as precision and detail as possible."""

    custom_human_message = "User Query: " + user_query + "\nAll Packets Summary: " + str(all_packets_summary) + "\n Packet Dump: \n" + str(packet_dump)
    print("Custom Human Message: ", custom_human_message)

    # Uses chat-gpt langchain structure to get responses from custom prompts
    custom_llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo-1106", max_retries=1, request_timeout=100)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(
            content=custom_human_message,
        ),
    ]
    output_msg = custom_llm(messages)

    print("Custom response from LLM", output_msg)

    return output_msg.content
