#!/usr/bin/env python3
from typing import Type

from wikidata.entity import EntityId
from wikidata_tree_generator.logger import Color
from wikidata_tree_generator.models import Entity
from .property_fetcher import PropertyFetcher


class CachePropertyFetcher(PropertyFetcher):
    def get(self, entity_id: EntityId, expected_type: Type[Entity]):
        if self.database.contains(entity_id):
            entity = self.database.get(entity_id)
            self.print(entity, expected_type, Color.OKGREEN)
            return entity
        return super().get(entity_id, expected_type)
