#!/usr/bin/env python3
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.tree_builder.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.tree.loader import AncestorsLoader
from .tree_builder import TreeBuilder


class AncestorsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(configuration)], configuration, logger)
