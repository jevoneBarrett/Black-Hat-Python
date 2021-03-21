'''
 !CLS
 To Capture packet frame ad infinitum run the following in scapy shell: sniff(iface="Wi-Fi", prn=lambda x: x.summary())
 For a detailed packet view run the following in the shell: sniff(count=1, iface="Wi-Fi", prn=lambda x: x.show())
 To send and return packet run the following: p = sendp(Ether()/"X", iface="Wi-Fi", return_packets=True)
 Send and receive one packet: p = sr1(IP(dst="8.8.4.4")/ICMP()/"TEST")
 Example DNS Query to Google: p = sr1(IP(dst="8.8.8.8")/UDP()/DNS(rd=1, qd=DNSQR(qname="YOUR_WEBSITE_HERE")))
 Example Send and Receive continuous to check ports: sr(IP(dst='TARGET_IP')/TCP(dport=[21, 22, 23, 80]))
 Ports: 21(FTP) 22(SSH) 23(TELNET) 80(HTTP)
 socket.getaddrinfo("example.com", None, socket.AF_INET6)
 socket.gethostbyaddr("162.159.136.234")

This is an example Discord Packet
###[ Ethernet ]###
  dst= e8:6f:38:47:ae:2d
  src= f8:2c:18:17:49:9d
  type= IPv4
###[ IP ]###
     version= 4
     ihl= 5
     tos= 0x0
     len= 114
     id= 48937
     flags= DF
     frag= 0
     ttl= 55
     proto= tcp
     chksum= 0x98e9
     src= 162.159.134.234
     dst= 192.168.1.65
     \options\
###[ TCP ]###
        sport= https
        dport= 57983
        seq= 2268454327
        ack= 3663286954
        dataofs= 5
        reserved= 0
        flags= PA
        window= 86
        chksum= 0x7e46
        urgptr= 0
        options= []
###[ Raw ]###
           load= '\x17\x03\x03\x00E \x1c$\xaay\x0e\x1e\x84\x97\xd3\x13.$\xebn\x97\xca\xc8V\xc7^\r1>\xc1\x9a4S\x85NZ\x8a\xc4\xf5\xa6p\xc4\xcd\xf7\xac%\x9eo%\xab\xb0\\Y+\xe5\xb0\x80\x84\xc7fd\x86\xf9}S\xbd>\xee\x04\xa0\xa3\xad{\x18'

<Sniffed: TCP:1 UDP:0 ICMP:0 Other:0>
'''

