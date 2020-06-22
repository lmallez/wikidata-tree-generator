#!/usr/bin/env python3
from Configuration import ExportConfiguration
from Database import Database
from logger import Logger


class Exporter:
    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        self.database = database
        self.properties = properties
        self.configuration = configuration
        self.logger = logger

    def export(self, output_file: str):
        pass
