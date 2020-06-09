#!/usr/bin/env python3
from wikidata.entity import EntityId


class Properties:
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


class CharacterEntity(dict):
    id: EntityId

    def has_property(self, property_id: EntityId):
        return property_id in self.keys()

    def get_property(self, property_id: EntityId):
        if not self.has_property(property_id):
            raise
        return self[property_id]
