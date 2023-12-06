from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
import matplotlib.pyplot as plt
from scapy.all import *
import streamlit as st
from custom_llm_prompt import collect_messages_from_custom_prompts


def analyze_packet_headers(packets):
    src_ip_count = {}
    dst_ip_count = {}
    protocol_count = {}
    custom_message = ""
    for packet in packets:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            # Count source and destination IP addresses
            src_ip_count[src_ip] = src_ip_count.get(src_ip, 0) + 1
            dst_ip_count[dst_ip] = dst_ip_count.get(dst_ip, 0) + 1
            custom_message += f" Source IP: {src_ip} and its count: {src_ip_count[src_ip]} is being displayed in the first graph."
            custom_message += f" Destination IP: {dst_ip} and its count: {dst_ip_count[dst_ip]} is being displayed in the second graph."
        if Ether in packet:
            protocol = packet[Ether].type
            protocol_name = get_protocol_name(protocol)
            # Count protocol distribution
            protocol_count[protocol_name] = protocol_count.get(protocol_name, 0) + 1
            custom_message += f" Protocol: {protocol_name} and its count: {protocol_count[protocol_name]} is being displayed in the third graph."
    # Plot source and destination IP addresses
    plot_ip_addresses(src_ip_count, "Source IP Addresses")
    plot_ip_addresses(dst_ip_count, "Destination IP Addresses")

    # Plot protocol distribution
    plot_protocol_distribution(protocol_count)

    human_message = f"""
        {custom_message}
        """
    try:
        print("Building the custom response...")
        custom_response = collect_messages_from_custom_prompts(human_message)
    except Exception as e:
        print("Count packets response builder:", e)
        custom_response = f"The below three graphs display the count of packets associated with the source IP, destination IP and protocol type respectively."
    return custom_response


def get_protocol_name(protocol):
    # Define a mapping of Ethernet protocol types to their string representations
    protocol_mapping = {
        0x0800: 'IPv4',
        0x86DD: 'IPv6',
        # Add more protocols as needed
    }
    # Return the protocol name or 'Unknown' if not found
    return protocol_mapping.get(protocol, f'Unknown ({hex(protocol)})')


def plot_ip_addresses(ip_count, title):
    plt.figure()
    plt.figure(figsize=(10, 6))
    plt.bar(ip_count.keys(), ip_count.values(), color='green', alpha=0.7)
    plt.title(title)
    plt.xlabel('IP Address')
    plt.ylabel('Packet Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)


def plot_protocol_distribution(protocol_count):
    plt.figure()
    plt.figure(figsize=(10, 6))
    plt.bar(protocol_count.keys(), protocol_count.values(), color='orange', alpha=0.7)
    plt.title('Protocol Distribution')
    plt.xlabel('Protocol Type')
    plt.ylabel('Packet Count')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)


## Gets called from OpenAI Function Agent
def pcap_display_graphs(dummy_property=None, user_name=None):
    # Read the pcap file
    pcap_file = 'sniffed_packets.pcap'
    packets = rdpcap(pcap_file)
    # Analyze packet headers
    response = analyze_packet_headers(packets)
    return response
