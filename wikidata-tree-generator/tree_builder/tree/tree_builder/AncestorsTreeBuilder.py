#!/usr/bin/env python3
from logger.Logger import Logger
from tree_builder.CharacterFetcher import CharacterFetcher
from Config import Config
from tree_builder.tree.loader.AncestorsLoader import AncestorsLoader
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.tree_builder.TreeBuilder import TreeBuilder


class AncestorsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, config: Config, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(config)], config, logger)
