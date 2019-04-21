import sys
import socket
import struct
import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QPushButton, QWidget, QApplication, QLineEdit

class MainWindow(QWidget):
    
    # Check data, calculated from the ICMP header and data
    def checksum(self, msg):
        summ = 0
        for i in range(0, len(msg), 2):
            w = msg[i] + (msg[i+1] << 8)
            summ = ((summ + w) & 0xffff) + ((summ + w) >> 16)
        return socket.htons(~summ & 0xffff)

    # Construct the header and data of packet and pack it
    def construct_packet(self, length, freq):
        header = struct.pack("bbHHh", 8, 0, 0, 1, 1)
        data = (length - 50) * 'Q'
        data = struct.pack("d", time.time()) + data.encode('ascii')
        header = struct.pack("bbHHh", 8, 0, socket.htons(self.checksum(header + data)), 1, 1)
        return header + data

    # Create socket to send packets to specified ip address
    # Close the created socket after using
    def create_socket(self):
        ip = str(self.entry1.text())
        port = int(self.entry2.text())
        length = int(self.entry3.text())
        freq = float(self.entry4.text())

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        
        for i in range(0, 6):
            packet = self.construct_packet(length, freq)
            sock.sendto(packet, (ip, port))
            time.sleep(freq)
    
        sock.close()

    # Main window for programm
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

        self.btn1 = QPushButton('Send packet', self)
        self.btn1.clicked.connect(self.create_socket)

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
        grid.addWidget(self.btn1, 5, 0, 1, 3)

        self.setLayout(grid)
        self.setGeometry(600, 470, 600, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
