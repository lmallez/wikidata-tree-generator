#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from models.CharacterEntity import Properties, CharacterEntity
from tree_builder.tree.loader.Loader import Loader


class AncestorsLoader(Loader):
    def __init__(self, configuration: TreeConfiguration):
        super().__init__(configuration)

    def load(self, character: CharacterEntity) -> [EntityId]:
        next_entity_ids = []
        if self.configuration.load_fathers and character.has_property(Properties.FATHER_ID):
            next_entity_ids.append(character.get_property(Properties.FATHER_ID))
        if self.configuration.load_mothers and character.has_property(Properties.MOTHER_ID):
            next_entity_ids.append(character.get_property(Properties.MOTHER_ID))
        return next_entity_ids
