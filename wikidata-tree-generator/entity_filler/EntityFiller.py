from wikidata.entity import Entity

from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.fillers.GivenNameFiller import GivenNameFiller
from models.CharacterEntity import Properties
from ConfigService import ConfigService


class EntityFiller:
    def __init__(self, config: ConfigService, entity_database: Database, wikidata: WikidataFetcher):
        self.entity_database = entity_database
        self.config = config
        self.entity_filler = {
            Properties.GIVEN_NAME: GivenNameFiller(wikidata)
        }
        self.fillers = []
        self.__init()

    def __init(self):
        self.fillers = []
        for prop in self.config.get_character_fields():
            if prop not in self.entity_filler.keys():
                continue
            self.fillers.append(self.entity_filler[prop])

    def process_entity(self, entity: Entity):
        for filler in self.fillers:
            filler.process(entity)

    def process(self):
        for entity in self.entity_database.cache.values():
            self.process_entity(entity)