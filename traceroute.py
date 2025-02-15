import socket
import os
import sys
import struct
import time
import select
import binascii

# Program Level Comment: This program implements an ICMP Traceroute to trace the route to a destination host.

ICMP_ECHO_REQUEST = 8  # ICMP Echo Request Type
ICMP_TIME_EXCEEDED = 11  # ICMP Time Exceeded Type
ICMP_DEST_UNREACHABLE = 3  # ICMP Destination Unreachable Type
ICMP_ECHO_REPLY = 0  # ICMP Echo Reply Type
MAX_HOPS = 30  # Maximum number of hops before stopping
TIMEOUT = 2.0  # Timeout per request
TRIES = 2  # Number of tries per TTL
MAX_RUNTIME = 10  # Maximum execution time in seconds

def checksum(source_string):
    """Calculate checksum for ICMP packet."""
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count += 2
    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    """Create an ICMP Echo Request packet with a checksum."""
    my_checksum = 0
    my_id = os.getpid() & 0xFFFF
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, my_id, 1)
    data = struct.pack("d", time.time())
    my_checksum = checksum(header + data)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), my_id, 1)
    packet = header + data
    return packet

def get_route():
    """Interactive function to allow user input and trace the route dynamically."""
    hostname = input("Enter a hostname to trace route (e.g., google.com): ")
    timeLeft = TIMEOUT
    start_time = time.time()  # Track execution time
    
    for ttl in range(1, MAX_HOPS):
        if time.time() - start_time > MAX_RUNTIME:
            print("\nExecution time limit reached (10 seconds). Stopping trace.")
            return
        for tries in range(TRIES):
            try:
                destAddr = socket.gethostbyname(hostname)
                
                # Create raw socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
                mySocket.settimeout(TIMEOUT)
                
                packet = build_packet()
                mySocket.sendto(packet, (destAddr, 0))
                startTime = time.time()
                
                whatReady = select.select([mySocket], [], [], timeLeft)
                if whatReady[0] == []:
                    print(f"  {ttl}\t*\t*\t*\tRequest timed out.")
                    continue
                
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                icmpHeader = recvPacket[20:28]
                icmpType, _, _, _, _ = struct.unpack("bbHHh", icmpHeader)
                
                if icmpType == ICMP_TIME_EXCEEDED:
                    print(f"  {ttl}\trtt={int((timeReceived - startTime) * 1000)} ms\t{addr[0]}")
                elif icmpType == ICMP_ECHO_REPLY:
                    print(f"  {ttl}\trtt={int((timeReceived - startTime) * 1000)} ms\t{addr[0]}")
                    return
                elif icmpType == ICMP_DEST_UNREACHABLE:
                    print(f"  {ttl}\tDestination Unreachable")
                    return
            except socket.timeout:
                print(f"  {ttl}\t*\t*\t*\tRequest timed out.")
            except KeyboardInterrupt:
                print("\nTraceroute interrupted by user. Exiting gracefully.")
                return
            finally:
                mySocket.close()

if __name__ == "__main__":
    try:
        get_route()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")

