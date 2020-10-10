#!/usr/bin/env python3
from wikidata.entity import EntityId

from wikidata_tree_generator.builder.fetcher.character_fetcher import CharacterFetcher
from wikidata_tree_generator.configuration import TreeConfiguration
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import Character
from wikidata_tree_generator.tree_builder.dispatcher import Dispatcher
from wikidata_tree_generator.tree_builder.loader import Loader


class TreeGenerator:
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        self.fetcher = fetcher
        self.dispatcher = dispatcher
        self.loaders = loaders
        self.configuration = configuration
        self.logger = logger

    def get_next_entities(self, entity_ids: [EntityId]) -> [EntityId]:
        return entity_ids

    def compute(self, entity_id: EntityId, depth=0) -> Character:
        character = self.fetcher.get(entity_id)
        if depth < self.configuration.generation_limit:
            entity_ids = []
            for loader in self.loaders:
                entity_ids += loader.load(character)
            self.dispatcher.compute(self.get_next_entities(entity_ids), self.compute, depth + 1)
        return character
