from typing import Dict, Any

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton
)

from src.flooder import Flooder


class FloodingWindow(QWidget):
    """
    This class extends PyQt5.QtWidgets.QWidget class which provides ability to build
    and show GUI window. This class build window which contains information about
    running flooding process.

    :argument:
        args (Dict[str, Any]):
            The arguments which user has been entered to flood.
        parent:
            The parent object (default = None).

    :attributes:
        all_threads (List):
            This container stored all running flooding threads.
        address (AnyStr):
            The target ip-address.
        port (int):
            The target port number.
        length (int):
            The length to build ICMP-packet.
        frequency (float):
            The frequency to send ICMP-packets.
        num_threads (int):
            The amount of threads to flood.
    """

    def __init__(self, args: Dict[str, Any], parent=None):
        QWidget.__init__(self, parent)

        self.all_threads = list()

        self.address = args.get('ip')
        self.port = args.get('port')
        self.length = args.get('length')
        self.frequency = args.get('frequency')
        self.num_threads = args.get('threads')

        self.setLayout(self._buildGUI())
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def _buildGUI(self) -> QGridLayout:
        """
        This method creates, configures and returns QGridLayout object with
        replaced into GUI elements.

        :return:
            QGridLayout object.
        """

        self.setWindowTitle('Flooding')

        labelAddress = QLabel('Sending...', self)

        buttonClose = QPushButton('Close', self)
        buttonClose.clicked.connect(self.__close__all_threads)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(1)

        gridLayout.addWidget(labelAddress, 1, 0)
        gridLayout.addWidget(buttonClose, 2, 0)

        return gridLayout

    def show_window(self) -> None:
        """
        This method provides ability to show initialized GUI window
        from another class which is invoked this method.
        """

        self.__sendTo()
        self.show()

    def __close__all_threads(self) -> None:
        """
        This method just terminates all running threads.
        """

        [self.thread.terminate() for self.thread in self.all_threads]
        self.close()

    def __sendTo(self) -> None:
        """
        There is wrapper method to code simplistic.
        """

        [self.__build_flooder_thread() for _ in range(0, self.num_threads)]

    def __build_flooder_thread(self) -> None:
        """
        This method just run flooding into another thread.
        """

        self.thread = QThread()
        self.flooder = Flooder(
            address=self.address,
            port_number=self.port,
            packet_length=self.length,
            sending_frequency=self.frequency
        )

        self.flooder.moveToThread(self.thread)
        self.thread.started.connect(self.flooder.run)
        self.flooder.finished.connect(self.thread.quit)
        self.flooder.finish_signal.connect(
            self.__close__all_threads, QtCore.Qt.QueuedConnection)

        self.all_threads.append(self.thread)
        self.thread.start()
