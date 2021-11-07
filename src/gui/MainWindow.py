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
        self.initGUI()

    def initGUI(self):
        lbl1 = QLabel('Enter IP adress:', self)
        lbl2 = QLabel('Specify port: ', self)
        lbl3 = QLabel('Specify packet length: ', self)
        lbl4 = QLabel('Specify frequency value :', self)

        self.entry1 = QLineEdit(self)
        self.entry2 = QLineEdit(self)
        self.entry3 = QLineEdit(self)
        self.entry4 = QLineEdit(self)

        btn1 = QPushButton('Send packet', self)
        btn1.clicked.connect(self.sendTo)

        btn2 = QPushButton('Close', self)
        btn2.clicked.connect(self.close)

        grid = QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(lbl1, 0, 0)
        grid.addWidget(lbl2, 1, 0)
        grid.addWidget(lbl3, 2, 0)
        grid.addWidget(lbl4, 3, 0)
        grid.addWidget(self.entry1, 0, 1)
        grid.addWidget(self.entry2, 1, 1)
        grid.addWidget(self.entry3, 2, 1)
        grid.addWidget(self.entry4, 3, 1)
        grid.addWidget(btn1, 5, 0, 1, 3)
        grid.addWidget(btn2, 6, 2, 1, 1)

        self.setLayout(grid)
        self.setGeometry(600, 470, 600, 400)
        self.show()

    def sendTo(self):
        ip = str(self.entry1.text())
        port = int(self.entry2.text())
        length = int(self.entry3.text())
        freq = float(self.entry4.text())

        Flooder(ip, port, length, freq, 1)
