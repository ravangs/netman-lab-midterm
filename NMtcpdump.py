import pyshark

def reverse_eui_64(last_64_bits):
    four_parts = last_64_bits.split(':')

    padded = [part.zfill(4) for part in four_parts]

    combined = ''.join(padded)

    hex_to_integer = int(combined, 16)

    flipped_first_eight_bits = (hex_to_integer >> 56) ^ 0x02

    combined_int = (flipped_first_eight_bits << 56) | (hex_to_integer & 0x00FFFFFFFFFFFFFF)

    combined_hex = format(combined_int,'0x')

    final_hex = combined_hex[:6] + combined_hex[10:]

    return '.'.join(final_hex[i:i+4] for i in range(0,12,4))


def extract_mac_addresses(pcap_file, ipv6_prefix, required_mac_dict):
    print(f'Extracting MAC addresses from {pcap_file}')
    pcap = pyshark.FileCapture(pcap_file, display_filter='ipv6')

    ipv6_set = set()
    ipv6_mac = {}

    for packet in pcap:
        try:
            ipv6_src = packet.ipv6.src

            if ipv6_src.startswith(ipv6_prefix):
                ipv6_set.add(ipv6_src)
        except AttributeError:
            continue

    for ipv6_address in ipv6_set:

        last_64_bits = ':'.join(ipv6_address.split(':')[-4:])
        ipv6_mac[ipv6_address] =reverse_eui_64(last_64_bits)
    
    host_mac = {required_mac_dict[ip]: ipv6_mac[ip] for ip in required_mac_dict}

    print(f'Extracted mac addresses: {host_mac}')
    
    return host_mac



