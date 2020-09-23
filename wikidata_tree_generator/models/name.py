#!/usr/bin/env python3
from wikidata.entity import EntityId


class Name:
    def __init__(self, id: EntityId, name: str = None):
        self.id = id
        self.name = name
