#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from wikidata.entity import EntityId

from wikidata_tree_generator.macros.property import PropertyTag
from wikidata_tree_generator.macros.wikidata import wikidata_properties, Sex
from wikidata_tree_generator.models import Name, Date
from wikidata_tree_generator.models.character import Character
from wikidata_tree_generator.models.place import CoordinateLocation, Place


class ExtractType(Enum):
    ALL = 0
    SINGLE = 1
    MULTIPLE = 2


class ExtractMethod(Enum):
    ID = 0
    DATE = 1
    IS_HUMAN = 2
    SEX = 3
    COORDINATES = 4


@dataclass
class PropertyMeta:
    tag: PropertyTag
    wikidata_id: EntityId
    value_type: type
    extract_type: ExtractType
    extract_method: ExtractMethod
    to_load: bool = False
    value_multiple: bool = False


PropertyList = Dict[PropertyTag, PropertyMeta]

# TODO : check if extract type and extract method are compatible
# TODO : replace with a configuration file

character_property_metas: PropertyList = {
    PropertyTag.SEX: PropertyMeta(PropertyTag.SEX, wikidata_properties['sex'], Sex, ExtractType.SINGLE, ExtractMethod.SEX),
    PropertyTag.IS_HUMAN: PropertyMeta(PropertyTag.IS_HUMAN, wikidata_properties['instance_of'], bool, ExtractType.ALL, ExtractMethod.IS_HUMAN),
    PropertyTag.MOTHER: PropertyMeta(PropertyTag.MOTHER, wikidata_properties['mother'], Character, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    PropertyTag.FATHER: PropertyMeta(PropertyTag.FATHER, wikidata_properties['father'], Character, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    PropertyTag.CHILDREN: PropertyMeta(PropertyTag.CHILDREN, wikidata_properties['child'], Character, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    PropertyTag.DATE_BIRTH: PropertyMeta(PropertyTag.DATE_BIRTH, wikidata_properties['date_of_birth'], Date, ExtractType.SINGLE, ExtractMethod.DATE),
    PropertyTag.DATE_DEATH: PropertyMeta(PropertyTag.DATE_DEATH, wikidata_properties['date_of_death'], Date, ExtractType.SINGLE, ExtractMethod.DATE),
    PropertyTag.GIVEN_NAME: PropertyMeta(PropertyTag.GIVEN_NAME, wikidata_properties['given_name'], Name, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    PropertyTag.FAMILY_NAME: PropertyMeta(PropertyTag.FAMILY_NAME, wikidata_properties['family_name'], Name, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    PropertyTag.PLACE_BIRTH: PropertyMeta(PropertyTag.PLACE_BIRTH, wikidata_properties['place_of_birth'], Place, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    PropertyTag.PLACE_DEATH: PropertyMeta(PropertyTag.PLACE_DEATH, wikidata_properties['place_of_death'], Place, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
}

place_property_metas: PropertyList = {
    PropertyTag.COORDINATE_LOCATION: PropertyMeta(PropertyTag.COORDINATE_LOCATION, wikidata_properties['coordinate_location'], CoordinateLocation, ExtractType.SINGLE, ExtractMethod.COORDINATES)
}

name_property_metas: PropertyList = {
}

property_metas_by_type = {
    Name: name_property_metas,
    Place: place_property_metas,
    Character: character_property_metas,
}
