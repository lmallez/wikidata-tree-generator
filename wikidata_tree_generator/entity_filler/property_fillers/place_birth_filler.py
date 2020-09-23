#!/usr/bin/env python3
from wikidata_tree_generator.models.character import Character, Properties
from .place_filler import PlaceFiller


class PlaceBirthFiller(PlaceFiller):
    def process(self, entity: Character):
        self.process_property(entity, Properties.PLACE_BIRTH)
