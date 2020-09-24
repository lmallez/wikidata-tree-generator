#!/usr/bin/env python3
from .entity import Entity, Properties


class Character(Entity):
    PROPERTIES = [
        Properties.MOTHER,
        Properties.FATHER,
        Properties.CHILDREN,
        Properties.DATE_DEATH,
        Properties.DATE_BIRTH,
        Properties.FAMILY_NAME,
        Properties.GIVEN_NAME,
        Properties.IS_HUMAN,
        Properties.PLACE_BIRTH,
        Properties.PLACE_DEATH,
        Properties.SEX
    ]
