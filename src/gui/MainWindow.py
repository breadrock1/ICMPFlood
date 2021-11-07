from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QGridLayout,
    QPushButton,
    QWidget,
    QApplication,
    QLineEdit
)

from src.flooder import Flooder


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('ICMP Packet')
        self._buildGUI()

    def _buildGUI(self):
        labelAddress = QLabel('Enter IP adress:', self)
        labelPortNum = QLabel('Specify port: ', self)
        labelLength = QLabel('Specify packet length: ', self)
        labelFrequency = QLabel('Specify frequency value :', self)

        self.editAddress = QLineEdit(self)
        self.exitPortNum = QLineEdit(self)
        self.editLength = QLineEdit(self)
        self.editFrequency = QLineEdit(self)

        buttonSend = QPushButton('Send packet', self)
        buttonSend.clicked.connect(self.sendTo)

        buttonClose = QPushButton('Close', self)
        buttonClose.clicked.connect(self.close)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(1)

        gridLayout.addWidget(labelAddress, 0, 0)
        gridLayout.addWidget(labelPortNum, 1, 0)
        gridLayout.addWidget(labelLength, 2, 0)
        gridLayout.addWidget(labelFrequency, 3, 0)
        gridLayout.addWidget(self.editAddress, 0, 1)
        gridLayout.addWidget(self.exitPortNum, 1, 1)
        gridLayout.addWidget(self.editLength, 2, 1)
        gridLayout.addWidget(self.editFrequency, 3, 1)
        gridLayout.addWidget(buttonSend, 5, 0, 1, 3)
        gridLayout.addWidget(buttonClose, 6, 2, 1, 1)

        self.setLayout(gridLayout)
        self.setGeometry(600, 470, 600, 400)
        self.show()

    def sendTo(self):
        addr = str(self.editAddress.text())
        port = int(self.exitPortNum.text())
        length = int(self.editLength.text())
        freq = float(self.editFrequency.text())

        Flooder(addr, port, length, freq, 1)
