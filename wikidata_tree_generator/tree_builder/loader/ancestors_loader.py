#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.models import Character, Properties
from .loader import Loader


class AncestorsLoader(Loader):
    def load(self, character: Character) -> [EntityId]:
        next_entity_ids = []
        if self.configuration.load_fathers and character.has_property(Properties.FATHER):
            next_entity_ids.append(character.get_property(Properties.FATHER).loader)
        if self.configuration.load_mothers and character.has_property(Properties.MOTHER):
            next_entity_ids.append(character.get_property(Properties.MOTHER).loader)
        return next_entity_ids
