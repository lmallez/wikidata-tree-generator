#!/usr/bin/env python3
from wikidata.entity import Entity
from wikidata_tree_generator.models.name import Name
from .property_filler import PropertyFiller


class NameFiller(PropertyFiller):
    def convert(self, entity: Entity) -> Name:
        return Name(entity.id, str(entity.label))
