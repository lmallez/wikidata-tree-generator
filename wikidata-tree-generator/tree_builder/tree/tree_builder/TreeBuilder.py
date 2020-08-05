#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger, Color
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
        self.logger.log("{} : Start tree generation with a maximum depth of {}.".format(self.__class__.__name__, self.configuration.generation_limit), color=Color.HEADER)
        generator = (CacheTreeGenerator if self.configuration.branch_cache else TreeGenerator)(self.fetcher, self.dispatcher, self.loaders, self.configuration, self.logger)
        entity = generator.compute(entity_id)
        self.logger.log("{} : End of the generation of the tree, {} entities loaded".format(self.__class__.__name__, len(self.fetcher.database.cache)), color=Color.HEADER)
        return entity
