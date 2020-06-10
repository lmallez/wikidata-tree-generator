#!/usr/bin/env python3
from entity_filler.EntityFiller import EntityFiller
from entity_filler.ThreadedEntityFiller import ThreadedEntityFiller
from tree_builder.CharacterFetcher import CharacterFetcherService
from ConfigService import ConfigService
from Database import Database
from export.GedcomExportService import GedcomExportService
from logger.LoggerService import LoggerService
from WikidataFetcher import WikidataFetcher
from tree_builder.CharacterBuilder import CharacterBuilder
from tree_builder.PlacerBuilder import PlaceBuilder
from tree_builder.tree.dispatcher.ThreadedDispatcher import ThreadedDispatcher
from tree_builder.tree.tree_builder.AncestorsTreeBuilder import AncestorsTreeBuilder
from tree_builder.tree.tree_builder.ClassicTreeBuilder import ClassicTreeBuilder
from tree_builder.tree.tree_builder.DescandantsTreeBuilder import DescendantsTreeBuilder
from tree_builder.tree.tree_builder.FullTreeBuilder import FullTreeBuilder


class MainModule:
    def __init__(self):
        self.logger = LoggerService()
        self.config = ConfigService()
        self.wikidata_fetcher = WikidataFetcher()
        self.character_database = Database()
        self.character_builder = CharacterBuilder(self.logger, self.config)
        self.place_database = Database()
        self.place_builder = PlaceBuilder(self.logger)

        self.fetcher = CharacterFetcherService(self.wikidata_fetcher, self.character_database, self.character_builder)

        # self.dispatcher = BasicDispatcher()
        self.dispatcher = ThreadedDispatcher(self.config.max_thread)

        self.ancestors_tree_builder = AncestorsTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.descandants_tree_builder = DescendantsTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.full_tree_builder = FullTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.classic_tree_builder = ClassicTreeBuilder(self.ancestors_tree_builder, self.descandants_tree_builder)

        self.entity_filler = ThreadedEntityFiller(self.config, self.character_database, self.place_database, self.wikidata_fetcher, self.place_builder)

        self.exporter = GedcomExportService(self.character_database, self.config, self.logger)
