#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from tree_builder.CharacterBuilderService import CharacterBuilderService
from Database import Database
from WikidataFetcher import WikidataFetcher


class CharacterFetcherService:
    def __init__(self, wikidata: WikidataFetcher, database: Database, builder: CharacterBuilderService):
        self.wikidata = wikidata
        self.database = database
        self.builder = builder

    def get(self, entity_id: EntityId) -> CharacterEntity:
        if self.database.contains(entity_id):
            return self.database.get(entity_id)
        entity = self.wikidata.get(entity_id)
        character = self.builder.build_character(entity)
        if not self.database.contains(entity_id):
            self.database.add(entity_id, character)
        return character
