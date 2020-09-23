#!/usr/bin/env python3from wikidata.entity import Entity
from wikidata.entity import Entity, EntityId
from wikidata_tree_generator.entity_filler.property_fetcher.property_fetcher import PropertyFetcher
from wikidata_tree_generator.entity_filler.property_fillers.property_filler import PropertyFiller
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models.character import Character
from wikidata_tree_generator.models.place import Place
from wikidata_tree_generator.entity_builder.place_builder import PlaceBuilder


class PlaceFiller(PropertyFiller):
    def __init__(self, fetcher: PropertyFetcher, place_builder: PlaceBuilder, logger: Logger):
        super().__init__(fetcher, logger)
        self.place_builder = place_builder

    def print(self, entity: Place, color=None):
        self.logger.log('Place | {} {}'.format(entity.id, entity.name), color)

    def convert(self, entity: Entity) -> Place:
        return self.place_builder.build(entity)

    def process_property(self, entity: Character, prop: EntityId):
        if prop not in entity.keys():
            return
        entity[prop] = self.get_entity(entity[prop])
