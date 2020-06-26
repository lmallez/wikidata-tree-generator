#!/usr/bin/env python3
from entity_filler.property_fillers.NameFiller import NameFiller
from models import CharacterEntity
from models.CharacterEntity import Properties
from models.Name import Name


class FamilyNameFiller(NameFiller):
    def print(self, entity: Name, color=None):
        self.logger.log('Family Name | {} {}'.format(entity.id, entity.name), color)

    def process(self, entity: CharacterEntity):
        if Properties.FAMILY_NAME not in entity.keys():
            return
        family_names = entity[Properties.FAMILY_NAME]
        entity[Properties.FAMILY_NAME] = [self.get_entity(family_name) for family_name in family_names]
