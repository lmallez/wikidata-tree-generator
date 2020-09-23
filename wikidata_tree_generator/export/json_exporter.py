#!/usr/bin/env python3
import json
from json import JSONEncoder
from wikidata.multilingual import MultilingualText
from .exporter import Exporter


class MultilingualEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, MultilingualText):
            return str(o)
        return o.__dict__


class JsonExporter(Exporter):
    def export(self, output_file: str):
        export_character = dict(filter(lambda x: self.allow_export(x[1]), self.database.cache.items()))
        file = open(output_file, "w+")
        json.dump(export_character, file, cls=MultilingualEncoder, indent=4)
        file.close()
        self.log(len(export_character), 'JSON', output_file)
