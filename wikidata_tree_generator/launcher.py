#!/usr/bin/env python3
from wikidata.entity import EntityId

from wikidata_tree_generator.entity_filler.database_filler import DatabaseFiller
from wikidata_tree_generator.export import Exporter
from wikidata_tree_generator.tree_builder.tree_builder import TreeBuilder


class Launcher:
    def __init__(self, tree_builder: TreeBuilder, filler: DatabaseFiller, exporter: Exporter):
        self.tree_builder = tree_builder
        self.filler = filler
        self.export = exporter

    def execute(self, entity_id: EntityId, output_file: str):
        self.tree_builder.compute(entity_id)
        self.filler.process()
        self.export.export(output_file)
