#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.tree_builder.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from .ancestors_tree_builder import AncestorsTreeBuilder
from .decendants_tree_builder import DescendantsTreeBuilder


class ClassicTreeBuilder:
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        self.ancestors = AncestorsTreeBuilder(fetcher, configuration, dispatcher, logger)
        self.descendants = DescendantsTreeBuilder(fetcher, configuration, dispatcher, logger)

    def compute(self, entity_id: EntityId):
        self.ancestors.compute(entity_id)
        self.descendants.compute(entity_id)
