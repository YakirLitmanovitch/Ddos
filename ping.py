import subprocess
import time
import datetime


def ping_ip(ip_address, index, log_file = "pings_result_p.txt"):
    # Run the ping command (single ping)
    ping_result = subprocess.run(
        ["ping", "-c", "1", ip_address],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Get current timestamp
    timestamp = time.time()

    # Write results to log file
    with open(log_file, "a") as f:
        status = "SUCCESS" if ping_result.returncode == 0 else "FAILED"
        f.write(f"SEQ = {index} TTL[{timestamp}]\n")

        # If you want to include the actual ping output
        if ping_result.returncode == 0:
            for line in ping_result.stdout.split('\n'):
                if "time=" in line:
                    f.write(f"    {line.strip()}\n")

    return ping_result.returncode == 0


def main():
    # Configuration
    ip_address = "8.8.8.8"  # Change this to your target IP
    log_file = "ping_log.txt"
    interval = 5  # seconds

    # Initialize index
    index = 1

    print(f"Starting ping monitoring of {ip_address}")
    print(f"Logging results to {log_file}")

    try:
        while True:
            ping_ip(ip_address, index, log_file)
            index += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")


if __name__ == "__main__":
    main()
