#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.models import CharacterEntity, Properties
from wikidata_tree_generator.tree_builder.tree.loader import Loader


class AncestorsLoader(Loader):
    def load(self, character: CharacterEntity) -> [EntityId]:
        next_entity_ids = []
        if self.configuration.load_fathers and character.has_property(Properties.FATHER_ID):
            next_entity_ids.append(character.get_property(Properties.FATHER_ID))
        if self.configuration.load_mothers and character.has_property(Properties.MOTHER_ID):
            next_entity_ids.append(character.get_property(Properties.MOTHER_ID))
        return next_entity_ids
