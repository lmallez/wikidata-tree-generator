#!/usr/bin/env python3
from typing import List

from wikidata.entity import EntityId, Entity

from models.Date import Date
from services.ConfigService import ConfigService
from services.logger.LoggerService import LoggerService
from macros.WikidataProperties import wikidata_entities, wikidata_properties, Sex
from models.CharacterEntity import CharacterEntity, Properties

sex_list = {
    wikidata_entities['male']: Sex.MALE,
    wikidata_entities['female']: Sex.FEMALE
}


class CharacterBuilderService:
    def __init__(self, logger: LoggerService, config: ConfigService):
        self.logger = logger
        self.config = config

    def build_character(self, entity: Entity) -> CharacterEntity:
        character = CharacterEntity()
        character.id = entity.id
        character[Properties.ID] = entity.id
        character[Properties.LABEL] = entity.label
        # TODO : use function pointer choose from array of properties
        fields = self.config.get_character_fields()
        for field in fields:
            if field not in field_method.keys():
                self.logger.log("method {} not found".format(field))
            try:
                character[field] = field_method[field](self, entity)
            except:
                self.logger.log('{}: {} is impossible to get'.format(self.__class__.__name__, field))
        return character

    def get_is_human(self, entity: Entity) -> bool:
        instance_of = self.__get_property(entity, wikidata_properties["instance_of"])
        if len(instance_of) == 0:
            self.logger.log('{}: {} -> is instance of nothing'.format(self.__class__.__name__, entity.id))
            return False
        instance_of_ids = [instance_of_x['mainsnak']['datavalue']['value']['id'] for instance_of_x in instance_of]
        if wikidata_entities['human'] not in instance_of_ids:
            self.logger.log('{}: {} -> is not human -> is {}'.format(self.__class__.__name__, entity.id, ", ".join(instance_of_ids)))
            return False
        return True

    def get_sex(self, entity: Entity) -> int:
        sex = self.__get_property(entity, wikidata_properties["sex"])
        if len(sex) == 0:
            self.logger.log('{}: {} -> sex not specified'.format(self.__class__.__name__, entity.id))
            return Sex.UNDEFINED
        if len(sex) > 1:
            self.logger.log('{}: {} -> multiple sex specified'.format(self.__class__.__name__, entity.id))
        sex = sex[0]['mainsnak']['datavalue']['value']['id']
        if sex not in sex_list:
            self.logger.log('{}: {} -> sex {} unknown'.format(self.__class__.__name__, entity.id, sex))
            return Sex.UNDEFINED
        return sex_list[sex]

    def get_father_id(self, entity) -> EntityId:
        return self.__get_parent_id(entity, wikidata_properties["father"])

    def get_mother_id(self, entity) -> EntityId:
        return self.__get_parent_id(entity, wikidata_properties["mother"])

    def __get_parent_id(self, entity, property_id):
        property = self.__get_property(entity, property_id)
        parents_ids = [parent['mainsnak']['datavalue']['value']['id'] for parent in property]
        # for parent in property:
        #     if 'datavalue' in parent['mainsnak']:
        #         parents_ids.append(parent['mainsnak']['datavalue']['value']['id'])
        if len(parents_ids) == 0:
            return None
        if len(parents_ids) > 1:
            self.logger.log('{}: {} -> has more than one parent -> {}'.format(self.__class__.__name__, entity.id, ", ".join(parents_ids)))
            # TODO : implement like this to get priority to already loaded entities + implements filter to select the father or manage multiple fathers
            # loads_parents = list(set(parents_ids).intersection(entity_cache))
            # return loads_parents[0] if len(loads_parents) > 0 else parents_ids[0]
        return parents_ids[0]

    def get_child_ids(self, entity) -> List[EntityId]:
        child_ids = []
        childs = self.__get_property(entity, wikidata_properties["child"])
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
        dates = self.__get_property(entity, property_id)
        if len(dates) > 0:
            self.logger.log('{}: {} -> has multiple date {}'.format(self.__class__.__name__, entity.id, property_id))
        date = dates[0]
        if not 'datavalue' in date['mainsnak']:
            raise
        return Date(
            date['mainsnak']['datavalue']['value']['time'],
            date['mainsnak']['datavalue']['value']['precision']
        )

    def __get_property(self, entity: Entity, property_id: EntityId):
        if property_id not in entity.data['claims']:
            self.logger.log('{}: {} -> property {} not found'.format(self.__class__.__name__, property_id, entity.id))
            raise
        return entity.data['claims'][property_id]


field_method = {
    Properties.SEX: CharacterBuilderService.get_sex,
    Properties.IS_HUMAN: CharacterBuilderService.get_is_human,
    Properties.MOTHER_ID: CharacterBuilderService.get_mother_id,
    Properties.FATHER_ID: CharacterBuilderService.get_father_id,
    Properties.CHILD_IDS: CharacterBuilderService.get_child_ids,
    Properties.DATE_BIRTH: CharacterBuilderService.get_date_birth,
    Properties.DATE_DEATH: CharacterBuilderService.get_date_death,
}
