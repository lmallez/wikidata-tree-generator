#!/usr/bin/env python3
from ..macros import PropertyTag
from ..models.entity import Entity


class Character(Entity):
    PROPERTIES = [
        PropertyTag.MOTHER,
        PropertyTag.FATHER,
        PropertyTag.CHILDREN,
        PropertyTag.DATE_DEATH,
        PropertyTag.DATE_BIRTH,
        PropertyTag.FAMILY_NAME,
        PropertyTag.GIVEN_NAME,
        PropertyTag.IS_HUMAN,
        PropertyTag.PLACE_BIRTH,
        PropertyTag.PLACE_DEATH,
        PropertyTag.SEX
    ]
