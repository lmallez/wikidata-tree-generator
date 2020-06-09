#!/usr/bin/env python3
from wikidata.entity import EntityId


class Database:
    def __init__(self):
        self.cache = dict()

    def add(self, entity_id: EntityId, character):
        if self.contains(entity_id):
            raise
        # useful for redirections
        if entity_id != character.id:
            self.cache[entity_id] = entity_id
        self.cache[character.id] = character

    def remove(self, character):
        if not self.contains(character.id):
            raise
        del self.cache[character.id]

    def get(self, key: EntityId):
        if not self.contains(key):
            raise
        return self.cache[key]

    def contains(self, key: EntityId):
        return key in self.cache.keys()
