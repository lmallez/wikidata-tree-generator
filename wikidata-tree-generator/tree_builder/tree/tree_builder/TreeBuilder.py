#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import Properties, CharacterEntity
from tree_builder.CharacterFetcher import CharacterFetcherService
from ConfigService import ConfigService
from tree_builder.tree.loader import Loader
from tree_builder.tree.dispatcher.Dispatcher import Dispatcher


class TreeBuilder:
    def __init__(self, fetcher: CharacterFetcherService, dispatcher: Dispatcher, loaders: [Loader], config: ConfigService):
        self.fetcher = fetcher
        self.dispatcher = dispatcher
        self.loaders = loaders
        self.config = config

    def print(self, prof, branch, character, start="", end=""):
        print("{}{:>3} {:>3} | {:>10} {}{}\n".format(
            start, prof, branch, character.id, character.get_property(Properties.LABEL), end), flush=True, end='')

    def compute(self, entity_id: EntityId, prof=0, branch=0) -> CharacterEntity:
        character = self.fetcher.get(entity_id)
        self.print(prof, branch, character)
        prof += 1
        if prof <= self.config.max_prof:
            entity_ids = []
            for loader in self.loaders:
                entity_ids += loader.load(character)
            not_entity_ids = list(filter(lambda x: self.fetcher.database.contains(x), entity_ids))
            entity_ids = list(filter(lambda x: not self.fetcher.database.contains(x), entity_ids))
            for not_id in not_entity_ids:
                entity = self.fetcher.database.get(not_id)
                self.print(prof, branch, entity, '\033[93m', '\033[0m')
            self.dispatcher.compute(entity_ids, self.compute, prof, branch)
        return character
