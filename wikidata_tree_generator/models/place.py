#!/usr/bin/env python3
from wikidata.entity import EntityId


class Place:
    def __init__(self, id: EntityId = None, name: str = None, latitude: float = None, longitude: float = None):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
