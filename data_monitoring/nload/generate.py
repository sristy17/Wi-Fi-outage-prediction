import pandas as pd
import random

# Function to generate random data
def generate_random_network_data(num_rows=100):
    data_rows = []

    for _ in range(num_rows):
        # Randomly generate values for each column within realistic ranges
        curr_incoming = round(random.uniform(5.0, 40.0), 2)  # kBit/s
        avg_incoming = round(random.uniform(5.0, 40.0), 2)  # kBit/s
        min_incoming = round(random.uniform(5.0, curr_incoming), 2)  # kBit/s, less than or equal to current incoming
        max_incoming = round(random.uniform(curr_incoming, 50.0), 2)  # kBit/s, greater than or equal to current incoming

        curr_outgoing = round(random.uniform(0.5, 30.0), 2)  # kBit/s
        avg_outgoing = round(random.uniform(0.5, 30.0), 2)  # kBit/s
        min_outgoing = round(random.uniform(0.5, curr_outgoing), 2)  # kBit/s, less than or equal to current outgoing
        max_outgoing = round(random.uniform(curr_outgoing, 35.0), 2)  # kBit/s, greater than or equal to current outgoing

        ttl_value = round(random.uniform(1.0, 20.0), 2)  # MByte or Byte

        # Randomly assign network quality based on Curr_Incoming value
        if curr_incoming > 30:
            network_quality = 'good'
        elif 10 <= curr_incoming <= 30:
            network_quality = 'avg'
        else:
            network_quality = 'bad'

        # Append the row
        data_rows.append({
            'Curr_Incoming': curr_incoming,
            'Avg_Incoming': avg_incoming,
            'Min_Incoming': min_incoming,
            'Max_Incoming': max_incoming,
            'Curr_Outgoing': curr_outgoing,
            'Avg_Outgoing': avg_outgoing,
            'Min_Outgoing': min_outgoing,
            'Max_Outgoing': max_outgoing,
            'Ttl_Value': ttl_value,
            'Ttl_Unit': 'MByte',  # Assuming all values are in MByte
            'Network_Quality': network_quality
        })

    return pd.DataFrame(data_rows)

# Generate random data and create DataFrame
num_rows = 100  # Adjust the number of rows you want to generate
df = generate_random_network_data(num_rows)

# Save DataFrame to CSV
csv_file_path = '/home/sristy/Desktop/wifi-outage-prediction/ml_model/models/network_data.csv'  # Update this path
df.to_csv(csv_file_path, index=False)

print(f"Random data generated and saved to {csv_file_path}")
print(df.head())
