#!/usr/bin/env python3
from models.CharacterEntity import Properties


class ConfigService:
    max_thread = 100

    load_fathers = True
    load_mothers = True

    load_men_child = True
    load_women_child = True

    export_women = True
    export_men = True

    max_prof = 6

    def get_character_fields(self):
        # TODO : generate this
        return [
            Properties.SEX,
            Properties.IS_HUMAN,
            Properties.FATHER_ID,
            Properties.MOTHER_ID,
            Properties.CHILD_IDS,
            Properties.DATE_DEATH,
            Properties.DATE_BIRTH,
            Properties.GIVEN_NAME,
            Properties.FAMILY_NAME,
            Properties.PLACE_BIRTH,
            Properties.PLACE_DEATH,
        ]

    def get_export_fields(self):
        # TODO : generate this
        return [
            Properties.SEX,
            Properties.DATE_DEATH,
            Properties.DATE_BIRTH,
            Properties.GIVEN_NAME,
            Properties.PLACE_BIRTH,
            Properties.PLACE_DEATH,
        ]
