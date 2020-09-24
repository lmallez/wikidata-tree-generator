#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum

from wikidata.entity import EntityId

from wikidata_tree_generator.macros.wikidate_properties import wikidata_properties, Sex
from wikidata_tree_generator.models import Properties, Date, Name, Place
from wikidata_tree_generator.models.character import Character
from wikidata_tree_generator.models.place import CoordinateLocation


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
    name: Properties
    wikidata_id: EntityId
    value_type: type
    extract_type: ExtractType
    extract_method: ExtractMethod
    to_load: bool = False
    value_multiple: bool = False


# TODO : check if extract type and extract method are compatible
# TODO : replace with a configuration file
character_property_metas = {
    Properties.SEX: PropertyMeta(Properties.SEX, wikidata_properties['sex'], Sex, ExtractType.SINGLE, ExtractMethod.SEX),
    Properties.IS_HUMAN: PropertyMeta(Properties.IS_HUMAN, wikidata_properties['instance_of'], bool, ExtractType.ALL, ExtractMethod.IS_HUMAN),
    Properties.MOTHER: PropertyMeta(Properties.MOTHER, wikidata_properties['mother'], Character, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    Properties.FATHER: PropertyMeta(Properties.FATHER, wikidata_properties['father'], Character, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    Properties.CHILDREN: PropertyMeta(Properties.CHILDREN, wikidata_properties['child'], Character, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    Properties.DATE_BIRTH: PropertyMeta(Properties.DATE_BIRTH, wikidata_properties['date_of_birth'], Date, ExtractType.SINGLE, ExtractMethod.DATE),
    Properties.DATE_DEATH: PropertyMeta(Properties.DATE_DEATH, wikidata_properties['date_of_death'], Date, ExtractType.SINGLE, ExtractMethod.DATE),
    Properties.GIVEN_NAME: PropertyMeta(Properties.GIVEN_NAME, wikidata_properties['given_name'], Name, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    Properties.FAMILY_NAME: PropertyMeta(Properties.FAMILY_NAME, wikidata_properties['family_name'], Name, ExtractType.MULTIPLE, ExtractMethod.ID, to_load=True, value_multiple=True),
    Properties.PLACE_BIRTH: PropertyMeta(Properties.PLACE_BIRTH, wikidata_properties['place_of_birth'], Place, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
    Properties.PLACE_DEATH: PropertyMeta(Properties.PLACE_DEATH, wikidata_properties['place_of_death'], Place, ExtractType.SINGLE, ExtractMethod.ID, to_load=True),
}

place_property_metas = {
    Properties.COORDINATE_LOCATION: PropertyMeta(Properties.COORDINATE_LOCATION, wikidata_properties['coordinate_location'], CoordinateLocation, ExtractType.SINGLE, ExtractMethod.COORDINATES)
}

name_property_metas = {
}

property_metas_by_type = {
    Name: name_property_metas,
    Place: place_property_metas,
    Character: character_property_metas,
}


@dataclass
class Property:
    value: object
    to_load = False
    sources = None


@dataclass
class PropertyToLoad:
    loader: EntityId
    value: object = None
    to_load = True
