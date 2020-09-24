#!/usr/bin/env python3
from wikidata_tree_generator.macros.property import PropertyTag


json_property_tag_str = {
    PropertyTag.ID: 'id',
    PropertyTag.LABEL: 'label',
    PropertyTag.SEX: 'sex',
    PropertyTag.IS_HUMAN: 'is_human',
    PropertyTag.MOTHER: 'mother',
    PropertyTag.FATHER: 'father',
    PropertyTag.CHILDREN: 'children',
    PropertyTag.DATE_BIRTH: 'date_birth',
    PropertyTag.DATE_DEATH: 'date_death',
    PropertyTag.GIVEN_NAME: 'given_name',
    PropertyTag.FAMILY_NAME: 'family_name',
    PropertyTag.PLACE_BIRTH: 'place_birth',
    PropertyTag.PLACE_DEATH: 'place_death',
    PropertyTag.COORDINATE_LOCATION: 'coordinate_location',
}
