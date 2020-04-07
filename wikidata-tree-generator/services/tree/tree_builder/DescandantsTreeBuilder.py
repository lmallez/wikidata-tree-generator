#!/usr/bin/env python3
from wikidata.entity import EntityId

from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.tree.loader.DescendantsLoader import DescendantsLoader
from services.tree.dispatcher.Dispatcher import Dispatcher
from services.tree.tree_builder.TreeBuilder import TreeBuilder


class DescendantsTreeBuilder(TreeBuilder):
    def __init__(self, fetcher: CharacterFetcherService, config: ConfigService, dispatcher: Dispatcher):
        super().__init__(fetcher, dispatcher, [DescendantsLoader(config)], config)
