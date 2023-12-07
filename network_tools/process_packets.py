from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.all import *
from scapy.layers.inet import TCP, IP, UDP, ICMP
from scapy.layers.l2 import Ether
from custom_llm_prompt import construct_response_summary, construct_dns_response_summary


file_path = "sniffed_packets.pcap"

tcp_count = 0
udp_count = 0
icmp_count = 0
ip_count = 0
ether_count = 0
dns_count = 0
dns_query_count = 0
dns_answer_count = 0


def count_packet_protocols(pkts):
    global tcp_count, udp_count, icmp_count, ip_count, ether_count, dns_count, dns_query_count, dns_answer_count
    tcp_count = 0
    udp_count = 0
    icmp_count = 0
    ip_count = 0
    ether_count = 0
    dns_count = 0
    dns_query_count = 0
    dns_answer_count = 0

    for p in pkts:
        if p.haslayer(TCP):
            tcp_count += 1
        if p.haslayer(UDP):
            udp_count += 1
        if p.haslayer(ICMP):
            icmp_count += 1
        if p.haslayer(IP):
            ip_count += 1
        if p.haslayer(Ether):
            ether_count += 1
        if p.haslayer(DNS):
            dns_count += 1
        if p.haslayer(DNSQR):
            dns_query_count += 1
        if p.haslayer(DNSRR):
            dns_answer_count += 1
    packet_count_string = f" TCP: {tcp_count}, UDP: {udp_count}, ICMP: {icmp_count}, IP: {ip_count}, Ether: {ether_count}, DNS: {dns_count}, DNS Query: {dns_query_count}, DNS Answer: {dns_answer_count}"
    return packet_count_string


def process_predicted_packets(raw_user_input, prediction, website_name=None, user_name=None):
    filtered_packet_info = []
    all_packets = []
    # Load packets from the pcap file
    if os.path.exists(file_path):
        print("Reading the PCAP file")
        all_packets = rdpcap(file_path)
        # print(str(all_packets.summary()))
    if prediction == 'TCP':
        filtered_packet_info = []
        # print("TCP predicted")
        for p in all_packets:
            if p.haslayer(TCP):
                filtered_packet_info.append(p.summary())
    if prediction == 'DNS':
        # print("DNS predicted")

        for p in all_packets:
            if p.haslayer(DNS):
                filtered_packet_info.append(p.summary())
                # Match the IP address with the DNS request
                filtered_packet_info.append(dns_name_ip_mapping(p))
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
    # if website_name is not None:
    #     for p in all_packets:
    #         filtered_packet_info.append(domain_matching_ip(p, website_name))

    if prediction == 'All':
        filtered_packet_info = []
        for p in all_packets:
            filtered_packet_info.append(p.summary())

    common_protocol_count = count_packet_protocols(all_packets)

    # print("All Packets Summary: \n", str(all_packets))
    # print("All packets summary ends")
    # all_packets_summary_string = str(all_packets) + " " + common_protocol_count
    try:
        print("Building the custom response, getting summary")
        custom_response = construct_response_summary(None, common_protocol_count, str(filtered_packet_info))
    except Exception as e:
        print("Exception thrown in process_packets.process_predicted_packets:", e)
        custom_response = "I am sorry, I couldn't process your request. "

    return custom_response



def dns_name_ip_mapping(pkt):
    ip_to_domain_mapping = {}
    dns_string = ""
    # Check if the packet is a DNS packet (UDP and has DNS layer)
    if UDP in pkt and DNS in pkt:
        dns_query = pkt[DNS]

        # Check if it's a DNS query and has an answer
        if dns_query.qr == 0 and dns_query.an:
            # Extract the IP address and domain name from DNS answer
            if hasattr(dns_query, 'qd') and dns_query.qd and hasattr(dns_query.qd, 'qname') and dns_query.qd.qname:
                ip_address = dns_query.an.rdata
                domain_name = dns_query.qd.qname.decode()

                # Map IP address to domain name
                ip_to_domain_mapping[ip_address] = domain_name
                print(ip_to_domain_mapping)
                dns_string += f" {domain_name} => {ip_address}"

    return dns_string


# def domain_matching_ip(pckt, target_domain):
#     ip_addresses = set()
#     domain_string = ""
#     final_ip = None
#
#     if UDP in pckt and DNS in pckt:
#         dns_query = pckt[DNS]
#
#         # Check if it's a DNS response and has an answer
#         if dns_query.qr == 1 and dns_query.an:
#             # Extract the IP address and domain name from DNS answer
#             domain_name = dns_query.qd.qname.decode()
#             if domain_name == target_domain:
#                 # If the domain matches the target, extract IP addresses
#
#                 for answer in dns_query.an:
#                     if answer.type == 1:  # A record (IPv4 address)
#                         ip_addresses.add(answer.rdata)
#                         final_ip = answer.rdata
#     domain_string += (f" The website name {target_domain} is mapped to IP address {final_ip}.")
#
#     return domain_string

