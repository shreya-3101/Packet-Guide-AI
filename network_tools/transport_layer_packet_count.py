from scapy.layers.inet import TCP, UDP, ICMP
from scapy.utils import PcapReader

from custom_llm_prompt import collect_messages_from_custom_prompts
from db_operations import retrieve_packets

# Variables to count packet types
tcp_count = 0
udp_count = 0
icmp_count = 0
other_count = 0


def packet_transport_layer(packets):
    global tcp_count, udp_count, icmp_count, other_count

    if packets.haslayer(TCP):
        tcp_count += 1
        # Additional processing for TCP packets
        # You can access TCP fields using packet[TCP].field_name
    elif packets.haslayer(UDP):
        udp_count += 1
        # Additional processing for UDP packets
        # You can access UDP fields using packet[UDP].field_name
    elif packets.haslayer(ICMP):
        icmp_count += 1
        # Additional processing for ICMP packets
        # You can access ICMP fields using packet[ICMP].field_name
    else:
        other_count += 1
        # Additional processing for other types of packets


def transport_layer_packets_count(user_name):
    pcap_path = "sniffed_packets.pcap"
    try:
        for packet in PcapReader(pcap_path):
            packet_transport_layer(packet)
    except FileNotFoundError:
        return "Please capture some network packets first."

    total_count = tcp_count + udp_count + icmp_count + other_count

    # Print the counts after sniffing is complete
    print(f"TCP: {tcp_count} packets")
    print(f"UDP: {udp_count} packets")
    print(f"ICMP: {icmp_count} packets")
    print(f"Other: {other_count} packets")
    print(f"Total: {total_count} packets")
    response_string = f"TCP: {tcp_count} packets\nUDP: {udp_count} packets\nICMP: {icmp_count} packets\nOther: {other_count} packets\nTotal: {total_count} packets"

    human_message = f"""
    {response_string}
    """
    custom_response = collect_messages_from_custom_prompts(human_message)
    return custom_response

