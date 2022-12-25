# ICMP-flooder

![GitHub version](https://img.shields.io/badge/version-v1.2.0-green?style=plastic&labelColor=dark)

[![Building Project](https://github.com/breadrock1/ICMPFlood/actions/workflows/build-project-action.yml/badge.svg?branch=master)](https://github.com/breadrock1/ICMPFlood/actions/workflows/build-project-action.yml)

There is simple python script that i had been implemented while studying at the University.
The main goal of current project was being familiarization with python programming language.
And i decided to implement this simple python script that provides flooding ability by sending
empty ICMP-packets to specified target by passed IP or URL-address. Also this script provides
additional options as settings up packet length, frequency of sending generated ICMP-packets
and threads amount. So you're welcome! :) 

## Usage

```shell

usage: python3 launch.py { gui | cmd [options] }
                    There are two modes to use this simple application:
                    1. gui  - Allows to run application with GUI interface;
                    2. cmd  - Run application into terminal (print -h for more details).
            

There is simple python script that i had been implemented while studying at the University. 
The main goal of current project was being familiarization with python programming language. 
And i decided to implement this simple python script that provides flooding ability by sending 
empty ICMP-packets to specified target by passed IP or URL-address. Also this script provides 
additional options as settings up packet length, frequency of sending generated ICMP-packets 
and threads amount. So you're welcome! :)

optional arguments:
  -h, --help  show this help message and exit

Script Modes:
  {gui,cmd}
    gui       Allows to run application with GUI interface.
    cmd       Run application into terminal (print -h for more details).

```

## License

MIT License

Copyright (c) 2022 Bread White

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

