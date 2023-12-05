import pytz
from scapy.all import sniff, rdpcap
from scapy.layers.inet import IP, ICMP, UDP, TCP
from scapy.layers.l2 import Ether
from scapy.utils import wrpcap
from custom_llm_prompt import collect_messages_from_custom_prompts, construct_response_summary
import os
from scapy.all import *

processed_streamlit_data = []
file_path = "sniffed_packets.pcap"


# Print packet summary
def packet_callback(packet):
    # Print packet summary
    print(packet.summary())


def list_interfaces():
    """List all available network interfaces."""
    return get_if_list()


# Uses scapy to extract information regarding an individual packet
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


from scapy.all import *


def process_packets_detailed(packets):
    processed_data = []
    for single_packet in packets:
        utc_time = datetime.utcfromtimestamp(single_packet.time).replace(tzinfo=pytz.utc)
        # Convert UTC time to EST
        est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))
        # Basic packet details
        packet_info = {
            "Time": est_time.strftime('%Y-%m-%d %H:%M:%S %Z'),  # formatted as a string,
            "Length": len(single_packet),
            # "Protocol Layers": single_packet.summary(),
            "Info": single_packet.summary()  # or create a custom summary
        }

        # Ethernet layer
        if Ether in single_packet:
            packet_info["Ethernet Source"] = single_packet[Ether].src
            packet_info["Ethernet Destination"] = single_packet[Ether].dst

        # IP layer
        if IP in single_packet:
            packet_info["Source IP"] = single_packet[IP].src
            packet_info["Destination IP"] = single_packet[IP].dst

        # TCP layer
        if TCP in single_packet:
            packet_info["Source Port"] = single_packet[TCP].sport
            packet_info["Destination Port"] = single_packet[TCP].dport
            tcp_flags = single_packet[TCP].sprintf("%TCP.flags%")
            packet_info["TCP Flags"] = tcp_flags

        # UDP layer
        if UDP in single_packet:
            packet_info["Source Port"] = single_packet[UDP].sport
            packet_info["Destination Port"] = single_packet[UDP].dport

        # ICMP layer
        if ICMP in single_packet:
            packet_info["ICMP Type"] = single_packet[ICMP].type
            packet_info["ICMP Code"] = single_packet[ICMP].code

        # Payload length (if needed)
        packet_info["Payload Length"] = len(single_packet[Raw].load) if Raw in single_packet else 0

        processed_data.append(packet_info)

    return processed_data


# Sniff a particular number of packets on a specific interface
# def sniff_count_packets(raw_interface=r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}", count=None,
#                         user_name=None):
def sniff_count_packets(count=0, user_name=None):
    global processed_streamlit_data
    processed_streamlit_data = []
    # if raw_interface.lower() == "wifi":
    #     interface = r"\Device\NPF_{B39E2535-D0BA-4504-84C5-3ECD281ECDBE}"
    # elif raw_interface.lower() == "ethernet" or raw_interface.lower() == "eth0":
    #     interface = r"\Device\NPF_{D41ABC33-1765-4E8E-BCF1-B0907DB3166E}"
    # elif raw_interface.lower() == "loopback":
    #     interface = r"\Device\NPF_Loopback"
    # else:
    #     interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"
    total_count = 0

    if count is not None:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been removed.")
        else:
            print(f"File '{file_path}' does not exist.")
        # print(f"Sniffing {count} packets on interface {raw_interface}")
        print(f"Sniffing {count} packets on all interfaces")
        # total_packets = sniff(iface=interface, prn=packet_callback, count=count)
        total_packets = sniff(count=count)
        processed_streamlit_data = process_packets_detailed(total_packets)
        wrpcap("sniffed_packets.pcap", total_packets)
        print("Total packets:", total_packets)
        for p in total_packets:
            total_count += 1
            with open("sniffed_packets_string.txt", "a") as f:
                f.write(str(p))
                f.write("\n")

        print("Done sniffing!")

        # response_string = f"Sniffed {total_count} packets on interface {raw_interface}"
        response_string = f"Sniffed {total_count} packets on all interfaces"
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
        custom_response = f"Sniffed {total_count} packets on all interfaces"

    return custom_response


