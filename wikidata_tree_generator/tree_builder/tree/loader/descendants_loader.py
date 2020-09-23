#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.macros.wikidate_properties import Sex
from wikidata_tree_generator.models import Properties, Character
from .loader import Loader


class DescendantsLoader(Loader):
    def load(self, character: Character) -> [EntityId]:
        next_entity_ids = []
        if character.has_property(Properties.SEX):
            sex = character.get_property(Properties.SEX)
            if (sex == Sex.MALE and not self.configuration.load_men_children) or (sex == Sex.FEMALE and not self.configuration.load_women_children):
                return []
        if character.has_property(Properties.CHILD_IDS):
            next_entity_ids = character.get_property(Properties.CHILD_IDS)
        return next_entity_ids
