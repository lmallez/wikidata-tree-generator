#!/usr/bin/env python3
from wikidata.entity import Entity

from entity_filler.property_fillers.PropertyFiller import PropertyFiller
from models.Name import Name


class NameFiller(PropertyFiller):
    def convert(self, entity: Entity) -> Name:
        return Name(entity.id, str(entity.label))