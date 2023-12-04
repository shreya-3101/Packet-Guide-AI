# from scapy.all import get_if_list, get_if_addr
#
# # Print the list of available interfaces and their names
# interfaces = get_if_list()
# print("Available interfaces:")
# for interface in interfaces:
#     interface_name = get_if_addr(interface)
#     print(f"Interface Name: {interface}, Interface Address: {interface_name}, ")

from scapy.all import *
import base64

from scapy.layers.dns import DNSQR, DNS

network_packets = rdpcap('sniffed_packets.pcap')
decoded_commands = []
decoded_data = ""
for packet in network_packets:
    print(packet)
    if DNSQR in packet:
        if packet[DNS].id == 0x1337:
            decoded_data = base64.b64decode(str(packet[DNS].an.rdata))
        if 'FILE:' in decoded_data:
            continue
        else:
            print(decoded_data)
            decoded_commands.append(decoded_data)
    print("No decoded data found")
for command in decoded_commands:
    print(command)
    if len(command) > 1:
        print(command.rstrip())
