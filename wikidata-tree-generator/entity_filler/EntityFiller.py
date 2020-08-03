from wikidata.entity import Entity

from Database import Database
from entity_filler.property_fetcher.PropertyFetcher import PropertyFetcher
from entity_filler.property_fillers.FamilyNameFiller import FamilyNameFiller
from entity_filler.property_fillers.GivenNameFiller import GivenNameFiller
from entity_filler.property_fillers.PlaceBirthFiller import PlaceBirthFiller
from entity_filler.property_fillers.PlaceDeathFiller import PlaceDeathFiller
from logger.Logger import Logger
from models.CharacterEntity import Properties
from tree_builder.PlacerBuilder import PlaceBuilder


class EntityFiller:
    def __init__(self, properties: list, character_database: Database, property_fetcher: PropertyFetcher, place_builder: PlaceBuilder, logger: Logger):
        self.entity_database = character_database
        self.entity_filler = {
            Properties.FAMILY_NAME: FamilyNameFiller(property_fetcher, logger),
            Properties.GIVEN_NAME: GivenNameFiller(property_fetcher, logger),
            Properties.PLACE_BIRTH: PlaceBirthFiller(property_fetcher, place_builder, logger),
            Properties.PLACE_DEATH: PlaceDeathFiller(property_fetcher, place_builder, logger),
        }
        self.fillers = []
        self.properties = properties
        self.logger = logger
        self.__init()

    def __init(self):
        self.fillers = []
        for prop in self.properties:
            if prop not in self.entity_filler.keys():
                continue
            self.fillers.append(self.entity_filler[prop])

    def process_entity(self, entity: Entity):
        for filler in self.fillers:
            filler.process(entity)

    def process(self):
        for entity in self.entity_database.cache.values():
            self.process_entity(entity)
