#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import Properties, CharacterEntity
from ConfigService import ConfigService
from tree_builder.tree.loader.Loader import Loader


class AncestorsLoader(Loader):
    def __init__(self, config: ConfigService):
        super().__init__(config)
        self.entity_cache = []

    def load(self, character: CharacterEntity) -> [EntityId]:
        if character.id in self.entity_cache:
            return []
        self.entity_cache.append(character.id)
        next_entity_ids = []
        if self.config.load_fathers and character.has_property(Properties.FATHER_ID):
            next_entity_ids.append(character.get_property(Properties.FATHER_ID))
        if self.config.load_mothers and character.has_property(Properties.MOTHER_ID):
            next_entity_ids.append(character.get_property(Properties.MOTHER_ID))
        return next_entity_ids
