#!/usr/bin/env python3
from entity_filler.property_fillers.PlaceFiller import PlaceFiller
from models import CharacterEntity
from models.CharacterEntity import Properties


class PlaceBirthFiller(PlaceFiller):
    def process(self, entity: CharacterEntity):
        self.process_property(entity, Properties.PLACE_BIRTH)
