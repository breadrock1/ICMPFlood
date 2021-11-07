from sys import exit, argv

from argparse import ArgumentParser
from PyQt5.QtWidgets import QApplication

from src.flooder import Flooder


def log_print() -> None:
    print(
            "   ___ _                 _           \n" +
            "  / __\ | ___   ___   __| | ___ _ __ \n" +
            " / _\ | |/ _ \ / _ \ / _` |/ _ \ '__|\n" +
            "/ /   | | (_) | (_) | (_| |  __/ |   \n" +
            "\/    |_|\___/ \___/ \__,_|\___|_|   \n"
    )


def main():
    argumentParser = ArgumentParser(
        prog='ICMP-Flooder',
        usage='''./launch.py MODE {gui | cmd}
                Mods details (Select one of those methods and '--help' to get more information about options):
                1. gui  - Allow you to run project with GUI interface;
                2. cmd  - Run project into terminal (options see further).
        ''',
        description='''
                This simple python project provides ability to flood by sending ICMP-packets to specified
                target IP/URL-address, port. Also you may set length, frequency of generated ICMP-packet.
        ''',
        add_help=True,
        allow_abbrev=True
    )

    mode = ''

    subArgumentParser = argumentParser.add_subparsers(title='Script Modes', dest=mode)
    subArgumentParser.add_parser('gui', help='launch with GUI')

    cmd = subArgumentParser.add_parser('cmd', help='launch from terminal')
    cmd.add_argument(
            '-i', metavar='--ip-address',
            help='Target ip address',
            required=True,
            type=str
    )
    cmd.add_argument(
            '-u', metavar='--url-address',
            help='Target url address',
            required=False, type=str
    )
    cmd.add_argument(
            '-p', metavar='--port-number',
            help='Target address port number',
            required=False,
            choices=range(0,65536),
            default=80,
            type=int
    )
    cmd.add_argument(
            '-t', metavar='--threads',
            help='Number of threads',
            required=False,
            default=1,
            type=int
    )
    cmd.add_argument(
            '-l', metavar='--packet-length',
            help='Packet length',
            required=False,
            default=60,
            type=int
    )
    cmd.add_argument(
            '-f', metavar='--packet-freq',
            help='Value of frequents',
            required=False,
            default=0.1,
            type=float
    )

    arguments = argumentParser.parse_args()

    if mode is "gui":
        app = QApplication(argv)
        MainWindow()
        exit(app.exec_())

    else:
        Flooder(arguments.i, arguments.p, arguments.l, arguments.f, arguments.t)


if __name__ == "__main__":
    log_print()
    main()
