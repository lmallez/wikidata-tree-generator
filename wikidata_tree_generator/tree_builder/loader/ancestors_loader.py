#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.models import Character
from .loader import Loader
from ...macros import PropertyTag


class AncestorsLoader(Loader):
    def load(self, character: Character) -> [EntityId]:
        next_entity_ids = []
        if self.configuration.load_fathers and character.has_property(PropertyTag.FATHER):
            next_entity_ids.append(character.get_property(PropertyTag.FATHER).loader)
        if self.configuration.load_mothers and character.has_property(PropertyTag.MOTHER):
            next_entity_ids.append(character.get_property(PropertyTag.MOTHER).loader)
        return next_entity_ids
