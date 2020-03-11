#!/usr/bin/env python3
from wikidata.entity import EntityId

from models.CharacterEntity import Properties
from macros.WikidataProperties import Sex
from services.CharacterFetcherService import CharacterFetcherService
from services.ConfigService import ConfigService
from services.logger.LoggerService import LoggerService


class DescandantsTreeBuilderService:
    def __init__(self, fetcher: CharacterFetcherService, config: ConfigService, logger: LoggerService):
        self.fetcher = fetcher
        self.config = config
        self.logger = logger
        self.loads_entities = []

    def build_tree(self, entity_id: EntityId, prof=0, branch=0):
        if entity_id in self.loads_entities or prof > self.config.max_prof:
            return
        self.loads_entities.append(entity_id)
        character = self.fetcher.get(entity_id)
        self.logger.log("{:>5} | {:>3} {:>3} | {:>10} {}".format(len(self.loads_entities), prof, branch, character.id, character.get_property(Properties.LABEL)))
        if character.has_property(Properties.SEX):
            sex = character.get_property(Properties.SEX)
            if (sex == Sex.MALE and not self.config.load_men_child) or (sex == Sex.FEMALE and not self.config.load_women_child):
                return
        if character.has_property(Properties.CHILD_IDS):
            for child_id in character.get_property(Properties.CHILD_IDS):
                branch = branch + 1
                self.build_tree(child_id, prof+1, branch)
