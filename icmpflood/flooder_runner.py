from typing import Dict, Any
from threading import Thread, Event

from icmpflood.flooder import Flooder


class FlooderConsoleRunner(Thread):
    """
    This class extends threading.Thread class which provides ability to run
    any class with another thread. This class runs flooding with another threads.
    """

    threads_number: int
    """The amount of threads to flood."""

    arguments: Dict[str, Any]
    """The arguments which user has been entered to flood."""

    def __init__(self, threads_number: int, arguments: Dict[str, Any]):
        Thread.__init__(self)

        self.args = arguments
        self.threads_num = threads_number

        self.all_threads = list()
        self.flooder = Flooder(
            address=self.args.get('ip'),
            port_number=self.args.get('port'),
            packet_length=self.args.get('length'),
            sending_frequency=self.args.get('frequency')
        )

    def run(self):
        """
        This method runs with another thread to create ICMP-packet and send it
        to specified target ip-address.
        """

        interrupt_event = Event()

        for thread_iter in range(0, self.threads_num):

            thread = Thread(
                daemon=True,
                target=self.flooder.run,
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
