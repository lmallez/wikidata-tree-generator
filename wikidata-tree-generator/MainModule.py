#!/usr/bin/env python3
from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.DatabaseService import DatabaseService
from services.export.GedcomExportService import GedcomExportService
from services.logger.LoggerService import LoggerService
from services.WikidataFetcherService import WikidataFetcherService
from services.CharacterBuilderService import CharacterBuilderService
from services.tree.dispatcher.ThreadedDispatcher import ThreadedDispatcher
from services.tree.tree_builder.AncestorsTreeBuilder import AncestorsTreeBuilder
from services.tree.tree_builder.ClassicTreeBuilder import ClassicTreeBuilder
from services.tree.tree_builder.DescandantsTreeBuilder import DescendantsTreeBuilder
from services.tree.tree_builder.FullTreeBuilder import FullTreeBuilder


class MainModule:
    def __init__(self):
        self.logger = LoggerService()
        self.config = ConfigService()
        self.wikidata_fetcher = WikidataFetcherService()
        self.database = DatabaseService()
        self.character_builder = CharacterBuilderService(self.logger, self.config)

        self.fetcher = CharacterFetcherService(self.wikidata_fetcher, self.database, self.character_builder)

        # self.dispatcher = BasicDispatcher()
        self.dispatcher = ThreadedDispatcher(self.config.max_thread)

        self.ancestors_tree_builder = AncestorsTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.descandants_tree_builder = DescendantsTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.full_tree_builder = FullTreeBuilder(self.fetcher, self.config, self.dispatcher)
        self.classic_tree_builder = ClassicTreeBuilder(self.ancestors_tree_builder, self.descandants_tree_builder)

        self.exporter = GedcomExportService(self.database, self.config, self.logger)
