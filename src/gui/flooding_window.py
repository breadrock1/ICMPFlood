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
        self.setWindowTitle('Flooding')

        labelAddress = QLabel('Sending...', self)

        buttonClose = QPushButton('Close', self)
        buttonClose.clicked.connect(self.__close__all_threads)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(1)

        gridLayout.addWidget(labelAddress, 1, 0)
        gridLayout.addWidget(buttonClose, 2, 0)

        return gridLayout

    def show_window(self):
        self.__sendTo()
        self.show()

    def __close__all_threads(self):
        [self.thread.terminate() for self.thread in self.all_threads]
        self.close()

    def __build_flooder_thread(self):
        self.thread = QThread()
        self.flooder = Flooder(
            ip=self.address,
            port=self.port,
            length=self.length,
            frequency=self.frequency
        )

        self.flooder.moveToThread(self.thread)
        self.thread.started.connect(self.flooder.run)
        self.flooder.finished.connect(self.thread.quit)
        self.flooder.finish_signal.connect(
            self.__close__all_threads, QtCore.Qt.QueuedConnection)

        self.all_threads.append(self.thread)
        self.thread.start()

    def __sendTo(self):
        [self.__build_flooder_thread()\
            for number in range(0, self.num_threads)]
