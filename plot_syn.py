import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd

# Function to parse the syn_results files
def parse_syn_results(filename):
    packet_times = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Extract values using regex
            match = re.search(r'SEQ = (\d+) TTL\[(.+?)\]', line)
            if match:
                seq_num = int(match.group(1))
                time_taken = float(match.group(2))
                
                # For the first packet, we don't have a previous to calculate time difference
                if seq_num == 1:
                    continue
                    
                # Calculate time needed to send this packet
                packet_times.append(time_taken / seq_num)  # Average time per packet
    
    return packet_times

# Parse data files
c_packet_times = parse_syn_results('syn_results_c')
python_packet_times = parse_syn_results('syn_results_p')

# Calculate statistics
c_avg = np.mean(c_packet_times)
c_std = np.std(c_packet_times)
python_avg = np.mean(python_packet_times)
python_std = np.std(python_packet_times)

print(f"C Implementation Statistics:")
print(f"Average time per packet: {c_avg:.6f} seconds")
print(f"Standard deviation: {c_std:.6f} seconds")
print()
print(f"Python Implementation Statistics:")
print(f"Average time per packet: {python_avg:.6f} seconds")
print(f"Standard deviation: {python_std:.6f} seconds")

# Create histogram for C implementation
plt.figure(figsize=(10, 6))
plt.hist(c_packet_times, bins=50, alpha=0.7, log=True)
plt.xlabel('Time to Send a Packet (seconds)')
plt.ylabel('Number of Packets (log scale)')
plt.title('Distribution of Packet Send Times - C Implementation')
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Syn_pkts_c.png')

# Create histogram for Python implementation
plt.figure(figsize=(10, 6))
plt.hist(python_packet_times, bins=50, alpha=0.7, log=True)
plt.xlabel('Time to Send a Packet (seconds)')
plt.ylabel('Number of Packets (log scale)')
plt.title('Distribution of Packet Send Times - Python Implementation')
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Syn_pkts_p.png')

# Create comparison plot
plt.figure(figsize=(12, 7))
plt.hist(c_packet_times, bins=50, alpha=0.6, label='C Implementation', log=True)
plt.hist(python_packet_times, bins=50, alpha=0.6, label='Python Implementation', log=True)
plt.xlabel('Time to Send a Packet (seconds)')
plt.ylabel('Number of Packets (log scale)')
plt.title('Comparison of Packet Send Times: C vs Python')
plt.legend()
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Syn_pkts_comparison.png')

# Additional analysis - Create percentile table for both implementations
def create_percentile_table(c_times, py_times):
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    c_percentiles = np.percentile(c_times, percentiles)
    py_percentiles = np.percentile(py_times, percentiles)
    
    data = {
        'Percentile': percentiles,
        'C (seconds)': c_percentiles,
        'Python (seconds)': py_percentiles,
        'Difference (Python/C)': py_percentiles / c_percentiles
    }
    
    df = pd.DataFrame(data)
    return df

percentile_table = create_percentile_table(c_packet_times, python_packet_times)
print("\nPercentile Analysis:")
print(percentile_table.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