# Sniff network packets on a specific interface for a particular duration
# def sniff_packets_duration(raw_interface=r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}", stop_time=None,
#                            user_name=None):
def sniff_packets_duration(stop_time=None, user_name=None):
    global processed_streamlit_data
    processed_streamlit_data = []
    # if raw_interface.lower() == "wifi":
    #     interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"
    # elif raw_interface.lower() == "ethernet" or raw_interface.lower() == "eth0":
    #     interface = r"\Device\NPF_{D41ABC33-1765-4E8E-BCF1-B0907DB3166E}"
    # elif raw_interface.lower() == "loopback":
    #     interface = r"\Device\NPF_Loopback"
    # else:
    #     interface = r"\Device\NPF_{2273133D-4348-40B8-8B3C-56FE7E8A8D32}"

    total_count = 0

    if stop_time is not None:

        # Check if the file exists
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been removed.")
        else:
            print(f"File '{file_path}' does not exist.")

        # print(f"Sniffing packets on interface {raw_interface} for {stop_time} seconds")
        print(f"Sniffing packets for {stop_time} seconds")
        total_count = 0
        # total_packets = sniff(iface=interface, prn=packet_callback, timeout=stop_time)
        total_packets = sniff(timeout=stop_time)
        wrpcap("sniffed_packets.pcap", total_packets)
        for _ in total_packets:
            total_count += 1

        print("Time's up!")
        # response_string = f"Sniffed {total_count} packets on interface {raw_interface} for {stop_time} seconds"
        response_string = f"Sniffed {total_count} packets for {stop_time} seconds"
        processed_streamlit_data = process_packets_detailed(total_packets)

    else:
        response_string = "Please specify the duration in seconds of the packet capture."

    human_message = f"""
    {response_string}
    """
    try:
        custom_response = collect_messages_from_custom_prompts(human_message)
    except Exception as e:
        print("Duration packets response builder:", e)
        # custom_response = f"Sniffed {total_count} packets on interface {raw_interface} for {stop_time} seconds"
        custom_response = f"Sniffed {total_count} packets for {stop_time} seconds"

    return custom_response


def process_predicted_packets(raw_user_input, prediction, user_name):
    filtered_packet_info = []
    all_packets = []
    # Load packets from the pcap file
    if os.path.exists(file_path):
        print("Reading the PCAP file")
        all_packets = rdpcap(file_path)
        print(all_packets)
    if prediction == 'TCP':
        filtered_packet_info = []
        # print("TCP predicted")
        for p in all_packets:
            if p.haslayer(TCP):
                filtered_packet_info.append(p.summary())
    if prediction == 'IP':
        # print("IP predicted")
        filtered_packet_info = []
        for p in all_packets:
            if p.haslayer(IP):
                filtered_packet_info.append(p.summary())
    if prediction == 'UDP':
        # print("UDP predicted")
        filtered_packet_info = []
        for p in all_packets:
            if p.haslayer(UDP):
                filtered_packet_info.append(p.summary())
    if prediction == 'Ether':
        # print("Ether predicted")
        filtered_packet_info = []
        for p in all_packets:
            if p.haslayer(Ether):
                filtered_packet_info.append(p.summary())
    if prediction == 'ICMP':
        # print("ICMP predicted")
        filtered_packet_info = []
        for p in all_packets:
            if p.haslayer(ICMP):
                filtered_packet_info.append(p.summary())

    print("All Packets Summary: \n", str(all_packets.summary()))
    print("All packets summary ends")
    try:
        print("Building the custom response, getting summary")
        custom_response = construct_response_summary(raw_user_input, str(all_packets.summary()), str(filtered_packet_info))
    except Exception as e:
        print("Exception thrown:", e)
        custom_response = "I am sorry, I couldn't process your request. "

    return custom_response


def get_processed_packet_data():
    return processed_streamlit_data
