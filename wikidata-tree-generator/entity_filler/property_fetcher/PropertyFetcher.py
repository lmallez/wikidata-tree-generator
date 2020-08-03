#!/usr/bin/env python3
from wikidata.entity import EntityId

from Database import Database
from WikidataFetcher import WikidataFetcher


class PropertyFetcher:
    def __init__(self, wikidata: WikidataFetcher, database: Database):
        self.wikidata = wikidata
        self.database = database

    def get(self, entity_id: EntityId, convert_method, print_method):
        entity = convert_method(self.wikidata.get(entity_id))
        self.database.set(entity_id, entity)
        print_method(entity)
        return entity
