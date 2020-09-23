#!/usr/bin/env python3
from wikidata.entity import EntityId, Entity
from wikidata_tree_generator.entity_filler.property_fetcher import PropertyFetcher
from wikidata_tree_generator.logger.logger import Logger


class PropertyFiller:
    def __init__(self, fetcher: PropertyFetcher, logger: Logger):
        self.fetcher = fetcher
        self.logger = logger

    def print(self, entity: object, color=None):
        self.logger.log('Entity | {}'.format(entity.id), color)

    def convert(self, entity: Entity):
        raise Exception('not implemented')

    def get_entity(self, entity_id: EntityId):
        return self.fetcher.get(entity_id, self.convert, self.print)
