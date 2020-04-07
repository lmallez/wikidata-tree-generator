#!/usr/bin/env python3
from wikidata.entity import EntityId

from macros.WikidataProperties import Sex
from models.CharacterEntity import Properties, CharacterEntity
from services.ConfigService import ConfigService
from services.tree.loader.Loader import Loader


class DescendantsLoader(Loader):
    def __init__(self, config: ConfigService):
        super().__init__(config)

    def load(self, character: CharacterEntity) -> [EntityId]:
        if character.id in self.entity_cache:
            return []
        self.entity_cache.append(character.id)
        next_entity_ids = []
        if character.has_property(Properties.SEX):
            sex = character.get_property(Properties.SEX)
            if (sex == Sex.MALE and not self.config.load_men_child) or (sex == Sex.FEMALE and not self.config.load_women_child):
                return []
        if character.has_property(Properties.CHILD_IDS):
            next_entity_ids = character.get_property(Properties.CHILD_IDS)
        return next_entity_ids

