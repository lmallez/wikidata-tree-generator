#!/usr/bin/env python3
from Configuration import TreeConfiguration
from logger.Logger import Logger
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader.DescendantsLoader import DescendantsLoader
from tree_builder.tree.tree_builder.TreeBuilder import TreeBuilder


class DescendantsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [DescendantsLoader(configuration)], configuration, logger)
