#!/usr/bin/env python3
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.tree_builder.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.tree.loader import AncestorsLoader, DescendantsLoader
from wikidata_tree_generator.tree_builder.tree.tree_builder import TreeBuilder


class FullTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(configuration), DescendantsLoader(configuration)], configuration, logger)
