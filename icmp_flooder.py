import sys
import socket
import struct
import time
import icmp_flooder_cmd
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QPushButton, QWidget, QApplication, QLineEdit


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

        icmp_flooder_cmd.Flooder(ip, port, length, freq, 1)


class Window(QWidget):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.setWindowTitle('Sending Packets')
        self.initGUI()

    def initGUI(self):
        lbl1 = QLabel('Flooding', self)
        
        btn1 = QPushButton('Close', self)
        btn1.clicked.connect(self.close)

        grid = QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(lbl1, 1, 0)
        grid.addWidget(btn1, 2, 1)

        self.setLayout(grid)
        self.setGeometry(600, 470, 600, 400)
        self.show()


# class Flooder:
#     @staticmethod
#     def checksum(msg):
#         s = 0
#         for i in range(0, len(msg), 2):
#             w = msg[i] + (msg[i+1] << 8)
#             s = ((s + w) & 0xffff) + ((s + w) >> 16)
#         return socket.htons(~s & 0xffff)
#
#     def construct_packet(self, length):
#         header = struct.pack("bbHHh", 8, 0, 0, 1, 1)
#         data = (length - 50) * 'Q'
#         data = struct.pack("d", time.time()) + data.encode('ascii')
#         header = struct.pack("bbHHh", 8, 0, socket.htons(self.checksum(header + data)), 1, 1)
#         return header + data
#
#     def create_socket(self, ip, port, length, freq):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
#         for i in range(0, 10):
#             packet = self.construct_packet(length)
#             sock.sendto(packet, (ip, port))
#             time.sleep(freq)
#
#         sock.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
