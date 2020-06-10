#!/usr/bin/env python3
from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.fillers.PlaceFiller import PlaceFiller
from models import CharacterEntity
from models.CharacterEntity import Properties
from tree_builder.PlacerBuilder import PlaceBuilder


class PlaceBirthFiller(PlaceFiller):
    def __init__(self, fetcher: WikidataFetcher, database: Database, place_builder: PlaceBuilder):
        super().__init__(fetcher, database, place_builder)

    def process(self, entity: CharacterEntity):
        self.process_property(entity, Properties.PLACE_BIRTH)
