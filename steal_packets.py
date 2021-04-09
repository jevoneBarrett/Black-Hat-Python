# Don't forget to run this as root!
from scapy.all import *
import time
import os


TIME_LIMIT = time.time() + 60

def main():
    if os.name == 'nt':
        inteface = "Wi-Fi"
    else:
        inteface = "en1"
    while time.time() < TIME_LIMIT:
        packets = sniff(iface=inteface)
    wrpcap("captured.pcap", packets)

if __name__=='__main__':
    main()