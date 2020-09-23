#!/usr/bin/env python3
from wikidata.entity import EntityId
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.entity_builder import CharacterBuilder
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models import CharacterEntity, Properties
from wikidata_tree_generator.wikidata_fetcher import WikidataFetcher


class CharacterFetcher:
    def __init__(self, wikidata: WikidataFetcher, database: Database, builder: CharacterBuilder, logger: Logger):
        self.wikidata = wikidata
        self.database = database
        self.builder = builder
        self.logger = logger

    def print(self, entity_id: EntityId, character: CharacterEntity, color=None):
        self.logger.log("{:>10} {}".format(entity_id, character[Properties.LABEL]), color)

    def get(self, entity_id: EntityId) -> CharacterEntity:
        character = self.builder.build(self.wikidata.get(entity_id))
        self.database.set(entity_id, character)
        self.print(entity_id, character)
        return character