# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:48:36 2023

@author: rajshekharbhatta-w20152
National Tsinghua University, Taiwan
feature extraction from PCAP file
"""

# Import necessary libraries
# Import necessary libraries
import pandas as pd
from scapy.all import PcapReader, IP

# Defining variables in the global scope
num_packets, packet_sizes, source_ips, destination_ips, protocol_types = None, None, None, None, None

def filter_packets(pcap_file):
    # Function to read a PCAP file
    global num_packets, packet_sizes, source_ips, destination_ips, protocol_types

    try:
        # Reading packets from the PCAP file
        packets = list(PcapReader(pcap_file))  # Convert to list to get the length

        # Feature extraction
        num_packets = len(packets)
        packet_sizes = [len(packet) for packet in packets]
        source_ips = [packet[IP].src if IP in packet else None for packet in packets]
        destination_ips = [packet[IP].dst if IP in packet else None for packet in packets]
        protocol_types = [packet[IP].proto if IP in packet else None for packet in packets]

        # Display or return features as needed
        print("Number of Packets:", num_packets)
        print("Packet Sizes:", packet_sizes)
        print("Source IPs:", source_ips)
        print("Destination IPs:", destination_ips)
        print("Protocol Types:", protocol_types)

        # Create a DataFrame
        df = pd.DataFrame({
            'Packet Size': packet_sizes,
            'Source IP': source_ips,
            'Destination IP': destination_ips,
            'Protocol Type': protocol_types
        })

        # Export DataFrame to CSV
        csv_file_path = 'output_report.csv'
        df.to_csv(csv_file_path, index=False)
        print(f"CSV report created: {csv_file_path}")

        # You can add more features based on your requirements

    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

# Example usage:
pcap_file_path = 'C:\\NTHU\\Research@irat\\RA\\QoE_VR\\360-VR-QoE-In-band-QoS\\Data_Preprocess\\Raw_Data_Sample\\HTTPS(TCP)\\HTTP-1.1\\Persistant\\host-1_ts-60_thd-1_vpe-0_algo-0_bft-6_delay-5\\host-1_ts-60_thd-1_vpe-0_algo-0_bft-6_delay-5-1.pcap'
filter_packets(pcap_file_path)

# Access variables for further analysis or processing
print("Number of Packets:", num_packets)
print("Packet Sizes:", packet_sizes)
print("Source IPs:", source_ips)
print("Destination IPs:", destination_ips)
print("Protocol Types:", protocol_types)

    
    