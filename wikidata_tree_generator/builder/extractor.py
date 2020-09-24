#!/usr/bin/env python3
from typing import Dict, Callable

from wikidata_tree_generator.macros.character_properties import Property, PropertyToLoad, PropertyMeta, ExtractMethod
from wikidata_tree_generator.macros.wikidate_properties import wikidata_entities, Sex
from wikidata_tree_generator.models import Date
from wikidata_tree_generator.models.place import CoordinateLocation


class PropertyNotFoundException(BaseException):
    pass


def extract_property_is_human(wiki_properties):
    instance_of_ids = [instance_of_x['mainsnak']['datavalue']['value']['id'] for instance_of_x in wiki_properties]
    return wikidata_entities['human'] in instance_of_ids


sex_list = {
    wikidata_entities['male']: Sex.MALE,
    wikidata_entities['female']: Sex.FEMALE
}


def extract_property_sex(wiki_property):
    if not 'datavalue' in wiki_property['mainsnak']:
        raise PropertyNotFoundException()
    sex = wiki_property['mainsnak']['datavalue']['value']['id']
    if sex not in sex_list:
        return Sex.UNDEFINED
    return sex_list[sex]


def extract_property_date(wiki_property):
    if not 'datavalue' in wiki_property['mainsnak']:
        raise PropertyNotFoundException()
    return Date(
        wiki_property['mainsnak']['datavalue']['value']['time'],
        wiki_property['mainsnak']['datavalue']['value']['precision']
    )


def extract_property_coordinate(wiki_property):
    if not 'datavalue' in wiki_property['mainsnak']:
        raise PropertyNotFoundException()
    coordinates = wiki_property['mainsnak']['datavalue']['value']
    if not 'latitude' in coordinates or not 'longitude' in coordinates:
        raise PropertyNotFoundException()
    return CoordinateLocation(coordinates['latitude'], coordinates['longitude'])


def extract_property_id(wiki_property):
    if not 'datavalue' in wiki_property['mainsnak']:
        raise PropertyNotFoundException()
    return wiki_property['mainsnak']['datavalue']['value']['id']


def extract_property(property_meta: PropertyMeta, wiki_property) -> Property:
    value = extract_property_methods[property_meta.extract_method](wiki_property)
    return Property(value) if not property_meta.to_load else PropertyToLoad(value)


extract_property_methods: Dict[ExtractMethod, Callable] = {
    ExtractMethod.ID: extract_property_id,
    ExtractMethod.DATE: extract_property_date,
    ExtractMethod.SEX: extract_property_sex,
    ExtractMethod.IS_HUMAN: extract_property_is_human,
    ExtractMethod.COORDINATES: extract_property_coordinate,
}
