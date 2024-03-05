import json
from easysnmp import Session
import matplotlib.pyplot as plt
import time

community_string = 'public'
snmp_version = 2
routers = {
    'R1':'198.51.102.1',
    'R2':'198.51.102.2',
    'R3':'198.51.102.3',
    'R4':'198.51.100.4',
    'R5':'198.51.101.5'
}
snmp_data = {}

interface_oid = '1.3.6.1.2.1.2.2.1.2'
mapping_oid = '1.3.6.1.2.1.4.20.1.2'
ip_oid = '1.3.6.1.2.1.4.20.1.1'  
status_oid = '1.3.6.1.2.1.2.2.1.8'  
cpu_oid = '1.3.6.1.4.1.9.9.109.1.1.1.1.3'

def fetch_snmp_data(host, oid):
    session = Session(hostname=host, community=community_string, version=snmp_version)
    return session.walk(oid)

def run_snmp():
    print("Fetching SNMMP info")
    for router,ip in routers.items():

        snmp_data[router] = {}
        interface_names ={}
        ip_int_map = {}
        for item in fetch_snmp_data(ip, interface_oid):
            interface_names[item.oid_index] = item.value
        for item in fetch_snmp_data(ip, mapping_oid):
            ip_int_map[item.oid_index] = item.value
        for item in fetch_snmp_data(ip, ip_oid):
            interface_index = ip_int_map.get(item.oid_index)
            interface_name = interface_names.get(interface_index)
            if interface_name not in snmp_data[router]:
                snmp_data[router][interface_name] = {'ip': '', 'status': ''}
            snmp_data[router][interface_name]['ip'] = item.value
        
        for item in fetch_snmp_data(ip, status_oid):
            interface_name = interface_names.get(item.oid_index)
            if interface_name not in snmp_data[router]:
                snmp_data[router][interface_name] = {'ip': '', 'status': ''}
            snmp_data[router][interface_name]['status'] = 'up' if item.value == '1' else 'down'

    print("Saving data.txt")
    with open('data.txt', 'w') as file:
        json.dump(snmp_data, file, indent=4)


    print("Monitoring")
    cpu_usage = []
    end_time = time.time() + 120

    while time.time() < end_time:
        cpu_data = fetch_snmp_data(routers['R1'], cpu_oid)[0]
        if cpu_data.value.isdigit():
            cpu_usage.append(int(cpu_data.value))
        time.sleep(5)

    plt.plot([x*5 for x in range(len(cpu_usage))],cpu_usage)
    plt.title('CPU Utilization over Time')
    plt.xlabel('Time')
    plt.ylabel('CPU Utilization (%)')
    plt.savefig('cpu_utilization.jpg')
