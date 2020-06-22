from wikidata.entity import Entity

from Config import Config
from Database import Database
from WikidataFetcher import WikidataFetcher
from entity_filler.property_fillers.PlaceBirthFiller import PlaceBirthFiller
from entity_filler.property_fillers.PlaceDeathFiller import PlaceDeathFiller
from logger.Logger import Logger
from models.CharacterEntity import Properties
from tree_builder.PlacerBuilder import PlaceBuilder


class EntityFiller:
    def __init__(self, config: Config, entity_database: Database, place_database: Database, wikidata: WikidataFetcher, place_builder: PlaceBuilder, logger: Logger):
        self.entity_database = entity_database
        self.config = config
        self.entity_filler = {
            # Properties.GIVEN_NAME: GivenNameFiller(wikidata),
            Properties.PLACE_BIRTH: PlaceBirthFiller(wikidata, place_database, place_builder, logger),
            Properties.PLACE_DEATH: PlaceDeathFiller(wikidata, place_database, place_builder, logger),
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
