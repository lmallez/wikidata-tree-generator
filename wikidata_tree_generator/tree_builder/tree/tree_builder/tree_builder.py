#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger, Color
from wikidata_tree_generator.models import Character
from wikidata_tree_generator.tree_builder.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.tree.loader import Loader
from wikidata_tree_generator.tree_builder.tree.tree_generator import TreeGenerator, CacheTreeGenerator


class TreeBuilder:
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        self.fetcher = fetcher
        self.dispatcher = dispatcher
        self.loaders = loaders
        self.configuration = configuration
        self.logger = logger

    def compute(self, entity_id: EntityId) -> Character:
        self.logger.log("{} : Start tree generation with a maximum depth of {}.".format(self.__class__.__name__, self.configuration.generation_limit), color=Color.HEADER)
        generator = (CacheTreeGenerator if self.configuration.branch_cache else TreeGenerator)(self.fetcher, self.dispatcher, self.loaders, self.configuration, self.logger)
        entity = generator.compute(entity_id)
        self.logger.log("{} : End of the generation of the tree, {} entities loaded".format(self.__class__.__name__, len(self.fetcher.database.cache)), color=Color.HEADER)
        return entity
