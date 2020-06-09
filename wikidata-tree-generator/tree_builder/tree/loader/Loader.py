#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from ConfigService import ConfigService


class Loader:
    def __init__(self, config: ConfigService,):
        self.config = config
        self.entity_cache = []

    def load(self, character: CharacterEntity) -> [EntityId]:
        pass

    def prof(self, prof: int) -> int:
        pass