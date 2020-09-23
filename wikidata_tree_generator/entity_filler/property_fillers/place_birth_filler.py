#!/usr/bin/env python3
from wikidata_tree_generator.entity_filler.property_fillers.place_filler import PlaceFiller
from wikidata_tree_generator.models.character import Character, Properties


class PlaceBirthFiller(PlaceFiller):
    def process(self, entity: Character):
        self.process_property(entity, Properties.PLACE_BIRTH)
