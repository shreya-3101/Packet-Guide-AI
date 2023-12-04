from scapy.all import get_if_list, get_if_addr
from scapy.interfaces import IFACES


def show_interfaces(resolve_mac=True):
    """Print list of available network interfaces"""
    return IFACES.show(resolve_mac)


# Print the list of available interfaces and their names
interfaces = get_if_list()
print("Available interfaces:")
for interface in interfaces:
    interface_name = get_if_addr(interface)
    print(f"Interface Name: {interface}, Interface Address: {interface_name}")
print(show_interfaces(True))
