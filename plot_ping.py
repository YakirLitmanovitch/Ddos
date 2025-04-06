import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd

# Function to parse the ping results files
def parse_ping_results(filename):
    rtts = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Look for RTT information in ping output
            # This regex might need adjustment based on your actual file format
            match = re.search(r'time=(\d+\.?\d*)\s*ms', line)
            if match:
                rtt = float(match.group(1))
                rtts.append(rtt)
    
    return rtts

# Parse data files
c_rtts = parse_ping_results('ping_results_c')
python_rtts = parse_ping_results('ping_results_p')

# Calculate statistics
c_avg = np.mean(c_rtts)
c_std = np.std(c_rtts)
python_avg = np.mean(python_rtts)
python_std = np.std(python_rtts)

print(f"C Implementation Statistics:")
print(f"Average RTT: {c_avg:.2f} ms")
print(f"Standard deviation: {c_std:.2f} ms")
print()
print(f"Python Implementation Statistics:")
print(f"Average RTT: {python_avg:.2f} ms")
print(f"Standard deviation: {python_std:.2f} ms")

# Create histogram for C implementation
plt.figure(figsize=(10, 6))
plt.hist(c_rtts, bins=50, alpha=0.7, log=True)
plt.xlabel('RTT (milliseconds)')
plt.ylabel('Number of Pings (log scale)')
plt.title('Distribution of Ping RTTs - C Implementation')
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Pings_c.png')

# Create histogram for Python implementation
plt.figure(figsize=(10, 6))
plt.hist(python_rtts, bins=50, alpha=0.7, log=True)
plt.xlabel('RTT (milliseconds)')
plt.ylabel('Number of Pings (log scale)')
plt.title('Distribution of Ping RTTs - Python Implementation')
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Pings_p.png')

# Create comparison plot
plt.figure(figsize=(12, 7))
plt.hist(c_rtts, bins=50, alpha=0.6, label='C Implementation', log=True)
plt.hist(python_rtts, bins=50, alpha=0.6, label='Python Implementation', log=True)
plt.xlabel('RTT (milliseconds)')
plt.ylabel('Number of Pings (log scale)')
plt.title('Comparison of Ping RTTs: C vs Python')
plt.legend()
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.tight_layout()
plt.savefig('Pings_comparison.png')

# Additional analysis - Create percentile table for both implementations
def create_percentile_table(c_times, py_times):
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    c_percentiles = np.percentile(c_times, percentiles)
    py_percentiles = np.percentile(py_times, percentiles)
    
    data = {
        'Percentile': percentiles,
        'C (ms)': c_percentiles,
        'Python (ms)': py_percentiles,
        'Ratio (Python/C)': py_percentiles / c_percentiles
    }
    
    df = pd.DataFrame(data)
    return df

percentile_table = create_percentile_table(c_rtts, python_rtts)
print("\nPercentile Analysis:")
print(percentile_table.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
