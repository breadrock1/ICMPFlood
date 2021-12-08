from typing import Dict, Any
from threading import Thread, Event

from src.flooder import Flooder


class FlooderConsoleRunner(Thread):

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

    def run(self) -> None:
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
