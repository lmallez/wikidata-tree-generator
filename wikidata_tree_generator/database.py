#!/usr/bin/env python3
from wikidata.entity import EntityId


class DatabaseException(BaseException):
    pass


class Database:
    def __init__(self):
        self.cache = dict()

    def set(self, entity_id: EntityId, entity):
        if entity_id != entity.id:
            self.cache[entity_id] = entity
        self.cache[entity.id] = entity

    def add(self, entity_id: EntityId, entity):
        if self.contains(entity_id):
            raise DatabaseException()
        # useful for redirections
        if entity_id != entity.id:
            self.cache[entity_id] = entity
        self.cache[entity.id] = entity

    def remove(self, entity):
        if not self.contains(entity.id):
            raise DatabaseException()
        del self.cache[entity.id]

    def get(self, key: EntityId):
        if not self.contains(key):
            raise DatabaseException()
        return self.cache[key]

    def contains(self, key: EntityId):
        return key in self.cache.keys()
