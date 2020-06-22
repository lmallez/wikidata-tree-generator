#!/usr/bin/env python3
from logger.Logger import Logger
from tree_builder.CharacterFetcher import CharacterFetcher
from Config import Config
from tree_builder.tree.loader.DescendantsLoader import DescendantsLoader
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.tree_builder.TreeBuilder import TreeBuilder


class DescendantsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, config: Config, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [DescendantsLoader(config)], config, logger)
