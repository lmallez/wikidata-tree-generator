#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.tree_builder.AncestorsTreeBuilder import AncestorsTreeBuilder
from tree_builder.tree.tree_builder.DescandantsTreeBuilder import DescendantsTreeBuilder


class ClassicTreeBuilder:
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        self.ancestors = AncestorsTreeBuilder(fetcher, configuration, dispatcher, logger)
        self.descendants = DescendantsTreeBuilder(fetcher, configuration, dispatcher, logger)

    def compute(self, entity_id: EntityId):
        self.ancestors.compute(entity_id)
        self.descendants.compute(entity_id)
