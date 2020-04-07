#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import Properties
from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.tree.loader.AncestorsLoader import AncestorsLoader
from services.tree.dispatcher.Dispatcher import Dispatcher
from services.tree.tree_builder.TreeBuilder import TreeBuilder


class AncestorsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcherService, config: ConfigService, dispatcher: Dispatcher):
        super().__init__(fetcher, dispatcher, [AncestorsLoader(config)], config)
