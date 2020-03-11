#!/usr/bin/env python3
from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.DatabaseService import DatabaseService
from services.export.GedcomExportService import GedcomExportService
from services.logger.LoggerService import LoggerService
from services.WikidataFetcherService import WikidataFetcherService
from services.CharacterBuilderService import CharacterBuilderService
from services.tree.AncestorsTreeBuilderService import AncestorsTreeBuilderService
from services.tree.DescandantsTreeBuilderService import DescandantsTreeBuilderService
from services.tree.TotalTreeBuilderService import TotalTreeBuilderService
from services.tree.TreeBuilderService import TreeBuilderService


class MainModule:
    def __init__(self):
        self.logger = LoggerService()
        self.config = ConfigService()
        self.wikidata_fetcher = WikidataFetcherService()
        self.database = DatabaseService()
        self.character_builder = CharacterBuilderService(self.logger, self.config)
        self.character_fetch = CharacterFetcherService(self.wikidata_fetcher, self.database, self.character_builder)
        self.a_tree_builder = AncestorsTreeBuilderService(self.character_fetch, self.config, self.logger)
        self.d_tree_builder = DescandantsTreeBuilderService(self.character_fetch, self.config, self.logger)
        self.tree_builder = TreeBuilderService(self.character_fetch, self.a_tree_builder, self.d_tree_builder)
        self.t_tree_builder = TotalTreeBuilderService(self.character_fetch, self.config, self.logger)
        self.gedcom_exporter = GedcomExportService(self.database, self.config, self.logger)
