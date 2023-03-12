from argparse import ArgumentParser, Namespace
from logging import info, error
from socket import gethostbyname
from sys import argv, exit

from icmpflood.flooder_runner import FlooderRunner


def log_print():
    info(
        msg="   ___ _                 _           \n"
            + "  / __\ | ___   ___   __| | ___ _ __ \n"
            + " / _\ | |/ _ \ / _ \ / _` |/ _ \ '__|\n"
            + "/ /   | | (_) | (_) | (_| |  __/ |   \n"
            + "\/    |_|\___/ \___/ \__,_|\___|_|   \n"
    )


def launch_gui():
    try:
        from PyQt5.QtWidgets import QApplication
        from icmpflood.gui.main_window import MainWindow

        app = QApplication(argv)
        window = MainWindow()
        window.show()
        exit(app.exec_())

    except ImportError as err:
        error(msg=f'Failed while importing PyQt5 libraries: {err}')
        error(msg=f'{argument_parser.usage}')


def launch_cmd(cmd_options: Namespace):
    ip_address = gethostbyname(cmd_options.u) if cmd_options.u else cmd_options.i
    FlooderRunner(
        threads_number=cmd_options.t,
        arguments={
            'address': ip_address,
            'port': cmd_options.p,
            'delay': cmd_options.d,
            'length': cmd_options.l
        }
    ).launch_flooder()


argument_parser = ArgumentParser(
        prog='ICMP-Flooder',
        usage='''python3 icmpflood.py { gui | cmd [options] }
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

sub_arg_parser = argument_parser.add_subparsers(title='Script Modes', dest='mode', required=True)
sub_arg_parser.add_parser('gui', help='Allows to run application with GUI interface.')
cmd_args = sub_arg_parser.add_parser('cmd', help='Run application into terminal (print -h for more details).')

cmd_args.add_argument('-u', metavar='--url', help='Target url-address', required=False, type=str)
cmd_args.add_argument('-i', metavar='--ip', help='Target ip-address', required=False, type=str)
cmd_args.add_argument('-p', metavar='--port', help='Target port number (for ip-address)',
                      required=False, choices=range(0, 65536), default=80, type=int)

cmd_args.add_argument('-t', metavar='--threads', help='Threads amount', required=False, default=1, type=int)
cmd_args.add_argument('-l', metavar='--length', help='Packet frame length', required=False, default=60, type=int)
cmd_args.add_argument('-d', metavar='--delay', help='Packet sending delay', required=False, default=0.1, type=float)


if __name__ == "__main__":
    log_print()

    arguments = argument_parser.parse_args()
    launch_gui() if arguments.mode == "gui" else launch_cmd(arguments)
