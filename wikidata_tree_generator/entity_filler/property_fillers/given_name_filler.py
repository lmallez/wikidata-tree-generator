#!/usr/bin/env python3
from wikidata_tree_generator.entity_filler.property_fillers.name_filler import NameFiller
from wikidata_tree_generator.models.character import Character, Properties
from wikidata_tree_generator.models.name import Name


class GivenNameFiller(NameFiller):
    def print(self, entity: Name, color=None):
        self.logger.log('Given Name | {} {}'.format(entity.id, entity.name), color)

    def process(self, entity: Character):
        if Properties.GIVEN_NAME not in entity.keys():
            return
        given_names = entity[Properties.GIVEN_NAME]
        entity[Properties.GIVEN_NAME] = [self.get_entity(given_name) for given_name in given_names]
