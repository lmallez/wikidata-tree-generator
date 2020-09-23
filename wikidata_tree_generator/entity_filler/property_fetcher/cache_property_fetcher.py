#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.entity_filler.property_fetcher import PropertyFetcher
from wikidata_tree_generator.logger import Color


class CachePropertyFetcher(PropertyFetcher):
    def get(self, entity_id: EntityId, convert_method, print_method):
        if self.database.contains(entity_id):
            entity = self.database.get(entity_id)
            print_method(entity, Color.OKGREEN)
            return entity
        return super().get(entity_id, convert_method, print_method)
