import pandas as pd
import re

# Sample network data string (you would replace this with the actual data)
data_string = """
Device wlp0s20f3 [10.52.14.64] (1/1):
Curr: 20.30 kBit/s
Incoming:
Avg: 20.30 kBit/s
Min: 20.30 kBit/s
Max: 20.30 kBit/s
Curr: 19.80 kBit/s
Outgoing:
Avg: 19.80 kBit/s
Min: 19.80 kBit/s
Max: 19.80 kBit/s
Ttl: 6.02 MByte
Device wlp0s20f3 [10.52.14.64] (1/1):
Curr: 31.71 kBit/s
Incoming:
Avg: 31.71 kBit/s
Min: 20.30 kBit/s
Max: 31.71 kBit/s
Curr: 10.56 kBit/s
Outgoing:
Avg: 10.56 kBit/s
Min: 10.56 kBit/s
Max: 19.80 kBit/s
Ttl: 6.02 MByte
Device wlp0s20f3 [10.52.14.64] (1/1):
Curr: 31.98 kBit/s
Incoming:
Avg: 28.09 kBit/s
Min: 20.30 kBit/s
Max: 31.98 kBit/s
Curr: 680.00 Bit/s
Outgoing:
Avg: 7.04 kBit/s
Min: 680.00 Bit/s
Max: 19.80 kBit/s
Ttl: 6.02 MByte
"""

# Function to parse the data and add a 'Network Quality' label
def parse_data_with_quality(data_string):
    # Regular expression pattern to match the required information
    pattern = r"Curr:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Incoming:\s+Avg:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Min:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Max:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Curr:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Outgoing:\s+Avg:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Min:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Max:\s*([\d.]+)\s*(kBit/s|Bit/s)\s+Ttl:\s*([\d.]+)\s*(MByte|Byte)"
    
    data_rows = []

    # Find all matches in the data string
    matches = re.findall(pattern, data_string)
    for match in matches:
        curr_incoming, incoming_unit, avg_incoming, _, min_incoming, _, max_incoming, _, curr_outgoing, outgoing_unit, avg_outgoing, _, min_outgoing, _, max_outgoing, _, ttl_value, ttl_unit = match

        # Convert units to standard scale if necessary (e.g., kBit/s to Bit/s)
        curr_incoming_val = float(curr_incoming) if incoming_unit == 'kBit/s' else float(curr_incoming) / 1000
        
        # Label network quality based on current incoming traffic
        if curr_incoming_val > 30:
            network_quality = 'good'
        elif 10 <= curr_incoming_val <= 30:
            network_quality = 'avg'
        else:
            network_quality = 'bad'
        
        # Create a row of data
        data_rows.append({
            'Curr_Incoming': curr_incoming_val,
            'Avg_Incoming': float(avg_incoming),
            'Min_Incoming': float(min_incoming),
            'Max_Incoming': float(max_incoming),
            'Curr_Outgoing': float(curr_outgoing),
            'Avg_Outgoing': float(avg_outgoing),
            'Min_Outgoing': float(min_outgoing),
            'Max_Outgoing': float(max_outgoing),
            'Ttl_Value': float(ttl_value),
            'Ttl_Unit': ttl_unit,
            'Network_Quality': network_quality
        })

    return pd.DataFrame(data_rows)

# Parse the data and create DataFrame with network quality labels
df = parse_data_with_quality(data_string)

# Save DataFrame to CSV
csv_file_path = '/home/sristy/Desktop/wifi-outage-prediction/data_monitoring/network_data_with_quality.csv'  # Update this path
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
print(df.head())
