#!/usr/bin/env python3
import sys
from enum import Enum


class Color(Enum):
    HEADER = 1
    OKBLUE = 2
    OKGREEN = 3
    WARNING = 4
    FAIL = 5
    ENDC = 6
    BOLD = 7
    UNDERLINE = 8


class Logger:
    def __print(self, file, log: str, color=None, end='\n'):
        if not color:
            print('{}{}'.format(log, end), end='', flush=True, file=file)
        else:
            color = self.__colors[color]
            print("{}{}{}{}".format(color, log, '\033[0m', end), end='', flush=True, file=file)

    def log(self, log: str, color=None, end='\n'):
        self.__print(sys.stdout, log, color, end)

    def error(self, log: str, color=None, end='\n'):
        self.__print(sys.stderr, log, color, end)

    __colors = {
        Color.HEADER: '\033[95m',
        Color.OKBLUE: '\033[94m',
        Color.OKGREEN: '\033[92m',
        Color.WARNING: '\033[93m',
        Color.FAIL: '\033[91m',
        Color.ENDC: '\033[0m',
        Color.BOLD: '\033[1m',
        Color.UNDERLINE: '\033[4m',
    }
