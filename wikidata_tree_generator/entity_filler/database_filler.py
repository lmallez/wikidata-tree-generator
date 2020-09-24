#!/usr/bin/env python3
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import Entity
from .entity_filler import EntityFiller


class DatabaseFiller:
    def __init__(self, entity_filler: EntityFiller, database: Database, logger: Logger):
        self.entity_filler = entity_filler
        self.database = database
        self.logger = logger

    def print(self, entity):
        self.logger.log("Filler | {:>10}".format(entity.id))

    def load_entity(self, entity: Entity):
        self.entity_filler.load(entity)

    def process(self):
        for entity in self.database.cache.values():
            self.print(entity)
            self.entity_filler.load(entity)
