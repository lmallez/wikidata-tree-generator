#!/usr/bin/env python3
from tree_builder.CharacterFetcherService import CharacterFetcherService
from ConfigService import ConfigService
from tree_builder.tree.loader.AncestorsLoader import AncestorsLoader
from tree_builder.tree.loader.DescendantsLoader import DescendantsLoader
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.tree_builder.TreeBuilder import TreeBuilder


class FullTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcherService, config: ConfigService, dispatcher: Dispatcher):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(config), DescendantsLoader(config)], config)
