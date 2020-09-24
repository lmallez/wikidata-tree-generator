#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.macros.wikidata import Sex
from wikidata_tree_generator.models import Character
from .loader import Loader
from ...macros import PropertyTag


class DescendantsLoader(Loader):
    def load(self, character: Character) -> [EntityId]:
        next_entity_ids = []
        if character.has_property(PropertyTag.SEX):
            sex = character.get_property(PropertyTag.SEX).value
            if (sex == Sex.MALE and not self.configuration.load_men_children) or (sex == Sex.FEMALE and not self.configuration.load_women_children):
                return []
        if character.has_property(PropertyTag.CHILDREN):
            next_entity_ids = [child.loader for child in character.get_property(PropertyTag.CHILDREN)]
        return next_entity_ids
