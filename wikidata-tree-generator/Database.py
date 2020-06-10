#!/usr/bin/env python3
from wikidata.entity import EntityId


class Database:
    def __init__(self):
        self.cache = dict()

    def add(self, entity_id: EntityId, entity):
        if self.contains(entity_id):
            raise
        # useful for redirections
        if entity_id != entity.id:
            self.cache[entity_id] = entity
        self.cache[entity.id] = entity

    def remove(self, entity):
        if not self.contains(entity.id):
            raise
        del self.cache[entity.id]

    def get(self, key: EntityId):
        if not self.contains(key):
            raise
        return self.cache[key]

    def contains(self, key: EntityId):
        return key in self.cache.keys()
