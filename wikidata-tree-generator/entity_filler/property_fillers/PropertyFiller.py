#!/usr/bin/env python3
from wikidata.entity import EntityId, Entity

from Database import Database
from WikidataFetcher import WikidataFetcher
from logger.Logger import Logger, Color


class PropertyFiller:
    def __init__(self, fetcher: WikidataFetcher, database: Database, logger: Logger):
        self.fetcher = fetcher
        self.database = database
        self.logger = logger

    def print(self, entity: object, color=None):
        self.logger.log('Entity | {}'.format(entity.id), color)

    def convert(self, entity: Entity):
        raise Exception('not implemented')

    def get_entity(self, entity_id: EntityId):
        if self.database.contains(entity_id):
            entity = self.database.get(entity_id)
            self.print(entity, Color.OKGREEN)
            return entity
        entity = self.convert(self.fetcher.get(entity_id))
        # in case the entity has already been found during the http request
        if self.database.contains(entity_id):
            entity = self.database.get(entity_id)
            self.print(entity, Color.OKBLUE)
            return entity
        self.database.add(entity_id, entity)
        self.print(entity)
        return entity
