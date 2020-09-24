#!/usr/bin/env python3
from wikidata.entity import Entity
from wikidata_tree_generator.models import Place, Properties
from .builder import Builder
from ..logger import Logger
from ..macros.character_properties import place_property_metas


class PlaceBuilder(Builder):
    def __init__(self, logger: Logger, properties: [Properties]):
        super().__init__(logger, properties, place_property_metas)

    @staticmethod
    def create_new(entity: Entity):
        return Place(entity.id, str(entity.label))
