from datetime import datetime
from logging import error, warning
from typing import Any, Dict, List

from icmpflood.flooder import Flooder


class FlooderRunner:
    """
    This class extends threading.Thread class which provides ability to run
    any class with another thread. This class runs flooding with another threads.
    """

    JOIN_TIMEOUT = 5

    def __init__(self, threads_number: int, arguments: Dict[str, Any]):
        """
        The FlooderRunner class constructor.

        Args:
            threads_number (int): The amount of target threads.
            arguments (Dict[str, Any]): The dict of arguments for Flooder class.

        """

        self.arguments = arguments
        self.threads_num = threads_number

        self._threads: List[Flooder] = []

    def _interrupt_threads(self):
        """
        This method interrupts all running threads.
        """
        for thread in self._threads:
            thread.shutdown_flag.set()
            thread.join(FlooderRunner.JOIN_TIMEOUT)

        self._threads.clear()

    def _launch_threads(self):
        """
        This method initializing multiple threads by passed threads number option.
        """
        for thread_iter in range(0, self.threads_num):
            thread = Flooder(name=f'thread-{thread_iter}', arguments=self.arguments)
            self._threads.append(thread)
            thread.start()

    def launch_flooder(self):
        """
        This method runs with another thread to create ICMP-packet and send it
        to specified target ip-address.
        """

        try:
            start_time = datetime.now()
            self._launch_threads()
            while True:
                print('Packets sending duration: {}'.format(datetime.now() - start_time), end='\r')
                pass

        except KeyboardInterrupt:
            warning(msg='\nHas been triggered keyboard interruption!')
            warning(msg='Terminating all running threads...')

        except Exception as err:
            error(msg=f'Has been caught unknown runtime error: {err}')

        finally:
            self._interrupt_threads()
