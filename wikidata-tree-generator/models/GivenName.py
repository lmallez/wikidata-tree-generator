#!/usr/bin/env python3
from wikidata.entity import EntityId


class GivenName:
    def __init__(self, id: EntityId = None, given: str = None):
        self.id = id
        self.given = given
