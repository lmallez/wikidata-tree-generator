#!/usr/bin/env python3
from enum import Enum


class TreeMethod(Enum):
    ANCESTORS = 1
    DESCENDANTS = 2
    FULL = 3
    CLASSIC = 4


class ExportFormat(Enum):
    GEDCOM = 1
    JSON = 2


class ThreadConfiguration:
    enable = True
    max_thread = 10


class TreeConfiguration:
    method = None
    generation_limit = None
    load_fathers = True
    load_mothers = True
    load_men_children = True
    load_women_children = True


class ExportConfiguration:
    format = None
    export_men = True
    export_women = True


class Configuration:
    tree_configuration = TreeConfiguration()
    thread_configuration = ThreadConfiguration()
    export_configuration = ExportConfiguration()
    properties = []
