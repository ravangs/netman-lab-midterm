import NMtcpdump, NMdhcpserver, NMsnmp
from jinja2 import Template

## tcpdump
pcap_file = '/home/student/labs/labmidterm/ping_packet.pcap'
ip_mac_dict = {
        '2001:1:1:0:C802:35FF:FE4A:0': 'r2_mac',
        '2001:1:1:0:C803:35FF:FE68:0': 'r3_mac'
}

## dhcp server
r4 = {
    'device_type': 'cisco_ios',
    'host': '198.51.100.4',
    'username': 'admin',
    'password': 'admin',
    'secret': 'admin',
}

config_template = """
interface f0/0
ip address 198.51.101.5 255.255.255.0
no shutdown
exit
ip dhcp excluded-address 198.51.101.4 198.51.101.10                                                                                    
ip dhcp pool R2
host 198.51.101.2 255.255.255.0
hardware-address {{ r2_mac }} 
exit
ip dhcp pool R3
host 198.51.101.3 255.255.255.0
hardware-address {{ r3_mac }} 
exit
ip dhcp pool R4
network 198.51.101.0 255.255.255.0
default-router 198.51.101.5 
dns-server 198.51.101.5
exit
"""

#main method
def main():
    print("Starting Script...")
    ip_mac_details = NMtcpdump.extract_mac_addresses(pcap_file, '2001:1:1:0:',
                                                     {k.lower():v for k,v in ip_mac_dict.items()})

    template = Template(config_template)

    config_commands = template.render(ip_mac_details)

    r5_ip = NMdhcpserver.get_r5_ip(r4, ip_mac_details.values())

    print(f"DHCPv4 clients: {NMdhcpserver.configure_ipv4_dhcp(r4, r5_ip, config_commands)}")

    NMsnmp.run_snmp()

if __name__ == "__main__":
    main()
