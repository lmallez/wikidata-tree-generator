#!/usr/bin/env python3
from dataclasses import dataclass, field
from enum import Enum


class TreeMethod(Enum):
    ANCESTORS = 1
    DESCENDANTS = 2
    FULL = 3
    CLASSIC = 4


class ExportFormat(Enum):
    GEDCOM = 1
    JSON = 2


@dataclass
class ThreadConfiguration:
    enable: bool = True
    max_thread: int = 10


@dataclass
class TreeConfiguration:
    method: TreeMethod = None
    generation_limit: bool = None
    load_fathers: bool = True
    load_mothers: bool = True
    load_men_children: bool = True
    load_women_children: bool = True
    branch_cache: bool = True


@dataclass
class ExportConfiguration:
    format: ExportFormat = None
    export_men: bool = True
    export_women: bool = True


@dataclass
class Configuration:
    entity_cache: bool = True
    tree_configuration: TreeConfiguration = field(default_factory=TreeConfiguration)
    thread_configuration: ThreadConfiguration = field(default_factory=ThreadConfiguration)
    export_configuration: ExportConfiguration = field(default_factory=ExportConfiguration)
    properties: list = field(default_factory=list)
