#!/usr/bin/env python3
import json
from json import JSONEncoder

from wikidata.entity import EntityId
from wikidata.multilingual import MultilingualText
from Configuration import ExportConfiguration
from Database import Database
from export.Exporter import Exporter
from logger.Logger import Logger


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        if type(o) is MultilingualText:
            return str(o)
        return o.__dict__


class JsonExporter(Exporter):
    def __init__(self, database: Database, properties: list, configuration: ExportConfiguration, logger: Logger):
        super().__init__(database, properties, configuration, logger)

    def export(self, output_file: str):
        export_character = dict(filter(lambda x: self.allow_export(x[1]), self.database.cache.items()))
        f = open(output_file, "w+")
        json.dump(export_character, f, cls=EmployeeEncoder, indent=4)
        f.close()
