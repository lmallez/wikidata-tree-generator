#!/usr/bin/env python3
from wikidata.entity import EntityId

from logger.Logger import Logger, Color
from models.CharacterEntity import CharacterEntity
from tree_builder.CharacterBuilder import CharacterBuilder
from Database import Database
from WikidataFetcher import WikidataFetcher
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher


class CacheCharacterFetcher(CharacterFetcher):
    def __init__(self, wikidata: WikidataFetcher, database: Database, builder: CharacterBuilder, logger: Logger):
        super().__init__(wikidata, database, builder, logger)

    def get(self, entity_id: EntityId) -> CharacterEntity:
        if self.database.contains(entity_id):
            character = self.database.get(entity_id)
            self.print(entity_id, character, Color.OKGREEN)
            return character
        return super().get(entity_id)
