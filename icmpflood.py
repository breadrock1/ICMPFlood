from argparse import ArgumentParser, Namespace
from logging import info
from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from icmpflood.gui.main_window import MainWindow
from icmpflood.flooder_runner import FlooderConsoleRunner


def log_print():
    info(
        msg="   ___ _                 _           \n"
            + "  / __\ | ___   ___   __| | ___ _ __ \n"
            + " / _\ | |/ _ \ / _ \ / _` |/ _ \ '__|\n"
            + "/ /   | | (_) | (_) | (_| |  __/ |   \n"
            + "\/    |_|\___/ \___/ \__,_|\___|_|   \n"
    )


def launch_gui():
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())


def launch_cmd(cmd_options: Namespace):
    FlooderConsoleRunner(
        threads_number=cmd_options.t,
        arguments={
            'ip': cmd_options.i,
            'port': cmd_options.p,
            'length': cmd_options.l,
            'frequency': cmd_options.f
        }
    ).run()


if __name__ == "__main__":
    log_print()

    argumentParser = ArgumentParser(
        prog='ICMP-Flooder',
        usage='''python3 launch.py { gui | cmd [options] }
                    There are two modes to use this simple application:
                    1. gui  - Allows to run application with GUI interface;
                    2. cmd  - Run application into terminal (print -h for more details).
            ''',
        description='''
                    There is simple python script that i had been implemented while studying at the University.
                    The main goal of current project was being familiarization with python programming language.
                    And i decided to implement this simple python script that provides flooding ability by sending 
                    empty ICMP-packets to specified target by passed IP or URL-address. Also this script provides 
                    additional options as settings up packet length, frequency of sending generated ICMP-packets 
                    and threads amount. So you're welcome! :)
            ''',
        add_help=True,
        allow_abbrev=True
    )

    subArgumentParser = argumentParser.add_subparsers(title='Script Modes', dest='mode', required=True)

    subArgumentParser.add_parser('gui', help='Allows to run application with GUI interface.')
    cmd = subArgumentParser.add_parser('cmd', help='Run application into terminal (print -h for more details).')

    cmd.add_argument('-u', metavar='--url', help='Target url-address', required=False, type=str)
    cmd.add_argument('-i', metavar='--ip', help='Target ip-address', required=True, type=str)
    cmd.add_argument('-p', metavar='--port', help='Target address port number (for ip-address)',
                     required=False, choices=range(0, 65536), default=80, type=int)

    cmd.add_argument('-t', metavar='--threads', help='Threads amount', required=False, default=1, type=int)
    cmd.add_argument('-l', metavar='--length', help='Packet frame length', required=False, default=60, type=int)
    cmd.add_argument('-f', metavar='--frequents', help='Frequents of sending', required=False, default=0.1, type=float)

    arguments = argumentParser.parse_args()

    launch_gui() if arguments.mode == "gui" else launch_cmd(arguments)
