from scapy.all import *
from scapy.layers.inet import IP, ICMP
from network_tools import capture_packets
from network_tools.capture_packets import process_packets_detailed
from custom_llm_prompt import construct_response_summary

file_path = "sniffed_packets.pcap"


# Define a packet handler function
def packet_handler(pckt):
    # Process the packet as needed
    print(pckt.summary())


def ping_icmp_packets(target_ip, user_name):
    """
    Send an ICMP ping packet to the target IP address
    """
    # Check if the file exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been removed.")
    else:
        print(f"File '{file_path}' does not exist.")
    ping_response = ""
    # Craft an ICMP Echo Request packet (ping)
    ping_packet = [IP(dst=target_ip) / ICMP() for _ in range(4)]

    # Sniff network traffic in the background
    sniff_thread = AsyncSniffer(prn=packet_handler, store=0)
    sniff_thread.start()

    # Send the ping packet and wait for a response
    # response = sr1(ping_packet, timeout=2, verbose=False)
    # Send the ping packets and wait for responses
    responses, unanswered = sr(ping_packet, timeout=2, verbose=False)

    # Stop sniffing after sending the ping
    sniff_thread.stop()
    wrpcap(file_path, responses)
    print("Responses:", responses)
    print("Sniffed packets saved to file")
    capture_packets.processed_streamlit_data = process_packets_detailed(responses)
    print("Processed packets saved to file")

    # Check responses
    for sent_packet, received_packet in responses:
        if received_packet.type == 0:  # ICMP Echo Reply
            ping_response += f" Response received from {received_packet[IP].src}"
        else:
            ping_response += f" Unexpected response received"
            print("Unexpected response received")

    # Check for unanswered packets
    if unanswered:
        ping_response += f" {len(unanswered)} packets unanswered"
        print(f"{len(unanswered)} packets unanswered")
    else:
        ping_response += f" All packets answered"
        print("All packets answered")

    human_message = f"""
        {ping_response}
        """
    try:
        # custom_response = collect_messages_from_custom_prompts(human_message)
        user_query = (
            "Given the ICMP packets captured from Ping, analyze the data and give me a brief summary of the ICMP "
            "packets."
            "Start the response by saying that you have successfully pinged the domain and captured the ICMP packets."
            "For the response that you will be giving, make sure it is in Markdown format and always "
            "highlight important information like IP addresses, domain names, ports, Flags, etc in green. Also, "
            "make sure to"
            " keep it crisp and concise.")
        custom_response = construct_response_summary(user_query, responses, ping_response)
    except Exception as e:
        print("Ping packets response builder:", e)
        # custom_response = f"Sniffed {total_count} packets on interface {raw_interface} for {stop_time} seconds"
        custom_response = ping_response

    return custom_response
