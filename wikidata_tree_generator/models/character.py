#!/usr/bin/env python3
from enum import Enum
from wikidata.entity import EntityId


class Properties(Enum):
    ID = 'id'
    LABEL = 'label'
    SEX = 'sex'
    IS_HUMAN = 'is_human'
    MOTHER_ID = 'mother_id'
    FATHER_ID = 'father_id'
    CHILD_IDS = 'child_ids'
    DATE_BIRTH = 'date_birth'
    DATE_DEATH = 'date_death'
    GIVEN_NAME = 'given_name'
    FAMILY_NAME = 'family_name'
    PLACE_BIRTH = 'place_birth'
    PLACE_DEATH = 'place_death'


class CharacterException(BaseException):
    pass


class Character(dict):
    def __init__(self, entity_id: EntityId):
        super().__init__()
        self.id = entity_id

    def has_property(self, entity_property: Properties):
        return entity_property in self.keys()

    def get_property(self, entity_property: Properties):
        if not self.has_property(entity_property):
            raise CharacterException()
        return self[entity_property]

    def __repr__(self):
        return repr(self.__dict__)
