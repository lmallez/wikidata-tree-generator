#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.models import Character


class Loader:
    def __init__(self, configuration: TreeConfiguration):
        self.configuration = configuration

    def load(self, character: Character) -> [EntityId]:
        pass
