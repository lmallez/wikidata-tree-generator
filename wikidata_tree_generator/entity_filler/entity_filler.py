from wikidata.entity import Entity
from wikidata_tree_generator.database import Database
from wikidata_tree_generator.entity_builder import PlaceBuilder
from wikidata_tree_generator.entity_filler.property_fetcher import PropertyFetcher
from wikidata_tree_generator.entity_filler.property_fillers import FamilyNameFiller, GivenNameFiller, PlaceBirthFiller, \
    PlaceDeathFiller
from wikidata_tree_generator.logger import Logger
from wikidata_tree_generator.models.character import Properties


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
