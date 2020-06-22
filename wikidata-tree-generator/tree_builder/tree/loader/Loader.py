#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from Configuration import TreeConfiguration


class Loader:
    def __init__(self, configuration: TreeConfiguration):
        self.configuration = configuration
        self.entity_cache = []

    def load(self, character: CharacterEntity) -> [EntityId]:
        pass

    def prof(self, prof: int) -> int:
        pass
