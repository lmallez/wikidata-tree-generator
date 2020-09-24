#!/usr/bin/env python3
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.builder.fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.loader import DescendantsLoader
from .tree_builder import TreeBuilder


class DescendantsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcher, configuration: TreeConfiguration, dispatcher: Dispatcher, logger: Logger):
        super().__init__(fetcher, dispatcher, [DescendantsLoader(configuration)], configuration, logger)
