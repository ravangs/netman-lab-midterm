from netmiko import ConnectHandler
import time

prefix = '2001:1:1:'

def parse_dhcp_bindings_to_ip(output):
    ips = []
    lines = output.split('\n')
    
    for line in lines:
        text = line.split()

        if len(text) > 0:
            if '198.51.101' in text[0]:
                ips.append(text[0])
    
    return ips

def parse_ip_from_output(output, wrong_macs):
    lines = output.split('\n')

    for line in lines:
        if prefix in line:
            for mac in wrong_macs:
                if mac not in line:
                    return line.split()[0].strip()
        
def get_r5_ip(router_details, wrong_macs):
    r4_device = router_details.copy()
    with ConnectHandler(**r4_device) as net_connect:
        print("Connecting to R4 established")
        net_connect.enable()

        output = net_connect.send_command("show ipv6 neighbor")

        r5_ip = parse_ip_from_output(output, wrong_macs)
        print(f"IPv6 address of R5-F0/0: {r5_ip}")
        return r5_ip
    
def configure_ipv4_dhcp(router_details, r5_ip, config_commands):
    print("Starting DHCP setup")
    r5_device = router_details.copy()
    r5_device['host'] = r5_ip
    with ConnectHandler(**r5_device) as net_connect:
        print("Connection to R5 established")
        net_connect.enable()

        print("Configuring DHCP...")

        net_connect.send_config_set(config_commands.splitlines())
        time.sleep(60)
        print("Completed!")

        output = net_connect.send_command('show ip dhcp binding')
        return parse_dhcp_bindings_to_ip(output)

    






