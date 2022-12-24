from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit
)

from src.gui.flooding_window import FloodingWindow


class MainWindow(QWidget):
    """
    This class extends PyQt5.QtWidgets.QWidget class which provides ability to build
    and show GUI window. This class build main window which provides ability to enter
    unnecessary data to run flooding.

    :argument:
        parent:
            The parent object (default = None).

    :attributes:
        all_threads (List):
            This container stored all running flooding threads.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.all_threads = list()

        self.setLayout(self._buildGUI())
        self.setGeometry(600, 470, 600, 400)

    def _buildGUI(self) -> QGridLayout:
        """
        This method creates, configures and returns QGridLayout object with
        replaced into GUI elements.

        :return:
            QGridLayout object.
        """

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
        """
        This method just close current QWidget object.
        """

        self.close()

    def __sendTo(self):
        """
        This method initializes the flooding window to run flooding.
        """

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
