from wikidata.entity import Entity

from Database import Database
from WikidataFetcher import WikidataFetcher
from models import CharacterEntity
from models.CharacterEntity import Properties
from models.GivenName import GivenName


class GivenNameFiller:
    def __init__(self, fetcher: WikidataFetcher):
        self.wikidata = fetcher
        self.database = Database()

    def print(self, given_name: GivenName, start="", end=""):
        print("{}Given | {:>10} {}{}\n".format(
            start, given_name.id, given_name.given, end), flush=True, end='')

    def convert(self, entity: Entity) -> GivenName:
        return GivenName(entity.id, str(entity.label))

    def get_given_name(self, given_name_id):
        if self.database.contains(given_name_id):
            place = self.database.get(given_name_id)
            self.print(place, '\033[93m', '\033[0m')
            return place
        wikidata_entity = self.convert(self.wikidata.get(given_name_id))
        if not self.database.contains(given_name_id):
            self.database.add(given_name_id, wikidata_entity)
        else:
            place = self.database.get(given_name_id)
            self.print(place, '\033[94m', '\033[0m')
            return place
        self.print(wikidata_entity)
        return wikidata_entity

    def process(self, entity: CharacterEntity):
        if Properties.GIVEN_NAME not in entity.keys():
            return
        given_names = entity[Properties.GIVEN_NAME]
        entity[Properties.GIVEN_NAME] = [self.get_given_name(given_name) for given_name in given_names]
