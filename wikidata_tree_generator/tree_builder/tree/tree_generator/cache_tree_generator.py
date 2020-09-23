#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger, Color
from wikidata_tree_generator.models import CharacterEntity
from wikidata_tree_generator.tree_builder.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.tree.loader import Loader
from wikidata_tree_generator.tree_builder.tree.tree_generator import TreeGenerator


class CacheTreeGenerator(TreeGenerator):
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        super().__init__(fetcher, dispatcher, loaders, configuration, logger)
        self.entity_loaded = []

    def get_next_entities(self, entity_ids, depth=0):
        excluded = list(filter(lambda x: x in self.entity_loaded, entity_ids))
        for exclude in excluded:
            self.logger.log("{:>10}".format(exclude), Color.OKBLUE)
        return list(filter(lambda x: x not in self.entity_loaded, entity_ids))

    def compute(self, entity_id: EntityId, depth=0) -> CharacterEntity:
        self.entity_loaded.append(entity_id)
        return super().compute(entity_id, depth)
