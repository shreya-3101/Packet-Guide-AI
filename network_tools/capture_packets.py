from scapy.all import sniff
from scapy.layers.inet import IP
from scapy.utils import wrpcap
from custom_llm_prompt import collect_messages_from_custom_prompts
import os
from scapy.all import *


processed_streamlit_data = []
# Print packet summary
def packet_callback(packet):
    # Print packet summary
    print(packet.summary())


# Sniff a particular number of packets on a specific interface
def sniff_count_packets(raw_interface=r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}", count=None,
                        user_name=None):
    if raw_interface.lower() == "wifi":
        interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"
    elif raw_interface.lower() == "ethernet" or raw_interface.lower() == "eth0":
        interface = r"\Device\NPF_{D41ABC33-1765-4E8E-BCF1-B0907DB3166E}"
    elif raw_interface.lower() == "loopback":
        interface = r"\Device\NPF_Loopback"
    else:
        interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"
    total_count = 0

    if count is not None:
        os.remove("sniffed_packets.pcap")
        print(f"Sniffing {count} packets on interface {raw_interface}")
        total_packets = sniff(iface=interface, prn=packet_callback, count=count)
        wrpcap("sniffed_packets.pcap", total_packets)
        print("Total packets:", total_packets)
        for packet in total_packets:
            total_count += 1
            with open("sniffed_packets_string.txt", "a") as f:
                f.write(str(packet))
                f.write("\n")

        print("Done sniffing!")

        response_string = f"Sniffed {total_count} packets on interface {raw_interface}"
    else:
        response_string = "Please specify the number of packets to capture."

    human_message = f"""
    {response_string}
    """
    try:
        print("Building the custom response...")
        custom_response = collect_messages_from_custom_prompts(human_message)
    except Exception as e:
        print("Count packets response builder:", e)
        custom_response = f"Sniffed {total_count} packets on interface {raw_interface}"

    return custom_response


def process_packets(packets):
    processed_data = []
    for single_packet in packets:
        # Extract relevant fields from each packet
        packet_info = {
            "Time": single_packet.time,
            "Source": single_packet[IP].src if IP in single_packet else None,
            "Destination": single_packet[IP].dst if IP in single_packet else None,
            # Add more fields as needed
        }
        processed_data.append(packet_info)
    return processed_data



# Sniff network packets on a specific interface for a particular duration
def sniff_packets_duration(raw_interface=r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}", stop_time=None,
                           user_name=None):
    global processed_streamlit_data
    if raw_interface.lower() == "wifi":
        interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"
    elif raw_interface.lower() == "ethernet" or raw_interface.lower() == "eth0":
        interface = r"\Device\NPF_{D41ABC33-1765-4E8E-BCF1-B0907DB3166E}"
    elif raw_interface.lower() == "loopback":
        interface = r"\Device\NPF_Loopback"
    else:
        interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"

    total_count = 0

    if stop_time is not None:
        os.remove("sniffed_packets.pcap")
        print(f"Sniffing packets on interface {raw_interface} for {stop_time} seconds")
        total_count = 0
        total_packets = sniff(iface=interface, prn=packet_callback, timeout=stop_time)
        wrpcap("sniffed_packets.pcap", total_packets)
        for _ in total_packets:
            total_count += 1

        print("Time's up!")
        response_string = f"Sniffed {total_count} packets on interface {raw_interface} for {stop_time} seconds"
        processed_streamlit_data = process_packets(total_packets)

    else:
        response_string = "Please specify the duration in seconds of the packet capture."

    human_message = f"""
    {response_string}
    """
    try:
        custom_response = collect_messages_from_custom_prompts(human_message)
    except Exception as e:
        print("Duration packets response builder:", e)
        custom_response = f"Sniffed {total_count} packets on interface {raw_interface} for {stop_time} seconds"

    return custom_response
