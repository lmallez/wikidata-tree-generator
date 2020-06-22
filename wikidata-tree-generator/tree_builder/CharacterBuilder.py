#!/usr/bin/env python3
from typing import List

from wikidata.entity import EntityId, Entity

from logger.Logger import Logger
from macros.WikidataProperties import wikidata_entities, wikidata_properties, Sex
from models.CharacterEntity import CharacterEntity, Properties
from models.Date import Date
from tree_builder.Builder import Builder

sex_list = {
    wikidata_entities['male']: Sex.MALE,
    wikidata_entities['female']: Sex.FEMALE
}


class CharacterBuilder(Builder):
    def __init__(self, logger: Logger, properties: list):
        super().__init__(logger)
        self.properties = properties + [
            Properties.FATHER_ID,
            Properties.MOTHER_ID,
            Properties.CHILD_IDS,
        ]

    def build(self, entity: Entity) -> CharacterEntity:
        character = CharacterEntity()
        character.id = entity.id
        character[Properties.ID] = entity.id
        character[Properties.LABEL] = entity.label
        # TODO : use function pointer choose from array of properties
        fields = self.properties
        for field in fields:
            if field not in field_method.keys():
                self.logger.error("method {} not found".format(field))
            try:
                character[field] = field_method[field](self, entity)
            except:
                self.logger.error('{}: {} is impossible to get'.format(self.__class__.__name__, field))
        return character

    def get_is_human(self, entity: Entity) -> bool:
        instance_of = self.get_property(entity, wikidata_properties["instance_of"])
        if len(instance_of) == 0:
            self.logger.error('{}: {} -> is instance of nothing'.format(self.__class__.__name__, entity.id))
            return False
        instance_of_ids = [instance_of_x['mainsnak']['datavalue']['value']['id'] for instance_of_x in instance_of]
        if wikidata_entities['human'] not in instance_of_ids:
            self.logger.error('{}: {} -> is not human -> is {}'.format(self.__class__.__name__, entity.id,
                                                                       ", ".join(instance_of_ids)))
            return False
        return True

    def get_sex(self, entity: Entity) -> int:
        sex = self.get_property(entity, wikidata_properties["sex"])
        if len(sex) == 0:
            self.logger.error('{}: {} -> sex not specified'.format(self.__class__.__name__, entity.id))
            return Sex.UNDEFINED
        if len(sex) > 1:
            self.logger.error('{}: {} -> multiple sex specified'.format(self.__class__.__name__, entity.id))
        sex = sex[0]['mainsnak']['datavalue']['value']['id']
        if sex not in sex_list:
            self.logger.error('{}: {} -> sex {} unknown'.format(self.__class__.__name__, entity.id, sex))
            return Sex.UNDEFINED
        return sex_list[sex]

    def get_father_id(self, entity) -> EntityId:
        return self.__get_parent_id(entity, wikidata_properties["father"])

    def get_mother_id(self, entity) -> EntityId:
        return self.__get_parent_id(entity, wikidata_properties["mother"])

    def __get_parent_id(self, entity, property_id):
        parents = self.get_property(entity, property_id)
        parents_ids = [parent['mainsnak']['datavalue']['value']['id'] for parent in parents]
        # for parent in property:
        #     if 'datavalue' in parent['mainsnak']:
        #         parents_ids.append(parent['mainsnak']['datavalue']['value']['id'])
        if len(parents_ids) == 0:
            return None
        if len(parents_ids) > 1:
            self.logger.error('{}: {} -> has more than one parent -> {}'.format(self.__class__.__name__, entity.id,
                                                                                ", ".join(parents_ids)))
            # TODO : implement like this to get priority to already loaded entities + implements filter to select the father or manage multiple fathers
            # loads_parents = list(set(parents_ids).intersection(entity_cache))
            # return loads_parents[0] if len(loads_parents) > 0 else parents_ids[0]
        return parents_ids[0]

    def get_child_ids(self, entity) -> List[EntityId]:
        child_ids = []
        childs = self.get_property(entity, wikidata_properties["child"])
        for child in childs:
            # TODO : remove adoptive childs
            # if 'qualifiers' in child and wikidata_properties('type_of_kinship') in child['qualifiers']:
            #     if sum([1 if kinship['datavalue']['value']['id'] in [wikidata_entities('adopted')] else 0 for kinship in
            #             child['qualifiers'][wikidata_properties('type_of_kinship')]]) > 0:
            #         continue
            if 'datavalue' in child['mainsnak']:
                child_ids.append(child['mainsnak']['datavalue']['value']['id'])
        return child_ids

    def get_date_birth(self, entity: Entity) -> Date:
        return self.__get_date(entity, wikidata_properties['date_of_birth'])

    def get_date_death(self, entity: Entity) -> Date:
        return self.__get_date(entity, wikidata_properties['date_of_death'])

    def __get_date(self, entity: Entity, property_id: EntityId) -> Date:
        dates = self.get_property(entity, property_id)
        if len(dates) > 0:
            self.logger.error('{}: {} -> has multiple date {}'.format(self.__class__.__name__, entity.id, property_id))
        date = dates[0]
        if not 'datavalue' in date['mainsnak']:
            raise
        return Date(
            date['mainsnak']['datavalue']['value']['time'],
            date['mainsnak']['datavalue']['value']['precision']
        )

    def get_given_name(self, entity: Entity):
        return self.__get_name(entity, wikidata_properties['given_name'])

    def get_family_name(self, entity: Entity):
        return self.__get_name(entity, wikidata_properties['family_name'])

    def __get_name(self, entity: Entity, property_id: EntityId):
        given_names = self.get_property(entity, property_id)
        return [given_name['mainsnak']['datavalue']['value']['id'] for given_name in given_names]

    def get_place_birth(self, entity: Entity) -> EntityId:
        return self.__get_place(entity, wikidata_properties['place_of_birth'])

    def get_place_death(self, entity: Entity) -> EntityId:
        return self.__get_place(entity, wikidata_properties['place_of_death'])

    def __get_place(self, entity: Entity, property_id: EntityId):
        places = self.get_property(entity, property_id)
        if not places:
            raise
        # TODO : select right place
        return places[0]['mainsnak']['datavalue']['value']['id']


field_method = {
    Properties.SEX: CharacterBuilder.get_sex,
    Properties.IS_HUMAN: CharacterBuilder.get_is_human,
    Properties.MOTHER_ID: CharacterBuilder.get_mother_id,
    Properties.FATHER_ID: CharacterBuilder.get_father_id,
    Properties.CHILD_IDS: CharacterBuilder.get_child_ids,
    Properties.DATE_BIRTH: CharacterBuilder.get_date_birth,
    Properties.DATE_DEATH: CharacterBuilder.get_date_death,
    Properties.GIVEN_NAME: CharacterBuilder.get_given_name,
    Properties.FAMILY_NAME: CharacterBuilder.get_family_name,
    Properties.PLACE_BIRTH: CharacterBuilder.get_place_birth,
    Properties.PLACE_DEATH: CharacterBuilder.get_place_death,
}
