#!/usr/bin/env python3
from wikidata_tree_generator.configuration import Configuration, TreeMethod, ExportFormat
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.tree_builder.tree.dispatcher import Dispatcher
from wikidata_tree_generator.wikidata_fetcher import WikidataFetcher
from wikidata_tree_generator.launcher import Launcher
from wikidata_tree_generator.entity_filler.entity_filler import EntityFiller
from wikidata_tree_generator.entity_filler.threaded_entity_filler import ThreadedEntityFiller
from wikidata_tree_generator.entity_filler.property_fetcher.cache_property_fetcher import CachePropertyFetcher
from wikidata_tree_generator.entity_filler.property_fetcher.property_fetcher import PropertyFetcher
from wikidata_tree_generator.export.gedcom_exporter import GedcomExporter
from wikidata_tree_generator.export.json_exporter import JsonExporter
from wikidata_tree_generator.logger.logger import Logger
from wikidata_tree_generator.entity_builder.character_buidler import CharacterBuilder
from wikidata_tree_generator.entity_builder.place_builder import PlaceBuilder
from wikidata_tree_generator.tree_builder.character_fetcher.cache_character_fetcher import CacheCharacterFetcher
from wikidata_tree_generator.tree_builder.character_fetcher.character_fetcher import CharacterFetcher
from wikidata_tree_generator.tree_builder.tree.dispatcher.threaded_dispatcher import ThreadedDispatcher
from wikidata_tree_generator.tree_builder.tree.tree_builder.ancestors_tree_builder import AncestorsTreeBuilder
from wikidata_tree_generator.tree_builder.tree.tree_builder.classic_tree_builder import ClassicTreeBuilder
from wikidata_tree_generator.tree_builder.tree.tree_builder.decendants_tree_builder import DescendantsTreeBuilder
from wikidata_tree_generator.tree_builder.tree.tree_builder.full_tree_builder import FullTreeBuilder


class LauncherCreator:
    __tree_builders = {
        TreeMethod.ANCESTORS: AncestorsTreeBuilder,
        TreeMethod.DESCENDANTS: DescendantsTreeBuilder,
        TreeMethod.FULL: FullTreeBuilder,
        TreeMethod.CLASSIC: ClassicTreeBuilder,
    }

    __exporters = {
        ExportFormat.GEDCOM: GedcomExporter,
        ExportFormat.JSON: JsonExporter,
    }

    def __init__(self, configuration: Configuration):
        self.logger = Logger()
        self.wikidata_fetcher = WikidataFetcher()
        self.character_database = Database()
        self.character_builder = CharacterBuilder(self.logger, configuration.properties)
        self.character_fetcher = (CacheCharacterFetcher if configuration.entity_cache else CharacterFetcher)(self.wikidata_fetcher, self.character_database, self.character_builder, self.logger)

        self.property_database = Database()
        self.place_builder = PlaceBuilder(self.logger)
        self.property_fetcher = (CachePropertyFetcher if configuration.entity_cache else PropertyFetcher)(self.wikidata_fetcher, self.property_database)

        self.dispatcher = None
        self.tree_builder = None
        self.entity_filler = None

        if not configuration.thread_configuration.enable:
            self.dispatcher = Dispatcher()
            self.entity_filler = EntityFiller(configuration.properties, self.character_database, self.property_fetcher, self.place_builder, self.logger)
        else:
            self.dispatcher = ThreadedDispatcher(configuration.thread_configuration.max_thread)
            self.entity_filler = ThreadedEntityFiller(configuration.properties, self.character_database, self.property_fetcher, self.place_builder, self.logger, configuration.thread_configuration)

        self.tree_builder = self.__tree_builders[configuration.tree_configuration.method](self.character_fetcher, configuration.tree_configuration, self.dispatcher, self.logger)

        self.exporter = self.__exporters[configuration.export_configuration.format](self.character_database, configuration.properties, configuration.export_configuration, self.logger)

    def get_launcher(self) -> Launcher:
        return Launcher(self.tree_builder, self.entity_filler, self.exporter)
