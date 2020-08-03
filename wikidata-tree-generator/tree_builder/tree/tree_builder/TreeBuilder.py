#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger
from models.CharacterEntity import Properties, CharacterEntity
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader import Loader
from tree_builder.tree.tree_generator.CacheTreeGenerator import CacheTreeGenerator
from tree_builder.tree.tree_generator.TreeGenerator import TreeGenerator


class TreeBuilder:
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        self.fetcher = fetcher
        self.dispatcher = dispatcher
        self.loaders = loaders
        self.configuration = configuration
        self.logger = logger

    def compute(self, entity_id: EntityId) -> CharacterEntity:
        generator = (CacheTreeGenerator if self.configuration.branch_cache else TreeGenerator)(self.fetcher, self.dispatcher, self.loaders, self.configuration, self.logger)
        return generator.compute(entity_id)
