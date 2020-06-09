#!/usr/bin/env python3
import sys

from logger.LoggerService import LoggerService


class LoggerErrorService(LoggerService):
    def log(self, log: str):
        print(log, file=sys.stderr)