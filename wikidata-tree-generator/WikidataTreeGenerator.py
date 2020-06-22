#!/usr/bin/env python3
from wikidata.entity import EntityId


class WikidataTreeGenerator:
    def __init__(self, tree_builder, entity_filler, exporter):
        self.tree_builder = tree_builder
        self.entity_filler = entity_filler
        self.export = exporter

    def execute(self, entity_id: EntityId, output_file: str):
        self.tree_builder.compute(entity_id)
        self.entity_filler.process()
        self.export.export(output_file)
