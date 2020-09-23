#!/usr/bin/env python3
from wikidata.entity import Entity
from wikidata_tree_generator.macros.wikidate_properties import wikidata_properties
from wikidata_tree_generator.models import Place
from .builder import Builder, PropertyNotFoundException


class InvalidCoordinateException(PropertyNotFoundException):
    pass


class PlaceBuilder(Builder):
    def build(self, entity: Entity) -> Place:
        place = Place(entity.id)
        place.name = str(entity.label)
        try:
            self.get_coordinate_location(entity, place)
        except PropertyNotFoundException:
            self.logger.error('{}: coordinate impossible to get'.format(entity.id))
        return place

    def get_coordinate_location(self, entity: Entity, place: Place):
        coordinate = self.get_property(entity, wikidata_properties['coordinate_location'])
        if not coordinate:
            raise InvalidCoordinateException(entity.id, wikidata_properties['coordinate_location'])
        value = coordinate[0]['mainsnak']['datavalue']['value']
        place.latitude = value['latitude']
        place.longitude = value['longitude']
