#!/usr/bin/env python3
from Configuration import Configuration, TreeMethod, ExportFormat
from Database import Database
from WikidataFetcher import WikidataFetcher
from WikidataTreeGenerator import WikidataTreeGenerator
from entity_filler.EntityFiller import EntityFiller
from entity_filler.ThreadedEntityFiller import ThreadedEntityFiller
from entity_filler.property_fetcher.CachePropertyFetcher import CachePropertyFetcher
from entity_filler.property_fetcher.PropertyFetcher import PropertyFetcher
from export.GedcomExporter import GedcomExporter
from export.JsonExporter import JsonExporter
from logger.Logger import Logger
from tree_builder.CharacterBuilder import CharacterBuilder
from tree_builder.PlacerBuilder import PlaceBuilder
from tree_builder.character_fetcher.CacheCharacterFetcher import CacheCharacterFetcher
from tree_builder.character_fetcher.CharacterFetcher import CharacterFetcher
from tree_builder.tree.dispatcher.BasicDispatcher import BasicDispatcher
from tree_builder.tree.dispatcher.ThreadedDispatcher import ThreadedDispatcher
from tree_builder.tree.tree_builder.AncestorsTreeBuilder import AncestorsTreeBuilder
from tree_builder.tree.tree_builder.ClassicTreeBuilder import ClassicTreeBuilder
from tree_builder.tree.tree_builder.DescandantsTreeBuilder import DescendantsTreeBuilder
from tree_builder.tree.tree_builder.FullTreeBuilder import FullTreeBuilder


class MainModule:
    __tree_builders = {
        TreeMethod.ANCESTORS: AncestorsTreeBuilder,
        TreeMethod.DESCENDANTS: DescendantsTreeBuilder,
        TreeMethod.FULL: FullTreeBuilder,
        TreeMethod.CLASSIC: ClassicTreeBuilder,
    }

    __exporter = {
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
            self.dispatcher = BasicDispatcher()
            self.entity_filler = EntityFiller(configuration.properties, self.character_database, self.property_fetcher, self.place_builder, self.logger)
        else:
            self.dispatcher = ThreadedDispatcher(configuration.thread_configuration.max_thread)
            self.entity_filler = ThreadedEntityFiller(configuration.properties, self.character_database, self.property_fetcher, self.place_builder, self.logger, configuration.thread_configuration)

        self.tree_builder = self.__tree_builders[configuration.tree_configuration.method](self.character_fetcher, configuration.tree_configuration, self.dispatcher, self.logger)

        self.exporter = self.__exporter[configuration.export_configuration.format](self.character_database, configuration.properties, configuration.export_configuration, self.logger)

    def get_generator(self) -> WikidataTreeGenerator:
        return WikidataTreeGenerator(self.tree_builder, self.entity_filler, self.exporter)
