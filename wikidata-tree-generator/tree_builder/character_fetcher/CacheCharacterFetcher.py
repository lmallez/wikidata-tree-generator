#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import CharacterEntity
from tree_builder.CharacterBuilder import CharacterBuilder
from Database import Database
from WikidataFetcher import WikidataFetcher
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher


class CacheCharacterFetcher(CharacterFetcher):
    def __init__(self, wikidata: WikidataFetcher, database: Database, builder: CharacterBuilder):
        super().__init__(wikidata, database, builder)

    def get(self, entity_id: EntityId) -> CharacterEntity:
        if self.database.contains(entity_id):
            return self.database.get(entity_id)
        return super().get(entity_id)
