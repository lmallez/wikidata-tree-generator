from wikidata.entity import Entity

from entity_filler.property_fillers.PropertyFiller import PropertyFiller
from models import CharacterEntity
from models.CharacterEntity import Properties
from models.GivenName import GivenName


class GivenNameFiller(PropertyFiller):
    def print(self, entity: GivenName, color=None):
        self.logger.log('Place | {} {}'.format(entity.id, entity.given), color)

    def convert(self, entity: Entity) -> GivenName:
        return GivenName(entity.id, str(entity.label))

    def process(self, entity: CharacterEntity):
        if Properties.GIVEN_NAME not in entity.keys():
            return
        given_names = entity[Properties.GIVEN_NAME]
        entity[Properties.GIVEN_NAME] = [self.get_entity(given_name) for given_name in given_names]
