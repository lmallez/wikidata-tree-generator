#!/usr/bin/env python3
from enum import Enum


class PropertyTag(Enum):
    ID = 'id'
    LABEL = 'label'
    SEX = 'sex'
    IS_HUMAN = 'is_human'
    MOTHER = 'mother'
    FATHER = 'father'
    CHILDREN = 'children'
    DATE_BIRTH = 'date_birth'
    DATE_DEATH = 'date_death'
    GIVEN_NAME = 'given_name'
    FAMILY_NAME = 'family_name'
    PLACE_BIRTH = 'place_birth'
    PLACE_DEATH = 'place_death'
    COORDINATE_LOCATION = 'coordinate_location'
