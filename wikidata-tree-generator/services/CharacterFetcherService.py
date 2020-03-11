#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from services.CharacterBuilderService import CharacterBuilderService
from services.DatabaseService import DatabaseService
from services.WikidataFetcherService import WikidataFetcherService


class CharacterFetcherService:
    def __init__(self, wikidata: WikidataFetcherService, database: DatabaseService, builder: CharacterBuilderService):
        self.wikidata = wikidata
        self.database = database
        self.builder = builder

    def get(self, entity_id: EntityId) -> CharacterEntity:
        if self.database.contains(entity_id):
            return self.database.get(entity_id)
        entity = self.wikidata.get(entity_id)
        character = self.builder.build_character(entity)
        self.database.add(entity_id, character)
        return character
