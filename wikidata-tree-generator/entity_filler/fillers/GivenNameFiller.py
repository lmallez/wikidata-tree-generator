from wikidata.entity import Entity

from Database import Database
from WikidataFetcher import WikidataFetcher
from models.CharacterEntity import Properties


class GivenNameFiller:
    def __init__(self, fetcher: WikidataFetcher):
        self.wikidata = fetcher
        self.database = Database()

    def extract(self, entity):
        return entity.label

    def get_given_name(self, given_name_id):
        if self.database.contains(given_name_id):
            return self.database.get(given_name_id)
        wikidata_entity = self.wikidata.get(given_name_id)
        # entity = self.extract(wikidata_entity)
        self.database.add(given_name_id, wikidata_entity)
        return wikidata_entity

    def process(self, entity: Entity):
        if Properties.GIVEN_NAME not in entity.keys():
            return
        given_names = entity[Properties.GIVEN_NAME]
        entity[Properties.GIVEN_NAME] = [self.get_given_name(given_name) for given_name in given_names]
