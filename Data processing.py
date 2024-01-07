# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 18:10:40 2023

@author: raj_w20152
"""
import pandas as pd
from scapy.all import PcapReader, IP
import datetime

# Function to perform feature engineering on network data
def feature_engineering(df):
    # Packet Size Aggregation
    df['Packet Size per Second'] = df['Packet Size'].rolling(window=1).sum()

    # Time-Based Features
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour

    # Rolling Statistics
    df['Rolling Mean Packet Size'] = df['Packet Size'].rolling(window=5).mean()

    # Lag Features
    df['Latency Lag'] = df['Latency'].shift(1)

    # Protocol-Based Features
    protocol_counts = df['Protocol Type'].value_counts()
    df['Protocol Type Count'] = df['Protocol Type'].map(protocol_counts)

    # Binning
    bins = [0, 10, 50, 100, float('inf')]
    labels = ['Low', 'Medium', 'High', 'Very High']
    df['Latency Category'] = pd.cut(df['Latency'], bins=bins, labels=labels)

    # Rate Features
    df['Packet Arrival Rate'] = df.groupby('Source IP')['Timestamp'].diff().dt.total_seconds()

    # Feature Interaction
    df['Packet Size * Latency'] = df['Packet Size'] * df['Latency']

    # Categorical Encoding
    df = pd.get_dummies(df, columns=['Protocol Type'], prefix='Protocol')

    # Feature Scaling (Min-max scaling)
    df['Packet Size Scaled'] = (df['Packet Size'] - df['Packet Size'].min()) / (df['Packet Size'].max() - df['Packet Size'].min())

    return df

# Function to read a PCAP file and perform feature engineering
def process_pcap_file(pcap_file_path):
    try:
        # Reading packets from the PCAP file
        packets = list(PcapReader(pcap_file_path))
        
        # Feature extraction
        df = pd.DataFrame({
            'Timestamp': [datetime.datetime.fromtimestamp(packet.time) for packet in packets],
            'Packet Size': [len(packet) for packet in packets],
            'Source IP': [packet[IP].src if IP in packet else None for packet in packets],
            'Destination IP': [packet[IP].dst if IP in packet else None for packet in packets],
            'Protocol Type': [packet[IP].proto if IP in packet else None for packet in packets],
            'Latency': [(packet.time - packets[i - 1].time) if i > 0 else 0 for i, packet in enumerate(packets)],
        })

        # Perform feature engineering
        df = feature_engineering(df)

        # Display or return the resulting DataFrame
        print(df.head())
        return df

    except Exception as e:
        print(f"Error processing PCAP file: {e}")
        return None

# Example usage:
pcap_file_path = 'File path.csv'
processed_data = process_pcap_file(pcap_file_path)

# Save the processed data to a CSV file
if processed_data is not None:
    processed_data.to_csv('processed_data.csv', index=False)

