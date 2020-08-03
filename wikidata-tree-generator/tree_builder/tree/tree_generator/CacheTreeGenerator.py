#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger, Color
from models.CharacterEntity import CharacterEntity
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader import Loader
from tree_builder.tree.tree_generator.TreeGenerator import TreeGenerator


class CacheTreeGenerator(TreeGenerator):
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        super().__init__(fetcher, dispatcher, loaders, configuration, logger)
        self.entity_loaded = []

    def get_next_entities(self, entity_ids, prof=0):
        excluded = list(filter(lambda x: x in self.entity_loaded, entity_ids))
        for exclude in excluded:
            self.logger.log("{:>10}".format(exclude), Color.OKBLUE)
        return list(filter(lambda x: x not in self.entity_loaded, entity_ids))

    def compute(self, entity_id: EntityId, prof=0) -> CharacterEntity:
        self.entity_loaded.append(entity_id)
        return super().compute(entity_id, prof)
