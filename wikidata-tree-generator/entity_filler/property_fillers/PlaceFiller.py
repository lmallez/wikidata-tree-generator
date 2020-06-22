#!/usr/bin/env python3from wikidata.entity import Entity
from wikidata.entity import Entity, EntityId

from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.property_fillers.PropertyFiller import PropertyFiller
from logger.Logger import Logger
from models import CharacterEntity
from models.Place import Place
from tree_builder.PlacerBuilder import PlaceBuilder


class PlaceFiller(PropertyFiller):
    def __init__(self, fetcher: WikidataFetcher, database: Database, place_builder: PlaceBuilder, logger: Logger):
        super().__init__(fetcher, database, logger)
        self.place_builder = place_builder

    def print(self, entity: Place, color=None):
        self.logger.log('Place | {} {}'.format(entity.id, entity.name), color)

    def convert(self, entity: Entity) -> Place:
        return self.place_builder.build(entity)

    def process_property(self, entity: CharacterEntity, prop: EntityId):
        if prop not in entity.keys():
            return
        entity[prop] = self.get_entity(entity[prop])
