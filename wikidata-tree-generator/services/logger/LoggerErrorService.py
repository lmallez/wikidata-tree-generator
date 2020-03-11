#!/usr/bin/env python3
import sys

from services.logger.LoggerService import LoggerService


class LoggerErrorService(LoggerService):
    def log(self, log: str):
        print(log, file=sys.stderr)