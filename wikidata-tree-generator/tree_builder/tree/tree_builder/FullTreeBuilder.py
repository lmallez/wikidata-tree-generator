#!/usr/bin/env python3
from Configuration import TreeConfiguration
from logger.Logger import Logger
from tree_builder.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader.AncestorsLoader import AncestorsLoader
from tree_builder.tree.loader.DescendantsLoader import DescendantsLoader
from tree_builder.tree.tree_builder.TreeBuilder import TreeBuilder


class FullTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(configuration), DescendantsLoader(configuration)], configuration, logger)
