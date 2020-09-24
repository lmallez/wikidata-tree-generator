#!/usr/bin/env python3
from .builder import Builder
from ..logger import Logger
from ..macros import PropertyTag
from ..macros.property_meta import place_property_metas
from ..models import Entity, Place


class PlaceBuilder(Builder):
    def __init__(self, logger: Logger, property_tags: [PropertyTag]):
        super().__init__(logger, property_tags, place_property_metas)

    @staticmethod
    def create_new(entity: Entity):
        return Place(entity.id, str(entity.label))
