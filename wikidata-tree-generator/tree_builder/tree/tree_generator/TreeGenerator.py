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

    def print(self, prof, branch, character, color=None):
        self.logger.log(
            "{:>3} {:>3} | {:>10} {}".format(prof, branch, character.id, character[Properties.LABEL]), color
        )

    def get_next_entities(self, entity_ids, prof=0, branch=0):
        return entity_ids

    def compute(self, entity_id: EntityId, prof=0, branch=0) -> CharacterEntity:
        character = self.fetcher.get(entity_id)
        self.print(prof, branch, character)
        prof += 1
        if prof <= self.configuration.generation_limit:
            entity_ids = []
            for loader in self.loaders:
                entity_ids += loader.load(character)
            self.dispatcher.compute(self.get_next_entities(entity_ids, prof, branch), self.compute, prof, branch)
        return character
