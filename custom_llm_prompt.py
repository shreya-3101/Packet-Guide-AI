from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def collect_messages_from_custom_prompts(human_msg, system_msg="""
    You will be given a summary of the captured network packets. Your job is to convert this summary into a human understandable format.
    Make it simple and easy to understand. Make sure to keep it crisp, concise and light on technical jargon. If possible use analogies.
    """):
    """
    Uses chat-gpt langchain structure to get responses from custom prompts
    """
    custom_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", max_retries= 1, request_timeout=10)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(
            content=human_msg,
        ),
    ]
    output_msg = custom_llm(messages)

    return output_msg.content
