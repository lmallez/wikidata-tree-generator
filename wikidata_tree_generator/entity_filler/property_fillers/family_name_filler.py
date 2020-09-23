#!/usr/bin/env python3
from wikidata_tree_generator.entity_filler.property_fillers.name_filler import NameFiller
from wikidata_tree_generator.models.character import Character, Properties
from wikidata_tree_generator.models.name import Name


class FamilyNameFiller(NameFiller):
    def print(self, entity: Name, color=None):
        self.logger.log('Family Name | {} {}'.format(entity.id, entity.name), color)

    def process(self, entity: Character):
        if Properties.FAMILY_NAME not in entity.keys():
            return
        family_names = entity[Properties.FAMILY_NAME]
        entity[Properties.FAMILY_NAME] = [self.get_entity(family_name) for family_name in family_names]
