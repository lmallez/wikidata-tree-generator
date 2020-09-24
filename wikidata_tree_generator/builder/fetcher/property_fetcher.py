#!/usr/bin/env python3
from typing import Dict, Type

from wikidata.entity import EntityId
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.builder import Builder, PlaceBuilder, CharacterBuilder
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import Name, Character, Place, Entity
from wikidata_tree_generator.wikidata_fetcher import WikidataFetcher


builder_by_entity_type: Dict[Type[Entity], Type[Builder]] = {
    Name: Builder,
    Place: PlaceBuilder,
    Character: CharacterBuilder
}


class PropertyFetcher:
    def __init__(self, wikidata: WikidataFetcher, database: Database, logger: Logger):
        self.wikidata = wikidata
        self.database = database
        self.logger = logger
        self.builder = {obj_type: obj_builder(logger, obj_type.PROPERTIES) for obj_type, obj_builder in builder_by_entity_type.items()}

    def print(self, entity: Entity, expected_type: Type[Entity], color=None):
        self.logger.log("{:<10} {:<10} {}".format(entity.id, expected_type.__name__, entity.label), color)

    def get(self, entity_id: EntityId, expected_type: Type[Entity]):
        wiki_entity = self.wikidata.get(entity_id)
        entity = self.builder[expected_type].build(wiki_entity)
        self.database.set(entity_id, entity)
        self.print(entity, expected_type)
        return entity
