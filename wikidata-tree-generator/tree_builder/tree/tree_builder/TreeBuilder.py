#!/usr/bin/env python3
from wikidata.entity import EntityId

from Configuration import TreeConfiguration
from logger.Logger import Logger, Color
from models.CharacterEntity import Properties, CharacterEntity
from tree_builder.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher
from tree_builder.tree.loader import Loader


class TreeBuilder:
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

    def compute(self, entity_id: EntityId, prof=0, branch=0) -> CharacterEntity:
        character = self.fetcher.get(entity_id)
        self.print(prof, branch, character)
        prof += 1
        if prof <= self.configuration.generation_limit:
            entity_ids = []
            for loader in self.loaders:
                entity_ids += loader.load(character)
            not_entity_ids = list(filter(lambda x: self.fetcher.database.contains(x), entity_ids))
            entity_ids = list(filter(lambda x: not self.fetcher.database.contains(x), entity_ids))
            for not_id in not_entity_ids:
                entity = self.fetcher.database.get(not_id)
                self.print(prof, branch, entity, Color.OKGREEN)
            self.dispatcher.compute(entity_ids, self.compute, prof, branch)
        return character
