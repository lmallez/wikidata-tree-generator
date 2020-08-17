#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger
from models.CharacterEntity import Properties, CharacterEntity
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader import Loader


class TreeGenerator:
    def __init__(self, fetcher: CharacterFetcher, dispatcher: Dispatcher, loaders: [Loader], configuration: TreeConfiguration, logger: Logger):
        self.fetcher = fetcher
        self.dispatcher = dispatcher
        self.loaders = loaders
        self.configuration = configuration
        self.logger = logger

    def get_next_entities(self, entity_ids, depth=0):
        return entity_ids

    def compute(self, entity_id: EntityId, depth=0) -> CharacterEntity:
        character = self.fetcher.get(entity_id)
        if depth < self.configuration.generation_limit:
            entity_ids = []
            for loader in self.loaders:
                entity_ids += loader.load(character)
            self.dispatcher.compute(self.get_next_entities(entity_ids, depth), self.compute, depth + 1)
        return character
