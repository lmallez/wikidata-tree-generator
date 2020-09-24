#!/usr/bin/env python3

from wikidata.entity import Entity

from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import Properties, Character
from .builder import Builder
from ..macros.character_properties import character_property_metas


class CharacterBuilder(Builder):
    def __init__(self, logger: Logger, properties: [Properties]):
        super().__init__(logger, properties + [
            Properties.FATHER,
            Properties.MOTHER,
            Properties.CHILDREN,
        ], character_property_metas)

    @staticmethod
    def create_new(entity: Entity) -> Character:
        return Character(entity.id, str(entity.label))
