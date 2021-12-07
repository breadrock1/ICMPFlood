from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit
)

from src.gui.flooding_window import FloodingWindow


class MainWindow(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.all_threads = list()

        self.setLayout(self._buildGUI())
        self.setGeometry(600, 470, 600, 400)

    def _buildGUI(self) -> QGridLayout:
        self.setWindowTitle('ICMP Packet')

        labelAddress = QLabel('IP-address: ', self)
        labelPortNum = QLabel('Port number: ', self)
        labelLength = QLabel('Packet length: ', self)
        labelFrequency = QLabel('Frequency: ', self)
        labelThreads = QLabel('Threads: ', self)

        self.editAddress = QLineEdit(self)
        self.exitPortNum = QLineEdit(self)
        self.editLength = QLineEdit(self)
        self.editFrequency = QLineEdit(self)
        self.editThreads = QLineEdit(self)

        buttonSend = QPushButton('Send packet', self)
        buttonSend.clicked.connect(self.__sendTo)

        buttonClose = QPushButton('Close', self)
        buttonClose.clicked.connect(self.__close)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(1)

        gridLayout.addWidget(labelAddress, 0, 0)
        gridLayout.addWidget(labelPortNum, 1, 0)
        gridLayout.addWidget(labelLength, 2, 0)
        gridLayout.addWidget(labelFrequency, 3, 0)
        gridLayout.addWidget(labelThreads, 4, 0)

        gridLayout.addWidget(self.editAddress, 0, 1)
        gridLayout.addWidget(self.exitPortNum, 1, 1)
        gridLayout.addWidget(self.editLength, 2, 1)
        gridLayout.addWidget(self.editFrequency, 3, 1)
        gridLayout.addWidget(self.editThreads, 4, 1)

        gridLayout.addWidget(buttonSend, 5, 0, 1, 3)
        gridLayout.addWidget(buttonClose, 6, 2, 1, 1)

        return gridLayout

    def __close(self):
        self.close()

    def __sendTo(self):
        address = str(self.editAddress.text())
        port_number = int(self.exitPortNum.text())
        num_threads = int(self.editThreads.text())
        packet_length = int(self.editLength.text())
        frequency = float(self.editFrequency.text())

        self.flooding_window = FloodingWindow(
            args={
                'ip': address,
                'port': port_number,
                'length': packet_length,
                'frequency': frequency,
                'threads': num_threads
            }
        )

        self.flooding_window.show_window()
