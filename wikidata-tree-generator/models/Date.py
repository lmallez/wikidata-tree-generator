#!/usr/bin/env python3


class Date:
    def __init__(self, time: str, precision: int):
        self.time = time
        self.precision = precision

    def __repr__(self):
        return '{}!{}'.format(self.precision, self.time)
