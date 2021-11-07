from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QPushButton,
    QWidget
)


class Window(QWidget):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.setWindowTitle('Sending Packets')
        self.initGUI()

    def initGUI(self):
        labelFlood = QLabel('Flooding', self)

        buttonClose = QPushButton('Close', self)
        buttonClose.clicked.connect(self.close)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(1)

        gridLayout.addWidget(labelFlood, 1, 0)
        gridLayout.addWidget(buttonClose, 2, 1)

        self.setLayout(gridLayout)
        self.setGeometry(600, 470, 600, 400)
        self.show()
