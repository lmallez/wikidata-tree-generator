#!/usr/bin/env python3
from entity_filler.property_fillers.NameFiller import NameFiller
from models import CharacterEntity
from models.CharacterEntity import Properties
from models.Name import Name


class GivenNameFiller(NameFiller):
    def print(self, entity: Name, color=None):
        self.logger.log('Given Name | {} {}'.format(entity.id, entity.name), color)

    def process(self, entity: CharacterEntity):
        if Properties.GIVEN_NAME not in entity.keys():
            return
        given_names = entity[Properties.GIVEN_NAME]
        entity[Properties.GIVEN_NAME] = [self.get_entity(given_name) for given_name in given_names]
