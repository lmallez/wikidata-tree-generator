#!/usr/bin/env python3

from wikidata.entity import Entity

from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import Character
from .builder import Builder
from ..macros import PropertyTag
from ..macros.property_meta import character_property_metas


class CharacterBuilder(Builder):
    def __init__(self, logger: Logger, properties: [PropertyTag]):
        super().__init__(logger, properties, character_property_metas)

    @staticmethod
    def create_new(entity: Entity) -> Character:
        return Character(entity.id, str(entity.label))
