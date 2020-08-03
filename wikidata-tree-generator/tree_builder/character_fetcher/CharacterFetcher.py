#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from tree_builder.CharacterBuilder import CharacterBuilder
from Database import Database
from WikidataFetcher import WikidataFetcher


class CharacterFetcher:
    def __init__(self, wikidata: WikidataFetcher, database: Database, builder: CharacterBuilder):
        self.wikidata = wikidata
        self.database = database
        self.builder = builder

    def get(self, entity_id: EntityId) -> CharacterEntity:
        character = self.builder.build(self.wikidata.get(entity_id))
        self.database.set(entity_id, character)
        return character
