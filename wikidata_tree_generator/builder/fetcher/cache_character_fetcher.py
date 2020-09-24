#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.logger import Color
from wikidata_tree_generator.models import Character
from .character_fetcher import CharacterFetcher


class CacheCharacterFetcher(CharacterFetcher):
    def get(self, entity_id: EntityId) -> Character:
        if self.database.contains(entity_id):
            character = self.database.get(entity_id)
            self.print(entity_id, character, Color.OKGREEN)
            return character
        return super().get(entity_id)
