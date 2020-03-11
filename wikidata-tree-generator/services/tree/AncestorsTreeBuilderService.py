#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import Properties
from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.logger.LoggerService import LoggerService


class AncestorsTreeBuilderService:
    def __init__(self, fetcher: CharacterFetcherService, config: ConfigService, logger: LoggerService):
        self.fetcher = fetcher
        self.config = config
        self.logger = logger
        self.loads_entities = []

    def build_tree(self, entity_id: EntityId, prof=0, branch=0):
        if entity_id in self.loads_entities or prof < -self.config.max_prof:
            return
        self.loads_entities.append(entity_id)
        character = self.fetcher.get(entity_id)
        self.logger.log("{:>5} | {:>3} {:>3} | {:>10} {}".format(len(self.loads_entities), prof, branch, character.id, character.get_property(Properties.LABEL)))
        if self.config.load_fathers and character.has_property(Properties.FATHER_ID):
            self.build_tree(character.get_property(Properties.FATHER_ID), prof-1, branch)
            branch = branch+1
        if self.config.load_mothers and character.has_property(Properties.MOTHER_ID):
            self.build_tree(character.get_property(Properties.MOTHER_ID), prof-1, branch)
