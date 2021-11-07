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
