import pandas as pd
import numpy as np
import re
import scapy.all as scapy

def preprocess_snmpwalk(file_path):
    """Preprocess SNMPWalk data to handle multi-line STRING values."""
    cleaned_lines = []
    buffer = ""

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("iso"):
                if buffer:
                    cleaned_lines.append(buffer.strip())
                buffer = line.strip()  
            else:
                buffer += " " + line.strip()

            if "End of MIB" in line:
                if buffer:
                    cleaned_lines.append(buffer.strip())
                    buffer = ""

    processed_lines = []
    for line in cleaned_lines:
        line = re.sub(r'=\s*STRING:\s*"(.*?)"', lambda m: '=' + m.group(0).replace("\n", " "), line)
        line = re.sub(r'\s+', ' ', line)

        if '=' in line:
            fields = line.split('=')
            if len(fields) == 2:
                processed_lines.append(line)

    cleaned_file_path = file_path.replace('.log', '_cleaned.log')
    with open(cleaned_file_path, 'w') as cleaned_file:
        cleaned_file.write("\n".join(processed_lines) + "\n")

    return cleaned_file_path

def extract_tcpdump_data(file_path):
    """Extract relevant information from TCPDump data."""
    packets = scapy.rdpcap(file_path)
    
    data = []
    for packet in packets:
        if scapy.IP in packet:
            data.append({
                'timestamp': packet.time,
                'src': packet[scapy.IP].src,
                'dst': packet[scapy.IP].dst,
                'size': len(packet)
            })

    return pd.DataFrame(data)

def load_data():
    """Load all data from different sources."""
    # Load VNStat data
    vnstat_data = pd.DataFrame()
    try:
        vnstat_data = pd.read_csv('data_monitoring/vnstat/traffic_stats.log', sep=';', header=None, skiprows=1)
        print("VNStat data loaded successfully.")
    except pd.errors.ParserError as e:
        print(f"Error loading VNStat data: {e}")
    except Exception as e:
        print(f"Unexpected error loading VNStat data: {e}")

    # Load Ping data
    ping_data = pd.DataFrame()
    try:
        ping_data = pd.read_csv('data_monitoring/ping/latency.log', sep=';', header=None)
        print("Ping data loaded successfully.")
    except Exception as e:
        print(f"Error loading Ping data: {e}")

    # Load TCPDump data
    tcpdump_data = extract_tcpdump_data('data_monitoring/tcpdump/traffic.pcap')

    # Load SNMPWalk data
    snmpwalk_data = pd.DataFrame()
    try:
        cleaned_file_path = preprocess_snmpwalk('data_monitoring/snmpwalk/snmp_data.log')
        snmpwalk_data = pd.read_csv(cleaned_file_path, sep='=', header=None, names=['OID', 'Value'])
        snmpwalk_data['Value'] = snmpwalk_data['Value'].str.strip() 
        print("SNMPWalk data loaded successfully.")
    except pd.errors.ParserError as e:
        print(f"Error loading SNMPWalk data: {e}")
    except Exception as e:
        print(f"Unexpected error loading SNMPWalk data: {e}")

    return vnstat_data, ping_data, tcpdump_data, snmpwalk_data

if __name__ == "__main__":
    vnstat_data, ping_data, tcpdump_data, snmpwalk_data = load_data()
