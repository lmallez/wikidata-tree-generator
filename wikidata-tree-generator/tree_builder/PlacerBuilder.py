#!/usr/bin/env python3
from wikidata.entity import Entity

from logger.LoggerService import LoggerService
from macros.WikidataProperties import wikidata_properties
from models.Place import Place
from tree_builder.Builder import Builder


class PlaceBuilder(Builder):
    def __init__(self, logger: LoggerService):
        super().__init__(logger)

    def build(self, entity: Entity) -> Place:
        place = Place()
        place.id = entity.id
        place.name = str(entity.label)
        try:
            self.get_coordinate_location(entity, place)
        except:
            self.logger.log('{}: coordinate impossible to get'.format(entity.id))
        return place

    def get_coordinate_location(self, entity: Entity, place: Place):
        coordinate = self.get_property(entity, wikidata_properties['coordinate_location'])
        if not coordinate:
            raise
        value = coordinate[0]['mainsnak']['datavalue']['value']
        place.latitude = value['latitude']
        place.longitude = value['longitude']
