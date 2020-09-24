#!/usr/bin/env python3
from dataclasses import field, dataclass
from enum import Enum

from wikidata.entity import EntityId


class Properties(Enum):
    ID = 'id'
    LABEL = 'label'
    SEX = 'sex'
    IS_HUMAN = 'is_human'
    MOTHER = 'mother_id'
    FATHER = 'father_id'
    CHILDREN = 'child_ids'
    DATE_BIRTH = 'date_birth'
    DATE_DEATH = 'date_death'
    GIVEN_NAME = 'given_name'
    FAMILY_NAME = 'family_name'
    PLACE_BIRTH = 'place_birth'
    PLACE_DEATH = 'place_death'
    COORDINATE_LOCATION = 'coordinate_location'


class EntityException(BaseException):
    pass


@dataclass
class Entity:
    id: EntityId
    label: str
    properties: dict = field(default_factory=dict)
    PROPERTIES = []

    def has_property(self, entity_property: Properties):
        return entity_property in self.properties.keys()

    def get_property(self, entity_property: Properties):
        if not self.has_property(entity_property):
            raise EntityException()
        return self.properties[entity_property]
