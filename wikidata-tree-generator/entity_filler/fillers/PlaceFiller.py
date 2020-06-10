#!/usr/bin/env python3from wikidata.entity import Entity
from wikidata.entity import Entity, EntityId

from Database import Database
from WikidataFetcher import WikidataFetcher
from models import CharacterEntity
from models.Place import Place
from tree_builder.PlacerBuilder import PlaceBuilder


class PlaceFiller:
    def __init__(self, fetcher: WikidataFetcher, database: Database, place_builder: PlaceBuilder):
        self.wikidata = fetcher
        self.database = database
        self.place_builder = place_builder

    def print(self, place: Place, start="", end=""):
        print("{}Place | {:>10} {}{}\n".format(
            start, place.id, place.name, end), flush=True, end='')

    def convert(self, entity: Entity) -> Place:
        return self.place_builder.build(entity)

    def get_place(self, place_id) -> Place:
        if self.database.contains(place_id):
            place = self.database.get(place_id)
            self.print(place, '\033[93m', '\033[0m')
            return place
        wikidata_entity = self.convert(self.wikidata.get(place_id))
        if not self.database.contains(place_id):
            self.database.add(place_id, wikidata_entity)
        else:
            place = self.database.get(place_id)
            self.print(place, '\033[94m', '\033[0m')
            return place
        self.print(wikidata_entity)
        return wikidata_entity

    def process_property(self, entity: CharacterEntity, prop: EntityId):
        if prop not in entity.keys():
            return
        place = entity[prop]
        entity[prop] = self.get_place(place)
