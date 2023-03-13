from typing import Any, Dict, Tuple

from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit
)

from icmpflood.gui.flooding_window import FloodingWorker


class MainWindow(QWidget):
    """
    This class extends PyQt5.QtWidgets.QWidget class which provides ability to build
    and show GUI window. This class build main window which provides ability to enter
    unnecessary data to run flooding.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.all_threads = []

        self.setLayout(self._build_gui())
        self.setGeometry(600, 470, 600, 400)

    def _build_gui(self) -> QGridLayout:
        """
        This method creates, configures and returns QGridLayout object with
        replaced into GUI elements.

        Returns:
            QGridLayout object.
        """

        self.setWindowTitle('ICMP Packet')

        self.statistic_label = QLabel("Setting up flooding data and press Start!", self)

        self.address_line_edit = QLineEdit(self)
        self.port_line_edit = QLineEdit(self)
        self.length_line_edit = QLineEdit(self)
        self.delay_line_edit = QLineEdit(self)
        self.threads_line_edit = QLineEdit(self)

        self.address_line_edit.setPlaceholderText('127.0.0.1')
        self.port_line_edit.setPlaceholderText('80')
        self.length_line_edit.setPlaceholderText('32')
        self.delay_line_edit.setPlaceholderText('0.1')
        self.threads_line_edit.setPlaceholderText('1')

        self.send_button = QPushButton('Start flooding', self)
        self.send_button.clicked.connect(self._send_packets_slot)

        self.close_button = QPushButton('Stop', self)
        self.close_button.clicked.connect(self._interrupt_threads)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(1)

        grid_layout.addWidget(QLabel('IP-address: ', self), 0, 0)
        grid_layout.addWidget(QLabel('Port number: ', self), 1, 0)
        grid_layout.addWidget(QLabel('Packet length: ', self), 2, 0)
        grid_layout.addWidget(QLabel('Frequency: ', self), 3, 0)
        grid_layout.addWidget(QLabel('Threads: ', self), 4, 0)

        grid_layout.addWidget(self.address_line_edit, 0, 1)
        grid_layout.addWidget(self.port_line_edit, 1, 1)
        grid_layout.addWidget(self.length_line_edit, 2, 1)
        grid_layout.addWidget(self.delay_line_edit, 3, 1)
        grid_layout.addWidget(self.threads_line_edit, 4, 1)

        grid_layout.addWidget(self.statistic_label, 5, 0, 1, 3)

        grid_layout.addWidget(self.send_button, 6, 0, 1, 3)
        grid_layout.addWidget(self.close_button, 7, 2, 1, 1)

        return grid_layout

    def _close(self):
        """
        This method just close current QWidget object.
        """

        self._interrupt_threads()
        self.close()

    def _interrupt_threads(self):
        """
        This method interrupts all running threads.
        """

        for thread in self.all_threads:
            thread.interrupt_worker()
            thread.terminate()

        self.all_threads.clear()
        self.send_button.setEnabled(True)
        self.statistic_label.setText("Setting up flooding data and press Start!")

    def _extract_entered_data(self) -> Tuple[int, Dict[str, Any]]:
        delay = self.delay_line_edit.text()
        address = self.address_line_edit.text()
        port = self.port_line_edit.text()
        length = self.length_line_edit.text()
        thread_nums = self.threads_line_edit.text()

        return (
            int(thread_nums) if thread_nums else 1,
            {
                'address':  address,
                'port':     int(port) if port else 80,
                'length':   int(length) if length else 32,
                'delay':    float(delay) if delay else 0.5
            }
        )

    def _send_packets_slot(self):
        """
        This method initializes the flooding window to run flooding.
        """

        thread_nums, arguments = self._extract_entered_data()
        for thread_iter in range(0, thread_nums):
            worker = FloodingWorker(
                name=f'thread-{thread_iter}',
                arguments=arguments
            )

            worker.start()
            self.all_threads.append(worker)

        self.send_button.setEnabled(False)
        self.statistic_label.setText("Flooding has been started!")
