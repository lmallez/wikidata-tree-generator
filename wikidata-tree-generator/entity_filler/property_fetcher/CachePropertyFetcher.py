#!/usr/bin/env python3
from wikidata.entity import EntityId

from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.property_fetcher.PropertyFetcher import PropertyFetcher
from logger.Logger import Color


class CachePropertyFetcher(PropertyFetcher):
    def __init__(self, wikidata: WikidataFetcher, database: Database):
        super().__init__(wikidata, database)

    def get(self, entity_id: EntityId, convert_method, print_method):
        if self.database.contains(entity_id):
            entity = self.database.get(entity_id)
            print_method(entity, Color.OKGREEN)
            return entity
        return super().get(entity_id, convert_method, print_method)
